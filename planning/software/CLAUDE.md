# software - local memory

Owner: the software and data role, abba.
This is the planning repo.
Nothing here is copied into the event repo, and the code under `canopy/` is a pre-event prototype that proved the contract, not a submission.
At the event this plan is rebuilt from scratch, in this order.

## What this directory becomes

One Python package, `canopy`, that runs on the demo laptop.
It reads the board over USB serial, or replays a recorded run, and serves one page that shows the light reaching the bench.
It also plays one real day from the dataset to the board as LED brightness and sun angle.

## Decisions that bind this directory

- The stack is Python 3.13, FastAPI, uvicorn, and pyserial, in one virtual environment with a pinned `requirements.txt`.
- The page is one HTML file with plain CSS and vanilla JavaScript, vendored under `canopy/static/`.
  No React, no Node, no build step, no CDN, no web fonts fetched at runtime.
- Live data goes to the page over Server-Sent Events, and commands come back as plain POST requests.
- It must start with no serial port and no network.
  `python -m canopy serve --source fixture` always works.
- The data moves the sun and only the photoresistor moves the leaves.
  The app sends `L` and `A` in the normal demo and never `S`.
- The number is `bench / light * 100`, averaged separately while the leaves are flared and while they are resting.
- A sensor that is not fitted shows "not fitted", never zero.

## The screen tells the story

`ui-brief.md` is derived from `../pitch/storyboard.md`: one scene, a sky, a sun, the stop, and a seated figure, with two bars that pull apart when the leaves bend.
No numbers before Play, the big figures only on the result card, one button for the judge, and every other control in a hidden drawer.
The stop is drawn from the front, the view the judge has of the rig, and each leaf is a rib and a translucent sheet: blades with sky between them when resting, petals that close the gaps when bent, every pose driven by `angle`.
`mockup-prompt.md` holds the Claude Design prompts, the twelve states, and the 28 row scorecard the mockup must pass, and "every state in the mockup prompt" in step 6 means that file.
Step 6 below builds that page, and step 4 must expose what it needs: leaf state, which sensors are fitted, the running averages for bent and resting, and whether the day has finished.

## The skeleton, in build order

Each step ends with a check, and nothing starts before the previous check passes.

| Step | Module | What it does | Check | Minutes |
|---|---|---|---|---|
| 1 | `contract.py` | Parses one line of `firmware/SERIAL_FORMAT.md` into a header, a reading, or nothing, and builds the `L`, `A`, `S`, `O`, and `P` commands. Standard library only | A test that reads the sample lines out of the contract file itself, plus a list of garbage lines that must return nothing | 20 |
| 2 | `sources.py` | Three sources with one interface, readings out and commands in: `FixtureSource` replays a file paced by `t_ms`, `FakeSource` simulates the board, `SerialSource` wraps pyserial | The fixture source yields the same readings the file holds, in order, and loops | 25 |
| 3 | `fixtures/synthetic-day.csv` | A hand made v2 stream of one fast forward day, so the page has something to show before any board exists | It parses with step 1 | 10 |
| 4 | `state.py` | Turns readings into what the page shows: the two percentages, leaf state from `angle`, cycle count, the temperature difference, which sensors are fitted | Unit tests with five or six hand written readings | 30 |
| 5 | `app.py` and `__main__.py` | FastAPI with `/`, `/events` as the SSE stream, `/health`, and POST `/play`, `/pause`, `/led`, `/sun`, `/replay-mode` | `curl /health` returns 200 and `/events` streams with the Wi-Fi off | 40 |
| 6 | `static/index.html` | The page, ported from the mockup by hand | The 3 second test from a metre away, and every state in the mockup prompt | 60 |
| 7 | `day.py` | Loads `data/processed/day-houston.csv` and sends `L` and `A` ten times a second so 24 hours play in about 60 seconds | Against the fake source, the leaves flare after sunrise and rest after sunset | 40 |
| 8 | `SerialSource` for real, and `recorder.py` | Reads the board, writes every line unchanged to `fixtures/` | The first clean run is recorded and committed, and replays | 30 |
| 9 | Replay mode | The hour twelve pivot: the app sends `S` from the day's data, and a banner says so in words | The banner shows whenever `override` is 1 and the app sent `S` | 20 |

About four and a half hours.
Steps 1 to 7 need no hardware, so they run in parallel with the engineers from 11:00.

## Pivots that land here

- Hour 8, no servo mounted sun: hide the sun angle control, stop sending `A`.
- Hour 12, threshold unreliable: replay mode, step 9.
- Hour 13, bench sensor shows no difference: the number becomes the cycle count, already derived in step 4.
- Hour 14, no temperature: hide the tile.
- Any time, serial dead at the table: `--source fixture` with the recorded run.

## What the prototype taught

- Reading the test samples out of the contract file catches a contract change the moment it happens.
- Optional fields as empty strings parse cleanly and keep "not fitted" honest.
- FastAPI 0.141, uvicorn 0.53, and pyserial 3.5 install cleanly on Python 3.13 on the demo laptop.
- Windows serial ports are named `COM3` and so on, so the port is a command line argument and never a constant.

## Open questions

- The mockup is being designed by abba, and the page is ported from it by hand, because generated React code is not used.
- Whether the city picker ships is decided last, after the core demo is rehearsed.
