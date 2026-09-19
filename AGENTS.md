# flecto-stop: rules for anyone, human or agent, working in this repo

This is the repo the team submits to HackMIT 2026.
It is a tabletop bus stop roof made of three hingeless leaves that bend into shade on their own when a light sensor sees the sun, with a laptop app that plays one real Houston day and shows the light reaching the bench.

Status on 2026-09-19: planning context imported, nothing built yet.
Do not start building until abba hands over a work package.

## The rule that outranks every other

All project code is written between 11:00 Saturday 2026-09-19 and 11:00 Sunday 2026-09-20.

- Write every line of code here, fresh, from the specifications under `planning/`.
- Never copy code from the planning repo, https://github.com/andomo3/hack-mit.
  Its `firmware/canopy/`, `firmware/host_test/`, `software/canopy/`, and `tests/` directories are a labelled pre-event prototype and are off limits, to read or to copy.
- `planning/` is Markdown only and is a frozen snapshot.
  Do not edit it and do not put code in it.
- Cite every open source library, every dataset, and every AI tool in the submission, because the rules require it.

## Read first

1. `planning/README.md`, what the planning record is and where to start in it.
2. `planning/plans/README.md`, the two plans, the shared core, the gate, and the rules for the build agent.
3. `planning/docs/meetings/2026-09-19.md`, the newest decisions.

## Which plan

Two plans exist because some hardware could not be sourced.
Plan A is the live demo and Plan B is the simulated one.
Decision: Plan B, made by abba on Saturday 2026-09-19, in the afternoon and ahead of the 17:00 gate.
Reason: the team can demo the flapping leaf and nothing else, so the stop, the sun, the sensing, and the reaction are all simulated.
The one real thing on the table is the leaf on its servo, and the simulation drives it through the contract's `S` command, packages B13 and B14 in `planning/plans/plan-b-simulated.md`.
Plan A is not built.

Two boundaries that hold whatever is simulated:

- The leaves react to how bright the light is, through a threshold, and have two states.
  Never build a roof that tracks the sun's position, because that is not the roof the team designed.
- The leaf's buckling is never simulated live.
  The simulation is light, geometry, and the control law, and the leaf's shape comes from one of the three routes in `planning/plans/packages/R1-simulation-research.md`.

Order of work: R1, then C6, then the shared core C1 to C9, then B1 to B9 with B13 and B14, then the stretch, with V1 to V3 beside them if a second session exists.

## How work is handed over

Abba plans the code and the build agent writes it.
Every task is one work package from `planning/plans/`, handed over with four things:

- the package ID, for example C1,
- the command that must exit 0 for it to be done,
- the files it may create or change,
- the files it must not touch.

A package is done only when its command exits 0 and a person has run the behaviour once.
Generated code is untrusted until it has been run and read.
If a package fails its check twice, stop and say so rather than patching further.

## Layout, once building starts

| Directory | Becomes | Specification |
|---|---|---|
| `software/` | The Python package `canopy`, its fixtures, and its tests | `planning/software/CLAUDE.md` |
| `firmware/` | One Arduino sketch and `config.h`, Plan A only | `planning/firmware/CLAUDE.md` and `planning/firmware/SERIAL_FORMAT.md` |
| `data/` | `raw/`, gitignored, and `processed/`, committed, with one script that rebuilds it offline | `planning/data/CLAUDE.md` |
| `software/canopy/sim/` | The shade simulation, Plan B only | `planning/plans/plan-b-simulated.md` |
| `hardware/` | Photographs, the pinout, and milestone exports | `planning/hardware/` |
| `pitch/` | The final scripts, cards, and submission text, copied out of `planning/pitch/` only when they are edited for the real numbers | `planning/pitch/` |

## Constraints that bind every package

- Python 3.13, FastAPI, uvicorn, and pyserial, in one virtual environment with a pinned `requirements.txt`.
- The page is one HTML file with plain CSS and vanilla JavaScript: no React, no Node, no build step, no CDN, no web fonts fetched at run time.
- Everything runs with no network and no serial port: `python -m canopy serve --source fixture` must always work.
- The serial contract in `planning/firmware/SERIAL_FORMAT.md`, version 2, is the seam.
  Every source, real or simulated, speaks it, and nobody changes it alone.
- A sensor that is not fitted shows "not fitted", never zero.
- The data moves the sun, and only the light sensor moves the leaves.
- Check that every dependency exists and is needed before adding it.
- No secrets, tokens, keys, or personal data in any file, commit, prompt, or log.

## Honesty rules

- Only what was measured on the table during the event is called measured.
- Anything from a dataset or a simulation is called modelled or simulated, on the screen, on the cards, and out loud.
- A light reading is never turned into a claim about temperature, health, or lives.
- If replay mode or simulation mode is on, a banner says so in words.

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
