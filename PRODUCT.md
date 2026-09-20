# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The primary user of this surface is a HackMIT 2026 judge, standing at the team's table, on a 13 to 16 inch laptop screen in bright hall lighting, often viewed at an angle and over someone's shoulder.
They have roughly ninety seconds, they have already seen dozens of projects, and their job is to decide whether this one is real, honest, and different.
They interact exactly once, by pressing Play.

The product's end user, who is depicted but never present, is a commercial grower running several crops under one shade house roof.
Their job is to give each crop its own light and its own water without running three separate houses.

There is one surface, and it is the grower's console.
There is no separate judge build: the judge watches the grower's tool being driven, so the console must read correctly to a stranger in ninety seconds while still being the thing a grower would actually operate.
The surface succeeds if the judge understands the mechanism and believes the numbers.

## Product Purpose

A shade house roof made of many small hingeless fins, grouped into zones, where each zone holds its own daily light target and admits rain only when its own soil is dry.

The project is a simulation of that roof, driven by one real year of Greater Boston weather, plus the pitch and the story around it.
Success is a judge who, after one forty second run, can say what the roof did and why, and who has no reason to doubt any figure on the screen.

The demo moment is the point where three zones stop behaving as one roof: the fern has taken its light by eleven, the hydrangea by noon, the blueberry wants all of it, and then one storm gets three different answers.

## Positioning

The mechanism is resolution, not capability.

Everything else in the idea already exists and is sold today.
Roofs that open, screens that shade, and climate computers that water by the sun's energy and hold a daily light target are standard practice.
What was not found is control of light from a mechanical roof at the scale of a single bed or bench: today one gear motor moves up to 50,000 square feet of roof, and one drive motor up to 40,000 square feet of screen.

A roof of small fins can treat one bed differently from the next.
That is the whole claim, and it is the only one a neighbouring product could not truthfully copy.

Research across Flectofin, Flectofold, greenhouse, agrivoltaic and crop terms found no prior proposal to put a Flectofin over crops.
That is an absence in those searches and not proof, so the words are "we found no prior proposal", and never "first".

## Operating Context

The setting is a shade house, which the team calls a greenhouse in plain speech.
It is deliberately not a closed glasshouse, because closed greenhouses keep rain off the crop on purpose: the maker of rain admitting roofs closes them before rain to avoid crop damage and foliar disease, and rain is used today by collecting it and feeding it through drippers, never by dropping it on the crop.

The place is Greater Boston, Massachusetts, on the Boston Logan International Airport gauge, chosen on 2026-09-20 so that the site is the one the judges are standing in at HackMIT, and because a New England summer still puts sun and rain on the same days.
2023 was a wet year there, 1,242.7 mm against a 1991 to 2020 normal of 1,107, which gives the rain rule something to do.

The site was the Apopka area of Central Florida until that date, chosen because the University of Florida's Mid-Florida Research and Education Center there describes itself as located in the heart of Florida's greenhouse and nursery industry.
The three crops below, and the published sources behind their light targets and shade shares, were picked for that site and have not been rechosen for a Massachusetts one.
The southern highbush blueberry in particular is a southern cultivar; northern highbush is the Massachusetts crop.
Nothing in the simulation depends on the choice, since every crop figure is read from `data/crops.csv`, but the pitch should not claim the crop list is regional.

Three zones, one crop each, all sourced:

| Zone | Crop | Light rule | Rain |
|---|---|---|---|
| A | Boston fern, Nephrolepis | 8 mol per m2 per day | opted out, the foliage is sold on clean fronds |
| B | Hydrangea, as nursery stock | 12 mol per m2 per day | opted in |
| C | Southern highbush blueberry | 0.40 shade share | opted in |

The judging surface is a page that plays one real day, 10 June 2023, in 40.5 seconds, and ends on a result card.

## Capabilities and Constraints

