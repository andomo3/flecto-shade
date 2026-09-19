---
title: Which real, messy public datasets can support the canopy and compete for the Voloridge "Signal in the Noise" challenge
type: research
status: in-progress
owner: abba
updated: 2026-09-19
idea: adaptive-bus-stop-canopy
---

# Which real, messy public datasets can support the canopy and compete for the Voloridge "Signal in the Noise" challenge

## Answer

Houston METRO's own ridership by stop layer, which carries a shelter flag in the same row, supports a ranking of the unsheltered stops where the most riders wait in the harshest sun.
The PVGIS typical year replay does not count for this challenge by itself, because it is a cleaned statistical product with no noise in it and no finding comes out of it.
This is planning: any analysis script is project code and is written in the event repo, never here.

## The challenge

Voloridge Investment Management, platinum sponsor, announced at the opening on 2026-09-19.
"Signal in the Noise: build something interesting from real-world data. Create a tool, model, visualization, or system that turns messy data into useful insights."
Dataset themes named: Earth, Health, Climate, Transport, Genomics, Economics.
Judged on originality, technical excellence, insight, and execution.
First place is 5,000 dollars and a fast tracked interview process.
The judges are likely quants, so expect questions on the assumptions, the spread, and what breaks the finding.

Open, and to settle at the Voloridge booth before any hour is spent: the challenge text transcribed on 2026-09-15, in `../../sources/2026-09-15-sponsor-challenges.md`, says "We'll provide a curated selection of large, publicly available datasets".
It is not known whether a public dataset from outside that selection counts.
Ask for the curated list, ask whether outside public data is allowed, and if it is not, look in the list for a transit, climate, or earth observation set that supports the same ranking.

## Findings

Found by a research agent on 2026-09-19.
Rows marked "checked" were also fetched by hand the same day, and the rest are the agent's report and need a spot check before anyone relies on them.

### 1. Houston METRO "October Ridership by Stop", the pick

- `https://services5.arcgis.com/p8QKnlioaN3sruqA/arcgis/rest/services/October_Ridership_by_Stop/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&outSR=4326&resultOffset=0&resultRecordCount=2000&f=json`
- JSON, no key, 2,000 rows a page, so five pages.
- Checked: 9,085 stops, 2,165 with `WITH_SHLTR` 1 and 6,920 with 0.
- Boardings: `WkAvOn19`, `WkAvOff19`, `WkAvAct19`, `WkAvOn22`, and matching `Sa` and `Su` columns.
- Also `WITH_BNCH`, `SPOT`, `SRVD_RTS`, `ZIP`.
- A sister April layer exists at `.../RidershipByStop_WkSaSu_0423/FeatureServer/7`, 9,123 rows, with different column names, `WkAvgOn23`.
- No licence text on the layer, so use METRO's attribution line and cite it in the submission.
- What is messy, and this is a plus for the challenge:
  - `LON` and `LAT` are 0 in sampled rows, `POINT_X` and `POINT_Y` exist, and geometry is untested.
  - The description promises 2019, 2021, and 2022, and only the 19 and 22 columns exist.
  - One of the busiest stops has a blank name.
  - The shelter flag is from about 2022, and the ridership is October and April averages, not July.
- The trap, which is the talking point for a quant judge:
  the naive sum says 44.9 percent of October 2022 weekday boardings, 63,352 of 141,149, happen at stops flagged unsheltered.
  But 14 of the top 15 "unsheltered" stops are transit centres and park and rides, all with `SPOT='AT'`, which have large canopies the flag does not record.
  The headline number is wrong until those are removed.
  These figures are the agent's and are recomputed at the event before they are said.

### 2. NOAA SOLRAD Hanford, one minute measured irradiance, the farmworker's sky

