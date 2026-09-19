---
title: What already exists for moving greenhouse roofs, shade, and smart irrigation, and what a Flectofin roof would add
type: research
status: done
owner: abba
updated: 2026-09-19
idea: flectofin-greenhouse-roof
---

# What already exists for moving greenhouse roofs, shade, and smart irrigation, and what a Flectofin roof would add

## Answer

Almost everything in the idea already exists except its resolution.
Roofs that open, screens that shade, and climate computers that water by the sun's energy and hold a daily light target are all sold today, and the control logic the team planned is standard practice.
What nobody was found doing is controlling light from a mechanical roof at the scale of a bed or a bench: today one motor moves thousands of square feet.
Letting rain fall on the crop is the opposite of what closed greenhouses do on purpose, so the idea fits a shade house or an open field roof, and does not fit a closed glasshouse.

Found by a research agent that opened every source on 2026-09-19.
Anything it saw only in a search snippet is marked unverified and is not said out loud.

## Findings

### The maker of rain admitting roofs closes them before it rains

- Cravo's Luis Gaxiola: the weather station "helps to anticipate closing the greenhouse completely before the rain starts to fall thus avoiding any damage to the crop", and "Drying off the leaves will also help reduce the risk of foliar disease."
- Cravo counts as a milestone a roof that could "shed rain to a gutter system", and treats its older roofs, which "were not capable of keeping rain off the plants", as a defect.
- No maker was found that markets rain as irrigation.

### Rain is used today by collecting it, never by dropping it on the crop

- A Dutch greenhouse builder: "rainwater is the preferred irrigation source of all: it is naturally soft, low in salts", with 0.1 to 0.5 millimoles of sodium per litre against 3 to 10 for well water, and it is fed "precisely through the dripper".
- Grey mould, Botrytis: "infection of the host is dependent on a film of moisture for 8 to 12 hours", and spores spread by "splashing water".

### The control logic is standard practice

- Ridder: irrigation intervals "can often be adjusted automatically based on the radiation sum", which it also calls "only a rough indication" of water need.
- Hoogendoorn: "You can initiate irrigation cycles per valve based on time, radiation, slab weight, water content and drainage."
- Argus sells a "Daily Light Integral Control Program" that "begins with a target DLI" and carries surplus light forward for up to 7 days, driving supplementary lights.
- Priva: from its light sensor, "your process computer calculates how you can use shading curtains, CO2 and the growing light."
- A maker's own words for a daily light target driving a shade screen were not found, so that exact claim is unverified.

### Existing moving roofs and screens control large areas

- Retractable roof: "One gear motor will handle up to 50,000 sq ft of roof."
- Screens: "one drive motor can handle up to 40,000 sq ft", at "$2.00-2.50/sq ft installed".
- Van Wingerden's open roof: "Each zone has independent windward and leeward operation", with the zone's size not stated.

### Their maintenance is a documented chore, with no cost figure found

- An insurer's guide: "Roof and sidewall vents get a lot of use, so they need continuous attention. Lubricate bearings, rack and pinions, and vent arm hinge points."
- A university fact sheet on screens: "Regular maintenance is needed to keep proper tension in the cable system", "Pulleys and gear motors should be lubricated once or twice a year", and "Screen materials tend to wear on rub points."
- The same source on retractable roofs: "greater infiltration through gaps and cracks in the seals."

### Smart glass exists and barely beats screens

- Wageningen: electrochromic glass and similar covers "already exist in the market", and their yield gains "are comparable to those obtained with existing technology, such as shading mobile screens."
- A 2025 review of smart covers mentions no kinetic or louvred roof and no zoning in space.
- Shading coatings are sprayed over a whole roof, "manually, by machine or by helicopter", for a season.

### Dynamic agrivoltaics is the closest thing to the idea

- Sun'Agri: "The shutters can be moved by + or - 90 degrees", "shade can vary by 10 to 90%", panels "more than 4.50 metres" high, driven by "an agronomic growth model", with irrigation "on average, 30% less".
- Insolight with Agroscope: "an algorithm controlling the photovoltaic modules, irrigation and nutrient supply as a function of plant species, developmental stage and solar radiation."
- Neither describes admitting rain by soil moisture.

### No Flectofin in agriculture was found

Searches across Flectofin, Flectofold, greenhouse, agrivoltaic, and crops returned no such proposal.
That is an absence in these searches and not proof, so the words are "we found no prior proposal", never "first".
The fin is ITKE's, patented as EP2320015, see [the sector research](../flectofin-design-tool/sector-choice.md).

## What exists, against the idea

| Practice | Maker | Controls | Smallest area it controls alone | How it moves | Overlap |
|---|---|---|---|---|---|
| Retractable roof | Cravo | Light, ventilation, keeping rain out | A section, up to 50,000 sq ft a motor | A gear motor pulls a film curtain | Opening the roof, zoning by section |
| Open roof | Van Wingerden | Ventilation | A "zone", size not stated | Hinged peaks on a drive | Opening the roof |
| Shade and energy screens | Svensson and others | Light, heat | Up to 40,000 sq ft a motor | Cable and drum, push pull, or chain | Managing light |
| Climate computers | Priva, Hoogendoorn, Ridder, Argus | Irrigation per valve by radiation, daily light targets | One valve | Software | All of the control logic |
| Coatings | ReduSystems | Shade, diffusion | The whole roof, for a season | Sprayed on | Shade |
| Smart glass | Various | Transmission | A pane in principle, no zoned use found | Electrical | Zoning light |
| Dynamic agrivoltaics | Sun'Agri, Insolight | Shade, and through it irrigation | Not stated | Shutters tilting 90 degrees either way | The closest overall |

