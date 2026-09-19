# H1: zone targets, light, rain, and the soil bucket

The heart of the louvre roof simulation.
Planned on 2026-09-19 by a planning agent that opened every source and read the real rain file.
VERIFIED means opened or computed that day, ASSUMED means a choice the team made, and RECALLED means from memory and to be checked before it is trusted.

## Goal

Build a crops table, a clean hourly weather file with rain, and a deterministic hour by hour simulation of three crop zones under a roof of fins, for Houston.
It runs with the network off, gives identical bytes on every run, and labels everything modelled.

## The setting

A shade house or open field louvre roof over soil or container crops, not a closed glasshouse, because closed greenhouses keep rain off the crop on purpose, see `../../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md`.
Houston stays the location: hot sun, real rain, and both files checked and on disk.
A glasshouse hub such as Leamington, Ontario buys nothing for a shade house.

## Inputs

### The solar year

`flecto-stop/data/processed/year-houston-2023.csv`, written by package S1 from NASA POWER, for Houston Hobby in 2023, the same place and year as the rain.
If it is absent, stop and report, and do not rebuild it here.
H1 uses its `time_utc`, `month`, `local_hour`, `ghi`, and `t2m` columns, and joins the rain on `time_utc`, because both files stamp the start of the hour.
Every expected value below was recomputed on that file on 2026-09-19, and the values first computed on the PVGIS typical year are gone.

### The rain, VERIFIED on the real file

- `hack-mit/data/raw/isd-rain/72244012918-2023.csv`, NOAA ISD global hourly, Houston Hobby, 2023: 6,702,547 bytes, sha256 `2951a8e5231ef98655982cddf0531ca50681e267cb9e0336b567a2a5d394a392`.
  A person copies it into `flecto-stop/data/raw/isd-rain/` and checks the sha256.
- 10,916 rows. `REPORT_TYPE` is FM-15 in 8,772, FM-16 in 1,767, `SOD  ` in 365, and `SOM  ` in 12, with trailing spaces.
- The rain is in `AA1`, `AA2`, and `AA3`, each "period hours, depth in tenths of a mm, condition, quality": `01,0000,9,5`, `01,0099,9,5`, a trace as `01,0000,2,5`, and missing as `24,9999,1,9`.
- The traps:
  - FM-16 special reports repeat the running hourly total, for example `01,0078,3,1` at 12:50 and then the FM-15 `01,0099,9,5` at 12:53, so summing every one hour period gives 2,142.6 mm, double the truth.
  - `AA2` and `AA3` hold 3, 6, and 24 hour totals, and the `SOD` rows hold 24 hour totals.
  - Three hours have two FM-15 rows.
  - A trace always has depth 0.
- The rule: FM-15 rows only, `AA1` with period 01, depth not 9999, floor the time to the UTC hour, keep the last row in each hour, divide by 10, and the 4 missing hours become 0.
- The 2024 file was also saved and rejected, because 105 of its hourly reports lack `AA1`.
- Cross check: the station's daily summaries sum to 1000.2 mm, a gap of 0.4 percent.
  The 1981 to 2010 normal is 54.65 inches, 1,388 mm, so 2023 was 28 percent below it, a drought year with no rain at all in August.

### The crops, each from a source

| Zone | Crop | Light rule | Value | Source |
|---|---|---|---|---|
| A | Lettuce | Daily light sum | 17 mol per m2 per day | VERIFIED: "For the lettuce production the recommended level is 17 mol/m2/d", Cornell CEA Hydroponic Lettuce Handbook, page 14. A hydroponic greenhouse figure, and said as one |
| B | Hydrangea, as nursery stock | Daily light sum | 12 mol per m2 per day, the start of "high quality" | VERIFIED: Purdue HO-238-W, Table 2, hydrangea: minimum 6, good 8 to 10, high quality 12 and up |
| C | Blueberry | Shade share | 0.40, the middle of 30 to 50 percent | VERIFIED: "A 30-50% shade net is recommended for blueberry plants, while 75% or more shade can lessen fruit quality", Washington State University fact sheet |

Good daily light tables exist only for greenhouse crops, so the blueberry's figure is a shade share and not a light sum, and the package handles both kinds of rule.

### Light

- VERIFIED: 4.57 micromol per joule of photosynthetic light, and that light is 0.44 to 0.55 of global solar, with measured values of 1.69 to 1.96 mol per MJ of global solar, Noriega Gardea et al. 2021.
- `K = 0.45 x 4.57 = 2.0565` micromol per joule of global solar, a named constant.
  0.45 is a choice inside the verified range, and the measured range is lower, so light sums may read 5 to 18 percent high, and the README says so.
