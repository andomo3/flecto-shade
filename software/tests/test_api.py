"""Tests for the persistent zone backend.

The engine holds no rules of its own, so the sharpest test here is the one that runs it
against package H1's committed simulation for the demo day and asserts the same hours
come back. The rest cover what the API is for: the four-zone limit, immutable
configuration revisions, override expiry and idempotency, optimistic concurrency, the
controlled metric registry, and the structured errors the console has to explain.
"""

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
API_DIR = REPO_ROOT / "software" / "api"
sys.path.insert(0, str(API_DIR))

from flecto import engine, metrics, seed, store, weather  # noqa: E402
from flecto.app import Request, dispatch  # noqa: E402

LOCAL_TZ = ZoneInfo("America/New_York")
DEMO_DATE = "2023-06-10"
STORM_HOUR = 14          # local, the one hour of the demo day that rains in daylight


@pytest.fixture
def db_path(tmp_path):
    """One file, opened fresh per request, the way a serverless invocation does."""
    path = tmp_path / "flecto.db"
    handle = store.open_database(path)
    seed.seed_site(handle)
    handle.close()
    return path


@pytest.fixture
def db(db_path):
    handle = store.open_database(db_path, auto_migrate=False)
    yield handle
    handle.close()


@pytest.fixture
def call(db_path):
    def send(method, path, body=None, query=None, headers=None):
        payload = None if body is None else json.dumps(body).encode("utf-8")
        request = Request(method, path, query or {}, payload, headers or {})
        return dispatch(request,
                        db_factory=lambda: store.open_database(db_path, auto_migrate=False))
    return send


@pytest.fixture
def site_zones(call):
    return call("GET", "/api/sites/boston-demo/zones").body["zones"]


def zone_by_letter(zones, letter):
    return next(zone for zone in zones if zone["letter"] == letter)


NEW_ZONE = {
    "name": "Gerbera trial bed",
    "crop_name": "Gerbera",
    "light_rule": "dli",
    "light_target": 10.0,
    "soil_request_below_mm": 28.0,
    "rain_ok": True,
    "kc": 1.0,
    "note": "Modelled fourth zone, added by the grower.",
}


# ----------------------------------------------------------- the engine is H1's rules

