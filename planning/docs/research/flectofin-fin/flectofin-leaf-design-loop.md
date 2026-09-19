---
title: How the evolved structures loop applies to making the Flectofin leaf, in a version the team can run at the event
type: research
status: done   # open | in-progress | done | dropped
owner: ameya   # one word handle of the teammate doing the research
updated: 2026-09-19
idea: adaptive-bus-stop-canopy
---

# How the evolved structures loop applies to making the Flectofin leaf, in a version the team can run at the event

## Answer

Yes, and the version that works now is a physical design loop on the leaf itself, with the canopy's own bench as the test rig and no new build.
It keeps three things from the rejected [AI that evolves biomimetic structures](../../ideas/evolved-biomimetic-structures.md) idea: a physical rig as the scorer, the measured history feeding the next proposal, and the manufacturing limits written into what may vary.
It runs at two speeds: a slow loop through the print queue that changes what is printed, and a fast loop on the bench that changes the leaf after printing, by pin span, stroke, and trimming the sheet, in minutes and with no queue.
A spare servo cycles a spare leaf through the evening, so the pitch gets a fatigue number instead of "we have not answered it".
A language model choosing the next variant is optional, costs five minutes a round, and is allowed because it sits in the design loop and never in the control loop.
Everything here fits inside the mechanism owner's hours 4 to 6 wait for the three leaf print, and it stops the moment it competes with the one leaf on the servo checkpoint.

## Findings

### What carries over from the rejected idea and what does not

| From the evolved structures idea | Kept | Why |
|---|---|---|
| A physical rig as the scorer, not a simulation | Yes | The bench jig, the photoresistor, and the servo are already on the table |
| The full history goes back to the proposer each round | Yes | It is one table, the variant table [hardware/leaves/CLAUDE.md](../../../hardware/leaves/CLAUDE.md) already asks for |
| Manufacturing limits inside the search | Yes | 0.2 mm layers, flat L print, PLA only, one print round left before the queue closes |
| Generating geometry from biological strategies with CadQuery or OpenSCAD | No | One mechanism is chosen, only its dimensions vary |
| Ten generations through the printer | No | The venue queue gives one more round at most, so most generations happen after printing |
| The crush test against a solid control | No | The leaf is scored on flare, shade, force, and set, not strength |

### What may vary

Printed, slow, one round left at most:

- Rib bending depth `t`, 1.5 or 2.0 mm, in the direction the rib bows.
- Rib height `h`, 5 mm to start.
- Sheet thickness `s`, 0.4 or 0.6 mm, never 0.5 mm, because it must be a multiple of the 0.2 mm layer.
- A pin tab with three holes at each end instead of one, 10 mm apart, so the pin span becomes a bench variable.
  This is the one design change worth making if another plate goes in.

After printing, fast, minutes each:

- Pin span `L`, by choosing a hole, reversible.
- Servo stroke, the end push `Delta`, by the servo end points, reversible.
- Sheet width `w`, trimmed with the flush cutters or the knife, not reversible.
- Sheet outline, a taper or rounded outer corners, not reversible.

Reversible changes are tried first and cuts last, so a leaf is never ruined before its settings are known.

### The pre-print check, modelled, from beam formulas

The rib is pinned at both ends and pushed along its axis, so it buckles into a bow of sideways sag `delta`.
Three formulas screen a variant before any print or cut, with `E` about 3 GPa for printed PLA, an assumption the first force reading corrects.

- Rib force, the Euler load, which stays within a few percent over bends this size: `P = pi^2 E h t^3 / (12 L^2)`.
- Peak rib strain: `eps = pi^2 t delta / (2 L^2)`, kept at or below 1 percent, half of where PLA starts to take a set.
- End push needed for a sag: `Delta = pi^2 delta^2 / (4 L)`.

| `t` mm | `L` mm | Rib force N | Strain at 20 mm sag | Largest sag at 1 percent | Push for 20 mm sag |
|---|---|---|---|---|---|
| 1.5 | 150 | 1.9 | 0.66 % | 30 mm | 6.6 mm |
| 2.0 | 150 | 4.4 | 0.88 % | 23 mm | 6.6 mm |
| 1.5 | 120 | 2.9 | 1.03 % | 19 mm | 8.2 mm |
| 2.0 | 120 | 6.9 | 1.37 %, fails | 15 mm | 8.2 mm |

