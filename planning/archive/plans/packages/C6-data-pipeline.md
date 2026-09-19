# C6: the data pipeline, PVGIS Houston typical year to the demo day and the year file

Planned on 2026-09-19 by a planning agent that downloaded and read the real file.
"Verified" means read from the real file or fetched that day, and "assumed" means it was not.

## Goal

Turn the raw PVGIS v5_2 Houston file into `data/processed/day-houston.csv`, 600 rows of one day, and `data/processed/year-houston.csv`, 8,760 rows, with the sun's position from `pvlib`.
The build runs with the network off and gives identical bytes on every run.

## The demo day: 5 July 2013

The sunniest day of the file is 3 June 2013, and the pitch opens with "three in the afternoon in July".
So the day file is the sunniest July day, 5 July 2013, which is what the screen shows.

- It is rank 4 of 358 whole local days, 3.05 percent below 3 June, a difference nobody can see on an LED. Verified.
- It is a clean single peak with no cloud dips, in both `ghi` and `dni`. Verified.
- At 15:00 local the file reads 915 W/m2 and 34.32 C, so the pitch's line is literally a row on the screen. Verified.
- No row clamps at LED duty 255, so the full scale question disappears. Verified.
- The screen label is "5 July 2013, the sunniest July day in the PVGIS typical year for Houston, modelled".
  It is never called the sunniest day of the year.
- Fallbacks if this day is ever rejected: 18 July 2013, sum 7803.0, then 3 June 2013.
  31 July has an odd temperature curve and is avoided.

This replaces the line in `../../data/CLAUDE.md` that says the demo day is the sunniest day in the file, and a person confirms it before the package is handed over.

## Inputs, verified from the real file

- `hack-mit/data/raw/pvgis-tmy-houston-v5_2.csv`, 594,218 bytes, sha256 `0ab9fa1b1fa605f6f691a13c1f4fb55b9d9e7eb80f8533651e70bb2cd12c1867`, CRLF line endings, 8,790 lines.
  Source: `https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=29.76&lon=-95.37&outputformat=csv`, HTTP 200 on 2026-09-19.
- A spare, `pvgis-tmy-houston-v5_3.csv`, 599,170 bytes, is in the same folder.
  Its time offset is 0.5 and its source years differ, so it is not a drop in replacement and is not used.
- Lines 1 to 4: `Latitude (decimal degrees): 29.760`, `Longitude (decimal degrees): -95.370`, `Elevation (m): 18.0`, `Irradiance Time Offset (h): 0.0`.
- Line 5 is `month,year`, and lines 6 to 17 give the source year of each month: 1 2014, 2 2008, 3 2005, 4 2008, 5 2007, 6 2013, 7 2013, 8 2013, 9 2013, 10 2013, 11 2005, 12 2005.
- Line 18 is the column row: `time(UTC),T2m,RH,G(h),Gb(n),Gd(h),IR(h),WS10m,WD10m,SP`.
- 8,760 data rows, no missing values, no 29 February.
  The first is `20140101:0000,14.1,66.65,0.0,-0.0,0.0,331.94,1.85,109.0,102551.0`.
- The time format is `%Y%m%d:%H%M` in UTC, and the minutes are always 00.
- The footer is a blank line, nine unit lines, a blank line, and `PVGIS (c) European Union, 2001-2026`.
- Irradiance is in W/m2 and `T2m` in degrees Celsius.
- The offset of 0.0 was cross checked: `G(h) = Gb(n) * sin(elevation) + Gd(h)` closes with an error of 1.1 W/m2 at offset 0 and 37 W/m2 at plus or minus half an hour, so the values are instantaneous at the top of the hour.

## Traps, each one hit on the real file

- The time index jumps between years at month edges, so it is not in order, and slicing it by a date string raises a KeyError.
- `Gb(n)` holds `-0.0`.
- Linear interpolation leaves `ghi` above 0 while the sun is down, before sunrise at steps 151 to 162 and after sunset at steps 509 to 524.
- Solar noon in Houston in July is about 13:26 CDT, not noon.
- The azimuth wraps through north at night, so it is never interpolated.
- A spline goes negative, so it is never used.

## Outputs

`day-houston.csv`, 600 rows, one step every 144 seconds, LF line endings:

