# Mockup prompt, for a design tool

Two prompts for iterating the page's mockup until it passes a scorecard.
Prompt A anchors the design session and is pasted once, at the start of a session.
Prompt B is pasted every round after that.
Both are derived from `ui-brief.md`, packages H2 and H3 under `../plans/packages/`, the demo gate in `../plans/gates.md`, and the playbook's UI checklist, and they are planning, not code.
The mockup is never copied into `software/page/`: the page is written by hand, in plain HTML, CSS, and vanilla JavaScript, with the mockup as a picture to aim at.
Any AI tool used for the mockup is cited in the submission.

## How to run the rounds

- One round is one paste of Prompt B, one revised design, and one scorecard.
- The scorecard is the signal, and a round that does not move it is a stuck round.
- Cap the session at 7 rounds: 28 scorecard rows, about 5 fixed per round, plus one round of slack.
- Two rounds in a row with no row changing from FAIL to PASS means stop and reframe, not push on.
- The design tool's own PASS is a claim, not a proof.
  Rows 1, 2, and 25 are checked by a person, standing a metre from the laptop.
- Frame 1 is drawn with no clock, no date, and no footer line that holds a number, because beat 1 of the demo gate allows not one digit.
  How the real page words its footer before Play is an open point in `ui-brief.md`.
- The mockup comes second to the build.
  H2's last 30 minutes are polish and can be cut, so a session that is not converging is dropped, and the page is built from `ui-brief.md` alone.

## Prompt A, paste once per session

