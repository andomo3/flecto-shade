# Data

Owner: Ameya, data engineering.

Provenance of every dataset the project uses, so a claim built on public data can be audited by a judge.
Every row says what was downloaded, from where, on what date, and which processed file it feeds.

The place is the Apopka area of Central Florida, and the demo day is 3 June 2023.
Both files are for the Orlando Executive Airport gauge, latitude 28.54653, longitude -81.33544, elevation 31.7 m.
The sun is a satellite product and is labelled modelled.
The rain is one real NOAA gauge and is the only thing in the project that is measured.

## Provenance

| Dataset | Source | Downloaded | Feeds |
|---|---|---|---|
| NASA POWER hourly, Orlando Executive, 2023 | `https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_DNI,ALLSKY_SFC_SW_DIFF,T2M,PRECTOTCORR&community=RE&longitude=-81.33544&latitude=28.54653&start=20230101&end=20231231&format=CSV&time-standard=UTC` | 2026-09-19 | `processed/year-apopka-2023.csv`, by S1 |
| NOAA ISD global hourly, "ORLANDO EXECUTIVE AIRPORT, FL US" `72205312841`, 2023 | `https://www.ncei.noaa.gov/data/global-hourly/access/2023/72205312841.csv` | 2026-09-19 | `processed/weather-apopka.csv`, by H1 |

`raw/` is gitignored, so each laptop fetches its own copy and checks the sha256.

| File | Bytes | sha256 |
|---|---|---|
| `raw/nasa-power/power-hourly-orlando-executive-2023.csv` | 340,893 | `c81490d249cb1fc857b0edf44c54d6fcdbc7c1e5b30b326310138a10f25cefc4` |
| `raw/isd-rain/72205312841-2023.csv` | 6,393,887 | `d26366ed5b470b8a79d0c447b08b693b7b77f810bc8ee7a138c1a75682c64f08` |

Both were checked against these values on 2026-09-19, and every expected value in packages S1 and H1 was recomputed from them and matched.

## Why the sun is from a real year and not a typical one

An earlier plan joined a typical year of sun, stitched from several years, to one real year of rain.
On real files that made the rainy daylight hours brighter than the dry ones, a ratio of 1.11, because the two had nothing to do with each other.
With the sun from the same year as the rain the ratio is 0.627, so rainy hours are dark hours, as they are outside.

## Assumptions

Gate F6 checks this section.
Every named constant that S1 or H1 marks ASSUMED or RECALLED appears here with its value and its label.
S1 creates this section, and H1 adds its own rows.

| Constant | Value | Label | Package | Why it is not verified |
|---|---|---|---|---|
| `LOCAL_TZ`, and the hour stamp it converts | `America/New_York` | ASSUMED | S1 | No sentence saying the stamp is the start of the hour and the value its mean was found on NASA's pages. It rests on a fit done on the Houston file, where global closed best against direct and diffuse with the sun taken half an hour after the stamp. It matters only for joining to the rain, and both files stamp hour starts |

H1's evaporation constants belong here too, and the sources for them were checked on 2026-09-19.
They are written up in the next section so that H1 can copy them into rows.

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
So `g = 0.067116` kPa per C at 31.7 m stands, reached two independent ways.

Two limits that the packages did not record, and that belong on the label:

- Makkink is defined on a daily timescale, and H1 applies it hour by hour.
  The `D / (D + g)` weight moves with temperature through the day, so twenty four hourly values do not sum to what the daily formula would give.
  H1's sensitivity sweep from 0.95 to 1.05 probably brackets the difference, but this is an assumption stacked on an assumption.
- Makkink's reference surface is grass, and FAO-56's crop coefficients are calibrated against Penman-Monteith reference evaporation rather than Makkink's.
  Multiplying a Makkink figure by an FAO-56 `kc` is common practice and is still a small mismatch.

Every evaporation figure therefore stays labelled modelled, and none of it is called measured.

## What the sun file is, and is not

- The grid is coarse: 1 degree for the irradiance, and half a degree by five eighths for the rest.
  A cell is about 100 km across, so it is a regional average and not the sky over one shade house.
- Wh/m2 over one hour is the mean W/m2 for that hour, so nothing is converted.
- NASA's own precipitation column is not used anywhere.
  It is reanalysis, and it has 4,395 wet hours in 2023 where the gauge has 373.
- A local storm can rain under a bright cell.
  On 29 July 2023 at 14:00 local the gauge caught 11.2 mm in the hour while the satellite cell read 681.20 W/m2.
  That is the honest limit of joining a coarse satellite product to a point gauge, and it is why the sun is never called measured.
- Temperature goes below zero exactly once in the year, -0.27 C, so only the three irradiance columns are checked as non-negative.

## What downstream packages read from this file

`processed/year-apopka-2023.csv` is the interface H1 and H2 read.

H2's playback speeds were computed by a planner from this file before any page code existed, and they reproduce from it exactly.
On local 2023-06-03 the file gives 14 lit hours, local 6 to 19, and 10 dark.
At 2.4 seconds a lit hour and 0.5 a dark one that is 38.6 seconds for the day, 15.0 by the end of local hour 10 when the fern's fins shut, and 24.6 by the end of local hour 14 when the storm starts.
Those are H2's three asserted values, confirmed on 2026-09-19.

## Honesty label for the screen

"Orlando Executive Airport gauge, near Apopka, Florida, 2023, a real year.
Sun: NASA POWER, a satellite product for a cell about 100 km across, hourly means, modelled.
Rain: one NOAA gauge, measured."

## Citations for the submission

- "The data was obtained from National Aeronautics and Space Administration (NASA) Langley Research Center's Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division."
- "The data was obtained from the POWER Project's Hourly 2.10.2 version on 2026/09/19."
- No licence text was found on NASA's referencing page, and the submission says so.
- NOAA National Centers for Environmental Information, Integrated Surface Database, global hourly access.
- FAO-56, Allen, Pereira, Raes and Smith 1998, for the latent heat of vaporisation and the psychrometric constant.
- Copernicus Climate Change Service and KNMI, user manual for the reference evapotranspiration package, for the modified Makkink coefficient and its attribution to de Bruin 1987.

## Layout

- `raw/` is gitignored.
  Everything in it is downloaded by a person, with the sha256 checked.
- `processed/` holds the small CSVs the software reads, and is committed.
- `build_solar_2023.py` rebuilds `processed/year-apopka-2023.csv` from `raw/`, with the network off, giving identical bytes on every run.
