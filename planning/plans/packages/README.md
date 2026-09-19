# Work packages for the build agent

One file per package, written by planning agents that checked every input against the real data before writing a word.
Each package is a specification, not code, and it is handed to the build agent one at a time.
The rules for the agent are `AGENTS.md` and `CHECKLIST.md` at the event repo's root, and nothing else.
`../README.md` in this folder is the record of the bus stop plans, and no package is built from it.

## The packages

The current plan is `../plan-d-louvre-roof.md`, the simulated smart louvre roof, chosen on 2026-09-19 at about 16:45.

| ID | File | What | Status |
|---|---|---|---|
| G1 | `G1-gate-runner.md` | One command that runs every fast gate in `../gates.md` and prints the gate report | ready, first |
| S1 | `S1-solar-2023.md` | The sun for the Apopka area of Central Florida in 2023 from NASA POWER, the same year as the rain, one row an hour, no new dependency | ready, second |
| H1 | `H1-zones-light-rain-soil.md` | The crops, the rain, the light, the soil bucket, the nine rules, and the year's summary | ready, third, and it needs S1's file. Central Florida, three crops, the demo day of 3 June 2023 |
| H2 | `H2-page.md` | The page that plays 3 June 2023 in a minute from H1's output, with each zone's reason in words | ready, and it needs H1 and K2 |
| H3 | `H3-result-card.md` | The result card, the year by month, and `headline.json`, the one file every spoken figure comes from | ready, and it needs H2 |
| K1, K2 | specified in `CHECKLIST.md` at the event repo's root | The display fin, and the roof layout the page draws | ready, for the CAD modeller |

Set aside with the plans they served, and kept as the record: `C6-data-pipeline.md`, `R1-simulation-research.md`, `V-metro-exposure.md`, and `F1-farmworker-shade-drift.md`.
None of them is handed to the build agent.

## Where the raw data is

Downloaded on 2026-09-19 into `hack-mit/data/raw/`, which is gitignored.
For the current plan the two files are `nasa-power/power-hourly-orlando-executive-2023.csv` and `isd-rain/72205312841-2023.csv`.
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
- You are one of three agents in this repo, one per teammate. Read CHECKLIST.md first. Work
  only on your person's packages, in your person's directories, on the branch pkg/[ID]. Edit
  only your person's section of CHECKLIST.md. Never merge: the integrator does.
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