```text
CONTEXT
You are designing the UI mockup for a HackMIT 2026 project: a simulated smart louvre roof
over a shade house near Apopka, in Central Florida. A grower has three crops under one
roof: Boston fern, hydrangea, and blueberry. The roof is made of many small hingeless fins,
grouped into three zones, one zone per crop. Each zone opens and shuts by written rules:
it gives its crop its own amount of light, and it lets the rain through only when its
soil is dry. Everything is simulated from real 2023 weather. Nothing is a live reading.

The mockup is for one web page shown on one laptop at a judging table. A judge stands
about a metre away and watches for ninety seconds, and presses exactly one button. The
page will be built by hand as plain HTML, CSS, vanilla JavaScript, and inline SVG,
offline, with a system font, so the design must be achievable with exactly that.

The story the screen tells: the judge presses Play, and 3 June 2023 runs in about sixty
seconds. The sun rises and every fin opens. The fern's zone shuts late in the morning,
when it has had its light. The hydrangea's zone shuts an hour later. The blueberry's zone
stays open. In the afternoon it rains hard. The hydrangea's fins reopen, because its soil
is dry, and its soil gauge climbs to full. The blueberry's fins stay shut, because its
soil is wet enough. The fern's fins stay shut, because that crop opted out of rain. Same
rain, three answers, each with its reason in words. Then a result card, then the year by
month.

TASK
Design one scene, not a dashboard: the shade house roof seen from directly above.

How the roof is drawn. Three rectangular beds side by side, labelled "Zone A, Boston
fern", "Zone B, hydrangea", and "Zone C, blueberry". Over each bed sits a grid of fins,
4 rows of 6 in the mockup.
- A fin that is open is a thin line, with the bed and its plants visible beneath it.
- A fin that is shut is a filled leaf shape that covers its part of the bed.
- There are no hinges. A fin goes from line to leaf shape by bending, like a petal
  unfurling, and never rotates like a shutter slat. The change takes 1.5 seconds.
- A zone can also be partly shut, with each fin about 40 percent of the way to the leaf
  shape. Show the three poses, open, partly shut, and shut, as a small reference strip.
- All the fins in one zone move together. The three zones move independently, and that
  independence is the point of the whole design.

Per zone, close to its bed and clearly belonging to it:
- A light gauge that fills toward a target mark. The fern's target is 8 mol, the
  hydrangea's 12 mol. The blueberry has no target mark, and its gauge says "shade rule".
- A soil gauge, drawn as a bucket of 60 mm with marks at 18, 30, and 54.
- One line of words that says what the zone's fins are doing and why. Use only these:
  "Night", "Open: still needs light", "Shut: it has had its light for today",
  "Partly shut: too hot", "Open for the rain: the soil is dry",
  "Shut: this crop opted out of rain", "Shut: the soil is wet enough",
  "Shut: no daylight left to dry the leaves", "Shut: the rain is too hard".

Around the scene:
- A sky strip whose colour follows the light through the day, and rain drawn over all
  three beds in the hours it falls.
- The local hour as a clock, and the date.
- One large Play button.
- A footer in words: "simulated", then "Sun: NASA POWER, satellite product, hourly means,
  modelled", then the rain's source, the NOAA gauge at Orlando Executive Airport, near
  Apopka, Florida, then "The fin is the Flectofin, by ITKE, University of Stuttgart,
  patented as EP2320015." "Reset the day" sits quietly in the footer.

Design these twelve states as separate frames, and mark state 5 as the hero frame:
1. Before Play: the roof shut, three zones named with their crops, one large Play
   button, the word "simulated". Not one digit anywhere on the page, so no clock, no
   date, and no footer line that holds a number.
2. Morning: every fin open, three light gauges filling together, each zone saying
   "Open: still needs light".
3. The fern's zone shut, "Shut: it has had its light for today". The other two open.
4. The fern's and the hydrangea's zones shut. The blueberry's open.
5. The rain. The hydrangea's fins open again, "Open for the rain: the soil is dry", its
   soil gauge climbing. The blueberry's shut, "Shut: the soil is wet enough". The
   fern's shut, "Shut: this crop opted out of rain". HERO FRAME.
6. Evening and night: the sky cooling, the fins shut, "Night".
7. The result card: the heading "3 June 2023, simulated". One row per zone: the crop,
   its light against its target, when its fins shut for light, the rain it stored, and
   one word for the rain: opened, wet enough, or opted out. One line for the trade:
   "Opening for the rain gave the hydrangea X mm of water and Y mol of light it did not
   want." Two buttons: "Play again" and "The whole year".
8. The year by month: twelve columns, and for the hydrangea and the blueberry two
   stacked bars each, rain stored and the grower's irrigation, with a wet season and a
   dry season plain to see. Three sentences under it, and a short honesty block in
   words: what is modelled, which figures rest on assumed constants, and that the
   blueberry's shade figure comes from Washington State and is not Florida practice.
9. Loading: grey skeleton shapes in the place of the beds and gauges, no spinner.
10. The day's file is missing: "The day's file is missing. Run python
    software/page/build_day.py, then reload."
11. The layout file is absent: the default grid, and "default layout" in the footer.
12. A hot afternoon: the blueberry's zone partly shut, "Partly shut: too hot", the
    other two zones shut for the day.

CONSTRAINTS
- The judge presses exactly one button. No slider, no settings panel, no picker.
- Three colours plus neutrals: sky, sun, and leaf. Deep blue before dawn, warm at noon,
  cooling at dusk, and dimmer but not dark under the rain. Green, orange, and red are
  reserved for status.
- Numbers arrive late: none before Play, small beside the gauges while the day runs,
  large only on the result card.
- The screen shows a slow roof. Nothing moves faster than a fin, which takes 1.5
  seconds, and nothing moves at all before Play or after the year view.
- Nothing on the page is under 18 px. The zone names, the zone's words, and the result
  figures read from a metre away.
- One typeface from a system font stack, no web fonts. Two heading sizes and one body
  size.
- All spacing in multiples of 4 px. Rounded corners throughout. Soft shadows instead of
  borders. One icon style. Text contrast at least 4.5 to 1 against every sky colour,
  including the warm noon sky.
- Inline SVG and CSS only: no photographs, no raster images, no libraries.
- The year view has one hue per series, direct labels, and no legend to decode.
- Honesty is part of the layout. The word "simulated" is on every frame that shows a
  figure. The sun is called modelled. The structure is called a shade house. The words
  "first", "maintenance free", and "weatherproof" appear nowhere, and no figure for
  cost, yield, energy, or water saved appears anywhere. Every figure in the mockup is a
  sample value, and you say so in your notes, not on the screen.
- Laptop layout only, 1440 by 900. No mobile layout, no navigation bar.
- No lorem ipsum and no placeholder text anywhere.

FORMAT
After each revision, reply in this order:
1. The revised frames.
2. The scorecard below as a table: row, PASS or FAIL, and one line of evidence that
   names the frame and the element. Never mark PASS without evidence.
3. The three changes that would move the most FAIL rows, which you will make next round.
Change at most five things per round, so each round can be reviewed.

SCORECARD
The 3 second test
 1. At a glance, frame 1 says what this is: one roof, three crops, each zone on its own.
 2. The zone names, the zone's words, and the result figures are legible at a metre.
Main action
 3. Play is the only interactive element that draws the eye in frame 1.
 4. No control other than Play, "Reset the day", "Play again", and "The whole year"
    exists on any frame.
Hierarchy and spacing
 5. Every gap and padding is a multiple of 4 px.
 6. Two heading sizes and one body size, and no text under 18 px.
 7. The roof from above is the largest thing on every day-running frame.
 8. Each zone's gauges and words visibly belong to that zone, not to a side panel.
Colour
 9. Three colours plus neutrals: sky, sun, leaf.
10. Green, orange, and red appear only as status.
11. Text passes 4.5 to 1 on the dawn, noon, rain, and dusk skies.
Story
12. Frame 1 shows not one digit.
13. Frames 2 to 6 show only small numbers, beside the gauges.
14. In frame 4 the three zones visibly differ: two shut, one open.
15. In frame 5 the three zones show three different lines of words, and the difference
    is the most striking thing on the page.
16. An open fin reads as a thin line with the bed visible, and a shut fin as a leaf
    shape that covers it.
17. The fins bend between poses and never rotate like slats, and the reference strip
    shows open, partly shut, and shut.
18. The rain is drawn over all three beds, including the two whose fins are shut.
19. The blueberry's light gauge has no target mark and says "shade rule".
States
20. Loading is a skeleton, not a spinner.
21. The missing file state is human and says how to fix it.
22. "default layout" reads as deliberate, not broken.
23. The result card is still: the live gauges are gone and nothing moves.
24. The year view shows the wet season and the dry season without reading a number.
Premium
25. Frame 5 could go in a README as it is: no placeholder, no clutter, nothing misaligned.
26. Soft shadows not borders, rounded corners throughout, one icon style.
27. Hover and focus states exist for Play, "Play again", and "The whole year".
28. Every frame is buildable with plain CSS and inline SVG, and "simulated" is on every
    frame that shows a figure.
```

## Prompt B, paste every round

```text
Round N of 7. Make the three changes you proposed, plus these from me: [my notes, or none].
Keep everything that already passes. Then reply in the agreed format: the frames, the full
scorecard with evidence, and the next three changes. If no FAIL row moved to PASS this
round, say so plainly and tell me what is blocking it.
```

## When it is done

All 28 rows PASS, rows 1, 2, and 25 confirmed by a person at a metre, and frame 5 exported as the picture the hero frame is built toward.
The README's screenshot is taken from the real page, H2's state 5, with figures from the real run, never from the mockup.
