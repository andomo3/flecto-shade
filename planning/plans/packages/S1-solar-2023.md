# S1: the sun for the Apopka area in 2023, the same year as the rain

Planned on 2026-09-19 by planning agents that downloaded and read the real file.
The method was first run on files for another Gulf Coast site, and every value below was recomputed from the Florida file.
VERIFIED means fetched or computed from the real file that day, and ASSUMED means it was not.

## Why the sun is from a real year and not a typical one

An earlier plan joined a typical year of sun, stitched from several years, to one real year of rain.
A check on real files, done for another Gulf Coast site, showed what that does: the rainy daylight hours came out brighter than the dry ones, by a ratio of 1.11, because the two had nothing to do with each other.
With the sun from the same year as the rain, rainy hours are darker, as they are outside: the ratio is 0.627 for this file.
A demo where rain falls under a clear sky is wrong in a way any judge can see.

## Goal

Turn the NASA POWER hourly file for the Orlando Executive Airport gauge, 2023, into `data/processed/year-apopka-2023.csv`, one row an hour, in UTC, with the local hour.
It runs with the network off, gives identical bytes on every run, and needs no new dependency.

`pvlib` is not used.
Nothing in this plan needs the sun's position, because the roof reacts to how much light arrives and not to where the sun is.

## Inputs, VERIFIED

- `hack-mit/data/raw/nasa-power/power-hourly-orlando-executive-2023.csv`, 340,893 bytes, sha256 `c81490d249cb1fc857b0edf44c54d6fcdbc7c1e5b30b326310138a10f25cefc4`.
  A person copies it into `flecto-shade/data/raw/nasa-power/` and checks the sha256.
- The request that produced it, HTTP 200, the whole year in one call:
  `https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_DNI,ALLSKY_SFC_SW_DIFF,T2M,PRECTOTCORR&community=RE&longitude=-81.33544&latitude=28.54653&start=20230101&end=20231231&format=CSV&time-standard=UTC`
- The coordinates are the rain gauge's own, from the ISD file: latitude 28.54653, longitude -81.33544, elevation 31.7 m.
  It is the most complete hourly gauge of the four near Apopka that were checked.
  Its distance from Apopka was not computed, so the page says "the Orlando Executive Airport gauge, near Apopka" and gives no distance.
- 8,774 lines: 13 header lines from `-BEGIN HEADER-` to `-END HEADER-`, the column row on line 14, then 8,760 data rows, so the file is read with 13 rows skipped.
- Columns: `YEAR,MO,DY,HR,ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_DNI,ALLSKY_SFC_SW_DIFF,T2M,PRECTOTCORR`.
- Units, as the header states them: the three irradiances in Wh/m^2, from CERES SYN1deg, temperature in C and precipitation in mm/hour, from MERRA-2.
  Wh/m^2 over one hour is the mean W/m^2 for that hour, so there is nothing to convert.
- The missing value code is -999. The header's text mentions it, and the data holds none. The index is unique and in order.
- The grid is coarse: 1 degree for the irradiance and half a degree by five eighths for the rest, from NASA's own sources page.
- The timestamp labels the start of the hour, and the value is the hour's mean.
  NASA's pages do not say so in a sentence that was found, so this rests on a fit done on the file for another Gulf Coast site: global against direct and diffuse closed best with the sun taken half an hour after the stamp.
  It matters here only for joining to the rain, and both files are hour starts.
- NASA's own precipitation column is not used, anywhere.
  It is reanalysis, and it has 4,395 wet hours where the gauge has 373.

## Output

`data/processed/year-apopka-2023.csv`, 8,760 rows, LF line endings:

