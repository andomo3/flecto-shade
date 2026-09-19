---
title: Which public dataset to download before the event for the planner app
type: research
status: done   # open | in-progress | done | dropped
owner: abba   # one word handle of the teammate doing the research
updated: 2026-09-18
idea: adaptive-bus-stop-canopy
---

# Which public dataset to download before the event for the planner app

## Answer

Primary: the PVGIS typical meteorological year (TMY) hourly CSV from the EU Joint Research Centre, one file per city, with sun elevation and azimuth computed locally by pvlib instead of downloaded.
It needs no key, it answered for both Houston and Boston when probed on 2026-09-18, each file is about 0.6 MB, and EU content is CC BY 4.0.
Fallback: the NSRDB GOES TMY v4 CSV from the NLR (formerly NREL) developer API, which is the better irradiance product but needs a free API key and an email address in the request.
Alongside either one, download the Houston METRO GTFS zip for real stop locations, and the City of Houston GIS bus stop layer for which stops have a shelter.
The shade hours number is modelled from geometry and these files, and the only measured numbers in the project stay the two bench sensors on the table.

## Findings

### Primary: PVGIS TMY plus pvlib solar position

- The PVGIS API is open, needs no key, allows 30 calls per second per IP, and does not allow calls from browser JavaScript, so it is fetched once with curl or Python and never from the app, see [the PVGIS API page](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/api-non-interactive-service_en).
- Exact calls, verified to return HTTP 200 on 2026-09-18:
  - Houston: `https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=29.76&lon=-95.37&outputformat=csv`
  - Boston: `https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=42.36&lon=-71.06&outputformat=csv`
  - Swap `v5_2` for `v5_3` to get the newer release.
- Coverage of both cities is confirmed by the responses themselves, not by a coverage map.
  The `v5_2` response reports `radiation_db: PVGIS-NSRDB`, years 2005 to 2015, for both Houston and Boston.
  The `v5_3` response reports `radiation_db: PVGIS-ERA5`, years 2005 to 2023, for Houston.
- Use `v5_2` as the file the app reads, because its irradiance is satellite derived (from NSRDB) while `v5_3` falls back to the ERA5 reanalysis for the Americas.
  In the `v5_3` Boston file the first daylight hour of 1 January shows beam irradiance of 955 W/m2 with the sun about 10 degrees up, which is not physical, and the same hour in `v5_2` shows 519 W/m2.
  Download both versions anyway, they are small, and keep `v5_3` in `data/raw/` as a spare.
- File size, measured: 599,170 bytes for Houston `v5_3`, 594,218 bytes for Houston `v5_2`, 596,069 bytes for Boston `v5_3`.
  Each file has 8760 hourly rows plus a short header and footer.
- Columns in the file: `time(UTC)`, `T2m`, `RH`, `G(h)`, `Gb(n)`, `Gd(h)`, `IR(h)`, `WS10m`, `WD10m`, `SP`.
  We use `time(UTC)`, `G(h)` (global horizontal, W/m2), `Gb(n)` (beam normal, W/m2), `Gd(h)` (diffuse horizontal, W/m2), and `T2m` (air temperature, C) for the scene label.
- The header carries an `Irradiance Time Offset (h)` line, 0.5 in the `v5_3` files and 0.0 in the `v5_2` Boston response, so solar position must be computed at the timestamp plus that offset.
- A TMY stitches twelve months from different years, so the `year` in each timestamp varies by month.
  pvlib's reader handles this, and `pvlib.iotools.read_pvgis_tmy(filename, map_variables=True)` renames the columns to `ghi`, `dni`, `dhi`, `temp_air`.
- License: the file footer reads "PVGIS (c) European Union, 2001-2026", and the European Commission legal notice licenses EU owned content under CC BY 4.0, so attribution is required and reuse is allowed.
  I did not find a PVGIS specific licence page, the old legal notice URL returns 404.
- pvlib is on PyPI as `pvlib`, version 0.15.2 released 2026-06-16, licence BSD-3-Clause, Python 3.10 or later, and it pulls in numpy, pandas, scipy, pytz, requests, and h5py.
  It must be pip installed today, because there is no network at the venue.
