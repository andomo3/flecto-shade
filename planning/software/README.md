# Software

Owner: the software and data role.

## Pre-event prototype, not a submission

This repository is the team's public planning repo.
HackMIT requires all project code to be written during the hacking period, so the event repo starts empty at 11:00 on Saturday 2026-09-19 and nothing is copied into it from here.
The contract parser in `canopy/contract.py` was written on 2026-09-18 to check that the serial contract can be implemented, and it stays here, labelled, as part of the planning record.
The plan the event code is rebuilt from is in `CLAUDE.md` in this directory.

## The plan


The Python package in `canopy/` runs on the demo laptop and does three things:

- Reads the serial log line from the board, or replays a recorded run from `fixtures/` when no board is attached.
- Logs every line to a CSV under `fixtures/` so the first clean run becomes the replay forever after.
- Serves the one page app: the LED sun brightness control, and the light, flex, leaf state, and temperature difference live, readable from a metre away.

Rules:

- Python 3.12 or later, one virtual environment, pinned `requirements.txt`, no node, no build step.
- Starts with no serial port and no network.
  `--source fixture` must always work.
- `fixtures/` is demo infrastructure and is committed, never gitignored.
- Anything the page loads is vendored under `canopy/static/`, never fetched from a CDN.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r software/requirements.txt
cd software
python -m canopy serve --source fixture
```

On macOS and Linux the second line is `source .venv/bin/activate`.
