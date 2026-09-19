# Firmware

Owner: the firmware role.

## Pre-event prototype, not a submission

This repository is the team's public planning repo.
HackMIT requires all project code to be written during the hacking period, so the event repo starts empty at 11:00 on Saturday 2026-09-19 and nothing is copied into it from here.
The sketch in `canopy/` and the laptop harness in `host_test/` was written on 2026-09-18 to check that the serial contract can be implemented, and it stays here, labelled, as part of the planning record.
The plan the event code is rebuilt from is in `CLAUDE.md` in this directory.

## The plan

The serial contract in `SERIAL_FORMAT.md` is owned by the software and data role.

One sketch in `canopy/`, plain Arduino C, that compiles for both boards:

- `arduino:avr:uno`, the Uno R3, used at home this week and as rung two of the downgrade ladder.
- `arduino:zephyr:unoq`, the Arduino UNO Q, used at the event for the Arduino challenge.

Rules:

- `Serial` only, 115200 baud, no Bridge, no Python on the board.
  On the UNO Q, `Serial` is the D0 and D1 pins, not USB, see `../hardware/electronics/README.md`.
- Pins and thresholds live in `canopy/config.h` so the firmware owner can change them without touching the loop.
- The loop is: read sensors, choose a servo target from the control law, move the servo with a rate limit, print one log line at ten hertz.
- Every log line matches `SERIAL_FORMAT.md` exactly.
  If the display cannot parse it, the firmware is wrong, not the display.

Install both cores before Friday so no download happens at the venue:

```
arduino-cli core install arduino:avr
arduino-cli core install arduino:zephyr
arduino-cli compile --fqbn arduino:avr:uno firmware/canopy
arduino-cli compile --fqbn arduino:zephyr:unoq firmware/canopy
```