- Everything is simulated. Nothing is built, nothing is sensed, and there is no physical object. The printed display fin was cut at about 19:15 on Saturday 2026-09-19 so that every remaining hour goes to the simulation, the pitch, and the story.
- The roof follows nine written deterministic rules per zone, in the priority night, then rain, then light. No language model and no learned model sits in the loop.
- The fins react to how much light has arrived, to rain, and to the soil. They never track the sun's position.
- The page is plain HTML, CSS and vanilla JavaScript. No React, no Node, no build step, no CDN, no web font fetched at run time, and no framework.
- Everything builds and runs with the network off. The page fetches no address beginning `http://`, `https://` or `//`.
- Data work is Python 3.13 with `pandas==2.2.3`, `numpy==2.2.3` and `pytest==9.0.2`, pinned, and no other dependency without a package naming it.
- Two runs of any build produce identical bytes.
- All project code is written between 11:00 Saturday 2026-09-19 and 11:00 Sunday 2026-09-20. Nothing is copied from the team's planning repository.
- Every expected value was computed from the real data by a planner before any code existed. A value that does not match is reported, never edited to make a test pass.
- The mobile layout is dropped on purpose, because the judging scene is a laptop.

Open decisions, recorded rather than invented:

- Whether the soil bucket is sized for containers or for ground soil.
- Whether the hydrangea stays as zone B's crop.

## Brand Commitments

- The fin is not the team's. It is the Flectofin, by ITKE at the University of Stuttgart, patented as EP2320015, and the page credits it.
- The control logic, watering by the sun's energy and holding a daily light target, is standard practice in greenhouse computers, and nothing claims otherwise.
- Nothing simulated is ever called measured. Every figure on every screen and in every file says simulated or modelled. The single exception is the rain source line, where "measured" is true of the gauge.
- These words are never written or displayed: "first", "measured" outside that one line, "maintenance free", "weatherproof", and any figure for cost, yield, energy, or water saved.
- Writing style is one sentence per line in Markdown, plain dashes, never an em dash.
- Standing visual preference, chosen by the user in the direction round of 2026-09-19 over the assigned direction and two alternates: the category standard for an operator console, played straight, without irony and without smuggled quirk. The craft bar the user named is Linear, Vercel, and the Stripe Dashboard, and it is their finish level that binds, not their look: a strict spacing scale, restrained colour, real empty and loading states, keyboard reachable, nothing decorative.

## Evidence on Hand

Real, downloaded, and checksummed:

- `data/raw/nasa-power/power-hourly-boston-logan-2023.csv`, NASA POWER hourly for the Boston Logan International Airport gauge, 2023. A satellite product for a cell about 100 km across. Always labelled modelled.
- `data/raw/isd-rain/72509014739-2023.csv`, NOAA Integrated Surface Database hourly for the same gauge and year. A real instrument, and the only measured thing in the project.
- `data/processed/year-boston-2023.csv`, 8,760 rows, committed, built by package S1 and checked against values recomputed from the raw file on 2026-09-20.

Every crop figure has a published source: Purdue HO-238-W for the fern's and hydrangea's daily light sums, a Washington State University fact sheet for the blueberry's shade share, and FAO-56 Table 12 for the crop coefficients, with 1.00 assumed where the table has no row.

Deliberately absent, and never to be fabricated:

- No physical artifact, prototype, rig, or sensor reading.
- No customers, testimonials, pilots, trials, or partnerships.
- No cost, yield, energy, or water saved figure, in any form.
- No claim of novelty stronger than "we found no prior proposal".

## Product Principles

1. **The honest line is the strongest line.** Naming exactly what is modelled and what is measured is the differentiator against a table of projects that overclaim, not a caveat that weakens the pitch.
2. **Resolution is the claim.** Every design decision should make it obvious that zones behave independently. A screen where three zones look alike has failed regardless of its polish.
3. **Nobody reads data as data.** The weather exists to be the input to the rules. What is shown is what the rules did.
4. **Every number traces to a file.** No figure is typed by hand anywhere, in a script, a card, a README, or a spoken line.
5. **One interaction.** The judge presses Play. Anything that needs a second explained gesture is a thing the demo cannot afford.

## Accessibility & Inclusion

Driven by the judging scene, a laptop in a bright hall read at an angle, not by a formal standard.

- Nothing on the page smaller than 18 px.
- Text contrast at least 4.5 to 1 against every sky colour the strip passes through, including the bright midday states.
- Three colours plus neutrals, with green, orange and red reserved for status.
- System font stack only, since no web font may be fetched at run time.
- Every zone's state is given in words as well as colour, so the three answers to the storm do not depend on colour discrimination.