- Per hour: `mol_h = ghi x K x 3600 / 1e6 x T_STRUCT x (open + (1 - open) x T_CLOSED)`, and the day's total is the daily light sum.
- `T_STRUCT = 0.90`, ASSUMED, for a roof with no glazing. `T_CLOSED = 0.0`, ASSUMED, a closed fin is opaque. Both are named constants.

### Water

- VERIFIED: evaporation in mm per day is 0.408 times radiation in MJ per m2 per day, FAO-56 equation 20.
- VERIFIED crop coefficients, FAO-56 Table 12: lettuce 1.00, berries on bushes 1.05. Hydrangea has no row, so 1.00 is ASSUMED.
- Reference evaporation per hour by Makkink: `0.65 x D / (D + g) x (ghi x 3600 / 1e6) / 2.45`.
- VERIFIED, FAO-56 chapter 3: equation 13, `D = 4098 [0.6108 exp(17.27 T / (T + 237.3))] / (T + 237.3)^2`; equation 8, `g = 0.665 x 10^-3 P`; equation 7, `P = 101.3 [(293 - 0.0065 z) / 293]^5.26`.
- The solar file has no pressure column, so pressure is a constant from the gauge's elevation, 13.2 m: `P = 101.1441` kPa and `g = 0.067261` kPa per C.
- NOT verified: the Makkink form itself, its 0.65 coefficient, and the 2.45 MJ per kg divisor. They are RECALLED, the README says so, and the evaporation figures are labelled with that.
- Crop use is the coefficient times reference evaporation times the share of light reaching the crop, ASSUMED.
- The soil bucket, all ASSUMED: capacity 60 mm, dry below 30, full at 54, and the grower's own irrigation tops it back to 54 when it falls below 18.

## Outputs

- `data/crops.csv`: `crop`, `zone`, `light_rule` as `dli` or `shade_pct`, `light_value`, `kc`, `rain_ok`, `light_source_url`, `kc_source_url`, `note`.
  Rows: A lettuce `dli` 17, `kc` 1.00, `rain_ok` 0; B hydrangea `dli` 12, `kc` 1.00, `rain_ok` 1; C blueberry `shade_pct` 0.40, `kc` 1.05, `rain_ok` 1.
- `data/processed/weather-houston.csv`: every column of the solar file plus `rain_mm`, joined on `time_utc`. 8,760 rows.
- `data/processed/sim-houston.csv`: `hour`, `time_utc`, `zone`, `crop`, `open_fraction`, `light_mol_so_far`, `soil_mm`, `rain_in_mm`, `irrigation_mm`, `state`. 26,280 rows.
- `data/processed/sim-summary-houston.csv`: by zone and month, `rain_in_mm`, `irrigation_mm`, the rain's share of the two, and the days the light target was met.

## The rules, each hour, decided from the state at the end of the hour before

1. Daylight means `ghi > 0`, and `light_mol_so_far` resets when `local_hour` is 0.
2. `want_rain` latches on when `soil_mm` falls below 30 and off when it reaches 54.
3. If `ghi <= 0`: open 0, state NIGHT. Rain is never admitted at night.
4. Otherwise, if it is raining, the crop has opted in, `want_rain` is on, there is daylight three rows later, and the hour's rain is under 25 mm: open 1, state RAIN_OPEN.
   The three hour drying rule and the 25 mm hard rain cap are ASSUMED simplifications.
5. Otherwise, if it is raining: open 0, state RAIN_SHUT.
6. Otherwise, for a daily light crop: open 1 and LIGHT_OPEN while `light_mol_so_far` is under the target, then open 0 and SHADE.
7. Otherwise, for a shade share crop: open 0.60 and HEAT_SHADE when `t2m` is at or above 32.2 C, and open 1 when it is not.
   32.2 C is the fact sheet's 90 F cooling trigger reused, ASSUMED.
8. Within the hour, in this order: add the rain and cap at 60, so `rain_in_mm = min(60, soil + rain_mm x open) - soil`, which is only what was stored; then subtract the crop's use; then, if `soil < 18`, set `irrigation_mm = 54 - soil` and `soil = 54`.
9. The soil starts at 54, and the fins are fully open or fully shut except in rule 7.

The priority is night, then rain, then light, and it is the answer to "opening for rain also lets light in".

## Dependencies

`pandas==2.2.3`, `numpy==2.2.3`, `pytest==9.0.2`, already pinned by S1, and nothing new.

## Steps

