"""Tests for H1, the zones, the rules, the year.

Every expected value here was computed from the real files by a planner before any code
existed, and is quoted from `planning/plans/packages/H1-zones-light-rain-soil.md`.
If one does not match, stop and report it. Never edit the value to make a test pass.

The soil latch makes results depend on the path, so the package gives tolerances:
shares within 0.03, days within 3, state counts within 5 hours.
"""

import csv
import importlib.util
import socket
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BUILD = REPO_ROOT / "software" / "h1" / "build.py"
PROCESSED = REPO_ROOT / "data" / "processed"
LOCAL_TZ = ZoneInfo("America/New_York")


def load():
    spec = importlib.util.spec_from_file_location("h1_build", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def h1():
    return load()


@pytest.fixture(scope="module")
def run(h1):
    """One in-memory run of the whole year. Writes nothing."""
    crops, weather, runs = h1.build(write=False)
    return {"crops": crops, "weather": weather, "runs": runs}


def totals(series):
    states = {}
    for row in series:
        states[row["state"]] = states.get(row["state"], 0) + 1
    rain = sum(row["rain_in_mm"] for row in series)
    irr = sum(row["irrigation_mm"] for row in series)
    return {
        "states": states, "rain": rain, "irrigation": irr,
        "use": sum(row["crop_use_mm"] for row in series),
        "share": rain / (rain + irr) if (rain + irr) else 0.0,
        "soil_min": min(row["soil_mm"] for row in series),
        "soil_max": max(row["soil_mm"] for row in series),
    }


def local_hour_rows(run, date, zone):
    out = {}
    for hour, row in zip(run["weather"], run["runs"][zone]):
        local = hour["ts"].astimezone(LOCAL_TZ)
        if local.strftime("%Y-%m-%d") == date:
            out[local.hour] = row
    return out


# --- the rain parser ---------------------------------------------------------

def test_rain_parser(h1):
    rain, seen = h1.read_rain()
    assert sum(rain.values()) == pytest.approx(1338.6, abs=0.05)
    assert sum(1 for value in rain.values() if value > 0) == 373
    assert max(rain.values()) == pytest.approx(37.8, abs=0.05)
    wettest = max(rain, key=rain.get)
    assert wettest.strftime("%Y-%m-%dT%H") == "2023-07-04T21"
    assert rain[datetime(2023, 6, 3, 19, tzinfo=timezone.utc)] == pytest.approx(23.9, abs=0.05)
    assert rain[datetime(2023, 6, 3, 20, tzinfo=timezone.utc)] == pytest.approx(18.5, abs=0.05)
    assert not [stamp for stamp, count in seen.items() if count > 1], "two FM-15 rows in one hour"


def test_missing_hours_become_zero(h1, run):
    """2 hours carry no AA1 field, and the rule makes them 0.

    That day's own daily summary equals its hourly sum, so no rain was lost.
    """
    rain, _ = h1.read_rain()
    missing = sorted(h["time_utc"] for h in run["weather"] if h["ts"] not in rain)
    assert missing == ["2023-07-30T22:00:00Z", "2023-07-30T23:00:00Z"]
    for hour in run["weather"]:
        if hour["time_utc"] in missing:
            assert hour["rain_mm"] == 0.0


def test_monthly_rain(run):
    spec = [12.4, 21.1, 18.0, 61.0, 133.5, 197.9, 189.6, 183.1, 171.9, 69.8, 144.9, 135.4]
    got = [0.0] * 12
    for hour in run["weather"]:
        got[hour["month"] - 1] += hour["rain_mm"]
    for month, (a, b) in enumerate(zip(got, spec), start=1):
        assert a == pytest.approx(b, abs=0.1), f"month {month}"


# --- the join ----------------------------------------------------------------

def test_the_join(run):
    weather = run["weather"]
    assert len(weather) == 8760
    assert sum(h["rain_mm"] for h in weather) == pytest.approx(1338.6, abs=0.05)
    lit = [h for h in weather if h["ghi"] > 0]
    assert len(lit) == 4568
    wet = [h for h in lit if h["rain_mm"] > 0]
    dry = [h for h in lit if h["rain_mm"] == 0]
    assert len(wet) == 242
    assert sum(h["rain_mm"] for h in wet) == pytest.approx(924.2, abs=0.05)
    ratio = (sum(h["ghi"] for h in wet) / len(wet)) / (sum(h["ghi"] for h in dry) / len(dry))
    assert ratio == pytest.approx(0.627, abs=0.005), "rainy hours must be darker than dry ones"


# --- light and evaporation ---------------------------------------------------

def test_light_constant_and_year(h1, run):
    assert h1.K == pytest.approx(2.0565, abs=0.0001)
    outdoor = sum(h["ghi"] * h1.K * 3600 / 1e6 for h in run["weather"])
    assert outdoor == pytest.approx(13497.5, rel=0.001)
    assert outdoor / 365 == pytest.approx(36.98, abs=0.05)


def test_reference_evaporation_year(h1, run):
    total = sum(h1.reference_evaporation(h["ghi"], h["t2m"]) for h in run["weather"])
    assert total == pytest.approx(1332.6, rel=0.001)


def test_pressure_and_gamma(h1):
    assert h1.PRESSURE_KPA == pytest.approx(100.9258, abs=0.001)
    assert h1.GAMMA == pytest.approx(0.067116, abs=0.000001)


# --- the year, with the package's tolerances ---------------------------------

YEAR = {
    "A": {"states": {"NIGHT": 4192, "LIGHT_OPEN": 1740, "SHADE": 2586, "RAIN_SHUT": 242},
          "rain": 0.0, "irrigation": 325.2, "use": 344.7, "share": 0.000,
          "soil_min": 18.02, "soil_max": 54.0},
    "B": {"states": {"NIGHT": 4192, "LIGHT_OPEN": 2094, "SHADE": 2232,
                     "RAIN_SHUT": 182, "RAIN_OPEN": 60},
          "rain": 260.0, "irrigation": 216.7, "use": 503.8, "share": 0.545,
          "soil_min": 18.03, "soil_max": 59.77},
    "C": {"states": {"NIGHT": 4192, "LIGHT_OPEN": 3681, "HEAT_SHADE": 645,
                     "RAIN_SHUT": 182, "RAIN_OPEN": 60},
          "rain": 186.3, "irrigation": 904.8, "use": 1109.1, "share": 0.171,
          "soil_min": 18.0, "soil_max": 55.55},
}


@pytest.mark.parametrize("zone", ["A", "B", "C"])
def test_the_year(run, zone):
    got = totals(run["runs"][zone])
    want = YEAR[zone]
    assert set(got["states"]) == set(want["states"]), "an unexpected state appeared"
    for state, count in want["states"].items():
        assert got["states"][state] == pytest.approx(count, abs=5), state
    assert got["rain"] == pytest.approx(want["rain"], abs=0.5)
    assert got["irrigation"] == pytest.approx(want["irrigation"], abs=0.5)
    assert got["use"] == pytest.approx(want["use"], abs=0.5)
    assert got["share"] == pytest.approx(want["share"], abs=0.03)
    assert got["soil_min"] == pytest.approx(want["soil_min"], abs=0.05)
    assert got["soil_max"] == pytest.approx(want["soil_max"], abs=0.05)


def test_days_the_target_was_met(h1, run):
    rows = h1.summary_rows(run["crops"], run["weather"], run["runs"])
    year = {row[0]: row for row in rows if row[2] == "year"}
    assert int(year["A"][6]) == pytest.approx(354, abs=3)
    assert int(year["B"][6]) == pytest.approx(346, abs=3)


# --- the demo day ------------------------------------------------------------

def test_demo_day_soil_at_midnight(run):
    for zone, want in (("A", 53.26), ("B", 26.71), ("C", 34.11)):
        rows = local_hour_rows(run, "2023-06-03", zone)
        assert rows[5]["soil_mm"] == pytest.approx(want, abs=0.02), zone


def test_demo_day_three_zones_three_answers(run):
    """The whole product in one afternoon. At 15:00 it rains 23.9 mm."""
    a = local_hour_rows(run, "2023-06-03", "A")
    b = local_hour_rows(run, "2023-06-03", "B")
    c = local_hour_rows(run, "2023-06-03", "C")

    assert a[10]["state"] == "LIGHT_OPEN" and a[11]["state"] == "SHADE"
    assert a[10]["light_mol_so_far"] == pytest.approx(8.08, abs=0.02)
    assert b[11]["state"] == "LIGHT_OPEN" and b[12]["state"] == "SHADE"
    assert b[11]["light_mol_so_far"] == pytest.approx(12.72, abs=0.02)

    for hour in (15, 16):
        assert a[hour]["state"] == "RAIN_SHUT" and a[hour]["reason"] == "opted_out"
        assert b[hour]["state"] == "RAIN_OPEN"
        # Rests on a margin of 1.2 mm: the blueberry's soil is 31.17 against 30.
        assert c[hour]["state"] == "RAIN_SHUT" and c[hour]["reason"] == "wet_enough"

    assert b[14]["soil_mm"] == pytest.approx(25.48, abs=0.02)
    assert b[15]["soil_mm"] == pytest.approx(49.03, abs=0.02)
    assert b[16]["soil_mm"] == pytest.approx(59.75, abs=0.02)
    assert c[14]["soil_mm"] == pytest.approx(31.17, abs=0.02)
    assert c[19]["soil_mm"] == pytest.approx(30.91, abs=0.02)


def test_demo_day_the_price_of_the_rain_rule(run):
    b = local_hour_rows(run, "2023-06-03", "B")
    stored = sum(row["rain_in_mm"] for row in b.values())
    assert stored == pytest.approx(34.9, abs=0.1), "the 60 mm cap refuses about 7.5 mm"
    assert b[19]["light_mol_so_far"] - b[11]["light_mol_so_far"] == pytest.approx(5.96, abs=0.05)


def test_demo_day_has_no_heat_shade(run):
    peak = max(h["t2m"] for h in run["weather"]
               if h["ts"].astimezone(LOCAL_TZ).strftime("%Y-%m-%d") == "2023-06-03")
    assert peak == pytest.approx(29.84, abs=0.02)
    for zone in "ABC":
        assert all(row["state"] != "HEAT_SHADE"
                   for row in local_hour_rows(run, "2023-06-03", zone).values())


@pytest.mark.parametrize("scale", [0.95, 0.97, 0.99, 1.01, 1.03, 1.05])
def test_the_fern_and_the_blueberry_hold_under_a_nudged_evaporation(h1, scale):
    """How far to trust it. The hydrangea held in six runs of seven and is not asserted
    here: at 0.95 its second rain hour flips to shut, which the package records."""
    _, weather, runs = h1.build(write=False, et_scale=scale)
    for zone, reason in (("A", "opted_out"), ("C", "wet_enough")):
        rows = {}
        for hour, row in zip(weather, runs[zone]):
            local = hour["ts"].astimezone(LOCAL_TZ)
            if local.strftime("%Y-%m-%d") == "2023-06-03":
                rows[local.hour] = row
        for hour in (15, 16):
            assert rows[hour]["state"] == "RAIN_SHUT", f"{zone} at {hour} under {scale}"
            assert rows[hour]["reason"] == reason


# --- it runs with the network off, and repeats itself ------------------------

def test_builds_with_the_network_off(h1, monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("H1 opened a socket, and it must run with the network off")

    monkeypatch.setattr(socket, "socket", refuse)
    crops, weather, runs = h1.build(write=False)
    assert len(weather) == 8760 and len(runs) == 3


def test_two_runs_give_identical_bytes(h1, tmp_path, monkeypatch):
    before = {name: (PROCESSED / name).read_bytes() for name in
              ("weather-apopka.csv", "sim-apopka.csv", "sim-summary-apopka.csv")}
    h1.build(write=True)
    after = {name: (PROCESSED / name).read_bytes() for name in before}
    assert before == after
