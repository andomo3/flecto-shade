# Data

Owner: Ameya, data engineering.

Provenance of every dataset the project uses, so a claim built on public data can be audited by a judge.
Every row says what was downloaded, from where, on what date, and which processed file it feeds.

The place is Greater Boston, Massachusetts, and the demo day is 10 June 2023.
Both files are for the Boston Logan International Airport gauge, latitude 42.36057, longitude -71.00975, elevation 3.2 m.
The site moved here from the Apopka area of Central Florida on 2026-09-20; every figure below was recomputed from the new files on that date.
The sun is a satellite product and is labelled modelled.
The rain is one real NOAA gauge and is the only thing in the project that is measured.

## Provenance

| Dataset | Source | Downloaded | Feeds |
|---|---|---|---|
| NASA POWER hourly, Boston Logan, 2023 | `https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_DNI,ALLSKY_SFC_SW_DIFF,T2M,PRECTOTCORR&community=RE&longitude=-71.00975&latitude=42.36057&start=20230101&end=20231231&format=CSV&time-standard=UTC` | 2026-09-20 | `processed/year-boston-2023.csv`, by S1 |
| NOAA ISD global hourly, "BOSTON LOGAN INTERNATIONAL AIRPORT, MA US" `72509014739`, 2023 | `https://www.ncei.noaa.gov/data/global-hourly/access/2023/72509014739.csv` | 2026-09-20 | `processed/weather-boston.csv`, by H1 |
| NOAA NCEI 1991-2020 annual normals, `USW00014739` | `https://www.ncei.noaa.gov/data/normals-annualseasonal/1991-2020/access/USW00014739.csv` | 2026-09-20 | the `normal_mm` figure in `day.json`, by H2 |

`raw/` is gitignored, so each laptop fetches its own copy and checks the sha256.

| File | Bytes | sha256 |
|---|---|---|
| `raw/nasa-power/power-hourly-boston-logan-2023.csv` | 335,201 | `9d6310e79a7986e7bee10fcea8d71494b7b842ce659dd97be107e0acdbb355e3` |
| `raw/isd-rain/72509014739-2023.csv` | 8,784,897 | `2654aba24fe8fe2ad2ad36686346f92d9dc812caf507a53ec2e94638aacbccd9` |

Both were downloaded and hashed on 2026-09-20, and every expected value in packages S1 and H1 was recomputed from them on the same day.
The recomputed values are the ones now asserted in `software/tests/test_solar_2023.py` and `software/tests/test_h1.py`; the Apopka figures quoted in `planning/` describe the old site and no longer apply.

## Why the sun is from a real year and not a typical one

An earlier plan joined a typical year of sun, stitched from several years, to one real year of rain.
On real files that made the rainy daylight hours brighter than the dry ones, a ratio of 1.11, because the two had nothing to do with each other.
With the sun from the same year as the rain the ratio is 0.348 at this site, so rainy hours are dark hours, as they are outside.
The Apopka files gave 0.627 for the same check.

## Assumptions

Gate F6 checks this section.
Every named constant that S1 or H1 marks ASSUMED or RECALLED appears here with its value and its label.
ASSUMED means a choice the team made, and RECALLED means from memory rather than a source.

