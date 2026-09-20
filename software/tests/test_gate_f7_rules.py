"""Gate F7: the rules are deterministic, and only the rules act.

Two runs of the simulation give identical bytes, every state is one of the names in
H1's nine rules, no RAIN_OPEN occurs where ghi is 0, and no zone that opted out takes
in rain. Asserts that and nothing else.
"""

import csv
import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = REPO_ROOT / "data" / "processed"
BUILD = REPO_ROOT / "software" / "h1" / "build.py"
SIM = PROCESSED / "sim-boston.csv"


def load_build():
    spec = importlib.util.spec_from_file_location("h1_build", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sim_rows():
    with open(SIM, newline="") as handle:
        return list(csv.DictReader(handle))


def test_two_runs_give_identical_bytes():
    build = load_build()
    names = ["weather-boston.csv", "sim-boston.csv", "sim-summary-boston.csv"]
    before = {name: (PROCESSED / name).read_bytes() for name in names}
    build.build(write=True)
    after = {name: (PROCESSED / name).read_bytes() for name in names}
    assert before == after


def test_every_state_is_one_of_the_nine_rules_names():
    build = load_build()
    for row in sim_rows():
        assert row["state"] in build.STATES, row["state"]
        if row["reason"]:
            assert row["reason"] in build.REASONS, row["reason"]
            assert row["state"] == "RAIN_SHUT", "only RAIN_SHUT carries a reason"


def test_no_rain_open_in_the_dark():
    weather = {}
    with open(PROCESSED / "weather-boston.csv", newline="") as handle:
        for row in csv.DictReader(handle):
            weather[row["time_utc"]] = float(row["ghi"])
    for row in sim_rows():
        if row["state"] == "RAIN_OPEN":
            assert weather[row["time_utc"]] > 0, f"RAIN_OPEN in the dark at {row['time_utc']}"


def test_no_zone_that_opted_out_takes_in_rain():
    with open(REPO_ROOT / "data" / "crops.csv", newline="") as handle:
        opted_out = {row["zone"] for row in csv.DictReader(handle) if row["rain_ok"] == "0"}
    assert opted_out, "no zone opts out, so this gate would prove nothing"
    for row in sim_rows():
        if row["zone"] in opted_out:
            assert float(row["rain_in_mm"]) == 0.0, f"zone {row['zone']} took in rain"
            assert row["state"] != "RAIN_OPEN"
