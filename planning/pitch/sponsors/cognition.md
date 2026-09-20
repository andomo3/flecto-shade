# Cognition: how we used Devin

Owner: abba speaks this one.
Written 2026-09-20 from the repository, and every claim below names the pull request, file or command it came from.

## 1. What they ask for

[GAP. The challenge text is not public: the day-of prizes page needs a login, and the planner would not write a judging criterion from memory.
abba pastes the text here, and the sections below are then checked against it rather than assumed to fit.]

What is known without it: Cognition sponsors the event, and the team is allowed to have Devin write code.
Nothing below depends on the wording of the challenge, because it is all an account of what actually happened.

## 2. Our one sentence

"We did not use Devin to write code faster.
We used it to find out whether a specification was good enough to be built from, and four of its seven pull requests tell us more than the three that merged."

## 3. How we attacked it

**We wrote the answer before we wrote the prompt.**
Every work package in `planning/plans/packages/` carries its expected values, computed from the real data, before any code existed.
`H1-zones-light-rain-soil.md` holds the year's expected figures, and `S1-solar-2023.md` labels every value VERIFIED, ASSUMED or RECALLED.
The point is that an agent cannot pass a test by agreeing with its own mistake, because the number it has to hit was fixed by a person reading a source first.

**The specification was the unit of work, not the ticket.**
Seven packages, each one file, each with a falsifiable "done when".
Devin's job was to satisfy a document, and a reviewer's job was to check the diff against that same document.
`planning/plans/packages/README.md` states the rule for the agent, and `AGENTS.md` line 12 says the rule for the report: "Do not mark unrun checks as passing or change test expectations merely to get green checks."

**Three of seven merged, and we can say exactly why the other four did not.**
PR 4 integrated the CAD rendering and the simulation dependencies, PR 6 renamed the project and added the agricultural data research, and PR 7 adopted the PR based workflow and the CI that now gates every change.
PR 3 was superseded by PR 7 rather than rejected.
PRs 1, 2 and 5 are the interesting ones, and they are section 4.

**The honesty rules were enforced by tests, not by good intentions.**
Five gate tests under `software/tests/` police the labelling: every figure on the page is gauge, modelled, simulated or assumed, and `test_no_figure_for_cost_yield_energy_or_water_saved` fails the build if the page claims a saving.
An agent writing enthusiastic copy trips them in CI, which is the only reliable place to catch it.
One of our own commits, `d047530`, exists because a code comment tripped that gate.

**We know what Devin did not do.**
Devin authored no commit on `main` under its own name, and all of its accepted work arrived through PRs 4, 6 and 7.
PR 4 was an integration of Ameya's CAD revision rather than original build work.
The README's line is the ceiling we hold to: "Devin, from Cognition, assisted with implementation, integration and checks."

## 4. The four that did not merge, which is the part worth your time

A judge will hear "Devin wrote our code" from every table today.
This is what we learned instead, and each item cost us something real.

| What happened | The evidence | What we changed |
|---|---|---|
| PR 1 built a different product entirely: a serial contract, a board, a `DayPlayer`, and a Houston 2013 dataset. It read our planning folder, found stale files from an idea we had set aside, and built those | PR 1, closed unmerged, branch `devin/1789856444-shared-core`, 3937 additions. `planning/RUN.md` line 39 records the branch as never to be merged | We rewrote every file under `planning/` the same night, "because a build agent reads whatever it finds". Stale planning is not neutral: to an agent it is an instruction |
| PR 5 replaced the page instead of adding to it. Its `index.html` dropped `scene.js`, `console.js`, `flectofin.js` and `rules.js`, so merging it would have deleted the 3D roof and the console, and it added a second rain model beside the shared rules | PR 5, still open, 2861 additions and 353 deletions across 34 files. The review comment on the PR gives the mechanism | We stopped asking for a feature and started naming the files a task may touch. The plan that followed, `devin-parallel-2026-09-20.md`, divides the page file by file between two agents |
| PR 2 solved a problem that had stopped existing. It built a gate runner for the package rules, which `AGENTS.md` had since replaced with CI | PR 2, still open, 22 commits behind `main` | An agent holds the world as it was when its session started. A long running session needs re-briefing, not more instructions |
| A session ran out of credits mid task and had pushed nothing, so the work was unrecoverable | The team's own account. There is no repository evidence, because nothing was pushed | Commit and push early, even when the work is unfinished. Unpushed agent work does not exist |

The one line version: **our failures with Devin were all failures of context, not of capability.**
Every one of them came from what the agent could see, and none from what it could do.

## 5. Show, do not tell

Thirty seconds, in the repository and not on the page.

1. Open `planning/plans/packages/H1-zones-light-rain-soil.md` and point at the expected values table. Say: this was written before any code.
2. Open the pull request list, filtered to the Devin bot. Say: seven, three merged, and here is PR 1.
3. Open PR 1's body. Say: it built a different product, from planning files we had not cleaned up. That is what taught us to treat the planning folder as an instruction to the agent.
4. Open `planning/plans/devin-parallel-2026-09-20.md` at the "Who may touch what" table. Say: this is what we do now.

## 6. What we do not claim

- We do not claim Devin built this project. Ameya built the 3D roof and the console, the simulation rules and the research were specified by people, and the judging polish was made outside Devin.
- We do not claim a productivity figure. We did not measure one, and we will not invent one.
- We do not claim the agent was at fault in any of the four failures. In each case it did what its context implied.
- The credits exhaustion is our own account, with no repository evidence, and we say so.

## 7. Questions they will ask

**"So what did Devin actually build that shipped?"**
"Three pull requests merged: the integration of the CAD rendering with the simulation pipeline, the project rename with the agricultural data research, and the workflow and CI that now gate every change.
Devin authored no commit on `main` under its own name, and PR 4 was an integration rather than original build work.
Our README says it assisted with implementation, integration and checks, and that is the ceiling we hold to."

**"How do you stop it from writing code that passes its own tests?"**
"The expected values were computed by a person, from the real data, before any code existed, and they live in the package file.
The agent's job is to hit a number it did not choose.
On top of that, five gate tests enforce the labelling, and one of our own commits exists because a comment tripped one."

**"What would you do differently?"**
"Three things, all about context. Clean the planning folder before starting an agent, because it reads whatever it finds. Name the files a task may touch, instead of describing a feature. And re-brief a long running session, because it holds the world as it was when it started.
We would also push unfinished work, since we lost a session's output this morning to a credit limit."

## Where each fact came from

| Fact | Source |
|---|---|
| Seven Devin pull requests, three merged, two closed, two open | `gh pr list --repo andomo3/flecto-shade --state all --author "app/devin-ai-integration"` |
| PR 1 built a different product from stale planning files | PR 1 body, branch `devin/1789856444-shared-core`, and `planning/RUN.md` line 39 |
| PR 5 would have removed the console and the roof | PR 5 diff and the review comment on PR 5 |
| PR 2 is 22 commits behind and duplicates CI | PR 2, and the review comment on it |
| Expected values written before code | `planning/plans/packages/H1-zones-light-rain-soil.md` and `S1-solar-2023.md` |
| The labelling gates | `software/tests/test_gate_f4_schema.py`, `f5_labels`, `f6_assumptions`, `f7_rules`, `f14_sources` |
| A comment tripped the measured word gate | commit `d047530` |
| Devin authored no commit on `main` | `git log --format='%an' | sort | uniq -c` on `main`: 87 abba, 10 Ameya, 0 Devin |
| The README's credit line | `README.md` line 133 |
| The credits ran out mid session | The team's own account, no repository evidence |
