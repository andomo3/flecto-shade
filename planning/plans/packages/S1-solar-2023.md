# S1: the sun for Houston in 2023, the same year as the rain

Planned on 2026-09-19 by a planning agent that downloaded and read the real file.
It replaces package C6, the PVGIS typical year, for this plan.
VERIFIED means fetched or computed from the real file that day, and ASSUMED means it was not.

## Why the source changed

The first plan joined a typical year of sun, stitched from 2005 to 2014, to the rain of 2023.
A check on the real files showed what that does: in the joined data the rainy daylight hours are brighter than the dry ones, by a ratio of 1.11, because the two have nothing to do with each other.
With the sun from 2023 the ratio is 0.436, so rainy hours are darker, as they are outside.
A demo where rain falls under a clear sky is wrong in a way any judge can see, so the sun comes from 2023.

## Goal

Turn the NASA POWER hourly file for Houston Hobby, 2023, into `data/processed/year-houston-2023.csv`, one row an hour, in UTC, with the local hour.
It runs with the network off, gives identical bytes on every run, and needs no new dependency.

`pvlib` is not used.
Nothing in this plan needs the sun's position, because the roof reacts to how much light arrives and not to where the sun is.

## Inputs, VERIFIED

- `hack-mit/data/raw/nasa-power/power-hourly-houston-hobby-2023.csv`, 340,342 bytes, sha256 `ddace1f61931cd130e71d1947c2d4c5fe3cdc99872d62cd03dac1a0fa8943feb`.
  A person copies it into `flecto-stop/data/raw/nasa-power/` and checks the sha256.
- The request that produced it, HTTP 200, the whole year in one call:
  `https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_DNI,ALLSKY_SFC_SW_DIFF,T2M,PRECTOTCORR&community=RE&longitude=-95.28212&latitude=29.64586&start=20230101&end=20231231&format=CSV&time-standard=UTC`
- The coordinates are the rain gauge's own, from the ISD file: latitude 29.64586, longitude -95.28212, elevation 13.2 m.
- 8,774 lines: 13 header lines from `-BEGIN HEADER-` to `-END HEADER-`, the column row on line 14, then 8,760 data rows, so the file is read with 13 rows skipped.
- Columns: `YEAR,MO,DY,HR,ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_DNI,ALLSKY_SFC_SW_DIFF,T2M,PRECTOTCORR`.
- Units, as the header states them: the three irradiances in Wh/m^2, from CERES SYN1deg, temperature in C and precipitation in mm/hour, from MERRA-2.
  Wh/m^2 over one hour is the mean W/m^2 for that hour, so there is nothing to convert.
- The missing value code is -999, and the file holds none. The index is unique and in order.
- The grid is coarse: 1 degree for the irradiance and half a degree by five eighths for the rest, from NASA's own sources page.
- The timestamp labels the start of the hour, and the value is the hour's mean.
  NASA's pages do not say so in a sentence that was found, so this is VERIFIED only by a fit: global against direct and diffuse closes best with the sun taken half an hour after the stamp, an error of 14.8 W/m2 against 33.2 at the stamp and 34.0 an hour after.
  It matters here only for joining to the rain, and both files are hour starts.
- NASA's own precipitation column is not used, anywhere.
  It is reanalysis, it has 4,523 wet hours where the gauge has 381, and it puts the year's wettest day on 7 April where the gauge has 26 October.

## Output

`data/processed/year-houston-2023.csv`, 8,760 rows, LF line endings:

| Column | Type | Note |
|---|---|---|
| `hour` | int | 0 to 8759 |
| `time_utc` | ISO 8601 | the start of the hour, as in the raw file |
| `month` | int | 1 to 12, from the UTC stamp |
| `source_year` | int | 2023 |
| `local_hour` | int | 0 to 23, America/Chicago |
| `ghi` | float, 2 decimals | W/m2, the hour's mean, from `ALLSKY_SFC_SW_DWN` |
| `dni` | float, 2 decimals | W/m2, from `ALLSKY_SFC_SW_DNI` |
| `dhi` | float, 2 decimals | W/m2, from `ALLSKY_SFC_SW_DIFF` |
| `t2m` | float, 2 decimals | degrees C |

Example: `4460,2023-07-05T20:00:00Z,7,2023,15,625.92,444.24,226.28,32.10`.
The hour index 4460 is 185 days times 24 plus 20, ASSUMED, and the test confirms it.

