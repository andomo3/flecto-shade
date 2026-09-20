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

## P1, an addendum: why Vercel, and the setup that outlives today

Appended at 09:00, after abba asked for the hosting to be set up properly.

The recommendation is Vercel, and P1 above is the way in.
The reasons: the repository already carries `software/vercel.json` and `software/DEPLOYMENT.md`, the CLI is installed, the free tier serves a public address with no login, and it can run the Python API beside the static page, which GitHub Pages cannot.
GitHub Pages is the second choice, and it is the fallback of last resort if Vercel's login fails at the table: it serves `software/page/` alone, with the console in its offline state.
Netlify and Render add nothing here and would need new configuration.

Two steps beyond P1, both abba's, both after the production address is checked:

1. **Connect the project to GitHub.** In Vercel's dashboard, open the project, then Settings, then Git, and connect `andomo3/flecto-shade` with the Root Directory `software` and the production branch `main`.
   From then on every merge to `main` deploys, and every pull request gets a preview address, which is what `DEPLOYMENT.md` means by "preview deployments come from a feature branch".
   Do this only after the freeze at 10:00 is agreed, because a merge after it would change the address a judge is looking at.
2. **Set `APP_ENV` to `production`** in the project's environment variables, so `/api/health` tells production from preview. It is not a secret. No other variable is needed without a database.

The executor records both in `DEPLOYMENT.md` as done or not done, and never as done on abba's word alone: it checks `/api/health` for the `app_env` value.

## P3. Adapt the pitch to abba's thinking, and the questions that keep it moving

Appended at 09:00, on abba's instruction, and written through the `hackathon-pitch` skill.
Branch `docs/pitch-adaptation`. Files: `planning/pitch/story.md`, `planning/pitch/questions.md`, and the three scripts only where a beat changes.

A note on the source.
Abba meant to paste a detail of this thinking and nothing arrived, so this section is built from what abba said in Saturday night's sessions.
When the paste arrives, the executor checks it against the table below and adds a row for anything new, before touching a script.

### What abba has been thinking, and where each idea may live in the pitch

| The idea | The verdict | Where it lives |
|---|---|---|
| The roof is also an instrument: a record of what every bed received, which joined to soil telemetry could teach something about soil decline and plant illness | Keep, as a vision in future tense with no figure. It is already the "what comes next" beat | The close, and the Voloridge brief |
| The judge plays the farmer and chooses the areas to water | Keep, and it is the strongest demo moment once Ameya's component is merged. Until then it is not shown and not said | The demo storyboard, only after the merge |
| Generalise beyond three crops | Done. The story rests on the state of one bed, crop, stage, season and soil, and the three beds are three light classes | `story.md`, "The general problem" |
| Miles of irrigation equipment wasted, motor energy saved, less spent on lamps | Dropped on Saturday night, because the sources contradict all three. Never said, and the irrigation system stays | `story.md` already says so. A smaller model must not bring them back |
| The next step is a Monte Carlo study, led by an operations research student | New, and it is the beat that turns "it is only a simulation" from a weakness into the plan | The "what is next" beat, the Q&A bank, and P4 |

### How the pitch changes, by the skill's rules

The spine does not change: the grower, the blunt roof, the fin, the storm with three answers.
Three beats change.

1. **Prime the judge early.** The skill says a judge evaluates through whatever lens the opening sets.
   The lens is "simulated, and honest about it".
   Within the first twenty seconds: "Everything you will see is a simulation, run over one real day of Florida weather, and every number on the screen says where it came from."
2. **"What is next" becomes a rule of three, in the order of cost.**
   - First, stress the model: a Monte Carlo study over our own assumed constants, to find out which of our guesses the result depends on. It is specified, and it needs nothing we do not have.
   - Second, check the inputs on site: the same rules run over the weather station at Apopka, with no hardware.
   - Third, the record: every bed's light and rain, kept, and joined to soil sensors.

   No figure is attached to any of the three.
