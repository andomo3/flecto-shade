# flecto-stop

hack-mit project w/ Shanon, Abba, &amp; Ameya ;p

A bus stop roof that bends into shade on its own.
Three hingeless leaves, borrowed from the bird of paradise flower, feel the sun and bend over the bench, and open again when the light is gentle.

## Status

HackMIT 2026, hacking from 11:00 Saturday 2026-09-19 to 11:00 Sunday.
The shared core, packages C1 to C9, is built: the serial contract, the sources, the derived state, the server and its page, the Houston day, the day player, and the recorder.
The measured numbers, the hardware photographs, and the video land here before the freeze.

## Run it

No network, no build step, no serial port required.

```
python -m venv .venv
.venv/Scripts/pip install -r software/requirements.txt   # .venv/bin/pip on macOS and Linux
cd software
../.venv/Scripts/python -m canopy serve --source fixture
```

Then open http://127.0.0.1:8000 and press Play.

| Source | What it is | What the page says |
|---|---|---|
| `--source serial --port-name COM3` | The board on the table | Measured today on this table |
| `--source fixture` | A run recorded earlier, replayed line for line | Replayed from a run recorded on this table |
| `--source fake` | A board that is not there | Simulation: no hardware is connected |

Add `--record` to keep every line of a live run under `software/fixtures/`, unchanged, so it can be replayed exactly.
`cd software && ../.venv/Scripts/python -m pytest tests -q` runs the tests.

## How it works

The dataset moves the sun, and only the light sensor moves the leaves.

Ten times a second the app sends the board an LED duty and a sun arm angle taken from one real Houston day, `data/processed/day-houston.csv`, so 24 hours passes in about a minute.
Nothing tells the leaves what to do: the board crosses its own light threshold and bends.
Cover the roof sensor with a hand and they relax.
The board prints one line of eleven fields back, the app derives the share of light reaching the bench, and the page draws it.

Replay mode exists for a room that defeats the threshold, and the page says so in a banner whenever it is on.

## Measured against modelled

- Measured is what a sensor on this table read during the event.
- Modelled is the solar dataset, the LED sun, and anything the shade simulation reports.
- A sensor that was never fitted reads "not fitted", never zero.

The page, the placards, and the spoken pitch use the same three rules.

## What is in here

| Path | What |
|---|---|
| `software/canopy/` | The `canopy` package: the contract, the sources, the state, the app, the day player, the recorder, and the one page |
| `software/tests/` | The tests for all of it |
| `data/` | The Houston day, and the script that rebuilds it offline from PVGIS |
| `pitch/` | The scripts, the placards, the demo runbook, the checklist, and the submission text |
| `planning/` | The planning record, Markdown only, frozen. Start at `planning/README.md` |
| `AGENTS.md` | The rules for everyone, human or agent, who works in this repo |

## Built with

Python 3.13, FastAPI, uvicorn, pyserial, pandas, pvlib, pytest, and one HTML file with plain CSS and vanilla JavaScript.
Solar data: PVGIS v5.2 typical meteorological year, (c) European Union, CC BY 4.0.

## Prior work, stated plainly

The team planned this project before the event, in public, at https://github.com/andomo3/hack-mit.
That repo holds research, specifications, the pitch, and one labelled throwaway prototype of the serial format.
No code was copied from it.
Every line of code in this repo is written during the hacking period.
