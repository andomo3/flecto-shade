# Checklist: who builds what, in what order, and how three agents share one repo

The live board for the build.
`AGENTS.md` holds the rules, `planning/plans/plan-d-louvre-roof.md` holds the plan, and this file holds the state.
`planning/README.md` says which files under `planning/` are current and which are only the record, and `planning/playbook.md` is the team's HackMIT playbook, for the pitch, the screen, the README, and the testing.
Read all three before doing anything.

## The team

Three people, each driving a Devin agent on their own laptop, all in this one repo.

| Person | Role | Owns these directories | Packages |
|---|---|---|---|
| Abba | Software engineering, and the integrator who merges | `tools/`, `software/page/`, `pitch/`, the root files | G1, H2, H3 |
| Ameya | Data engineering | `data/`, `software/h1/`, `software/tests/` for S1 and H1 | S1, H1 |
| Shannon | The roof layout, and whatever the team agrees out loud now that the printed fin is cut | `data/roof-layout.json` | K2, optional |

An agent works only on its own person's packages, and only in that person's directories.
If a package seems to need a file someone else owns, stop and tell your person, who asks the owner.

## How three agents share one repo without colliding

1. **One package, one branch, one owner.** Branch names are `pkg/ID`, for example `pkg/S1`. Never commit to `main` directly.
2. **Claim before you start.** Set your package's status below to `in progress`, with the branch name, in a commit of its own on your branch, and push the branch, so the others can see it on GitHub.
3. **Edit only your own section of this file.** Each person has a section below, kept apart on purpose so that git can merge the edits. Never touch another person's section.
4. **Pull before you branch, rebase before you ask for a merge.** `git fetch`, then `git rebase origin/main`, then run your checks again, because someone else's merge may have changed what you depend on.
5. **Only Abba merges into `main`**, one package at a time, after running the package's acceptance commands once by hand and reading the diff. Nobody merges their own work.
6. **Shared files have one owner.** `software/requirements.txt` and `.gitignore` belong to Ameya's S1, and after S1 is merged any change to them goes through Abba. `AGENTS.md`, `CHECKLIST.md`'s structure, and everything under `planning/` belong to Abba.
7. **Gate reports never collide.** Each package writes its own file, `gates-log/ID.md`, and no agent writes to another package's file.
8. **An interface is a file with a schema.** Packages meet only through the files named under "Interfaces" below. If a schema has to change, stop, and the two owners agree the change before either side writes code.
9. **If you are blocked by a package that is not merged yet**, do not build a stand in for it and do not reach into its branch. Say so, and take the next package in your own section that is not blocked.
10. **Say which agent you are.** Start every reply to your person with the package ID and the branch, so three conversations do not get confused.

## Before any package, on every laptop

- [ ] `git clone` or `git pull`, and read `AGENTS.md`, this file, and the plan.
- [ ] Python 3.13 is installed, and a virtual environment exists at `.venv/`, which is ignored.
- [ ] The two raw data files are in place. `data/raw/` is ignored by git on purpose, so each laptop fetches its own copy:
  - `data/raw/nasa-power/power-hourly-orlando-executive-2023.csv`, from the address in `planning/plans/packages/S1-solar-2023.md`, expected sha256 `c81490d249cb1fc857b0edf44c54d6fcdbc7c1e5b30b326310138a10f25cefc4`.
  - `data/raw/isd-rain/72205312841-2023.csv`, from `https://www.ncei.noaa.gov/data/global-hourly/access/2023/72205312841.csv`, expected sha256 `d26366ed5b470b8a79d0c447b08b693b7b77f810bc8ee7a138c1a75682c64f08`.
  - NASA may stamp a new date into the file's header when it is fetched again, which changes the sha256 and nothing else. If only that checksum differs, check that the 8,760 data rows give the sums in S1's tests, and carry on. If the rain file's checksum differs, stop and tell Abba.
  - Abba's laptop already has both, checked on 2026-09-19.
- [ ] Only Ameya's laptop strictly needs the raw files. Abba's and Shannon's packages read the processed files, which are committed.

