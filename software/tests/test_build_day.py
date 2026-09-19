"""C6: the Houston day is real data, and the day the app plays is the file."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd

from tools.build_day import (
    CITIES,
    COLUMNS,
    ROWS,
    read_tmy,
    sunniest_day,
    to_led,
    to_steps,
    to_sun_angle,
)

PROCESSED = Path(__file__).resolve().parents[2] / "data" / "processed"
HOUSTON = PROCESSED / "day-houston.csv"

TMY = """Latitude (decimal degrees): 29.760
Longitude (decimal degrees): -95.370
Elevation (m): 18.0
Irradiance Time Offset (h): 0.5

month,year
1,2014

time(UTC),T2m,RH,G(h),Gb(n),Gd(h),IR(h),WS10m,WD10m,SP
20140101:0600,14.1,66.65,0.0,-0.0,0.0,331.94,1.85,109.0,102551.0
20140101:1800,20.0,50.00,500.0,300.0,200.0,340.00,2.00,120.0,102500.0
20140102:0600,15.0,60.00,10.0,0.0,10.0,331.00,1.00,100.0,102000.0
20140102:1800,21.0,40.00,100.0,50.0,50.0,339.00,1.50,110.0,102400.0

P: PV system power
"""


def test_the_header_block_and_the_footer_are_not_data(tmp_path):
    path = tmp_path / "tmy.csv"
    path.write_text(TMY, encoding="utf-8")
    frame, offset = read_tmy(path)
    assert offset == 0.5
    assert len(frame) == 4
    assert frame["G(h)"].max() == 500.0
    assert str(frame.index.tz) == "UTC"


def test_the_demo_day_is_the_sunniest_local_day(tmp_path):
    path = tmp_path / "tmy.csv"
    path.write_text(TMY, encoding="utf-8")
    frame, _ = read_tmy(path)
    day = sunniest_day(frame, "America/Chicago")
    assert {stamp.date().isoformat() for stamp in day.index} == {"2014-01-01"}


def test_duty_is_dark_at_night_and_full_at_full_sun():
    duty = to_led(np.array([0.0, 500.0, 1000.0, 1200.0]))
    assert list(duty) == [0, 128, 255, 255]


def test_the_sun_arm_rides_the_arc_from_east_to_west():
    elevation = np.array([-10.0, 20.0, 80.0, 20.0, -10.0])
    azimuth = np.array([80.0, 100.0, 170.0, 260.0, 280.0])
    angles = to_sun_angle(elevation, azimuth)
    assert angles[0] == 0  # Before sunrise the arm waits at the east horizon.
    assert angles[4] == 180  # After sunset it waits at the west.
    assert angles[1] < angles[2] < angles[3]
    assert set(angles) <= set(range(181))


def test_the_day_is_resampled_to_one_minute_of_ten_hertz(tmp_path):
    path = tmp_path / "tmy.csv"
    path.write_text(TMY, encoding="utf-8")
    frame, _ = read_tmy(path)
    day = sunniest_day(frame, "America/Chicago")
    position = pd.DataFrame(
        {"apparent_elevation": [-5.0, 60.0], "azimuth": [90.0, 250.0]},
        index=day.index,
    )
    steps = to_steps(day, position)
    assert list(steps.columns) == COLUMNS
    assert len(steps) == ROWS
    assert steps["step"].tolist() == list(range(ROWS))
    assert steps["ghi"].min() >= 0


def test_the_committed_houston_day_is_playable():
    assert HOUSTON.exists(), "run tools/build_day.py --city houston"
    rows = list(csv.DictReader(HOUSTON.open(encoding="utf-8")))
    assert len(rows) == ROWS
    assert list(rows[0]) == COLUMNS

    duty = [int(row["led"]) for row in rows]
    angles = [int(row["sun_angle"]) for row in rows]
    assert duty[0] == 0 and duty[-1] == 0
    assert max(duty) >= 240
    assert all(0 <= value <= 255 for value in duty)
    assert all(0 <= value <= 180 for value in angles)

    dates = {row["local_time"][:10] for row in rows}
    assert len(dates) == 1, "one real date, shown on screen"


def test_houston_is_the_city_the_story_is_about():
    houston = CITIES["houston"]
    assert (houston.latitude, houston.longitude) == (29.76, -95.37)
    assert houston.timezone == "America/Chicago"
