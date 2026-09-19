# electronics - local memory

> **SUPERSEDED on 2026-09-19 at about 16:45. This file is the record of the bus stop canopy, and nothing is built from it.**
> The current plan is the simulated louvre roof over three crops.
> Read `AGENTS.md` and `CHECKLIST.md` at the repo root, then `planning/plans/plan-d-louvre-roof.md`.
> If you are a build agent and you arrived here, stop, and go back to those files.

Owner: the electronics role, one of the two engineers.

What is on the board, by priority:

| Part | Job | Priority |
|---|---|---|
| Leaf servo | Bends the backbone | core |
| Incident photoresistor | Drives the threshold, the only thing that moves the leaves | core |
| Bench light sensor | The number, light at the bench against incident light | core, the engineers' plan named one photoresistor, so this one is an addition |
| LED sun on a PWM pin | Dimmed by the app to play a day | core |
| Override button, to ground with the internal pull up | The backup trigger | core |
| Flex sensor on the backbone | An indicator that the bend happened, never a control input | hour 8 |
| Sun mount servo | Moves the LED sun | ideal, decided at hour 8 |
| Two DS18B20s, or the thermal camera | Temperature, secondary | hours 12 to 14, only if time allows |
| Fixed roof bench sensor | The backup comparison | only if the backup roof is built |

Rules:

- The servo runs from its own 5 V supply or battery with a common ground, never the board's 5 V pin, because a servo can brown out the board and reset it.
  Flagged on 2026-09-18, believed covered, checked at the first servo test in hour 2.
- On an Uno the Servo library takes PWM on pins 9 and 10, so the LED goes on pin 5 or 6.
- A photoresistor needs a fixed resistor as a divider, and the value sets the usable range, so pick it under the LED sun and the room light, not by guess.
- The DS18B20 needs a 4.7 kilohm pull up on its data line.
- On the UNO Q the serial link to the laptop is the D0 and D1 pins at 3.3 V, through a level shifter to a USB serial adapter or a second Uno as a bridge.
- `pinout.md` is the contract with firmware: every pin, both sensor positions, the supplies, the common ground.
  The firmware's `config.h` is copied from it.

Pivots, with their hours:

- Hour 9, the flex sensor is noisy: indicator only, or dropped.
- Hour 12, the threshold is unreliable in room light: a shroud on the photoresistor, then the override, then replay mode.
- Hour 13, the bench sensor shows no clear difference: move or shroud it.
- Hour 14, temperature shows nothing: drop it.
