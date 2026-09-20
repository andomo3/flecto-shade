# Design partner prompt, for planning the page as part of the pitch

A prompt for a design agent used as a thinking partner, before anything is drawn.
It is a different tool from `mockup-prompt.md`: that file tells a mockup tool what to draw, and this one sets up a conversation about how the screen should carry the pitch.
It is written in the playbook's four parts, context, task, constraints, and format, and it is self contained, because the design agent does not have this repo.

How to use it.

- Paste the whole block below as the first message, and answer the agent's questions before it designs anything.
- Every simulation figure in it is provisional, from the planner's run, and is checked against `data/processed/headline.json` before it is shown or said.
- What comes back is a plan in words, not code, and abba decides what goes into `ui-brief.md`.
  Anything that would change a specification, H2 or H3, is a decision for abba and is never made by the design agent.
- The playbook's warning applies: accept nothing untested, and hold every suggestion against the ninety second table.

```text
CONTEXT

You are my design partner for a hackathon project, and I want you to think with me, not
to draw yet. We are at HackMIT 2026, judged expo style: a judge walks up to our table,
stands about a metre from one laptop, and gives us two to three minutes. There is no
hardware and nothing to hold. The project is one web page and the story told over it, so
the screen is the second storyteller, and the pitch wins or loses on what that page shows
in ninety seconds.

The project: a SIMULATED smart louvre roof for a foliage grower whose beds want different light under one shade
house roof near Apopka, in Central Florida. The screen shows three beds as three light classes: Boston fern, hydrangea,
and blueberry, one per zone, named A, B, and C.

The story, in the order the judge hears it:
1. The hero is a grower we call Elena, introduced as illustrative with "Picture Elena".
   The general problem comes from her own university: fifty foliage crops with shade from
   30 to 90 percent, croton wanting 30 percent in summer where 47 is too much in winter,
   and a shade house that gives every bed one number.
2. How a roof like hers works today: "a fine brain, and a blunt hand". The climate
   computer is already fine grained: it holds a daily light target and waters one valve
   at a time. The roof is not: one motor pulls up to 50,000 square feet of curtain. So
   every plant under it gets one decision.
3. The pain: the fern is at its best from 8 mol of light a day and the hydrangea from 12,
   and to change a plant's light today, Elena moves the plant. Rain is the same problem:
   under cloth a storm falls on every bed alike, and on a bed that is already wet it
   leaches the fertilizer. So one bed should use the rain and another be protected from it.
4. Why the fin: to decide bed by bed a roof needs many small parts, and with hinges every
   one is a bearing to grease, a documented chore. So the roof is made of a part with no
   hinge: the Flectofin, a thin blade on a rib that bends open. The same part shades,
   opens for air, and lets rain through. The fin is NOT ours: it is by ITKE at the
   University of Stuttgart, patented as EP2320015, and the page credits it.
5. What IS ours is one thing: the size of the decision, "a bed, not a building".
6. The demo: the judge presses one Play button, and the page plays a real day, 3 June
   2023, from a real rain gauge and a satellite's sun for the same place and year.
7. The close: the year by month, what we do not claim, the ask (one grower near Apopka
   to tell us where it is wrong), and back to Elena.

What the page does, which is fixed by the specification and is not yours to change:
- It shows the roof FROM ABOVE: three beds side by side, each under its own grid of fins,
  by default 4 rows of 6 fins per zone. A fin drawn open is a thin line with the bed
  visible beneath. A fin drawn shut is a filled leaf shape that covers the bed.
- Per zone: the crop's name, a light gauge that fills toward its target (8 mol for the
  fern, 12 for the hydrangea, and no target for the blueberry, which says "shade rule"),
  a soil gauge drawn against a 60 mm bucket with marks at 18, 30, and 54, and one line of
  words that says why the zone is doing what it is doing.
- A sky strip whose colour follows the sun, rain drawn over all three beds when it
  falls, the clock as a local hour, the date, one Play button, and "Reset the day".
- A footer in words: the label "simulated", the two data sources, and the credit to ITKE.
- The zone's words are fixed, nine of them: "Night", "Open: still needs light", "Shut: it
  has had its light for today", "Partly shut: too hot", "Open for the rain: the soil is
  dry", "Shut: this crop opted out of rain", "Shut: the soil is wet enough", "Shut: no
  daylight left to dry the leaves", "Shut: the rain is too hard".
- At the end of the day it shows a result card: each crop's light against its target,
  when each zone shut for light, the rain each zone stored, and one line for the trade:
  opening for the rain gave the hydrangea about 35 mm of water and about 6 mol of light
  it did not want. Then the year by month, as inline SVG bars.

The timing, which is fixed and computed from the real data. A dark hour plays in 0.5
seconds, a daylight hour in 2.4 seconds, and an hour with rain in 5.0 seconds:
- Play to 15.0 s: night, then sunrise, all fins open, three light gauges filling.
- 15.0 s: the fern's fins shut. 17.4 s: the hydrangea's fins shut. The blueberry stays
  open. This is the moment the three zones stop behaving as one roof, and it is the
  moment the project wins or loses.
- 24.6 s to 34.6 s: the storm, 42 mm in two hours. The hydrangea's fins REOPEN because
  its soil is dry, the blueberry stays shut because its soil is wet enough, the fern
  stays shut because it opted out. Same rain, three answers, each with its reason in
  words. The storm holds the screen for 10 seconds, slowed on purpose so they can be read.
- 43.8 s: the result card.
- A fin takes 1.5 seconds to change, and never less: the screen shows a slow roof.

TASK

Help me decide how this page should look and behave so that it carries the pitch. Work
through these with me, in this order, and push back where I am wrong:

1. The three second test. A judge a metre away glances at the page before Play. What do
   they understand, and what is the one thing the layout has to make obvious? Propose
   the visual hierarchy.
2. Showing the villain. The story opens on "a fine brain, and a blunt hand", but the page
   before Play is a shut roof. Should the screen show the old way at all, for example
   one curtain over all three beds, or is that the speaker's job alone? Give me the case
   for and against, and what it costs in build time.
3. Drawing the fin. How should a hingeless fin read from above, open, shut, and partly
   shut, so that 72 of them look like a roof of many small parts and never like a solid
   panel or a bar chart? It has to stay cheap to draw in plain SVG or CSS.
4. The moment at 15.0 to 17.4 seconds. How do I make "three zones stop behaving as one
   roof" impossible to miss without an animation that feels like a trick?
5. The storm problem. Three reasons in words have to be read in 10 seconds from a metre
   away. What do I do with type size, position, colour, and what persists after the
   rain stops? Tell me plainly if 10 seconds cannot work, and what the smallest change
   would be.
6. The honesty on screen. "Simulated" has to be on every figure, and the credit to ITKE
   has to be on the page, without the page reading as a wall of disclaimers. Where do
   these live?
7. The result card and the year view. One still screen has to land the trade and one
   figure. What is the single largest thing on it, and what is cut?
8. Look and feel. Propose two or three directions, each in one paragraph with a named
   palette of three colours and a system font stack, and say which one serves a grower's
   story and a judge a metre away. It should look like a product, not a dashboard.
9. States. Before Play, playing, the card, the year, reset, a missing data file, and the
   default layout. Say what each one looks like in one line.

CONSTRAINTS

- Plain HTML, CSS, and vanilla JavaScript. No framework, no library, no chart library,
  no build step, no CDN, no web fonts fetched at run time, and no image or script loaded
  from any outside address. System fonts only. Charts are inline SVG drawn by hand.
- One laptop, laptop layout only, designed at 1440 by 900. No mobile layout.
- The page adds no physics and invents no number. Everything it shows is read from two
  JSON files written by the simulation, so do not propose a feature that needs data the
  list above does not contain.
- The judge touches exactly one thing, the Play button. No sliders, no settings, no
  second control needed to understand the demo.
- Honesty rules, which outrank every design idea. Every figure says "simulated" or
  "modelled". The word "measured" may appear once only, in the rain source line, because
  the rain is a real gauge. Never show or suggest these words as claims: "first",
  "maintenance free", "weatherproof", or any figure for cost, yield, energy, or water
  saved. Nothing may imply that a roof or a fin was built or tested, that the fins track
  the sun's position, or that any AI is in the control loop. The roof follows nine
  written rules.
- The structure is a shade house on the page, never a greenhouse.
- One open conflict I want your view on: the specification wants no digit at all on the
  page before Play, but the date, the patent number, and the gauge number all hold
  digits. Propose how to honour the intent.
- Build time is about two hours for the whole page, by an AI coding agent working from a
  written specification. Rank every idea as must, should, or only if there is time, and
  give each a rough cost in minutes. If an idea takes more than thirty minutes and the
  demo can run without it, say so and offer the smaller version.
- Do not write code, and do not redesign the story, the rules, the timing, or the nine
  fixed phrases. If you think one of those hurts the demo, say so as a flagged note and
  carry on.

FORMAT

Round 1: before proposing anything, ask me up to five questions whose answers would
change your advice. Then stop and wait.
Round 2: answer items 1 to 9 above, each under its own heading, each ending with a one
line recommendation and its cost in minutes.
Round 3: after my replies, give me the final plan as:
- a frame by frame table for the ninety seconds, with columns for time, what the judge
  sees, what changes on screen, and the one thing their eye should be on;
- the chosen palette and type scale, with sizes in pixels that survive a metre;
- a ranked build list, must, should, and only if time, with minutes;
- the three biggest risks to the demo, and the cheapest guard against each.
Keep every answer in plain, short sentences. No hype. When you are unsure, say so.
```
