---
title: Which public dataset can show, in one honest chart, a link between irrigation, soil moisture, or humidity and soil degradation or plant disease?
type: research
status: done
owner: abba
updated: 2026-09-19
idea: flectofin-greenhouse-roof
---

# Which public dataset can show, in one honest chart, a link between irrigation, soil moisture, or humidity and soil degradation or plant disease?

## Summary

Top pick: the juniper and Phytophthora field survey on Zenodo (record 4086316, CC0), because it is the only candidate found where soil moisture and a disease outcome were both recorded on the same unit, by people in the field, with a peer reviewed paper that already states the link.
Runner up: the USDA ARS soil salinity survey on Ag Data Commons (DOI 10.15482/USDA.ADC/1527809, CC0), which records the degradation outcome (soil salinity as ECe) by year and depth on irrigated land, but holds no irrigation variable, so the irrigation story comes from the cited papers and not from the file.
An honest chart is realistic in 2 hours with the top pick, and a planner already ran it with pandas only: in all three sites the wetter half of the quadrats shows a higher share of symptomatic juniper than the drier half.
The relationship is modest (Spearman 0.18 over 147 quadrats), it is a forest and not a shade house, and it is soil moisture and not irrigation, so the chart supports the mechanism and nothing more.
No public dataset was found that pairs irrigation or substrate moisture with a recorded disease outcome in a greenhouse, nursery, or container setting, and three datasets that look like they do turned out not to on inspection.

Found by a research agent on 2026-09-19.
Every file marked "opened" below was downloaded and read with pandas 2.2.3 on the day, and the column names are copied from the files.
Anything not opened is marked "not verified".

## Ranked candidates

Ranked by how likely one data engineer can show a clean, honest, non spurious relationship in one chart within 2 hours, with pandas and numpy only.

| Rank | Dataset | Setting | Driver recorded | Outcome recorded | Rows | Licence | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Juniper and Phytophthora austrocedri, Zenodo 4086316 | UK upland forest, 3 sites | Soil moisture per quadrat | Yes, area of symptoms and qPCR result | 147 | CC0 | Use this |
| 2 | USDA ARS soil salinity surveys, Ag Data Commons | Irrigated farmland, California | None in file, irrigation history is in the papers | Yes, ECe by depth and year | 8,575 | CC0 | Runner up, for the degradation half |
| 3 | Greenhouse tomato, Universidad de Antioquia, Zenodo 16745911 | Greenhouse, Colombia | Soil moisture, air humidity, fertiliser treatment | Partly, soil EC and leaf chlorophyll, no disease | 2,665 | CC BY 4.0 | Usable but the obvious chart is confounded by sensor physics |
| 4 | Coffee leaf rust, Mendeley wpy54dw6t7 | Coffee plots, shade and full sun | Humidity, rain, shade | Yes, rust incidence | 442 | CC BY 4.0 | Humidity shows no relationship, shade does |
| 5 | AgriDataValue grapevine mildew, Zenodo 14989522 | Vineyard IoT, 2020 to 2024 | Daily humidity, temperature, rain | Doubtful, labels are 5 day blocks | 1,511 real rows | CC BY 4.0 | Do not use as an outcome |
| 6 | Grapevine resistance inducers, Zenodo 15077508 | Vineyard, Italy, 3 seasons | Daily leaf wetness, humidity, rain | Yes, but only season summaries | About 30 disease rows | CC BY 4.0 | Too few seasons for a weather link |
| 7 | Grape Disease Dataset, Mendeley 94j4ws2325 | Vineyard, India | Temperature, humidity, leaf wetness | No, the file has no disease column | 10,001 | CC BY 4.0 | Half useful only |
| 8 | Others: Horti-M3 tomato, Mendeley gnybw8p7zg, Kaggle sets, FAWN, SCAN, NEON | Mixed | Mixed | No, or unusable tonight | - | Mixed | Skip |

## Candidate 1 - Juniper and Phytophthora austrocedri (top pick)