- Function names, confirmed by installing 0.15.2 in a scratch environment and running them:
  - `pvlib.solarposition.get_solarposition(time, latitude, longitude)` uses the NREL SPA algorithm by default (`method='nrel_numpy'`) and returns the columns `apparent_zenith`, `zenith`, `apparent_elevation`, `elevation`, `azimuth`, `equation_of_time`.
  - `pvlib.shading.projected_solar_zenith_angle(solar_zenith, solar_azimuth, axis_tilt, axis_azimuth)` projects the sun onto the roof's cross section, which is the one angle the shade model needs.
  - `pvlib.iotools.get_pvgis_tmy` and `pvlib.iotools.read_pvgis_tmy` fetch and parse the PVGIS file.
- Solar position is astronomy, so it is computed, not downloaded, and it works offline for any stop and any hour.

### Fallback: NSRDB GOES TMY v4

- NREL is now NLR, and the old hosts `developer.nrel.gov` and `nsrdb.nrel.gov` no longer resolve.
  The live hosts are `developer.nlr.gov` and `nsrdb.nlr.gov`.
- Exact call, from [the endpoint docs](https://developer.nlr.gov/docs/solar/nsrdb/nsrdb-GOES-tmy-v4-0-0-download/), with the key and email filled in at run time and never committed:
  `https://developer.nlr.gov/api/nsrdb/v2/solar/nsrdb-GOES-tmy-v4-0-0-download.csv?wkt=POINT(-95.37%2029.76)&names=tmy-2024&interval=60&utc=false&attributes=ghi,dni,dhi,air_temperature,solar_zenith_angle&email=YOUR_EMAIL&api_key=YOUR_KEY`
- The endpoint is alive: a probe with the public `DEMO_KEY` and a placeholder email returned a structured 400 asking for a valid email, not a 404.
- Allowed `names` values include `tmy-2022`, `tmy-2023`, `tmy-2024`, and the `tdy` and `tgy` variants.
  Attributes include `ghi`, `dni`, `dhi`, `clearsky_ghi`, `clearsky_dni`, `air_temperature`, `solar_zenith_angle`, `cloud_type`, `wind_speed`, `relative_humidity`.
- Rate limit for direct CSV: 10,000 requests a day, at most 1 per second.
- A key comes from [the signup form](https://developer.nlr.gov/signup/), and the docs say a key is given after signing up.
  I could not confirm that issue is instant, because the form is rendered by JavaScript and I did not submit it.
- pvlib wraps this as `pvlib.iotools.get_nsrdb_psm4_tmy`, and its docs page resolves.
- Why it is the fallback and not the primary: it needs a key and a real email in the URL, the key wait is unverified, and I could not read a licence statement on `nsrdb.nlr.gov` because the site is JavaScript only.
  If PVGIS is down today, this is the next call to make.
- Last resort with no download at all: `pvlib.location.Location(lat, lon).get_clearsky(times, model='haurwitz')` returns a clear sky `ghi` from solar position alone.
  It is a model, not a dataset, so it does not satisfy the Voloridge "real public dataset" requirement on its own.

### Companion: real stops and shelters

- Houston METRO GTFS: `https://metro.resourcespace.com/pages/download.php?ref=4835&ext=zip` returns a zip of 12,660,993 bytes, and the Mobility Database mirror `https://files.mobilitydatabase.org/mdb-2060/mdb-2060-202609010158/mdb-2060-202609010158.zip` returns the same byte count.
  The Mobility Database lists it as the official feed, service period 2026-08-30 to 2027-02-13, 79 MB unzipped.
  The old URL `ridemetro.org/Downloads/google_transit.zip` now redirects to the home page and is dead.
- METRO terms, from [the digital assets page](https://www.ridemetro.org/about/news-media/digital-assets): reproduce, redistribute, and publicly display are permitted, and the notice "Data is provided by permission of The Metropolitan Transit Authority of Harris County, Texas." must be shown prominently.
  That line goes in the app footer and the README.
- Houston shelters: the City of Houston GIS layer "RS2689 Bus Stops shape file" has 13,162 stops with `WITH_SHLTR`, `SHELTER`, `BENCH`, `WITH_BNCH`, `STOPNAME`, `LAT`, `LON`.
  A live query returned 2,187 stops with `WITH_SHLTR = 1` and 10,975 with 0.
  The layer was last edited in June 2022, and its licence field only says the data was downloaded from the METRO digital assets page, so treat it as METRO data under the METRO terms and label it a 2022 snapshot.
  CSV export call, which pages at 2000 rows: `https://services.arcgis.com/NummVBqZSIJKUeVR/arcgis/rest/services/RS2689_Bus_Stops___shape_file/FeatureServer/0/query?where=1%3D1&outFields=STOPNAME,STOPABBR,LAT,LON,WITH_SHLTR,WITH_BNCH&returnGeometry=false&resultOffset=0&resultRecordCount=2000&f=json`
- MBTA GTFS: `https://cdn.mbta.com/MBTA_GTFS.zip`, 24,938,477 bytes, under the MassDOT Developers License Agreement, which grants non-exclusive, limited, revocable rights to use, reproduce, and redistribute, and requires clearly acknowledging MassDOT as the provider.
- Boston shelters: I found no MBTA dataset with a shelter field.
  The MBTA "PATI Bus Stops" layer (7,015 stops, CC0-1.0) records benches and trees per stop (`SeatNum17`, `SeatType17`, `Trees17`) but not shelters, and the MBTA GTFS reference does not mention shelters.
  Boston can be a second city for sun and irradiance, but the "which stops have a shelter" beat is Houston only.

### The Houston heat study

- The citation is Lanza, Ernst, Watkins, and Chen, "Heat stress mitigation by trees and shelters at bus stops", Transportation Research Part D, volume 140, article 104653, 2025, [doi 10.1016/j.trd.2025.104653](https://doi.org/10.1016/j.trd.2025.104653).
  The repo currently links the phys.org write-up, and the DOI is the primary source.
- Crossref lists the published version under CC BY 4.0, so the paper is open access.
- The UTHealth release gives the numbers: 17 stops, 13 days from 2023-07-20 to 2023-08-07, mean unshaded wet bulb globe temperature 92.5 F, tree shade 5.9 F cooler, the best shelter 5.9 F cooler, and the worst enclosed shelter 5.2 F hotter than open ground.
- I found no public dataset for the study: the UTHealth release links none, and OpenAlex lists none.
  ScienceDirect returned 403 to my fetch, so I could not read the paper's data availability statement.
  The study is a pitch citation, not a data source.

### Candidates compared

| Candidate | Key or wait | Size | Licence | Verdict |
|---|---|---|---|---|
| PVGIS TMY v5_2, per city | None | 0.6 MB, measured | CC BY 4.0 under the EC legal notice | Primary, works today for both cities |
| PVGIS TMY v5_3, per city | None | 0.6 MB, measured | Same | Spare, ERA5 irradiance is weaker at low sun |
| NSRDB GOES TMY v4 | Free key plus email, wait unverified | Not verified, 8760 rows | Not verified | Fallback, better product but more friction |
| pvlib solar position | pip install today | Package only | BSD-3-Clause | Used with either, replaces any sun position download |
| pvlib clear sky | None | None | BSD-3-Clause | Last resort, a model and not a dataset |
| Houston METRO GTFS | None | 12.7 MB zip | METRO terms, attribution line | Companion, real stop names and coordinates |
| City of Houston bus stop layer | None | 13,162 rows, size not verified | Points back to METRO terms | Companion, the only verified shelter flag |
| MBTA GTFS | None | 24.9 MB zip | MassDOT developer licence | Optional second city, no shelter data |
| MBTA PATI Bus Stops | None | 7,015 rows | CC0-1.0 | Lost, benches and trees but no shelters |
| Lanza et al. 2025 study data | Not public | None | Paper is CC BY 4.0 | Lost as data, kept as the pitch citation |

### How shade hours is computed

- Work in the vertical cross section perpendicular to the roof's long axis, which runs along the street.
  `projected_solar_zenith_angle(apparent_zenith, azimuth, 0, street_bearing)` gives the projected sun angle theta in that plane, 0 when the sun is over the ridge and positive toward one side.
- The roof is a slab of width `w` pivoting about its centre at height `h` above the bench seat, tilted by `beta`, and the bench has width `b` centred below.
- A point at height `z` casts its shadow `z * tan(theta)` away from the sun, so the slab's shadow on the bench plane is centred at `-h * tan(theta)` with width `w * cos(beta - theta) / cos(theta)`.
- The fixed roof holds `beta` at the noon value of theta, which is 0 for a north to south street.
  The tracking roof sets `beta = theta`, clipped to the leaf's travel, so its shadow width is `w / cos(theta)`.
- The shaded fraction of the bench for an hour is the overlap of the shadow interval with `[-b/2, b/2]`, divided by `b`.
- Shade hours per day or year is the sum of that fraction over hours with sun elevation above 5 degrees.
  The weighted version multiplies each hour by `Gb(n)` from the TMY, giving beam energy kept off the bench in kWh/m2, and hours with `Gb(n)` near zero count for neither roof because there is no beam to block.
- The geometry says something the pitch has to respect: tilting a slab about its centre widens the shadow but does not move it, so tracking alone gains little.
  With `w = 2.4`, `h = 2.4`, `b = 1.5` metres on a north to south street, geometry only and no weather, my check run gave Houston 1,123 shade hours a year fixed against 1,285 tracking, and Boston 979 against 1,129, a gain of about 15 percent.
- A leaf of length `L` on the sunward eave that turns square to the rays extends the shadow by `L / cos(theta)` on the side the sun gets in.
  With `L = 0.8` the same run gave Houston 1,925 and Boston 1,716, a gain of about 70 percent.
  That is closer to how the flaring leaves work, so the model in the app should be the eave leaf, and the dimensions should be the tabletop model's scaled up, not my placeholders.
- Modelled: sun position, the shadow geometry, the shade hours number, and the TMY irradiance, which is a statistical typical year built from satellite or reanalysis data and not any real day.
  The model ignores diffuse light, buildings, trees, roof transmittance, and partial leaf closure.
- Measured: only the two bench light sensors on the table, fixed roof against adaptive leaves under the lamp.
  The display should label shade hours as "modelled" and the two bars as "measured", and nobody should say the app measures heat stress.

## Implications for the build

- Today, with network: `pip install pvlib` into the project environment, download the two PVGIS files per city and the Houston GTFS zip into `data/raw/`, and page the Houston shelter layer into `data/raw/`.
  Keep `data/raw/` out of git if the GTFS zip is included, it is 12.7 MB.
- Processing to the committed CSVs, one script under `data/`:
  1. `read_pvgis_tmy` the raw file, shift the index by the header's irradiance time offset, and convert to the city's time zone.
  2. Call `get_solarposition` on that index and keep `apparent_elevation` and `azimuth`.
  3. Write `data/sun_houston.csv` with `month, day, hour, elevation, azimuth, ghi, dni, dhi, temp_air`, 8760 rows, under 1 MB.
  4. From GTFS `stops.txt` keep `stop_id, stop_name, stop_lat, stop_lon`, join the shelter flag from the city layer on the stop code where it matches, and write `data/stops_houston.csv` with 20 to 50 hand picked stops, because the app needs a picker and not the network.
  5. Precompute shade hours per stop and month with the model above, or compute it live, it is a few thousand multiplications.
- The street bearing per stop is not in GTFS `stops.txt`.
  Either type it in for the hand picked stops, or derive it from `shapes.txt`, which costs more than it is worth for a demo.
- The five lamp marks on the arc rig come from `sun_houston.csv` for one chosen day, so the structure role can have elevations today.
- Attribution lines for the app footer and README: PVGIS (c) European Union, the METRO permission notice quoted above, and MassDOT as provider if MBTA data is used.
- If Voloridge's curated set at the event includes a solar or transit dataset, the loader swaps the raw file and the rest of the pipeline stays.
- Replace the phys.org link in the idea file and the sibling research files with the DOI, as a separate change.

## Sources

- [PVGIS API, non-interactive service](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/api-non-interactive-service_en), endpoints, parameters, rate limit, no key, no AJAX.
- [PVGIS TMY generator](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/pvgis-tools/pvgis-typical-meteorological-year-tmy-generator_en), what the TMY is and the method paper.
- [PVGIS 5.3 release notes](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/pvgis-releases/pvgis-53_en), SARAH-3 and ERA5, 2005 to 2023.
- [PVGIS TMY v5_2, Houston](https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=29.76&lon=-95.37&outputformat=csv) and [v5_3, Houston](https://re.jrc.ec.europa.eu/api/v5_3/tmy?lat=29.76&lon=-95.37&outputformat=csv), the live responses probed on 2026-09-18.
- [European Commission legal notice](https://commission.europa.eu/legal-notice_en), CC BY 4.0 for EU owned content.
- [NLR developer network, NSRDB APIs](https://developer.nlr.gov/docs/solar/nsrdb/), the endpoint list.
- [NSRDB GOES TMY v4 download endpoint](https://developer.nlr.gov/docs/solar/nsrdb/nsrdb-GOES-tmy-v4-0-0-download/), parameters, attributes, rate limits.
- [NLR API key docs](https://developer.nlr.gov/docs/api-key/) and [key signup](https://developer.nlr.gov/signup/).
- [NSRDB home](https://nsrdb.nlr.gov/), resolves, content not readable without JavaScript.
- [pvlib on PyPI](https://pypi.org/project/pvlib/), version, licence, dependencies.
- [pvlib LICENSE](https://github.com/pvlib/pvlib-python/blob/main/LICENSE), BSD 3-Clause.
- [pvlib get_solarposition](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.solarposition.get_solarposition.html), [projected_solar_zenith_angle](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.shading.projected_solar_zenith_angle.html), [get_pvgis_tmy](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.iotools.get_pvgis_tmy.html), [read_pvgis_tmy](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.iotools.read_pvgis_tmy.html), [get_nsrdb_psm4_tmy](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.iotools.get_nsrdb_psm4_tmy.html).
- [pvlib solarposition.py source](https://github.com/pvlib/pvlib-python/blob/main/pvlib/solarposition.py) and [iotools/pvgis.py source](https://github.com/pvlib/pvlib-python/blob/main/pvlib/iotools/pvgis.py), output column names and the PVGIS column mapping.
- [Houston METRO digital assets and data terms](https://www.ridemetro.org/about/news-media/digital-assets) and [METRO transit data collection](https://metro.resourcespace.com/pages/collections_featured.php?parent=1726).
- [Mobility Database, Houston METRO feed mdb-2060](https://mobilitydatabase.org/feeds/gtfs/mdb-2060), producer URL, mirror URL, service period, and [the superseded mdb-154](https://mobilitydatabase.org/feeds/gtfs/mdb-154).
- [City of Houston GIS, RS2689 Bus Stops layer](https://services.arcgis.com/NummVBqZSIJKUeVR/arcgis/rest/services/RS2689_Bus_Stops___shape_file/FeatureServer/0), fields and the shelter counts.
- [MBTA GTFS developer page](https://www.mbta.com/developers/gtfs), [MassDOT Developers License Agreement](https://cdn.mbta.com/sites/default/files/2023-08/mbta-massdot-develop-license-agreement.pdf), and [MBTA GTFS reference](https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs.md).
- [MBTA PATI Bus Stops](https://mbta-massdot.opendata.arcgis.com/datasets/pati-bus-stops), fields and CC0-1.0 licence read through the ArcGIS Hub API.
- [Lanza et al. 2025, Transportation Research Part D](https://doi.org/10.1016/j.trd.2025.104653), metadata from [Crossref](https://api.crossref.org/works/10.1016/j.trd.2025.104653).
- [UTHealth Houston release on the study](https://sph.uth.edu/news/story/shelters-at-bus-stops-intended-to-provide-relief-from-heat-can-actually-result-in-higher-temperatures-uthealth-houston-researchers-discover), the study numbers.
- [Software demo and sponsor fit](software-demo-and-sponsor-fit.md), abba, 2026-09-15, the two jobs the data has to do.