| Constant | Value | Label | Package | Why it is not verified |
|---|---|---|---|---|
| `LOCAL_TZ`, and the hour stamp it converts | `America/New_York` | ASSUMED | S1 | No sentence saying the stamp is the start of the hour and the value its mean was found on NASA's pages. It rests on a fit done on the Houston file. It matters only for joining to the rain, and both files stamp hour starts. Massachusetts keeps the same zone the Florida site used |
| `PAR_FRACTION` | `0.45` | ASSUMED | H1 | A choice inside the verified 0.44 to 0.55 range of global solar that is photosynthetic light. The measured range is lower, so light sums may read 5 to 18 percent high |
| `T_STRUCT` | `0.90` | ASSUMED | H1 | The shade house structure's own transmittance, for a roof with no glazing. Leaving it out changes every figure in the year table, which is how it was caught |
| `T_CLOSED` | `0.0` | ASSUMED | H1 | A closed fin is treated as opaque |
| `SOIL_CAPACITY` | `60.0` | ASSUMED | H1 | The bucket's size in mm. Whether it should be sized for containers or for ground soil is an open team decision |
| `SOIL_DRY_BELOW` | `30.0` | ASSUMED | H1 | Where the `want_rain` latch turns on |
| `SOIL_FULL_AT` | `54.0` | ASSUMED | H1 | Where the latch turns off |
| `SOIL_IRRIGATE_BELOW` | `18.0` | ASSUMED | H1 | Where the grower's own water takes over |
| `SOIL_START` | `54.0` | ASSUMED | H1 | The soil at the first hour of the year |
| `HARD_RAIN_MM` | `25.0` | ASSUMED | H1 | Rain this hard is shut out whatever the soil wants. A simplification |
| `DRYING_HOURS` | `3` | ASSUMED | H1 | Rain is only admitted when daylight remains three rows later. A simplification |
| `HEAT_SHADE_C` | `32.2` | ASSUMED | H1 | The blueberry fact sheet's 90 F cooling trigger, reused as a shading trigger. A Massachusetts year reaches it in only 5 hours, against 645 at the Apopka site, so this rule barely fires here |
| `HEAT_SHADE_OPEN` | `0.60` | ASSUMED | H1 | The open fraction that delivers the 40 percent shade the fact sheet recommends |
| `MAKKINK_C` | `0.65` | RECALLED | H1 | Confirmed at source on 2026-09-19, and misattributed. See the next section |
| `LATENT_HEAT_MJ_PER_KG` | `2.45` | RECALLED | H1 | Confirmed at source on 2026-09-19. See the next section |

The crop coefficients in `crops.csv` are a separate case.
FAO-56 Table 12 gives 1.05 for berries on bushes, VERIFIED, and the fern and the hydrangea have no row, so 1.00 is assumed for both and each row says so in its `note`.

## The evaporation constants, checked at source on 2026-09-19

Package H1 marks the Makkink form, its 0.65 coefficient, and the 2.45 divisor RECALLED, meaning from memory and not confirmed.
All three are now confirmed, and one of them is misattributed.

**The 2.45 divisor is right.**
FAO-56 chapter 3 states that a single value of 2.45 MJ per kg is taken in the simplification of the Penman-Monteith equation, and that it is the latent heat for an air temperature of about 20 C.
Source: `https://www.fao.org/4/x0490e/x0490e07.htm`.

**The 0.65 coefficient is right, but it is not Makkink's.**
The Copernicus Climate Change Service user manual for the KNMI reference evapotranspiration package prints the formula with C = 0.65, and footnotes it:
"This formula differs slightly from the original Makkink (1957) formula, who used C=0.61 and an additive term of 0.12mm/day. De Bruin (1987) concludes that the current form describes reasonably well the evapotranspiration of grass."
So the constant is the modified Makkink of de Bruin 1987, which KNMI has run operationally since 1987, and not Makkink 1957.
The project should name it "modified Makkink, de Bruin 1987" wherever it names the method.
Source: `https://surfobs.climate.copernicus.eu/documents/C3S_D311a_Lot4.3.1.5_user_manual_PET_v5_APPROVED_Ver2.pdf`.

**The psychrometric constant agrees from two directions.**
The same manual writes it as `0.00163 x P / lambda`.
Dividing 0.00163 by 2.45 gives 0.0006653, which is FAO-56 equation 8's `0.665 x 10^-3 x P`.
So `g = 0.067339` kPa per C at the gauge's 3.2 m stands, reached two independent ways.

Two limits that the packages did not record, and that belong on the label:

- Makkink is defined on a daily timescale, and H1 applies it hour by hour.
  The `D / (D + g)` weight moves with temperature through the day, so twenty four hourly values do not sum to what the daily formula would give.
  H1's sensitivity sweep from 0.95 to 1.05 probably brackets the difference, but this is an assumption stacked on an assumption.
- Makkink's reference surface is grass, and FAO-56's crop coefficients are calibrated against Penman-Monteith reference evaporation rather than Makkink's.
  Multiplying a Makkink figure by an FAO-56 `kc` is common practice and is still a small mismatch.