3. **The offer, said by abba in the first person.** The skill ends on what the team wants from this judge.
   "I study industrial engineering and operations research. The simulation is the product today, so the next thing I build is the study that tries to break it. If you know a grower, or a soil dataset, I want the introduction."
   Change the asking to fit the judge: a dataset for Voloridge, a view on how we directed Devin for Cognition.

What does not change: nothing is claimed about yield, cost, energy or water saved, no figure for the year is spoken, and Elena stays illustrative.

Then cut twenty percent, and keep each length in its range: 75 to 90 words, 150 to 180, and 450 to 540.
The skill names a timer script, `pitch_timer.py`, and this repo does not hold it, so count the spoken words of each script with a few lines of Python, leaving out headings, stage directions and anything in square brackets, and write the counts in the pull request.

### Questions for abba, which the executor asks before editing a script

Each has a default, so silence does not block the work.

1. Which track is entered: Entertainment, Education, Sustainability or Healthcare? Default: Sustainability. `submission.md` still has it as a gap.
2. Booth or stage, and how many minutes? Default: booth, three minutes, product first and no slides.
3. Who speaks? Default: abba drives, Ameya clicks and takes the questions about the page.
4. Is Ameya's farmer component merged and working on the deployed address by 10:15? If not, the demo is the storm with three answers, and the farmer beat is not said.
5. Does abba want the first person line about operations research? Default: yes, once, in the offer, and never as an opening.
6. Which sponsor challenges are entered? This is P2's question, and the answer decides which offers are rehearsed.
7. Is the soil telemetry analysis from Saturday night far enough along to show one chart? Default: no, and it stays a sentence in future tense.

### Questions a judge will ask, to add to `questions.md`

Each answer follows the skill's formula: the direct answer, the evidence, the honest scope.
The executor drafts the answers from the files named, and leaves a marked gap where the repo does not hold the fact.

1. "It is a simulation. Why should I believe any of it?" From `simulation-and-field-test-plan.md`, sections 1 and 4: the rules are written down, two runs give identical bytes, every figure is labelled, and the next step is the study that attacks our own assumptions.
2. "Which of your assumptions matters most?" The honest answer today is that we do not know yet, and P4 is how we find out. Name the twelve assumed constants and the rank correlation that will order them.
3. "Why Monte Carlo and not a discrete event tool such as Simio or Arena?" Section 3: the roof has no queue and no entity waiting for a server. It is a time stepped system with uncertain constants and uncertain weather.
4. "Why uniform distributions?" Because we have no evidence for a shape, and a bell curve we made up would claim knowledge we do not have. The ranges tighten as constants are sourced.
5. "How many runs, and how do you know that is enough?" P4's stopping rule: the half width of the interval on the headline output, checked after a pilot run.
6. "What would make you stop?" Section 5, "What would make us stop".
7. "What is your model's worst flaw?" Section 2, first item: under a shut roof the crop's water use is zero. Say it before the judge finds it.
8. "What does the data you would collect look like, and who would want it?" The per bed record, from the "what comes next" beat and its sources. Future tense, no figure.
9. "What did the people do, and what did Devin do?" The Cognition brief from P2.
10. "What would a grower pay for this?" We do not know, and we make no claim about cost. The ladder in section 5 says what has to be true before anyone should ask.

### Done when

- `story.md` carries the three changed beats, and no dropped claim has come back. Search the pitch folder for "irrigation infrastructure", "motor energy" and "lamp" and read every hit.
- Every script is inside its word range, by the count.
- `questions.md` holds the ten new questions with answers or marked gaps.
- The full suite passes.

## P4. The simulation study brief

Appended at 09:00. Branch `docs/simulation-study-brief`.
One new file, `planning/docs/research/flectofin-greenhouse-roof/simulation-study-protocol.md`, and one row for it in `planning/docs/STATE.md`.
Documents only. No code is written today, and `software/h1/` is not touched.

### Why a second document, when section 3 of the simulation plan exists

