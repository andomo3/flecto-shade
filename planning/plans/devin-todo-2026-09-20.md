# Devin's to-do list, Sunday 2026-09-20

Written by the planner at about 04:00, for Devin to work through while abba sleeps.
Submission is at 11:00, and nothing touches the page after 10:00.

## How this list is worked

- Devin executes, and opens one pull request per task.
  The planner reviews each pull request before it is merged, and abba has the last word.
- Work the tasks in the order given, and stop at the cut line if the clock says so.
- Branch every page task from `feat/judging-ui-polish`, and not from `main`, until that branch is merged.
  It holds the judging polish the planner already made, and a task built on `main` will conflict with it.
- One task, one branch, one pull request, small commits, and the workflow in `CONTRIBUTING.md`.
- Every pull request states the checks that were run and the behaviour that was not tested.
  An unrun check is never written as passing.
- Run `python -m pytest software` and `node --check` on every page script before opening a pull request.
  The full suite, never a part of it: the planner ran a part once tonight and shipped a comment that tripped the honesty gate.
- An expected value that does not match is reported, and never edited to make a test pass.
- If a task fails its own check twice, stop, write what happened on the pull request, and move to the next task.

## What is already done, so nobody does it twice

| Branch | What | State |
|---|---|---|
| `fix/health-storage-status` | `/api/health` reported storage as unavailable when it was ready | pushed, needs a pull request |
| `feat/judging-ui-polish` | The page opens at its top, the run button is on the roof, zone cards read at a glance, the camera fits a narrow frame, a headline that says what the page does, a favicon | pushed, needs a pull request |
| `feat/pitch-video-script` | The 90 second video script, the dataset research, the package D1 | pushed, needs a pull request |

Pull request 5, the farmer-selected watering flow, conflicts with `main` and is not part of this list.
Abba decides what happens to it.

## The layout the page must have

Abba's instruction, and it outranks the older specifications: four regions, read left to right and top to bottom.

| Region | Where | What goes in it on our page |
|---|---|---|
| 1. The hook | A header across the top | The mark and the name Flecto Shade, the tagline, and the badges |
| 2. The command centre | A left sidebar | Everything a judge presses: run, go to the storm, restore, the hour, the zone, the view, the zone's settings |
| 3. The wow | The centre, the largest area | The roof, its clock, and its zone tags, and nothing else |
| 4. The validation | A right panel, and a strip along the bottom | Every zone's answer and its reason, the result of the run, where each number comes from, and how far the result holds |

The judge's eye goes from the control on the left, to the roof moving in the centre, to the reason on the right.

## The tasks

### T1. Play a rain hour in 5.0 seconds

Priority 0, about 20 minutes, branch `fix/storm-playback-seconds`.

- **Why.** The storm is the claim of the whole pitch, and it is on the screen for 4.8 seconds, because a rain hour plays in 2.4 seconds like any other daylight hour.
  `planning/pitch/story.md` asked for 5.0 seconds so that three reasons can be read from a metre away, and the page was built without it.
- **Do.** In `software/page/build_day.py`, give an hour with rain a `play_seconds` of 5.0, as a named constant `RAIN_HOUR_SECONDS`, and rebuild `day.json`.
- **Done when.** The two rain hours of 3 June 2023 carry 5.0 seconds, `day.play_seconds` is 43.8, and `test_playback_matches_the_spoken_demo` passes with its expected values changed to match, with the reason written in the pull request: the story's requirement, never a convenience.
- **Behaviour check.** Run the day in a browser and time the storm with a stopwatch: about 10 seconds.
- **Must not touch.** `software/h1/`, `data/processed/`.

### T2. The four region layout

Priority 0, about 120 minutes, branch `feat/four-region-layout`, from `feat/judging-ui-polish`.

