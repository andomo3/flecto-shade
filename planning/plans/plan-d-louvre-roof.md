# Plan D: the smart louvre roof, simulated

The current plan, chosen at about 16:45 on Saturday 2026-09-19 and frozen at the 17:00 standup.
It replaces Plan A, Plan B, and the design tool, which are kept only as the record.
After the freeze a change is a cut, never a pivot.

The idea is in `../docs/ideas/flectofin-greenhouse-roof.md`, and the market research that shaped it is in `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md`.

## The one sentence

A grower with three crops under one shade roof gives each its own light, and lets the rain through only where the soil is dry, with a roof made of many small hingeless fins in place of one big curtain.

## What is ours, and what is not

- Not ours: the fin, which is ITKE's and patented, EP2320015.
- Not ours: watering by the sun's energy and holding a daily light target, which Ridder, Hoogendoorn, Argus, and Priva already sell.
- Not ours: a moving roof over crops, which Cravo and Sun'Agri already sell.
- Ours: the resolution. Today one motor moves up to 50,000 square feet of roof, and a roof of fins can treat one bed differently from the next.
  We found no prior proposal to put a Flectofin over crops, and those are the words, never "first".

## The MVP

Simulated, with one printed fin on the table.

In:

- Three zones, three crops, each with a light rule from a source: lettuce and hydrangea by daily light sum, blueberry by shade share.
- A roof of fins per zone that opens and shuts by nine written rules, in the priority night, then rain, then light.
- Real hourly rain from the Houston Hobby gauge in 2023, and the sun for the same place and the same year, so that rainy hours are dark hours.
- A soil water bucket per zone, with the grower's own irrigation as the backstop, so the question becomes how much of the water the rain supplied.
- One page that plays one day in about a minute, and ends on a result card.
- The year's summary, by zone and by month.

In if time allows, in this order: a second view that draws the roof's fins one by one, and the printed fin's dimensions shown beside it.

Out: any physical rig, any sensor, water, AI in the loop, wind and hail, a closed glasshouse, a second city, the ray cast shade table, cost and yield figures, and everything in the plans set aside.

## The packages, in order

| Order | ID | What | Spec | Minutes |
|---|---|---|---|---|
| 1 | G1 | The gate runner | `packages/G1-gate-runner.md` | 60 |
| 2 | S1 | The sun for Houston in 2023, from NASA POWER, one row an hour | `packages/S1-solar-2023.md` | 30 |
| 3 | H1 | The crops, the rain, the light, the soil, the rules, and the year's summary | `packages/H1-zones-light-rain-soil.md` | 85 |
| 4 | H2 | The page: the roof from above, three zones, the fins, a light gauge and a soil gauge per zone, Play, and one day in a minute, read from H1's output with no new physics | To be written once H1's columns are fixed by a first run | about 90 |
| 5 | H3 | The result card and `headline.json`: each crop's light against its target, the rain's share of each zone's water, the year by month | To be written with H2 | about 45 |

G1 and S1 can start now.
Package C6, the PVGIS typical year, is set aside: joined to the 2023 rain it made rainy hours brighter than dry ones, which S1's file explains and fixes.
`pvlib` is no longer needed, because nothing in this plan uses the sun's position.
The day the page plays is 5 June 2023, sun until early afternoon and then 17 mm of rain, and H1's planner ran the rules on it: the story happens, with no constant tuned.

## The demo, ninety seconds

| Time | Say | The screen |
|---|---|---|
| 0:00 | The grower, three crops, one sky | The roof from above, shut, three zones named, one Play button, the words "simulated" |
| 0:20 | "This is one of the fins. It has no hinge. Bend it." | Unchanged. The judge holds the printed fin |
| 0:30 | "Would you press play?" | The sun rises, all fins open, three light gauges fill at the same rate |
| 0:45 | "The hydrangea has had its light for the day. An hour later, so has the lettuce. The blueberries want all of it." | Zone B's fins shut at noon, zone A's an hour later, and zone C stays open. This is the moment the three zones stop behaving as one roof |
| 0:55 | "Then it rains. This is the real afternoon of 5 June 2023 in Houston, and the sky has gone dark with it." | Rain over all three, 17 mm in four hours. The hydrangea's fins reopen, because its soil is dry, and its soil gauge climbs. The lettuce stays shut, because it opted out of rain. The last hour of rain is refused by every zone, because there is no daylight left to dry the leaves |
| 1:10 | "And the day ends. Opening for the rain cost the hydrangea three mol of light it did not want. That is the trade, and it is on the card." | The result card: light against target per crop, and the rain's share of each zone's water |
| 1:20 | The close, and what it is not | The year by month, with August at zero |

The judge touches it twice, Play and the fin.
The fallback is the recorded run, then the screen recording.

## The presentation

- The hero is a grower, named as illustrative, with three crops and one roof.
- The villain is the single curtain: one motor, one decision, for every plant under it.
- The three specifics: 50,000 square feet a motor, from the UMass fact sheet; the lettuce's 17 mol a day, from Cornell; and the rain's share in a drought year, from our own run.
- The honesty comes first and unasked: the fin is ITKE's, the control logic is standard, growers keep rain off glasshouse crops on purpose, and nothing here is measured.
- The list of words the team never says is in the market research file.
- The scripts, the question bank, the cards, and the submission are rewritten from these points once H1 has produced real numbers, and the old ones under `../pitch/` are the record of the bus stop.

## The gates

`gates.md` is written for this plan: fourteen fast gates after every package, four milestones walked by a person, and the demo gate beat by beat from the table above.

## Risks

- Four plans in six hours, and nothing built at 17:00. The order above gets a running simulation before a page, so there is always something to show.
- The sun is a satellite product for a cell about 100 km across, so a local storm can rain under a bright cell, as on 25 July 2023, and the page says the sun is modelled.
- 2023 was a drought year in Houston with no rain in August, so the rain's share is small. That is the honest finding and not a bug.
- A horticulture expert at the table. The answers are written in the market research, and the first of them is to concede.
- Wind, hail, and the cost of many actuators are not modelled and not claimed.