1. The rain parser. Check: annual total 1004.1 mm, 381 rain hours, the wettest UTC day 2023-10-26 at 71.8 mm, the wettest hour 38.4 mm at `2023-10-26T18`, and `2023-01-03T12` reads 9.9.
2. The join. Check: 8,760 rows, the rain sums to 1004.1, 4,566 rows have `ghi > 0`, 226 rain hours fall in daylight holding 662.5 mm, and the mean `ghi` of rainy daylight hours over dry ones is 0.436 within 0.005.
3. The light. Check: `K` is 2.0565, the outdoor annual light is 12,816.8 mol, the mean is 35.11 a day, 2023-07-05 reads 43.26, 2023-06-05 reads 28.42, the darkest whole local day is 2023-11-13 at 4.28, and the brightest is 2023-04-30 at 59.61.
4. The reference evaporation. Check: 1,244.3 mm for the year, 4.43 mm on 2023-07-05, and 2.76 mm on 2023-06-05, by local days.
5. The simulation. Check: no RAIN_OPEN where `ghi` is 0, the lettuce takes in no rain at all, the soil stays between 0 and 60, 897 daylight hours have `t2m` at or above 32.2, and rule 4 can pass at most 171 hours holding 433.7 mm.
6. The summary. Check: two runs give identical bytes.

Monthly rain, for the parser's test: 101.7, 18.1, 44.8, 102.8, 137.0, 92.0, 69.9, 0.0, 84.3, 172.8, 111.3, 69.4.

Local days are America/Chicago.
The UTC file starts at local 18:00 on 2022-12-31, six night hours, so 2023-12-31 lacks only dark evening hours and counts as a whole day.

## Acceptance

`python software/h1/build.py --city houston` and `pytest software/tests/test_h1.py` exit 0 with `socket.socket` patched to raise.
If an expected value does not match, the agent stops and reports it, and does not edit the value.

### The year, asserted with tolerances

The soil latch makes the results depend on the path, so these carry tolerances: shares within 0.03, days within 3, state counts within 5 hours.

| Zone | Hours in each state | Rain stored, mm | Irrigation, mm | Crop use, mm | Rain's share | Soil range, mm |
|---|---|---|---|---|---|---|
| A lettuce | NIGHT 4194, LIGHT_OPEN 2641, SHADE 1699, RAIN_SHUT 226 | 0.0 | 579.0 | 606.4 | 0.000 | 18.0 to 54.0 |
| B hydrangea | NIGHT 4194, LIGHT_OPEN 2242, SHADE 2098, RAIN_SHUT 155, RAIN_OPEN 71 | 169.2 | 289.2 | 469.6 | 0.369 | 18.02 to 59.51 |
| C blueberry | NIGHT 4194, LIGHT_OPEN 3452, HEAT_SHADE 888, RAIN_SHUT 156, RAIN_OPEN 70 | 159.5 | 795.3 | 986.5 | 0.167 | 18.01 to 59.99 |

The rain's share is the rain stored over the rain stored plus the irrigation.
The lettuce meets its 17 mol on 301 of 365 days, and the hydrangea its 12 mol on 324.

By local month, rain stored and irrigation in mm:

| Month | Lettuce days met | B rain | B irrigation | C rain | C irrigation |
|---|---|---|---|---|---|
| 1 | 18 | 4.9 | 0.0 | 41.5 | 0.0 |
| 2 | 20 | 7.9 | 36.1 | 7.9 | 36.0 |
| 3 | 26 | 2.9 | 36.1 | 2.9 | 72.3 |
| 4 | 25 | 0.0 | 36.4 | 0.3 | 108.9 |
| 5 | 28 | 28.7 | 0.0 | 43.5 | 72.1 |
| 6 | 30 | 16.1 | 36.1 | 16.1 | 108.3 |
| 7 | 30 | 68.5 | 0.0 | 0.0 | 72.5 |
| 8 | 31 | 0.0 | 36.2 | 0.0 | 108.3 |
| 9 | 29 | 13.6 | 36.1 | 25.4 | 72.4 |
| 10 | 24 | 0.0 | 36.1 | 3.5 | 72.4 |
| 11 | 20 | 17.7 | 0.0 | 9.8 | 36.0 |
| 12 | 20 | 8.9 | 36.1 | 8.6 | 36.0 |

A monthly share of 1 only means no irrigation event fell in that month, so the summary shows the two amounts by month and the share only for the year.
In July the blueberry stores nothing while the hydrangea stores 68.5 mm, purely from where each zone's latch stood, and the page has to be able to say so.

### The demo day, 2023-06-05, asserted for the hydrangea only

The soil at local midnight: lettuce 35.17, hydrangea 22.89, blueberry 29.82.

