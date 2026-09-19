# F1: how far a fixed rest canopy's shadow drifts, Hanford, summer 2023

Planned on 2026-09-19 by a planning agent that downloaded and read the real files.
[V] means verified by fetching that day, [A] means assumed, and [P] means a rough preview that the build agent must recompute.

## Status: parked

The planner's own verdict is that this is not worth its hours ahead of the Houston analysis, and the reviewer agrees.

- The Houston data is messier, serves Rosa, and has a real trap in it, the transit centres.
- This data is clean and the geometry is simple.
- Its headline swings from about 32 percent to about 80 percent with the canopy size, which is an assumption the team chose. [P]

It is handed over only after V1 to V3 are green, as a side card for the farmworker in the pitch.
F1 is 150 minutes and the optional charts, F2, are 45.

## Goal

Measure how far a fixed rest canopy's shadow moves off a bench during sunny minutes above 80 F at Hanford, California, from June to September 2023.
Report the share of those minutes in which a bench centred under the canopy is partly or wholly in direct sun.

## Inputs, verified

Raw copies are in `hack-mit/data/raw/`, gitignored, and a person copies them into `flecto-stop/data/raw/`.
NOAA's server refused connections for a few minutes after three quick requests, so nobody fetches these again without `--retry 5 --retry-delay 4`.

### SOLRAD Hanford, one minute irradiance

- `solrad-hnx-2023/`: 123 files, 22,322,796 bytes, days 152 to 274 of 2023. [V]
  Day 274 is there because the evening of 30 September in local time falls in the next UTC file.
- The README is `https://gml.noaa.gov/aftp/data/radiation/solrad/README_SOLRAD.txt`. [V]
- Two header lines: ` Hanford`, then `   36.31 -119.63   73 -8 version 1` for days 152 to 156 and `   36.31357 -119.63164   73 -8 version 1` from day 157 on. [V]
  Use 36.31357, -119.63164, elevation 73 m, throughout.
- 22 whitespace separated columns: `year`, `jday`, `month`, `day`, `hour`, `min`, `dt`, `zen`, `dw_psp`, `qc_dwpsp`, `direct`, `qc_direct`, `diffuse`, `qc_diffuse`, `uvb`, `qc_uvb`, `uvb_temp`, `qc_uvb_temp`, `std_dw_psp`, `std_direct`, `std_diffuse`, `std_uvb`. [V]
- A real line: ` 2023 201  7 20  0  0  0.000  52.98   560.6 0   789.7 0    89.5 0    76.2 0    44.3 0     1.258     0.821     0.000     0.312`. [V]
- W/m2, UTC, one minute averages of one second samples, stamped at the end of the minute. [V]
- A flag of 0 is good, and a missing value is -9999.9 with flag 1. [V]
- Every file has exactly 1,440 rows. [V]
- Across days 152 to 273 the direct column has 171,303 good values and 4,377 flagged, 4,342 of them missing, about 60 minutes a day at low sun. [V]

### NCEI ISD hourly temperature

- `isd-2023/72389853119.csv`, Hanford Municipal Airport, KHJO, 36.3114, -119.62319, 76 m, beside the SOLRAD site: 5,642,479 bytes, 10,591 rows. [V]
  This is the temperature source.
- `isd-2023/72389093193.csv`, Fresno, 6,636,374 bytes, 11,267 rows, kept only as a robustness check. [V]
- `DATE` looks like `2023-01-01T00:53:00`, in UTC. [V]
- `TMP` looks like `+0144,5`: tenths of a degree C, then a quality code, and `+9999,9` is missing. [V]
- `REPORT_TYPE` is padded with spaces, such as `SOD  `, so it is stripped. [V]
- Hanford's summer rows: FM-15 2,928, all at minute 53, SOD 122, all missing `TMP`, FM-16 68, SOM 4. [V]
  `TMP` quality 5 in 2,981 rows, 9 in 138, 1 in 2, 6 in 1. [V]
- Keeping quality codes 1 and 5 rests on the codes seen in the data, and their meaning is from memory. [A]
  A person checks it against the ISD format document.

## Cleaning rules

1. Keep a SOLRAD row only if `qc_direct` is 0 and `direct` is above -9999.
2. Drop rows where `zen` is 90 or more.
3. Clip small negative `direct` values to 0.
4. Do not use `dw_psp`.
5. From ISD keep only `REPORT_TYPE` FM-15 and FM-16, stripped.
6. Keep `TMP` quality 1 and 5, and drop `+9999`.
7. If timestamps still repeat, keep the FM-15 row.
8. Join the temperature onto each irradiance minute with `merge_asof`, nearest, tolerance 45 minutes, count the unmatched rows, then drop them.
9. "Hot" is strictly above 80.0 F.
10. Work in UTC, and compute the sun's position at the timestamp minus 30 seconds.
11. Local time is America/Los_Angeles, PDT for the whole window.
12. The window is local dates 2023-06-01 to 2023-09-30, which is `2023-06-01T07:00Z` up to but not including `2023-10-01T07:00Z`.

## Geometry

- The canopy is a flat rectangle, W by D, at height H above the evaluation plane.
- The bench is L by B, centred under it, long axis along W.
- The shadow offset is `d = H / tan(elevation)`, with `dx = -d sin(az)` and `dy = -d cos(az)`, rotated by the canopy's orientation.
- Coverage is the overlap of the shifted canopy rectangle and the bench, divided by the bench area.
- Defaults: W and D 3.05 m, a 10 ft by 10 ft pop up canopy, clearance 2.03 m from a retailer's page, to be spot checked.
  The evaluation plane is the seat, 0.45 m, so H is 1.58 m. [A]
  The bench is 1.8 m by 0.45 m, long axis east to west. [A]