- Source: Donald, Green, Searle, Cunniffe, and Purse, deposited through Dryad and served by Zenodo.
- Landing page: https://zenodo.org/records/4086316 (opened).
- Dataset DOI: 10.5061/dryad.3xsj3txc9.
- Direct downloads, all opened and returning HTTP 200:
  - https://zenodo.org/records/4086316/files/Birk_Fell_SSSI_Data_v020819.csv?download=1 (7.3 kB, 46 rows).
  - https://zenodo.org/records/4086316/files/Glenartney_SSSI_Data_v020819.csv?download=1 (10.1 kB, 51 rows).
  - https://zenodo.org/records/4086316/files/North_Rothiemurchus_SSSI_Data_v020819.csv?download=1 (9.9 kB, 50 rows).
- Licence: CC0 1.0, no login, no request form.
- Size and format: three comma separated CSV files, 147 rows in total, one row per quadrat.
- Columns that matter, copied from the files: `Quadrat.ID`, `Area.of.juniper`, `Area.of.symptoms`, `Mean.soil.moisture`, `TWI`, `Mean.Ellenberg.F.value`, `Watercourse.proximity`, `Altitude`, `Slope`, `Soil.type` (absent from the Birk Fell file).
- The lab confirmation column is `qPCR.result` in the Birk Fell and Glenartney files and `qPCR_result` in the North Rothiemurchus file.
- The density column is `Juniper.density` in two files and is misspelt `Juniper.denisty` in the North Rothiemurchus file.
- The three files do not share the same set of plant species columns, so concatenate on the shared columns only.
- Time span and resolution: a single survey per quadrat, so this is cross sectional, not a time series.
- The survey dates and the unit of `Mean.soil.moisture` were not read from the paper, so treat the unit as not verified and label the axis "soil moisture as recorded in the survey".
- Outcome: RECORDED.
  `Area.of.symptoms` over `Area.of.juniper` gives the share of juniper showing symptoms, and the qPCR column records whether the pathogen was confirmed in the lab.
- Real or synthetic: real field data, on the evidence of the paper's methods, named Sites of Special Scientific Interest, grid coordinates, and lab qPCR results.
- Quality problems:
  - Tiny sample, 46 to 51 quadrats per site.
  - The qPCR column is empty for 50 of 147 rows.
  - Soil moisture was taken once, so it stands in for a long run wetness that was not logged.
  - Symptoms are a visual estimate of area.
- Established result: Donald, F., Green, S., Searle, K., Cunniffe, N. J., and Purse, B. V. (2020). Small scale variability in soil moisture drives infection of vulnerable juniper populations by invasive forest pathogen. Forest Ecology and Management, 473, 118324. https://doi.org/10.1016/j.foreco.2020.118324
  The Zenodo abstract states that infection increases with soil waterlogging, more so in soils rich in peat or clay, and decreases near watercourses in sandy soils.
- The one chart: for each of the three sites, two bars, the mean share of symptomatic juniper in the drier half and in the wetter half of that site's quadrats, split at the site's own median of `Mean.soil.moisture`.
- What the planner's trial run gave, pandas only:
  - Birk Fell: 0.169 drier half, 0.385 wetter half.
  - Glenartney: 0.545 drier half, 0.612 wetter half.
  - North Rothiemurchus: 0.166 drier half, 0.268 wetter half.
  - Pooled quartiles of soil moisture: 0.21, 0.38, 0.44, 0.41.
  - Pooled Spearman correlation 0.18, and by site 0.19, 0.23, and 0.01.
- Most likely confounder: site and soil type.
  Wet quadrats also differ in altitude, slope, grazing, and juniper density, and the paper itself reports that the moisture effect depends on the soil.
  Splitting within each site removes the between site difference but not the within site ones.
- Honest caveat for the slide: the direction holds in all three sites, the effect is modest, and North Rothiemurchus shows almost no rank correlation.

## Candidate 2 - USDA ARS soil salinity surveys of irrigated farmland (runner up)

- Source: Guevara, Corwin, Singh, Benes, Quinn, Scudiero, and Skaggs (2022), USDA ARS U.S. Salinity Laboratory, on Ag Data Commons.
- Landing page: https://agdatacommons.nal.usda.gov/articles/dataset/Geospatial_Measurements_of_Soil_Electrical_Conductivity_Soil_Salinity_and_Soil_Saturation_Percentage_in_Irrigated_Farmland/24855282
  The landing page returned HTTP 403 to the page reader, so the metadata was read through the Figshare API at https://api.figshare.com/v2/articles/24855282 (opened).
