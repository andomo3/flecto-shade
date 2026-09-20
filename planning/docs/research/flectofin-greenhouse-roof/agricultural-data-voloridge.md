---
title: Which agricultural dataset carries a finding that supports the zoned roof, and competes for the Voloridge "Signal in the Noise" challenge
type: research
status: in-progress
owner: abba
updated: 2026-09-20
idea: flectofin-greenhouse-roof
---

# Which agricultural dataset carries a finding that supports the zoned roof, and competes for the Voloridge "Signal in the Noise" challenge

## Answer

The Florida Automated Weather Network, FAWN, run by UF/IFAS, publishes 15 minute measured solar radiation and rainfall from 57 stations, one of which sits at the UF/IFAS Mid-Florida Research and Education Center in Apopka and has run since 1997.
It is free, needs no key, and is the same sky the project already claims to simulate, only measured instead of modelled.

The finding, computed today from the real files and not yet reproduced in the event repo:

- **Rain in Central Florida does not survive 21 km.**
  Of the 557 hours in 2023 that were wet at either the Apopka station or the Avalon station, 21 km apart, only 205 were wet at both, which is 36.8 percent, with a bootstrap 95 percent interval of 32.7 to 40.9 percent.
  The same figure over 2018 to 2024 is 34 to 43 percent, mean 38 percent, so it is not one odd year.
- **The day to day light difference across 21 km is the same size as the difference between two crops' light targets.**
  The mean absolute difference in daily light integral between Apopka and Avalon in 2023 is 4.16 mol, and 3.48 mol once a standing sensor offset is removed.
  The gap between the fern's 8 mol target and the hydrangea's 12 mol is 4 mol.
- **The modelled sky the simulation runs on cannot see that at all.**
  NASA POWER returns a byte for byte identical irradiance series for the Apopka station and for the Orlando Executive gauge 23 km away, because both fall in one 0.5 by 0.625 degree cell.
  Its daily light integral still misses the measured day by 4 mol or more on 82 of 365 days, 22 percent, which is a whole crop gap.

Together those say the thing the roof is for.
The weather decorrelates over a few kilometres, and the data most people would reach for is smoothed over a hundred.
One roof position, decided from one number, for a whole site, is the same mistake at a smaller scale: the decision is coarser than the thing it is deciding about.
That is the pitch's claim, turned into a number a quant can argue with.

There is also a cleaning trap worth the whole submission on its own.
FAWN's timestamps follow the local clock and shift with daylight saving, and joining them to NASA POWER's UTC at a fixed five hours gives hourly RMSE 175 W/m2 and r 0.812, which reads as a bad satellite product.
Handling the shift gives RMSE 103 and r 0.934 on the same two files.
Half of the apparent error was the join.
That is signal in the noise, literally, and it is the slide that makes quants trust the rest.

This is planning.
Any analysis script is project code and is written in the event repo during the hacking period, never here.
The numbers above came from throwaway scripts kept outside the repo, and every one of them is recomputed in the repo before it is said out loud.

## The challenge

Voloridge Investment Management, platinum sponsor.
"Signal in the Noise: build something interesting from real-world data. Create a tool, model, visualization, or system that turns messy data into useful insights."
Themes named: Earth, Health, Climate, Transport, Genomics, Economics.
Judged on originality, technical excellence, insight, and execution.
The judges are quants, so expect the questions to be about the assumptions, the spread, and what breaks the finding, not about the visualisation.

Still open, and the same question the bus stop research left open in `../../../archive/docs/research/adaptive-bus-stop-canopy/voloridge-datasets.md`.
The transcribed challenge text says "We'll provide a curated selection of large, publicly available datasets", and it is not known whether a public dataset from outside that selection counts.
Ask at the booth, and ask before any hour is spent.
If outside data is not allowed, the shape of the analysis below survives with any gridded or station climate set in the curated list: it needs two or more nearby stations and one modelled product over the same hours.

## The dataset

