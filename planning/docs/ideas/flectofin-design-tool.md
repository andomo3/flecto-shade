---
title: Flectofin leaf design tool
type: idea
status: shortlisted   # proposed | researching | shortlisted | rejected | chosen
owner: team   # team, or one word handle if a single person is driving it
updated: 2026-09-19
---

# Flectofin leaf design tool

Chosen by abba at about 16:00 on Saturday 2026-09-19, five hours into the event, as a pivot away from the bus stop canopy.
It grows out of ameya's [leaf design loop](../research/adaptive-bus-stop-canopy/flectofin-leaf-design-loop.md), which is the measured half of it.
The properties and the use cases were left "to be decided", and this file proposes both so the team can confirm or change them at one standup.

**Changed at about 16:30: the MVP is software only.**
Abba: "we are not doing hardware anymore besides building the fin itself just for display. The MVP now is the tool that optimises the params."
So there is no jig, no measured variant table, no fatigue run, no servo link, and no calibration factor from measurement.
The section below, "The software only MVP", is the current plan, and where the older sections disagree with it, it wins.
The bus stop and the other architectural uses are dropped as over engineered, and the sector is being chosen from five candidates in `../research/adaptive-bus-stop-canopy/design-tool-applications.md` and the research that follows it.


## The software only MVP

### What it does

The user picks a use case in the chosen sector and gives what the flap must do: the span, the opening it needs, the material, the actuator's force budget, the cycle life, and the air pressure across it.
The tool searches the rib's dimensions, throws out every design that breaks a gate, ranks the rest by the use case's objective, and recommends one.
It shows why: the feasible region, which gate killed each rejected design, and how far the recommendation sits from each limit.
It then writes the recommended fin as a printable file, and the fin on the table is that file, printed.

### With no measurements, what makes it trustworthy

A tool that only evaluates three textbook formulas invites "how do you know it is right", so the evidence has to come from somewhere other than a bench.

1. **The exact solution, not the approximation.**
   The three formulas in the design loop note are the small deflection approximation.
   A pinned column pushed past buckling has an exact closed form, the elastica, in elliptic integrals, which `scipy` provides.
   A throwaway check on 2026-09-19 showed the two agree within about 2 percent at a 20 mm sag on a 150 mm span and drift apart as the bend grows.
   At a 30 mm sag with a 1.5 mm rib the approximation gives 0.987 percent strain, which passes a 1 percent limit, and the exact solution gives 1.042 percent, which fails it.
   So the tool uses the exact solution, reports the approximation beside it, and can show a design the textbook formula would have passed and should not have.
2. **Tests against hand worked values.**
   The table in the design loop note, checked by hand, becomes the test data for the approximation, and the elastica's small bend limit must reproduce it.
3. **Published Flectofin figures, if a source states them.**
   Any dimension, force, or flap angle printed in Lienhard et al. 2011 is a check the tool can be run against, and none is used from memory.
4. **One ruler, optional.**
   The relation between the end push and the sag is pure geometry and does not depend on the material, so two ruler readings on the display fin check it in two minutes.
   This is measuring the display piece, not building a rig, and the team may decline it.

### What it cannot do, said on the page

- It sizes the rib and the actuation. It does not predict how far the sheet flips, because no formula here covers the sheet, and without measurements nothing else does either.
- The sheet's stiffness adds force the model ignores, so every force is a lower bound.
- No wind, no weight, no creep, no fatigue model: the cycle life enters only as a lower strain limit, chosen from a source.
- Every output is modelled.

### The demo

The judge picks a use case and drags the span and the actuator budget.
The feasible region redraws as they drag, and the recommended fin changes.
One slider position shows the design the textbook formula passes and the exact solution fails.
The speaker hands over the printed fin: "the tool designed this one, bend it."
A scaling panel shows the same proportions at ten times the size: the strain unchanged, the force a hundred times larger.

### What gets built, all of it software

