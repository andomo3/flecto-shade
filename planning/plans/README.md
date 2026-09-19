# Plans: live or simulated

Written 2026-09-19, on the first day of the event, because some hardware could not be sourced.
Two complete plans for the MVP, the demo, and the presentation, and one shared core that both of them need.
This directory is planning, and no file here is code.

| File | When it applies |
|---|---|
| `plan-a-live.md` | The materials are in hand, and the judge watches a physical roof move |
| `plan-b-simulated.md` | They are not, and the judge watches a simulated roof built from the team's CAD and real solar data |

`../project-brief.md` is read only during hacking and still describes Plan A.
Where Plan B departs from the brief, this directory is the record and `../docs/meetings/2026-09-19.md` carries the decision.

## The idea that makes this cheap: one contract, four sources

The app never knows where its readings come from.
It reads lines in the format of `../firmware/SERIAL_FORMAT.md`, version 2, from a source.
Plan A's source is the board over USB.
Plan B's source is a simulator that prints the same eleven fields.
So the page, the state, the fast forward day, the recorder, the fixtures, and the result card are identical in both plans, and they are built first.

```text
day.py (real Houston day) --> L and A commands --> [ source ] --> v2 lines --> state --> page
                                                     |
                     fixture | fake | serial (Plan A) | sim (Plan B)
```

## The shared core, built first whichever plan wins

These are steps 1 to 7 of `../software/CLAUDE.md` and steps 1 to 6 of `../data/CLAUDE.md`, unchanged.
Each work package ends in a command that exits 0, and nothing starts before the previous check passes.

| ID | Build | Done when |
|---|---|---|
| C1 | `contract.py`: parse one v2 line into a header, a reading, or nothing, and build the `L`, `A`, `S`, `O`, `P` commands | `pytest tests/test_contract.py` passes, reading its samples out of the contract text and rejecting a list of garbage lines |
| C2 | `sources.py`: one interface, readings out and commands in, with `FixtureSource` and `FakeSource` | `pytest tests/test_sources.py` passes: the fixture source yields the file's readings in order, paced by `t_ms`, and loops |
| C3 | `fixtures/synthetic-day.csv`: one hand made fast forward day | It parses with C1, inside the C2 test |
| C4 | `state.py`: the two percentages, leaf state from `angle`, which sensors are fitted, running averages for bent and resting, cycle count, whether the day has finished | `pytest tests/test_state.py` passes on five or six hand written readings, including empty fields that must show as "not fitted" |
| C5 | `app.py` and `__main__.py`: FastAPI with `/`, `/events` as server sent events, `/health`, and POST `/play`, `/pause`, `/reset`, `/led`, `/sun`, `/replay-mode` | `python -m canopy serve --source fixture` starts with the network off, `curl localhost:8000/health` returns 200, and `/events` streams |
| C6 | `data/` pipeline: PVGIS Houston file to `processed/day-houston.csv`, 600 rows, the sunniest day, sun position from `pvlib` | The script runs with the network off, the sun is highest near local noon, and duty is 0 at night |
| C7 | `day.py`: plays the day to the source as `L` and `A` ten times a second | Against `FakeSource`, the leaves bend after sunrise and rest after sunset, in a test |
| C8 | `static/index.html`: the page, ported by hand from the mockup, twelve states | Every state in `../software/mockup-prompt.md` renders from a fixture, and a person passes the 3 second test at a metre |
| C9 | `recorder.py`: every line from any source written unchanged to `fixtures/` | A recorded run replays through `FixtureSource` and gives the same result card |

The stack is fixed by `../software/CLAUDE.md`: Python 3.13, FastAPI, uvicorn, one HTML file with plain CSS and vanilla JavaScript, no build step, no CDN, no network at run time.

## The gate

Decided once, out loud, at **17:00 Saturday, venue hour 6**, and not reopened after.
[The team may move this hour, and must not remove it.]

Plan A needs all five in hand at the gate:

1. One leaf that bends and returns, by servo or by hand.
2. A board that runs a sketch and prints over USB.
3. Two light sensors, or one sensor and a confirmed second by hour 9.
4. A light to be the sun: the LED, a desk lamp, or a phone torch.
5. Something to hold them: foam board and tape are enough.

| At the gate | Go to |
|---|---|
| All five | Plan A |
| A leaf, but no board or no sensors | Plan B, with the leaf on the table as the object the judge bends by hand |
| No leaf at all | Plan B, with the CAD render on screen and a printed or paper leaf if anything can be cut |

Until the gate, the engineers chase parts and leaf variants, and the software builds the shared core, so no hour is spent on a plan that loses.
If Plan A is chosen and the simulator is wanted anyway, it is a stretch after Plan A's core loop is green, because it gives the adaptive against fixed number for free.

## Decided on 2026-09-19: Plan B, with the real leaf driven by the simulation