`simulation-and-field-test-plan.md` says which kind of simulation and why.
It does not yet say what an operations research reader looks for first: the question the study answers, the factors and the responses, the design of the experiment, how many runs and why, how the output is analysed, and what result would change a decision.
The protocol is that document, written before development so the study cannot be bent afterwards to fit what it finds.
It extends section 3 and contradicts nothing in it. Where they differ, the executor stops and asks abba.

### The parameters, defined here so the executor does not have to invent them

**1. The questions, in order.**

- Q1. Does the demo's claim survive our own assumptions? The claim: on 3 June 2023 three zones give three different answers to one storm.
- Q2. Which assumed constants drive the outputs, and so deserve a real source first?
- Q3. Do the results survive a different year, and the weather station on site?
- Q4. What happens when a part fails? Out of scope for the first study, and named so that nobody thinks it was forgotten.

**2. Factors. Three kinds, kept apart, because mixing them is the commonest error in a study like this.**

| Kind | What | Treatment |
|---|---|---|
| Uncertain constants | The twelve in `ASSUMED_CONSTANTS` in `software/h1/build.py`: `PAR_FRACTION`, `T_STRUCT`, `T_CLOSED`, `SOIL_CAPACITY`, `SOIL_DRY_BELOW`, `SOIL_FULL_AT`, `SOIL_IRRIGATE_BELOW`, `SOIL_START`, `HARD_RAIN_MM`, `DRYING_HOURS`, `HEAT_SHADE_C`, `HEAT_SHADE_OPEN` | Sampled |
| Exogenous inputs | The hourly sun, rain and air temperature | Layer A holds them fixed at 2023. Layer B varies the year |
| Decision variables | Each zone's crop profile, light rule, light target and whether it may admit rain | Held at the page's three zones. They are what a grower chooses, so they are scenarios and never random draws |

The two recalled constants, `MAKKINK_C` and `LATENT_HEAT_MJ_PER_KG`, are published values and are not sampled.

**3. Distributions and constraints.**

- Uniform, 20 percent either side of the page's value, because there is no evidence for a shape.
- Bounded where physics bounds them: a transmission or an open fraction stays within 0 and 1, so `T_CLOSED` at 0.0 is sampled on 0 to 0.10 and not by percentage, and `T_STRUCT` and `HEAT_SHADE_OPEN` are clipped at 1.
- `DRYING_HOURS` is an integer, drawn from 2, 3 and 4.
- The ordering `SOIL_IRRIGATE_BELOW < SOIL_DRY_BELOW < SOIL_FULL_AT <= SOIL_CAPACITY`, with `SOIL_START <= SOIL_CAPACITY`, holds in every draw.
  Enforce it by sampling the thresholds as shares of the capacity and not by rejecting draws, because rejection quietly changes the distribution that was promised.
- A row in the protocol for every constant: the value, the range, the reason for the range, and the source that would replace the guess.

**4. Responses.**

| Response | Kind | Why |
|---|---|---|
| Three distinct answers to the storm of 3 June 2023 | Yes or no for each draw, reported as a share with a Wilson interval | It is the claim the pitch makes |
| Days in the year each zone met its light target | Count, for each zone | It is on the page |
| Rain's share of each zone's water | Share, for each zone | It is on the page, and it is the figure the known flaw distorts most |
| Hours the roof's state differs from the base run | Count | It measures how far a guess moves the behaviour and not only the totals |

No response is a figure for yield, cost, energy or water saved.

**5. The design of the experiment.**

- Latin hypercube over the twelve dimensions, with one fixed seed, `numpy.random.default_rng(20260920)`, so the same seed gives the same bytes.
- The same weather in every draw of layer A. That is common random numbers, and it means a difference between two draws comes from the constants and not from the sky.
- The model is deterministic once the constants and the weather are fixed, so one run a design point. Replications would add nothing, and the protocol says so, because an examiner will ask.

**6. How many runs, and the rule for stopping.**

- A pilot of 100 points. Then the half width of the 95 percent interval on each response.
- For the yes or no response, n is at least z squared times p times (1 minus p) over h squared. At the worst case p of 0.5 and a half width of 0.05 that is 385, so plan 400 and say why.
- For the percentiles, intervals by bootstrap over the draws.
- Report the time a run takes from the pilot before promising a number of runs.

