# Work packages for the build agent

One file per package, written by planning agents that checked every input against the real data before writing a word.
Each package is a specification, not code, and it is handed to the build agent one at a time.
The rules for the agent are in `../README.md`, and the rules for the event repo are in its own `AGENTS.md`.

## The packages

| ID | File | What | Needs | Status |
|---|---|---|---|---|
| R1 | `R1-simulation-research.md` | Research, time boxed to 120 minutes: how to simulate and render the stop, 2D or 3D, where the geometry comes from, which of three routes gives the leaf its shape, and what not to build | The name of the engineers' CAD tool | spec ready, and it is the build agent's first task |
| G1 | `G1-gate-runner.md` | One command that runs every fast gate in `../gates.md` and prints the gate report, built before the features so every later package is checked the same way | Nothing | spec ready, and it is the second task |
| C6 | `C6-data-pipeline.md` | PVGIS Houston typical year to the 600 row demo day and the 8,760 hour year, sun position from `pvlib` | The raw file, already downloaded | spec ready |
| V1 to V4 | `V-metro-exposure.md` | The Voloridge analysis: rank Houston's unsheltered stops by modelled rider sun exposure | The raw METRO files, already downloaded, and C6's year file for V2 | spec ready, and outside public data is confirmed to count |
| F1 | `F1-farmworker-shade-drift.md` | How far a fixed rest canopy's shadow drifts during the hours California law requires shade | The raw NOAA files, already downloaded | spec ready and parked: its headline swings with the canopy size the team assumes, so it waits until V1 to V3 are green |

Order of handover: R1 first, because it decides what Plan B's scene is, and it is research, so it blocks nothing else.
Then G1, the gate runner, so that every package after it ends in the same checked report.
Then C6, because V2 and Plan B both read its year file.
V1 needs nothing from C6, so it can run beside it.
If the build agent can run two sessions at once, the app's shared core and V1 to V3 run side by side, in separate branches that touch separate directories.
If it can run only one, the shared core comes first, because every judge scores the demo and only one sponsor scores the analysis.
F1 is a side card and comes last.

C1 to C5 and C7 to C9, the app's shared core, are specified in `../README.md` and in `../../software/CLAUDE.md`, and get their own files here when they are handed over.

## Where the raw data is

Downloaded on 2026-09-19 into `hack-mit/data/raw/`, which is gitignored.
A downloaded public dataset is not code, so it is copied into `flecto-stop/data/raw/`, also gitignored, as the first step of the package that uses it.
Each package gives the byte size and the sha256 of its raw file, so the copy can be checked.

## The shape of every package file

1. ID and title.
2. Goal, in two lines.
3. Inputs, with facts verified from the real file.
4. Outputs, with the exact schema and an example row.
5. Dependencies, each confirmed to exist, with the version to pin.
6. Steps, numbered, each ending in a check.
7. Acceptance: the commands that must exit 0 with the network off, and the test cases with their expected values.
8. Files the agent may create, and files it must not touch.
9. Honesty labels for every output.
10. Provenance, licence, and citation lines.
11. Open questions for a person, which are answered before the package is handed over.
12. Estimated minutes.

The expected values in section 7 were computed from the real data by the planning agent.
They are what makes the package machine checkable: the build agent cannot pass by writing a test that agrees with its own mistake.

## The handoff prompt

Paste this to the build agent, with the brackets filled, one package at a time.

```text
CONTEXT
You are working in the repo flecto-stop, the HackMIT 2026 submission. Read AGENTS.md at
the root first and follow it. All code is written fresh. Never read or copy code from the
planning repo github.com/andomo3/hack-mit: its firmware/canopy, firmware/host_test,
software/canopy, and tests directories are an off-limits pre-event prototype.

TASK
Implement work package [ID], specified in planning/plans/packages/[FILE].md. Implement
that package and nothing else. Its open questions are answered here: [ANSWERS].

CONSTRAINTS
- Create or change only the files the package lists under "may create". Do not touch
  planning/ or anything the package lists under "must not touch".
- Pin exactly the dependency versions the package gives. Add no other dependency without
  asking. Confirm each one exists before installing it.
- Write the tests the package lists, with the expected values it gives. Do not change an
  expected value to make a test pass: if a value looks wrong, stop and report it.
- Everything must run with the network off.
- No secrets, keys, or personal data anywhere.
- Read planning/plans/gates.md before you start. The demo, the pitch, and the checklists in
  it are the definition of done. Before you write code, state in three lines which storyboard
  beat, which script sentence, and which gate this package serves. If it serves none, stop
  and say so.
- When the package's own check passes, run python tools/gates.py --package [ID] --allowed
  "[FILES]" --append. A gate that passed before and fails now is fixed before anything else.
  If the same gate fails twice, stop and report.

FORMAT
Work in one branch named pkg/[ID]. When done, reply with: the commands you ran and their
exit codes, the full pytest output, the list of files created, anything in the package you
could not satisfy, and any expected value that did not match, with what you got instead.
End with the gate report from planning/plans/gates.md, filled in, including its last line:
anything in the demo, the pitch, or a checklist that this package makes harder.
One commit, message starting "[ID]:". Do not merge.
```

## After the agent reports

A person runs the acceptance commands once, reads the diff, and only then merges.
A mismatch in an expected value is a finding, not a nuisance: either the package or the code is wrong, and it is settled before the merge.
If a package fails its check twice, it is reframed here, in the planning repo, and copied across again as a dated commit.
