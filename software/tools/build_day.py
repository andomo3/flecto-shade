"""C6: turn one real year of Houston weather into one day the demo can play.

Input is a PVGIS typical meteorological year file in ``data/raw/``, downloaded
while there was still a network. Output is ``data/processed/day-<city>.csv``:
600 rows, so twenty four hours play in sixty seconds at ten rows a second, with
the LED duty and the sun servo angle already worked out.

Everything here is modelled from the dataset. The only measured numbers in the
demo are the sensors on the table, and the two are never mixed.

Run: ``python tools/build_day.py --city houston``
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import pvlib

ROWS = 600
FULL_SUN = 1000.0  # W/m2 mapped to LED duty 255.
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
COLUMNS = ["step", "local_time", "ghi", "elevation", "azimuth", "t2m", "led", "sun_angle"]


@dataclass(frozen=True)
class City:
    name: str
    latitude: float
    longitude: float
    timezone: str
    raw: str


CITIES = {
    "houston": City("houston", 29.76, -95.37, "America/Chicago", "tmy-houston-v5_2.csv"),
}


def read_tmy(path: Path) -> tuple[pd.DataFrame, float]:
    """Read a PVGIS v5_2 TMY CSV, past its header block and before its footer.

    Returns the hourly frame indexed in UTC and the file's irradiance time
    offset in hours, which PVGIS states in the header and which shifts the
    timestamp to the middle of the measured interval.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    offset = 0.0
    start = None
    for number, line in enumerate(lines):
        if line.startswith("Irradiance Time Offset"):
            offset = float(line.split(":")[1])
        if line.startswith("time(UTC),"):
            start = number
            break
    if start is None:
        raise ValueError(f"{path}: no time(UTC) header row")

    rows = []
    for line in lines[start + 1 :]:
        if not line or not line[0].isdigit():
            break
        rows.append(line.split(","))

    frame = pd.DataFrame(rows, columns=lines[start].split(","))
    frame["time(UTC)"] = pd.to_datetime(frame["time(UTC)"], format="%Y%m%d:%H%M", utc=True)
    for column in ("T2m", "G(h)", "Gb(n)", "Gd(h)"):
        frame[column] = frame[column].astype(float)
    return frame.set_index("time(UTC)"), offset


def sunniest_day(frame: pd.DataFrame, timezone: str) -> pd.DataFrame:
    """The local day with the largest total ``G(h)``: the demo's real date."""
    local = frame.tz_convert(timezone)
    totals = local["G(h)"].groupby(local.index.date).sum()
    return local[local.index.date == totals.idxmax()]


def solar_position(day: pd.DataFrame, city: City, offset: float) -> pd.DataFrame:
    """Elevation and azimuth at each hour, from pvlib, not from the file."""
    times = day.index + pd.Timedelta(hours=offset)
    position = pvlib.solarposition.get_solarposition(times, city.latitude, city.longitude)
    return position.set_index(day.index)


def to_led(ghi: np.ndarray) -> np.ndarray:
    """0 W/m2 is dark, FULL_SUN is the brightest the LED goes."""
    return np.clip(np.round(ghi / FULL_SUN * 255), 0, 255).astype(int)


def to_sun_angle(elevation: np.ndarray, azimuth: np.ndarray) -> np.ndarray:
    """The lamp arm rides the day's arc: 0 is the east horizon, 90 overhead,
    180 the west horizon.

    Elevation sets how far along the arc the sun is, and azimuth says which
    side of noon it is on. Below the horizon the arm waits at the horizon it
    is nearest, because a servo cannot go under the table.
    """
    peak = max(float(np.max(elevation)), 1.0)
    along = np.clip(elevation, 0, None) / peak * 90
    morning = azimuth < 180
    return np.round(np.where(morning, along, 180 - along)).astype(int)


def to_steps(day: pd.DataFrame, position: pd.DataFrame, rows: int = ROWS) -> pd.DataFrame:
    """Interpolate the hourly day onto ``rows`` evenly spaced steps."""
    seconds = (day.index - day.index[0]).total_seconds().to_numpy()
    span = np.linspace(0, 24 * 3600, rows, endpoint=False)

    def over(values: pd.Series) -> np.ndarray:
        return np.interp(span, seconds, values.to_numpy())

    ghi = np.clip(over(day["G(h)"]), 0, None)
    elevation = over(position["apparent_elevation"])
    azimuth = over(position["azimuth"])
    stamps = day.index[0] + pd.to_timedelta(span, unit="s")

    return pd.DataFrame(
        {
            "step": np.arange(rows),
            "local_time": stamps.strftime("%Y-%m-%d %H:%M:%S"),
            "ghi": np.round(ghi, 1),
            "elevation": np.round(elevation, 2),
            "azimuth": np.round(azimuth, 2),
            "t2m": np.round(over(day["T2m"]), 2),
            "led": to_led(ghi),
            "sun_angle": to_sun_angle(elevation, azimuth),
        },
        columns=COLUMNS,
    )


def build(city: City, raw_dir: Path = RAW, out_dir: Path = PROCESSED) -> Path:
    frame, offset = read_tmy(raw_dir / city.raw)
    day = sunniest_day(frame, city.timezone)
    position = solar_position(day, city, offset)
    steps = to_steps(day, position)

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"day-{city.name}.csv"
    steps.to_csv(out, index=False, lineterminator="\n")
    print(
        f"{out}: {len(steps)} steps, {steps['local_time'][0][:10]}, "
        f"peak {steps['ghi'].max()} W/m2, peak {steps['t2m'].max()} C, "
        f"peak duty {steps['led'].max()}"
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--city", default="houston", choices=sorted(CITIES))
    arguments = parser.parse_args()
    build(CITIES[arguments.city])


if __name__ == "__main__":
    main()