- **Why.** Abba's layout above, and the three second rule: a judge must see what it is, what to press, and what happened, without scrolling.
- **Do, region by region.**
  1. **The hook.** A `<header>` holding the mark from `favicon.svg`, the name "Flecto Shade" as the `h1`, and the tagline "A simulated shade house roof that gives every bed its own light and rain."
     Three badges, each a word and a glyph as well as a colour: "Simulated", "Sun: NASA POWER, modelled. Rain: NOAA gauge, 2023", and "Built with Devin, by Cognition".
     The third badge is true and is already in the README.
     Add no badge for any sponsor whose product the page does not use.
     The identity card comes off the roof, because the header now says it.
  2. **The command centre.** A left sidebar of about 300 px holding, in this order: "Run the simulated day" as the largest control on the page, "Go to the storm", "Restore the baseline", the hour slider with its marks and its readout, a row of zone buttons A to D, the view presets and the detail tools, and a "Change this zone's settings" button that opens the existing zone form.
     Every control keeps its `id`, so `console.js` and `app.js` need no new wiring beyond where a node lives.
  3. **The wow.** The roof takes the centre, and it is the largest region at every width above 1040 px.
     Its height is the viewport's height less the header.
     Only the clock, the zone tags, and the module legend stay on top of it.
  4. **The validation.** The right panel holds the zone cards as they are on `feat/judging-ui-polish`.
     The bottom strip holds the selected zone's decision log, the source lines with their labels of gauge, modelled, simulated, and assumed, and one plain line: "The roof follows nine written rules. No learned model is in the loop, and two runs of the same day give identical output."
     That line is already checked by `test_two_runs_give_identical_bytes`, so it is true.
     T3 and T4 add the result card and the robustness strip to this region.
  5. **The configuration workspace** stays below the fold as it is, reached from the sidebar's settings button.
- **The test that must change.** `test_there_is_no_decorative_top_bar` forbids any `<header>`.
  Abba has changed the requirement, so replace it with `test_the_header_is_the_hook`: the header holds the `h1`, the tagline, and the word "Simulated", and holds no navigation link.
  Say in the pull request that the requirement changed and who changed it.
- **Done when.**
  - At a 1440 by 900 viewport and at a 1536 by 730 viewport, with no scrolling: the header, the run button, the whole roof, and the roof position and reason of all three zones are in view.
  - At 390 px wide the order is header, run controls, roof, zone cards, the rest, with no sideways scroll and no control under 44 px.
  - Every heading level is in order, the skip link still works, and the focus order follows the four regions.
  - A full run of the day plays to 23:00, the storm shows three answers, and the console shows no errors.
  - `style.css` keeps its rules: no type under 18 px, controls at 48 px, one palette, and no new colour.
- **Must not touch.** `software/h1/`, `software/api/`, `data/`, `rules.js`, `flectofin.js`, and the simulation logic in `console.js`.

### T3. The result card and `headline.json`

Priority 0, about 75 minutes, branch `feat/result-card`.
The specification is `planning/plans/packages/H3-result-card.md`, with two changes.

- The card sits in the validation region of T2, and appears when the run ends, as the page's success state: a heading "3 June 2023, simulated", one row a zone, the trade line, and "Play again".
- The year view is cut from this task.
  The three sentences for the year are kept, read from `headline.json`.
- **Done when.** The acceptance section of the package passes for the demo day, `pitch/figures.md` is generated, and every figure on the card equals the one in `data/processed/headline.json`.
- **Why it matters for the pitch.** Until this file exists nobody may say a figure for the year, and the video script says none.

### The cut line

If it is past 08:00 when T3 is merged, stop here and tell abba.
Everything below is worth doing and none of it is needed to submit.

### T4. How far the result holds: a Monte Carlo run over the assumed constants

Priority 1, about 90 minutes, branch `feat/robustness-monte-carlo`.
The design and the reasons are in `../docs/research/flectofin-greenhouse-roof/simulation-and-field-test-plan.md`, section 3.