- Dataset DOI: https://doi.org/10.15482/USDA.ADC/1527809.
- Direct downloads:
  - `ECe_USDA_ARS_USSL_v01.csv`, 736 kB, https://ndownloader.figshare.com/files/44529980 (opened, HTTP 200).
  - `README_GeospMeasurementsSoil.txt`, 6 kB, https://ndownloader.figshare.com/files/44529983 (opened).
  - `ECa_USDA_ARS_USSL_v01.csv`, 18 MB, https://ndownloader.figshare.com/files/44529974 (not opened, not needed).
- Licence: CC0, no login.
- Rows: 8,575 in the ECe file.
- Columns, copied from the file: `ECe`, `SP`, `Year`, `DATASET`, `ID`, `Top`, `Bottom`, `X`, `Y`.
  The README spells the year column `YEAR`, the file spells it `Year`.
  `ECe` is the electrical conductivity of the saturation paste extract in dS/m, `Top` and `Bottom` are sample depths, and `X` and `Y` are deliberately obfuscated coordinates.
- Time span: 1991 to 2019 in the `Year` column, across six survey campaigns.
- Outcome: RECORDED for degradation, since soil salinity is the outcome.
  The driver is NOT in the file: there is no irrigation amount, no water quality, and no soil moisture.
- Real or synthetic: real, lab determinations on soil cores, per the README.
- The useful subset is `DATASET_6`, one field in the southern San Joaquin Valley surveyed in 1999, 2002, 2004, 2011, and 2012, with 40 to 100 cores per year.
- The one chart: mean `ECe` by `Year` and depth band for `DATASET_6`.
  Trial run: surface layer 13.8, 12.4, 12.2, 14.3, 14.0 dS/m across the five years, and the 60 cm layer 22.6, 22.7, 22.3, 26.3, 24.8 dS/m.
  The clearer pattern is salinity rising with depth in every year, which is the signature of salts being pushed down by leaching.
- Quality problems:
  - In `DATASET_6` the rows with `Top` 0, 5, and 15 carry identical means, so one 0 to 30 cm sample appears to be repeated over three depth rows.
  - Different cores in different years, so year to year change mixes real change with sampling.
  - Field soil in California, not container media.
- Most likely confounder: the field was chosen because it was already saline and was irrigated with reused drainage water, so nothing here compares an irrigated with a non irrigated soil.
- Established result:
  - Corwin, D. L. (2012). Field-scale monitoring of the long-term impact and sustainability of drainage water reuse on the west side of California's San Joaquin Valley. Journal of Environmental Monitoring, 14(6), 1576-1596. https://doi.org/10.1039/c2em10796a (citation copied from the dataset README, the paper itself not opened).
  - Scudiero, E., Skaggs, T. H., and Corwin, D. L. (2017). Simplifying field-scale assessment of spatiotemporal changes of soil salinity. Science of the Total Environment, 587-588, 273-281. https://doi.org/10.1016/j.scitotenv.2017.02.136 (same, from the README).

## Candidate 3 - Greenhouse tomato, Universidad de Antioquia

- Landing page: https://zenodo.org/records/16745911 (opened), DOI 10.5281/zenodo.16745911, CC BY 4.0, no login.
- Direct download: https://zenodo.org/records/16745911/files/DB_Mobile_Manual_Tomato.csv?download=1 (opened, HTTP 200, 303 kB).
- Format: semicolon separated CSV, 2,665 data rows, 40 named columns plus an unnamed index, dates as day/month/year.
- Setting: 135 tomato plants in a greenhouse at Carmen de Viboral, Colombia, 27 fertiliser treatments, 20 weekly sessions from 2023-11-09 to 2024-04-01.
- Columns that matter, copied from the file: `Date`, `Plant`, `Treatment`, `N`, `P`, `K`, `Chlorophyll (SPAD)`, `Horiba Soil EC (mS/cm)`, `Horiba Soil  Na(ppm)` (two spaces in the name), `7in1_Moisture[%RH]`, `7in1_EC[uS/cm]`, `7in1_S_Temperature[C]`, `Air_sensor_Humidity[%RH]`, `Air_sensor_Temperature[C]`, `Total Weight of Harvest Fruits`, `Numer of Harvested Fruits` (misspelt in the file).
- Outcome: PARTLY recorded.
  Soil EC is a salt indicator and SPAD is a plant status indicator, but no disease and no irrigation amount is recorded.
