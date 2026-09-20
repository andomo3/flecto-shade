# Project Brief - the smart louvre roof, simulated

**Event:** HackMIT 2026, Saturday 19 to Sunday 20 September, 24 hours of hacking, submitted by 11:00 on Sunday.
**Team:** three people, with Devin build agents writing the code: Abba on software and integration, Ameya on data, and Shannon, whose CAD work was cut with the printed fin and whose new lane the team settles out loud.
Names against packages live in `../CHECKLIST.md`.
**Scope source:** `plans/plan-d-louvre-roof.md`, chosen at about 16:45 on Saturday 2026-09-19 and frozen at the 17:00 standup.
This brief is a one page summary of that plan, and where the two disagree the plan wins.
After the freeze a change is a cut, never a pivot.

## One sentence

A Central Florida grower with three crops under one shade house roof gives each its own light, and lets the rain through only where the soil is dry, with a roof made of many small hingeless fins in place of one big curtain.

## What is ours, and what is not

- Not ours: the fin, which is ITKE's Flectofin, patented as EP2320015.
- Not ours: watering by the sun's energy and holding a daily light target, which Ridder, Hoogendoorn, Argus, and Priva already sell.
- Not ours: a moving roof over crops, which Cravo and Sun'Agri already sell.
- Ours: the resolution, one bed treated differently from the next.
  We found no prior proposal to put a Flectofin over crops, and those are the words.

## The 90 seconds

The full table, with what is said at each beat, is in `plans/plan-d-louvre-roof.md`, and the scripts are in `pitch/`.

1. The judge sees the roof from above, shut, three zones named, one Play button, and the word "simulated", and hears how a roof like this works today: a fine brain, and a blunt hand.
   The grower near Apopka, three crops, one sky.
2. Why the fin, said while the roof sits shut, with the credit to ITKE on the page.
   "Bed by bed takes many small parts, and every hinge is a bearing to grease. So we borrowed a part with no hinge: ITKE's Flectofin, patented, and not ours."
3. The judge presses Play, and the page plays 3 June 2023 in about forty seconds.
   The sun rises, all fins open, and three light gauges fill at the same rate.
4. The fern's fins shut at eleven, the hydrangea's at noon, and the blueberry's stay open.
   This is the moment the three zones stop behaving as one roof, and it is the moment the project wins or loses.
5. The afternoon storm, 42 mm in two hours, from the real gauge.
   The hydrangea's fins reopen because its soil is dry, the blueberry's stay shut because its soil is wet enough, and the fern's stay shut because it opted out.
   Each zone shows its reason in words.
6. The result card: each crop's light against its target, and the rain's share of each zone's water.
7. The year by month, and the close, with what the project is not.

The judge touches it once: Play.
The fallback is the recorded run, then the screen recording.

## Build list

Only what the 90 seconds requires, in order.
Each package has a specification under `plans/packages/`, or in `../CHECKLIST.md` for K2.

| Package | What | Owner | Minutes | Needs |
|---|---|---|---|---|
| G1 | The gate runner, one command that checks every fast gate | Abba | 60 | nothing |
| S1 | The 2023 sun for the Apopka area from NASA POWER, one row an hour | Ameya | 30 | nothing |
| H1 | The crops, the rain, the light, the soil bucket, the nine rules, the year's summary | Ameya | 85 | S1 |
| K2 | The roof layout, as modelled data the page draws. Optional: without it H2 draws a default grid | Shannon | | nothing |
| H2 | The page that plays 3 June 2023 in about forty seconds, from H1's output, with no new physics | Abba | 120 | H1 |
| H3 | The result card, the year by month, and `headline.json` | Abba | 75 | H2 |

In if time allows: a second view that draws the roof's fins one by one.

## Cut list

Everything considered and rejected.
Written down so it stays rejected at 3am.

- Anything physical: a rig, a sensor, an actuator, water on the table, and the printed display fin, which was cut on Saturday evening.
- A language model or a learned model anywhere in the roof's control loop.
- Fins that track the sun's position.
  They react to how much light has arrived, to rain, and to the soil.
- Wind, hail, and the structure of a full size roof.
- A closed glasshouse, where growers keep rain off the crop on purpose.
- A second city, and a typical year in place of a real one.
- The ray cast shade table, and `pvlib`, because nothing in this plan uses the sun's position.
- Any figure for cost, yield, energy, or water saved.
- Auth, settings, onboarding, a web framework, a build step, a CDN: always cut.

## The cuts, by the clock

There are no pivots left.
Each checkpoint has an hour and a cut, agreed now so nobody argues it at the venue.

