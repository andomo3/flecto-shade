# Mockup prompt, for Claude Design

Two prompts for iterating the UI mockup until it passes a scorecard.
Prompt A re-anchors the design session and is pasted once, at the start of a session.
Prompt B is pasted every round after that.
Both are derived from `ui-brief.md`, `../pitch/storyboard.md`, and the playbook's UI checklist, and they are planning, not code.
The mockup is never copied into the event repo: the page is ported from it by hand.

## How to run the rounds

- One round is one paste of Prompt B, one revised design, and one scorecard.
- The scorecard is the signal, and a round that does not move it is a stuck round.
- Cap the session at 7 rounds: 28 scorecard rows, about 5 fixed per round, plus one round of slack.
- Two rounds in a row with no row changing from FAIL to PASS means stop and reframe, not push on.
- The design tool's own PASS is a claim, not a proof.
  Rows 1, 2, and 25 are checked by a person, standing a metre from the laptop.

## Prompt A, paste once per session

```text
CONTEXT
You are continuing the UI mockup for a HackMIT 2026 hardware project: a tabletop bus stop
roof made of three hingeless leaves that bend into shade on their own when a light sensor
sees the sun. The mockup is for one web page shown on one laptop at a judging table, next
to the physical model. A judge stands about a metre away and watches for ninety seconds.
The page will later be rebuilt by hand as a single HTML file with plain CSS, vanilla
JavaScript, and inline SVG, offline, so the design must be achievable with exactly that.

The story the screen tells: a rider waits on a bench in Houston in July. The judge presses
Play, one real Houston day runs in about sixty seconds, the sun climbs, the leaves bend,
and the bench falls into shade. At the end a result card shows how much light reached the
bench with the leaves bent against resting.

TASK
Continue improving the existing mockup. Do not start over and do not change the concept.
It is one scene, not a dashboard: a sky that changes colour through the day, a sun moving
across it, a simple front view of a bus stop with three leaves, and a plain seated
silhouette on the bench who is lit or falls into shade. Two bars, "Sun" and "Bench", sit
beside the scene. The hero moment is those two bars pulling apart when the leaves bend.

How the stop is drawn. Two posts, a beam across the top, a bench, and the seated figure,
seen from the front. The roof is not a panel. It is three leaves in a row above the beam.
Each leaf has two parts: a thick curved rib, and a thin translucent sheet attached along it.
- Resting: each sheet stands on edge, so the roof is three slim, slightly curved blades
  with open sky between them. Light shafts pass between the blades and land on the figure.
- Bent: the ribs arc and each sheet unfurls sideways into a wide curved petal. The three
  petals close the gaps, and one shadow band covers the bench and the figure.
- There are no hinges. The shapes bend like a flower opening and never rotate like
  shutters. The bend takes about four seconds.
- Every in-between pose follows one "angle" value from 0, resting, to 1, bent, so draw
  the leaf as a shape that can be interpolated, and show the poses at 0, 0.5, and 1.
- A conventional bus stop has one solid fixed slab for a roof. In state 10, draw that
  slab on a second, plainer stop beside ours, with its shade patch missing the bench.

Design these twelve states as separate frames, and mark state 3 as the hero frame:
1. Opening, before Play: headline "A bus stop roof that bends into shade on its own",
   the night scene, the date, "Houston", one large Play button. No numbers at all.
2. Day running, morning: leaves resting, both bars rising together, badge "Resting".
3. Day running, midday: leaves bent, Sun bar high, Bench bar low, badge "Bending into
   shade", the figure in shadow. HERO FRAME.
4. A hand over the sensor: the Sun bar collapsed, the badge following, the caption
   "The sensor moves the leaves, not the app".
5. The result card: two large figures, "X% bent" against "Y% resting", under the words
   "Light reaching the bench, measured today on this table", and a "Play again" button.
6. Waiting for the first reading: skeleton shapes, no spinner.
7. Only the sun sensor fitted: the Bench bar reads "not fitted" in muted text, never
   zero, and the figure stays neutral. It must look deliberate, not broken.
8. The board stopped sending: "The board stopped sending readings. Check the USB cable,
   or switch to this morning's recorded run." with a button for the recorded run.
9. Replay mode: a banner in words, "Replay mode: the app is driving the leaves from the
   data". Never a subtle icon.
10. Optional pieces on: a third bar "Fixed roof" that does not drop, a small temperature
    line under the scene, and the sun on an arc instead of a strip.
11. The drawer open: brightness, sun angle, source, replay mode, "Reset the day".
12. The city picker: a quiet selector beside the date, Houston first.

CONSTRAINTS
- The judge presses exactly one button. Every other control lives in the hidden drawer.
- Colour tells the time. Three colours only: sky, sun, shade. Deep blue before dawn, warm
  amber at noon, cooling at dusk. Green, orange, and red are reserved for status.
- Numbers arrive late: none before Play, small beside the bars while the day runs, large
  only on the result card.
- The screen must never out-animate the physical model. Motion is slow, and the only
  fast thing is the Sun bar reacting within a quarter second when a hand covers the sensor.
- The figure is a plain seated silhouette, no face, no name on screen.
- Nothing on the page is under 18 px. The headline, the badge, and the result figures
  read from a metre away.
- One typeface from a system font stack, no web fonts. Two heading sizes and one body size.
- All spacing in multiples of 4 px. Rounded corners throughout. Soft shadows instead of
  borders. One icon style. Text contrast at least 4.5 to 1 against every sky colour,
  including the amber noon sky.
- Inline SVG and CSS only: no photographs, no raster images, no libraries.
- Honesty is part of the layout. The dataset line reads "Sun: PVGIS typical year,
  Houston, real date". Anything modelled says "modelled". The result figures in the
  mockup are sample values, and say so in your notes, not on the screen.
- Laptop layout only, 1440 by 900. No mobile layout, no navigation bar, no footer.
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
 1. At a glance, frame 1 says what this is: a roof that bends into shade.
 2. The headline, the badge, and the result figures are legible at a metre on a laptop.
Main action
 3. Play is the only interactive element visible in frame 1.
 4. No control other than Play and "Play again" is visible outside the drawer.
Hierarchy and spacing
 5. Every gap and padding is a multiple of 4 px.
 6. Two heading sizes and one body size, and no text under 18 px.
 7. The scene takes the top two thirds of every day-running frame.
 8. The two bars are the second thing the eye lands on, after the scene.
Colour
 9. Three colours plus neutrals: sky, sun, shade.
10. Green, orange, and red appear only as status.
11. Text passes 4.5 to 1 on the dawn, noon, and dusk skies.
Story
12. Frame 1 shows no numbers.
13. Frames 2 to 4 show only small numbers, beside the bars.
14. In frame 3 the gap between the bars is the most striking thing on the page.
15. The figure is visibly lit in frame 2 and visibly shaded in frame 3.
16. The leaves in the picture are drawn resting in frame 2 and bent in frame 3.
17. Each leaf reads as a rib and a sheet, and the roof never reads as a solid panel.
18. Resting shows sky between the blades, and bent shows the gaps closed by the petals.
19. The leaf poses at angle 0, 0.5, and 1 are shown, and they bend rather than rotate.
States
20. Loading is a skeleton, not a spinner.
21. "Not fitted" reads as deliberate: muted text, no zero, no empty bar that looks broken.
22. The error state is human, says how to fix it, and offers the recorded run.
23. Replay mode is a banner in words.
24. The result card is still: the live bars are gone and nothing moves.
Premium
25. Frame 3 could go in a README as it is: no placeholder, no clutter, nothing misaligned.
26. Soft shadows not borders, rounded corners throughout, one icon style.
27. Hover and focus states exist for Play, "Play again", and every drawer control.
28. Every frame is buildable with plain CSS and inline SVG.
```

## Prompt B, paste every round

```text
Round N of 7. Make the three changes you proposed, plus these from me: [my notes, or none].
Keep everything that already passes. Then reply in the agreed format: the frames, the full
scorecard with evidence, and the next three changes. If no FAIL row moved to PASS this
round, say so plainly and tell me what is blocking it.
```

## When it is done

All 28 rows PASS, rows 1, 2, and 25 confirmed by a person at a metre, and frame 3 exported as the hero image.
