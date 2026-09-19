# The story

Written before the scripts, because every script is a cut of it.
Built from the playbook's storytelling section, through the `hackathon-pitch` skill, following `../plans/pitch-plan-d.md`.
Every figure below carries its source, and anything in square brackets is the team's to decide or to confirm.

Four honesty notes, settled before a word is spoken.
There is no hardware at all: nothing physical was built, nothing is on the table to hold, and the project is the simulation.
Elena is an illustrative grower, introduced with "picture", because we interviewed nobody.
The "ever since then" beat is a vision, said as a vision, because nothing has been built or deployed.
Every figure from our own run is provisional, from the planner's run, and is confirmed against `data/processed/headline.json` before it is said.

## The hero: the grower

[Elena], a grower near Apopka, in Central Florida, with three crops under one shade house roof: Boston fern, hydrangea, and blueberry.
She is not an engineer or a persona on a slide: she is someone with three kinds of plant and one sky to give them.
The name is illustrative and the team may change it.
The structure is a shade house, and the team may say greenhouse in plain speech.

Why Apopka: the University of Florida's research centre there describes itself as "Located in the heart of Florida's greenhouse and nursery industry", and shade houses are the practice there.
Any grander title for the town was seen only in search snippets, and is never said.

## The villain: the single curtain

Not "the weather", which is too large to fight, and not "inefficiency", which nobody can picture.
The villain is the single curtain: one motor, one decision, for every plant under it.
It is strong because it is the honest state of the art, and the numbers say so.

| Specific | Source | Status |
|---|---|---|
| "One gear motor will handle up to 50,000 sq ft of roof" | UMass fact sheet on retractable roof greenhouses and shadehouses, quoted in `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md` | spoken specific 1, read once more at the source before it is said |
| For screens, "one drive motor can handle up to 40,000 sq ft" | UMass fact sheet on selecting a screen system, the same research file | for the question bank only |
| Boston fern is "high quality" from 8 mol per m2 per day, and hydrangea from 12 | Purdue HO-238-W, Table 2, quoted in `../plans/packages/H1-zones-light-rain-soil.md` | spoken specific 2 |
| Blueberry: "A 30-50% shade net is recommended", so the zone uses a shade share of 0.40 | Washington State University fact sheet, in H1 | not Florida practice, said so whenever the blueberry's number is said |
| The rain supplied about 54 percent of the hydrangea zone's water over 2023, simulated | our own run, 0.545 in H1's year table | spoken specific 3, provisional, from the planner's run, confirm against `headline.json` before it is said |
| About 17 percent for the blueberry zone, and the fern held to its 8 mol on about 354 of 365 days, simulated | H1's year table, 0.171 and 354 | provisional, the same rule, for the card and the questions |
| 3 June 2023: 42 mm of rain in two hours, the fern shut at eleven, the hydrangea at noon | H1's demo day table, 42.4 mm, local hours 11 and 12 | provisional, the same rule |
| Opening for that rain gave the hydrangea about 6 mol of light it did not want | H1's demo day, 5.96 mol, 12.72 to 18.68 | provisional, the same rule |
| 2023 was an ordinary year for rain at that gauge, 2.4 percent above the 1991 to 2020 normal | H1, from the NOAA normals for station USW00012841 | for the questions |
| The fin is the Flectofin, by ITKE at the University of Stuttgart, patented as EP2320015 | `../docs/research/flectofin-design-tool/sector-choice.md` | said unasked, every time |

Three specifics per sixty seconds is the playbook's rule.
Ours are 50,000 square feet a motor, 8 mol against 12, and about 54 percent.

## The turn

A roof made of many small fins can give each bed its own answer.
That is the whole idea, and it is the only part that is ours.

## The story spine

- **Once upon a time** there was a grower named [Elena], near Apopka, with three crops under one shade house roof.
- **Every day** one curtain made one decision for all of them, because one motor moves up to 50,000 square feet of roof.
- **Until one day** we read the growers' own light tables, and the fern wanted 8 mol a day where the hydrangea wanted 12, and the blueberries wanted nearly all of it.
- **Because of that** whatever the curtain did was wrong for somebody, and we asked what a roof would do if it could decide bed by bed.
- **Because of that** we went looking for a roof element small enough, and found one that already exists: ITKE's Flectofin, a fin that bends open with no hinge.
- **Until finally** we simulated a roof of those fins over her three zones, on a real year of Central Florida weather, by nine written rules: night, then rain, then light.
- **And ever since then**, in the shade house we want, the fern is shut by eleven, the blueberries have the whole sky, and the afternoon storm falls only on the bed that is dry.
  That is a vision, and it is said as one.