- **Do.**
  1. `simulate` and `decide` in `software/h1/build.py` take an optional mapping of constants, whose defaults are the module's constants.
     The committed outputs stay byte for byte the same, which `test_two_runs_give_identical_bytes` already checks.
  2. `software/h1/robustness.py` draws 300 sets of the constants H1 marks ASSUMED, each from a uniform range of 20 percent either side of its value, with `numpy.random.default_rng(20260920)`, and runs the year for each zone.
     The ordering `SOIL_IRRIGATE_BELOW < SOIL_DRY_BELOW < SOIL_FULL_AT <= SOIL_CAPACITY` is kept in every draw, and a draw that breaks it is drawn again.
  3. It writes `data/processed/robustness-apopka.json`: for each zone the 5th, 50th, and 95th percentile of the rain's share and of the days the light target was met, and the share of draws in which the three zones still give different answers to the storm of 3 June.
     It also writes the rank correlation of each constant with the rain's share, so the page can name the two assumptions that matter most.
  4. The validation region shows it as one strip a zone: a line from the 5th to the 95th percentile, a mark at the median, and a mark at the value the page uses, labelled "simulated, over 300 draws of our assumed constants".
- **Done when.** `python software/h1/robustness.py` exits 0 with the network off in under ten minutes, two runs give identical bytes, and the tests check the seed, the ordering rule, and that the page's own value lies inside its own range.
  If 300 draws take over ten minutes, use 150 and say so.
- **Never said.** No figure for cost, yield, energy, or water saved comes out of this.
  It reports the spread of figures the page already shows.

### T5. The evidence chart

Priority 1, about 45 minutes, branch `feat/evidence-chart`.
The specification is `planning/plans/packages/D1-evidence-chart.md`, on the branch `feat/pitch-video-script`.
A person downloads the three files and checks their sha256 before Devin starts, so this task waits for abba.

### T6. The README's hero and its checklist lines

Priority 1, about 30 minutes, after T2 is merged, branch `docs/readme-hero`.

- A screenshot of the opening screen and one of the storm, at 1440 by 900, in `assets/screenshots/`.
- The status block at the top of the README rewritten to what `main` does now.
- The demo link and the video link are left as marked gaps for abba, who deploys and uploads.

## Not on this list, and why

| Idea | Why not now |
|---|---|
| Fixing the crop's water use under a shut roof, which the model sets to zero | It is the right fix, and it changes every soil figure, every expected value in H1's tests, and possibly the demo day itself. It is named as the known limit in the pitch and is the leading item in the plan for after the event |
| A weather ensemble over many years, and the FAWN station's own record | The research is done and the code is not. It is section 4 of the simulation plan |
| An AI explainer for the Long Lakes challenge | It needs a decision from abba, and it displaces T3 |
| Merging pull request 5 | It conflicts with `main`, and abba decides |

## The list checked against the judging and pitching checklists

| Checklist line | Covered by | State after this list |
|---|---|---|
| One clear headline, one subheadline, one primary action | T2, the hook and the run button | met |
| The main action is visible at once, and a judge knows what to do in three seconds | `feat/judging-ui-polish`, then T2 | met |
| Clean spacing and hierarchy, no type under 14 px | The stylesheet's own rule of 18 px, kept by T2 | met |
| Mobile: single column, 44 px targets, no sideways scroll | Checked at 390 px tonight, and again in T2 | met in a frame, not on a real phone |
| A loading state | The skeleton cards already on the page | met |
| A success state, with a next step | T3, the result card and "Play again" | met after T3 |
| An error state a person can read | The page's offline and fallback words, already there | met, and not checked tonight |
| Screenshot ready: a favicon, a title, no console errors | `feat/judging-ui-polish`, then T6 | met, less the social image, which needs the public address |
| The pitch matches what the page does, and every spoken figure is reproduced | The video script uses only `day.json`. T3 adds the year | met for the day, and for the year after T3 |
| Observations, modelled inputs, simulation, and assumptions are told apart | The badges in T2, the source lines in the validation strip, T4's label | met after T2 |
| The demo has a wow moment that can be read | T1 | met after T1 |
| A public demo address, a real phone, two timed rehearsals, a fallback recording | abba, because they need a login, a phone, and a voice | not started |

## What abba does on waking

1. Open the three pull requests listed under "What is already done", review, and merge.
2. Read Devin's pull requests with the planner's review on each.
3. Deploy: vercel.com, import `andomo3/flecto-shade`, set the root directory to `software`, and deploy.
4. Record the video from `planning/pitch/video-script-90s.md`.
   After T1 the storm holds for about 10 seconds by itself, so shot 5's held frame is no longer needed.
