---
title: Flectofin smart greenhouse roof
type: idea
status: chosen   # proposed | researching | shortlisted | rejected | chosen
owner: team   # team, or one word handle if a single person is driving it
updated: 2026-09-19
---

# Flectofin smart greenhouse roof

Chosen by the team at about 16:45 on Saturday 2026-09-19, the fourth plan of the day, replacing the [leaf design tool](flectofin-design-tool.md).
Four decisions were put to abba as questions and answered the same hour, and they are what makes this one small enough to finish.

| Decision | Answer |
|---|---|
| Physical or simulated | Simulated, with one printed fin on the table for display |
| How the roof waters | The fins over a zone open when it rains and that zone is dry, and stay shut over zones that are wet enough |
| What makes it smart | Programmed targets per zone, one crop per zone, each with a published daily light target and a water need. Deterministic rules, and no AI in the loop |
| The end user | A commercial grower with several crops under one roof |
| The setting, confirmed later the same day | A shade house, which the team calls a greenhouse in plain speech, because closed greenhouses keep rain off the crop on purpose |
| The place, chosen later the same day | The Apopka area of Central Florida, after the team dropped Houston, and checked against University of Florida sources |

## Problem

A grower with three crops under one roof gives all three the same sky.
The ferns get too much light, the blueberries not enough, and the roof is either open or shut for the whole house.
A roof made of many small fins can treat each zone differently: shade the crop that has had its light for the day, open over the one that still needs it, and let the rain through only where the soil is dry.

## The demo moment

The judge sees a greenhouse from above, three zones, three crops, and a roof of fins over them.
They press play and one real day runs in a minute: the sun crosses, the light each crop has received fills toward its target, and the fins over the low light crop close first, while the fins over the high light crop stay open.
Then it rains, from a real weather record.
The fins over the dry zone open, the fins over the wet zone stay shut, and the soil gauge of the dry zone climbs.
The day ends on a card: each crop's light against its target, and the share of each zone's water that the rain supplied.
The speaker hands over the printed fin: "this is one of those, and it has no hinge."

## What "done" means, so it can be checked

- Given a day of real solar data and three crops with sourced light targets, every zone ends the day within a stated band of its target, or the card says which zone could not and why.
- Given an hour of rain, a dry zone's fins open and a wet zone's do not, in a test.
- Every number on the screen says modelled.
- It runs with no network.

## Hardware needed

- One printed fin, for display. Nothing else.

## Software needed

- The sun for the place and the year of the rain, package S1, from NASA POWER.
- An hourly rain series from a real weather record.
- A crops table, every row with its source.
- The zone simulation: light to a daily light sum, a soil water bucket per zone, and the rules.
- One page: the greenhouse from above, the zones, the fins, the light and soil gauges, and the result card.
- The gates and package G1, unchanged.

## What carries over from the plans set aside today

The solar pipeline and its downloaded file, the gates, the build agent's rules and the handoff prompt, the honesty rules, the stack, and the method of writing packages with expected values taken from real data.
The ray cast shade table from Plan B is probably more than this needs, because a zone's light can be the sky's light times the share of its fins that are open, and the data agent is asked to say so or disagree.

## Risks, said plainly

- Four plans in six hours.
  The worst outcome is no finished project, so this one is frozen at the 17:00 standup and the next change is a cut, never a pivot.
- A real greenhouse keeps the rain out on purpose: wet leaves bring disease, and water is dosed with nutrients through the irrigation lines.
  Letting rain fall on a crop may be the idea's weakest point, and the market research is asked to find the source that says so and the setting where it is normal, a shade house or an open field.
- Moving roofs, shade screens, and climate computers that water by the sun's energy already exist, so the claim has to be what the fin adds, and that waits for the market research.
- The fin itself is patented by its inventors at Stuttgart and Freiburg, EP2320015, so the claim is never the flap.
- Opening for rain also lets light in, and the rules need a stated priority for that case.
- A roof is large and sits in the wind, which is the scale problem the team called over engineered for the bus stop. The simulation does not model wind, and says so.

## Open questions

- All four first questions are answered: the place is the Apopka area, the crops are Boston fern, hydrangea, and blueberry, the market research is done, and the setting is a shade house. See `../../plans/plan-d-louvre-roof.md`.
- A soil bucket sized for containers or for soil, and whether the hydrangea stays or a second foliage crop replaces it: the team.

## Sources

- The team's description of the pivot, pasted by abba on 2026-09-19.
- [Sector choice for the design tool](../research/flectofin-design-tool/sector-choice.md), for the patent.
- [Plan B](../../plans/plan-b-simulated.md) and [package C6](../../plans/packages/C6-data-pipeline.md), for what carries over.
