# Planning record

Everything in this folder is planning, written in the team's public planning repo, https://github.com/andomo3/hack-mit, and copied here on Saturday 2026-09-19 from commit `7285fe1`.
It is here so that the people and the build agent working in this repo have the whole plan in one place.

## What this folder is, and is not

- It is Markdown only: the brief, the two plans, the specifications, the research, the meeting notes, and the pitch.
- It holds no project code.
  The HackMIT rules require all project code to be written during the hacking period, 11:00 Saturday 2026-09-19 to 11:00 Sunday.
- The planning repo also holds a labelled throwaway prototype, written before the event to test the serial format.
  None of it was copied here, no file in this repo is derived from it, and it stays in the planning repo where anyone can compare.
- Every line of code in this repo, outside this folder, is written after 11:00 Saturday.

## How to read it

These files were written for the planning repo and still speak in its voice.
Where one says "this is the planning repo" or "nothing here is copied", it means the code, and it is describing where it was written.
Paths inside them are relative to this folder, so `../firmware/SERIAL_FORMAT.md` in `software/CLAUDE.md` means `planning/firmware/SERIAL_FORMAT.md`.
A few links point at files that were left behind on purpose, the rejected ideas and the pasted source documents, and those open in the planning repo.

This folder is a snapshot and is not edited here.
Decisions made during the build are recorded at the root of this repo, and the planning repo stays the place where plans change.

## Start here

| Read | For |
|---|---|
| `plans/README.md` | The two plans, live and simulated, the shared core both need, the gate between them, and the rules for the build agent |
| `plans/plan-a-live.md` and `plans/plan-b-simulated.md` | The MVP, the demo, and the presentation under each plan, as work packages with a check each |
| `project-brief.md` | The scope, the cut list, the pivots, and the number |
| `docs/meetings/2026-09-19.md` | The event day decisions, which are the newest and override the brief where they differ |
| `firmware/SERIAL_FORMAT.md` | The serial contract, version 2, the one seam every part of the build shares |
| `software/CLAUDE.md`, `firmware/CLAUDE.md`, `data/CLAUDE.md` | Each build directory's locked decisions and its skeleton in build order |
| `software/ui-brief.md` and `software/mockup-prompt.md` | What the screen shows, its twelve states, and the scorecard |
| `hardware/` | The engineers' plan for the leaves, the rig, and the electronics |
| `pitch/` | The story, the three scripts, the storyboard, the question bank, the placards, the checklists, the video plan, and the submission draft |
| `docs/research/adaptive-bus-stop-canopy/` | The research behind the brief, including the dataset choice and the Voloridge datasets |
| `AGENTS.md` and `RUN.md` | The team's roles and seams, and the feature table as it stood before the event |

## What was left behind, on purpose

- All code: the prototype sketch, its host test harness, the prototype parser, the tests, and the repo's own tooling scripts.
- The two helper scripts that belong to the `hackathon-pitch` and `hackathon-readme` skills, a word counter and a README checker.
  The skills mention them, and they can be rewritten here during the event if they are wanted.
- The rejected ideas and their research, and the pasted source documents and images.
- The playbook file itself.
  The skills under `.claude/skills/` carry the parts of it the team uses.
