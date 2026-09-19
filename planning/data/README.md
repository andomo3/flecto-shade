# Data

Owner: Ameya, the data engineering, with packages S1 and H1.
Abba's H3 writes one processed file, `headline.json`, and Shannon's K2 writes `data/roof-layout.json`.

## What this folder is

This folder is planning, Markdown only.
The data and the build scripts live in the repo's own `data/` directory, and the simulation in `software/h1/`.
This file is the provenance of every dataset the project uses, so that a claim built on public data can be audited by a judge.
The specifications, `../plans/packages/S1-solar-2023.md` and `../plans/packages/H1-zones-light-rain-soil.md`, are authoritative for every schema and every expected value, and this file summarises them.
Note that S1 may also create a `data/README.md` in the repo's own `data/` directory, which is a different file from this one.

## The place and the year

The Orlando Executive Airport gauge, near Apopka, Florida, 2023, a real year.
The coordinates are the rain gauge's own: latitude 28.54653, longitude -81.33544, elevation 31.7 m.
The gauge's distance from Apopka was not computed, so the page says "near Apopka" and gives no distance.
2023 was an ordinary year for rain there, 2.4 percent above the 1991 to 2020 normal of 1,307 mm.

## The two raw datasets

`data/raw/` is ignored by git on purpose, so each laptop fetches its own copy, and a person checks the sha256 before anything is built.
Only Ameya's laptop strictly needs the raw files, because the other packages read the processed files, which are committed.

| | The sun | The rain |
|---|---|---|
| Dataset | NASA POWER, hourly, version 2.10.2 | NOAA NCEI Global Hourly, ISD, station 72205312841, "ORLANDO EXECUTIVE AIRPORT, FL US" |
| File | `data/raw/nasa-power/power-hourly-orlando-executive-2023.csv` | `data/raw/isd-rain/72205312841-2023.csv` |
| Size | 340,893 bytes | 6,393,887 bytes |
| sha256 | `c81490d249cb1fc857b0edf44c54d6fcdbc7c1e5b30b326310138a10f25cefc4` | `d26366ed5b470b8a79d0c447b08b693b7b77f810bc8ee7a138c1a75682c64f08` |
| Fetched | 2026-09-19 | checked on 2026-09-19 |
| What it is | A satellite and reanalysis product, modelled, hourly means, for a cell about 100 km across | One real gauge's hourly reports |
| Read by | S1 | H1 |
| Feeds | `data/processed/year-apopka-2023.csv` | `data/processed/weather-apopka.csv` |

The sun's source address, the whole year in one call:

```text
https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_DNI,ALLSKY_SFC_SW_DIFF,T2M,PRECTOTCORR&community=RE&longitude=-81.33544&latitude=28.54653&start=20230101&end=20231231&format=CSV&time-standard=UTC
```

The rain's source address:

```text
https://www.ncei.noaa.gov/data/global-hourly/access/2023/72205312841.csv
```

If a checksum differs:

- NASA may stamp a new date into the file's header when it is fetched again, which changes the sha256 and nothing else.
  If only that checksum differs, check that the 8,760 data rows give the sums in S1's tests, and carry on.
- If the rain file's checksum differs, stop and tell abba.

What is used from each file, in short, with the detail in the specifications:

- The sun: 13 header lines are skipped, then 8,760 rows, with the three irradiances in Wh/m^2, which over one hour is the mean W/m2, and the temperature in C.
  NASA's own precipitation column is not used, anywhere.
- The rain: the `AA1` field of the FM-15 rows only, period 01, depth in tenths of a mm, the last row in each UTC hour, and a missing hour becomes 0.
  The year's total by that rule is 1338.6 mm in 373 rain hours, against 1338.1 mm in the station's own daily summaries.

## The processed files, which are committed

| File | Written by | Read by | Rows | Schema lives in |
|---|---|---|---|---|
| `data/processed/year-apopka-2023.csv` | S1, `python data/build_solar_2023.py` | H1 | 8,760 | S1's spec |
| `data/processed/weather-apopka.csv` | H1, `python software/h1/build.py --city apopka` | H2 | 8,760 | H1's spec |
| `data/processed/sim-apopka.csv` | H1 | H2, H3 | 26,280 | H1's spec |
| `data/processed/sim-summary-apopka.csv` | H1 | H3 | by zone and month, and by zone for the year | H1's spec |
| `data/crops.csv` | H1 | H2, H3 | 3 | H1's spec |
| `data/processed/headline.json` | H3, `python software/h3/build_headline.py` | the page's result card, and the pitch through `pitch/figures.md` | | `../plans/packages/H3-result-card.md` |
| `data/roof-layout.json` | K2 | H2 | | `../../CHECKLIST.md`, under K2 |