## What is not already done

- Light controlled by a mechanical roof at the scale of a bed or a bench, where today one motor covers thousands of square feet.
- One element that shades, opens for air, and admits rain.
- A roof element with no hinge, bearing, or lubricant, which removes maintenance tasks the sources document. The saving is not quantified, so the words are "removes documented maintenance tasks" and never a figure.
- Rain admitted by zone according to soil moisture. It is new partly because the industry deliberately does the opposite.
- Failing open or failing closed, and a low part count, are plausible and unsupported by any source.

## The objections, and the honest answers

1. **Wet leaves bring disease.**
   Concede it for tomato and cucumber in a glasshouse.
   Rain admission is for rain tolerant crops grown in soil or containers, in daytime drying conditions, and each crop opts in.
2. **Irrigation already meters water, and rain is already harvested.**
   Agree. Rain admission saves pumping and storage only where crops grow in soil, and it is a secondary feature.
3. **An open roof loses heat, and carbon dioxide where it is dosed.**
   Open only when venting is wanted anyway, and aim at unheated structures. The carbon dioxide point was not sourced.
4. **Wind, hail, and snow on thin fins.**
   Unproven. The simulation does not model wind, and closing and stowing in a storm is future work.
5. **Cost per square metre against screens at about two dollars a square foot.**
   No cost claim is made. One actuator per row would keep the actuator count near that of screens, which is a hypothesis.
6. **"Your logic is already in Priva."**
   Yes. The contribution is the resolution of the actuator, not the algorithm.

## Where it fits

Ranked by how well each can be defended.

1. **A shade house or an open field roof.**
   A hingeless louvre roof over berries, nursery stock, or field crops, in the manner of dynamic agrivoltaics, giving light by the bed and optional rain admission.
   Rain on the crop is normal there, and Sun'Agri shows growers pay for a moving roof over a field.
2. **Light by zone for mixed crops under one roof.**
   Research stations, nurseries, and urban farms, with rain admission dropped or made minor.
3. **A retrofit shade layer in a closed glasshouse.**
   The weakest, because it competes head on with cheap, proven screens.

## Implications for the build

- The setting changes from "greenhouse" to a shade house or open field roof, and the end user becomes a grower of soil or container crops under shade, such as a berry or nursery grower.
- Light by the bed is the headline, because it is the one thing not found elsewhere, and rain admission is the second feature, per crop and opt in.
- The pitch credits the existing control logic out loud, because a judge who knows horticulture will know it.
- The crops and the location are chosen for that setting, and the data agent was told so while it was still working.

## What the team never says

- "No one does daily light or radiation based control."
- "Greenhouses waste rain", or "rain replaces irrigation".
- Any figure for cost, energy, yield, or water saved.
- "Maintenance free" or "weatherproof".
- "We invented the fin."
- "It works", of a simulation.
- "First ever".

## Sources

- [Cravo at a berry growers' event, Hortidaily](https://www.hortidaily.com/article/6040819/berry-growers-learn-about-improved-retractable-roof-technology/) and [Cravo's thirty years, MMJ Daily](https://www.mmjdaily.com/article/9233351/cravo-retractable-peaked-roof-greenhouses-turn-30-years-old/).
- [Ridder ProDrain leaflet](https://portal.ridder.com/media/files/rgs/Leaflet%20Ridder%20ProDrain%20EN.pdf), [Hoogendoorn IIVO](https://hoogendoorn.com/en/projects/smart-greenhouse-control-with-iivo), [Argus daily light integral data sheet](https://arguscontrols.com/uploads/documents/DLI-Data-Sheet-Rev.-Sept-2015.pdf), [Priva PAR sensor](https://www.priva.com/horticulture/solutions/par-sensor).
- [UMass, retractable roof greenhouses and shadehouses](https://www.umass.edu/agriculture-food-environment/greenhouse-floriculture/fact-sheets/retractable-roof-greenhouses-shadehouses), [UMass, selecting a screen system](https://www.umass.edu/agriculture-food-environment/greenhouse-floriculture/fact-sheets/selecting-energyshade-screen-system), [UMass, Botrytis blight](https://www.umass.edu/agriculture-food-environment/greenhouse-floriculture/fact-sheets/botrytis-blight-of-greenhouse-crops).
- [Van Wingerden products](https://van-wingerden.com/products), [Hortica maintenance recommendations](https://www.hortica.com/learning-center/loss-control/greenhouse-maintenance-recommendations).
- [Wageningen, smart greenhouse covers](https://research.wur.nl/en/publications/smart-greenhouse-covers-a-look-into-the-future/), [2025 review of smart covers](https://pmc.ncbi.nlm.nih.gov/articles/PMC12537742/), [ReduSol](https://www.redusystems.com/en/products/ReduSol).
- [Sun'Agri, Irrigation Europe](https://irrigationeurope.eu/en/dynamic-agrivoltaism-combining-crop-production-and-the-generation-of-energy/), [Sun'Agri](https://sunagri.fr/en/sunagris-agrivoltaic-technology-recognised-as-a-solution-for-adapting-to-climate-change/), [Insolight with Agroscope](https://www.agroscope.admin.ch/en/insolagrin-experimental-agrivoltaic-plant).
- [Dutch Greenhouses, rainwater collection](https://dutchgreenhouses.com/en/greenhouse-construction/rainwater-collection).
- [Lienhard et al. 2011, Flectofin](https://iopscience.iop.org/article/10.1088/1748-3182/6/4/045001), abstract.