## Interfaces, the only places where packages meet

| File | Written by | Read by | Schema lives in |
|---|---|---|---|
| `data/processed/year-apopka-2023.csv` | S1 | H1 | `planning/plans/packages/S1-solar-2023.md` |
| `data/processed/sim-apopka.csv` and `sim-summary-apopka.csv` | H1 | H2, H3 | `planning/plans/packages/H1-zones-light-rain-soil.md` |
| `data/crops.csv` | H1 | H2, H3 | the same |
| `data/roof-layout.json` | K2 | H2 | this file, under K2 |
| `data/processed/headline.json` | H3 | the pitch, and every test that checks a figure | `planning/plans/packages/H3-result-card.md` |
| `software/page/headline.json`, an identical copy written in the same run | H3 | the page, because `software/page/` is the only folder served | the same |

## Order, and what can run side by side

```text
Abba:     G1 ------------------> H2 ----------> H3 ----> pitch figures
Ameya:    S1 ------> H1 ----------^
Shannon:  K2 (optional) - - - - ^
```

G1 and S1 start at once and depend on nothing.
H1 needs S1 merged. H2 needs H1 merged. H3 needs H2.
K2 is optional: without `data/roof-layout.json`, H2 draws a default grid with the words "default layout", as its specification says.
Until G1 is merged there is no gate command, so S1 finishes on its own acceptance checks, and runs the gates as soon as G1 lands, before anything else.

## Abba's section: software engineering and integration

| Package | Spec | Status | Branch | Done when |
|---|---|---|---|---|
| G1, the gate runner | `planning/plans/packages/G1-gate-runner.md` | not started | | `pytest tools/tests/test_gates.py` exits 0, and `python tools/gates.py --package G1 --allowed "tools/,gates-log/"` exits 0 |
| H2, the page | `planning/plans/packages/H2-page.md` | blocked by H1 | | `python software/page/build_day.py --date 2023-06-03` and `pytest software/tests/test_page.py` exit 0, and a person passes the demo gate's beats 1 to 5 |
| H3, the result card and `headline.json` | `planning/plans/packages/H3-result-card.md` | blocked by H2 | | `python software/h3/build_headline.py` and `pytest software/tests/test_headline.py` exit 0, and a person passes beats 6 and 7 and the pitch gate |
| The pitch, the polish, the README, the table | `planning/plans/pitch-plan-d.md`, with `planning/playbook.md` and the `hackathon-*` skills | the story can start now, the figures wait for H3 | | the scripts sit inside their word targets, and every figure in them is in `headline.json` |
| The live link | `planning/plans/plan-d-louvre-roof.md`, under "The live link" | waits for H2 | | Abba has put `software/page/` on Vercel by hand, the address opens in a private window and plays the day with the laptop's network otherwise unused, and it is put up again after H3 |

Integration duties, each time a package is offered for merge:

- [ ] Rebased on `origin/main`, and one commit whose message starts with the package ID.
- [ ] The package's acceptance commands exit 0 on Abba's laptop, with the network off.
- [ ] `python tools/gates.py` shows no FAIL, and no gate that passed before now fails.
- [ ] The diff touches only the package's own files.
- [ ] Any expected value the agent reported as not matching has been settled, and never by editing the value.
- [ ] Merged, pushed, and the status below set to `merged` with the commit hash.

## Ameya's section: data engineering

| Package | Spec | Status | Branch | Done when |
|---|---|---|---|---|
| S1, the 2023 sun for the Apopka area | `planning/plans/packages/S1-solar-2023.md` | done, awaiting merge | `pkg/S1` | `python data/build_solar_2023.py` and `pytest software/tests/test_solar_2023.py` exit 0 with the network off |
| H1, the crops, the rain, the light, the soil, the nine rules, the year | `planning/plans/packages/H1-zones-light-rain-soil.md` | done, awaiting merge. Built on `pkg/S1` rather than waiting for it to land, at Ameya's call | `pkg/H1` | `python software/h1/build.py --city apopka` and `pytest software/tests/test_h1.py` exit 0 with the network off |

