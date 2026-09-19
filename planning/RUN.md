# Run

The plan's status in one place, and the log of decisions made during the event.
The live board, with who has claimed what and on which branch, is `../CHECKLIST.md`, and where this file and the board disagree the board wins.
Statuses are real, stubbed, recorded, planned, or cut, and a feature only ever moves down that ladder during the event.

Phase: building, Plan D, the simulated smart louvre roof, chosen at about 16:45 on Saturday 2026-09-19 and frozen at the 17:00 standup
Clock: hacking 11:00 Saturday 2026-09-19 to submission 11:00 Sunday 2026-09-20, venue closed 01:00 to 07:00
Freeze: 01:00 Sunday, the venue closure, nothing new after it
Demo path: the roof from above, shut, three zones named, the word "simulated", the fin is explained and credited to ITKE, the judge presses Play, the page plays 3 June 2023 in about forty seconds, the fern's fins shut at eleven and the hydrangea's at noon and the blueberry's stay open, the afternoon storm gets three different answers with each zone's reason in words, and the day ends on the result card and the year by month
The number: the rain's share of the hydrangea zone's water over the year, about 54 percent, and the six mol of light that opening for the storm cost it, both simulated, both provisional until `data/processed/headline.json` exists

## Features

| Feature | Status | Owner | Note |
|---|---|---|---|
| G1, the gate runner | planned | Abba | 60 minutes, due merged by 21:00 Saturday, not started at 19:00 |
| S1, the 2023 sun for the Apopka area | planned | Ameya | on `pkg/S1` at 18:34, waiting for review and merge |
| K1, a printed display fin | cut | Shannon | cut at about 19:15 Saturday, nothing physical is built, and the branch `pkg/K1` is not merged |
| H1, the crops, the rain, the light, the soil, the nine rules, the year | planned | Ameya | needs S1 merged, the hard checkpoint is 23:00 Saturday |
| K2, the roof layout | planned | Shannon | optional, without it H2 draws a default grid |
| H2, the page that plays the demo day | planned | Abba | needs H1, must play end to end by the 01:00 freeze |
| H3, the result card, the year by month, `headline.json` | planned | Abba | needs H2, 07:00 to 09:00 Sunday |
| The pitch, the polish, the README, the table | planned | Abba | the story can start now, the figures wait for H3 |
| If time allows: a second view that draws the fins one by one | planned | Abba | the first thing cut |
| If time allows: the printed fin's dimensions beside it | cut | Abba | cut with the fin |
| Fallback: a recorded run of H1's output, drawn simply | planned | Abba | only if H2 does not play by the freeze |

## Decisions

Logged during the event with the clock time, one line each, what was decided and why.

- 16:45 Saturday: the project is a simulated smart louvre roof of Flectofin fins for a commercial grower, because a roof that gives each crop its own light and rain has a user the team can picture.
- 16:45 Saturday: it is simulated, it waters by opening over dry zones when it rains, and it follows programmed targets per zone with no AI in the loop, because those were the smallest honest answers to the four questions put to abba.
- 17:00 Saturday: the plan is frozen, and any later change is a cut and never a pivot, because the worst outcome is no finished project.
- Saturday evening: the setting is a shade house, which the team calls a greenhouse in plain speech, because closed greenhouses keep rain off the crop on purpose and a shade house does not.
- Saturday evening: the sun comes from NASA POWER for the same place and year as the rain, because a typical year joined to a real year's rain made rainy hours brighter than dry ones.
- Saturday evening: the place is the Apopka area of Central Florida, because a shade house region with summer afternoon storms puts sun and rain on the same days.
- 19:00 Saturday: a build agent built the wrong packages on the branch `devin/1789856444-shared-core`, because stale planning files read as live rules. The branch is never merged, and the root `AGENTS.md` now says it is the only rules file.
- 19:15 Saturday: every file under `planning/` is rewritten for this plan, because a build agent reads whatever it finds.
- 19:15 Saturday: nothing physical is built, and the printed display fin, package K1, is cut, because every hour goes to the simulation, the pitch, and the story.
- About 19:20 Saturday: the page stays plain HTML, CSS, and vanilla JavaScript, and a static copy goes on Vercel for the live link. Next.js and Supabase were considered and set aside, because nothing is stored, nobody logs in, and the demo must run with no network.
- About 19:30 Saturday: every gate test file has an owning package, H3 writes a copy of `headline.json` into the served page folder, and the page plays a dark hour in half a second and a daylight hour in 2.4 seconds, so the screen keeps to the spoken script.

Open, for the team to settle out loud:

- Which track and which challenges the project enters.
- What Shannon works on now that the CAD packages are cut or optional.
- A soil bucket sized for containers or for soil, from H1.
- Whether the hydrangea stays, from H1.

## Rules used

Which rule from the `hackathon-build` skill fired, and what it did.

- The demo first rule: the simulation comes before the page, so there is always something to show.
- The scope creep brake: the per fin view and the fin's dimensions are "if time allows", and are cut first.
