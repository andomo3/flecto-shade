# Gates: what the build is checked against, every time

The demo, the pitch, and the checklists are the definition of done, and code that passes its own tests but breaks one of them is not done.
This file turns them into gates.
A gate is either something a command can check, or something a person must look at, and the two are never mixed, because "the agent says it checked" is not a check.

## How the loop runs

1. The build agent finishes a work package.
2. It runs the fast gates, all of them, with one command, `python tools/gates.py`, which package G1 builds.
3. It fills in the gate report below and puts it in its reply and in `GATES.md` at the root of the event repo, with the commit hash.
4. A gate that passed before and fails now is a regression, and it is fixed before anything else is touched.
5. If the same gate fails twice in a row, the agent stops and reports, and the package is reframed in the planning repo.
6. At each milestone, a person and the agent walk the milestone gates together, and the result goes in `GATES.md`.

A gate that does not apply yet, because the thing it checks is not built, is reported as NOT YET with the package that will switch it on.
It is never reported as PASS, and it is never left out.

## Fast gates, by command, after every package

| ID | Gate | How it is checked | Applies from |
|---|---|---|---|
| F1 | Every test passes | `pytest` exits 0 | the first package with a test |
| F2 | It runs with no network and no serial port | With sockets to the outside blocked, `python -m canopy serve --source fixture` starts, `/health` returns 200, and `/events` streams a reading | C5 |
| F3 | The page fetches nothing from the internet | No `http://`, `https://`, or `//` address in any `src`, `href`, `url(`, or `import` under `software/canopy/static/` | C8 |
| F4 | Every line on the wire obeys the contract | Every line from every source, fixture, fake, simulator, and serial, parses with C1's parser, in a test | C2 |
| F5 | Nothing simulated is called measured | A test renders the page's state for the simulator source and asserts three things: the simulation banner text is present, the word "measured" is absent from every label, and every figure on the result card carries the word "simulated" | C4, then C8, then B7 |
| F6 | A sensor that is not fitted is never zero | A test feeds a line with empty fields and asserts the state says "not fitted" and holds no 0 for them | C4 |
| F7 | The reaction is a threshold, not a tracker | A test runs the simulator through the demo day and asserts the leaf angle takes only its two end values and the ramp between them, and that it changes only when `light` crosses a threshold | B4 |
| F8 | The spoken numbers come from the code | [X], [Y], and [W] in `planning/pitch/script-plan-b.md` are read from a file the build writes, `data/processed/headline-sim.json`, and the result card shows the same values, in a test | B6 and B7 |
| F9 | The planning record is untouched | `git diff --name-only` against the last merge shows nothing under `planning/` | always |
| F10 | The package stayed in its files | The changed files are a subset of the package's "may create" list, passed to the command as an argument | always |
| F11 | Nothing private or bulky is committed | `git ls-files` shows nothing under `data/raw/`, no `.env`, and no file over 5 MB | always |
| F12 | Every dependency is pinned | Every line of `software/requirements.txt` has `==` | C6 |
| F13 | The writing rules hold | No em dash in any Markdown file outside `planning/` and `.claude/` | always |

## Milestone gates, by a person with the agent

Four milestones, and the clock for them is in `plan-b-simulated.md`.

| Milestone | When | What must be true |
|---|---|---|
| M1 | The page renders from a fixture, after C8 | The UI gate |
| M2 | The simulator plays the day end to end, the 23:00 hard checkpoint, after B4 and B5 | The demo gate and the UI gate |
| M3 | The freeze, 01:00 Sunday | The demo gate, the pitch gate, and the fallback gate |
| M4 | Before judging, 09:00 Sunday | Every gate, and the table routine in `../pitch/checklist.md` |

### The demo gate: the storyboard, beat by beat

The demo is the table in `plan-b-simulated.md`, and each beat has one thing a person can see.

| Beat | Time | It passes when |
|---|---|---|
| 1 | 0:00 | Before Play there is a headline, a night scene, one Play button, the simulation banner, and not one digit on the page |
| 2 | 0:10 | Nothing on the screen moves or asks for attention while the speaker talks |
| 3 | 0:20 | The real leaf is resting and still, and the page says in words that the simulation is driving it |
| 4 | 0:30 | One press of Play starts the day, the sun rises along a path, the sky warms, and the bars climb, with no second control needed |
| 5 | 0:40 | The leaves on the screen bend over about four seconds, the real leaf bends within a third of a second of them, the Bench bar falls away from the Sun bar, and the figure falls into shade |
| 6 | 0:50 | Dragging the cloud over the sun drops the Sun bar within a quarter of a second, the leaves relax, and they bend again when it leaves |
| 7 | 1:05 | The sun sets, the sky cools, the leaves rest, on the screen and on the table |
| 8 | 1:15 | The result card takes the screen, shows [X], [Y], and [W] with the word "simulated", and the live bars are gone |
| 9 | 1:25 | Nothing new appears, and nothing moves |
| Reset | between judges | "Reset the day" returns everything to beat 1 in under five seconds, leaf included |

The whole run, from the press of Play to the result card, is between 55 and 75 seconds.

### The UI gate

- The 28 row scorecard in `../software/mockup-prompt.md`, run against the built page and not the mockup, every row PASS with the state and the element named.
- The playbook's checklist through the `hackathon-ui-polish` skill, less the mobile layout, which is dropped on purpose.
- The 3 second test, done by a person standing a metre from the demo laptop, and never by the agent.
- Nothing on the page under 18 px.

### The pitch gate: the screen and the speaker never disagree

- Every figure the speaker says is on the result card, with the same value and the same label.
- Every sentence in `../pitch/script-plan-b.md` that describes the screen is true of the screen: "drag that cloud", "watch the screen, and watch the leaf", "that card says what we left out".
- The banner's words match the script's words: "simulated", "the simulation drives this leaf".
- The date on the screen is the demo day, "5 July 2013, the sunniest July day in the PVGIS typical year for Houston, modelled", and the pitch's "three in the afternoon in July" is a row the screen can show.
- Card 1 and card 2 in `../pitch/placards.md` carry the same figures and the same list of what was left out.
- No claim about temperature, health, or lives appears anywhere on the screen.

### The fallback gate

- A recorded simulator run is committed under `fixtures/` and replays to the same result card.
- The screen recording exists, on the laptop and on a phone, and plays.
- With the board unplugged the simulation still runs, and the recovery lines in the script match what the page then shows.
- The playbook's demo day test, through the `hackathon-testing` skill, at 30, 15, and 5 minutes before judging.

### The submission gate

- The README passes the `hackathon-readme` skill's 10 second test and its pre-submission checklist.
- The submission says "simulated" in its first paragraph.
- Every library, every dataset, and the build agent are cited: `pvlib`, `trimesh`, `rtree`, FastAPI, uvicorn, pyserial, PVGIS, Houston METRO if the analysis ships, and Devin.
- The prior work statement links the planning repo.

## The gate report

The build agent ends every reply with this table, filled in, and appends it to `GATES.md` with the commit hash.

```text
Package: [ID]   Commit: [hash]   Command: python tools/gates.py --package [ID]   Exit: [code]

| Gate | Result             | Evidence                                   |
| F1   | PASS / FAIL / NOT YET | [the line of output, or the package that switches it on] |
| ...  |                    |                                            |
| F13  |                    |                                            |

Regressions since the last report: [none, or the gate and the cause]
Milestone gates due next: [M1 to M4, and what is still open in them]
Anything in the demo, the pitch, or a checklist that this package makes harder: [plainly]
```

The last line is the one that matters most.
A package can pass every fast gate and still make the demo worse, and the agent is asked to say so without being asked.
