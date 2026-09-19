# Gates: what the build is checked against, every time

The demo, the pitch, and the checklists are the definition of done, and code that passes its own tests but breaks one of them is not done.
This file turns them into gates.
A gate is either something a command can check, or something a person must look at, and the two are never mixed, because "the agent says it checked" is not a check.

This file is aimed at Plan D, `plan-d-louvre-roof.md`, the simulated smart louvre roof.
The version written for the bus stop is in the git history.

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
| F2 | It runs with no network | With `socket.socket` patched to raise, every build command in the packages exits 0, and once the page exists, it is served locally and answers | S1, then H2 |
| F3 | The page fetches nothing from the internet | No `http://`, `https://`, or `//` address in any `src`, `href`, `url(`, or `import` in any `.html`, `.css`, or `.js` file under `software/` | H2 |
| F4 | Every output file has the schema its package gives | A test reads each processed CSV and asserts its columns, their order, and its row count: 8,760 for the year and the weather, 26,280 for the simulation | S1, then H1 |
| F5 | Nothing simulated is called measured | A test reads every label the page and the result card can show and asserts the word "simulated" or "modelled" is present on every figure, and the word "measured" is absent | H2, then H3 |
| F6 | Every assumed constant is declared | Every named constant the packages mark ASSUMED appears in the README's table of assumptions with its value, in a test that compares the two | H1 |
| F7 | The rules are deterministic, and only the rules act | Two runs of the simulation give identical bytes, every `state` is one of the names in H1's nine rules, no RAIN_OPEN occurs where `ghi` is 0, and no zone that opted out takes in rain | H1 |
| F8 | The spoken numbers come from the code | The figures the script says are read from `data/processed/headline.json`, which the build writes, and the result card shows the same values, in a test | H3 |
| F9 | The planning record is untouched | `git diff --name-only` against the last merge shows nothing under `planning/` | always |
| F10 | The package stayed in its files | The changed files are a subset of the package's "may create" list, passed to the command as an argument | always |
| F11 | Nothing private or bulky is committed | `git ls-files` shows nothing under `data/raw/`, no `.env`, and no file over 5 MB | always |
| F12 | Every dependency is pinned | Every line of `software/requirements.txt` has `==` | S1 |
| F13 | The writing rules hold | No em dash in any Markdown file outside `planning/` and `.claude/` | always |
| F14 | Every sourced number has its source | Every row of `data/crops.csv` has a source address in both source columns, in a test | H1 |

## Milestone gates, by a person with the agent

| Milestone | When | What must be true |
|---|---|---|
| M1 | The simulation runs for the whole year, after H1 | The year's summary exists, and a person has read ten rows of it and they make sense |
| M2 | The page plays one day end to end, the 23:00 hard checkpoint, after H2 | The demo gate and the UI gate |
| M3 | The freeze, 01:00 Sunday | The demo gate, the pitch gate, and the fallback gate |
| M4 | Before judging, 09:00 Sunday | Every gate, and the table routine in `../pitch/checklist.md` |

### The demo gate, beat by beat

The demo is the table in `plan-d-louvre-roof.md`, and each beat has one thing a person can see.

| Beat | Time | It passes when |
|---|---|---|
| 1 | 0:00 | Before Play the roof is shut, three zones are named with their crops, there is one Play button, the word "simulated" is on the page, and there is not one digit on it |
| 2 | 0:20 | Nothing on the screen moves while the judge holds the printed fin |
| 3 | 0:30 | One press of Play starts the day, the sun rises, every fin opens, and three light gauges fill, with no second control needed |
| 4 | 0:45 | The fern zone's fins shut when its gauge reaches 8 mol, the hydrangea zone's about an hour later at 12 mol, and the blueberry zone stays open: the three zones visibly stop behaving as one roof |
| 5 | 0:55 | Rain appears over all three zones, the hydrangea's fins reopen and its soil gauge climbs to full, the blueberry stays shut with the words "wet enough", and the fern stays shut with the words "opted out": three zones, three reasons, each in words |
| 6 | 1:10 | The result card takes the screen: light against target per crop, and the rain's share of each zone's water, each with the word "simulated" |
| 7 | 1:20 | The year by month shows, the wet season and the dry season plain to see, and nothing moves after it |
| Reset | between judges | One control returns everything to beat 1 in under five seconds |

The whole run, from the press of Play to the result card, is between 55 and 75 seconds.
The day that plays is 3 June 2023, sun until mid afternoon and then 42 mm of rain in two hours, named on the screen with its date.

### The UI gate

- The playbook's checklist through the `hackathon-ui-polish` skill, less the mobile layout, which is dropped on purpose.
- The 3 second test, done by a person standing a metre from the demo laptop, and never by the agent: what is this, in three seconds.
- Nothing on the page under 18 px, three colours plus neutrals, and green, orange, and red kept for status.
- A skeleton while loading, a human sentence when a file is missing, and no spinner.

### The pitch gate: the screen and the speaker never disagree

- Every figure the speaker says is on the result card, with the same value and the same label.
- Every sentence in the script that describes the screen is true of the screen.
- The page says in words where the sun and the rain come from: the sun a modelled satellite product, the rain one measured gauge, both the Orlando Executive Airport gauge near Apopka in 2023.
- The page credits the fin to ITKE, and never says or implies "first", "measured", "maintenance free", or any figure for cost, yield, energy, or water saved.
- The full list of words the team never says is in `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md`, and the page is read against it.

### The fallback gate

- A recorded run of the demo day is committed and replays to the same result card.
- The screen recording exists, on the laptop and on a phone, and plays.
- The playbook's demo day test, through the `hackathon-testing` skill, at 30, 15, and 5 minutes before judging.

### The submission gate

- The README passes the `hackathon-readme` skill's 10 second test and its pre-submission checklist.
- The submission says "simulated" in its first paragraph.
- Every library, every dataset, every source for a crop figure, and the build agent are cited.
- The prior work statement links the planning repo, and says the project changed direction during the event.

## The gate report

The build agent ends every reply with this table, filled in, and appends it to `GATES.md` with the commit hash.

```text
Package: [ID]   Commit: [hash]   Command: python tools/gates.py --package [ID]   Exit: [code]

| Gate | Result             | Evidence                                   |
| F1   | PASS / FAIL / NOT YET | [the line of output, or the package that switches it on] |
| ...  |                    |                                            |
| F14  |                    |                                            |

Regressions since the last report: [none, or the gate and the cause]
Milestone gates due next: [M1 to M4, and what is still open in them]
Anything in the demo, the pitch, or a checklist that this package makes harder: [plainly]
```

The last line is the one that matters most.
A package can pass every fast gate and still make the demo worse, and the agent is asked to say so without being asked.
