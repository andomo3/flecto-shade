# G1: the gate runner

## Goal

One command, `python tools/gates.py`, that runs every fast gate in `../gates.md` and prints the gate report.
It exists before the features do, so that every later package is checked the same way, and it grows as the gates it checks switch on.

## Why it is its own package, and an early one

A gate that is only a sentence gets skipped at three in the morning.
A gate that is a command does not.
G1 is handed over first, before any feature.

## Inputs

- `planning/plans/gates.md`, the list of gates F1 to F14 and the report format.
- Nothing else: on the day it is built the repo holds no product code, so most gates report NOT YET.

## Behaviour

- `python tools/gates.py` runs every gate and prints the report table from `gates.md`.
- `--package ID --allowed "path1,path2,..."` names the package and the files it may change, for gate F10.
- `--append` adds the report to `gates-log/ID.md`, one file per package, under a heading with the short commit hash and the local time.
  Three people's agents work in this repo at once, and one shared ledger would collide on every merge, so no package ever writes another package's file.
- Each gate is one function that returns PASS, FAIL, or NOT YET, and one line of evidence.
- A gate reports NOT YET when the thing it checks does not exist, for example no page under `software/` for F3, and names the package that switches it on.
  It never reports PASS for something that is not there.
- The exit code is 0 only when no gate is FAIL.
  NOT YET does not fail the run.
- It runs with the network off, uses the standard library and `pytest` only, and takes under 60 seconds.
- The gates that are tests, F4 to F8 and F14, are found by file name under `software/tests/`: `test_gate_f4_schema.py`, `test_gate_f5_labels.py`, `test_gate_f6_assumptions.py`, `test_gate_f7_rules.py`, `test_gate_f8_headline.py`, and `test_gate_f14_sources.py`.
  A gate whose test file does not exist yet is NOT YET, and names the package that creates it, from the table "The gates that are tests, and who writes each one" in `../gates.md`.
  G1 creates none of these six files.

## Steps

1. The skeleton: the table printer, the three results, the exit code. Check: on the empty repo it prints 14 rows and exits 0.
2. The always on gates, F9, F10, F11, F13. Check: the four tests below.
3. F1, by running `pytest` with `--ignore` for the two year files, `software/tests/test_h1_year.py` and `software/tests/test_headline_year.py`, and reading its exit code, with "no tests collected" reported as NOT YET. Then the two year files are run on their own, and the report carries one more line, "The year: PASS, FAIL, or NOT YET", which never changes the command's exit code. Check: the tests below.
4. F2, F3, and F12, each NOT YET until its directory or file exists. Check: creating a stub file flips the gate from NOT YET to a real result.
5. `--append`. Check: two runs with `--package G1` add two dated sections to `gates-log/G1.md`, change nothing else in it, and create no other file.

## Acceptance

`pytest tools/tests/test_gates.py` exits 0, and `python tools/gates.py --package G1 --allowed "tools/,gates-log/"` exits 0 on a clean tree.

Test cases, each in a temporary git repo made by the test:

- An empty repo gives 14 rows, no FAIL, and exit 0.
- A changed file under `planning/` makes F9 FAIL and the exit code 1.
- A changed file outside `--allowed` makes F10 FAIL.
- A tracked file under `data/raw/`, a tracked `.env`, or a tracked file over 5 MB each make F11 FAIL.
- An em dash in a Markdown file outside `planning/` and `.claude/` makes F13 FAIL, and one inside `planning/` does not.
- A `requirements.txt` line without `==` makes F12 FAIL.
- A page under `software/` with `src="https://..."` makes F3 FAIL, and the same address inside an HTML comment does not.
- A failing test makes F1 FAIL, and a repo with no tests makes F1 NOT YET.
- A failing test inside `software/tests/test_h1_year.py` leaves F1 at PASS and the exit code at 0, and makes the year's line read FAIL.
- `--append` twice with `--package X1` gives two sections in `gates-log/X1.md`, and `--append` without `--package` is refused with a plain message.

## Files the agent may create

`tools/gates.py`, `tools/tests/test_gates.py`, `gates-log/G1.md`.

## Files it must not touch

`planning/`, and nothing in the `hack-mit` repo.

## Honesty

The runner checks only what a command can check.
It prints, under the table, the line "Milestone gates M1 to M4 are checked by a person, see planning/plans/gates.md", so that a green run is never read as "the demo works".

## Estimated minutes

60.