| | |
|---|---|
| Name | Florida Automated Weather Network, FAWN, UF/IFAS |
| Station | `Apopka_320`, UF/IFAS Mid-Florida Research and Education Center, Orange County, N 28.63771, W 81.54675, 107 ft, Tavares-Millhopper fine sand, running since 1997-12-19 |
| Files | `https://fawn.ifas.ufl.edu/data/fawnpub/15_minute_obs/BY_STATION/Apopka_320/2023.csv`, one file a year, 1997 to 2026, about 2.9 MB each |
| Columns | Station ID, Date Time, soil temp, air temp at 60 cm, 2 m, and 10 m, relative humidity, dew point, rainfall in inches, wind speed, wind direction, solar radiation in W/m2 |
| Rows | 35,036 of an expected 35,040 for 2023 |
| Time | local clock, EST in winter and EDT in summer |
| Key | none, plain HTTP, directory listings browsable |
| Also | `daily_summaries/`, `hourly_summaries/`, and a peer reviewed gap-free 2005 to 2020 product for 30 stations, Peeling et al., Sci Data 10, 907 (2023) |

Two stations are worth naming out loud at the table.

- `Apopka_320` is at the Mid-Florida REC, which is the foliage and ornamental research station for the Apopka area, the setting the plan already chose.
- `Pierson_290`, 65 km north, is hosted by the Florida Fern Growers Association at Richardson Farms, which is the fern crop's own home.
  The project's fern zone has a weather station sitting in the industry that grows it.

Neighbours used for the pair analysis, all within 132 km:
`Avalon_304` Water Conserv II 20.9 km, `Okahumpka_303` USDA Whitmore Foundation Farm 33.4 km, `Umatilla_302` 33.7 km, `Ocklawaha_280` 59.2 km, `Lake_Alfred_330` UF/IFAS Citrus REC 61.7 km, `Pierson_290` 65.0 km, `Poinciana_335` 73.4 km.

## What is messy about it, which is the point

The challenge asks for messy data, and this is genuinely messy in ways that change the answer.

- **The schema changes between years.**
  2018 to 2020 split the stamp into `Date` and `Time` columns and carry a `Station Name`.
  2021 and 2022 are Excel's `M/D/YYYY h:MM:SS AM`, and midnight is written as a bare date with no time at all.
  2023 onward are ISO in a single `Date Time` column.
  A loader that assumes one format silently drops a year.
- **Rows are missing, and unevenly.**
  2023 row counts across the eight stations run 34,583 to 35,036 of 35,040.
  Apopka is short 4 quarter hours and Lake Alfred is short 457, which is four and threequarter days.
  An analysis that reindexes onto a full calendar and fills forward will invent weather at Lake Alfred, and the stations must be compared only on hours both of them actually recorded.
- **Two pyranometers 21 km apart disagree by a standing offset that drifts.**
  The median daily difference between Apopka and Avalon is -0.81 mol in 2018, +0.73 in 2019, +4.20 in 2020, +4.25 in 2021, +5.56 in 2022, +2.28 in 2023, and +2.28 in 2024.
  That is instrument bias, soiling, or a recalibration, not weather, and it has to be removed before any claim about weather is made.
  Removing it is the single most important step in the analysis, and it is the first thing a quant judge will ask about.
  It takes the 2023 mean absolute difference from 4.16 mol to 3.48 mol, so the finding survives, but only because it was checked.
- **Rainfall is a zero inflated tipping bucket in inches.**
  Most quarter hours are 0.00, so a mean is meaningless and a threshold has to be chosen and defended.
- **The timestamps follow the local clock, and the clock moves.**
  The irradiance weighted mean hour of the day at Apopka in 2023 is 12.13 in December and 12.36 in January, and 13.18 in June.
  Solar noon at longitude -81.55 barely moves across the year, so a one hour summer shift in the data is daylight saving, not the sun.
  NASA POWER is UTC, so the join is plus five hours in winter and plus four between 2023-03-12 and 2023-11-05.
  Getting it wrong costs 70 W/m2 of RMSE, as above, and it is invisible in any annual mean, which is how it survives review.
