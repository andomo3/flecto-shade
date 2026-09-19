# H1: zone targets, light, rain, and the soil bucket

The heart of the louvre roof simulation.
Planned on 2026-09-19 by planning agents that opened every source and read the real files.
The planner's replica first reproduced a full set of values on files for another Gulf Coast site, then ran the same method on the Florida files, so the method is checked and every value below is Florida's.
VERIFIED means opened or computed that day, ASSUMED means a choice the team made, and RECALLED means from memory and not confirmed.

## Goal

Build a crops table, a clean hourly weather file with rain, and a deterministic hour by hour simulation of three crop zones under a roof of fins, for the Apopka area of Central Florida.
It runs with the network off, gives identical bytes on every run, and labels everything modelled.

## The setting

A shade house over soil or container crops, which the team calls a greenhouse in plain speech.
It is not a closed glasshouse, because closed greenhouses keep rain off the crop on purpose, see `../../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md`.

Why Apopka, VERIFIED from the University of Florida:

- The Mid-Florida Research and Education Center, in Apopka, describes itself as "Located in the heart of Florida's greenhouse and nursery industry", and "MREC specializes in foliage and ornamental plant production."
- "Florida leads the nation in production of tropical foliage plants, accounting for more than 55 percent of national wholesale value every year since the 1960s", from the foliage breeding program housed at the same centre.
- Shade houses are the practice there: "Dracaena sp. should be grown in a shadehouse", under "63 to 73% shade", and for Boston fern "a 30% to 60% shade fabric".
- Phrases seen only in search snippets, such as any "capital of the world" title, are not verified and are never said.

## Inputs

### The solar year

`flecto-stop/data/processed/year-apopka-2023.csv`, written by package S1 from NASA POWER, for the same gauge and year as the rain.
If it is absent, stop and report, and do not rebuild it here.
H1 uses its `time_utc`, `month`, `local_hour`, `ghi`, and `t2m` columns, and joins the rain on `time_utc`, because both files stamp the start of the hour.

### The rain, VERIFIED on the real file

- `hack-mit/data/raw/isd-rain/72205312841-2023.csv`, NOAA ISD global hourly, "ORLANDO EXECUTIVE AIRPORT, FL US", 2023: 6,393,887 bytes, sha256 `d26366ed5b470b8a79d0c447b08b693b7b77f810bc8ee7a138c1a75682c64f08`.
  Latitude 28.54653, longitude -81.33544, elevation 31.7 m.
  A person copies it into `flecto-stop/data/raw/isd-rain/` and checks the sha256.
- It was chosen from four gauges near Apopka as the most complete: 8,760 hourly reports, 2 lacking the rain field, against 13 missing hours at Orlando International, 35 at Sanford, and 25 at Leesburg.
- 11,349 rows. `REPORT_TYPE` is FM-15 in 8,760, FM-16 in 2,212, `SOD  ` in 365, and `SOM  ` in 12, with trailing spaces.
- The rain is in `AA1`, as "period hours, depth in tenths of a mm, condition, quality": `01,0000,9,5`, a wet hour such as `01,0239,9,5`, a trace as `01,0000,2,5`, and missing as depth 9999.
- The traps:
  - FM-16 special reports repeat the running hourly total, so summing every FM-15 and FM-16 value gives 3,728.5 mm, nearly three times the truth.
  - The `SOD` rows hold 24 hour totals.
  - A trace always has depth 0, in 307 rows.
- The rule: FM-15 rows only, `AA1` with period 01, depth not 9999, floor the time to the UTC hour, keep the last row in each hour, divide by 10, and a missing hour becomes 0.
  It is the rule first written for another site's file and it applies unchanged, and the parser keeps its guard for two FM-15 rows in one hour even though this file has none.
- The 2 missing hours are `2023-07-30T22` and `T23`, and that day's own daily summary equals its hourly sum, so no rain was lost.
- Cross check: the station's daily summaries sum to 1338.1 mm, a gap of 0.04 percent. One day disagrees by more than half a mm: 2023-04-28, 4.3 in the summary against 0.0 hourly.
- The 1991 to 2020 normal for this station is 51.47 inches, 1,307 mm, so 2023 was 2.4 percent above normal, an ordinary year.

### The crops, each from a source

