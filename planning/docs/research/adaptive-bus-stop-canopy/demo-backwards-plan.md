---
title: What the 90 second demo requires, worked backwards into build steps, pre-event tests, and roles
type: research
status: in-progress   # open | in-progress | done | dropped
owner: abba   # one word handle of the teammate doing the research
updated: 2026-09-11
idea: adaptive-bus-stop-canopy
---

# What the 90 second demo requires, worked backwards into build steps, pre-event tests, and roles

## Answer

The demo in [the brief](../../../project-brief.md) is two miniature bus stops under one moving lamp, and every build step below exists because one of its four beats needs it.
Working backwards from the beats gives four independent workstreams, mechanism, structure and control canopy, electronics and rig, and software and evidence, which map onto the four people with almost no shared critical path.
Five assumptions sit under the demo and all five can be tested at home before 2026-09-16, which is when the team either confirms the plan or pivots to the impact insert.

## Findings

### The demo, beat by beat, and what each beat needs

| Beat | What the judge sees | What must be true | Who makes it true |
|---|---|---|---|
| 1 Setup | Two roofs, two benches, one lamp arm, two bars on a screen | Frame and fixed roof built, sensors placed, display running before the judge arrives | ameya, lily, abba |
| 2 Trigger | The lamp swings across five marks | Arc rig exists, the marks are taped, the judge can move it or press one button | ameya |
| 3 Response | Leaves bend, no hinge, right bar stays low, left bar climbs | Flexures survive, servo tracks the lamp, sensors read a wide range, display updates under a second | shannon, lily, abba |
| 4 Number | "Five of five against Y of five" | The measurement run was done and the table is on screen and on a card | abba, lily |

### Working back from beat 3, the moment that wins or loses

Beat 3 needs, in dependency order from the judge's eye back to the bench:

1. A leaf that bends visibly and repeatably, which needs a flexure thickness that survives ten cycles, which needs a coupon test on real TPU.
2. Leaves that move together, which needs one servo, a common bar, and a linkage that does not bind, which needs the frame to hold the servo and the bar in line.
3. A leaf angle that follows the lamp, which needs a control law fed by the incident sensor, which needs the sensor to read a wide range under the lamp.
4. A right bar that stays low, which needs the leaf area and angle range to actually cover the bench at the end positions, which needs a quick foam board mock of the geometry before printing.
5. A left bar that climbs, which needs the fixed roof to have the same leaf area at the noon angle, so the comparison is fair.

Step 4 is the one nobody has tested and it is cheap.
A foam board leaf on a skewer over a photoresistor under a desk lamp answers it in an hour.

### Pre-event tests, one per assumption

| Assumption | Test | Pass mark | Owner | Due |
|---|---|---|---|---|
| Flexure survives | Print coupons at 0.8, 1.0, 1.2 mm, bend ten times by hand | No tear, returns flat | shannon | 2026-09-16 |
| Geometry covers the bench | Foam board leaf over a photoresistor, lamp at both ends of the arc | Under-roof reading drops at both ends when the leaf is angled | ameya | 2026-09-16 |
| Sensors read a wide range | Photoresistor and TEMT6000 under a desk lamp, shaded and not | At least two to one between shaded and unshaded | lily | 2026-09-16 |
| Servo moves three leaves | SG90 on external 5 V lifting three foam leaves on a bar | No stall, two clean end positions | lily | 2026-09-16 |
| Printer access | Answer from help@hackmit.org, or a teammate's printer plus a written ruling on pre-printed parts | A yes in writing, or a printer in the car | abba | 2026-09-16 |

Optional, only if the heat probe is to join the demo: the halogen test over a black foam figure with a DS18B20, five minutes, owner lily, carried over from 2026-09-05.

### Roles, from what each person has already done

The team is one software engineer and three hardware and CAD engineers.
Here is what the repo shows each person doing, and the role that follows from it.

