# Planning

The team's working copy of the plan for HackMIT 2026.
The project is a simulated smart louvre roof for a Central Florida grower with three crops under one shade house roof.
It is the simulation alone: nothing physical is built.

## What this folder is, and is not

- It is Markdown only, and it holds no project code.
  The HackMIT rules require all project code to be written during the hacking period, 11:00 Saturday 2026-09-19 to 11:00 Sunday.
- It began as a copy of files from the team's public planning repo, https://github.com/andomo3/hack-mit, brought here on Saturday in several dated commits.
  From Saturday evening this copy is the one the team works from, and it is changed only by abba, never by a build agent.
- The planning repo also holds a labelled throwaway prototype, written before the event for a different idea, which the team set aside on Saturday.
  None of it was copied here, no file in this repo is derived from it, and it stays in the planning repo where anyone can compare.
- It holds no rules for a build agent.
  The only rules file is `../AGENTS.md` at the repo root, and the live board is `../CHECKLIST.md`.

## Read these

| Read | For |
|---|---|
| `../CHECKLIST.md`, at the repo root | The live board: who owns what, the order, the interfaces, the clock |
| `plans/plan-d-louvre-roof.md` | The plan: what is ours and what is not, the MVP, the packages, the demo beat by beat, the risks |
| `project-brief.md` | The plan on one page, with the cut list and the cuts by the clock |
| `RUN.md` | The status, and every decision made during the event, each with its reason |
| `plans/gates.md` | What every package is checked against, after every package and at four milestones |
| `plans/packages/README.md` | The package index, and the prompt for handing a package to a build agent |
| `plans/packages/G1-gate-runner.md`, `S1-solar-2023.md`, `H1-zones-light-rain-soil.md`, `H2-page.md`, `H3-result-card.md` | The five work packages, each with expected values computed from the real data before any code existed |
| `software/` | What the software is, the brief for the page, and the prompt for its mockup |
| `data/` | The two datasets, the processed files, and where each crop figure comes from |
| `pitch/` | The story, the scripts, the storyboard, the question bank, the cards, the checklists, the video plan, and the submission text |
| `plans/pitch-plan-d.md` | How the pitch, the screen's polish, the README, and the table are prepared, and the words the team never says |
| `playbook.md` | The HackMIT playbook, whole, for reference |
| `docs/STATE.md` | The index of the idea and the research, and the standing decisions |
| `docs/ideas/flectofin-greenhouse-roof.md` | The idea and the decisions behind it |
| `docs/research/flectofin-greenhouse-roof/market-and-differentiation.md` | What already exists, the objections, and the sources |
| `docs/research/flectofin-greenhouse-roof/fin-patent-and-credit.md` | Whose fin it is, the patent and its inventors, and how the team credits it |

## What was left behind, on purpose

- All code: the prototype, its tests, and the planning repo's own tooling scripts.
- Two helper scripts that belong to the `hackathon-pitch` and `hackathon-readme` skills, a word counter and a README checker, because they were written before the event.
  The skills mention them, and they can be written again here.
- The ideas the team did not choose, and the pasted source documents and images.

## The playbook

`playbook.md` is the team's HackMIT playbook, the file every `hackathon-*` skill under `.claude/skills/` was built from.
It carries no author's name, and it is kept here as the team's reference, not as the team's writing.