| Zone | Crop | Light rule | Value | Rain | Source |
|---|---|---|---|---|---|
| A | Boston fern, Nephrolepis | Daily light sum | 8 mol per m2 per day, the start of "high quality" | Opted out | VERIFIED: Purdue HO-238-W, Table 2, Nephrolepis: minimum 4, good 6, high quality 8 to 14 |
| B | Hydrangea, as nursery stock | Daily light sum | 12 mol per m2 per day, the start of "high quality" | Opted in | VERIFIED: the same table, hydrangea: minimum 6, good 8 to 10, high quality 12 and up |
| C | Southern highbush blueberry | Shade share | 0.40, the middle of 30 to 50 percent | Opted in | VERIFIED: "A 30-50% shade net is recommended for blueberry plants, while 75% or more shade can lessen fruit quality", Washington State University fact sheet |

What is solid and what is not, said plainly:

- The fern is the signature crop of the place, and it opts out of rain because its grower's guide wants the foliage "to dry during the day and prevent disease issues", and it is sold on clean fronds.
- The hydrangea is plausible and not a signature crop: "Best for North and Central Florida, French hydrangeas require shade, moist and fertile soils, and cool winters." It opts in as outdoor nursery stock.
- The blueberry industry is real there: Central Florida "accounts for approximately 50% of the total commercial blueberry acreage", about 5,700 acres, and "Drip irrigation is primarily used".
  Shading blueberries is not Florida practice, and the 40 percent is a heat figure from Washington State, and the page says so. It opts in as a field crop that is rained on anyway.
- Backups from the same Purdue table, if a crop is ever swapped: Dracaena, Aglaonema, and Dieffenbachia at 8 to 14, Schefflera from 14, and Ficus benjamina and Croton from 18.

### Light

- VERIFIED: 4.57 micromol per joule of photosynthetic light, and that light is 0.44 to 0.55 of global solar, with measured values of 1.69 to 1.96 mol per MJ of global solar, Noriega Gardea et al. 2021.
- `K = 0.45 x 4.57 = 2.0565` micromol per joule of global solar, a named constant.
  0.45 is a choice inside the verified range, and the measured range is lower, so light sums may read 5 to 18 percent high, and the README says so.
- Per hour: `mol_h = ghi x K x 3600 / 1e6 x T_STRUCT x (open + (1 - open) x T_CLOSED)`, and the day's total is the daily light sum.
- `T_STRUCT = 0.90`, ASSUMED, for a roof with no glazing. `T_CLOSED = 0.0`, ASSUMED, a closed fin is opaque. Both are named constants.

### Water

- VERIFIED crop coefficients, FAO-56 Table 12: berries on bushes 1.05. The fern and the hydrangea have no row, so 1.00 is ASSUMED for both.
- Reference evaporation per hour by Makkink: `ET0 = 0.65 x D / (D + g) x (ghi x 3600 / 1e6) / 2.45`.
- VERIFIED, FAO-56 chapter 3: equation 13, `D = 4098 [0.6108 exp(17.27 T / (T + 237.3))] / (T + 237.3)^2`; equation 8, `g = 0.665 x 10^-3 P`; equation 7, `P = 101.3 [(293 - 0.0065 z) / 293]^5.26`.
- The solar file has no pressure column, so pressure is a constant from the gauge's elevation, 31.7 m: `P = 100.9258` kPa and `g = 0.067116` kPa per C.
- NOT verified: the Makkink form itself, its 0.65 coefficient, and the 2.45 MJ per kg divisor. They are RECALLED, the README says so, and the evaporation figures carry that label.
- Crop use per hour is `kc x ET0 x open_fraction x T_STRUCT`, ASSUMED: a crop under shut fins uses no water in this model, and the 0.90 is part of it.
  Leaving out the 0.90 changes every figure in the year table, which is how it was caught.
- The soil bucket, all ASSUMED: capacity 60 mm, dry below 30, full at 54, and the grower's own irrigation tops it back to 54 when it falls below 18.

## Outputs

- `data/crops.csv`: `crop`, `zone`, `light_rule` as `dli` or `shade_pct`, `light_value`, `kc`, `rain_ok`, `light_source_url`, `kc_source_url`, `note`.
  Rows: A boston fern `dli` 8, `kc` 1.00, `rain_ok` 0; B hydrangea `dli` 12, `kc` 1.00, `rain_ok` 1; C blueberry `shade_pct` 0.40, `kc` 1.05, `rain_ok` 1.
  Where `kc` is ASSUMED, `kc_source_url` holds the FAO-56 table's address and `note` says "no row in the table, 1.00 assumed".
