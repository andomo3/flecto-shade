# Preparing the pitch, the screen, the README, and the table, for Plan D

A guide for abba, written on 2026-09-19 before the build began, because the pitch cannot be written until the simulation has produced its figures.
It says what to write, when, from which part of the playbook, and what may never be said.
The playbook is `../playbook.md`, which is `planning/playbook.md` in the event repo, and each `hackathon-*` skill under `.claude/skills/` is built from one part of it.

## When each thing is written

| When | What | With |
|---|---|---|
| While H1 builds | The story and the one sentence, which need no figures | The `hackathon-pitch` skill, and the playbook's storytelling section |
| After H3 is merged | The three scripts, with figures read from `pitch/figures.md`, never typed | The same skill. Word targets: 30 seconds is 75 to 90 words, 60 seconds is 150 to 180, 3 minutes is 450 to 540 |
| After H2 plays the day | The polish pass on the page | The `hackathon-ui-polish` skill, and the playbook's UI fast track and UI checklist |
| Sunday 07:00 to 09:00 | The cards, the question bank, the screen recording | The `hackathon-pitch` and `hackathon-testing` skills |
| Sunday 09:00 to 10:30 | The README and the submission | The `hackathon-readme` skill, and the playbook's README template |
| Before every judge | The table routine | `../pitch/checklist.md` still applies, with "leaf" read as "page" |

The skill's word counter, `pitch_timer.py`, was written before the event and was left behind on purpose.
A word count is one line in any editor, or the build agent can write a new counter in five minutes, and that is allowed because the event has started.

## The story, as far as it can be written now

- **The hero.** A grower near Apopka, Florida, with three crops under one shade house roof, introduced as illustrative with "picture", because nobody was interviewed.
- **The villain.** The single curtain: one motor, one decision, for every plant under it. Today one motor moves up to 50,000 square feet of roof.
- **The turn.** A roof made of many small fins can give each bed its own answer.
- **The demo as a scene.** 3 June 2023: the fern has its light by eleven, the hydrangea by noon, the blueberries want all of it, then the afternoon storm, and three zones give three answers to the same rain, each for its own reason.
- **The three specifics.** 50,000 square feet a motor, from the UMass fact sheet. The fern's 8 mol a day against the hydrangea's 12, from Purdue. The rain's share of the hydrangea zone's water, from `headline.json`.
- **The close.** Return to the grower. The closing line is abba's to write, in abba's own voice, and the `writing-voice` skill is not in this repo.

The pitch under `../pitch/` follows the playbook's method: the story spine, the emotional arc table, the question bank's formula of answer, evidence, and scope, the four cards, and the recovery lines.
Its simulation figures are provisional until H3 has produced `headline.json`.
Copy the shapes, never the content.

## Honesty first, and unasked

These are said before a judge can ask, because each is a question an expert would open with.

1. The fin is not ours. It is the Flectofin, by ITKE at the University of Stuttgart, patented as EP2320015. Ours is the roof logic and the simulation.
2. The control logic is standard. Greenhouse computers already water by the sun's energy and hold a daily light target. Ours is the resolution: a bed, not a bay.
3. Growers keep rain off glasshouse crops on purpose. That is why this is a shade house, why each crop opts in, only in daylight, only with time to dry, and why the fern opts out.
4. Nothing here is measured, except the rain, which is one real gauge. The sun is a satellite product. The soil and crop numbers are textbook coefficients with assumed bucket sizes.
5. Shading blueberries is not Florida practice. That figure is from Washington State.
6. Nothing physical was built. There is no prototype and no printed fin, and nothing is claimed about how the fin itself behaves.

## The words the team never says

"First". "Measured", of anything but the rain gauge. "Maintenance free". "Weatherproof". "It works", of a simulation.
Any figure for cost, yield, energy, or water saved.
"No one does light or radiation based control". "Greenhouses waste rain". "We invented the fin".
In their place: "we found no prior proposal in our searches", "simulated", and "removes documented maintenance tasks".
The sources for all of this are in `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md`.

## The questions to have answers for

Written in the playbook's formula: the answer in ten seconds, the evidence in twenty, the honest scope in ten.

- "Growers keep rain off crops, so why let it in?" Concede it, then the opt in rules.
- "Your logic is already in Priva." Yes. The contribution is the resolution of the actuator.
- "Is this real?" No, and then the list in the section above.
- "What about wind and hail on thin fins?" Unproven. The simulation does not model wind.
- "What does it cost against a screen at two dollars a square foot?" No cost claim. One actuator a row is a hypothesis.
- "Why would a hingeless fin matter here?" The sources document the chores it removes: lubricating bearings, racks, and hinge points, and tensioning cables. No saving is quantified.
- "Why Apopka?" The University of Florida calls it the heart of Florida's greenhouse and nursery industry, and shade houses are the practice there.
- "What did you build this weekend, and what did you plan before?" Everything in the repo was written during the event. Before the event the team planned a different idea, in public, and set it aside on Saturday, so this project was planned and built inside the hacking period. The planning repo is public and linked. Say that plainly: it is true, and the commit history shows it.
- "How did three of you use the build agents?" `CHECKLIST.md`: one package, one branch, one owner, expected values computed before any code, and gates after every package.

## The cards on the table

1. "Simulated today": the figures from `headline.json`, the place, the year, the two sources.
2. "Not claimed": yield, cost, water saved, safety from disease, wind, hail, a built roof.
3. "Not ours": the fin, ITKE, the patent number, and the control logic, with the makers named.
4. "Ours": light by the bed, one element that shades, vents, and admits rain, and the rules, printed.

## The README, before submission

The first screen answers three things: what it is, in one sentence; the hero frame, H2's state 5; and how to run it, in two commands.
Then: what is simulated and from what data, every source and library cited, the build agent named as a tool, the team, and the prior work statement with the link to the planning repo.
