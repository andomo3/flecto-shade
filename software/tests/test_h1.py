"""Tests for H1, the zones, the rules, the year.

Every expected value here was recomputed from the real files for the Boston Logan
International Airport gauge on 2026-09-20, when the project moved from the Apopka site
to a Massachusetts one. The Apopka figures quoted in
`planning/plans/packages/H1-zones-light-rain-soil.md` describe the old site and no
longer apply. If a value here does not match, stop and report it. Never edit one to make
a test pass: change it only when the underlying dataset is deliberately replaced, as it
was here.

The soil latch makes results depend on the path, so the package's tolerances are kept:
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
DEMO_DAY = "2023-06-10"
ET_SCALES = [0.95, 0.97, 0.99, 1.01, 1.03, 1.05]


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
    assert sum(rain.values()) == pytest.approx(1242.7, abs=0.05)
    assert sum(1 for value in rain.values() if value > 0) == 729
    assert max(rain.values()) == pytest.approx(26.9, abs=0.05)
    wettest = max(rain, key=rain.get)
    assert wettest.strftime("%Y-%m-%dT%H") == "2023-07-22T02"
    # The demo day's storm, local 14:00 on 2023-06-10.
    assert rain[datetime(2023, 6, 10, 18, tzinfo=timezone.utc)] == pytest.approx(5.3, abs=0.05)


def test_the_two_hours_with_two_fm15_rows(h1):
    """Unlike the Apopka gauge, this station files a second FM-15 row in two hours.

    Both are an off-schedule report from source 4 followed by the regular :54 report
    from source 7, and both report a period of 01, so the two windows overlap. The
    parser's documented rule, the last row in the hour wins, takes the regular report.
    Asserting the exact pair means a third one cannot appear unnoticed.
    """
    rain, seen = h1.read_rain()
    twice = sorted(stamp for stamp, count in seen.items() if count > 1)
    assert [stamp.strftime("%Y-%m-%dT%H") for stamp in twice] == [
        "2023-02-23T22", "2023-08-15T15"]
    assert all(seen[stamp] == 2 for stamp in twice)
    # The :54 rows read 0.0 mm and 1.5 mm; the earlier rows read 0.0 mm and 1.2 mm.
    assert rain[twice[0]] == pytest.approx(0.0, abs=0.05)
    assert rain[twice[1]] == pytest.approx(1.5, abs=0.05)


def test_missing_hours_become_zero(h1, run):
    """33 hours of the year carry no usable AA1 field, and the rule makes them 0.

    The Apopka gauge had 2. Asserting the count means a parser change that started
    dropping hours would show up here rather than as a quietly drier year.
    """
    rain, _ = h1.read_rain()
    missing = sorted(h["time_utc"] for h in run["weather"] if h["ts"] not in rain)
    assert len(missing) == 33
    assert missing[0] == "2023-03-21T14:00:00Z"
    assert missing[-1] == "2023-12-16T05:00:00Z"
    for hour in run["weather"]:
        if hour["time_utc"] in missing:
            assert hour["rain_mm"] == 0.0


def test_monthly_rain(run):
    spec = [141.5, 35.3, 107.0, 64.2, 76.0, 79.6, 235.8, 164.4, 96.2, 36.9, 49.5, 156.3]
    got = [0.0] * 12
    for hour in run["weather"]:
        got[hour["month"] - 1] += hour["rain_mm"]
    for month, (a, b) in enumerate(zip(got, spec), start=1):
        assert a == pytest.approx(b, abs=0.1), f"month {month}"


# --- the join ----------------------------------------------------------------

def test_the_join(run):
    weather = run["weather"]
    assert len(weather) == 8760
    assert sum(h["rain_mm"] for h in weather) == pytest.approx(1242.7, abs=0.05)
    lit = [h for h in weather if h["ghi"] > 0]
    assert len(lit) == 4513
    wet = [h for h in lit if h["rain_mm"] > 0]
    dry = [h for h in lit if h["rain_mm"] == 0]
    assert len(wet) == 372
    assert sum(h["rain_mm"] for h in wet) == pytest.approx(618.6, abs=0.05)
    ratio = (sum(h["ghi"] for h in wet) / len(wet)) / (sum(h["ghi"] for h in dry) / len(dry))
    assert ratio == pytest.approx(0.348, abs=0.005), "rainy hours must be darker than dry ones"


# --- light and evaporation ---------------------------------------------------

def test_light_constant_and_year(h1, run):
    assert h1.K == pytest.approx(2.0565, abs=0.0001)
    outdoor = sum(h["ghi"] * h1.K * 3600 / 1e6 for h in run["weather"])
    assert outdoor == pytest.approx(10055.0, rel=0.001)
    assert outdoor / 365 == pytest.approx(27.55, abs=0.05)


def test_reference_evaporation_year(h1, run):
    total = sum(h1.reference_evaporation(h["ghi"], h["t2m"]) for h in run["weather"])
    assert total == pytest.approx(810.6, rel=0.001)


def test_pressure_and_gamma(h1):
    assert h1.PRESSURE_KPA == pytest.approx(101.2622, abs=0.001)
    assert h1.GAMMA == pytest.approx(0.067339, abs=0.000001)


# --- the year, with the package's tolerances ---------------------------------

YEAR = {
    "A": {"states": {"NIGHT": 4247, "LIGHT_OPEN": 2083, "SHADE": 2058, "RAIN_SHUT": 372},
          "rain": 0.0, "irrigation": 216.9, "use": 237.4, "share": 0.000,
          "soil_min": 18.05, "soil_max": 54.0},
    "B": {"states": {"NIGHT": 4247, "LIGHT_OPEN": 2489, "SHADE": 1652,
                     "RAIN_SHUT": 241, "RAIN_OPEN": 131},
          "rain": 224.4, "irrigation": 108.5, "use": 338.5, "share": 0.674,
          "soil_min": 18.0, "soil_max": 59.63},
    # A Massachusetts year reaches the 32.2 C shading trigger in 5 hours, against 645
    # at the Apopka site, so the blueberry is open for light almost all year.
    "C": {"states": {"NIGHT": 4247, "LIGHT_OPEN": 4136, "HEAT_SHADE": 5,
                     "RAIN_SHUT": 263, "RAIN_OPEN": 109},
          "rain": 169.1, "irrigation": 578.4, "use": 749.6, "share": 0.226,
          "soil_min": 18.0, "soil_max": 54.81},
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
    assert int(year["A"][6]) == pytest.approx(307, abs=3)
    assert int(year["B"][6]) == pytest.approx(275, abs=3)


# --- the demo day ------------------------------------------------------------

def test_demo_day_soil_at_midnight(run):
    for zone, want in (("A", 33.89), ("B", 20.40), ("C", 48.02)):
        rows = local_hour_rows(run, DEMO_DAY, zone)
        assert rows[5]["soil_mm"] == pytest.approx(want, abs=0.02), zone


def test_demo_day_three_zones_three_answers(run):
    """The whole product in one afternoon. At 14:00 it rains 5.3 mm."""
    a = local_hour_rows(run, DEMO_DAY, "A")
    b = local_hour_rows(run, DEMO_DAY, "B")
    c = local_hour_rows(run, DEMO_DAY, "C")

    assert a[10]["state"] == "LIGHT_OPEN" and a[11]["state"] == "SHADE"
    assert a[10]["light_mol_so_far"] == pytest.approx(10.32, abs=0.02)
    assert b[11]["state"] == "LIGHT_OPEN" and b[12]["state"] == "SHADE"
    assert b[11]["light_mol_so_far"] == pytest.approx(14.31, abs=0.02)

    # One storm hour, and the three zones answer it three ways.
    assert a[14]["state"] == "RAIN_SHUT" and a[14]["reason"] == "opted_out"
    assert b[14]["state"] == "RAIN_OPEN"
    assert c[14]["state"] == "RAIN_SHUT" and c[14]["reason"] == "wet_enough"

    assert b[13]["soil_mm"] == pytest.approx(19.23, abs=0.02)
    assert b[14]["soil_mm"] == pytest.approx(24.14, abs=0.02)
    assert c[13]["soil_mm"] == pytest.approx(46.04, abs=0.02)
    assert c[19]["soil_mm"] == pytest.approx(45.07, abs=0.02)

    # The evening shower falls too late in the day to dry, so even the hydrangea shuts.
    assert b[19]["state"] == "RAIN_SHUT" and b[19]["reason"] == "no_drying_time"


def test_demo_day_the_price_of_the_rain_rule(run):
    b = local_hour_rows(run, DEMO_DAY, "B")
    stored = sum(row["rain_in_mm"] for row in b.values())
    assert stored == pytest.approx(5.3, abs=0.1), "the whole storm fits under the 60 mm cap"
    assert b[19]["light_mol_so_far"] - b[11]["light_mol_so_far"] == pytest.approx(4.43, abs=0.05)


def test_demo_day_has_no_heat_shade(run):
    peak = max(h["t2m"] for h in run["weather"]
               if h["ts"].astimezone(LOCAL_TZ).strftime("%Y-%m-%d") == DEMO_DAY)
    assert peak == pytest.approx(19.86, abs=0.02)
    for zone in "ABC":
        assert all(row["state"] != "HEAT_SHADE"
                   for row in local_hour_rows(run, DEMO_DAY, zone).values())


def demo_day_storm_hour(h1, scale):
    """What each zone does in the storm hour when evaporation is nudged by `scale`."""
    _, weather, runs = h1.build(write=False, et_scale=scale)
    out = {}
    for zone in "ABC":
        for hour, row in zip(weather, runs[zone]):
            local = hour["ts"].astimezone(LOCAL_TZ)
            if local.strftime("%Y-%m-%d") == DEMO_DAY and local.hour == 14:
                out[zone] = (row["state"], row["reason"])
    return out


@pytest.mark.parametrize("scale", ET_SCALES)
def test_the_fern_holds_under_a_nudged_evaporation(h1, scale):
    """The fern opts out of rain outright, so no evaporation assumption can move it."""
    assert demo_day_storm_hour(h1, scale)["A"] == ("RAIN_SHUT", "opted_out")


def test_where_the_demo_day_stops_being_robust(h1):
    """How far to trust the other two zones, recorded rather than asserted away.

    At the Apopka site the fern and the blueberry held across the whole sweep and the
    hydrangea was the fragile one. Here it is the other way round, and for a different
    reason: the margins on this day are wide (the blueberry's soil is 46.04 mm against
    a 30 mm latch) but the soil latch is path dependent, so a year run at a slightly
    different evaporation arrives at the storm in a different state.

    Each zone holds its baseline answer in four of the six nudged runs. This test pins
    the exact flips so a change in the rules cannot quietly widen them.
    """
    flips = {zone: sorted(scale for scale in ET_SCALES
                          if demo_day_storm_hour(h1, scale)[zone][0] != baseline)
             for zone, baseline in (("B", "RAIN_OPEN"), ("C", "RAIN_SHUT"))}
    assert flips["B"] == [1.01, 1.05], "the hydrangea shuts, wet enough, at these scales"
    assert flips["C"] == [1.03, 1.05], "the blueberry opens for the rain at these scales"


# --- it runs with the network off, and repeats itself ------------------------

def test_builds_with_the_network_off(h1, monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("H1 opened a socket, and it must run with the network off")

    monkeypatch.setattr(socket, "socket", refuse)
    crops, weather, runs = h1.build(write=False)
    assert len(weather) == 8760 and len(runs) == 3


def test_two_runs_give_identical_bytes(h1, tmp_path, monkeypatch):
    before = {name: (PROCESSED / name).read_bytes() for name in
              ("weather-boston.csv", "sim-boston.csv", "sim-summary-boston.csv")}
    h1.build(write=True)
    after = {name: (PROCESSED / name).read_bytes() for name in before}
    assert before == after