| Column | Type | Unit | Range |
|---|---|---|---|
| `step` | int | | 0 to 599 |
| `local_time` | ISO 8601 with offset | America/Chicago | `2013-07-05T00:00:00-05:00` to `23:57:36` |
| `ghi`, `dni`, `dhi` | float, 1 decimal | W/m2 | 0 and up |
| `t2m` | float, 2 decimals | degrees C | |
| `elevation` | float, 2 decimals | degrees, `pvlib` `apparent_elevation` | -90 to 90 |
| `azimuth` | float, 2 decimals | degrees from north | 0 to 360 |
| `led` | int | PWM duty | 0 to 255 |
| `sun_angle` | int | servo degrees | 0 to 180 |

Example, step 375, with the last four values approximate until `pvlib` runs: `375,2013-07-05T15:00:00-05:00,915.0,824.0,152.0,34.32,66.0,265.0,233,120`.

`year-houston.csv`, 8,760 rows, in the file's own order:

| Column | Type | Note |
|---|---|---|
| `hour` | int | 0 to 8759 |
| `time_utc` | ISO 8601 | with the real source year |
| `month` | int | 1 to 12, from the UTC timestamp |
| `source_year` | int | |
| `local_hour` | int | 0 to 23, America/Chicago, which package V2 needs |
| `ghi`, `dni`, `dhi` | float | W/m2 |
| `t2m` | float | degrees C |
| `elevation`, `azimuth` | float | degrees |

Example, with the angles approximate: `3690,2013-06-03T18:00:00Z,6,2013,13,1020.0,896.2,134.0,31.72,81.4,148.0`.

## Dependencies, pinned in `software/requirements.txt`

`pvlib==0.15.2`, `pandas==2.2.3`, `numpy==2.2.3`, `scipy==1.15.2`, `h5py==3.16.0`, `pytest==9.0.2`.
`pytz`, `requests`, and `tzdata` arrive with them.

- `pvlib` 0.15.2 is the newest on PyPI, BSD 3 clause, and needs numpy, pandas, pytz, requests, scipy, and h5py. Verified.
- `h5py` 3.16.0 has a wheel for Python 3.13 on Windows. Verified.
- `pvlib` is not installed anywhere on the demo laptop, so it is installed once, while the venue network works. Verified.
- numpy 2.2.3, pandas 2.2.3, scipy 1.15.2, and pytest are already in the system Python 3.13.5. Verified.
- `pvlib` 0.15.2 has not been run against pandas 2.2.3 on this machine. Assumed to work.
- The function signatures were read from the `pvlib` source at tag v0.15.2 and not run:
  `pvlib.iotools.read_pvgis_tmy(filename, pvgis_format=None, map_variables=True)` returns `(data, meta)`, renames the columns to `ghi`, `dni`, `dhi`, `temp_air`, and gives a UTC index, `meta['inputs']['irradiance time offset']`, and `meta['months_selected']`.
  `pvlib.solarposition.get_solarposition(time, latitude, longitude, altitude=None, ...)`.

## Steps

1. A person copies the raw file from `hack-mit/data/raw/` into `flecto-stop/data/raw/` and adds `data/raw/` to `.gitignore`. Check: the sha256 matches.
2. Create the virtual environment and install the pins. Check: `python -c "import pvlib; print(pvlib.__version__)"` prints 0.15.2.
3. Load with `read_pvgis_tmy(path, map_variables=True)`, and read the offset from the metadata, never hard code it. Check: 8,760 rows, offset 0.0, and the columns `ghi`, `dni`, `dhi`, `temp_air`.
4. Replace `-0.0` with `0.0`, and select rows by a boolean mask or by exact timestamps, never by a date string. Check: no `-0.0` in either output.
5. Sun position from `get_solarposition(index + offset, 29.76, -95.37, altitude=18.0)`, keeping `apparent_elevation` and `azimuth`. Check: over the year, no `ghi` above 0 where the elevation is under -1.
6. Write the year file, with `local_hour`. Check: 8,760 rows.
7. Convert to America/Chicago, sum `ghi` per local date, keep only dates with 24 rows in a row, and take the largest, over the whole year by default and within one month with `--month`. Check: no month gives 2013-06-03 and 8341.0, and `--month 7` gives 2013-07-05 and 8087.0.
8. Take the 25 hourly rows from local 00:00 to the next 00:00 and interpolate `ghi`, `dni`, `dhi`, and `t2m` linearly with `numpy.interp` onto 600 steps. Check: the minimum is 0 or more, and `ghi` at step 375 is 915.0.
9. Compute the sun position directly at the 600 timestamps, and set `ghi`, `dni`, and `dhi` to 0 wherever the elevation is 0 or less. Check: `ghi` is 0 across steps 151 to 159 and across steps 512 to 524.
10. `led = clamp(round(255 * ghi / 1000), 0, 255)`, with 1000 as a named constant.
11. `sun_angle = round(degrees(atan2(sin(el), cos(el) * sin(az))))`, the east to west arc, and where the elevation is 0 or less it is 0 before the peak step and 180 after. Check: it never decreases over the day.
12. Wrap it all as `build(city, lat, lon, tz, raw_path, month=None)`. Check: two runs give identical bytes.