| When | What must be true | If it is not |
|---|---|---|
| 21:00 Saturday | G1 and S1 are merged | S1 finishes on its own checks, and runs the gates when G1 lands |
| 23:00 Saturday, the hard checkpoint | H1 is merged with the demo day's checks passing, and the year is a bonus that blocks nothing | The page is drawn from the demo day's expected values in the specification, labelled "illustrative" |
| 01:00 Sunday, the freeze, the venue closes | H2 plays the demo day end to end | The fallback is a recorded run of H1's output, drawn as simply as possible |
| 07:00 to 09:00 Sunday | H3, the pitch figures read from `headline.json`, the screen recording | The card is cut to the demo day's two figures |
| 09:00 to 10:30 | Rehearsal, the README, the submission | |
| 11:00 | Submitted | |

## The numbers

All simulated, and all said as simulated.
The spoken figures come only from `data/processed/headline.json`, which H3 writes.
Until it exists these are the planner's values from the H1 and H3 specifications, and they are provisional.

| Figure | Value | From |
|---|---|---|
| The storm on the demo day | 42.4 mm in two hours, from the real gauge | H3's expected values |
| The rain the hydrangea zone stored that day | 34.9 mm | H3's expected values |
| The light the hydrangea did not want, from opening for the rain | 5.96 mol, said as six | H3's expected values |
| The fern shuts for light, the hydrangea shuts for light | 11:00 and 12:00 local | H3's expected values |
| The rain's share of the hydrangea zone's water over the year | about 54 percent | the plan |
| The fern's target against the hydrangea's | 8 mol a day against 12 | Purdue, with the source in H1's specification |
| One motor moves up to 50,000 square feet of roof | | the UMass fact sheet, by way of the market research file |

## What judging actually rewards

No 2026 rubric is published.
The 2025 day-of site listed creativity, technical difficulty, design, and usefulness, unweighted, judged expo style in a few minutes per team, so the watched moment decides.

| What's rewarded | How this project scores on it |
|---|---|
| A visible live result | One roof becomes three, at 0:45, and the same rain gets three answers, at 0:55 |
| A number said out loud | The rain's share of the hydrangea's water, and the six mol the rain cost it |
| A named user and an unglamorous problem | A grower, named as illustrative, and a single curtain that makes one decision for every plant under it |
| A reason to trust it | A real gauge, a real year, and rules a judge can read, with each zone saying its reason in words |
| Honesty | The fin is ITKE's, the control logic is standard, and nothing is measured, all said first and unasked |

## Tracks and challenges

The track is not yet recorded for this plan.
The 2026 tracks are Entertainment, Education, Sustainability, and Healthcare, and a project enters at most one.
The team settles it out loud before the submission form is filled in, and writes it in `RUN.md`.

Voloridge's challenge is open to this project.
It accepts any dataset, confirmed by abba on Saturday evening, so there is no curated list to stay inside, and the NASA POWER sun and the NOAA rain gauge qualify as they are.
No rule in this repo limits the choice of dataset for it, and any earlier note that said otherwise is overridden.
What the project already has to show for it, which is the planner's suggestion and the team's to decide: joined to a real year of rain, a typical year of sun made the rainy daylight hours brighter than the dry ones, by a ratio of 1.11 in a check on another Gulf Coast site's files, and with the sun taken for the same place and year as the rain, this project's file gives 0.627, rainy hours darker, as they are outside.
That finding is in S1's specification, and it came out of the noise in two public files.

Cognition's challenge, if it has one, is in reach because Devin wrote the code.
A hardware challenge is out, because nothing physical is built.

## Submission requirements

Verified again at the freeze.

- [ ] Every field of the submission form filled in.
- [ ] Exactly one track.
- [ ] The repo link, the demo video if the form asks for one, and the table cards photographed.
- [ ] Every open source library, every dataset, every source of a crop figure, and every AI tool cited, including Devin and Claude, because the rules require it.
- [ ] The prior work stated plainly: the public planning repo, and that no code was copied from it.

## Assumptions

- The rules, run on 3 June 2023 with no constant tuned, give three different answers to the same rain.
  H1's planner ran this before any code existed, and it holds.
- The sun is a satellite product for a cell about 100 km across, so a local storm can rain under a bright cell, as on 29 July 2023, and the page says the sun is modelled.
- Shading blueberries is not Florida practice and the figure is from Washington State, so the blueberry zone is the weakest of the three, and the page says where its number comes from.
- H1's evaporation formula is marked RECALLED, which means nobody has confirmed it at a source yet.
- Every constant a package marks ASSUMED is a named constant in the code and a row in the README's table of assumptions.

## Stack

Python 3.13, with `pandas==2.2.3`, `numpy==2.2.3`, and `pytest==9.0.2`, in one virtual environment with a pinned `requirements.txt`.
The page is plain HTML, CSS, and vanilla JavaScript, with no build step, no CDN, and no web fonts fetched at run time.
Everything builds and runs with no network.
A static copy of `software/page/` goes on Vercel for the live link, with no build step, see "The live link" in the plan.
Next.js and Supabase were considered on Saturday evening and set aside.
Not reopened during the event.
