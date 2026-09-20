"""The API surface: routing, serialisation, and nothing that decides about the roof.

Every route is a plain function of (request, path parameters). The engine is called,
never inlined, and persistence is called, never reimplemented, so this file stays the
one place where HTTP concerns live.

Responses that carry zone configuration, overrides, or simulation results are marked
`Cache-Control: no-store`, because they are a grower's operating state.
"""

import json
import os
import re

from . import engine, metrics as metric_registry, seed, store, units, weather
from .errors import ApiError, MethodNotAllowed, NotFound
from .validation import (
    OverrideCreate, ReviewProfilePut, RunCreate, ZoneCreate, ZonePatch,
)

API_VERSION = "1"
NO_STORE = "no-store"


class Request:
    def __init__(self, method, path, query=None, body=None, headers=None):
        self.method = method.upper()
        self.path = path
        self.query = query or {}
        self.body = body
        self.headers = {key.lower(): value for key, value in (headers or {}).items()}

    def json(self):
        if self.body in (None, b"", ""):
            return {}
        text = self.body.decode("utf-8") if isinstance(self.body, bytes) else self.body
        try:
            return json.loads(text)
        except ValueError:
            raise ApiError("The request body is not valid JSON.", code="invalid_json")

    def units(self):
        return units.resolve(self.query.get("units", ["metric"])[0]
                             if isinstance(self.query.get("units"), list)
                             else self.query.get("units", "metric"))

    def idempotency_key(self):
        return self.headers.get("idempotency-key")


class Response:
    def __init__(self, status, body, headers=None):
        self.status = status
        self.body = body
        self.headers = headers or {}


def json_response(body, status=200, cache=NO_STORE):
    return Response(status, body, {"Cache-Control": cache})


# ------------------------------------------------------------------ serialisation

def zone_payload(db, zone, system="metric"):
    config = store.current_config(db, zone["id"])
    overrides = store.effective_overrides(db, zone["id"])
    return {
        "id": zone["id"],
        "site_id": zone["site_id"],
        "letter": zone["letter"],
        "position": zone["position"],
        "archived": bool(zone["archived_at"]),
        "archived_at": zone["archived_at"],
        "created_at": zone["created_at"],
        "revision": config["revision"],
        "config": {
            "name": config["name"],
            "crop_profile_id": config["crop_profile_id"],
            "crop_name": config["crop_name"],
            "light_rule": config["light_rule"],
            "light_target": config["light_target"],
            "soil_request_below": units.convert("depth", config["soil_request_below_mm"], system),
            "soil_request_below_mm": config["soil_request_below_mm"],
            "rain_ok": bool(config["rain_ok"]),
            "kc": config["kc"],
            "note": config["note"],
            "revision": config["revision"],
            "created_at": config["created_at"],
        },
        "review_profile": store.review_profile(db, zone["id"]),
        "manual_overrides": overrides,
        "label": "modelled",
    }


def override_payload(row):
    return {
        "id": row["id"],
        "zone_id": row["zone_id"],
        "command": row["command"],
        "duration": row["duration"],
        "from_hour": row["from_hour"],
        "expires_at_hour": row["until_hour"],
        "reason": row["reason"],
        "created_at": row["created_at"],
        "released_at": row["released_at"],
        "active": row["released_at"] is None,
    }


def run_payload(db, run, system="metric"):
    snapshot = store.weather_snapshot(db, run["weather_snapshot_id"])
    return {
        "id": run["id"],
        "site_id": run["site_id"],
        "date_local": run["date_local"],
        "engine_version": run["engine_version"],
        "created_at": run["created_at"],
        "note": run["note"],
        "config_revisions": json.loads(run["config_snapshot_json"]),
        "config_sha256": run["config_sha256"],
        "weather_snapshot": {
            "id": snapshot["id"],
            "sha256": snapshot["sha256"],
            "date_local": snapshot["date_local"],
            "sources": json.loads(snapshot["sources_json"]),
        },
        "units": units.unit_block(system),
        "label": "simulated",
    }


# ------------------------------------------------------------------------- routes

def health(request, _params, db=None):
    """Service availability, with nothing about credentials or internals."""
    body = {
        "status": "ok",
        "api_version": API_VERSION,
        "engine_version": engine.ENGINE_VERSION,
        "app_env": os.environ.get("APP_ENV", "development"),
        "storage": "ready" if db is not None else "unavailable",
        "zone_limit": store.MAX_ACTIVE_ZONES,
    }
    return json_response(body)


def metric_definitions(_request, _params, db=None):
    return json_response({
        "metrics": metric_registry.METRIC_DEFINITIONS,
        "required": list(metric_registry.REQUIRED_METRICS),
        "default_profile": list(metric_registry.DEFAULT_PROFILE),
    }, cache="public, max-age=0, must-revalidate")


