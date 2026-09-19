# The demo, as it actually runs

The table version of `planning/pitch/storyboard.md`, edited for the software that now exists.
Everything here has been run on the demo laptop.

## Starting it

One virtual environment, no network, no build step.

```
cd software
../.venv/Scripts/python -m canopy serve --source fake     # no board on the table
../.venv/Scripts/python -m canopy serve --source fixture  # this morning's recorded run
../.venv/Scripts/python -m canopy serve --source serial --port-name COM3 --record
```

Then open `http://127.0.0.1:8000` and put the browser full screen at 100 percent zoom.
`--record` writes every line the board sent to `software/fixtures/run-YYYYmmdd-HHMM-serial.csv`, unchanged, which is the fallback if the board dies later.

The page says which of the three it is running, in words, at all times.

| Source | What the page says |
|---|---|
| `serial` | Measured today on this table |
| `fixture` | Replayed from a run recorded on this table |
| `fake` | Simulation: no hardware is connected |

## The beats

| Time | Say | The table | The screen |
|---|---|---|---|
| 0:00 | "Picture Rosa." | Leaves resting, LED off | The opening state: the scene, one Play button, no numbers |
| 0:25 | "Would you press play?" | The judge presses Play | The clock starts at 00:00, the sky lifts, the sun climbs its arc |
| 0:40 | Stop talking | The LED brightens, the leaves bend together | The Sun bar and the Bench bar separate, the badge reads "Leaves bent" |
| 0:50 | "Put your hand over that sensor." | The leaves relax, then bend again | The Bench bar climbs and falls with them |
| 1:15 | The number, and what was not measured | Hands off | The result card: bent against resting, with the provenance line under it |
| 1:25 | The closing line | Silence | The result card stays up |

The day is 600 steps at ten a second, so 24 hours takes about a minute.
The clock on screen is the Houston local time of the step, not the laptop clock.

## What drives what

The dataset moves the sun: every 100 ms the app sends `L <duty>` and `A <angle>` from `data/processed/day-houston.csv`.
Nothing tells the leaves what to do.
The board reads its own photoresistor and bends when the light crosses the threshold, which is why a hand over the sensor works.

Replay mode is the exception and the page says so in a banner: "Replay mode: the leaves are driven by recorded angles, not by the light sensor."
Turn it on only if the room's light defeats the threshold, and say the recovery line out loud.

## The drawer

Every control that is not Play lives behind the drawer, so the judge sees a scene and not a dashboard.

- LED duty, 0 to 255, the sun by hand.
- Sun angle, 0 to 180, the sun arm by hand.
- Replay mode, off by default, labelled in words when it is on.
- Reset the day, which takes under a second.

Keyboard, for the speaker: space plays and pauses, R resets, D opens the drawer, Escape closes whatever is open.

## When it breaks

- The board goes quiet for two and a half seconds: the page says so itself, in a red banner, and names the USB cable and the recorded run.
  Switch the source to `fixture` and keep talking.
- Nothing serves at all: play the backup clip, apologise once, keep telling Rosa's story over it.
- A sensor was never fitted: the page reads "not fitted", never a zero, and the pitch says the same.
