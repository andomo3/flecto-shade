# firmware - local memory

> **SUPERSEDED on 2026-09-19 at about 16:45. This file is the record of the bus stop canopy, and nothing is built from it.**
> The current plan is the simulated louvre roof over three crops.
> Read `AGENTS.md` and `CHECKLIST.md` at the repo root, then `planning/plans/plan-d-louvre-roof.md`.
> If you are a build agent and you arrived here, stop, and go back to those files.

Owner: the firmware role.
The proposal on the 2026-09-18 agenda is that abba takes it, so the engineers' hours nine to twelve shrink to wiring.
This is the planning repo.
The sketch under `canopy/` and the harness under `host_test/` are a pre-event prototype that proved the contract, and neither is copied into the event repo.
At the event the sketch is rewritten from this plan and from `SERIAL_FORMAT.md`.

## What this directory becomes

One Arduino C sketch that reads the sensors, runs a threshold with hysteresis, steps one leaf servo, drives the LED sun, and prints one contract line ten times a second.
It runs with no laptop attached.

## Decisions that bind this directory

- `SERIAL_FORMAT.md` version 2 is the contract, eleven fields, and it is a specification, so it is the one file here that carries over as is.
- The control law is a threshold on the incident photoresistor, never a tracker, and the flex sensor is never a control input.
- Bright light flares the leaves, and the flared leaf is the shading state.
  This is one constant, so if the engineers say otherwise it is a one line change.
- The laptop sets the LED brightness and the sun angle.
  It sets the leaf angle only in replay mode, the hour twelve pivot.
- Every pin, threshold, angle, and "is this sensor fitted" switch lives in `config.h`, so the loop is never edited at the venue.
- An unfitted sensor prints an empty field.

## The skeleton, in build order

| Step | What | Check | When |
|---|---|---|---|
| 0 | The hour one gate: an empty sketch with `Servo.h` and `analogRead` compiles and runs on the UNO Q | It runs, or the team moves to the Uno R3 and says so in `RUN.md` | hour 1 |
| 1 | A servo sweep sketch for the engineers, travel limits as two constants | The engineers have it in hand before their hour two servo test | by hour 2 |
| 2 | The ten hertz loop on `millis()`, the header line at boot and every ten seconds, a line with `light` only and every optional field empty | The laptop parser accepts every line | hour 3 |
| 3 | The threshold with hysteresis, and the rate limited servo step, a few degrees per tick | Covering and uncovering the photoresistor flares and rests the leaf at a pace a judge can follow | hour 4 |
| 4 | The command reader: a small line buffer, `L`, `O`, `P`, out of range and unknown input ignored | Typing commands in the serial monitor works, and garbage does nothing | hour 5 |
| 5 | The override button on an internal pull up | Holding it flares the leaves and the last field reads 1 | hour 5 |
| 6 | The `HAS_` switches for bench, fixed, flex, and sun servo, each printing its field only when fitted | Turning one on changes exactly one field | as each sensor arrives |
| 7 | `A` for the sun servo and `S` for replay mode, with `O 0` handing the leaves back | The app's day player moves the sun, and replay mode shows override 1 | hour 8 to 12 |
| 8 | The DS18B20s, secondary: start a conversion without waiting, collect it a second later, keep the last good value | The ten hertz line never stutters | hour 12 to 14, only if time allows |

## What the prototype taught

- The whole sketch is about 4.3 KB, 13 percent of the Uno's flash, and 8.5 KB with the temperature libraries.
- On the Uno the Servo library takes over PWM on pins 9 and 10, so the LED goes on pin 5 or 6.
- A DS18B20 read blocks for up to 750 ms unless `setWaitForConversion(false)` is set.
- The libraries are Servo, OneWire, and DallasTemperature, all open source, so they are cited in the submission.
- The toolchain is already on abba's laptop: `arduino-cli` at `~/tools/arduino-cli/`, with `arduino:avr` and `arduino:zephyr` installed, board names `arduino:avr:uno` and `arduino:zephyr:unoq`.
- Compile time switches can be passed as `--build-property "compiler.cpp.extra_flags=-DHAS_BENCH=1"`, which is how to build a variant without editing a file.
- The sketch can run on a laptop under a fake clock with a thirty line stand in for `Arduino.h`.
  Standard headers must be included before it, because `min` and `max` are macros in the Arduino core.
  Worth rebuilding at the event only if there is slack.
- The prototype was never compiled for or run on the UNO Q, so step 0 is still a real gate.

## Values the engineers must supply

Pins, the ADC full scale on the UNO Q, the resting and flared servo angles, the light thresholds measured in the judging room, and confirmation of the servo's own 5 V supply with a common ground.

## Pivots that land here

- Hour 1, UNO Q trouble: the Uno R3.
- Hour 12, threshold unreliable: a shroud, then replay mode through `S`.
- The servo browning out the board: its own supply, never the board's 5 V pin.