Abba decided, ahead of the 17:00 gate: the team can demo the flapping leaf and nothing else, so the whole setup is simulated, reaction included.
Plan B applies, with packages B13 and B14 added so that the leaf on the table bends at the same moment as the leaves on the screen.
Plan A and the third option below are kept as the record of what was considered, and neither is built.
The build agent's order is R1, then G1 the gate runner in `gates.md`, then C6, then the shared core, then B1 to B9 with B13 and B14, then the stretch, with V1 to V3 beside them if a second session exists.

## The inventory reported on 2026-09-19, and a third option, not taken

Abba reported what the team can lay hands on: a microcontroller, a servo or small motor, a photoresistor, an RGB LED, possibly a phone camera, sheet plastic or card, and access to a printer or a laser cutter.
Against the five gate items that is four and a half: a board, a leaf that can be cut from sheet, a light, something to hold them, and one light sensor where the number needs two.

So a third option sits between the plans, proposed by the planner and not yet decided by the team.

**Plan A-lite: the roof is real, the number is simulated.**

- Physical, on the table: the board, the one photoresistor as the incident sensor, the servo, and leaves laser cut from sheet plastic, which is already the hour 4 pivot in `../project-brief.md`.
  The threshold runs on the board, so the hand over the sensor still works, and it is still the proof that nothing is scripted.
- Simulated, on the screen: the light reaching the bench, from the shade table in `plan-b-simulated.md`, because there is no second sensor to measure it.
  The `bench` field stays empty on the wire, exactly as the contract allows, and the page shows the simulated figure beside the words "simulated from our CAD", never in the measured bar.
- The number said out loud is two numbers, kept apart: "N of N light triggered cycles, measured on this table", which the brief already names as the backup number, and the simulated day and year figures, said as simulated.
- The Arduino challenge stays in reach, because the board reads the physical world.

What it needs settled first:

- How many photoresistors there are. With two, this is simply Plan A.
- Whether the RGB LED is bright enough to be the sun.
  A single small LED is weak against room light, so the rig is a shrouded card box with the LED a few centimetres from the sensor, or the sun is a phone torch held by the speaker, which the cut list rejected as a hand swung lamp and which returns only as a fallback.
- Which board it is, because the UNO Q decides the Arduino challenge and the firmware's step 0.
- Whether the sheet plastic buckles cleanly as a lamina, which is the engineers' hour 0 to 2 test and nobody else's call.

The build order does not change: the shared core first, then the firmware packages A1 to A5 from `plan-a-live.md`, then B1 to B4 and B6 from `plan-b-simulated.md` for the number.
The 3D render in `packages/R1-simulation-research.md` becomes optional, because the physical roof is the thing the judge watches.

## What differs, on one page

| | Plan A, live | Plan B, simulated |
|---|---|---|
| The source | `SerialSource`, the board | `SimSource`, a virtual board |
| What moves | Three physical leaves | The leaves in the scene on screen, posed from the CAD |
| The sun | An LED, dimmed by the data | The same data, as a sun position and an irradiance |
| The number | Bench light, bent against resting, measured on the table | Bench light, adaptive against resting against a fixed slab, over a real day and a typical year, modelled |
| The proof it is not a script | A hand over the photoresistor | The judge drags a cloud over the sun, or covers the laptop camera, and the leaves respond |
| The honesty line | "Measured today on this table" | "Simulated from our CAD and public solar data. Nothing here was measured." |
| Challenges in reach | Arduino Touch Grass, Voloridge, the track | Voloridge, the track, [the Cognition challenge, once its text is read]. Arduino is dropped |
| The story | Rosa, unchanged | Rosa, unchanged |

## Rules for the build agent

Devin, from Cognition, is a sponsor of the event and the team is allowed to have it write the code.
Abba plans the code, and the agent builds from these files.

- The agent writes only into the event repo, which started empty at 11:00 Saturday.
- The agent never reads from or copies the labelled prototypes in this repo: `firmware/canopy/`, `firmware/host_test/`, and `software/canopy/`.
  Exclude those three directories from anything exported to it.
- The specification is this directory, the local memory files `../software/CLAUDE.md`, `../firmware/CLAUDE.md`, `../data/CLAUDE.md`, the contract `../firmware/SERIAL_FORMAT.md`, and `../software/ui-brief.md`.
- One work package per task.
  Each is handed over with its ID, its "done when" command, the files it may touch, and the files it must not.
- A package is done only when its command exits 0 and a person has run the behaviour once.
  Generated code is untrusted until it has been run and read.
- One commit per package, with the package ID in the message, so any package can be reverted alone.
- Every dependency the agent adds is checked to exist and to be needed before it is installed.
- If a package fails its check twice, stop and reframe it rather than patching further.
- No secrets, tokens, or keys in any prompt, commit, or log.
- The submission cites the agent as a tool, alongside the open source libraries, because the rules require citation.
