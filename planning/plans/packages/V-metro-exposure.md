# V1 to V4: where an adaptive roof matters most, from Houston METRO's own data

The Voloridge "Signal in the Noise" analysis, in four packages.
Planned on 2026-09-19 by a planning agent that fetched every source.
"Verified" below means fetched or computed from the real data that day, and "assumed" means it was not.

Abba confirmed on 2026-09-19 that public data from outside Voloridge's curated list counts, so these packages are clear to hand over.

## What was found, before any code

- METRO's layer says 44.88 percent of October 2022 weekday boardings, 63,352.1 of 141,149.0, happen at stops flagged unsheltered. Verified.
- All 15 of the busiest "unsheltered" stops are transit centres and park and rides, which have canopies the flag does not record. Verified.
- With 88 facilities removed, the share is 36.59 percent, 39,672.31 of 108,434.86, and a looser rule gives 36.19, so it is stable to the rule. Verified.
- Of 6,865 curbside stops flagged unsheltered, 666, or 9.7 percent, carry half the boardings, and 2,067 carry 80 percent, with a Gini of 0.6653. Verified.
- The ranking is stable over time: Spearman 0.8116 between the 2019 and 2022 columns, and 138 of the top 200 in common. Verified.

The honest limit, found by the planner and said out loud: the sun weighting barely moves the ranking.
The share of a stop's weekday departures that fall in the harsh hours spans only 0.375 to 0.50, so boardings drive the result.
The packages report both, and the pitch never implies the solar data did more than it did.

## Shared facts about the inputs

### The ridership layer, verified

- Layer `RidershipByStop_WkSaSu_1022`, point geometry, 9,085 rows, WGS84, `maxRecordCount` 2000.
- Raw copy: `hack-mit/data/raw/metro-ridership-oct/page-0.json` to `page-4.json`, 3,196,004, 3,221,463, 3,215,847, 3,225,360, and 1,706,037 bytes, 2000 + 2000 + 2000 + 2000 + 1085 features, ordered by `OBJECTID_12`.
- Coordinates come from the geometry only, and all 9,085 fall inside x -95.78 to -94.96 and y 29.52 to 30.32.
  `LON` and `LAT` are junk, 0 in 8,999 rows and 1 in 86.
  `POINT_X` and `POINT_Y` are about 3.10 million and 13.87 million, assumed to be Texas State Plane feet, and are not used.
- `BSID` is unique and is the key.
  `STOPABBR` is blank in 2 rows and matches nothing in GTFS.
- `StopName_1` is never blank and is the name.
  `STOPNAME` is blank in 2 rows, BSID 13169 and 13170, both transit centres.
- `WITH_SHLTR`: 0 in 6,920 rows and 1 in 2,165.
- `SPOT`: NS 7,076, FS 1,186, MB 735, AT 84, blank 4, assumed to mean near side, far side, mid block, and at a facility.
- `STATUS`: A 8,929, I 101, F 49, T 6, and all 49 F rows are named as a transit centre, park and ride, or station.
- `WkAvOn22`: no nulls or negatives, 365 zeros, sum 141,149.0, maximum 4,579.8, and 8,316 values are not whole numbers because they are averages.
  `WkAvOn19`: 443 zeros, sum 229,010.4.
- `WITH_TCAN` is a trash can, not a canopy.
- The name trap: a bare "TC" match wrongly catches about 50 street stops on "TC JESTER BLVD".

### The GTFS feed, verified

- `hack-mit/data/raw/metro-gtfs/metro-direct.zip`, 12,660,993 bytes, from `https://metro.resourcespace.com/pages/download.php?ref=4835&ext=zip`, found through the Mobility Database catalog, id 2060.
- `feed_version` is `August2026IVOMS_20260828`, valid 20260830 to 20270123.
- `stop_id` equals `stop_code`, and `BSID` matches 8,640 of 9,085 stops, 95.1 percent, with a median offset of 0.9 m and 37 over 100 m.
- 445 rows do not match: 362 of them flagged unsheltered, carrying 2,515.2 boardings, and 96 of them inactive.
- The weekday `service_id` is `6`, `stop_times.txt` has 1,415,650 rows, and hours run to 26, so the hour is taken modulo 24.
- A second file in that folder, `metro-mdb-2060.zip`, is an older feed, is unused, and may be deleted.

### The solar file, from package C6

`data/processed/year-houston.csv`, 8,760 rows, and V2 needs three of its columns: `month` as an integer 1 to 12, `local_hour` as an integer 0 to 23, and `ghi` in W/m2.
C6 writes all three.