- `data/processed/weather-apopka.csv`: every column of the solar file plus `rain_mm`, joined on `time_utc`. 8,760 rows.
- `data/processed/sim-apopka.csv`: `hour`, `time_utc`, `zone`, `crop`, `open_fraction`, `light_mol_so_far`, `soil_mm`, `rain_in_mm`, `irrigation_mm`, `state`, `reason`. 26,280 rows.
  `reason` is empty except when `state` is RAIN_SHUT, where it is the first of these that applies, in this order: `opted_out`, `wet_enough` when `want_rain` is off, `no_drying_time` when there is no daylight three rows later, and `hard_rain` when the hour's rain is 25 mm or more.
  The page in package H2 turns it into words, so the screen can say why a zone stayed shut.
- `data/processed/sim-summary-apopka.csv`: by zone and month, `rain_in_mm`, `irrigation_mm`, and the days the light target was met, and by zone for the year, the rain's share.

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
9. The soil starts the year at 54, and the fins are fully open or fully shut except in rule 7.

The priority is night, then rain, then light, and it is the answer to "opening for rain also lets light in".

## Dependencies

`pandas==2.2.3`, `numpy==2.2.3`, `pytest==9.0.2`, already pinned by S1, and nothing new.

## Steps

1. The rain parser. Check: annual total 1338.6 mm, 373 rain hours, the wettest UTC day 2023-11-17 at 78.8 mm, the wettest hour 37.8 mm at `2023-07-04T21`, `2023-06-03T19` reads 23.9 and `2023-06-03T20` reads 18.5, and 2 missing hours become 0.
2. The join. Check: 8,760 rows, the rain sums to 1338.6, 4,568 rows have `ghi > 0`, 242 rain hours fall in daylight holding 924.2 mm, and the mean `ghi` of rainy daylight hours over dry ones is 0.627 within 0.005.
3. The light. Check: `K` is 2.0565, the outdoor annual light is 13,497.5 mol, the mean is 36.98 a day, 2023-07-05 reads 41.53, 2023-06-03 reads 40.95, the darkest whole local day is 2023-12-16 at 5.34, and the brightest is 2023-04-18 at 60.19.
4. The reference evaporation. Check: 1,332.6 mm for the year, 4.27 mm on 2023-07-05, and 4.06 mm on 2023-06-03, by local days.
5. The simulation. Check: no RAIN_OPEN where `ghi` is 0, the fern takes in no rain at all, the soil stays between 0 and 60, 702 daylight hours have `t2m` at or above 32.2, and rule 4 can pass at most 172 hours holding 563.2 mm.
6. The summary. Check: two runs give identical bytes.

Monthly rain, for the parser's test: 12.4, 21.1, 18.0, 61.0, 133.5, 197.9, 189.6, 183.1, 171.9, 69.8, 144.9, 135.4.

Local days are America/New_York.
The UTC file starts at local 19:00 on 2022-12-31, five night hours, so 2023-12-31 lacks only dark evening hours and counts as a whole day.

## Acceptance

`python software/h1/build.py --city apopka` and `pytest software/tests/test_h1.py` exit 0 with `socket.socket` patched to raise.
If an expected value does not match, the agent stops and reports it, and does not edit the value.

### The year, asserted with tolerances

The soil latch makes the results depend on the path, so these carry tolerances: shares within 0.03, days within 3, state counts within 5 hours.

| Zone | Hours in each state | Rain stored, mm | Irrigation, mm | Crop use, mm | Rain's share | Soil range, mm |
|---|---|---|---|---|---|---|
| A fern | NIGHT 4192, LIGHT_OPEN 1740, SHADE 2586, RAIN_SHUT 242 | 0.0 | 325.2 | 344.7 | 0.000 | 18.02 to 54.0 |
| B hydrangea | NIGHT 4192, LIGHT_OPEN 2094, SHADE 2232, RAIN_SHUT 182, RAIN_OPEN 60 | 260.0 | 216.7 | 503.8 | 0.545 | 18.03 to 59.77 |
| C blueberry | NIGHT 4192, LIGHT_OPEN 3681, HEAT_SHADE 645, RAIN_SHUT 182, RAIN_OPEN 60 | 186.3 | 904.8 | 1109.1 | 0.171 | 18.0 to 55.55 |

The rain's share is the rain stored over the rain stored plus the irrigation.
The fern meets its 8 mol on 354 of 365 days, and the hydrangea its 12 mol on 346.

By local month, days the target was met, and rain stored and irrigation in mm:

