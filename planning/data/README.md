# Data

Owner: the software and data role.

Provenance of every dataset the project uses, so a claim built on public data can be audited by a judge.
Every row says what was downloaded, from where, on what date, and which processed file it feeds.
The dataset is the PVGIS hourly typical year file with `pvlib` for the sun's position, see `CLAUDE.md` in this directory and `../docs/research/adaptive-bus-stop-canopy/dataset-choice.md`.
The Voloridge challenge rewards thoughtful use of a real public dataset, and its curated set is provided at the event.
The download happens before the event, and the analysis script is written during it.
On 2026-09-19 `raw/` was still empty on the demo laptop, so the download happens at the venue, PVGIS first.
The datasets for the Voloridge analysis are listed in `../docs/research/adaptive-bus-stop-canopy/voloridge-datasets.md`, and each one gets a row below when it is downloaded.

| Dataset | Source | Downloaded | Feeds |
|---|---|---|---|
| (none yet) | | | |

Layout:

- `raw/` is gitignored.
  Everything in it is downloaded before Saturday.
- `processed/` holds the small CSVs the software reads, committed.
  Rebuilt by a script that must run with the network off.