### One environment

Both this analysis and the app share one virtual environment, so the pins are C6's: pandas 2.2.3, numpy 2.2.3, pytest 9.0.2, and matplotlib 3.10.1, all already on the demo laptop.
The planner found newer versions on PyPI, and they are not used, because `pvlib` 0.15.2 has not been tried against pandas 3.
Spearman is computed by ranking with pandas, so `scipy` is not imported here.

### For every package

- Files may be created only under `flecto-stop/data/` and `flecto-stop/analysis/`.
- Never touch `flecto-stop/planning/` or anything in `hack-mit`.
- A person copies the two raw folders into `flecto-stop/data/raw/` and adds `data/raw/` to `.gitignore` before V1 starts.
- Every output carries this label: "Modelled. October 2022 weekday averages, shelter flag about 2022, August 2026 schedule, PVGIS typical year. Not measured."
- Attribution: "Ridership and stop data: Metropolitan Transit Authority of Harris County (Houston METRO), ArcGIS account jl83_METRO_Houston, and GTFS feed August2026IVOMS_20260828."
- No licence text was found on either METRO source, and METRO's developer terms are unverified, so the submission says so.
- PVGIS is (c) European Union, CC BY 4.0.

## V1: the tidy stops table and the exclusion audit

Goal: turn the five raw pages into one tidy table.
Make the removal of facilities something a judge can audit row by row.

The facility rule: a stop is a facility if `STATUS` is `F`, or `SPOT` is `AT`, or its upper cased `StopName_1` has no `@` and matches `( TC| PR)$|TRANSIT CENTER|PARK AND RIDE`.
A hand editable override file is applied last.

Outputs:

- `data/processed/stops.csv`, 9,085 rows: `bsid` int, `name` str, `lon` float degrees, `lat` float degrees, `zip` str, `spot` str, `status` str, `in_service` int, `sheltered` int 0 or 1, `wk_on_19` float boardings per average weekday, `wk_on_22` float, `is_facility` int, `facility_reason` str.
  Example, with illustrative coordinates and ZIP: `11025,TEXAS MEDICAL CENTER TC,-95.40,29.70,77030,AT,F,1,0,7120.667,4579.8,1,F+AT+name`.
- `data/processed/exclusions_audit.csv`, 88 rows: `bsid`, `name`, `spot`, `status`, `sheltered`, `wk_on_22`, `reason`, `override`.
- `data/facility_overrides.csv`, header only: `bsid`, `action` as `force_keep` or `force_exclude`, `note`.

Steps:

1. Load the five pages. Check: 9,085 unique `bsid`.
2. Take coordinates from the geometry. Check: all inside the box above.
3. Take the name from `StopName_1`, stripped. Check: none blank.
4. Apply the rule, then the overrides. Check: 88 excluded.
5. Write the three files. Check: they read back identical.

Acceptance: `python -m analysis.clean` and `pytest analysis/tests/test_clean.py` exit 0 with the network off.

Tests:

- 9,085 rows, and the sheltered split is 2,165 and 6,920.
- The sum of `wk_on_22` is 141149.0 within 0.1.
- The naive unsheltered share is 0.4488 within 0.0001.
- BSIDs 11025, 11031, 75, 13170, 13169, and 4009 are excluded.
- No stop whose name contains "TC JESTER" is excluded.
- BSID 11016, "FARMER ST WB @ 5TH WD DNVR HRB TC", is kept, because it is a street stop beside a transit centre.
- 6,865 unsheltered stops are kept, and the corrected share is 0.3659 within 0.0001.

Minutes: 45.

## V2: the exposure metric and its sensitivity

Goal: compute modelled exposure for every kept, unsheltered stop.
Run the whole scenario grid, so no single assumption carries the result.

Exposure is `wk_on_22` times the wait in minutes times `f_harsh`, in modelled rider minutes of harsh sun per average weekday.
`f_harsh` is the share of the stop's weekday departures that fall in harsh hours, where hour h of month m counts by the share of that month's days with `ghi` at or above the threshold.
Stops with no GTFS match get the network's mean profile and are flagged.

A constant wait cannot change a rank or a Gini, so the wait is per stop: the smaller of a cap and 30 divided by the stop's weekday departures per service hour.
The grid is three thresholds, 400, 600, and 800 W/m2, by two periods, July and the whole year, by four waits, caps of 5, 10, and 15 minutes and a constant 10 as the baseline: 24 scenarios.
The default is July, 600, cap 10.

Inputs: `stops.csv`, the GTFS zip, and `year-houston.csv`.
If the year file is absent, use a committed fixture, `analysis/tests/fixtures/year-mini.csv`, and label every output "fixture".

