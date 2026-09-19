# Software

Owners: abba for the gate runner, the page, and the result card, and Ameya for the data build and the simulation.
The live board with the owners, the branches, and the status is `../../CHECKLIST.md`.

## What this folder is

This folder is planning, Markdown only.
The code lives in the repo's own `tools/`, `data/`, and `software/` directories, and every line of it is written during the event, from the specifications under `../plans/packages/`.
This file says what the software is under Plan D, `../plans/plan-d-louvre-roof.md`, and how its parts connect.
The specifications are authoritative for every schema, file name, command, constant, and figure, and this file only summarises them.

## What the software is

A simulation of a smart louvre roof over three crop zones in a shade house near Apopka, Florida, and one page that plays one simulated day of it in about a minute.
There is no hardware at all: no board, no sensor, no port to read, and nothing physical on the table.
The project is the simulation and its page.
Every figure the software produces is simulated or modelled.

The roof follows nine written, deterministic rules per zone, in the priority night, then rain, then light.
No language model and no learned model sits in the loop.
The fins react to how much light has arrived, to rain, and to the soil, and they never track the sun's position.

## The five parts

| Part | Package | Owner | Lives in | What it does | Spec |
|---|---|---|---|---|---|
| The gate runner | G1 | abba | `tools/` | One command that runs the fast gates F1 to F14 and prints the gate report | `../plans/packages/G1-gate-runner.md` |
| The sun | S1 | Ameya | `data/` | Turns the NASA POWER hourly file for 2023 into one row an hour | `../plans/packages/S1-solar-2023.md` |
| The simulation | H1 | Ameya | `software/h1/` | The crops table, the rain parser, the join, the light, the soil bucket, the nine rules, and the year's summary | `../plans/packages/H1-zones-light-rain-soil.md` |
| The page | H2 | abba | `software/page/` | Shows the roof from above and plays 3 June 2023 in about a minute, with no new physics | `../plans/packages/H2-page.md` |
| The result card | H3 | abba | `software/h3/`, and the page's card and year view | Writes `headline.json`, the one file every spoken and printed figure comes from, and shows it | `../plans/packages/H3-result-card.md` |

The tests for S1, H1, H2, and H3 live in `software/tests/`, and the gate runner's tests in `tools/tests/`.
The data side, the raw files, the processed files, and the citations, is described in `../data/README.md`.

## How the parts connect

Packages meet only through files with a schema, and the list is the "Interfaces" table in `../../CHECKLIST.md`.

```text
data/raw/ (two files, ignored by git)
   |  S1: data/build_solar_2023.py
   v
data/processed/year-apopka-2023.csv
   |  H1: software/h1/build.py --city apopka, which also reads the raw rain file
   v
data/crops.csv
data/processed/weather-apopka.csv
data/processed/sim-apopka.csv
data/processed/sim-summary-apopka.csv
   |                                  |
   |  H2: software/page/build_day.py  |  H3: software/h3/build_headline.py
   v                                  v
software/page/day.json            data/processed/headline.json
   |                                  |
   v                                  v
software/page/index.html, style.css, app.js     pitch/figures.md, generated
```

- `data/roof-layout.json`, from Shannon's package K2, is a modelled layout, plain data the page draws, and it feeds only H2's `build_day.py`, for how many fins sit over each bed.
  The simulation does not read it, so the layout changes what the judge sees and never a number on the result card.
- If `roof-layout.json` is absent, the page draws 4 rows of 6 fins per zone and says "default layout" in the footer.
- H2 adds no physics.
  Anything that can be decided in Python is decided in Python: which words a zone shows, when a fin moves, the gauges' values at each hour.
  The JavaScript only interpolates between hours and draws, because nothing here tests JavaScript.
- After H3, nobody types a number into a script, a card, or the README by hand.
- If a schema has to change, stop, and the two owners agree the change before either side writes code.

- The page reaches the result card's figures through `software/page/headline.json`, an identical copy that H3's build writes beside `day.json` in the same run as `data/processed/headline.json`, because `software/page/` is the only folder served, on the laptop and on Vercel alike.

## The live link

A static copy of `software/page/` is put on Vercel by abba, by hand, once H2 plays the day, and again after H3.
The laptop copy is the demo, and the Vercel address is the README's link and the backup.
Vercel serves the folder as it is, so there is no build step, no framework, and no change to H2, H3, or gate F3.
Nothing about Vercel is committed: no token, no setting, no `.vercel/` folder.

## The commands

Set up, once per laptop, on Windows:

```text
python -m venv .venv
.venv\Scripts\activate
pip install -r software/requirements.txt
```

On macOS and Linux the second line is `source .venv/bin/activate`.
The virtual environment is `.venv/` at the repo root, and it is ignored by git.
`software/requirements.txt` is written by S1, so the third line works only once S1 is merged.

Build and check, in the order the packages depend on each other:

```text
python tools/gates.py
pytest tools/tests/test_gates.py

python data/build_solar_2023.py
pytest software/tests/test_solar_2023.py

python software/h1/build.py --city apopka
pytest software/tests/test_h1.py

python software/page/build_day.py --date 2023-06-03
pytest software/tests/test_page.py

python software/h3/build_headline.py
pytest software/tests/test_headline.py
```

Show the page:

```text
python -m http.server --directory software/page 8000
```

Then open `http://localhost:8000` in the browser on the demo laptop.

After a package's own check passes:

```text
python tools/gates.py --package ID --allowed "files" --append
```

That writes the gate report to `gates-log/ID.md`, one file per package.
A green run never means "the demo works": the milestone gates M1 to M4 in `../plans/gates.md` are walked by a person.

## The constraints

- Python 3.13, with `pandas==2.2.3`, `numpy==2.2.3`, and `pytest==9.0.2`, every line of `software/requirements.txt` pinned with `==`.
- No other dependency unless a package names it.
  The gate runner uses the standard library and `pytest` only.
- The page is plain HTML, CSS, and vanilla JavaScript: no React, no Node, no build step, no CDN, no web fonts fetched at run time, and no web framework.
  It is served by Python's own `http.server`.
- Everything builds and runs with no network.
  Every build's test patches `socket.socket` to raise.
- Every build gives identical bytes on two runs.
- Every constant a package marks ASSUMED or RECALLED is a named constant in the code and a row in the README's table of assumptions, with its value.
- Every label the page and the result card can show says "simulated" or "modelled".
  The one allowed use of the word "measured" is inside the rain source line, where it is true of the gauge.
- The page never shows "first", "maintenance free", or "weatherproof", and no figure for cost, yield, energy, or water saved.
- The page credits the fin: "The fin is the Flectofin, by ITKE, University of Stuttgart, patented as EP2320015."
- The expected values in the specifications were computed from the real files before any code existed.
  If one does not match, stop and report it, and never edit the value.

## Where to read next

- `CLAUDE.md` in this folder: the decisions already made, the traps, and what not to build.
- `ui-brief.md`: the brief for the page, beat by beat against the demo.
- `mockup-prompt.md`: the prompt for drawing that page in a mockup tool.
- `../plans/gates.md`: what every package is checked against.
