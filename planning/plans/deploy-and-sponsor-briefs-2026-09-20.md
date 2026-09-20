# Deploy, and one brief a sponsor challenge, Sunday 2026-09-20

Written by the planner at 09:00, on abba's instruction, for a smaller model to execute in abba's terminal.
Submission is at 11:00.
Ameya owns the frontend, so this plan touches no file under `software/page/`.

Two jobs, in this order, one pull request each.
P1 is the deployment, because the release checklist needs a public address and the README needs the link.
P2 is the briefs, because the pitch needs them and nothing else waits on them.

## The to-do list

| # | Work | Who | Done by |
|---|---|---|---|
| P1.1 | Preflight: read the config, run the suite, serve the page locally | executor | 09:10 |
| P1.2 | Log in to Vercel | abba, one command | 09:12 |
| P1.3 | Preview deployment, and walk the check list against it | executor | 09:25 |
| P1.4 | Production deployment from `main`, and walk the list again | executor, after abba says yes | 09:35 |
| P1.5 | Put the address in the README and the repo's homepage field, open the pull request | executor | 09:40 |
| P2.1 | Get the text of each sponsor challenge | executor, abba if the site does not have it | 09:50 |
| P2.2 | Gather the evidence for each brief from the repo | executor | 10:00 |
| P2.3 | Write the briefs with the `hackathon-pitch` skill | executor | 10:25 |
| P2.4 | Full suite, pull request, abba merges | executor, abba | 10:30 |

## Rules for the executor

- Read `AGENTS.md` and `CONTRIBUTING.md` first. Never push to `main`, and open a pull request for each job.
- Run `python -m pytest software/tests -q` in full before every pull request.
- Never write a secret, a token, or a connection string into a file, a commit, or a log. `.vercel/` is already in `.gitignore`, and it stays there.
- No em dash in any file. One sentence a line in Markdown.
- A fact that cannot be found is written as a marked gap in square brackets for abba, and is never invented.
  This matters most for the challenge texts and for anything said about Devin.
- If a step fails twice, stop and tell abba what happened. Do not patch a third time.

## P1. Deploy what can be deployed

Branch `chore/deploy-vercel`.

### What is already there

`software/DEPLOYMENT.md` is the specification, and `software/vercel.json` is the configuration.
The Vercel project's Root Directory is `software`, the output directory is `page`, there is no build command, and `/api/*` is rewritten to the one Python function `api/index.py`.
Vercel CLI 59.0.0 is installed on abba's laptop and is not logged in.
The repository is public, and it has no homepage address and no GitHub Pages site.

### What can be deployed, and what cannot

| Part | Deployable | Note |
|---|---|---|
| The static page, `software/page/` | Yes | It needs no build and no network |
| The API, `software/api/` | Yes, without a store | A serverless disk does not persist, and no PostgreSQL driver is approved, so `/api/health` reports the store as unavailable and the console shows its offline state. `DEPLOYMENT.md` names this as a supported state |
| The data builds, `software/h1/`, `data/` | No | They are build tools, and their outputs are committed |

### The one known risk

`software/requirements.txt` pins `pandas`, `numpy` and `pytest`.
The API imports none of them, and Vercel's Python builder installs that file for the function all the same.
If the preview build fails on the function's size or on the install, do not fight it.
Take the fallback below, say so in the pull request, and move on.

### Steps

1. **Preflight.** On `main`, run the full suite, then `python software/api/local_server.py --port 8000`, and confirm `/` and `/api/health` answer 200.
2. **Login.** Ask abba to type `! vercel login` in the prompt. It is interactive, and the executor cannot do it.
3. **Preview.** From the `software` directory: `vercel deploy --yes`.
   Accept a new project named `flecto-shade`. The command prints the preview address.
4. **Walk the list.** Against the preview address, with `curl` and then in a private browser window, check every line under "What to check on the deployed address" in `software/DEPLOYMENT.md`.
   At the least: `/` is 200, `/day.json` is 200, `/style.css` is 200, `/api/health` is 200 with `"status": "ok"`, the page source holds the words "Simulated" and "EP2320015", and no secret appears in the source or the build log.
5. **Production.** Show abba the preview address and the results, and wait for a yes. Then `vercel deploy --prod --yes`, and walk the same list again.
6. **Record it.**
   - In `README.md`, put the production address where the demo link belongs. Find the place by reading the file; do not restructure it.
   - In `CHECKLIST.md`, change nothing. Its boxes are ticked by a person.
   - Run `gh repo edit andomo3/flecto-shade --homepage <address>`.
   - In `software/DEPLOYMENT.md`, add a short section "Deployed on 2026-09-20" with the address, the revision deployed, the results of the list, and what was not checked.

### The fallback, if the function will not build

Deploy the page alone: from `software/page`, run `vercel deploy --yes`, then `--prod`.
The console is written to run with no API, and `test_an_unavailable_service_still_leaves_the_demonstration_running` checks that path.
Record in `DEPLOYMENT.md` that the API is not deployed and why.
Do not add a `.vercelignore`, a second `vercel.json`, or a split of `requirements.txt` today. That is the right fix and it belongs after the event.

### Done when

- The production address opens in a private window with no login, plays the simulated day to 23:00, and shows the roof.
- The README holds that address, and the repo's homepage field holds it too.
- The pull request states the revision deployed, each check with its real result, and what was not tested. A physical phone is abba's check, not the executor's.

