# flecto-stop: rules for anyone, human or agent, working in this repo

This is the repo the team submits to HackMIT 2026.

The project, since about 16:45 on Saturday 2026-09-19: a simulated smart louvre roof for a grower with three crops under one shade roof.
The roof is made of many small hingeless fins, grouped into zones, and each zone gets its own light and lets the rain through only when its soil is dry.
Everything is simulated, from a real year of Central Florida weather near Apopka, and the one physical thing is a printed fin on the table.
The structure is a shade house, which the team calls a greenhouse in plain speech, and the page says shade house.

The plan is `planning/plans/plan-d-louvre-roof.md`.
Earlier the same day the team planned a bus stop canopy and then a leaf design tool, and those files are still under `planning/` as the record.
Build nothing from them.

Status: planning imported, nothing built yet.
Do not start until abba hands over a work package.

## The rule that outranks every other

All project code is written between 11:00 Saturday 2026-09-19 and 11:00 Sunday 2026-09-20.

- Write every line of code here, fresh, from the specifications under `planning/`.
- Never copy code from the planning repo, https://github.com/andomo3/hack-mit.
  Its `firmware/canopy/`, `firmware/host_test/`, `software/canopy/`, and `tests/` directories are a labelled pre-event prototype and are off limits, to read or to copy.
- `planning/` is Markdown only and is a snapshot.
  Do not edit it and do not put code in it.
- Cite every open source library, every dataset, every source of a crop figure, and every AI tool in the submission, because the rules require it.

## Read first

1. `planning/plans/plan-d-louvre-roof.md`, the plan: what is ours and what is not, the MVP, the packages in order, the demo, and the risks.
2. `planning/plans/gates.md`, what every package is checked against.
3. `planning/plans/packages/README.md`, the package index and the handoff prompt.
4. `planning/docs/research/flectofin-greenhouse-roof/market-and-differentiation.md`, what already exists, and the words the team never says.

## Order of work

G1 the gate runner, then S1 the 2023 sun for the Apopka area, then H1 the zones and the rules, then H2 the page, then H3 the result card.
Each has a file under `planning/plans/packages/`, or will before it is handed over.
These packages under the same folder belong to plans that were set aside, and are never built: R1, C6, V1 to V4, and F1.

## Boundaries that hold whatever else changes

- The roof follows written, deterministic rules per zone. No language model and no learned model sits in the loop.
- The fins react to how much light has arrived, to rain, and to the soil. They never track the sun's position.
- Nothing is measured. Every figure on every screen and in every file says simulated or modelled.
- The fin is not ours. It is ITKE's Flectofin, patented as EP2320015, and the page credits it.
- The control logic, watering by the sun's energy and holding a daily light target, is standard practice in greenhouse computers, and nothing here claims otherwise.
- Never write or display: "first", "measured", "maintenance free", "weatherproof", or any figure for cost, yield, energy, or water saved.

## How work is handed over

Abba plans the code and the build agent writes it.
Every task is one work package, handed over with four things:

- the package ID, for example S1,
- the command that must exit 0 for it to be done,
- the files it may create or change,
- the files it must not touch.

A package is done only when its command exits 0 and a person has run the behaviour once.
Generated code is untrusted until it has been run and read.
The expected values in a package were computed from the real data by a planner, before any code existed.
If one does not match, stop and report it, and never edit the value to make a test pass.
If a package fails its check twice, stop and say so rather than patching further.

## The demo, the pitch, and the checklists are the definition of done

Code that passes its own tests and breaks the demo is not done.
`planning/plans/gates.md` turns the demo, the pitch, the honesty rules, and the playbook's checklists into gates, and every package is checked against them, every time.

- Before writing code, say in three lines which beat of the demo, which claim of the pitch, and which gate the package serves.
  If it serves none, stop and say so, because it is probably scope creep.
- After the package's own check passes, run `python tools/gates.py --package ID --allowed "files" --append`, and end the reply with the gate report.
- A gate that passed before and fails now is a regression, and it is fixed before anything else is touched.
- If the same gate fails twice in a row, stop and report.
- A gate that does not apply yet is reported as NOT YET, never as PASS, and never left out.
- The fast gates are checked by the command, and the milestone gates, M1 to M4, by a person with the agent.
  A green command never means "the demo works".
- Always answer the report's last line: anything in the demo, the pitch, or a checklist that this package makes harder.

`GATES.md` at the root is the ledger: one dated section per package, written by the command.

## Layout, once building starts

| Directory | Becomes |
|---|---|
| `tools/` | The gate runner and its tests |
| `data/raw/` | Downloaded public datasets, gitignored, copied in by a person with the sha256 checked |
| `data/` | The build scripts, `crops.csv`, and `processed/`, which is committed |
| `software/` | The simulation, the page, `requirements.txt`, and `tests/` |
| `pitch/` | The final scripts, cards, and submission text, written once the simulation has produced real figures |

## Constraints that bind every package

- Python 3.13, with `pandas==2.2.3`, `numpy==2.2.3`, and `pytest==9.0.2`, in one virtual environment with a pinned `requirements.txt`.
- Add no other dependency unless the package names it. Check that it exists and is needed first.
- The page is plain HTML, CSS, and vanilla JavaScript: no React, no Node, no build step, no CDN, no web fonts fetched at run time, and no web framework unless a package asks for one.
- Everything builds and runs with no network.
- Every constant a package marks ASSUMED is a named constant in the code and a row in the README's table of assumptions.
- No secrets, tokens, keys, or personal data in any file, commit, prompt, or log.

## Commits

- One commit per work package, with the package ID in the message.
- Small and atomic, and commit whenever something works that did not before.
- No co-author trailers.
- Never commit `data/raw/`, a virtual environment, or a `.env` file.

## Writing rules

One sentence per line in Markdown.
Plain dashes, never an em dash.

## Skills

The `hackathon-*` skills under `.claude/skills/` are the team's playbook: build against the clock, stack, testing, UI polish, prompts, pitch, README, and team.
Two of them mention a helper script that was left in the planning repo on purpose, see `planning/README.md`.