- **The rain threshold has one real resolution and it is not the one you pick.**
  The gauge tips in hundredths of an inch, so 0.254 mm is the smallest nonzero reading, and thresholds of 0.1 mm and 0.2 mm give exactly the same answer.
  At 0.5 mm the wet hour agreement rises from 36.8 to 44.1 percent, interval 39 to 49, on 354 rather than 557 hours.
  The finding holds at every threshold, and the number moves, so the number is always quoted with its threshold.

## The findings, in full

Computed on 2026-09-20 from the files named above.
Every figure here is provisional until it is recomputed by project code in the event repo.

### 1. Rain does not survive 21 km

Apopka against Avalon, 2023, hourly, a wet hour being 0.2 mm or more.

| | hours |
|---|---|
| common hours | 8,754 |
| wet at both | 205 |
| wet only at Apopka | 172 |
| wet only at Avalon | 180 |
| wet at either | 557 |
| agreement | 36.8 percent, bootstrap 95 percent interval 32.7 to 40.9 |
| same at a 0.5 mm threshold | 44.1 percent of 354 hours, interval 39 to 49 |

Across seven years, the same pair:

| Year | wet at either | wet at both | agreement |
|---|---|---|---|
| 2018 | 734 | 279 | 38 percent |
| 2019 | 665 | 282 | 42 percent |
| 2020 | 703 | 260 | 37 percent |
| 2021 | 635 | 214 | 34 percent |
| 2022 | 624 | 267 | 43 percent |
| 2023 | 557 | 205 | 37 percent |
| 2024 | 654 | 244 | 37 percent |

Disagreement grows with distance, which is what a real convective signal should do and a broken sensor should not.
The share of days on which two stations disagree about whether it rained at all, 1 mm or more, rises from 13.0 percent at 21 km to 22.7 percent at 132 km, across all 28 pairs and the 361 days all eight stations recorded.
The curve is monotone in the rough, not in every pair, and the nearest pair is the most alike and the farthest pair the least, which is the shape a convective signal has and a broken sensor does not.

### 2. Light across 21 km moves as much as light between crops

Mean daily light integral over the 361 days common to all eight stations, 2023, taking PAR as 45 percent of shortwave by energy at 4.57 umol per joule.

| Station | mean DLI, mol/m2/d | rain, mm |
|---|---|---|
| Apopka 320 | 37.7 | 1,194 |
| Umatilla 302 | 36.5 | 1,118 |
| Okahumpka 303 | 35.5 | 1,146 |
| Lake Alfred 330 | 35.0 | 1,295 |
| Avalon 304 | 34.8 | 1,003 |
| Poinciana 335 | 34.1 | 1,038 |
| Pierson 290 | 31.4 | 1,197 |
| Ocklawaha 280 | 31.3 | 1,042 |

Apopka against Avalon, after removing the median standing offset, is 3.48 mol mean absolute difference, and 32 percent of days are more than 4 mol apart.
The fern's target and the hydrangea's target are 4 mol apart.

### 3. The modelled sky cannot see 23 km, and half its apparent error was the clock

NASA POWER hourly, the product S1 already uses, against the Apopka pyranometer, 2023.

| | fixed 5 hour join | daylight saving handled |
|---|---|---|
| daylight hours compared | 4,578 | 4,350 |
| measured mean | 404 W/m2 | 425 W/m2 |
| modelled mean | 398 W/m2 | 419 W/m2 |
| bias | -6.0 W/m2 | -6.3 W/m2 |
| RMSE | 175 W/m2 | 103 W/m2 |
| r | 0.812 | 0.934 |

The bias barely moves and the RMSE falls by 40 percent, which is the fingerprint of a timing error rather than a physics error.
Anyone who joins these two public products naively concludes the satellite is poor, and they are wrong, and the annual means agree either way so nothing warns them.