def list_zones(request, params, db):
    site_id = params["site_id"]
    seed.seed_site(db, site_id)
    system = request.units()
    zones = store.all_zones(db, site_id)
    active = [zone for zone in zones if not zone["archived_at"]]
    return json_response({
        "site_id": site_id,
        "zone_limit": store.MAX_ACTIVE_ZONES,
        "active_count": len(active),
        "can_add_zone": len(active) < store.MAX_ACTIVE_ZONES,
        "add_zone_blocked_because": None if len(active) < store.MAX_ACTIVE_ZONES else
            f"The roof carries {store.MAX_ACTIVE_ZONES} zones. Archive one to add another.",
        "units": units.unit_block(system),
        "zones": [zone_payload(db, zone, system) for zone in zones],
    })


def create_zone(request, params, db):
    site_id = params["site_id"]
    seed.seed_site(db, site_id)
    data = ZoneCreate.parse(request.json())
    zone = store.create_zone(db, site_id, data)
    return json_response({"zone": zone_payload(db, zone, request.units())}, status=201)


def patch_zone(request, params, db):
    data = ZonePatch.parse_partial(request.json())
    if "expected_revision" not in data:
        raise ApiError(
            "Send the revision this change was reviewed against.",
            code="expected_revision_required", status=428, field="expected_revision")
    zone = store.update_zone(db, params["zone_id"], data)
    return json_response({"zone": zone_payload(db, zone, request.units())})


def archive_zone(request, params, db):
    zone = store.archive_zone(db, params["zone_id"])
    return json_response({"zone": zone_payload(db, zone, request.units())})


def restore_zone(request, params, db):
    zone = store.restore_zone(db, params["zone_id"])
    return json_response({"zone": zone_payload(db, zone, request.units())})


def put_review_profile(request, params, db):
    data = ReviewProfilePut.parse(request.json())
    cleaned = store.set_review_profile(db, params["zone_id"], data["metrics"])
    return json_response({"zone_id": params["zone_id"], "metrics": cleaned})


def create_override(request, params, db):
    payload = request.json()
    key = request.idempotency_key()
    if key and not payload.get("idempotency_key"):
        payload["idempotency_key"] = key
    data = OverrideCreate.parse(payload)
    if not data["acknowledged_review"]:
        raise ApiError(
            "Review the change before it is applied.",
            code="review_required", status=428, field="acknowledged_review")
    row, replayed = store.create_override(db, params["zone_id"], data)
    return json_response({"override": override_payload(row), "replayed": replayed},
                         status=200 if replayed else 201)


def release_override(request, params, db):
    payload = request.json() if request.body else {}
    at_hour = payload.get("at_hour")
    released = store.return_to_automatic(db, params["zone_id"], at_hour)
    return json_response({"zone_id": params["zone_id"], "released": released,
                          "control": "automatic"})


def list_control_events(request, params, db):
    rows = store.control_events(db, params["zone_id"])
    return json_response({
        "zone_id": params["zone_id"],
        "events": [{
            "id": row["id"], "kind": row["kind"], "actor": row["actor"],
            "created_at": row["created_at"], "payload": json.loads(row["payload_json"]),
        } for row in rows],
    })


def create_run(request, params, db):
    data = RunCreate.parse(request.json())
    site_id = request.query.get("site_id") or store.DEFAULT_SITE
    seed.seed_site(db, site_id)

    day = weather.load_day()
    hours = weather.hours_from(day)
    date_local = data["date_local"] or day["date_local"]
    digest = engine.snapshot_digest(hours, day["sources"])
    snapshot = store.save_weather_snapshot(db, date_local, hours, day["sources"], digest)

    configs, overrides = [], {}
    for zone in store.active_zones(db, site_id):
        config = store.current_config(db, zone["id"])
        configs.append({
            "zone_id": zone["id"],
            "letter": zone["letter"],
            "revision": config["revision"],
            "name": config["name"],
            "crop_name": config["crop_name"],
            "light_rule": config["light_rule"],
            "light_target": config["light_target"],
            "soil_request_below_mm": config["soil_request_below_mm"],
            "rain_ok": bool(config["rain_ok"]),
            "kc": config["kc"],
            "soil_start": soil_start_for(day, zone["letter"]),
        })
        overrides[zone["id"]] = store.effective_overrides(db, zone["id"])

    results = engine.run_day(configs, hours, overrides)
    run = store.save_run(db, site_id, date_local, snapshot["id"], configs,
                         engine.config_digest(configs), engine.ENGINE_VERSION,
                         results, data["note"])
    return json_response({"run": run_payload(db, run, request.units())}, status=201)


def soil_start_for(day, letter):
    for zone in day["zones"]:
        if zone["zone"] == letter:
            return float(zone["soil_start"])
    return engine.RULES["SOIL_START"]


def get_run(request, params, db):
    run = store.get_run(db, params["run_id"])
    return json_response({"run": run_payload(db, run, request.units())})


