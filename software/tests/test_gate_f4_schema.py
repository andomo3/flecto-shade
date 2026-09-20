"""Gate F4: every output file has the schema its package gives.

Asserts columns, their order, and row counts, and nothing else.
Covers the year file from S1 as well as H1's own files.
"""

import csv
from pathlib import Path

PROCESSED = Path(__file__).resolve().parents[2] / "data" / "processed"

SCHEMAS = {
    "year-boston-2023.csv": (
        ["hour", "time_utc", "month", "source_year", "local_hour", "ghi", "dni", "dhi", "t2m"], 8760),
    "weather-boston.csv": (
        ["hour", "time_utc", "month", "source_year", "local_hour",
         "ghi", "dni", "dhi", "t2m", "rain_mm"], 8760),
    "sim-boston.csv": (
        ["hour", "time_utc", "zone", "crop", "open_fraction", "light_mol_so_far",
         "soil_mm", "rain_in_mm", "irrigation_mm", "state", "reason"], 26280),
}


def test_every_processed_file_matches_its_schema():
    for name, (columns, rows) in SCHEMAS.items():
        path = PROCESSED / name
        assert path.exists(), f"{name} is missing"
        with open(path, newline="") as handle:
            reader = csv.reader(handle)
            assert next(reader) == columns, f"{name} columns"
            assert sum(1 for _ in reader) == rows, f"{name} row count"