def test_the_engine_reproduces_package_h1_for_the_demo_day(db):
    """The API derives no physics. Given H1's inputs it must give H1's output back.

    These values were computed by package H1 from the real 2023 data, before this API
    existed. If this ever fails, the API has drifted and the API is what is wrong.
    """
    day = weather.load_day()
    hours = weather.hours_from(day)

    stamps = set()
    with open(REPO_ROOT / "data" / "processed" / "weather-boston.csv", newline="") as handle:
        for row in csv.DictReader(handle):
            local = datetime.strptime(row["time_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc).astimezone(LOCAL_TZ)
            if local.strftime("%Y-%m-%d") == DEMO_DATE:
                stamps.add(row["time_utc"])

    h1_rows = {}
    with open(REPO_ROOT / "data" / "processed" / "sim-boston.csv", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["time_utc"] in stamps:
                h1_rows.setdefault(row["zone"], []).append(row)

    for zone in day["zones"]:
        config = {
            "zone_id": zone["zone"],
            "light_rule": zone["light_rule"],
            "light_target": zone["light_target"],
            "soil_request_below_mm": day["constants"]["SOIL_DRY_BELOW"],
            "rain_ok": bool(zone["rain_ok"]),
            "kc": zone["kc"],
            "soil_start": zone["soil_start"],
        }
        produced = engine.run_zone(config, hours)
        expected = h1_rows[zone["zone"]]
        assert len(produced) == 24
        for index, (mine, theirs) in enumerate(zip(produced, expected)):
            assert mine["state"] == theirs["state"], f"zone {zone['zone']} hour {index}"
            assert mine["reason"] == theirs["reason"], f"zone {zone['zone']} hour {index}"
            assert mine["open_fraction"] == pytest.approx(float(theirs["open_fraction"]), abs=1e-4)
            assert mine["soil_mm"] == pytest.approx(float(theirs["soil_mm"]), abs=0.02)
            assert mine["light_mol_so_far"] == pytest.approx(
                float(theirs["light_mol_so_far"]), abs=0.02)


def test_the_engine_is_deterministic(db):
    day = weather.load_day()
    hours = weather.hours_from(day)
    config = {"zone_id": "A", "light_rule": "dli", "light_target": 8.0,
              "soil_request_below_mm": 30.0, "rain_ok": False, "kc": 1.0, "soil_start": 53.26}
    assert engine.run_zone(config, hours) == engine.run_zone(config, hours)


# --------------------------------------------------------------------- the zone limit

def test_a_site_seeds_three_zones_and_can_take_a_fourth(call, site_zones):
    assert [zone["letter"] for zone in site_zones] == ["A", "B", "C"]
    listing = call("GET", "/api/sites/boston-demo/zones").body
    assert listing["can_add_zone"] is True
    assert listing["zone_limit"] == 4

    created = call("POST", "/api/sites/boston-demo/zones", NEW_ZONE)
    assert created.status == 201
    assert created.body["zone"]["letter"] == "D"

    listing = call("GET", "/api/sites/boston-demo/zones").body
    assert listing["can_add_zone"] is False
    assert "Archive one" in listing["add_zone_blocked_because"]


def test_a_fifth_active_zone_is_refused_by_the_api(call):
    call("POST", "/api/sites/boston-demo/zones", NEW_ZONE)
    refused = call("POST", "/api/sites/boston-demo/zones",
                   dict(NEW_ZONE, name="One zone too many"))
    assert refused.status == 409
    assert refused.body["error"]["code"] == "zone_limit_reached"
    assert refused.body["error"]["details"]["limit"] == 4
    assert len(call("GET", "/api/sites/boston-demo/zones").body["zones"]) == 4


def test_archiving_frees_a_slot_and_keeps_the_zone_readable(call, site_zones):
    zone_a = zone_by_letter(site_zones, "A")
    call("POST", "/api/sites/boston-demo/zones", NEW_ZONE)
    archived = call("POST", f"/api/zones/{zone_a['id']}/archive")
    assert archived.status == 200
    assert archived.body["zone"]["archived"] is True

    listing = call("GET", "/api/sites/boston-demo/zones").body
    assert listing["can_add_zone"] is True
    assert any(zone["archived"] for zone in listing["zones"]), "the archived zone is still listed"

    refused = call("PATCH", f"/api/zones/{zone_a['id']}",
                   {"expected_revision": 1, "light_target": 9.0})
    assert refused.body["error"]["code"] == "zone_archived"


# ----------------------------------------------------------- immutable configuration

def test_a_change_writes_a_new_revision_and_leaves_the_old_one(call, db, site_zones):
    zone_b = zone_by_letter(site_zones, "B")
    assert zone_b["revision"] == 1
    updated = call("PATCH", f"/api/zones/{zone_b['id']}",
                   {"expected_revision": 1, "light_target": 14.0,
                    "name": "Hydrangea, raised target"})
    assert updated.status == 200
    assert updated.body["zone"]["revision"] == 2
    assert updated.body["zone"]["config"]["light_target"] == 14.0

    original = store.config_at(db, zone_b["id"], 1)
    assert original["light_target"] == 12.0, "revision 1 was rewritten"
    assert original["name"] != "Hydrangea, raised target"


def test_a_stale_revision_is_refused(call, site_zones):
    zone_b = zone_by_letter(site_zones, "B")
    call("PATCH", f"/api/zones/{zone_b['id']}", {"expected_revision": 1, "light_target": 14.0})
    stale = call("PATCH", f"/api/zones/{zone_b['id']}",
                 {"expected_revision": 1, "light_target": 15.0})
    assert stale.status == 409
    assert stale.body["error"]["code"] == "revision_conflict"
    assert stale.body["error"]["details"]["current_revision"] == 2


def test_a_change_without_a_reviewed_revision_is_refused(call, site_zones):
    zone_b = zone_by_letter(site_zones, "B")
    refused = call("PATCH", f"/api/zones/{zone_b['id']}", {"light_target": 14.0})
    assert refused.status == 428
    assert refused.body["error"]["code"] == "expected_revision_required"


def test_earlier_runs_stay_reproducible_after_a_configuration_change(call, db, site_zones):
    before = call("POST", "/api/simulation-runs", {}).body["run"]
    zone_b = zone_by_letter(site_zones, "B")
    call("PATCH", f"/api/zones/{zone_b['id']}", {"expected_revision": 1, "light_target": 20.0})
    after = call("POST", "/api/simulation-runs", {}).body["run"]

    assert before["id"] != after["id"]
    revisions_before = {item["letter"]: item["revision"] for item in before["config_revisions"]}
    revisions_after = {item["letter"]: item["revision"] for item in after["config_revisions"]}
    assert revisions_before["B"] == 1 and revisions_after["B"] == 2
    assert before["weather_snapshot"]["sha256"] == after["weather_snapshot"]["sha256"]

    replayed = call("GET", f"/api/simulation-runs/{before['id']}").body["run"]
    assert replayed["config_sha256"] == before["config_sha256"]
    timeline = call("GET", f"/api/simulation-runs/{before['id']}/timeline").body
    hours_b = timeline["zones"][zone_b["id"]]
    assert len(hours_b) == 24
    assert [hour["state"] for hour in hours_b][STORM_HOUR] == "RAIN_OPEN"


def test_a_run_names_the_inputs_that_made_it(call):
    run = call("POST", "/api/simulation-runs", {"note": "demo"}).body["run"]
    assert run["engine_version"] == engine.ENGINE_VERSION
    assert len(run["weather_snapshot"]["sha256"]) == 64
    assert run["weather_snapshot"]["date_local"] == DEMO_DATE
    assert "measured" in run["weather_snapshot"]["sources"]["rain"]
    assert run["label"] == "simulated"


def test_a_missing_run_says_so_with_a_stable_code(call):
    missing = call("GET", "/api/simulation-runs/run_nothing")
    assert missing.status == 404
    assert missing.body["error"]["code"] == "simulation_run_not_found"


# -------------------------------------------------------------------------- overrides

def test_an_override_needs_a_review_and_carries_an_expiry(call, site_zones):
    zone_c = zone_by_letter(site_zones, "C")
    unreviewed = call("POST", f"/api/zones/{zone_c['id']}/overrides",
                      {"command": "open", "duration": "one_hour", "from_hour": 15})
    assert unreviewed.status == 428
    assert unreviewed.body["error"]["code"] == "review_required"

    applied = call("POST", f"/api/zones/{zone_c['id']}/overrides",
                   {"command": "open", "duration": "one_hour", "from_hour": 15,
                    "acknowledged_review": True})
    assert applied.status == 201
    assert applied.body["override"]["expires_at_hour"] == 16
    assert applied.body["override"]["active"] is True

    day_long = call("POST", f"/api/zones/{zone_c['id']}/overrides",
                    {"command": "closed", "duration": "end_of_day", "from_hour": 9,
                     "acknowledged_review": True})
    assert day_long.body["override"]["expires_at_hour"] == 24


def test_an_override_is_idempotent_under_one_key(call, site_zones):
    zone_c = zone_by_letter(site_zones, "C")
    body = {"command": "open", "duration": "one_hour", "from_hour": 15,
            "acknowledged_review": True}
    made = call("POST", f"/api/zones/{zone_c['id']}/overrides", body,
                headers={"Idempotency-Key": "abc-123"})
    again = call("POST", f"/api/zones/{zone_c['id']}/overrides", body,
                 headers={"Idempotency-Key": "abc-123"})
    assert made.status == 201 and again.status == 200
    assert again.body["replayed"] is True
    assert again.body["override"]["id"] == made.body["override"]["id"]


def test_an_expired_override_leaves_the_zone_on_automatic(call, db, site_zones):
    zone_c = zone_by_letter(site_zones, "C")
    call("POST", f"/api/zones/{zone_c['id']}/overrides",
         {"command": "open", "duration": "one_hour", "from_hour": STORM_HOUR,
          "acknowledged_review": True})
    run_id = call("POST", "/api/simulation-runs", {}).body["run"]["id"]
    hours = call("GET", f"/api/simulation-runs/{run_id}/timeline").body["zones"][zone_c["id"]]

    assert hours[STORM_HOUR]["manual"] is True, "the override hour is manual"
    assert hours[STORM_HOUR + 1]["manual"] is False, "the hour after expiry is automatic again"
    # The storm is one hour long, so the automatic answer after it is the light rule.
    assert hours[STORM_HOUR + 1]["state"] == "LIGHT_OPEN"
    assert hours[STORM_HOUR + 1]["reason"] == ""


def test_a_safety_rule_outranks_a_manual_open(call, site_zones):
    """A held-open command at a dark hour is refused, and the console is told why.

    The demo day's heaviest hour is 5.3 mm, well under the 25.0 mm hard-rain rule, so
    that branch never fires on 10 June. The night rule is the conflict this day carries.
    """
    zone_b = zone_by_letter(site_zones, "B")
    call("POST", f"/api/zones/{zone_b['id']}/overrides",
         {"command": "open", "duration": "one_hour", "from_hour": 3,
          "acknowledged_review": True})
    run_id = call("POST", "/api/simulation-runs", {}).body["run"]["id"]
    hour = call("GET", f"/api/simulation-runs/{run_id}/timeline").body["zones"][zone_b["id"]][3]
    assert hour["conflict"] is True
    assert hour["state"] == "NIGHT"
    assert hour["open_fraction"] == 0


def test_the_hard_rain_rule_outranks_a_manual_open(db):
    """Synthetic hours, because no hour of the demo day reaches the threshold."""
    threshold = engine.RULES["HARD_RAIN_MM"]
    hours = [{"local_hour": hour, "ghi": 500.0, "rain_mm": 0.0, "t2m": 26.0}
             for hour in range(24)]
    hours[12]["rain_mm"] = threshold + 1.0
    config = {"zone_id": "B", "light_rule": "dli", "light_target": 40.0,
              "soil_request_below_mm": 30.0, "rain_ok": True, "kc": 1.0, "soil_start": 10.0}
    overrides = [{"command": "open", "from_hour": 12, "until_hour": 13}]
    hour = engine.run_zone(config, hours, overrides)[12]
    assert hour["conflict"] is True
    assert hour["reason"] == "hard_rain"
    assert hour["open_fraction"] == 0
    assert hour["rain_in_mm"] == 0


def test_return_to_automatic_releases_and_is_logged(call, site_zones):
    zone_c = zone_by_letter(site_zones, "C")
    call("POST", f"/api/zones/{zone_c['id']}/overrides",
         {"command": "closed", "duration": "end_of_day", "from_hour": 8,
          "acknowledged_review": True})
    released = call("POST", f"/api/zones/{zone_c['id']}/return-to-automatic", {"at_hour": 12})
    assert released.body["control"] == "automatic"
    assert released.body["released"]

    zones = call("GET", "/api/sites/boston-demo/zones").body["zones"]
    assert zone_by_letter(zones, "C")["manual_overrides"] == []

    kinds = [event["kind"] for event in
             call("GET", f"/api/zones/{zone_c['id']}/control-events").body["events"]]
    assert "returned_to_automatic" in kinds
    assert "manual_override_applied" in kinds


def test_the_control_log_only_grows(call, db, site_zones):
    zone_a = zone_by_letter(site_zones, "A")
    before = len(call("GET", f"/api/zones/{zone_a['id']}/control-events").body["events"])
    call("PATCH", f"/api/zones/{zone_a['id']}", {"expected_revision": 1, "rain_ok": True})
    call("POST", f"/api/zones/{zone_a['id']}/archive")
    after = call("GET", f"/api/zones/{zone_a['id']}/control-events").body["events"]
    assert len(after) == before + 2
    assert after[0]["created_at"] >= after[-1]["created_at"]


# ------------------------------------------------------------- the metric registry

def test_the_metric_registry_is_the_only_way_to_change_the_overview(call, site_zones):
    definitions = call("GET", "/api/metric-definitions").body
    supported = {item["id"] for item in definitions["metrics"]}
    assert "soil_water" in supported and "daily_light" in supported

    zone_a = zone_by_letter(site_zones, "A")
    reordered = ["roof_position", "control_state", "decision_reason", "soil_water", "daily_light"]
    saved = call("PUT", f"/api/zones/{zone_a['id']}/review-profile", {"metrics": reordered})
    assert saved.status == 200
    assert saved.body["metrics"] == reordered

    zones = call("GET", "/api/sites/boston-demo/zones").body["zones"]
    assert zone_by_letter(zones, "A")["review_profile"] == reordered


def test_an_invented_metric_is_refused(call, site_zones):
    zone_a = zone_by_letter(site_zones, "A")
    refused = call("PUT", f"/api/zones/{zone_a['id']}/review-profile",
                   {"metrics": ["roof_position", "control_state", "decision_reason",
                                "soil_mm * 2"]})
    assert refused.status == 422
    assert refused.body["error"]["code"] == "metric_not_supported"
    assert "soil_water" in refused.body["error"]["details"]["supported"]


def test_the_overview_keeps_the_metrics_a_grower_cannot_drop(call, site_zones):
    zone_a = zone_by_letter(site_zones, "A")
    refused = call("PUT", f"/api/zones/{zone_a['id']}/review-profile",
                   {"metrics": ["daily_light", "soil_water"]})
    assert refused.status == 422
    assert refused.body["error"]["details"]["missing"] == list(metrics.REQUIRED_METRICS)


# ------------------------------------------------------------------ validation errors

def test_an_invalid_configuration_lists_every_problem_at_once(call):
    refused = call("POST", "/api/sites/boston-demo/zones", {
        "name": "", "light_rule": "guesswork", "light_target": -3,
        "soil_request_below_mm": 900, "rain_ok": "yes", "mystery": 1,
    })
    assert refused.status == 422
    assert refused.body["error"]["code"] == "validation_failed"
    problems = {item["field"]: item["code"] for item in refused.body["error"]["details"]["problems"]}
    assert problems["name"] == "too_short"
    assert problems["light_rule"] == "not_a_choice"
    assert problems["light_target"] == "below_minimum"
    assert problems["soil_request_below_mm"] == "above_maximum"
    assert problems["rain_ok"] == "type_error"
    assert problems["mystery"] == "unknown_field"


def test_unknown_routes_and_methods_carry_stable_codes(call):
    assert call("GET", "/api/nothing-here").body["error"]["code"] == "not_found"
    refused = call("DELETE", "/api/sites/boston-demo/zones")
    assert refused.status == 405
    assert refused.body["error"]["code"] == "method_not_allowed"
    assert "GET" in refused.body["error"]["details"]["allowed"]


def test_health_reports_availability_without_internals(call):
    body = call("GET", "/api/health").body
    assert body["status"] == "ok"
    assert body["zone_limit"] == 4
    text = json.dumps(body).lower()
    for secret in ("password", "database_url", "postgres", "secret", "token", "/users/"):
        assert secret not in text


def test_health_reports_storage_ready_when_the_database_opens(call):
    assert call("GET", "/api/health").body["storage"] == "ready"


def test_health_stays_up_and_says_so_when_the_database_cannot_open():
    def broken():
        raise OSError("no database here")

    response = dispatch(Request("GET", "/api/health", {}, None, {}), db_factory=broken)
    assert response.status == 200
    assert response.body["status"] == "ok"
    assert response.body["storage"] == "unavailable"


def test_operating_state_is_never_cached(call, site_zones):
    for path in ("/api/sites/boston-demo/zones",
                 f"/api/zones/{site_zones[0]['id']}/control-events"):
        assert call("GET", path).headers["Cache-Control"] == "no-store"


# ---------------------------------------------------------------------------- units

def test_display_units_convert_only_at_the_boundary(call):
    run_id = call("POST", "/api/simulation-runs", {}).body["run"]["id"]
    metric = call("GET", f"/api/simulation-runs/{run_id}/timeline").body
    imperial = call("GET", f"/api/simulation-runs/{run_id}/timeline",
                    query={"units": "us"}).body

    assert metric["run"]["units"]["display"]["depth"] == "mm"
    assert imperial["run"]["units"]["display"]["depth"] == "in"
    zone_id = next(iter(metric["zones"]))
    millimetres = metric["zones"][zone_id][15]["soil_water_mm"]
    inches = imperial["zones"][zone_id][15]["soil_water"]
    assert inches == pytest.approx(millimetres / 25.4, abs=1e-3)
    assert imperial["zones"][zone_id][15]["soil_water_mm"] == millimetres