Outputs:

- `data/processed/stop_service.csv`: `bsid`, `gtfs_matched` int, `wk_departures` int, `service_hours` int, `dep_h00` to `dep_h23` int.
- `data/processed/exposure.csv`: `bsid`, `scenario` str such as `jul_600_cap10`, `wait_min` float, `f_harsh` float 0 to 1, `exposure` float, `rank` int.
  Illustrative row: `581,jul_600_cap10,4.2,0.41,599.3,1`.

Steps:

1. Stream `stop_times.txt` for `service_id` 6. Check: 8,791 stops have weekday service, and the match rate is 0.951 within 0.002.
2. Build the harsh hour table. Check: night hours are 0.
3. Compute `f_harsh`. Check: every value is between 0 and 1, and the matched median for hours 10 to 17 is near 0.43.
4. Run the grid. Check: 6,865 rows in each of 24 scenarios.

Acceptance: `python -m analysis.exposure` and `pytest analysis/tests/test_exposure.py` exit 0 with the network off.

Tests:

- In the constant wait scenario, the rank correlation against `wk_on_22` times `f_harsh` is exactly 1.0.
- Unmatched stops are flagged, 362 before any override.
- No missing values anywhere.
- Exposure is 0 wherever `wk_on_22` is 0.

Minutes: 60.

## V3: concentration, stability, and the outputs

Goal: produce the headline numbers, the ranked list, and two charts.

Outputs:

- `data/processed/ranked_stops.csv`, the default scenario: `rank`, `bsid`, `name`, `zip`, `lon`, `lat`, `wk_on_22`, `exposure`, `share`, `cum_share`.
- `data/processed/headline.json`: `naive_share`, `corrected_share`, `n_unsheltered`, `k50`, `k50_min`, `k50_max`, `k80`, `gini`, `spearman_19_22`, `top200_overlap`, `labels`.
- `analysis/out/lorenz.png`, and `analysis/out/trap_top15.png`, the top 15 before and after the exclusion.

This is a census of stops, not a sample, so a bootstrap would measure only how much the statistic depends on which stops are in it.
It is reported, if at all, as a robustness band and never as a confidence interval.
The evidence that matters is the rank stability between 2019 and 2022, the overlap of the top 200, and the lowest and highest `k50` across the 24 scenarios.

Steps:

1. Compute shares. Check: they sum to 1 within 1e-9.
2. The Lorenz curve, the Gini, `k50`, and `k80`.
3. `k50` across the grid, for `k50_min` and `k50_max`.
4. Spearman between 2019 and 2022, by ranking with pandas.
5. The two charts, with the Agg backend. Check: each file is over 5 KB.

Acceptance: `python -m analysis.report` and `pytest analysis/tests/test_report.py` exit 0 with the network off.

Tests, on a control that uses boardings alone:

- `k50` is 666, and `k80` is 2,067.
- The Gini is 0.6653 within 0.0005.
- Spearman is 0.8116 within 0.001, and the top 200 overlap is 138.
- `cum_share` never decreases and ends at 1.

Minutes: 60.

## V4, optional: a static page

`analysis/view/index.html` reads `headline.json` and `ranked_stops.csv`, with vanilla JavaScript and inline SVG and no CDN.
Check: it opens with the network off from `python -m http.server`.
Minutes: 40.

## What the team says

"METRO's own flag says 45 percent of boardings are at unsheltered stops. Take out 88 transit centres the flag gets wrong, and it is 37 percent. And just [K] of 6,865 curbside stops carry half of it."
K is 666 on boardings alone, and the final K and its range come from V3.

The three hardest questions, and the honest answers:

1. "Is your sun weighting doing anything?"
   Barely: the harsh hour share spans 0.375 to 0.50, so boardings drive the ranking, and we show it both ways.
2. "Is a confidence interval on a census meaningful?"
   No, so we do not give one: we give rank stability, 0.81 across three years, and the range across 24 scenarios.
3. "Is the 2022 shelter flag still right?"
   Unknown. The rule also removes 33 sheltered facilities, and a field check of the top stops is the next step.

Not claimed, anywhere: July ridership, today's shelters, counts as opposed to averages, measured exposure, or heat.
The schedule is from 2026 and the ridership from 2022, and the headway of combined routes understates the wait.

## Open questions for a person

- METRO's licence terms.
- Whether the default period is July or the whole year.
- A hand review of the 33 rows excluded on `SPOT` being `AT` alone, which include an airport, hospitals, and colleges.