| Person | Evidence in the repo | Draft role | Owns at the event |
|---|---|---|---|
| shannon | Wrote the canopy build plan and both briefs, and the inventory-only impact liner plan with its test protocol | Mechanism lead | Leaf and flexure CAD, print tuning, the spare leaf, the foam board motion fallback |
| ameya | Wrote the gecko and termite primary source audits, the finalist rescoring, and the three sponsor variants | Structure and comparison lead | Frame, linkage, servo mount, the fixed control roof, the lamp arc rig, the sponsor check at hour 0 |
| lily | Wrote the termite research with working firmware and a Python dashboard in the source folder | Electronics and rig lead | Sensors, servo power, wiring outside the aperture, the taped test geometry, pairs with abba on firmware |
| abba | The only software engineer, ships Python services, FastAPI, React, and evaluation harnesses | Software and evidence lead | Firmware control law and serial log, the display with fixture replay, the measurement run and results card, AGENTS.md, the submission form, the freeze clock |

Why the split works: the four streams meet only twice, when the servo goes into the frame at about hour 3 and when the sensors go under the roofs at about hour 5, and nobody's stream needs inverse kinematics or machine learning.
Why abba takes evidence and not just code: the number is the pitch, and building the harness first is the pattern that has worked before.

### Build order at the event, from the plan gates

| Elapsed | Work | Gate | Who |
|---|---|---|---|
| 0:00 to 0:30 | Confirm printer, filament, servo supply, lamp, queue the coupon and one leaf | Fabrication path confirmed or foam board fallback declared | all |
| 0:00 to 2:00 | Display runs on the fixture CSV, firmware compiles and logs a fake sensor | Two bars move on the laptop with no hardware | abba, lily |
| 0:30 to 2:00 | Frame, fixed roof, arc rig in foam board and print | One leaf bends by hand, lamp reaches all five marks | shannon, ameya |
| 2:00 to 3:30 | Servo in the frame, manual open and close | Two safe end positions, no stall | ameya, lily |
| 3:30 to 5:00 | All leaves on, sensors under both roofs | Leaves move together, both bars read live | shannon, lily |
| 5:00 to 6:00 | Control law on, override button, log verified | Leaves follow the lamp across the arc without help | abba, lily |
| 6:00 to 8:00 | Measurement run, five readings per position per roof, ten cycles | Results table on screen and on the card | abba, lily |
| 8:00 onwards | Finish, placards, rehearsal, spare leaf swap on camera | Three clean run-throughs by the judge's path | all |
| T-7 hours | Freeze, harden, video, submission | Nothing new after this line | abba enforces |

### What pivots the team

If the flexure coupon tears at every thickness, or no printer path exists by 2026-09-16, the team pivots to the impact insert, which is at 39 with nothing on the critical path that needs a printer.
The mound stays the second backup because its thermal signal is also untested.

## Implications for the build

- The software must run end to end on a fake serial stream before any hardware exists, so it is never on the critical path.
- The fixed roof is one hour and it is the difference between a demo that confirms the obvious and a demo with two possible outcomes, so it is built before the leaves are finished.
- The foam board geometry mock this week decides the leaf size and angle range, so the CAD waits for it.
- The heat probe stays on the cut list until the halogen test reports a number.

## Sources

- [Project brief](../../../project-brief.md).
- [Canopy build plan](feasible-build-plan.md), shannon, 2026-09-05, the gates and failure modes.
- [Score maximizing plan](score-maximizing-plan.md), team, 2026-09-07.
- [Frontrunner tweaks](../frontrunner-tweaks.md), abba, 2026-09-05, the adaptive against fixed tweak and the tracker reference designs.
- [Finalist rescoring](../hackathon-recon-scoring.md), 2026-09-07, the insert at 39 as the pivot.
- [Lily's termite research](../../sources/termite-mound-biomimicry-lily/README.md), the firmware and dashboard evidence for the electronics role.