| Local hour | `ghi` | Rain, mm | A lettuce | B hydrangea | C blueberry |
|---|---|---|---|---|---|
| 6 to 11 | rising to 681.6 | 0 | LIGHT_OPEN | LIGHT_OPEN, 12.86 mol by the end of 11 | LIGHT_OPEN |
| 12 | 677.9 | 0 | LIGHT_OPEN, reaches 17.37 mol | SHADE, holding 12.86 | LIGHT_OPEN |
| 13 | 651.0 | 0 | SHADE | SHADE | LIGHT_OPEN |
| 14 | 243.1 | 8.9 | RAIN_SHUT | RAIN_OPEN, soil 30.40 | RAIN_OPEN, soil 36.35 |
| 15 | 127.8 | 6.9 | RAIN_SHUT | RAIN_OPEN, soil 37.22 | RAIN_OPEN, soil 43.16 |
| 16 | 74.8 | 0.3 | RAIN_SHUT | RAIN_OPEN, soil 37.47 | RAIN_OPEN, soil 43.41 |
| 17 | 95.2 | 1.0 | RAIN_SHUT | RAIN_SHUT | RAIN_SHUT |
| 18 to 19 | about 20 | 0 | SHADE | SHADE | LIGHT_OPEN |
| 20 on | 0 | 0 | NIGHT | NIGHT | NIGHT |

- The hydrangea stores 16.1 mm that day, and takes 2.97 mol of light it did not want while open for the rain, 12.86 to 15.83, which is the honest cost of the rain rule, visible on the screen.
- The 17:00 rain is refused by every zone, because there is no daylight three hours later, so the drying rule fires too.
- Assert the hydrangea's trace. Do not assert the blueberry's: it opens on a margin of 0.18 mm, 29.82 against the threshold of 30, and any small difference in implementation flips it.
- No zone that opted in is "wet and therefore shut" that day. The lettuce stays shut because it opted out. The page says "opted out", never "wet enough".
- No HEAT_SHADE hour falls on 5 June. That branch fires on 888 other hours, so every rule is exercised within the year and no constant was tuned.
- Other days with a large RAIN_OPEN, as backups: hydrangea on 2023-05-14, 2023-07-06, and 2023-07-25, and blueberry on 2023-05-10 and 2023-09-04.

## Files

May create: `data/crops.csv`, `data/processed/weather-houston.csv`, `data/processed/sim-houston.csv`, `data/processed/sim-summary-houston.csv`, `software/h1/*.py`, `software/tests/test_h1.py`.
Must not touch: `planning/`, anything in `hack-mit`, and S1's files.

## Honesty labels

- "Modelled" on every output.
- "Sun and temperature are NASA POWER for 2023, modelled from satellite and reanalysis. Rain is the Houston Hobby gauge for 2023, measured. Same place, same year."
- "2023 was a dry year, 28 percent under the normal."
- Every ASSUMED constant is listed in the README with its value.
- Never claimed: climate control, safety from disease, yield, measured water savings.

## Citations

NASA POWER, with the two citation lines in package S1; NOAA NCEI Global Hourly, ISD, believed public domain and to be confirmed; Purdue HO-238-W; the Cornell CEA Hydroponic Lettuce Handbook; the Washington State University blueberry fact sheet; FAO Irrigation and Drainage Paper 56; Noriega Gardea et al. 2021, Atmosfera 34(3).

- Cornell: https://cpb-us-e1.wpmucdn.com/blogs.cornell.edu/dist/8/8824/files/2019/06/Cornell-CEA-Lettuce-Handbook-.pdf
- Purdue: https://www.extension.purdue.edu/extmedia/ho/ho-238-w.pdf
- WSU: https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/3274/2025/08/FactSheet_ReducingHeatDamageinBlueberries.pdf
- FAO-56: https://www.fao.org/4/x0490e/x0490e07.htm and https://www.fao.org/4/x0490e/x0490e0b.htm
- Noriega Gardea: https://www.redalyc.org/journal/565/56572301008/html/
- NWS Houston normals: https://www.weather.gov/hgx/climate_hou_normals_summary

## Cut, on purpose

The ray cast shade table, partial fin angles beyond rule 7, a second city, forecasts, leaf wetness, growth stages, and any screen, which is package H2.

## Open questions for a person

- Does the lettuce opt out of rain? The package says yes.
- A bucket sized for containers or for soil?
- Is a drought year the year the team wants to show? It makes the honest story harder and more interesting: no rain at all in August.

## What the team would say

"In Houston, in a dry year, letting the rain through met about 37 percent of the hydrangea zone's water and about 17 percent of the blueberry zone's, and none in August, when no rain fell at all, while the roof held the lettuce to its light target on about 300 of 365 days. Simulated."
The final figures are read from the build's own output, never typed from this file.

The two hardest questions:

- "Growers keep rain off crops, so why let it in?"
  True for glasshouses and for fruit near harvest, which is why each crop opts in, only in daylight, only with drying time, and why we claim the water arithmetic and never safety from disease.
- "Is this real?"
  No. The rain is a real gauge, the sun is a satellite product for the same hours, the soil and crop numbers are textbook coefficients with assumed bucket sizes, and the only physical object is one printed fin.

## Estimated minutes

85.
