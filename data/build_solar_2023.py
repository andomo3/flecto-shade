"""S1: the sun for the Greater Boston area in 2023, the same year as the rain.

Reads the NASA POWER hourly file for the Boston Logan International Airport gauge and
writes `data/processed/year-boston-2023.csv`, one row an hour, in UTC, with the local
hour.

The sun comes from a real year rather than a typical one so that rainy hours are dark
hours when this file is joined to the gauge's rain in package H1.

Runs with the network off, and gives identical bytes on every run.
"""

from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = REPO_ROOT / "data" / "raw" / "nasa-power" / "power-hourly-boston-logan-2023.csv"
OUT_PATH = REPO_ROOT / "data" / "processed" / "year-boston-2023.csv"

# The file carries 13 header lines from -BEGIN HEADER- to -END HEADER-, then the
# column row, then 8,760 data rows. VERIFIED on the real file.
HEADER_ROWS = 13
EXPECTED_ROWS = 8760
SOURCE_YEAR = 2023
MISSING_VALUE = -999

# ASSUMED: the timestamp labels the start of the hour and the value is the hour's mean.
# NASA's pages do not say so in a sentence that was found. It rests on a fit done on the
# Houston file, and it matters here only for joining to the rain, which is also hour starts.
LOCAL_TZ = ZoneInfo("America/New_York")

RAW_COLUMNS = [
    "YEAR",
    "MO",
    "DY",
    "HR",
    "ALLSKY_SFC_SW_DWN",
    "ALLSKY_SFC_SW_DNI",
    "ALLSKY_SFC_SW_DIFF",
    "T2M",
    "PRECTOTCORR",
]

# NASA's own precipitation column is not used, anywhere.
# It is reanalysis, and it has 3,742 wet hours where the gauge has 729.
RENAMES = {
    "ALLSKY_SFC_SW_DWN": "ghi",
    "ALLSKY_SFC_SW_DNI": "dni",
    "ALLSKY_SFC_SW_DIFF": "dhi",
    "T2M": "t2m",
}

OUT_COLUMNS = ["hour", "time_utc", "month", "source_year", "local_hour", "ghi", "dni", "dhi", "t2m"]
INT_COLUMNS = ["hour", "month", "source_year", "local_hour"]
FLOAT_COLUMNS = ["ghi", "dni", "dhi", "t2m"]

# Wh/m2 over one hour is the mean W/m2 for that hour, so there is nothing to convert.
# Irradiance cannot be negative. Temperature can, and does, often in a Massachusetts
# winter, so only the three irradiance columns are checked.
NON_NEGATIVE_COLUMNS = ["ghi", "dni", "dhi"]


def read_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Read the raw POWER file and fail loudly if it is not the file we planned against."""
    if not path.exists():
        raise FileNotFoundError(
            f"{path} is missing. It is gitignored on purpose, so each laptop fetches its own "
            "copy. The address and the expected sha256 are in "
            "planning/plans/packages/S1-solar-2023.md"
        )

    frame = pd.read_csv(path, skiprows=HEADER_ROWS)

    if list(frame.columns) != RAW_COLUMNS:
        raise ValueError(f"unexpected columns in {path.name}: {list(frame.columns)}")
    if len(frame) != EXPECTED_ROWS:
        raise ValueError(f"expected {EXPECTED_ROWS} rows in {path.name}, found {len(frame)}")

    missing = (frame == MISSING_VALUE).to_numpy().sum()
    if missing:
        raise ValueError(f"{path.name} holds {missing} values of {MISSING_VALUE}, the missing code")

    return frame


def build_frame(raw: pd.DataFrame) -> pd.DataFrame:
    """Turn the raw frame into the nine output columns."""
    stamps = pd.to_datetime(
        raw[["YEAR", "MO", "DY", "HR"]].rename(
            columns={"YEAR": "year", "MO": "month", "DY": "day", "HR": "hour"}
        ),
        utc=True,
    )

    if not stamps.is_unique:
        raise ValueError("the UTC index is not unique")
    if not stamps.is_monotonic_increasing:
        raise ValueError("the UTC index is not in order")

    first, last = stamps.iloc[0], stamps.iloc[-1]
    if (first.year, first.month, first.day, first.hour) != (SOURCE_YEAR, 1, 1, 0):
        raise ValueError(f"the index starts at {first}, not {SOURCE_YEAR}-01-01T00")
    if (last.year, last.month, last.day, last.hour) != (SOURCE_YEAR, 12, 31, 23):
        raise ValueError(f"the index ends at {last}, not {SOURCE_YEAR}-12-31T23")

    frame = raw.rename(columns=RENAMES)[list(RENAMES.values())].copy()
    frame.insert(0, "hour", range(len(frame)))
    frame.insert(1, "time_utc", stamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ"))
    frame.insert(2, "month", stamps.dt.month)
    frame.insert(3, "source_year", SOURCE_YEAR)
    frame.insert(4, "local_hour", stamps.dt.tz_convert(LOCAL_TZ).dt.hour)

    frame = frame[OUT_COLUMNS]

    for column in NON_NEGATIVE_COLUMNS:
        below = frame.loc[frame[column] < 0, column]
        if not below.empty:
            raise ValueError(f"{column} holds {len(below)} negative values, lowest {below.min()}")

    return frame


def format_rows(frame: pd.DataFrame) -> list[str]:
    """Format every row to fixed width decimals, so two runs give identical bytes."""
    lines = [",".join(OUT_COLUMNS)]
    for row in frame.itertuples(index=False):
        cells = []
        for column, value in zip(OUT_COLUMNS, row):
            if column in INT_COLUMNS:
                cells.append(str(int(value)))
            elif column in FLOAT_COLUMNS:
                # Adding zero turns -0.0 into 0.0, so no cell is ever written as "-0.00".
                cell = f"{float(value) + 0.0:.2f}"
                if cell.startswith("-0.00"):
                    raise ValueError(f"{column} formats to {cell} at hour {row.hour}")
                cells.append(cell)
            else:
                cells.append(str(value))
        lines.append(",".join(cells))
    return lines


def write_csv(frame: pd.DataFrame, path: Path = OUT_PATH) -> Path:
    """Write the file with LF line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(format_rows(frame)) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return path


def build(raw_path: Path = RAW_PATH, out_path: Path = OUT_PATH) -> Path:
    """Read the raw file, build the frame, and write it."""
    return write_csv(build_frame(read_raw(raw_path)), out_path)


def main() -> None:
    path = build()
    frame = pd.read_csv(path)
    print(f"wrote {path.relative_to(REPO_ROOT)}, {len(frame)} rows")
    print(f"  ghi sums to {frame['ghi'].sum():.2f} W/m2, over {(frame['ghi'] > 0).sum()} lit hours")
    print(f"  t2m runs {frame['t2m'].min():.2f} to {frame['t2m'].max():.2f} C")


if __name__ == "__main__":
    main()
