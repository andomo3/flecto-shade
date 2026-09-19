# Plan A: the live demo

> **SUPERSEDED on 2026-09-19 at about 16:45. This file is the record of the bus stop canopy, and nothing is built from it.**
> The current plan is the simulated louvre roof over three crops.
> Read `AGENTS.md` and `CHECKLIST.md` at the repo root, then `planning/plans/plan-d-louvre-roof.md`.
> If you are a build agent and you arrived here, stop, and go back to those files.

Applies when all five gate items in `README.md` are in hand at 17:00 Saturday.
This is the plan the team already had, gathered into one place with the event day changes folded in.
The detail stays in the files it points to, and this file is the order and the checks.

## The MVP

One miniature foam board bus stop, seen from the front, under an LED sun.
Three hingeless leaves on one backbone and one servo bend into shade when the incident light sensor crosses a threshold, and a second sensor on the bench gives the number.
The laptop plays one real Houston day to the LED in about sixty seconds and shows the scene, two bars, and a result card.

In: the leaves, one servo, the threshold with hysteresis, the incident and bench light sensors, the LED sun, the app, the fast forward day, fixture replay, the override button, the backup video.
In if time allows, in this order: the flex sensor, the servo mounted sun, the temperature sensors, the backup fixed roof, the city picker.
Out: everything on the cut list in `../project-brief.md`.

## The build, after the shared core

The shared core, C1 to C9 in `README.md`, comes first.
Then these, each with a check.

### Firmware, from `../firmware/CLAUDE.md`

The build agent writes the sketch and a person flashes and tests it, because the agent cannot touch the board.

| ID | Build | Done when |
|---|---|---|
| A1 | The hour one gate: an empty sketch with `Servo.h` and `analogRead` | It compiles with `arduino-cli compile` for the chosen board and runs, or the team moves to the Uno R3 and says so |
| A2 | A servo sweep sketch, travel limits as two constants in `config.h` | The engineers run it on their hour two servo test |
| A3 | The ten hertz loop on `millis()`, the header at boot and every ten seconds, `light` only, every optional field empty | C1's parser accepts every line from the real board |
| A4 | The threshold with hysteresis and the rate limited servo step | Covering and uncovering the photoresistor bends and rests the leaf at a pace a judge can follow |
| A5 | The command reader, `L`, `O`, `P`, garbage ignored, and the override button | Typed commands work, garbage does nothing, the last field reads 1 while the button is held |
| A6 | The `HAS_` switches for bench, fixed, flex, and the sun servo | Turning one on changes exactly one field |
| A7 | `A` for the sun servo and `S` for replay mode, `O 0` hands the leaves back | The day player moves the sun, and replay mode shows override 1 |
| A8 | The DS18B20s, only if there is slack | The ten hertz line never stutters |

### Software, the two steps that need the board

| ID | Build | Done when |
|---|---|---|
| A9 | `SerialSource` in `sources.py`, the port as a command line argument, reconnect after a pulled cable | `python -m canopy serve --source serial --port COM3` shows live readings, and pulling the cable shows state 8 and recovers |
| A10 | Replay mode, the hour twelve pivot: the app sends `S` from the day's data and the banner says so in words | The banner shows whenever `override` is 1 and the app sent `S` |

### Hardware, from `../hardware/CLAUDE.md`

The engineers' seventeen hour table is unchanged and is not reopened.
Two values are owed to the pitch: the state the leaf returns to with no power, and the spread of the bench readings in each state.

## Pivots

The table in `../project-brief.md` stands.
One row is new: a part that cannot be sourced by 17:00 Saturday sends the team to Plan B through the gate.
After the gate, a Plan A failure never falls to Plan B from scratch: it falls to replay mode, then the recorded fixture, then the backup video, because those are already built.

## The demo, ninety seconds

`../pitch/storyboard.md` is the script, beat by beat, unchanged except beat 2, which now gives the study's cause.

| Time | The judge sees | The judge does |
|---|---|---|
| 0:00 | The model still, the screen on its night scene with one Play button and no numbers | Listens to Rosa |
| 0:25 | The Play button | Presses it |
| 0:30 | The LED brightens, the sky warms, both bars climb | Watches the table |
| 0:40 | Three leaves bend over four seconds, the bars pull apart, the figure falls into shade | Watches the leaves, then the bars |
| 0:50 | The Sun bar collapses and recovers | Covers the sensor with a hand |
| 1:05 | The LED dims, the leaves rest | |
| 1:15 | The result card: X percent bent against Y percent resting, "measured today on this table" | Hears the number and what it is not |
| 1:25 | Stillness | Hears the closing line |

Pre-set before every judge and reset after in under five seconds with "Reset the day".
The fallbacks, in order: the override button, replay mode with its banner, the recorded fixture, the backup video.

## The presentation

Everything is already written under `../pitch/`, and Plan A changes none of it.

- The story, the hero, and the lens: `../pitch/story.md`.
- The 30 second, 60 second, and 3 minute scripts, inside their word targets: `../pitch/script.md`.
- The Q&A bank, including the rain answer and the ten event day questions: `../pitch/questions.md`.
- The four placards, with card 1 "Measured today": `../pitch/placards.md`.
- The table routine and rehearsal: `../pitch/checklist.md`.
- The two videos and the submission draft: `../pitch/video.md` and `../pitch/submission.md`.

The number is X percent bent against Y percent resting, with the count of readings and the spread on card 1.
Challenges entered: the track, Arduino Touch Grass if the UNO Q runs the sketch, and Voloridge if the METRO analysis ships, see `../docs/research/adaptive-bus-stop-canopy/voloridge-datasets.md`.

## The clock

| When | What must be true |
|---|---|
| 17:00 Saturday, hour 6 | The gate is passed, the shared core C1 to C7 is green, and the page renders from a fixture |
| 20:00, hour 9 | One leaf bends from the threshold, A1 to A5 |
| 23:00, hour 12 | The hard checkpoint: light on, leaves respond, the app shows it live, A9 |
| 23:00 to 00:45 | The safety take of the video is filmed |
| 01:00 Sunday | Freeze: nothing new after the venue closes |
| 07:00 to 09:00 | Thresholds set in the judging room, ten cycles back to back, the measurement run for X, Y, and the spread |
| 09:00 to 10:30 | Rehearsal, card 1 filled in, the submission checked |
| 11:00 | Submitted |