The sheet adds stiffness the formulas ignore, so these forces are lower bounds.
Divide the first measured force by the table's force to get a factor `k` for the sheet, and multiply every later prediction by it.
The SG90 is rated about 1.8 kg cm at 4.8 V, roughly 17 N at a 10 mm horn hole at stall, so plan on about 8 N per servo.
One leaf fits an SG90, and three 2.0 mm ribs at 150 mm, about 13 N before `k`, belong on the MG996R, as the [checkout list](../../../hardware/checkout-list.md) already says.
Every number in this section is modelled and is said that way.

### The rig, and what it measures with no new code

The bench jig is foam board with one fixed pin and the servo horn on the other end tab, as the checkout list describes.

| Measure | How | Unit |
|---|---|---|
| Clean buckle | Five pushes, count how many flip the intended way | n of 5 |
| Flare angle | Phone photo looking down the rib from the fixed end, against the cutting mat's angle lines | degrees, nearest 5 |
| Push and sag | Ruler, the end push `Delta` and the rib's sideways bow `delta` | mm |
| Shade | The spare photoresistor taped under the leaf's centre, the LED at a fixed height, the multimeter in ohms, read with no leaf, at rest, and flared | ohms, higher is darker |
| Force | The multimeter on its 10 A range in series with the servo's 5 V lead, holding at full flare | mA |
| Set | The rib's rest bow and the sheet's rest angle after release | mm, degrees |
| Make | Slicer minutes and grams, any print defect, minutes of trimming | min, g, yes or no |

Rank shade by the resistance ratio, flared over no leaf, because a photoresistor's resistance is not proportional to light.
The percent of light at the bench comes from the real rig later, not from this jig.
If the firmware owner has twenty spare minutes, an INA219 on the servo lead or the 5 kg load cell with its HX711 replaces the multimeter reading, written in the event repo and never here.

### How a variant wins

Gates first, all four or the variant is out: 5 of 5 clean buckles, strain at or below 1 percent, force within the servo budget, no crack or whitening.
Then rank by shade flared, then flare angle, then lower force, then lower set.
No weighted score, because a ranked list is easier to defend to a judge than weights nobody measured.

### The variant table

One row per test, in `hardware/leaves/CLAUDE.md` under "Record here at the event", by the mechanism owner.

| Gen | ID | Parent | Changed | t | s | L | w | Delta | Buckle n/5 | Flare deg | R none / rest / flared | mA | Set mm | Time | Kept |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | A1 | none | plate 1 | 2.0 | 0.4 | | | | | | | | | | |

### The schedule from 15:40 Saturday

| When | Step | Who | Minutes |
|---|---|---|---|
| Now to 16:15 | Generation 0: score every plate 1 variant, A, B, and C, with the protocol above, and fill the rows the hour 2 pick skipped | Mechanism | 30 |
| 16:15 to 16:30 | Start the fatigue run on the second copy of the winning variant | Mechanism, firmware for the sketch | 15 |
| 16:30 to 17:00 | Generations 1 and 2: pin span, then stroke, on the first copy of the winner | Mechanism | 30 |
| 17:00 standup | Decide the next plate: if the three leaf plate is not in, submit it with the winner and the three hole tab, if it is, the bench recipe is applied to it on arrival | Team | 5 |
| 17:00 to 17:30 | Generation 3: width, then outline, cutting a losing variant first, then the winner only once the loser shows the direction | Mechanism | 30 |
| Before the queue closes | Optional plate 3: one print candidate from the loop plus a spare, only if the desk still takes it and the main plate is safe | Mechanism | 10 |
| When the three leaf plate arrives | Generation 4, the production check: apply the recipe to each leaf and score all three, the spread across them is the repeatability number | Mechanism | 20 |
| Each standup to 23:00 | Read the fatigue specimen's cycle count and set | Whoever is free | 5 |
| 23:00 standup | The numbers go to the pitch owner | Mechanism | 5 |

Ask the print desk for the queue's exact closing time now, because every row with a print in it depends on it.
The whole loop costs the mechanism owner about two hours spread across the evening, most of it while the three leaf plate prints.

### The fatigue run

- The spare SG90 on the Uno R3, both idle, running the IDE's stock Servo Sweep example with its end points set to the tuned stroke, not 0 to 180.
- About two seconds a cycle is about 1,800 cycles an hour, so a 16:30 start reaches about 14,000 cycles by the 01:00 freeze.
- Its own 5 V supply, never the board's pin, and the supply the main bench is not using.
- Log the count from `millis()` over the serial monitor, or from the clock, and measure set with a ruler at each standup.
- If the main servo or board dies, the spare comes back to the main rig at once, and the fatigue run ends with the count it has.
- A servo that fails first is a servo finding, not a leaf finding, and is recorded as such.