| Month | A met | B met | B rain | B irrigation | C rain | C irrigation |
|---|---|---|---|---|---|---|
| 1 | 31 | 29 | 0.0 | 36.0 | 6.3 | 36.2 |
| 2 | 27 | 27 | 0.0 | 36.1 | 0.0 | 108.6 |
| 3 | 31 | 31 | 0.0 | 36.1 | 0.0 | 108.4 |
| 4 | 30 | 30 | 39.0 | 0.0 | 16.8 | 72.3 |
| 5 | 31 | 31 | 0.0 | 36.1 | 0.0 | 144.8 |
| 6 | 30 | 30 | 47.6 | 0.0 | 11.7 | 109.1 |
| 7 | 31 | 31 | 68.0 | 0.0 | 87.2 | 0.0 |
| 8 | 30 | 30 | 34.4 | 0.0 | 14.9 | 72.3 |
| 9 | 30 | 30 | 35.8 | 0.0 | 3.8 | 72.7 |
| 10 | 29 | 29 | 31.2 | 0.0 | 40.4 | 72.1 |
| 11 | 26 | 21 | 0.3 | 36.2 | 0.3 | 72.3 |
| 12 | 28 | 27 | 3.7 | 36.1 | 4.9 | 36.0 |

A month with no irrigation only means no irrigation event fell in it, so the summary shows the two amounts by month and the share only for the year.
From April to October the hydrangea zone needed no irrigation in six months of seven, which is Florida's wet season showing through, and the dry season, November to May, is where the grower's own water does the work.

### The demo day, 2023-06-03

The soil at local midnight: fern 53.26, hydrangea 26.71, blueberry 34.11.
The peak temperature is 29.84 C, so no HEAT_SHADE hour falls on this day.

| Local hour | `ghi` | Rain, mm | A fern | B hydrangea | C blueberry |
|---|---|---|---|---|---|
| 5 | 0 | 0 | NIGHT | NIGHT | NIGHT |
| 6 to 10 | 5.7, 89.6, 217.7, 351.1, 549.0 | 0 | LIGHT_OPEN, 8.08 mol by the end of 10 | LIGHT_OPEN | LIGHT_OPEN |
| 11 | 696.3 | 0 | SHADE | LIGHT_OPEN, reaches 12.72 mol | LIGHT_OPEN |
| 12 to 14 | 821.3, 792.7, 726.4 | 0 | SHADE | SHADE, soil 25.48 by the end of 14 | LIGHT_OPEN, soil 31.17 by the end of 14 |
| 15 | 516.7 | 23.9 | RAIN_SHUT | RAIN_OPEN, soil 49.03 | RAIN_SHUT, soil 31.17 |
| 16 | 377.4 | 18.5 | RAIN_SHUT | RAIN_OPEN, soil 59.75 | RAIN_SHUT |
| 17 to 19 | 218.4, 122.6, 46.6 | 0 | SHADE | SHADE | LIGHT_OPEN, soil 30.91 at the end |
| 20, 21 | 0 | 0 | NIGHT | NIGHT | NIGHT |

What the day shows, and it is the whole product in one afternoon:

- The fern shuts at 11:00 with its 8 mol, the hydrangea at 12:00 with its 12, and the blueberry stays open all day.
- At 15:00 it rains, 42.4 mm in two hours.
  The hydrangea's soil is dry, so its fins reopen and its soil climbs from 25.48 to 59.75.
  The blueberry's fins stay shut because its soil is wet enough, 31.17 against a threshold of 30.
  The fern's fins stay shut because it opted out.
  Three zones, three different answers to the same rain, for three different reasons, and the page names each reason in words.
- The hydrangea stores 34.9 of the 42.4 mm, because the second hour fills the bucket to its 60 mm cap and about 7.5 mm is refused, so rule 8 is exercised on the screen.
- Opening for the rain costs the hydrangea 5.96 mol of light it did not want, 12.72 to 18.68, which is the honest price of the rain rule and goes on the result card.

How far to trust it, tested by scaling the evaporation by 0.95, 0.97, 0.99, 1.01, 1.03, and 1.05:

- On the demo day at local 15:00 and 16:00, `reason` is `opted_out` for the fern and `wet_enough` for the blueberry, and both are asserted.
- Assert the fern's and the hydrangea's traces hour by hour. The hydrangea held in six runs of seven, and at 0.95 its second rain hour flipped to shut.
- Assert the blueberry's RAIN_SHUT, and label it in the test as resting on a margin of 1.2 mm. It held in all seven runs.
- The sun dims as the rain arrives, 726 to 517 to 377, and does not collapse.
- The first rain hour, 23.9 mm, is 1.1 mm under the 25 mm hard rain cap. That is the gauge's reading and nothing was tuned.
- Backups, each of which flipped under a change of 1 to 3 percent and so is never asserted: 2023-08-14, 2023-08-17, 2023-04-13, 2023-07-29, and 2023-07-31, the last with a true collapse of the sun and an hour of 37.1 mm that trips the hard rain cap for every zone.