**7. Analysis of the output.**

- For each response: the 5th, 50th and 95th percentile, and where the page's own value falls among them.
- Sensitivity, first pass: partial rank correlation of each constant with each response. It costs nothing more, and it handles a monotone response that is not a straight line.
- Sensitivity, second pass, only if the first is unclear: Morris screening, and then Sobol indices by the Saltelli scheme over the few constants that survive. It costs N times (k plus 2) runs, and it may bring a dependency, SALib, which needs abba's approval.
- A plot a constant: the response against the constant, which shows a threshold that a correlation hides.

**8. What result changes what decision.** Written before the study runs.

| If | Then |
|---|---|
| Three answers in 95 percent of draws or more | The pitch may say the demo's claim does not depend on our assumed constants, with the share and its interval |
| Under 95 percent | Name the constant that breaks it, source it properly, and say so in the pitch before a judge finds it |
| One constant dominates a response | That constant is sourced first, before any other modelling work |
| The known flaw in crop water use dominates the rain's share | Fix the flaw first and run the study again, because a study over a wrong model measures the wrong thing |

**9. Verification and validation.** Point at sections 4 and 5 of the simulation plan, and add three checks: the base case reproduces `data/processed/` byte for byte, an extreme draw behaves as physics says it must, and one draw is traced by hand for a single day.

**10. The order of work, and the point at which the known flaw is fixed.**

| Step | What | Depends on |
|---|---|---|
| S0 | Fix crop water use under a shut roof, with a floor marked ASSUMED, and rebuild H1's expected values | Nothing. It is the thirteenth constant, and it joins the study |
| S1 | `simulate` and `decide` take a mapping of constants, with the module's values as defaults. Outputs unchanged byte for byte | S0 |
| S2 | The pilot: 100 points, the time a run takes, the half widths | S1 |
| S3 | Layer A in full, its outputs file, its tests for the seed, the ordering and the base case | S2 |
| S4 | The sensitivity report, and the decisions of part 8 | S3 |
| S5 | Layer B: 2001 to 2023, then the FAWN station | S3 |
| S6 | Layer C: failures, as scenarios | After the event, and after S5 |

This order differs from task T4 in `devin-todo-2026-09-20.md`, which ran layer A before the fix because the clock demanded it.
After the event the fix comes first, and the protocol says why.

### Steps for the executor

1. Read `simulation-and-field-test-plan.md` in full, the constants in `software/h1/build.py`, and the "Assumptions" section of `data/README.md`.
2. Write the protocol with parts 1 to 10 above as its sections, in full sentences, one sentence a line, with the table of constants filled from the code and not from this plan.
3. Add "Sources for the methods": Latin hypercube sampling, McKay, Beckman and Conover, 1979. Global sensitivity analysis, Saltelli and others, 2008. Morris, 1991. Simulation output analysis, Law, "Simulation Modeling and Analysis".
   Give each as a citation to be confirmed, and quote nothing that has not been opened.
4. Add the twenty second version for the pitch, which P3 uses.
5. Run the full suite, open the pull request, and leave one question for abba at the top of its body: whether S0 comes before layer A, as written here, or whether layer A runs first on the model as it stands.

### Done when

- A reader with a first course in simulation can say what is sampled, from what, how many times, why that many, what is reported, and what result would change the team's mind.
- Every constant in the table matches `ASSUMED_CONSTANTS` by name and by value.
- Nothing in the protocol is a result. It holds no figure from a run that has not happened.

## The order, now that there are four jobs

P1, the deployment, first, because the submission needs the address.
P2, the Cognition brief before any other brief.
P3, because the pitch is spoken at the table and the questions need abba's answers.
P4 last. It is the only one a judge never reads, and it is the one abba will want to write the most, so it is also the one to hand to the executor and review afterwards.
If the clock forces a cut, cut P4 to its twenty second pitch version, which P3 needs, and write the protocol after the event.
