# Hardware

CAD lives in a cloud CAD tool with its own version history.
Onshape is the default suggestion because it is free for students and runs in the browser.
The team confirms the tool at the next meeting.

## Subdirectories

| Directory | Role | Owner |
|---|---|---|
| `leaves/` | Mechanism | see `AGENTS.md` |
| `frame-rig/` | Structure and rig | see `AGENTS.md` |
| `electronics/` | Electronics | see `AGENTS.md` |
| `exports/` | Milestone exports from all three | the part's owner |

Each has a README saying what belongs there.
The hotspot files `frame-rig/linkage.md` and `electronics/pinout.md` are the two contracts between these directories, see `../AGENTS.md`.

## Documents

| Part or assembly | Link | Owner |
|---|---|---|
| (none yet) | | |

## Exports

Only milestone exports are committed, under `hardware/exports/`.
Name them `<part>-<YYYY-MM-DD>.step` or `.stl`.
Do not commit native CAD files.
If a single export exceeds about 50 MB, stop and set up Git LFS as its own task.