Every evaporation figure therefore stays labelled modelled, and none of it is called measured.

What the sweep shows at this site, recorded on 2026-09-20:
the fern holds its answer in the demo day's storm hour in all six nudged runs, because it opts out of rain outright and no evaporation assumption can move it.
The hydrangea and the blueberry each hold in four of the six.
The margins on 10 June are wide, the blueberry's soil is 46.04 mm against a 30 mm latch, so this is not a near miss on the day; it is the soil latch being path dependent over a whole year.
A year run at a slightly different evaporation arrives at the storm in a different state.
At the Apopka site the fern and the blueberry held across the sweep and the hydrangea was the fragile one, so the ordering is a property of the site and not of the rules.
`software/tests/test_h1.py::test_where_the_demo_day_stops_being_robust` pins the exact flips.

## What the sun file is, and is not

- The grid is coarse: 1 degree for the irradiance, and half a degree by five eighths for the rest.
  A cell is about 100 km across, so it is a regional average and not the sky over one shade house.
- Wh/m2 over one hour is the mean W/m2 for that hour, so nothing is converted.
- NASA's own precipitation column is not used anywhere.
  It is reanalysis, and it has 3,742 wet hours in 2023 where the gauge has 729.
- A local storm can rain under a bright cell.
  The clearest case in this file is the demo day itself: on 10 June 2023 at 14:00 local the gauge caught 5.3 mm in the hour while the satellite cell read 664.42 W/m2.
  That is the honest limit of joining a coarse satellite product to a point gauge, and it is why the sun is never called measured.
  It is also why the demo day looks bright through its storm hour, and the screen should not claim otherwise.
- Temperature goes below zero in 1,259 hours of a Massachusetts year, down to -24.75 C, so only the three irradiance columns are checked as non-negative.
  At the Apopka site it went below zero once.
- The gauge files a second FM-15 row in two hours of the year, 2023-02-23T22 and 2023-08-15T15 UTC, an off-schedule report followed by the regular one at :54.
  Both report a period of 01, so the windows overlap; the parser's rule of taking the last row in the hour keeps the regular report.
  The Apopka gauge had none of these.
- 33 hours of the year carry no usable AA1 field and are read as 0 mm. The Apopka gauge had 2.

## What downstream packages read from this file

`processed/year-boston-2023.csv` is the interface H1 and H2 read.

H2's playback speeds are unchanged; the seconds they produce were recomputed from this file.
On local 2023-06-10 the file gives 15 lit hours, local 5 to 19, and 9 dark.
At 2.4 seconds a lit hour and 0.5 a dark one that is 40.5 seconds for the day, 16.9 by the end of local hour 10 when the fern's fins shut, and 26.5 by the end of local hour 14, the hour the storm falls in.
Those are H2's three asserted values, recomputed on 2026-09-20.

## Honesty label for the screen

"Boston Logan International Airport gauge, Boston, Massachusetts, 2023, a real year.
Sun: NASA POWER, a satellite product for a cell about 100 km across, hourly means, modelled.
Rain: one NOAA gauge, measured."

## Citations for the submission

- "The data was obtained from National Aeronautics and Space Administration (NASA) Langley Research Center's Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division."
- "The data was obtained from the POWER Project's Hourly 2.10.2 version on 2026/09/20."
- No licence text was found on NASA's referencing page, and the submission says so.
- NOAA National Centers for Environmental Information, Integrated Surface Database, global hourly access.
- FAO-56, Allen, Pereira, Raes and Smith 1998, for the latent heat of vaporisation and the psychrometric constant.
- Copernicus Climate Change Service and KNMI, user manual for the reference evapotranspiration package, for the modified Makkink coefficient and its attribution to de Bruin 1987.

## Layout

- `raw/` is gitignored.
  Everything in it is downloaded by a person, with the sha256 checked.
- `processed/` holds the small CSVs the software reads, and is committed.
- `build_solar_2023.py` rebuilds `processed/year-boston-2023.csv` from `raw/`, with the network off, giving identical bytes on every run.