Daily totals are immune to the shift, so they are the same in both columns: measured 37.5 mol, modelled 37.0 mol, RMSE 3.64 mol, and 82 of 365 days off by more than 4 mol, which is 22 percent and a whole crop gap.

And the reason that residual cannot be explained away as distance:

> A POWER request at the Apopka station, N 28.63771 W 81.54675, and a POWER request at the Orlando Executive gauge, N 28.54653 W 81.33544, 23.0 km apart, return byte for byte identical irradiance.
> Both points sit in one 0.5 by 0.625 degree MERRA-2 and CERES cell, about 55 by 61 km.

So the modelled product has no opinion at all about the thing the measured stations disagree about.
That is the cleanest single sentence in this research, and it belongs in the pitch: the data everyone uses is averaged over an area larger than the area where the rain actually differs.
The project's own simulation inherits that limit, and saying so first is both honest and the argument for the roof.

### 4. The demo's two shut hours check out, and the margin is thin

From measured Apopka light in 2023, the local hour at which the running daily light crosses each target.

| Crop | target | median shut hour | never reached |
|---|---|---|---|
| Boston fern | 8 mol | 11:00 | 6 days |
| hydrangea | 12 mol | 11:45 | 16 days |
| blueberry | 18 mol | 12:45 | 30 days |

The plan says the fern's fins shut at eleven and the hydrangea's at noon, and the measured year gives 11:00 and 11:45.
That is a real check on the beat the demo turns on, and it passes.
But the gap between the two is a median of 45 minutes and is over an hour on only 46 of 349 days, so the light rule alone separates the zones by less than the demo implies.

### 5. The rain rule is where the zones really part

At Apopka in 2023 there were 761 wet quarter hours, and 382 of them, 50 percent, fell before the hydrangea had taken its 12 mol.
Half of all rain arrives while opening the roof still costs the crop light.
That is the conflict the demo's fifth beat shows, and it is not a rare case.

## The risk this research found

The project assumes 8 mol a day for the Boston fern.
Seltsam et al., "Photosynthetic Daily Light Integral Influences Growth, Morphology, Physiology, and Quality of Swordfern Cultivars", HortScience 2022, DOI 10.21273/HORTSCI16717-22, recommend about 10 to 12 mol for containerised Nephrolepis in greenhouse production.
If the fern's target is 10 rather than 8, the fern and the hydrangea shut within about twenty minutes of each other and the demo's fourth beat, the moment one roof becomes three, is much weaker.

Three ways out, and the team picks one out loud.

1. Keep 8, cite the source it came from, and say on the page which figure it is and where it is from, as the honesty rules already require.
2. Lean the demo on the rain rule rather than the light rule, because finding 5 says half of all rain lands in the conflict window, and the three zones give three different answers to the same storm regardless of their light targets.
3. Swap the weakest crop for one with a genuinely low target.
   The blueberry zone is already the weakest of the three, by the plan's own assumptions.

Option 2 costs nothing, is supported by measured data, and is the recommendation.

## What Ameya would actually build, in about three hours

Each step with the check that makes it defensible.

1. Fetch `Apopka_320` and `Avalon_304` for 2018 to 2024 into `data/raw/fawn/`, gitignored, sha256 checked by a person.
   Check: row counts within 500 of 35,040, and the three date formats all parse.
2. Build a tidy 15 minute frame, local clock, with solar in W/m2 and rain in mm.
   Check: the irradiance weighted mean hour is near 12.2 in December and near 13.2 in June, which is how the daylight saving shift shows itself.
3. Wet hour agreement by pair and by year, at 0.1, 0.2, and 0.5 mm.
   Check: the ranking of the pairs does not change with the threshold, and say so if it does.
4. Daily DLI by station, the median offset removed per pair per year, and the residual spread reported with a bootstrap interval.
   Check: report the raw and the corrected number side by side, never only the corrected one.