### The optional proposer

Once a generation is scored, paste the table into Claude with this prompt, one call per generation.

> Context: we are tuning a Flectofin style leaf, a PLA rib with a thin sheet printed flat as one L section, pinned at both ends and pushed along its axis by a servo so the rib bows and the sheet flips sideways.
> The table below is every variant we have measured, on one bench jig.
> Task: propose the next two bench variants and, only if the print queue is still open, one print variant.
> Constraints: change one variable per proposal, from t, s, L, w, outline, or Delta; s must be 0.4 or 0.6 mm; keep strain pi^2 t delta / (2 L^2) at or below 1 percent; keep force below 8 N per SG90 after multiplying the Euler load by k = [k]; propose a cut only after the reversible changes on that leaf are exhausted; say stop if the last two generations moved flared shade by less than the spread of repeated readings.
> Format: one table row per proposal with parent, the change, the predicted direction of flare, shade, and force, the modelled strain and force, and the one measurement that would prove it wrong.
> [the variant table]

A person still cuts, prints, and measures every proposal, and turns down any that breaks a gate.
The pitch says a language model was used only if it was, and only as "it suggested the next variant from our measured table".

### Flectofin as a manufacturing idea, for the pitch only

For making the leaf, the true claim today is the part count: one flat print replaces a hinge, a pin, and a spring, with nothing to assemble.
The leaf's section is the same along its length, so at scale it could be a profile extrusion cut to length and trimmed, or a flat moulding with a straight pull, and neither is tested.
The published Flectofin was built in glass fibre reinforced polymer, not PLA, see [Lienhard et al. 2011](https://doi.org/10.1088/1748-3182/6/4/045001).

For use inside factories, the same principle already ships in a close relative.
Festo's DHAS adaptive gripper fingers use the Fin Ray effect from a fish's tail fin, polyurethane bands joined by webs with no pin hinges, sold for pick and place, see [the DHAS documentation](https://www.festo.com/media/catalog/202802_documentation.pdf).
A hingeless flap with no pin to wear or grease could suit vents and flaps in clean or washdown rooms, which is a direction for the judge, not a claim.

## Implications for the build

- No new build and no scope change: the loop uses the jig, the spare photoresistor, the spare SG90, the R3, and the multimeter already on the checkout list.
- The mechanism owner decides whether it runs, and it stops at once if the one leaf on the servo checkpoint is not green or any generation runs past thirty minutes.
- If another plate goes in, give the leaf a three hole pin tab at each end.
- The variant table replaces the free text "variant table" line in `hardware/leaves/CLAUDE.md`, which is the mechanism owner's edit.
- For the pitch owner, three lines to consider, none of them edits here:
  - Card 3's last line could read "One print. No hinges. No assembly."
  - "How did you pick the thickness": "we searched, N variants in G rounds on this jig, and kept the one that flared X degrees at Y mA."
  - The fatigue answer in [pitch/questions.md](../../../pitch/questions.md) gets the real count: "N cycles on a spare servo last night, Z mm of set."
- Strain and force from the formulas are modelled, and the flare angle, shade, current, cycles, and set are measured, as the honesty rules in [pitch/CLAUDE.md](../../../pitch/CLAUDE.md) require.

## Sources

- [AI that evolves biomimetic structures](../../ideas/evolved-biomimetic-structures.md), the L-01 design loop from the Load Paths catalog.
- [Engineers' build plan, 2026-09-18](../../meetings/2026-09-18.md), the hour by hour plan and the pivots.
- [Hardware desk checkout list](../../../hardware/checkout-list.md), the plate 1 variants, the PLA print settings, and the servo force estimate.
- [3D printing access](../3d-printing-access.md), the venue queue and its Saturday night close.
- [Lienhard et al. 2011, Flectofin: a hingeless flapping mechanism inspired by nature](https://doi.org/10.1088/1748-3182/6/4/045001), Bioinspiration and Biomimetics.
- [Festo, Adaptive gripper finger DHAS](https://www.festo.com/media/catalog/202802_documentation.pdf), the Fin Ray effect in an industrial gripper.
- The beam formulas are the Euler buckling load of a pinned column and the small deflection sine mode, standard results, computed here and not measured.
