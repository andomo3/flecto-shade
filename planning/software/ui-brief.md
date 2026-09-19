# UI brief, derived from the demo

The screen is the second storyteller at the table.
It shows one grower's roof, three crops under it, and one real day of Central Florida weather, and it is never a dashboard.
This brief is derived from the demo table in `../plans/plan-d-louvre-roof.md`, the demo gate in `../plans/gates.md`, and the story in `../plans/pitch-plan-d.md`.
It is a design brief, so it is planning and not code, and the code lives in the repo's own `software/page/` directory.
Packages H2 and H3, `../plans/packages/H2-page.md` and `../plans/packages/H3-result-card.md`, are authoritative for every file, word, and figure, and where this brief and a package disagree the package wins.

## The one idea

Three zones that stop behaving as one roof.
The sun rises, every fin opens, and three light gauges fill at the same rate.
Then the fern's fins shut, the hydrangea's an hour later, and the blueberry's stay open.
Then the rain comes, and the same rain gets three different answers, each for a reason the page says in words.
That divergence is the product, and every design decision either sharpens it or gets out of its way.

## What is on the page

- **The roof from above.**
  Three beds side by side, each under its own grid of fins, from `data/roof-layout.json`, a modelled layout and not a built structure, or 4 rows of 6 fins per zone when that file is absent.
  A fin is drawn open as a thin line with the bed visible beneath, and shut as a filled leaf shape that covers it.
  The structure is called a shade house, never a greenhouse.
- **Three named zones.**
  Zone A Boston fern, zone B hydrangea, zone C blueberry, each with its crop's name on it.
- **Two gauges per zone.**
  A light gauge that fills toward the crop's target, 8 mol for the fern and 12 for the hydrangea.
  The blueberry has no light target, so its gauge shows the light received with no target mark, and says "shade rule".
  A soil gauge drawn against the bucket's 60 mm, with marks at 18, 30, and 54.
- **The zone's words.**
  One short line per zone that says what its fins are doing and why, from the nine fixed values in H2's table, such as "Open: still needs light" and "Shut: the soil is wet enough".
  The page never invents a tenth.
- **The sky.**
  A strip whose colour follows `ghi`, and rain drawn over all three beds in the hours it falls.
- **The clock and the date.**
  The local hour, and 3 June 2023.
- **One Play button.**
  "Reset the day" is on the `R` key and in the footer, for the five seconds between judges.
- **The footer, in words.**
  The label "simulated", the two sources, and the credit: "The fin is the Flectofin, by ITKE, University of Stuttgart, patented as EP2320015."
  The sun is "NASA POWER, satellite product, hourly means, modelled", and the rain is the NOAA gauge at Orlando Executive Airport, near Apopka, Florida.

## The screen follows the demo, beat by beat

| Beat | Demo time | The speaker | The screen | What is absent |
|---|---|---|---|---|
| 1 | 0:00 | The grower near Apopka, three crops, one sky | The roof from above, shut, three zones named with their crops, one Play button, the word "simulated" | Every digit. A judge who sees zeroes reads "broken", and a judge who sees figures stops listening |
| 2 | 0:20 | "Bed by bed takes many small parts, and every hinge is a bearing to grease. So we borrowed a part with no hinge: ITKE's Flectofin, patented, and not ours." | Unchanged. Nothing on the screen moves before Play | Any idle animation |
| 3 | 0:30 | "Would you press play? This is 3 June 2023." | One press starts the day, the sun rises, every fin opens, and three light gauges fill at the same rate | A second control |
| 4 | 0:45 | "The fern has had its light by eleven. The hydrangea by noon. The blueberries want all of it." | Zone A's fins shut when its gauge reaches 8 mol, zone B's about an hour later at 12 mol, and zone C stays open | Anything that competes with the fins shutting |
| 5 | 0:55 | "Then the afternoon storm. Forty two millimetres in two hours, from the real gauge." | Rain over all three zones. The hydrangea's fins reopen and its soil gauge climbs to full. The blueberry stays shut, "the soil is wet enough". The fern stays shut, "this crop opted out of rain" | A reason shown as an icon or a colour alone. Each reason is in words |
| 6 | 1:10 | "Same rain, three answers. And opening for it cost the hydrangea six mol of light it did not want." | The result card takes the screen: light against target per crop, the rain each zone stored, and the line for the trade, under "3 June 2023, simulated" | The live gauges, which have done their job |
| 7 | 1:20 | The close, and what it is not | The year by month: the wet season carrying the hydrangea, the dry season on the grower's own water, and nothing moves after it | Anything new |
| Reset | between judges | | One control returns everything to beat 1 in under five seconds | |

The judge touches one thing, the Play button.
There is nothing physical at the table, so the screen carries the whole demo.

## How the day plays

- A dark hour plays in half a second and a daylight hour in 2.4 seconds, from `play_seconds` in `day.json`, and the whole run from Play to the result card is between 36 and 42 seconds.
- Gauges move linearly between an hour's value and the next.
- A fin changes at the hour boundary, over 1.5 seconds, and never faster.
  The screen shows a slow roof.