| Column | Type | Note |
|---|---|---|
| `hour` | int | 0 to 8759 |
| `time_utc` | ISO 8601 | the start of the hour, as in the raw file |
| `month` | int | 1 to 12, from the UTC stamp |
| `source_year` | int | 2023 |
| `local_hour` | int | 0 to 23, America/New_York |
| `ghi` | float, 2 decimals | W/m2, the hour's mean, from `ALLSKY_SFC_SW_DWN` |
| `dni` | float, 2 decimals | W/m2, from `ALLSKY_SFC_SW_DNI` |
| `dhi` | float, 2 decimals | W/m2, from `ALLSKY_SFC_SW_DIFF` |
| `t2m` | float, 2 decimals | degrees C |

Example, VERIFIED: `4460,2023-07-05T20:00:00Z,7,2023,16,330.98,94.53,237.13,34.60`.

## Dependencies

`pandas==2.2.3`, `numpy==2.2.3`, `pytest==9.0.2`, all already on the demo laptop.
These are the first lines of `software/requirements.txt`, every line pinned with `==`.

## Steps

1. Read the file with 13 rows skipped. Check: 8,760 rows, the nine column names above, and no -999 in the data, failing loudly if there is one.
2. Build the UTC index from `YEAR`, `MO`, `DY`, `HR`. Check: it runs from `2023-01-01T00` to `2023-12-31T23`, unique and in order.
3. Rename the columns, set `source_year`, take `month` from UTC and `local_hour` from America/New_York. Check: `local_hour` at `2023-07-05T20:00Z` is 16.
4. Write the file. Check: two runs give identical bytes, and no value is negative or `-0.0`.

## Acceptance

- `python data/build_solar_2023.py` exits 0 with the network off.
- `pytest software/tests/test_solar_2023.py` exits 0.

Test cases, from the real file, with the sums within 1:

- One test patches `socket.socket` to raise, then runs the build.
- 8,760 rows, and the header is exactly the nine output columns above.
- The sum of `ghi` is 1823145.29, of `dni` 1834269.42, of `dhi` 678850.26.
- 4,568 rows have `ghi` above 0.
- The largest `ghi` is 1050.12 at `2023-04-18T17:00Z`.
- `t2m` has a mean of 23.624 and a maximum of 37.55 at `2023-08-08T19:00Z`.
- The row at `2023-07-05T20:00Z`, hour 4460: `ghi` 330.98, `dni` 94.53, `dhi` 237.13, `t2m` 34.60, `local_hour` 16.
- The row at `2023-06-15T18:00Z`: `ghi` 850.15, `dni` 700.12, `dhi` 217.51, `t2m` 34.66, `local_hour` 14.
- By local day: 362 whole days, the sunniest is 2023-04-18 at 8129.79, then 2023-05-27 at 8001.96, and the sunniest in July is 2023-07-02 at 7531.16.

If an expected value does not match, the agent stops and reports it, and does not edit the value.

## Files

May create: `data/build_solar_2023.py`, `data/processed/year-apopka-2023.csv`, `data/README.md`, `software/requirements.txt`, `software/tests/test_solar_2023.py`, and one `.gitignore` line for `data/raw/`.
Must not touch: `planning/`, and anything in `hack-mit`.

## The demo day

The page plays **3 June 2023**, chosen in package H1, where the rules were run on it hour by hour.
31 days between April and October have at least 5 mm of daytime rain after at least four bright hours, so Central Florida's afternoon storms give plenty to choose from.

## Honesty labels

- On the screen: "Orlando Executive Airport gauge, near Apopka, Florida, 2023, a real year. Sun: NASA POWER, a satellite product for a cell about 100 km across, hourly means, modelled. Rain: one NOAA gauge, measured."
- The sun is never called measured.
- A local storm can rain under a bright cell, and the README says so with its example: on 29 July 2023 the gauge caught 11.2 mm in an hour while the satellite cell read 681 W/m2.

## Citations

- "The data was obtained from National Aeronautics and Space Administration (NASA) Langley Research Center's Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division."
- "The data was obtained from the POWER Project's Hourly 2.10.2 version on 2026/09/19."
- No licence text was found on NASA's referencing page, and the submission says so.

## Estimated minutes

30.
