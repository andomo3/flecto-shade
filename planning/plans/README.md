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