- Sweeps: H from 1.0 to 2.2 m; canopy 3.05 by 3.05, 3.05 by 4.6, and 3.05 by 6.1 m; orientation 0, 45, 90 degrees; direct irradiance threshold 120, 200, 400 W/m2, where 120 is the WMO sunshine definition, cited from memory; temperature from Hanford against Fresno.
- The adaptive comparison is the shade area needed: the smallest centred canopy that keeps coverage at 1.0 for 95 percent of the qualifying minutes, against the default 9.3 m2.
  It is not a claim about the team's leaf, which has two states and has never been outdoors.

## Outputs, under `flecto-stop/data/processed/`

- `shade_minutes.csv`: `ts_utc`, `local_pdt`, `dni_wm2`, `temp_c`, `temp_f`, `elev_deg`, `az_deg`, `offset_m`, `dx_m`, `dy_m`, `coverage` 0 to 1, `qualifies` bool.
  Illustrative row: `2023-07-20T20:00:00Z,2023-07-20 13:00,880.1,35.0,95.0,74.23,175.3,0.45,-0.04,0.45,1.0,True`.
- `shade_daily.csv`: `local_date`, `qualifying_min`, `partly_sun_min`, `wholly_sun_min`, `max_offset_m`, `missing_dni_min`, `tmax_f`.
- `shade_headline.json`: `n_days`, `n_qualifying_min`, `share_partly_or_wholly`, `share_wholly`, `median_offset_m`, `p90_offset_m`, `needed_area_m2`, `assumptions`, `sweep`.

## Dependencies

The shared environment from C6: `pvlib==0.15.2`, `pandas==2.2.3`, `numpy==2.2.3`, `matplotlib==3.10.1`, `pytest==9.0.2`.

## Steps

1. Parse the SOLRAD files. Check: 22 columns, both header variants parse, 1,440 rows each.
2. Parse the ISD file. Check: the row counts by report type above.
3. Clean and join. Check: the counts under Acceptance.
4. Sun position from `pvlib.solarposition.get_solarposition`. Check: the solar noon test.
5. Geometry. Check: the unit tests.
6. Run the sweeps and write the outputs. Check: the schema.
7. F2, optional: three PNG charts, an offset track over one day, the share by local hour, and the sensitivity grid. Check: the files exist.

## Acceptance

`python -m analysis.shade_drift` and `pytest analysis/tests/test_shade_drift.py` exit 0 with the network off.

Expected values from the real files, with 0.5 percent tolerance on the counts:

- Rows in the window: 175,680.
- Rows with `zen` under 90: 100,291.
- Rows with a good direct value: 96,003.
- Hanford temperature observations kept: 2,983.
- Minutes with no temperature match: 565.
- Hot minutes: 62,520.
- Hot minutes with direct irradiance at or above 120: 58,108, across 119 days.
- On 2023-07-20 the file's smallest `zen` is 15.72 at 20:05 UTC, so `pvlib`'s greatest elevation is 74.28 within 0.3 degrees, within 5 minutes of 20:05 UTC.
- At 45 degrees elevation the offset equals H.
- At 89.999 degrees the offset is under 1e-4 times H.
- With the sun due south, `dy` is positive, the shadow falls north, and `dx` is about 0.
- Coverage is 1 at zero offset, and 0 once the offset exceeds half the canopy plus half the bench.

## Files

The agent may create files only under `flecto-stop/data/` and `flecto-stop/analysis/`.
It never touches `flecto-stop/planning/` or the `hack-mit` repo.
One commit, with F1 in the message.

## Honesty labels

- Irradiance and temperature: "measured, NOAA, 2023".
- Sun position: "computed".
- Shadow and coverage: "modelled geometry, assumed canopy and bench, flat ground, direct beam only, no diffuse light, no heat claim".
- The law is quoted and never turned into a finding about anyone's compliance.

## Citations

- "Hicks, B. B., J. J. DeLuisi, D. R. Matt, 1996: The NOAA Integrated Surface Irradiance Study (ISIS), a new surface radiation monitoring program. Bull. Amer. Meteor. Soc., 77, 2857-2864." [V]
  The data licence is CC0 1.0.
- NOAA NCEI Integrated Surface Database, Global Hourly, stations 72389853119 and 72389093193.
- pvlib python, BSD 3 clause. [V]

## What the team would say

"On the [N] summer days when California law required shade and the sun was out, a bench centred under a standard 10 by 10 foot canopy had direct sun on it for [X] percent of those minutes."
A rough preview gave about 73 percent partly or wholly in sun, and about 27 percent wholly. [P]
At 10 by 20 feet it fell to about 32 percent, so the pitch leads with the offset in metres, which depends only on the height and the sun. [P]

The two hardest questions:

1. "Your number is an artefact of the bench and canopy size."
   Yes, which is why we show the whole sensitivity surface and lead with the offset.
2. "Workers move the bench, so what?"
   True. The finding is the area or the moving that is needed, not harm. We measured no worker, no heat, and no leaf.

## Open questions for a person

- The real size of a farm shade trailer, which would replace the pop up canopy assumption.
- Whether the evaluation plane is the seat or the ground.
- The ISD quality codes, checked against the format document.