- Real or synthetic: real, per the Zenodo description, though the description says missing or anomalous values were processed, and the method document was not opened.
- Quality problems: heavy gaps, the sensor columns are filled in 693 of 2,665 rows and the Horiba soil columns in 323.
- The one chart: mean `Horiba Soil EC (mS/cm)` by week, one line per nitrogen level `N`, to show salts building in the root zone as feeding goes on.
- Most likely confounder: fertiliser dose drives EC directly, so this is a fertiliser link and not an irrigation link.
- Trap to avoid: `7in1_Moisture[%RH]` and `7in1_EC[uS/cm]` correlate at 0.33, but a probe of this kind reads bulk conductivity, which rises with water content for physical reasons, so that scatter is not evidence of salt build-up.
- Peer reviewed paper using the data: none found, not verified.

## Candidate 4 - Coffee leaf rust subsets

- Landing page: https://data.mendeley.com/datasets/wpy54dw6t7/1 (opened), DOI 10.17632/wpy54dw6t7.1, CC BY 4.0, no login.
- Direct download of the smallest file, `CLRI_14D.csv`, 26.5 kB: https://data.mendeley.com/public-files/datasets/wpy54dw6t7/files/76f9fe43-9942-4176-927c-bb64385c220d/file_downloaded (opened, HTTP 200).
- Other files: `CLRI_7D.csv`, `CLRI_4D.csv`, `CLRI_3D.csv`, not opened.
- Rows: 442 in the file opened, where the landing page says 439.
- Columns, copied from the file: `tMin14-1`, `tAvg14-1`, `tMax14-1`, `tAmp14-1`, `hMin14-1`, `hAvg14-1`, `pre14-1`, `rDay14-1`, `hGrowth`, `cCLRI`, `shade`, `management`, `pCLRI`.
- Outcome: RECORDED, `pCLRI` is coffee leaf rust incidence at the prediction date and `cCLRI` is the current incidence.
- Real or synthetic: real plot monitoring, per the paper, with weather summarised over the 14 days before each date.
- There is no date column and no plot identifier, so rows cannot be ordered or grouped by place.
- Paper: Lasso, E., Corrales, D. C., Avelino, J., de Melo Virginio Filho, E., and Corrales, J. C. (2020). Discovering weather periods and crop properties favorable for coffee rust incidence from feature selection approaches. Computers and Electronics in Agriculture. https://www.sciencedirect.com/science/article/abs/pii/S0168169920309315 (author list and DOI not verified, the dataset page names Lasso, de Melo Virginio Filho, and Corrales).
- Trial result, and the reason for the low rank: average humidity against incidence gives a Spearman correlation of 0.01 and minimum humidity gives -0.02, so the humidity chart shows nothing.
- What does show: `shade` against `pCLRI` at 0.18, and `cCLRI` against `pCLRI` at 0.78.
- Most likely confounder: humidity stays between 83% and 97% in every row, so it never drops low enough to limit the disease, and last period's incidence dominates.
- Relevance: a shaded plot carrying more rust than a sunny one is a useful caution for a shade roof, and it is better to know it than to be asked it.

## Candidate 5 - AgriDataValue grapevine mildew

- Landing page: https://zenodo.org/records/14989522 (metadata opened through the Zenodo API), DOI 10.5281/zenodo.14989522, CC BY 4.0, no login.
- Direct download: https://zenodo.org/api/records/14989522/files/environmental_data.zip/content (opened, HTTP 200, 738 kB).
- Contents: 12 tab separated files under `environmental_data/env_data/`.
  Five are real sensor years, named `Temporal enviromental factors_Vine_original_2020_form.csv` through `..._2024_1_form.csv`, 1,511 daily rows from 2020-02-26 to 2024-04-28.
  Seven are synthetic, named `..._synth_form.csv` and `..._noised_N_form.csv`, generated with a Gaussian copula or added noise per the description, and must not be used.