- `https://gml.noaa.gov/aftp/data/radiation/solrad/hnx/2023/hnx23201.dat`, one file a day.
- Checked: the file answers, 181 KB.
- The station is at 36.31, -119.63, in California's Central Valley.
- Fixed width text with a quality flag after every value, -9999.9 for missing, and negative readings at night.
- US government data, and the README asks for a citation of Hicks et al. 1996.
- Pairs with NCEI ISD hourly temperature for Fresno, `https://www.ncei.noaa.gov/data/global-hourly/access/2023/72389093193.csv`, 6.6 MB, where `TMP` is a packed string such as "+0194,5".
- The question it could answer: on how many afternoons above 80 F, when California's Title 8 section 3395 requires shade, does a fixed shade's shadow drift off the bench.
- There appears to be no SOLRAD or SURFRAD station in Texas, so this serves the farmworker and not Rosa.

### 3. NCEI ISD Houston Hobby, July and August 2023, the study's real hours

- `https://www.ncei.noaa.gov/data/global-hourly/access/2023/72244012918.csv`, 6.7 MB, no key.
- The real weather of the Lanza study period, 2023-07-20 to 2023-08-07, to sit beside the typical year day.
- NASA POWER hourly answers with no key for the same dates, and it is a satellite and reanalysis product, to be labelled modelled.
- A supplement to pick 1, and no finding by itself.

### Weaker or unverified

- OSHA Severe Injury Reports, `https://obis.osha.gov/severeinjury/xml/severeinjury.csv`, 29 MB: last modified November 2020, and believed to exclude California as a state plan state, unchecked.
- CIMIS needs registration and a key.
- CDC Heat and Health Tracker has no bulk download that was found, and CDC WONDER refused the request.
- InSPIRE agrivoltaics and the Tree Equity Score: pages answer, no download was reached, and no shade against yield table was found.
- The NOAA Houston 2020 heat island campaign and Texas DSHS heat data were not reached.

## Implications for the build

- The analysis is one person, about three to four hours, and it competes for the same hours as the app, so the app's core loop comes first and the pivots in `project-brief.md` still hold.
- The sketch, each step with its check:
  1. Page all rows with geometry into `raw/`: 9,085 rows, 2,165 and 6,920, and usable coordinates.
  2. Flag the facilities, `SPOT='AT'`, names ending in TC or PR, and blank names: the top 15 unsheltered stops are now curbside stops, and both the naive and the corrected share are reported.
  3. Build the exposure weight from hourly irradiance and temperature, weighted by departures per hour from GTFS `stop_times.txt`: report the match rate between GTFS stop codes and `STOPABBR`, and keep the unmatched stops in the count.
  4. Rider sun minutes per stop, boardings times an assumed wait of half the headway times the share of service hours in harsh sun: state the wait assumption and rerun at 5 and 10 minutes to see whether the ranking holds.
  5. The concentration curve, how many unsheltered stops carry half the exposure, with a bootstrap interval and the rank stability between the 2019 and 2022 columns as a Spearman correlation.
  6. Group by ZIP and map the top 20: every number labelled as October averages and a 2022 flag, not July measurements.
- The insight to aim for, not yet computed: a few hundred of about 6,900 unsheltered stops carry half of the riders' sun exposure, and the official flag hides it until the transit centres are removed.
- It answers the cost question in `pitch/questions.md`: the leaf belongs at the few stops the ranking names, not at all of them.
- The honesty rules carry over: the ranking is modelled exposure from averages and assumptions, it is said as modelled, and the only measured numbers stay the sensors on the table.
- `data/raw/` was empty on the demo laptop on 2026-09-19, so the Friday PVGIS download either did not happen or sits on another machine, and every dataset here needs the venue network.

## Sources

- The Voloridge challenge slide, photographed at the opening ceremony, 2026-09-19.
- Houston METRO ArcGIS account `jl83_METRO_Houston`, the layer URL above.
- NOAA Global Monitoring Laboratory, SOLRAD network, the file URL above.
- NOAA NCEI Integrated Surface Database, global hourly access, the URLs above.
- California Code of Regulations, Title 8, section 3395, https://www.dir.ca.gov/title8/3395.html
