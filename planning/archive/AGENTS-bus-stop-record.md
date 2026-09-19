# AGENTS.md

> **SUPERSEDED on 2026-09-19 at about 16:45. This file is the record of the bus stop canopy, and nothing is built from it.**
> The current plan is the simulated louvre roof over three crops.
> Read `AGENTS.md` and `CHECKLIST.md` at the repo root, then `planning/plans/plan-d-louvre-roof.md`.
> If you are a build agent and you arrived here, stop, and go back to those files.

Rules for the build.
Every agent working in this repo reads this file first, and every human too.
`CLAUDE.md` points here, `project-brief.md` holds the scope, and `RUN.md` holds the status.

## What we are building

A tabletop bus stop roof made of hingeless leaves that buckle open on their own when the sun comes out, so the bench underneath stays cooler than the open ground beside it.

The 90 second demo path lives in `project-brief.md` and is read only once the event starts.
A feature serves those 90 seconds or it does not exist.
The MVP is the engineers' build plan, adopted in `docs/meetings/2026-09-18.md`, and the brief and `RUN.md` follow it.

## Do not build

The brief's cut list, plus the tech debt list in the `hackathon-build` skill, plus one line that matters at this venue.

- A two sensor tracker or a hand swung lamp.
  The control law is a threshold.
- The servo mounted sun or the backup fixed roof ahead of the core loop.
  The servo mount is the ideal and the fixed LED mount is the pivot, the fixed roof is a backup, and neither starts before the leaves respond to light.
- The flex sensor as a control input.
  It is an indicator only.
- Individually addressed leaves, a second actuator, or a fan.
- Machine learning or a language model anywhere in the control loop.
- A weatherproof or full scale shelter.
- A cloud dashboard, a phone app, or anything that needs the venue Wi-Fi.
  Anything the software needs from the network is downloaded before the event.
  The display runs from a serial cable or a fixture.
- Auth, settings, onboarding, responsive breakpoints on the live view, migrations, Docker, retry logic, telemetry.
- Tests beyond the four in CI: the sync check, the serial contract parser, the fixture smoke test, and the sketch compile.

If a task seems to need one of these, say what it costs and offer the substitute from the `hackathon-build` skill's tech debt table.

## Roles and ownership

Seven roles for three people, so everyone carries two or three.
The person column is empty until the team votes, and is filled in the same commit as the meeting note that records the vote.

| Role | Person | Owns | Directory |
|---|---|---|---|
| Team lead and integrator | | `main`, the clock, the freeze, standups, the measurement run, the submission form | `RUN.md`, `pitch/submission.md` |
| Software and data | | Serial reader, CSV logger, the display with fixture replay, any dataset the sponsor challenge needs | `software/`, `data/` |
| Electronics | | Incident photoresistor, bench light sensor, flex sensor, temperature sensors, LED sun, servo power, wiring, pinout | `hardware/electronics/` |
| Firmware | | The sketch: the control law, the override button, the log line | `firmware/` |
| Mechanism | | Backbone and lamina leaf variants, the three leaf assembly, the pull wire or rigid link, the print queue at the event, the spare leaf | `hardware/leaves/` |
| Structure and rig | | The foam board bus stop frame, the LED sun mount, servo driven or fixed, the servo box, the mount points, the backup fixed roof | `hardware/frame-rig/` |
| Pitch | | Demo script, placards, Q&A bank, backup video, the spoken pitch | `pitch/` |

Hotspot files carry one named owner and are changed by nobody else.

| File | Owner | Why |
|---|---|---|
| `firmware/SERIAL_FORMAT.md` | Software and data | The contract between firmware and software. A change needs the firmware and software owners in the same conversation. |
| `hardware/frame-rig/linkage.md` | Structure and rig | The dimensioned interface between leaves and frame. The mechanism owner signs it. |
| `hardware/electronics/pinout.md` | Electronics | Pins, sensor positions, power. The structure owner signs the sensor positions. |
| `RUN.md` | Team lead and integrator | The status the README renders from. |
| `project-brief.md` | nobody | Read only. Scope changes go through a meeting note. |