Notes for this section:

- Every expected value in both specs was computed from the real files before any code existed. If one does not match, stop and report it. Never edit the value.
- H1's evaporation formula is marked RECALLED in its spec, which means nobody confirmed it at a source. If there is a spare ten minutes, confirm the Makkink form, its 0.65 coefficient, and the 2.45 divisor at a source, and record the address in the README.
- Two questions in H1 are the team's to answer and do not block the build: a soil bucket sized for containers or for soil, and whether the hydrangea stays.

## Shannon's section: the roof layout

| Package | What | Status | Branch | Done when |
|---|---|---|---|---|
| K1, the display fin | CUT at about 19:15 on Saturday 2026-09-19. There is no hardware, and the project is the simulation alone | cut | `pkg/K1` is not merged | never |
| K2, the roof layout | How the roof is laid out over the three zones, as data the page can draw: how many fins, how big, over what size of bed | blocked by nothing | | `data/roof-layout.json` validates against the schema below, in a test at `software/tests/test_roof_layout.py`, and `data/roof-layout.md` shows a plan view with the dimensions |

K1 was cut so that every hour goes to the simulation, the pitch, and the story.
The fin is ITKE's Flectofin, patented as EP2320015, and the page says so.

The schema for `data/roof-layout.json`, which H2 reads and nothing else does:

```json
{
  "units": "m",
  "note": "modelled layout, not a built structure",
  "fin": { "length_m": 0.0, "sheet_width_m": 0.0, "source": "modelled, after ITKE's Flectofin, EP2320015" },
  "zones": [
    { "zone": "A", "crop": "boston fern", "bed_width_m": 0.0, "bed_length_m": 0.0, "fin_rows": 0, "fins_per_row": 0 },
    { "zone": "B", "crop": "hydrangea",   "bed_width_m": 0.0, "bed_length_m": 0.0, "fin_rows": 0, "fins_per_row": 0 },
    { "zone": "C", "crop": "blueberry",   "bed_width_m": 0.0, "bed_length_m": 0.0, "fin_rows": 0, "fins_per_row": 0 }
  ]
}
```

- The zone letters and crop names must match `data/crops.csv`, which the test checks once H1 is merged.
- Every number is greater than 0, the fins in a zone must cover its bed when shut, within 10 percent, and the test checks that arithmetic.
- The sizes are Shannon's to choose, as a modelled design. Nothing about it is called built or tested.
- The simulation does not read this file. It treats a zone's roof as one open fraction, so the layout changes what the judge sees and never a number on the result card.

## Rules every agent follows, in one place

- The rules in `AGENTS.md` bind every package: all code written during the event, nothing copied from the planning repo, no AI in the roof's control loop, nothing called measured, the fin credited to ITKE, and the list of words never to write.
- The demo, the pitch, and the checklists are the definition of done, through the gates in `planning/plans/gates.md`.
- Before writing code, say which beat of the demo, which claim of the pitch, and which gate the package serves.
- End every reply with the gate report, and answer its last line: anything this package makes harder.
- If a check fails twice, stop and report. Never patch a third time.
- Commit small, one package per branch, no co-author trailers, nothing under `data/raw/`, no secrets.

## The clock

| When | What must be true |
|---|---|
| 21:00 Saturday | G1 and S1 are merged |
| 23:00 Saturday, the hard checkpoint | H1 is merged with the demo day's checks passing. The year is a bonus: its checks are reported and block nothing. If H1 is not merged, the page is drawn from the demo day's expected values in the specification, labelled "illustrative" |
| 01:00 Sunday, the freeze, the venue closes | H2 plays the demo day end to end, or the fallback is a recorded run of H1's output drawn as simply as possible |
| 07:00 to 09:00 Sunday | H3, the pitch figures read from `headline.json`, the screen recording |
| 09:00 to 10:30 | Rehearsal, the README, the submission |
| 11:00 | Submitted |