- On the demo day, from H1's table: night until local hour 5, every zone open from 6, the fern shut at 11 with 8.08 mol, the hydrangea shut at 12 with 12.72, rain at 15 and 16, 23.9 and then 18.5 mm, the hydrangea's soil from 25.48 to 59.75, and night from 20.
  All of it is simulated.
- On the demo day the fern shuts 15 seconds after Play, the rain starts 24.6 seconds after Play, and the card arrives at 38.6, which is the demo table's 0:45, 0:55, and 1:10 with Play at 0:30.

## Design consequences

- **A picture, not a grid of tiles.**
  The roof from above is the largest thing on the page, and the gauges and the words belong to their zone, not to a side panel.
- **Colour tells the time.**
  Three colours plus neutrals: sky, sun, and leaf.
  The sky strip follows the light through the day, and it dims as the rain arrives without going dark, because the sun that afternoon falls from 726 to 517 to 377 W/m2 and does not collapse.
  Green, orange, and red stay reserved for status.
- **Numbers arrive late.**
  None before Play, small ones beside the gauges while the day runs, and the large figures only on the result card.
- **Words carry the reasons.**
  The zone's line is the thing the speaker points at in beat 5, so it is legible from a metre and it changes exactly when the fins do.
- **Honesty is part of the layout.**
  "Simulated" is on the page before Play and on every figure after it.
  The sun is said as modelled.
  The word "measured" appears once at most, inside the rain source line, where it is true of the gauge.
  The blueberry's shade figure is said to come from Washington State, and not to be Florida practice, in the honesty block under the year view.
- **Never on the page.**
  "First", "maintenance free", "weatherproof", and any figure for cost, yield, energy, or water saved.
- **One control.**
  The judge presses Play, and later "Play again" or "The whole year" on the card.
  There is no settings panel, no slider, and no picker.
- **Read from a metre away.**
  Nothing under 18 px, a system font stack, text contrast at least 4.5 to 1 against every sky colour, spacing in multiples of 4 px, rounded corners, soft shadows, and a laptop layout only at 1440 by 900.

NEEDED: beat 1 allows not one digit on the page, and the footer's rain source line holds a station number, the credit holds a patent number, and the date holds digits.
Abba settles how the footer and the date read before Play.

## The result card

- A heading in words: "3 June 2023, simulated".
- One row per zone: the crop, its light against its target, when its fins shut for light, the rain it stored, and its words for the rain: opened, wet enough, or opted out.
- One line for the trade: "Opening for the rain gave the hydrangea [rain stored] mm of water and [unwanted light] mol of light it did not want."
- Two buttons: "Play again" and "The whole year".
- Every figure on it is read from `data/processed/headline.json`, and none is typed.
- Until H3 exists, the end of the day shows the three zones' end of day values in a plain table.

## The year by month

- Twelve columns, one a month, and for zones B and C two stacked bars each: rain stored, and the grower's irrigation.
  The wet season and the dry season should be plain to see without reading a number.
- Under it, three sentences read from `headline.json`: the rain's share for the hydrangea, for the blueberry, and the days the fern met its light target.
- The rain's share is shown for the year only, never by month.
- The honesty block, in words: what is modelled, which figures rest on assumed constants, where the rain comes from, and that the blueberry's shade figure comes from Washington State and is not Florida practice.
- Inline SVG drawn by hand, one hue per series, direct labels, no legend to decode.

## States to design

These are H2's ten states, with the two H3 adds.

1. Before Play: the roof shut, three zones named, the Play button, the word "simulated", and not one digit.
2. Morning: all open, three gauges filling together.
3. The fern shut, the other two open.
4. The fern and the hydrangea shut, the blueberry open.
5. The rain: the hydrangea open for it, the blueberry shut as wet enough, the fern shut as opted out, each with its words.
   This is the hero frame, and the screenshot for the README.
6. Evening and night.
7. The end of day table, until H3 replaces it with the result card.
8. Loading: grey skeleton shapes, no spinner.
9. `day.json` missing or unreadable: "The day's file is missing. Run python software/page/build_day.py, then reload."
10. `roof-layout.json` absent: the default grid and the words "default layout" in the footer.
11. The result card, from H3.
12. The year by month, from H3.

One more drawing is needed though the demo day never shows it: a zone partly shut, open 0.60, with the words "Partly shut: too hot", because the blueberry's heat rule fires in the year and the words table has it.

## Acceptance, from the playbook's UI checklist

Through the `hackathon-ui-polish` skill: the 3 second test at a metre, done by a person and never by the agent, the main action visible at once, hierarchy on a 4 px grid, a skeleton loading state, a success state that is the result card, a human error state, and a screenshot ready hero frame with figures from the real run.
The mobile layout item is dropped on purpose, because the page lives on one laptop.
The page passes the demo gate's beats 1 to 7, the UI gate, and the pitch gate in `../plans/gates.md`, which means the screen and the speaker never disagree.
