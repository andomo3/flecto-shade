# data

`raw/` is gitignored: it holds the downloaded source files.
`processed/` is committed: one small CSV per city, the day the demo plays.
`software/tools/build_day.py` rebuilds `processed/` from `raw/` with the network off.

## Provenance

| File | Source | Downloaded | Size |
|---|---|---|---|
| `raw/tmy-houston-v5_2.csv` | PVGIS typical meteorological year, `https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=29.76&lon=-95.37&outputformat=csv` | 2026-09-19 | 594,218 bytes |

## The Houston day

`processed/day-houston.csv` is 3 June 2013, the sunniest day in the Houston
file: the largest daily total of `G(h)`, peak 1020 W/m2, peak air temperature
34.6 C. It is 600 steps, so twenty four hours play in sixty seconds at ten
steps a second.

Columns: `step, local_time, ghi, elevation, azimuth, t2m, led, sun_angle`.
`ghi`, `t2m` and `local_time` come from the dataset. `elevation` and `azimuth`
are computed locally with `pvlib`. `led` and `sun_angle` are how the app drives
the lamp and the sun arm.

Everything in this directory is modelled: it sets the scene. The only measured
numbers in the demo are the sensors on the table, and the two are never mixed.

## Licences

PVGIS content is (c) European Union; EU content is CC BY 4.0.
`pvlib` is BSD 3 clause.