| Piece | What |
|---|---|
| The engine | The elastica, the approximation, the gates, the pressure check, the search, and the ranking, as one small Python module with no web code in it |
| The materials list | A small table of stiffness and strain limit per material, every row with its source |
| The use cases | Three rows of requirements and an objective each, in the chosen sector |
| The page | The sliders, the feasible region, the recommendation, the reasons, and the scaling panel |
| The export | The recommended fin as a printable mesh, generated in code |
| The gates | Package G1, unchanged |

### What this change drops

The variant table and its loader, the calibration factor, the proposer, the fatigue counter, the link to the real leaf through the `S` command, and the Arduino challenge.
The print queue closes on Saturday night, so the display fin is printed from the first recommendation the formulas give, today, and not from the finished tool.

## Problem

A hingeless leaf replaces a hinge, a pin, and a spring with one printed part, and nobody can tell you how thick to make it.
Today the answer is to print, bend, crack, and print again.
The tool takes what the leaf has to do and what is available to drive it, and recommends the leaf's dimensions, with the force, the strain, and the stroke it predicts, checked against leaves measured on the table.

## What the tool is, stated so it can be checked

"For [use case], with [span], [material], and [actuator], make the leaf [dimensions], push it [stroke], and expect [force] and [strain], and here is how close that prediction came on the leaves we measured."

It is three things, and the word "optimises" is earned only by the first:

1. **A screen and a search, from physics.**
   The rib is a pinned column pushed along its axis, so three standard formulas give the force, the peak strain, and the end push for any rib.
   The tool searches the dimensions a printer can make and keeps those that pass the gates: strain at or below the material's limit, force inside the actuator's budget, and printable.
   Within that set it ranks by the use case's objective.
2. **A calibration, from measurement.**
   The formulas ignore the sheet, so the first measured force gives a factor `k`, and every later prediction is multiplied by it.
   The flare angle and the shade cannot be predicted from the formulas at all, so they come only from the variant table, as measured points, never as a fitted curve through a handful of leaves.
3. **A proposer, for the next experiment.**
   One variable at a time, reversible changes before cuts, and "stop" when the last two rounds moved less than the spread of repeated readings.
   A language model may fill this role, in the design loop and never in a control loop.

### Two results the formulas give for free

Both follow from the three formulas in the design loop note, were checked by hand on 2026-09-19, and are modelled, not measured.

- **Strain does not depend on size.**
  Scale every length of a leaf by the same factor, and `eps = pi^2 t delta / (2 L^2)` does not change.
  A leaf that survives at 150 mm has the same strain at 1.5 m, so the proportions found on the table carry to any scale.
- **Force grows with the square of the size, and with the stiffness of the material.**
  `P = pi^2 E h t^3 / (12 L^2)` scales as the factor squared, so ten times larger needs a hundred times the force, before the material changes.

Those two sentences are what lets a tabletop leaf say something about a full size one, and they are the tool's best claim to insight.
What they do not cover: the sheet, the weight of the leaf, wind, and fatigue.

## The properties the tool recommends, proposed

| Property | Symbol | How it is decided |
|---|---|---|
| Rib bending depth | `t` | Searched, in steps the printer can make |
| Rib height | `h` | Searched |
| Pin span | `L` | Given by the use case, or searched under a largest span |
| End push, the actuator's stroke | `Delta` | Computed from the sag the use case needs |
| Sheet thickness | `s` | From a list, multiples of the layer height |
| Sheet width and outline | `w` | From the measured table only, because no formula covers it |
| Actuator class | | The smallest whose budget exceeds the force times `k` |

Reported with every recommendation: the force, the strain and its margin, the stroke, which gates passed, and whether each figure is modelled or measured.

## The use cases, proposed, three and no more

A use case is a row of requirements the model can score, not a story.