### Not part of this job

A continuous deployment from GitHub, a custom domain, a database, authentication.
Connecting the Vercel project to the GitHub repository is a two minute step abba can take in Vercel's dashboard after submission.

## P2. One brief a sponsor challenge

Branch `docs/sponsor-briefs`. New files under `planning/pitch/sponsors/`, and one line added to `planning/pitch/README.md` pointing at the folder.

### Step 1: the challenge texts

The repository holds no sponsor's challenge text. It holds three names.

| Sponsor | What the repo knows | Where |
|---|---|---|
| Cognition | Devin wrote code from the team's work packages, and the team may say so. Whether Cognition posts a challenge is not recorded | `planning/pitch/submission.md` |
| Voloridge | The challenge is called "Signal in the Noise", it wants a finding drawn from data, and it accepts any dataset | `planning/project-brief.md`, `planning/RUN.md`, `planning/docs/research/flectofin-greenhouse-roof/agricultural-data-voloridge.md` |
| Long Lakes | It wants an AI explainer, which the project does not have, and abba has not decided to enter it | `planning/plans/devin-todo-2026-09-20.md` |

Look for the published text first: HackMIT's own site and its Devpost page for 2026, under sponsor challenges or prizes.
Give this five minutes.
If the text is not found, ask abba to paste it, and meanwhile write each brief with its first section as a marked gap.
Never write a judging criterion from memory or from a guess.
If the site lists a challenge the project fits and the repo has not named, list it for abba with one sentence of reasoning, and write no brief until abba says yes.
The hardware challenge is out, because nothing physical was built.

### Step 2: the evidence

Gather it before writing, in a scratch file, with the source of every line.

For Cognition, the brief that matters most:

- `gh pr list --state all --author "app/devin-ai-integration"` gives Devin's pull requests. At the time of writing: 1, 2, 3, 4, 5, 6, 7, of which 4, 6 and 7 merged, 1 and 3 closed, 2 and 5 open.
- For each one: what it delivered, whether it merged, and what the review said. Read the pull request's body and its comments.
- The work package specifications Devin built from: `planning/plans/packages/`, and the two to-do files in `planning/plans/`.
- The workflow around it: a person writes a specification with a falsifiable "done when", Devin builds and opens a pull request, a reviewer checks it against the specification, and a person merges.
- The honest failures, which are the strongest material: Devin once built the wrong product from stale planning files, which led to the rule that every decision lands in a file. Pull request 5 replaced the page instead of adding to it, and was not merged. This morning a session ran out of credits before it pushed.
  A judge from Cognition has heard "Devin wrote our code" all day. A team that can say what it learned about directing an agent is rarer.
- What was not Devin: the simulation's rules and the research were specified by people, Ameya built the 3D roof and the console, and the judging polish was made outside Devin. Say so. The README's line is "Devin, from Cognition, assisted with implementation, integration and checks", and the brief must not claim more than that line can carry without evidence.

For Voloridge:

- The two datasets, their provenance and their labels: `data/README.md`.
- The finding already on record: a typical year of sun joined to a real year of rain made rainy daylight hours brighter than dry ones, and sun from the same place and year corrected it. Find the figures in the repo before using them, and cite the file. If they describe an older site than the page now uses, say so or leave them out.
- The FAWN research and the evidence chart draft, package D1, in `planning/plans/packages/`.
- The honesty gates in `software/tests/`, which label every figure as gauge, modelled, simulated or assumed. For a quantitative firm this is the point: the project separates signal from its own assumptions.

### Step 3: write, with the pitch skill

Invoke the `hackathon-pitch` skill before writing a word, and follow it.
One file a challenge: `cognition.md`, `voloridge.md`, and any other abba approves.
Then `README.md` in the same folder: a table of challenge, the one sentence, and the file.

Each brief has these sections, in this order, and fits one screen:

1. **What they ask for.** The challenge's own words, quoted, with the address they came from. Or the marked gap.
2. **Our one sentence.** What the team says when this sponsor's judge walks up. Under 25 words.
3. **How we attacked it.** Three to five points, each with its evidence: a file, a pull request number, a test name.
4. **Show, do not tell.** The exact 30 seconds of the demo to show this judge, as steps on the deployed page or in the repo.
5. **What we do not claim.** The limits, in the project's usual words: simulated, not a result about a real roof, no figure for yield, cost, energy or water saved.
6. **Questions they will ask, and the answers.** Three, taken from or added to `planning/pitch/questions.md`.

The Cognition brief carries one section more, **How we worked with Devin**, a short table: the task, what the person specified, what Devin did, how it was checked, what happened.
It also names what the team would change next time.

### Done when

- Every sentence about Devin, a dataset or a figure has a source a judge could open.
- No brief states a criterion that is not quoted from the sponsor.
- No figure for the year appears, because `headline.json` does not exist.
- The full suite passes, since it gates wording.
- abba has read the Cognition brief aloud once and it takes under 40 seconds to say the one sentence and the first two points.

### Not part of this job

Slides, the video, any change to the page, and any new analysis of data.
A badge or a sponsor's name on the page is Ameya's call, and the rule from the earlier plan stands: no badge for a sponsor whose product the page does not use.