- Columns, copied from the files: `date`, `air_hum`, `air_hum_min`, `air_hum_max`, `air_temp`, `air_temp_min`, `air_temp_max`, `pluvm`, `down_mildew`, `powdery_mildew`, `botrytis`, `erysiphe`.
- Outcome: DOUBTFUL.
  The description says the data includes "labeling on whether there is or not Powdery Mildew and Downy Mildew".
  On inspection every positive label is a block of exactly 5 days (one block of 4), there are 41 downy blocks and 42 powdery blocks, and the two columns agree on 99% of days.
  Two different diseases do not appear and vanish together in tidy 5 day windows, so these look like risk or treatment windows and not field observations.
  No document was found that says how the labels were made, so this is not verified either way.
- Trial result: within April to July, the share of labelled days by 7 day mean humidity runs 0.32, 0.41, 0.33, 0.30, 0.46, 0.49 across the bins, and the yearly correlations swing from -0.43 to 0.17.
- Most likely confounder: season, since every label falls in the growing season and humidity is highest in winter.
- Verdict: do not present these labels as recorded disease.

## Candidate 6 - Grapevine resistance inducers, Università Cattolica del Sacro Cuore

- Landing page: https://zenodo.org/records/15077508 (opened through the API), DOI 10.5281/zenodo.15077508, CC BY 4.0, no login.
- Files opened: `Readme.txt`, `NT_UCSC_RIs_DiseaseIncidenceSeverityTreatment.csv` (31 rows), `NT_UCSC_RIs_WeatherdataYear2.csv` (184 rows), `NT_UCSC_RIs_AUDPC.csv` (31 rows).
- Download pattern: https://zenodo.org/api/records/15077508/files/FILENAME/content.
- Columns: weather files `Date`, `Leafwetness`, `Rain`, `Temperature`, `Relativehumidity`, and disease file `Portion`, `Resistance_inducers`, `Disease`, `Incidence`, `Severity`.
- Setting: a vineyard at Castell'Arquato, Italy, seasons 2020 to 2022.
- Outcome: RECORDED, real field ratings, but only as treatment summaries, so a weather link would rest on three seasons, which is three points.
- The `Date` strings in the weather file look like day and month are swapped, for example `2021-02-04T00:00:00Z` following `2021-01-04T00:00:00Z` in a daily series that starts in April.
- Paper: Taibi, O., Fedele, G., Salotti, I., and Rossi, V. (2023). Infection Risk-Based Application of Plant Resistance Inducers for the Control of Downy and Powdery Mildews in Vineyards. Agronomy, 13(12), 2959. https://doi.org/10.3390/agronomy13122959
- Sister records by the same authors, not opened: https://zenodo.org/records/15077593 and https://zenodo.org/records/15081991.

## Candidate 7 - Grape Disease Dataset, Mendeley

- Landing page: https://data.mendeley.com/datasets/94j4ws2325/1, DOI 10.17632/94j4ws2325.1, CC BY 4.0.
- Direct download: https://data.mendeley.com/public-files/datasets/94j4ws2325/files/91e5b739-0366-44e5-b0ce-aecb43237f5e/file_downloaded (opened, HTTP 200, 287 kB).
- Data paper: Data in Brief, 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11190471/ (read through a page reader).
- Rows: 10,001, readings a few seconds apart on 25 dates from 2023-03-20.
- Columns, copied from the file: `Date ` (trailing space), `Time`, `Temperature`, `Humidity`, `LW ` (trailing space).
- Outcome: NOT RECORDED.
  The paper describes records "classified" for powdery mildew, downy mildew, and bacterial leaf spot, but the published file holds no disease column.
- Quality: `LW ` is 0 in at least three quarters of rows with a maximum of 1024, which looks like a raw sensor count.

## Other sources checked and set aside