| Use case | Span | Material | Actuator | What "best" means | Evidence behind it |
|---|---|---|---|---|---|
| The tabletop leaf | 120 to 150 mm | Printed PLA | One SG90, about 8 N | The most sag inside the strain limit and the servo's budget | Measured on the jig tonight, so this is the one the tool is checked against |
| A shading fin at building scale | 1 to 2 m | Glass fibre reinforced polymer, as the published Flectofin | To be sized | The least actuator force for the sag needed | The two scaling results, and material values only if a source states them. Modelled, and said so |
| A flap that cycles all day, a vent or a damper | 50 to 150 mm | PLA now, a tougher polymer named as untested | A small servo | The most cycles, so a lower strain limit | The fatigue run on the spare leaf, which is the only cycle evidence the team has |

The bus stop is the second row under another name, and keeping it there costs nothing and keeps a person in the pitch.
Whether it stays is the team's call, and abba's words were "forget the bus stop".

## The demo moment

The judge picks a use case and moves two sliders, the span and the actuator.
The feasible region redraws, and the tool names one leaf: its dimensions, its stroke, its predicted force and strain.
Then the speaker says "and here is that leaf", and the leaf on the table bends at the recommended stroke, driven from the screen.
Beside it on the screen, two rows: what the tool predicted, and what the team measured on that leaf.
In the corner, a counter that has been running since the afternoon: the cycles the spare leaf has survived.
The judge bends a spare leaf by hand.

The prediction beside the measurement is the honest centre of the demo, and it works whether they agree or not, because the gap is `k`, and `k` is a finding.

## Hardware needed

- Whatever the design loop note already assumes: the bench jig, printed leaf variants, an SG90 or two, the Uno R3, a photoresistor, an LED, a multimeter, a ruler, and a phone for the flare angle.
  [Which of these are really on the bench is not confirmed, and abba's own inventory earlier in the day was shorter.]
- No new part.

## Software needed

- The design engine: the three formulas, the gates, the search, and `k`, as one small Python module with tests against the hand worked table in the design loop note.
- The variant table as a CSV, and a loader that refuses a row with a missing unit or an impossible value.
- One page: the use case, two sliders, the feasible region, the recommendation, and predicted against measured.
- The link to the real leaf: the contract's `S` command, packages B13 and B14 from Plan B, unchanged.
- The cycle counter, read from the fatigue board's serial line.
- The proposer, optional, and the last thing built.

## What carries over, and what is dropped

Carried over: the gates and package G1, the handoff prompt and the rules for the build agent, the honesty rules, packages B13 and B14, the stack, and the pitch's method.
Dropped: the solar data pipeline, the shade table and the whole light simulation, the METRO analysis, the farmworker analysis, the mockup and its scorecard, and both sets of scripts.
That is most of a day's planning, and it was cheap: no code was written against any of it.

## Risks, said plainly

- This is the third plan today.
  The playbook's rule is that the worst outcome is no finished project, so this is the last pivot, and the 17:00 standup closes the question.
- A handful of measured leaves cannot support a fitted model, so the tool never draws a curve through them and never says "optimal flare".
- Without a person in the story the pitch loses the lens the keynote asked for.
- The Voloridge challenge asks for public data, and this project's data is its own, so that prize is likely out of reach.
- The measuring is the engineers' time, and the tool is empty without it.

## Open questions

- Which parts are really on the bench, and has plate 1 printed? The engineers, now.
- Are the three use cases and the seven properties right? The team, at the 17:00 standup.
- Does the bus stop stay as the second use case? The team.
- The elastic modulus and the strain limit of glass fibre reinforced polymer, from a source, for the second use case. Whoever takes the research, and never from memory.
- Does Dimensional have a challenge, and does the proposer fit it? Abba.

## Sources

- [The leaf design loop](../research/adaptive-bus-stop-canopy/flectofin-leaf-design-loop.md), ameya, 2026-09-19.
- [Which applications a design tool could optimise for](../research/adaptive-bus-stop-canopy/design-tool-applications.md), the earlier, light driven framing, now superseded by this file.
- [Lienhard et al. 2011, Flectofin](https://doi.org/10.1088/1748-3182/6/4/045001), as cited in the design loop note, not re-read here.