## Dependencies

`pandas==2.2.3`, `numpy==2.2.3`, `pytest==9.0.2`, all already on the demo laptop.
These are the first lines of `software/requirements.txt`, every line pinned with `==`.

## Steps

1. Read the file with 13 rows skipped. Check: 8,760 rows, the nine column names above, and no -999, failing loudly if there is one.
2. Build the UTC index from `YEAR`, `MO`, `DY`, `HR`. Check: it runs from `2023-01-01T00` to `2023-12-31T23`, unique and in order.
3. Rename the columns, set `source_year`, take `month` from UTC and `local_hour` from America/Chicago. Check: `local_hour` at `2023-07-05T20:00Z` is 15.
4. Write the file. Check: two runs give identical bytes, and no value is negative or `-0.0`.

## Acceptance

- `python data/build_solar_2023.py` exits 0 with the network off.
- `pytest software/tests/test_solar_2023.py` exits 0.

Test cases, from the real file, with the sums within 1:

- One test patches `socket.socket` to raise, then runs the build.
- 8,760 rows, and the header is exactly the nine columns above.
- The sum of `ghi` is 1731203.78, of `dni` 1705340.10, of `dhi` 635704.05.
- 4,566 rows have `ghi` above 0.
- The largest `ghi` is 1017.03 at `2023-04-30T18:00Z`.
- `t2m` has a mean of 22.651 and a maximum of 41.13 at `2023-08-27T20:00Z`.
- The row at `2023-07-05T20:00Z`: `ghi` 625.92, `dni` 444.24, `dhi` 226.28, `t2m` 32.10.
- The row at `2023-06-15T18:00Z`: `ghi` 966.88, `dni` 801.97, `dhi` 166.29, `t2m` 33.95.
- By local day: 362 whole days, the sunniest is 2023-04-30 at 8052.33, then 2023-06-27 at 8034.06, and the sunniest in July is 2023-07-17 at 7861.25.

If an expected value does not match, the agent stops and reports it, and does not edit the value.

## Files

May create: `data/build_solar_2023.py`, `data/processed/year-houston-2023.csv`, `data/README.md`, `software/requirements.txt`, `software/tests/test_solar_2023.py`, and one `.gitignore` line for `data/raw/`.
Must not touch: `planning/`, and anything in `hack-mit`.

## The demo day

The page plays one day, and it needs sun and then rain in daylight.
From the real record, days from April to October with at least 5 mm of daytime rain after at least four bright hours:

| Date | Daytime rain, mm | Bright hours before | First rain, local hour | Lowest `ghi` during the rain |
|---|---|---|---|---|
| 2023-06-05 | 17.1 | 4 | 14 | 75 |
| 2023-06-08 | 32.5 | 7 | 17 | 119 |
| 2023-06-23 | 10.7 | 9 | 19 | 3 |
| 2023-04-12 | 8.3 | 7 | 16 | 288 |
| 2023-07-25 | 40.1 | 5 | 14 | 692 |

The pick is **2023-06-05**, because the sun collapses as the rain arrives.
Its `ghi` from local 06:00 to 19:00: 8, 78, 208, 352, 602, 682, 678, 651, 243, 128, 75, 95, 19, 20.
Its rain at local 14, 15, 16, and 17: 8.9, 6.9, 0.3, 1.0 mm.
The runner up is 2023-06-08, brighter and raining late.
2023-07-25 is rejected: 40 mm fell at the gauge while the satellite cell stayed at about 700 W/m2, which is the coarse grid missing a local storm.
Whether the roof's rules actually produce the demo's story on 5 June is being checked by the planner of package H1, and the pick waits for that.

## Honesty labels

- On the screen: "Houston Hobby, 2023, a real year. Sun: NASA POWER, a satellite product for a cell about 100 km across, hourly means, modelled. Rain: one NOAA gauge, measured."
- The sun is never called measured.
- A local storm can rain under a bright cell, and the README says so with the 25 July example.

## Citations

- "The data was obtained from National Aeronautics and Space Administration (NASA) Langley Research Center's Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division."
- "The data was obtained from the POWER Project's Hourly 2.10.2 version on 2026/09/19."
- No licence text was found on NASA's referencing page, and the submission says so.

## Estimated minutes

30.