## Acceptance

- `python data/build_processed.py --city houston --month 7` exits 0 with the Wi-Fi off.
- `pytest software/tests/test_data_pipeline.py` exits 0.

Test cases, with values computed from the real file:

- One test patches `socket.socket` to raise, then runs the build, to prove it is offline.
- The raw parse: 8,760 rows, offset 0.0, and the twelve source years listed above.
- The year: the sum of `ghi` is 1793390.0, of `dni` 1834836.08, of `dhi` 662874.0, each within 1; the maximum `ghi` is 1039.0 at `2008-04-28T18:00Z`; and 4,231 rows have `ghi` above 0.
- The picker: with no month, 2013-06-03 and a daily sum of 8341.0; with month 7, 2013-07-05 and 8087.0, then 2013-07-18 and 7803.0 as the second.
- The July day, hourly `ghi` from 07:00 to 20:00 local: 52, 236, 446, 643, 809, 926, 985, 981, 915, 792, 622, 420, 212, 48.
- The July day: 600 rows, peak `ghi` 985.0 at 13:00 local, peak `t2m` 34.36 at 16:00 local, and at 15:00 `ghi` 915.0, `dni` 824.0, `dhi` 152.0, `t2m` 34.32.
- The maximum elevation is 83.0 within 0.5, at step 336 within 3.
  The first elevation above 0 is at step 160 to 164, and the last at 507 to 511.
  These three came from an approximation and not from `pvlib`, which is why they carry tolerances.
- `led` is 0 wherever the elevation is 0 or less, its maximum is 251 at step 325, and at step 375 it is 233.
- `sun_angle` never decreases, is under 45 at step 200, is between 80 and 100 at the step of maximum elevation, and is over 135 at step 450.
- No negative value and no `-0.0` anywhere in either file.

If an expected value does not match, the agent stops and reports it, and does not edit the value.

## Files the agent may create

`data/build_processed.py`, `data/README.md`, `data/processed/day-houston.csv`, `data/processed/year-houston.csv`, `software/requirements.txt`, `software/tests/test_data_pipeline.py`, and one line in `.gitignore`.

## Files it must not touch

`flecto-stop/planning/`, and nothing in the `hack-mit` repo is written or read.

## Honesty labels

- Every value in both files is modelled: satellite derived irradiance from a typical year, and a computed sun position.
- The year is never called a real year, because its months come from 2005 to 2014.
- Times are CDT, and the sun peaks near 13:26, not at noon.

## Provenance, licence, citation

The row for `data/README.md`: PVGIS TMY v5_2, Houston 29.76, -95.37, PVGIS-NSRDB, the URL above, downloaded 2026-09-19, 594,218 bytes, feeds `day-houston.csv` and `year-houston.csv`.

- "PVGIS (c) European Union, 2001-2026, CC BY 4.0."
- "pvlib python 0.15.2, BSD 3-Clause, Anderson et al. 2023, Journal of Open Source Software." The DOI, 10.21105/joss.05994, is from memory and is confirmed before it is printed.

## Open questions for a person

1. Does the sun mount sweep east to west, which step 11 assumes? The engineers answer this, and under Plan B it does not matter.
2. Confirm 5 July 2013 as the demo day.

## Estimated minutes

75.
