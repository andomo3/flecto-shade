# data - local memory

Owner: the software and data role, abba.
This is the planning repo, and no analysis script is written here before the event.
Downloading a public dataset beforehand is allowed, and there is no network at the venue, so the download happens on Friday 2026-09-18.
The full reasoning is in `../docs/research/adaptive-bus-stop-canopy/dataset-choice.md`.

## What this directory becomes

`raw/` holds the downloaded files and is gitignored.
`processed/` holds one small CSV per city, the fast forward day, committed.
One script rebuilds `processed/` from `raw/` with the network off.

## Decisions that bind this directory

- Primary dataset: the PVGIS typical meteorological year hourly file, API version `v5_2`, no key, about 0.6 MB per city.
  Houston is `https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=29.76&lon=-95.37&outputformat=csv`.
- The sun's position is computed locally with `pvlib`, which must be pip installed on Friday.
- Fallback: the NSRDB file from `developer.nlr.gov`, which needs a free key, because NREL is now NLR and the old hosts are dead.
- The demo day is the sunniest day in the Houston file, the largest daily sum of `G(h)`, and its real date is shown on screen.
- Houston is the story.
  Other cities are a stretch, shown through a city picker, on the same calendar date so the comparison is honest.
- What is modelled and what is measured are never mixed: the dataset sets the scene, and the only measured numbers are the sensors on the table.

## To do on Friday, no code

- Download the Houston `v5_2` file into `raw/`, and the `v5_3` file as a spare.
- For each stretch city, one far north, one near the equator, one in the southern hemisphere, request the same URL with its latitude and longitude and see whether PVGIS answers.
  Coverage at very high latitudes and in the far south is unverified.
  If a city fails, `pvlib` clear sky irradiance works anywhere and is labelled "modelled clear sky".
- `pip install pvlib` into the virtual environment.
- Fill the provenance table in `README.md` with the URL, the date, and the file size.

## The skeleton, at the event

| Step | What | Check | Minutes |
|---|---|---|---|
| 1 | Load one raw file with pandas, skipping the header and footer blocks, and read the "Irradiance Time Offset" from the header | 8760 rows, the columns `time(UTC)`, `G(h)`, `Gb(n)`, `Gd(h)`, `T2m` | 15 |
| 2 | Sum `G(h)` per day and pick the largest | One date, printed with its peak `G(h)` and peak `T2m` | 10 |
| 3 | Convert UTC to local time, add the offset, and get elevation and azimuth from `pvlib.solarposition.get_solarposition` | The sun is highest near local noon and below the horizon at night | 20 |
| 4 | Map `G(h)` from 0 to about 1000 W/m2 onto LED duty 0 to 255, and elevation onto a sun servo angle 0 to 180 | Duty is 0 at night and near 255 at the day's peak | 10 |
| 5 | Interpolate to 600 rows, so 24 hours play in 60 seconds at ten rows a second, and write `processed/day-<city>.csv` | Columns `step, local_time, ghi, elevation, azimuth, t2m, led, sun_angle` | 15 |
| 6 | Wrap steps 1 to 5 in a function of city name, latitude, and longitude | The same script produces every city | 10 |

About an hour and a half, none of it blocking the engineers.

## The second track, for the Voloridge challenge, added 2026-09-19

The PVGIS replay sets the scene and is not an insight, so it does not compete for "Signal in the Noise" by itself.
The analysis that does is in `../docs/research/adaptive-bus-stop-canopy/voloridge-datasets.md`, with its six steps and a check per step.

- The pick is Houston METRO's "October Ridership by Stop" layer: 9,085 stops, boardings and a shelter flag in the same row, no key.
- The output is a ranking of the unsheltered stops where the most riders wait in the harshest sun, and the concentration curve behind it.
- The trap to handle and to show: transit centres and park and rides are flagged unsheltered and must be removed before any share is quoted.
- The farmworker's dataset, if there is time, is NOAA SOLRAD at Hanford with NCEI hourly temperature for Fresno.
- Before starting, ask Voloridge for the curated list and whether outside public data counts.
- It comes after the app's core loop, steps 1 to 7 in `../software/CLAUDE.md`, and it takes its hours from the city picker and the stretch features, never from the core loop.
- Every result is said as modelled, from October averages, a 2022 shelter flag, and an assumed wait.

On 2026-09-19 `raw/` was empty on the demo laptop.
The PVGIS Houston file is downloaded first, while the venue network works, because the demo needs it and this track does not.

## Pitch facts from the research, with their sources in the research file

- Houston's city bus stop layer marks 2,187 of 13,162 stops as sheltered, last edited June 2022.
- The heat study is Lanza, Ernst, Watkins and Chen 2025, Transportation Research Part D, doi 10.1016/j.trd.2025.104653.
- In a geometric model a leaf on the sunward eave adds far more shade hours than a roof tilting about its centre, modelled with placeholder dimensions and never measured.

## Licences to cite in the submission

PVGIS content is marked (c) European Union and EU content is CC BY 4.0.
Houston METRO's feed needs its attribution line if it is used.
`pvlib` is BSD 3 clause.