## Files

May create: `data/crops.csv`, `data/processed/weather-apopka.csv`, `data/processed/sim-apopka.csv`, `data/processed/sim-summary-apopka.csv`, `software/h1/*.py`, `software/tests/test_h1.py`, and the four gate tests `software/tests/test_gate_f4_schema.py`, `test_gate_f6_assumptions.py`, `test_gate_f7_rules.py`, and `test_gate_f14_sources.py`.
May change: `data/README.md`, only to add the section "Assumptions", a table of every constant S1 and H1 mark ASSUMED or RECALLED, with its value and its label, which is what gate F6 checks.
The four gate tests assert what `../gates.md` says for F4, F6, F7, and F14 and nothing more, and the expected values above stay in `test_h1.py`.
Must not touch: `planning/`, anything in `hack-mit`, and S1's files, except that one section of `data/README.md`.

## Honesty labels

- "Modelled" or "simulated" on every output.
- "Sun and temperature are NASA POWER for 2023, modelled from satellite and reanalysis. Rain is the Orlando Executive Airport gauge for 2023, measured. Same place, same year."
- "2023 was an ordinary year for rain there, 2.4 percent above the 1991 to 2020 normal."
- "The blueberry's shade figure comes from Washington State and is not Florida practice."
- Every ASSUMED and RECALLED constant is listed in the section "Assumptions" of `data/README.md` with its value.
- Never claimed: climate control, safety from disease, yield, measured water savings.

## Citations

NASA POWER, with the two citation lines in package S1; NOAA NCEI Global Hourly, ISD, believed public domain and to be confirmed; NOAA NCEI 1991 to 2020 normals for station USW00012841; Purdue HO-238-W; the Washington State University blueberry fact sheet; University of Florida IFAS documents EP149, EP550, and HS742; FAO Irrigation and Drainage Paper 56; Noriega Gardea et al. 2021, Atmosfera 34(3).

- Purdue: https://www.extension.purdue.edu/extmedia/ho/ho-238-w.pdf
- WSU: https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/3274/2025/08/FactSheet_ReducingHeatDamageinBlueberries.pdf
- UF/IFAS MREC: https://mrec.ifas.ufl.edu/about/ and foliage breeding: https://programs.ifas.ufl.edu/plant-breeding/tropical-foliage/
- UF/IFAS EDIS: EP149 on Dracaena, EP550 on Boston fern, and HS742 on blueberries, found through https://edis.ifas.ufl.edu, whose exact addresses the build agent records when it opens them.
- FAO-56: https://www.fao.org/4/x0490e/x0490e07.htm and https://www.fao.org/4/x0490e/x0490e0b.htm
- Noriega Gardea: https://www.redalyc.org/journal/565/56572301008/html/

## Cut, on purpose

The ray cast shade table, partial fin angles beyond rule 7, a second place, forecasts, leaf wetness, growth stages, and any screen, which is package H2.

## Open questions for a person

- A bucket sized for containers or for soil? Nursery and foliage stock is commonly grown in containers, which was not checked at a source, and a container holds far less than 60 mm, so a smaller bucket would mean more frequent rain openings and more irrigation events.
- Does the hydrangea stay, or does a second foliage crop from the Purdue table replace it, so that all three zones are signature crops of the place?

## What the team would say

"Near Apopka, Florida, in an ordinary year, letting the rain through met about 54 percent of the hydrangea zone's water and about 17 percent of the blueberry zone's, while the roof held the fern to its light target on about 354 of 365 days. Simulated."
The final figures are read from the build's own output, never typed from this file.

The two hardest questions:

- "Growers keep rain off crops, so why let it in?"
  True for glasshouses, for ferns, and for fruit near harvest, which is why each crop opts in, only in daylight, only with drying time, and why we claim the water arithmetic and never safety from disease.
- "Is this real?"
  No. The rain is a real gauge, the sun is a satellite product for the same hours, the soil and crop numbers are textbook coefficients with assumed bucket sizes, and nothing physical was built.

## Estimated minutes

85.
