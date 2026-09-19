# Plans

There is one plan: `plan-d-louvre-roof.md`, the simulated smart louvre roof over three crops.
It was chosen at about 16:45 on Saturday 2026-09-19 and frozen at the 17:00 standup.
After the freeze a change is a cut, never a pivot.
This directory is planning, and no file here is code.

The project is the simulation alone.
Nothing physical is built, and the printed fin first planned for display was cut on Saturday evening.

## What is here

| File | What it is for |
|---|---|
| `plan-d-louvre-roof.md` | The plan: what is ours and what is not, the MVP, the packages in order, the ninety second demo beat by beat, the presentation, the risks |
| `gates.md` | What every package is checked against: fourteen fast gates after every package, four milestones walked by a person, and the demo gate beat by beat |
| `pitch-plan-d.md` | How to prepare the pitch, the screen's polish, the README, and the table, and the words the team never says |
| `packages/README.md` | The package index, and the prompt for handing a package to a build agent |
| `packages/G1-gate-runner.md`, `S1-solar-2023.md`, `H1-zones-light-rain-soil.md`, `H2-page.md`, `H3-result-card.md` | The five work packages, each with expected values computed from the real data before any code existed |

## The order

```text
Abba:     G1 ------------------> H2 ----------> H3 ----> pitch figures
Ameya:    S1 ------> H1 ----------^
```

G1 and S1 start at once and depend on nothing.
H1 needs S1 merged, H2 needs H1 merged, and H3 needs H2.
The simulation comes before the page on purpose, so there is always something to show.
The live state, with who has claimed what and the clock, is `../../CHECKLIST.md`.

`data/roof-layout.json`, package K2, is optional.
It only changes how many fins the page draws over each bed, and H2 draws a default grid, with the words "default layout", when the file is absent.

## Rules for the build agent

There is one rules file, `../../AGENTS.md` at the repo root, and one live board, `../../CHECKLIST.md`.
No file under `planning/` adds to them or overrides them.

In short, and the root file is the authority:

- Devin, from Cognition, is a sponsor of the event, and the team is allowed to have it write the code.
  Abba plans the code, and each person's agent builds that person's packages.
- One work package per task, handed over with its ID, the command that must exit 0, the files it may create or change, and the files it must not touch.
- A package is done only when its command exits 0 and a person has run the behaviour once.
- The expected values in a package were computed from the real data before any code existed.
  If one does not match, stop and report it, and never edit the value.
- If a package fails its check twice, stop and say so rather than patching further.
- All code is written during the event, fresh, from these specifications, and nothing is copied from the planning repo.
- The submission cites every library, every dataset, every source of a crop figure, and every AI tool.

## What was set aside

Three earlier plans from the same Saturday are under `../archive/`, kept as the record, and nothing is built from them.

- Plan A and Plan B, the bus stop canopy, live and simulated, with their shared core, packages C1 to C9, and the serial contract.
- The Flectofin leaf design tool.
- Packages C6, R1, V, and F1, which served those plans.

Why each was set aside is in `../docs/meetings/2026-09-19.md`.
