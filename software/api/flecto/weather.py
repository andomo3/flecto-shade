"""The historical weather a run is measured against, read once and hashed.

The page and the API read the same file, `software/page/day.json`, written by package
H2 from package H1's output. A run stores the hash of the hours it used, so a run can
always say which inputs produced it even after the file is rebuilt.
"""

import json
from pathlib import Path

from .errors import ApiError

_API_DIR = Path(__file__).resolve().parents[1]
DAY_CANDIDATES = (
    _API_DIR.parent / "page" / "day.json",
    _API_DIR.parent.parent / "software" / "page" / "day.json",
)


def day_path():
    for candidate in DAY_CANDIDATES:
        if candidate.exists():
            return candidate
    raise ApiError(
        "The simulated day file is missing. Run python software/page/build_day.py.",
        code="weather_snapshot_missing", status=503,
    )


def load_day():
    return json.loads(day_path().read_text(encoding="utf-8"))


def hours_from(day):
    return [{
        "local_hour": hour["local_hour"],
        "ghi": float(hour["ghi"]),
        "rain_mm": float(hour["rain_mm"]),
        "t2m": float(hour["t2m"]),
        "play_seconds": float(hour["play_seconds"]),
    } for hour in day["hours"]]