def run_timeline(request, params, db):
    run = store.get_run(db, params["run_id"])
    system = request.units()
    snapshot = store.weather_snapshot(db, run["weather_snapshot_id"])
    hours = json.loads(snapshot["hours_json"])
    by_zone = {}
    for row in store.run_results(db, run["id"]):
        by_zone.setdefault(row["zone_id"], []).append({
            "local_hour": row["local_hour"],
            "open_fraction": row["open_fraction"],
            "daily_light": row["light_mol_so_far"],
            "soil_water": units.convert("depth", row["soil_mm"], system),
            "soil_water_mm": row["soil_mm"],
            "rain_in": units.convert("depth", row["rain_in_mm"], system),
            "irrigation": units.convert("depth", row["irrigation_mm"], system),
            "state": row["state"],
            "reason": row["reason"],
            "conflict": bool(row["conflict"]),
            "manual": bool(row["manual"]),
        })
    return json_response({
        "run": run_payload(db, run, system),
        "hours": [{
            "local_hour": hour["local_hour"],
            "irradiance": hour["ghi"],
            "rain": units.convert("depth", hour["rain_mm"], system),
            "rain_mm": hour["rain_mm"],
            "air_temperature": units.convert("temperature", hour["t2m"], system),
            "play_seconds": hour.get("play_seconds", 2.4),
        } for hour in sorted(hours, key=lambda item: item["local_hour"])],
        "zones": by_zone,
    })


def list_runs(request, params, db):
    site_id = request.query.get("site_id") or store.DEFAULT_SITE
    rows = store.list_runs(db, site_id)
    return json_response({
        "site_id": site_id,
        "runs": [{
            "id": row["id"], "date_local": row["date_local"], "created_at": row["created_at"],
            "engine_version": row["engine_version"], "config_sha256": row["config_sha256"],
            "note": row["note"],
        } for row in rows],
    })


# The last field says whether the view needs the database: True, False, or OPTIONAL,
# which opens it if it can and hands the view None if it cannot.
OPTIONAL = "optional"

ROUTES = [
    ("GET", r"^/api/health$", health, OPTIONAL),
    ("GET", r"^/api/metric-definitions$", metric_definitions, False),
    ("GET", r"^/api/sites/(?P<site_id>[\w.-]+)/zones$", list_zones, True),
    ("POST", r"^/api/sites/(?P<site_id>[\w.-]+)/zones$", create_zone, True),
    ("PATCH", r"^/api/zones/(?P<zone_id>[\w.-]+)$", patch_zone, True),
    ("POST", r"^/api/zones/(?P<zone_id>[\w.-]+)/archive$", archive_zone, True),
    ("POST", r"^/api/zones/(?P<zone_id>[\w.-]+)/restore$", restore_zone, True),
    ("PUT", r"^/api/zones/(?P<zone_id>[\w.-]+)/review-profile$", put_review_profile, True),
    ("POST", r"^/api/zones/(?P<zone_id>[\w.-]+)/overrides$", create_override, True),
    ("POST", r"^/api/zones/(?P<zone_id>[\w.-]+)/return-to-automatic$", release_override, True),
    ("GET", r"^/api/zones/(?P<zone_id>[\w.-]+)/control-events$", list_control_events, True),
    ("POST", r"^/api/simulation-runs$", create_run, True),
    ("GET", r"^/api/simulation-runs$", list_runs, True),
    ("GET", r"^/api/simulation-runs/(?P<run_id>[\w.-]+)/timeline$", run_timeline, True),
    ("GET", r"^/api/simulation-runs/(?P<run_id>[\w.-]+)$", get_run, True),
]

COMPILED = [(method, re.compile(pattern), view, needs_db)
            for method, pattern, view, needs_db in ROUTES]


def dispatch(request, db_factory=store.open_database):
    """Route one request. Returns a Response, and raises nothing the caller must catch."""
    path = request.path.rstrip("/") or request.path
    allowed = set()
    for method, pattern, view, needs_db in COMPILED:
        match = pattern.match(path)
        if not match:
            continue
        allowed.add(method)
        if method != request.method:
            continue
        db = None
        try:
            if needs_db == OPTIONAL:
                try:
                    db = db_factory()
                except Exception:  # noqa: BLE001 - health reports this, and stays up
                    db = None
            elif needs_db:
                db = db_factory()
            return view(request, match.groupdict(), db)
        except ApiError as error:
            return Response(error.status, error.payload(), {"Cache-Control": NO_STORE})
        except Exception as error:  # noqa: BLE001 - the boundary turns anything into a code
            return Response(500, {"error": {
                "code": "internal_error",
                "message": "The service could not complete this request.",
                "details": {"kind": type(error).__name__},
            }}, {"Cache-Control": NO_STORE})
        finally:
            if db is not None:
                db.close()

    if allowed:
        error = MethodNotAllowed(
            f"{request.method} is not allowed here.",
            details={"allowed": sorted(allowed)})
        return Response(error.status, error.payload(),
                        {"Allow": ", ".join(sorted(allowed)), "Cache-Control": NO_STORE})

    error = NotFound(f"No API route matches {request.path!r}.")
    return Response(error.status, error.payload(), {"Cache-Control": NO_STORE})
