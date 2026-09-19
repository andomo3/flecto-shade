# Planning record

Everything in this folder is planning, written in the team's public planning repo, https://github.com/andomo3/hack-mit, and copied here during Saturday 2026-09-19 in several dated commits.
It is here so that the three people and their build agents have the whole plan in one place, and from Saturday evening this copy is the one the team works from.

## What this folder is, and is not

- It is Markdown only.
- It holds no project code.
  The HackMIT rules require all project code to be written during the hacking period, 11:00 Saturday 2026-09-19 to 11:00 Sunday.
- The planning repo also holds a labelled throwaway prototype, written before the event for an earlier idea.
  None of it was copied here, no file in this repo is derived from it, and it stays in the planning repo where anyone can compare.
- Every line of code in this repo, outside this folder, is written after 11:00 Saturday.

## The project changed direction four times on Saturday, and this folder shows it

The team arrived planning a bus stop canopy, could not source the hardware, planned a simulated version, then a leaf design tool, and at about 16:45 settled on the current plan, a simulated smart louvre roof over crops.
The older plans are kept because they are the honest record, and because their method carried over.
Build nothing from them.

## Current: read these

| Read | For |
|---|---|
| `../CHECKLIST.md`, at the repo root | The live board: who owns what, the order, the interfaces, and the rules for three agents in one repo |
| `plans/plan-d-louvre-roof.md` | The plan: what is ours and what is not, the MVP, the packages, the demo, the risks |
| `plans/gates.md` | What every package is checked against, after every package and at four milestones |
| `plans/packages/README.md` | The package index and the prompt for handing a package to a build agent |
| `plans/packages/G1-gate-runner.md`, `S1-solar-2023.md`, `H1-zones-light-rain-soil.md`, `H2-page.md`, `H3-result-card.md` | The five work packages, each with expected values computed from the real data before any code existed |
| `plans/pitch-plan-d.md` | Preparing the pitch, the screen's polish, the README, and the table, and the words the team never says |
| `playbook.md` | The HackMIT playbook, whole, for reference when preparing the pitch, the screen, the README, and the testing |
| `docs/ideas/flectofin-greenhouse-roof.md` | The idea and the decisions behind it |
| `docs/research/flectofin-greenhouse-roof/market-and-differentiation.md` | What already exists, the objections, and the sources |
| `docs/research/flectofin-design-tool/sector-choice.md` | The fin's patent and its inventors |
| `docs/research/adaptive-bus-stop-canopy/flectofin-leaf-design-loop.md` | The fin itself: the rib and sheet dimensions, the print settings, and the beam formulas, for the display fin in package K1 |
| `docs/meetings/2026-09-19.md` | Every decision made on Saturday, in order, each with its reason |

## The record: kept, and never built from

- `project-brief.md`, `AGENTS-bus-stop-record.md`, which was `AGENTS.md` until it was renamed so that no agent loads it as rules, `RUN.md`, `plans/plan-a-live.md`, `plans/plan-b-simulated.md`, and `plans/README.md`: the bus stop canopy, live and simulated.
- `software/`, `firmware/`, `data/`, and `hardware/` in this folder: the bus stop's build directories and their local memory files.
  They say "this is the planning repo", which was true where they were written.
- `pitch/`: the bus stop's story, scripts, storyboard, question bank, cards, checklists, video plan, and submission draft, kept for their method.
- `plans/packages/C6-data-pipeline.md`, `R1-simulation-research.md`, `V-metro-exposure.md`, and `F1-farmworker-shade-drift.md`: packages for plans that were set aside.
- `docs/ideas/flectofin-design-tool.md` and the older research under `docs/research/adaptive-bus-stop-canopy/`.
- `docs/STATE.md` is the planning repo's index as it stood at the first copy, and is not kept current here.

## What was left behind, on purpose

- All code: the prototype, its tests, and the planning repo's own tooling scripts.
- Two helper scripts that belong to the `hackathon-pitch` and `hackathon-readme` skills, a word counter and a README checker, because they were written before the event.
  The skills mention them, and they can be written again here.
- The rejected ideas from before the event, and the pasted source documents and images.

## The playbook

`playbook.md` is the team's HackMIT playbook, the file every `hackathon-*` skill under `.claude/skills/` was built from.
It carries no author's name, and it is kept here as the team's reference, not as the team's writing.