## The lens: the honesty is the pitch

A judge who knows horticulture will know within a minute that most of this exists.
So the story says it before they can, and that is what earns the one claim that is left.
The lens changes the order, not the claims.

- **One hero, still.**
  Elena carries the pitch from the opening line to the last.
  The plants are never the hero: the stake is a grower's living.
- **What is not ours is said unasked, in this order.**
  The fin is ITKE's.
  The control logic, watering by the sun's energy and holding a daily light target, is standard practice in greenhouse computers sold by Ridder, Hoogendoorn, Argus, and Priva.
  Moving roofs over crops are sold by Cravo and Sun'Agri.
  Growers keep rain off glasshouse crops on purpose, which is why this is a shade house, why each crop opts in, and why the fern opts out.
  Nothing here is measured.
- **What is ours is one thing.**
  The resolution, zone by zone.
  The words are "we found no prior proposal to put a Flectofin over crops", and never anything stronger.
- **The roof is dumb on purpose.**
  Nine written rules, no AI and no learned model in the loop, and the fins never follow the sun's position.
  They react to how much light has arrived, to rain, and to the soil.

## The emotional arc, at the table

| Beat | Feeling | What carries it |
|---|---|---|
| Setup | recognition | "Picture Elena", three crops, one sky |
| Tension | unease | one motor, 50,000 square feet, one decision for every plant under it |
| Disarming | trust | what is not ours, said before anyone asks |
| Rising action | curiosity | what a fin is, over the shut roof: a blade that bends open with no hinge, ITKE's and credited |
| Climax | delight | the judge presses Play, and by noon the three zones stop behaving as one roof |
| Proof | surprise | the same storm, three answers, each with its reason in words |
| Resolution | respect | the trade on the card: the rain came with six mol of light the hydrangea did not want |
| Close | warmth | back to Elena, then the offer |

Without the low the high does not land, so the single curtain gets its full breath before the fins appear.

## The closing story

The callback close, because the story opened on a person and should end on her.
The closing line is abba's to write, in abba's own voice.
Until then the scripts carry this working draft, and it is replaced, not polished.

"Elena still has three crops and one sky.
Now the roof can tell them apart."

Then the offer, which at a booth is an invitation and not a funding ask.

"Press Play again, and this time watch only the hydrangea."

If a judge asks what we want next: one grower near Apopka willing to tell us where this is wrong.

## The demo as a scene

The playbook's five rules, applied.

1. Never without a backup: the recorded run of the same day, then the screen recording.
2. A story during the demo: the judge is not shown a dashboard, the judge is handed Elena's third of June.
3. The transformation, not the process: no code, no data pipeline, three zones parting ways is the whole show.
4. End on an emotional beat: the same rain, three answers, and the trade said plainly.
5. Under sixty seconds: the day plays in about a minute, so the narration runs over it and never before it.

The scene, from `../plans/plan-d-louvre-roof.md`: the fern has its light by eleven, the hydrangea by noon, the blueberries want all of it, then the afternoon storm, and three zones give three answers to the same rain, each for its own reason.

## What this story asks of the screen

The screen is the second storyteller at the table, and its specification is `../plans/packages/H2-page.md` and `H3-result-card.md`.
In one line: the screen shows Elena's roof and Elena's day, never a dashboard, and every zone says its reason in words.

## Where each figure came from

| Figure | File |
|---|---|
| 50,000 and 40,000 square feet a motor | `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md` |
| 8 and 12 mol, the 0.40 shade share, the Apopka quote | `../plans/packages/H1-zones-light-rain-soil.md` |
| 54 and 17 percent, 354 days, 42 mm, eleven and noon, 6 mol, 2.4 percent | the same file, from the planner's run, all provisional until `headline.json` exists |
| The patent number and the inventors | `../docs/research/flectofin-design-tool/sector-choice.md` |