- Every build runs with the network off and gives identical bytes on two runs.
- Every output is labelled modelled or simulated.
- `year-apopka-2023.csv` has one row an hour in UTC, with `hour`, `time_utc`, `month`, `source_year`, `local_hour` in America/New_York, `ghi`, `dni`, `dhi`, and `t2m`.
- `weather-apopka.csv` is every column of that file plus `rain_mm`, joined on `time_utc`, because both files stamp the start of the hour.
- `sim-apopka.csv` is one row per hour per zone, with the zone's open fraction, its light so far, its soil, the rain stored, the irrigation, the `state`, and the `reason`.
- `roof-layout.json` is a modelled layout, plain data the page draws, and the simulation does not read it.

NEEDED: the exact column names and row layout of `sim-summary-apopka.csv`.
H1's spec names `rain_in_mm`, `irrigation_mm`, the days the light target was met, and the year's share per zone, and gives no column name for the last two or how the year's rows sit beside the month rows, and H3 reads this file.

## `crops.csv`, and where each figure comes from

Columns: `crop`, `zone`, `light_rule` as `dli` or `shade_pct`, `light_value`, `kc`, `rain_ok`, `light_source_url`, `kc_source_url`, `note`.
Gate F14 asserts that every row has a source address in both source columns.

| Zone | Crop | Light rule and value | Source of the light figure | `kc` | Source of `kc` | Rain |
|---|---|---|---|---|---|---|
| A | Boston fern | `dli`, 8 mol per m2 per day, the start of "high quality" | Purdue HO-238-W, Table 2, Nephrolepis | 1.00, ASSUMED | FAO-56 Table 12 has no row, so `note` says "no row in the table, 1.00 assumed" | Opted out, `rain_ok` 0 |
| B | Hydrangea, as nursery stock | `dli`, 12 mol per m2 per day, the start of "high quality" | The same table, hydrangea | 1.00, ASSUMED | The same, with the same note | Opted in, `rain_ok` 1 |
| C | Southern highbush blueberry | `shade_pct`, 0.40, the middle of 30 to 50 percent | Washington State University fact sheet on heat damage in blueberries | 1.05 | FAO-56 Table 12, berries on bushes | Opted in, `rain_ok` 1 |

Said plainly, on the page and in the README:

- The blueberry's shade figure comes from Washington State and is not Florida practice.
- The fern opts out of rain because its grower's guide wants the foliage to dry during the day, University of Florida IFAS EP550.
- The light sums use `K = 0.45 x 4.57 = 2.0565` micromol per joule of global solar, from Noriega Gardea et al. 2021.
  0.45 is a choice inside the verified range, so light sums may read 5 to 18 percent high.
- The soil bucket, 60 mm with marks at 18, 30, and 54, is ASSUMED, and so are `T_STRUCT` 0.90, `T_CLOSED` 0.0, the three hour drying rule, the 25 mm hard rain cap, and the 32.2 C heat trigger.
- The evaporation formula's Makkink form, its 0.65 coefficient, and its 2.45 divisor are RECALLED, not confirmed at a source, and the evaporation figures carry that label.
- Every ASSUMED and RECALLED constant is a named constant in the code and a row in the README's table of assumptions, with its value, which gate F6 checks.

## The citations the submission needs

- NASA POWER, two lines, word for word:
  "The data was obtained from National Aeronautics and Space Administration (NASA) Langley Research Center's Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division."
  "The data was obtained from the POWER Project's Hourly 2.10.2 version on 2026/09/19."
  No licence text was found on NASA's referencing page, and the submission says so.
- NOAA NCEI Global Hourly, ISD, station 72205312841, believed public domain and to be confirmed.
- NOAA NCEI 1991 to 2020 normals for station USW00012841, for the "ordinary year" sentence.
- Purdue HO-238-W: https://www.extension.purdue.edu/extmedia/ho/ho-238-w.pdf
- The Washington State University blueberry fact sheet: https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/3274/2025/08/FactSheet_ReducingHeatDamageinBlueberries.pdf
- University of Florida IFAS: the Mid-Florida Research and Education Center, https://mrec.ifas.ufl.edu/about/, the foliage breeding program, https://programs.ifas.ufl.edu/plant-breeding/tropical-foliage/, and EDIS documents EP149, EP550, and HS742, found through https://edis.ifas.ufl.edu, whose exact addresses the build agent records when it opens them.
- FAO Irrigation and Drainage Paper 56: https://www.fao.org/4/x0490e/x0490e07.htm and https://www.fao.org/4/x0490e/x0490e0b.htm
- Noriega Gardea et al. 2021, Atmosfera 34(3): https://www.redalyc.org/journal/565/56572301008/html/
- The libraries: `pandas`, `numpy`, and `pytest`, at the versions pinned in `software/requirements.txt`.
- The fin: the Flectofin, by ITKE, University of Stuttgart, patented as EP2320015.
- Every AI tool used, the build agents included.

## The honesty labels

- On the screen: "Orlando Executive Airport gauge, near Apopka, Florida, 2023, a real year. Sun: NASA POWER, a satellite product for a cell about 100 km across, hourly means, modelled. Rain: one NOAA gauge, measured."
  That rain source line is the one place the word "measured" may appear, because it is true of the gauge.
- The sun is never called anything but modelled.
- Every figure the simulation produces is simulated.
- Never claimed: climate control, safety from disease, yield, or any figure for cost, energy, or water saved.
