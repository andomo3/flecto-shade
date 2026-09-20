"""Gate F14: every sourced number has its source.

Every row of data/crops.csv carries an address in both source columns, and nothing else.
"""

import csv
from pathlib import Path

CROPS = Path(__file__).resolve().parents[2] / "data" / "crops.csv"


def test_every_crop_row_has_both_sources():
    with open(CROPS, newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows, "crops.csv is empty"
    for row in rows:
        for column in ("light_source_url", "kc_source_url"):
            value = row[column].strip()
            assert value.startswith("http"), f"{row['zone']} has no address in {column}"
