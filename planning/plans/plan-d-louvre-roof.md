# Plan D: the smart louvre roof, simulated

The current plan, chosen at about 16:45 on Saturday 2026-09-19 and frozen at the 17:00 standup.
It replaces Plan A, Plan B, and the design tool, which are kept only as the record.
After the freeze a change is a cut, never a pivot.

The idea is in `../docs/ideas/flectofin-greenhouse-roof.md`, and the market research that shaped it is in `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md`.

## The one sentence

A Central Florida grower with three crops under one shade house roof gives each its own light, and lets the rain through only where the soil is dry, with a roof made of many small hingeless fins in place of one big curtain.

## What is ours, and what is not

- Not ours: the fin, which is ITKE's and patented, EP2320015.
- Not ours: watering by the sun's energy and holding a daily light target, which Ridder, Hoogendoorn, Argus, and Priva already sell.
- Not ours: a moving roof over crops, which Cravo and Sun'Agri already sell.
- Ours: the resolution. Today one motor moves up to 50,000 square feet of roof, and a roof of fins can treat one bed differently from the next.
  We found no prior proposal to put a Flectofin over crops, and those are the words, never "first".

## The MVP

Simulated, all of it.
Nothing physical is built, and there is no printed fin: the fin was cut at about 19:15 on Saturday, as a cut and not a pivot, so that every hour goes to the simulation, the pitch, and the story.

In:

- Three zones, three crops, each with a light rule from a source: Boston fern and hydrangea by daily light sum, blueberry by shade share.
- The place is the Apopka area of Central Florida, which the University of Florida calls "the heart of Florida's greenhouse and nursery industry", in a shade house, which the team calls a greenhouse in plain speech.
- A roof of fins per zone that opens and shuts by nine written rules, in the priority night, then rain, then light.
- Real hourly rain from the Orlando Executive Airport gauge in 2023, and the sun for the same place and the same year, so that rainy hours are darker hours.
- A soil water bucket per zone, with the grower's own irrigation as the backstop, so the question becomes how much of the water the rain supplied.
- One page that plays one day in about a minute, and ends on a result card.
- The year's summary, by zone and by month.

In if time allows: a second view that draws the roof's fins one by one.

Out: any physical rig, a printed fin, any sensor, water, AI in the loop, wind and hail, a closed glasshouse, a second city, the ray cast shade table, cost and yield figures, and everything in the plans set aside.

## The packages, in order

| Order | ID | What | Spec | Minutes |
|---|---|---|---|---|
| 1 | G1 | The gate runner | `packages/G1-gate-runner.md` | 60 |
| 2 | S1 | The sun for the Apopka area in 2023, from NASA POWER, one row an hour | `packages/S1-solar-2023.md` | 30 |
| 3 | H1 | The crops, the rain, the light, the soil, the rules, and the year's summary | `packages/H1-zones-light-rain-soil.md` | 85 |
| 4 | H2 | The page: the roof from above, three zones, the fins, a light gauge and a soil gauge per zone, Play, and one day in a minute, read from H1's output with no new physics | `packages/H2-page.md` | 120 |
| 5 | H3 | The result card and `headline.json`: each crop's light against its target, the rain's share of each zone's water, the year by month | `packages/H3-result-card.md` | 75 |

G1 and S1 can start now.
Package C6, the PVGIS typical year, is set aside: joined to a real year's rain it made rainy hours brighter than dry ones, which S1's file explains and fixes.
`pvlib` is no longer needed, because nothing in this plan uses the sun's position.
The day the page plays is 3 June 2023, sun until mid afternoon and then 42 mm of rain in two hours, and H1's planner ran the rules on it: the story happens, with no constant tuned, and three zones give three different answers to the same rain.

## The demo, ninety seconds

| Time | Say | The screen |
|---|---|---|
| 0:00 | The grower near Apopka, three crops, one sky | The roof from above, shut, three zones named, one Play button, the word "simulated" |
| 0:20 | "Each of those is a fin with no hinge, which bends to open and shut. The fin is not ours. It is ITKE's Flectofin, and it is patented." | Unchanged, the roof shut, with the credit to ITKE on the page |
| 0:30 | "Would you press play? This is 3 June 2023." | The sun rises, all fins open, three light gauges fill at the same rate |
| 0:45 | "The fern has had its light by eleven. The hydrangea by noon. The blueberries want all of it." | Zone A's fins shut, then zone B's an hour later, and zone C stays open. This is the moment the three zones stop behaving as one roof |
| 0:55 | "Then the afternoon storm. Forty two millimetres in two hours, from the real gauge." | Rain over all three. The hydrangea's fins reopen, because its soil is dry, and its soil gauge climbs to full. The blueberry's stay shut, because its soil is wet enough. The fern's stay shut, because it opted out. Each zone shows its reason in words |
| 1:10 | "Same rain, three answers. And opening for it cost the hydrangea six mol of light it did not want. That is the trade, and it is on the card." | The result card: light against target per crop, and the rain's share of each zone's water |
| 1:20 | The close, and what it is not | The year by month: the wet season carrying the hydrangea, the dry season on the grower's own water |

The judge touches it once, Play.
The fallback is the recorded run, then the screen recording.

## The presentation

- The hero is a grower, named as illustrative, with three crops and one roof.
- The villain is the single curtain: one motor, one decision, for every plant under it.
- The three specifics: 50,000 square feet a motor, from the UMass fact sheet; the fern's 8 mol a day against the hydrangea's 12, from Purdue; and the rain's share of the hydrangea zone's water, about 54 percent, from our own run.
- The honesty comes first and unasked: the fin is ITKE's, the control logic is standard, growers keep rain off glasshouse crops on purpose, and nothing here is measured.
- The list of words the team never says is in the market research file.
- The scripts, the question bank, the cards, and the submission under `../pitch/` were rewritten from these points on Saturday evening, following `pitch-plan-d.md`, and their simulation figures are checked against `headline.json` once H3 has produced it.

## The live link

Decided at about 19:20 on Saturday: the page stays plain HTML, CSS, and vanilla JavaScript, exactly as H2 specifies, and a static copy of `software/page/` is put on Vercel.
Next.js and Supabase were considered and set aside, because nothing in this project is stored, nobody logs in, and a database would put a network call into a demo that must run with no network.

- The laptop copy, served by `python -m http.server`, is the demo. The Vercel address is the link in the README and the submission, and the backup at the table.
- Vercel serves the folder as it is, with no build step and no framework, so H2, H3, and gate F3 do not change.
- Abba puts it up by hand, once H2 plays the day, before the 01:00 freeze, and again after H3.
- No token, no project setting, and no `.vercel/` folder is committed.
- It depends on one open question in H3: the page has to reach `headline.json` from inside `software/page/`, because that folder is all that is served, on Vercel and on the laptop alike.

## The gates

`gates.md` is written for this plan: fourteen fast gates after every package, four milestones walked by a person, and the demo gate beat by beat from the table above.

## Risks

- Four plans in six hours, and nothing built at 17:00. The order above gets a running simulation before a page, so there is always something to show.
- The sun is a satellite product for a cell about 100 km across, so a local storm can rain under a bright cell, as on 29 July 2023, and the page says the sun is modelled.
- Shading blueberries is not Florida practice, and the figure is from Washington State, so the blueberry zone is the weakest of the three and the page says where its number comes from.
- A horticulture expert at the table. The answers are written in the market research, and the first of them is to concede.
- Wind, hail, and the cost of many actuators are not modelled and not claimed.