- Horti-M3 tomato, https://zenodo.org/records/17217565, CC BY 4.0: one zip of 28.3 GB, unusable tonight, and disease records not verified.
  Data paper: https://www.nature.com/articles/s41597-026-07074-w (redirected to a login, not opened).
- Mendeley gnybw8p7zg, powdery mildew and late blight under irrigation configurations in organic tomato, https://data.mendeley.com/datasets/gnybw8p7zg/1, CC BY NC 3.0: the only file is a PowerPoint, `Suppl Fig 1-Microclimate Data by Treatment and Year.pptx`, so there is no table to analyse.
  The topic is exactly right, so the associated paper is worth citing if someone finds it, not verified.
- Kaggle, "Plant-Health-Data" (https://www.kaggle.com/datasets/ziya07/plant-health-data) and "Crop Health and Environmental Stress Dataset" (https://www.kaggle.com/datasets/datasetengineer/crop-health-and-environmental-stress-dataset): the pages returned only a title to the reader, and downloads need a Kaggle login.
  A search summary describes the former as simulated biosensor data, not verified.
  Treat both as synthetic until someone proves otherwise, and do not use them.
- FAWN, https://fawn.ifas.ufl.edu/data/reports/ (opened): Apopka is a listed station, no login, 15 minute to monthly intervals, with relative humidity, rainfall, soil temperature at 10 cm, solar radiation, and ET.
  The page lists neither leaf wetness nor soil moisture, and there is no outcome of any kind.
- USDA NRCS SCAN and NEON soil sensor data: soil moisture and, for some SCAN sites, salinity, with no disease or degradation outcome attached.
  Not opened, not verified, and set aside for that reason.
- Dryad and Figshare API searches for irrigation with Phytophthora, greenhouse humidity with disease, and irrigation with salinity returned no usable table.
- USDA ARS work on Phytophthora root rot of container rhododendron by Weiland and colleagues is the closest match in setting, and no public data deposit for it was found.

## Mechanism sources

These let the pitch cite established science whatever the chart shows.

1. Over-irrigation and root rot in nurseries.
   Koike, S. T., Tjosvold, S. A., and Mathews, D. M. Phytophthora Root and Crown Rots, Floriculture and Ornamental Nurseries, UC IPM Pest Management Guidelines, text updated November 2020. https://ipm.ucanr.edu/agriculture/floriculture-and-ornamental-nurseries/phytophthora-root-and-crown-rots/
   Quote: "Root and crown rots are most common under wet or over-irrigated soil conditions."
2. Wet soil and Pythium, from UF/IFAS.
   Elliott, M. L., and Harmon, P. F. Pythium Root Rot, SS-PLP-11/LH050, UF/IFAS EDIS. https://ask.ifas.ufl.edu/publication/LH050
   Quote: "Symptoms may appear at any time of the year, but they are always associated with wet soil conditions, either from excessive rainfall or from irrigation."
   This publication is about turfgrass, so cite it for the mechanism and not for nursery crops.
3. Substrate moisture and Phytophthora in container rhododendron.
   Weiland and colleagues, "Is Disease Induced by Flooding Representative of Nursery Conditions in Rhododendrons Infected with Phytophthora cinnamomi or P. plurivora?", Plant Disease. https://doi.org/10.1094/PDIS-06-21-1340-RE
   The journal page returned HTTP 403, so the full author list, year, volume, and pages are not verified.
   A search summary reports that P. cinnamomi caused more disease where substrate moisture was held above 90%, not verified against the paper.
4. Soil moisture and Phytophthora in the field, the paper behind the top pick.
   Donald et al. (2020), Forest Ecology and Management, 473, 118324. https://doi.org/10.1016/j.foreco.2020.118324
5. Humidity, leaf wetness, and foliar disease in greenhouses.
   Bartok, J. W. Jr. Reducing Humidity in the Greenhouse, UMass Extension Greenhouse Crops and Floriculture Program, November 2003, resources added 2015. https://www.umass.edu/agriculture-food-environment/greenhouse-floriculture/fact-sheets/reducing-humidity-in-greenhouse
   Quote: "This moisture promotes the germination of fungal pathogen spores such as Botrytis and powdery mildew."
   Quote: "The key to successfully suppressing diseases is to keep the plant canopy dry, especially from dusk to dawn."
6. Leaf wetness duration as the input to disease warning systems.
   Rowlandson, T., Gleason, M., Sentelhas, P., Gillespie, T., Thomas, C., and Hornbuckle, B. (2015). Reconsidering Leaf Wetness Duration Determination for Plant Disease Management. Plant Disease, 99(3), 310-319. https://doi.org/10.1094/PDIS-05-14-0529-FE
   Citation confirmed through search results, the paper itself not opened.
7. Salts in container media, from UF/IFAS.
   Hanlon, E. A., and McNeal, B. L. Soil and Container Media Electrical Conductivity Interpretations, CIR 1092/SS117, UF/IFAS EDIS, April 1993, reviewed December 2017 per a search summary. https://ask.ifas.ufl.edu/publication/SS117
   Quote: "If containerized plants are not provided sufficient drainage, then the salts from irrigation water and fertilizers can also be concentrated due to drying of the media during evapotranspiration."
   Quote: "A small amount of excess irrigation water should be provided to allow leaching from the container (usually about 20% of the water added)."
8. Leaching fraction as the grower's routine check, from UF/IFAS.
   Million, J., and Yeager, T. Monitoring Leaching Fraction for Irrigation Scheduling in Container Nurseries, ENH1268/EP529, UF/IFAS EDIS. https://ask.ifas.ufl.edu/publication/EP529

The quotes came through a page reader that returns the page's words, so check the wording against the page before any quote goes on a slide.

Sources 7 and 8 cut both ways for this project.
Too little water through the pot concentrates salts, and too much favours root rot, so the grower is steering between two failures.
That is a fair argument for a per bed record of water in, and it should be told as a balance and not as "less water is better".

## What we can and cannot claim

Can claim:

- Published field data shows more Phytophthora symptoms where the soil is wetter, and the team reproduced the direction of that result from the public file in all three sites.
- Extension sources from UC, UF/IFAS, and UMass state that wet media favours root rot, that a wet canopy favours Botrytis and powdery mildew, and that salts build up in container media without leaching.
- A per bed record of water let in and soil moisture is the input a grower would need to look for these links in their own beds.
- The roof's log is simulated, and the chart uses someone else's real field data.

Cannot claim:

- That the chart shows irrigation causing disease.
  The driver is soil moisture in a wild upland stand, recorded once, and nobody irrigated anything.
- That the result transfers to a Florida shade house, to container media, or to any crop on the page.
- That the roof prevents, reduces, or detects disease or salt build-up.
  Nothing in the simulation models either one.
- That the team discovered the link.
  Cite Donald et al. (2020) and say the team re-plotted a published result.
- Any figure for cost, yield, energy, or water saved.
- That humidity was shown to drive disease in any dataset here.
  The one real humidity and incidence dataset opened, the coffee rust set, shows no relationship.

Suggested wording for the chart caption: "Re-plot of public field data from Donald et al. 2020, CC0. Wetter quadrats show a higher share of symptomatic juniper in all three sites. Association only, not our data, not a shade house."

## Could not verify

- The unit and the survey dates of `Mean.soil.moisture` in the juniper files, because the paper was not opened.
- The Ag Data Commons landing page, which returned HTTP 403, though the Figshare API for the same record and both downloads worked.
- Corwin (2012) and Scudiero et al. (2017), cited from the dataset README only.
- How the AgriDataValue disease labels were produced.
- The method document for the Antioquia tomato dataset, and whether any paper uses it.
- The full citation of the Weiland rhododendron paper, because the journal page returned HTTP 403, and the reported 90% substrate moisture finding.
- The full author list and DOI of the coffee rust paper, and the three larger coffee rust files.
- The Scientific Data paper for Horti-M3, which redirected to a login, and whether that dataset holds disease records.
- Both Kaggle datasets, including licence, origin, and columns.
- SCAN and NEON, which were not opened.
- The `ECa_USDA_ARS_USSL_v01.csv` file, which was not downloaded.
- The publication and review dates of the EDIS documents, which the page reader did not return.
- Every quote, which came through a page reader and should be checked against the page before it is shown.
