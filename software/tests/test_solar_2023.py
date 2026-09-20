"""Tests for S1, the 2023 sun for the Greater Boston area.

Every expected value here was recomputed from the real NASA POWER file for the Boston
Logan International Airport gauge on 2026-09-20, when the project moved from the Apopka
site to a Massachusetts one. The Apopka figures the planner quoted in
`planning/plans/packages/S1-solar-2023.md` describe the old site and no longer apply.
If a value here does not match, stop and report it. Never edit one to make a test pass:
change it only when the underlying dataset is deliberately replaced, as it was here.
"""

import importlib.util
import socket
from pathlib import Path

import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPT = REPO_ROOT / "data" / "build_solar_2023.py"

OUT_COLUMNS = ["hour", "time_utc", "month", "source_year", "local_hour", "ghi", "dni", "dhi", "t2m"]


def load_builder():
    """Load data/build_solar_2023.py by path, because data/ is not an importable package."""
    spec = importlib.util.spec_from_file_location("build_solar_2023", BUILD_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def builder():
    return load_builder()


@pytest.fixture(scope="module")
def built(builder, tmp_path_factory):
    """Build the file once into a temporary directory and read it back."""
    out = tmp_path_factory.mktemp("processed") / "year-boston-2023.csv"
    builder.build(out_path=out)
    return pd.read_csv(out), out


@pytest.fixture(scope="module")
def frame(built):
    return built[0]


@pytest.fixture(scope="module")
def local_days(frame):
    """Sum ghi over local days that hold a whole 24 hours."""
    stamps = pd.to_datetime(frame["time_utc"], utc=True, format="%Y-%m-%dT%H:%M:%SZ")
    local = stamps.dt.tz_convert("America/New_York")
    grouped = frame.groupby(local.dt.date)
    whole = grouped.filter(lambda group: len(group) == 24)
    return whole.groupby(local.loc[whole.index].dt.date)["ghi"].sum()


def row_at(frame, time_utc):
    matched = frame.loc[frame["time_utc"] == time_utc]
    assert len(matched) == 1, f"expected one row at {time_utc}, found {len(matched)}"
    return matched.iloc[0]


def test_builds_with_the_network_off(builder, tmp_path, monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("the build opened a socket, and it must run with the network off")

    monkeypatch.setattr(socket, "socket", refuse)
    out = builder.build(out_path=tmp_path / "year-boston-2023.csv")
    assert out.exists()


def test_rows_and_header(frame):
    assert len(frame) == 8760
    assert list(frame.columns) == OUT_COLUMNS


def test_sums(frame):
    assert frame["ghi"].sum() == pytest.approx(1358153.58, abs=1)
    assert frame["dni"].sum() == pytest.approx(1369747.69, abs=1)
    assert frame["dhi"].sum() == pytest.approx(583321.43, abs=1)


def test_lit_hours(frame):
    assert (frame["ghi"] > 0).sum() == 4513


def test_largest_ghi(frame):
    assert frame["ghi"].max() == pytest.approx(990.33, abs=0.01)
    assert row_at(frame, "2023-05-18T16:00:00Z")["ghi"] == pytest.approx(990.33, abs=0.01)


def test_t2m(frame):
    assert frame["t2m"].mean() == pytest.approx(10.415, abs=0.001)
    assert frame["t2m"].max() == pytest.approx(33.17, abs=0.01)
    assert row_at(frame, "2023-07-05T21:00:00Z")["t2m"] == pytest.approx(33.17, abs=0.01)
    # A New England winter, so 1,259 hours are below zero. Only irradiance is checked
    # for sign; see NON_NEGATIVE_COLUMNS in the builder.
    assert (frame["t2m"] < 0).sum() == 1259


def test_the_example_row(frame):
    row = row_at(frame, "2023-07-05T20:00:00Z")
    assert row["hour"] == 4460
    assert row["month"] == 7
    assert row["source_year"] == 2023
    assert row["local_hour"] == 16
    assert row["ghi"] == pytest.approx(561.42, abs=0.01)
    assert row["dni"] == pytest.approx(596.47, abs=0.01)
    assert row["dhi"] == pytest.approx(169.80, abs=0.01)
    assert row["t2m"] == pytest.approx(31.23, abs=0.01)


def test_a_second_row(frame):
    row = row_at(frame, "2023-06-15T18:00:00Z")
    assert row["local_hour"] == 14
    assert row["ghi"] == pytest.approx(731.38, abs=0.01)
    assert row["dni"] == pytest.approx(519.72, abs=0.01)
    assert row["dhi"] == pytest.approx(271.78, abs=0.01)
    assert row["t2m"] == pytest.approx(22.83, abs=0.01)


def test_whole_local_days(local_days):
    assert len(local_days) == 362


def test_the_sunniest_local_days(local_days):
    ranked = local_days.sort_values(ascending=False)
    assert str(ranked.index[0]) == "2023-05-31"
    assert ranked.iloc[0] == pytest.approx(8523.25, abs=1)
    assert str(ranked.index[1]) == "2023-05-30"
    assert ranked.iloc[1] == pytest.approx(8475.33, abs=1)

    july = local_days[[day.month == 7 for day in local_days.index]]
    assert str(july.idxmax()) == "2023-07-23"
    assert july.max() == pytest.approx(7787.72, abs=1)


def test_two_runs_give_identical_bytes(builder, tmp_path):
    first = builder.build(out_path=tmp_path / "first.csv").read_bytes()
    second = builder.build(out_path=tmp_path / "second.csv").read_bytes()
    assert first == second


def test_line_endings_are_lf(built):
    raw = built[1].read_bytes()
    assert b"\r" not in raw
    assert raw.endswith(b"\n")


def test_no_negative_irradiance_and_no_minus_zero(built):
    frame, path = built
    for column in ["ghi", "dni", "dhi"]:
        assert (frame[column] >= 0).all()
    assert "-0.00" not in path.read_text(encoding="utf-8")


def test_the_demo_day_still_feeds_h2s_playback(frame):
    """H2's playback timing follows from one property of S1's output.

    It is how many hours of 2023-06-10, the demo day, are lit. Asserting it here means a
    change to S1 cannot break H2's timing silently. The seconds below were recomputed
    from this file on 2026-09-20, with the site; the speeds themselves are unchanged.
    """
    stamps = pd.to_datetime(frame["time_utc"], utc=True, format="%Y-%m-%dT%H:%M:%SZ")
    local = stamps.dt.tz_convert("America/New_York")
    day = frame[local.dt.strftime("%Y-%m-%d") == "2023-06-10"]
    local_hours = local.loc[day.index].dt.hour

    assert len(day) == 24
    lit = sorted(local_hours[day["ghi"] > 0])
    assert lit == list(range(5, 20)), "the demo day must have 15 lit hours, local 5 to 19"

    # H2 plays a lit hour in 2.4 seconds and a dark one in 0.5.
    play_seconds = day["ghi"].apply(lambda ghi: 2.4 if ghi > 0 else 0.5)
    assert play_seconds.sum() == pytest.approx(40.5, abs=0.1)
    # By the end of local hour 10, when the fern's fins shut, and of local hour 14,
    # the hour the storm falls in.
    assert play_seconds[local_hours <= 10].sum() == pytest.approx(16.9, abs=0.1)
    assert play_seconds[local_hours <= 14].sum() == pytest.approx(26.5, abs=0.1)


def test_local_hour_and_month_are_in_range(frame):
    assert frame["local_hour"].between(0, 23).all()
    assert frame["month"].between(1, 12).all()
    assert (frame["source_year"] == 2023).all()
    assert list(frame["hour"]) == list(range(8760))
