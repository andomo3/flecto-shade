# hardware - local memory

Owners: the two engineers, across the mechanism, structure and rig, and electronics roles.
The engineers decide what the hardware is, and their hour by hour plan in `../docs/meetings/2026-09-18.md` is the MVP.
Do not reopen their scope, only record it and keep the seams to firmware and software clear.

## The event rule

The HackMIT rules, in their 2023 wording, allow bringing hardware components but forbid assembling or programming them before the hacking period.
Designing, sizing, and sketching beforehand is planning and is allowed.
Whether parts printed beforehand may be used is still unanswered in writing, and the engineers' plan prints at the venue, so it does not depend on the answer.

## What gets built, in the engineers' order

| Venue hours | Step | Checkpoint |
|---|---|---|
| 0 to 2 | Two or three backbone and lamina variants from 2 mm and 0.5 mm with a built in resting curve, prints queued first, hand flexed | The best combination picked |
| 2 to 4 | One leaf on one servo through a pull wire or rigid link | Repeatable across several cycles |
| 4 to 6 | Three leaves on one backbone, one servo | Reliable, or two leaves |
| 6 to 8 | The foam board rig: bus stop frame, LED sun mount, servo box, mount points | The LED sees the photoresistor |
| 8 to 9 | The flex sensor on the backbone | A rough indicator |
| 9 to 12 | The photoresistor, the threshold, the LED sun | Hard checkpoint: light on, leaves respond |
| 12 to 14 | Everything into the rig, the bench light sensor, the secondary temperature sensors, wiring secured | First full run in the rig |
| 14 to 15 | Debugging the move from bench to rig | The full cycle verified |
| 15 to 17 | Back to back runs, servo pacing, the override, the rehearsal | Consistent |

The plan was written for more hands than the team now has.
With two engineers the parallel rig build in hours six to eight has nobody free, so expect a pivot or two to fire.

## Ideal, backup, and pivots

- Ideal: the LEDs on a servo mount so the sun moves, decided at hour 8, and the pivot is the fixed LED mount.
- Backup: a fixed roof with its own bench sensor, an hour of foam board, built only if the core loop is green at hour 12 and someone is free.
- The full pivot table with its hours is in `../project-brief.md`.
- A mechanical overrun takes its time from the software layer first, never the other way round.

## What firmware and software need from here

- A second light sensor on the bench, looking up at the roof, because the number is bench light against incident light.
- Confirmation that the flared leaf is the shading state.
- The servo on its own 5 V supply or battery with a common ground, never the board's 5 V pin.
- The pins in `electronics/pinout.md`, the resting and flared servo angles, and the light thresholds measured in the judging room.
- On an Uno the LED goes on a PWM pin that is not 9 or 10, because the Servo library takes those.

## Subdirectories

`leaves/` is the mechanism, `frame-rig/` is the structure and the LED sun mount, `electronics/` is sensors, power, and the pinout, and `exports/` holds milestone exports only.
Each has its own README and local memory.