## Seams

Directory ownership prevents merge conflicts.
It does not prevent a servo horn that does not fit the leaf bar at hour three.
Each seam has one written contract, one owner, and one signer, and the contract is agreed before either side builds.

| Seam | Between | Contract |
|---|---|---|
| Serial log | firmware and software | `firmware/SERIAL_FORMAT.md` |
| Linkage | leaves and frame | `hardware/frame-rig/linkage.md` |
| Sensor aperture | electronics and frame | `hardware/electronics/pinout.md` |
| Line of sight | rig and electronics | The LED sun mount and the photoresistor position, photographed, in `hardware/frame-rig/` |

The lanes meet twice at the event: hour nine when the photoresistor is tested against the LED sun on the rig, and hour twelve when everything is mounted into the rig.
Nobody waits on anybody before those points.

## Git during the build

- Everyone commits straight to `main` inside their own directory, after `git pull --rebase`.
- Anything outside your directory goes through its owner, by asking them or handing them a patch.
- The team lead owns `main` for anything that touches two directories at once, and runs the demo path after every such merge.
- Commit every time something works that did not work before, and before anything risky.
- Never commit agent output nobody has run locally.
  Read anything over about 300 lines before committing it.
- No force push to `main`, no destructive git commands without a human saying so.
- CI runs the sync check, the unit tests, and the sketch compile on every push.
  A red `main` is the first thing fixed.

## Offline rule

The display must run from `software/fixtures/` with no serial port and no network.
Any dataset the sponsor challenge needs is downloaded into `data/raw/` before Saturday and the small processed CSVs are committed.
Turn the Wi-Fi off and the demo still runs.
That is a pass or fail gate, not a preference.

## The downgrade ladder

A feature that is not working is demoted, never debated.
Real, then stubbed, then fixture, then cut.
Triggers, from the `hackathon-build` skill's scope creep brake: a feature over thirty minutes is deferred, and a bug over thirty minutes means walk away and come back.

The ladder for the control board, decided before the event:

1. The control loop on the Arduino UNO Q.
2. The control loop on the Uno R3, the Arduino challenge dropped, one line in `RUN.md`.
3. Fixture replay on the laptop only, the leaves still.
4. The backup video.

Gate at hour one: the sketch compiles for the UNO Q with the core already installed, and `analogRead` and the Servo library work on it.
If not, move to rung two and say so.

## Standups and decisions

- Standups at 13:00, 15:00, 17:00, 19:00, 21:00, and 23:00 on Saturday, then 07:30 and 09:30 on Sunday.
  Ten minutes, three questions each: finished, next, blocked.
- Every decision goes into the decisions log in `RUN.md` with the clock time.
  If it is not there, it did not happen.
- Blocker ladder: fifteen minutes alone, then the owner of the neighbouring directory, then the team lead, then a five minute huddle where someone leaves owning the fix.
- Away from the table for more than thirty minutes, say so in Discord.
- Tie breaks: mechanism to the mechanism owner, pitch to the pitch owner, anything technical or anything touching the clock to the team lead.
- The venue closes 01:00 to 07:00 on Sunday.
  The freeze is 01:00 and nobody argues with it.

## Clock

| Phase | Window | The only goal |
|---|---|---|
| Build | 11:00 Saturday to 01:00 Sunday | The demo path runs end to end |
| Freeze | 01:00 Sunday | Nothing new after this line |
| Harden | 07:00 to 09:00 Sunday | It cannot fail on stage |
| Pitch | 09:00 to 11:00 Sunday | Script, video, submission |

Judging starts at 12:00 Sunday.
The print queue closes Saturday night, so every printed part is submitted by Saturday afternoon.