5. Disagreement against distance across all 28 pairs, with the slope and its interval.
   Check: eight stations give 28 pairs and only 8 independent sites, so the interval is computed by resampling days, not pairs.
6. NASA POWER against the pyranometer at Apopka, hourly and daily, with the daylight saving join asserted in a test.
   Check: the fixed five hour join must give a clearly worse fit than the corrected one, and that gap, 175 against 103 W/m2, is the test.
   Second check: pull POWER at two coordinates 23 km apart and assert the series are identical, because that one assertion is the finding.
7. One figure: disagreement against distance, with the fern to hydrangea target gap drawn as a horizontal line, so the eye reads "the noise between two farms is the size of the difference between two crops".

That figure is the submission, and it is the one thing to build if the hours run out.

## What was considered and set aside

- USDA NASS Quick Stats API, `https://quickstats.nass.usda.gov/api`, and the 2019 Census of Horticultural Specialties, which is the only national source for shade structure area by state.
  It sizes the market and it holds no hour by hour signal, so it is a citation for the pitch, not the analysis.
  The API needs a free key by email, which is a venue network dependency, and the census tables are downloadable as PDF without one.
- The gap-free FAWN product, 2005 to 2020, 30 stations, figshare and Sci Data.
  It is cleaner and it stops at 2020, and the cleaning is somebody else's, which is the opposite of what this challenge rewards.
  Use the raw yearly files and cite the gap-free paper for the station metadata.
- NOAA NCEI ISD at Orlando Executive, station 72205312841, which H1 already uses for rain.
  It is 23.0 km from the Apopka station, and finding 1 is the reason that matters.
  Keep it, because swapping the project's rain source after the freeze is a pivot, not a cut, but say at the table that the gauge is 23 km away and that the analysis measures what that costs.
- NASA POWER as the only sky.
  Keep it for the simulation, because S1 is built on it and the freeze holds, and use the pyranometer only to say how wrong it is.
- Everything in the archived bus stop research, which is a different project.

## Honesty, which the gates already require

- Every figure here is modelled or measured, and which one is said every time.
  The FAWN irradiance and rainfall are measured, and gate F5 allows the word "measured" only in the page's rain source line, so none of these numbers go on the page without the team deciding how to word them.
- No figure for cost, yield, energy, or water saved appears here or anywhere.
- The analysis says the weather decorrelates over kilometres.
  It does not say what a roof is worth, and nobody says that it does.

## Sources

- FAWN data access and the FTP listings, UF/IFAS, `https://fawn.ifas.ufl.edu/data/` and `https://fawn.ifas.ufl.edu/data/fawnpub/15_minute_obs/BY_STATION/`, fetched 2026-09-20.
- FAWN station locations, `https://fawn.ifas.ufl.edu/tour/location_info.php`, fetched 2026-09-20.
- Peeling, J. A., Judge, J., Misra, V. et al. "Gap-free 16-year (2005-2020) sub-diurnal surface meteorological observations across Florida", Sci Data 10, 907 (2023), `https://doi.org/10.1038/s41597-023-02826-4`.
- NASA POWER hourly point API, version 2.10.2, the call already recorded in `../../../data/README.md`.
- Seltsam, L. et al. "Photosynthetic Daily Light Integral Influences Growth, Morphology, Physiology, and Quality of Swordfern Cultivars", HortScience (2022), DOI 10.21273/HORTSCI16717-22.
- USDA NASS Quick Stats API, `https://quickstats.nass.usda.gov/api`, and the 2019 Census of Horticultural Specialties tables, `https://www.nass.usda.gov/Publications/AgCensus/2017/Online_Resources/Census_of_Horticulture_Specialties/`.
- The Voloridge challenge slide, photographed at the opening ceremony, 2026-09-19, transcribed in `../../../archive/docs/research/adaptive-bus-stop-canopy/voloridge-datasets.md`.
