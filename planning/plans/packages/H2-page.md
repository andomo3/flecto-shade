# H2: the page that plays one day

Written on 2026-09-19 against the output schema in package H1, before H1 had run.
If H1's real output differs from its schema, settle that first, and do not bend this package around it.
Owner: abba. It needs H1 and K2 merged.

## Goal

One page that shows the shade house roof from above, three zones, and plays 3 June 2023 in about forty seconds, with the dark hours quick and the daylight hours slow, from files the simulation already wrote.
It adds no physics: every number it shows was computed by H1.

## The shape of it

Two parts, so that the part with logic in it can be tested.

1. `software/page/build_day.py`, Python, reads H1's output and writes one small file, `software/page/day.json`, for one local day.
2. `software/page/index.html`, with `style.css` and `app.js` beside it, plain HTML, CSS, and vanilla JavaScript, which reads `day.json` and draws.
   It is served with `python -m http.server --directory software/page 8000`, and no web framework is added.

Anything that can be decided in Python is decided in Python: which words a zone shows, when a fin moves, the gauges' values at each hour.
The JavaScript only interpolates between hours and draws, because nothing here tests JavaScript.

## Inputs

- `data/processed/sim-apopka.csv`, from H1, including its `reason` column.
- `data/processed/weather-apopka.csv`, from H1, for `ghi`, `rain_mm`, and `t2m`.
- `data/crops.csv`, from H1, for each zone's crop, light rule, and target.
- `data/roof-layout.json`, from K2, for how many fins sit over each bed and how big they are.
  If it is absent, draw each zone with a default of 4 rows of 6 fins, and show the words "default layout" in the footer.

## `day.json`

```json
{
  "label": "simulated",
  "date_local": "2023-06-03",
  "place": "Orlando Executive Airport gauge, near Apopka, Florida",
  "sources": {
    "sun": "NASA POWER, satellite product, hourly means, modelled",
    "rain": "NOAA ISD gauge 72205312841, measured"
  },
  "credit": "The fin is the Flectofin, by ITKE, University of Stuttgart, patented as EP2320015.",
  "hours": [ { "local_hour": 0, "ghi": 0.0, "rain_mm": 0.0, "t2m": 0.0, "play_seconds": 0.5 } ],
  "zones": [
    {
      "zone": "A", "crop": "boston fern", "light_rule": "dli", "light_target": 8,
      "rain_ok": 0, "fin_rows": 4, "fins_per_row": 6,
      "hours": [ { "local_hour": 0, "open_fraction": 0.0, "light_mol_so_far": 0.0,
                   "soil_mm": 0.0, "rain_in_mm": 0.0, "state": "NIGHT", "words": "Night" } ]
    }
  ]
}
```

24 entries in every `hours` list, local hours 0 to 23, America/New_York.
`play_seconds` is how long the page spends on that hour: 0.5 where the hour's `ghi` is 0, and 2.4 where it is above 0.
It is decided in `build_day.py`, from the two named constants `NIGHT_HOUR_SECONDS` and `DAY_HOUR_SECONDS`, so that a test can check the demo's timing, and `app.js` only obeys it.
`soil_mm` is drawn against the bucket's 60 mm, with marks at 18, 30, and 54.

The words for each state, fixed here so the screen and the speaker agree:

| `state` | `reason` | `words` |
|---|---|---|
| NIGHT | | Night |
| LIGHT_OPEN | | Open: still needs light |
| SHADE | | Shut: it has had its light for today |
| HEAT_SHADE | | Partly shut: too hot |
| RAIN_OPEN | | Open for the rain: the soil is dry |
| RAIN_SHUT | `opted_out` | Shut: this crop opted out of rain |
| RAIN_SHUT | `wet_enough` | Shut: the soil is wet enough |
| RAIN_SHUT | `no_drying_time` | Shut: no daylight left to dry the leaves |
| RAIN_SHUT | `hard_rain` | Shut: the rain is too hard |

## What the page shows

- The roof from above, three beds side by side, each under its grid of fins. A fin is drawn open as a thin line with the bed visible beneath, and shut as a filled leaf shape that covers it.
- Per zone: the crop's name, a light gauge that fills toward its target, a soil gauge, and the zone's words.
  The blueberry has no light target, so its gauge shows the light received with no target mark, and says "shade rule".
- The sky: a strip whose colour follows `ghi`, and rain drawn over all three beds in the hours it falls.
- The clock, as the local hour, and the date.
- One Play button. "Reset the day" on the `R` key and in the footer.
- A footer in words: the label "simulated", the two sources, and the credit to ITKE.

## How it plays

- Each hour plays for its `play_seconds`: half a second for a dark hour, and 2.4 seconds for a daylight hour.
  A flat 2.5 seconds an hour would open the demo with 15 seconds of night in which nothing moves, and would put every beat late against the spoken script.
- On the demo day that puts the fern's fins shutting 15 seconds after Play, the storm starting about 25 seconds after Play, and the result card 38.6 seconds after Play, which is the table in `../plan-d-louvre-roof.md`: 0:45, 0:55, and 1:10 with Play at 0:30.
- Gauges move linearly between an hour's value and the next.
- A fin changes at the hour boundary, over 1.5 seconds, and never faster: the screen shows a slow roof.
  A change that starts at the end of the daylight runs its full 1.5 seconds across the short dark hours that follow.
- When the last hour ends, the page shows the result card, which is package H3, and until H3 exists it shows the three zones' end of day values in a plain table.

## States to build

1. Before Play: the roof shut, three zones named, the Play button, the word "simulated", and not one digit anywhere on the page.
2. Morning: all open, three gauges filling together.
3. The fern shut, the other two open.
4. The fern and the hydrangea shut, the blueberry open.
5. The rain: the hydrangea open for it, the blueberry shut as wet enough, the fern shut as opted out, each with its words. This is the hero frame, and the screenshot for the README.
6. Evening and night.
7. The end of day table, until H3 replaces it.
8. Loading: grey skeleton shapes, no spinner.
9. `day.json` missing or unreadable: "The day's file is missing. Run python software/page/build_day.py, then reload."
10. `roof-layout.json` absent: the default grid and the words "default layout".

## Constraints

- No address beginning `http://`, `https://`, or `//` anywhere in the three page files. No CDN, no web font, no library.
- System font stack. Nothing under 18 px. Three colours plus neutrals, sky, sun, and leaf, with green, orange, and red kept for status.
- Spacing in multiples of 4 px, rounded corners, soft shadows, laptop layout only at 1440 by 900.
- Text contrast at least 4.5 to 1 against every sky colour.
- The words "measured", "first", "maintenance free", and "weatherproof" appear nowhere, except "measured" inside the rain source line, where it is true.
- No figure for cost, yield, energy, or water saved.

## Steps

1. `build_day.py --date 2023-06-03`. Check: the tests below.
2. The static page with state 1 only. Check: it opens with the network off, and no digit is on it.
3. Playback: the clock, the sky, the gauges. Check: Play to the end takes 38.6 seconds within 2, by a timer.
4. The fins and the words. Check: a person walks states 2 to 6 against H1's demo day table, hour by hour.
5. States 7 to 10. Check: renaming `day.json` shows state 9, and removing the layout file and rebuilding shows state 10.

## Acceptance

- `python software/page/build_day.py --date 2023-06-03` exits 0 with the network off.
- `pytest software/tests/test_page.py` exits 0.
- A person passes the demo gate's beats 1 to 5 in `planning/plans/gates.md`, standing a metre from the laptop.

Test cases, from H1's asserted demo day:

- `day.json` has 24 hours, three zones A, B, and C, and the label "simulated".
- Zone A: `state` is LIGHT_OPEN at local hours 6 to 10 and SHADE at 11, and `light_mol_so_far` at the end of 10 is 8.08 within 0.1.
- Zone B: SHADE at 12, RAIN_OPEN at 15 and 16, `soil_mm` 49.03 at the end of 15 and 59.75 at the end of 16, each within 0.2.
- Zone C: RAIN_SHUT at 15 with the words "Shut: the soil is wet enough". The test carries a comment that this rests on a margin of 1.2 mm.
- Zone A at 15: the words "Shut: this crop opted out of rain".
- The hours list has `rain_mm` 23.9 at local 15 and 18.5 at local 16.
- `play_seconds` is 0.5 in every hour whose `ghi` is 0 and 2.4 in every other hour. On the demo day 14 hours have `ghi` above 0, local hours 6 to 19, and 10 do not, so the sum is 38.6 within 0.1.
- The `play_seconds` of local hours 0 to 10 sum to 15.0 within 0.1, which is when the fern's fins shut, and those of local hours 0 to 14 sum to 24.6 within 0.1, which is when the storm starts. These three values were computed by the planner from S1's processed year for 2023-06-03, before any page code existed.
- Every `words` value is one of the nine in the table above.
- The three page files contain no external address, by the same pattern gate F3 uses.
- The page files do not contain the forbidden words, with the one allowed use of "measured".

## Files

May create: `software/page/build_day.py`, `software/page/index.html`, `software/page/style.css`, `software/page/app.js`, `software/page/day.json`, `software/tests/test_page.py`, and the gate test `software/tests/test_gate_f5_labels.py`.
The gate test asserts what `../gates.md` says for F5 and nothing more: every label the page can show carries "simulated" or "modelled", and "measured" appears only in the rain source line.
Must not touch: `planning/`, `data/`, `software/h1/`, and anything in `hack-mit`.

## Gates it switches on

F3 and F5, and the demo gate's beats 1 to 5.

## For the polish pass

Use the `hackathon-ui-polish` skill and the UI sections of `planning/playbook.md`: the three colour, one font system, the 8 item checklist, the premium shortcuts, and the 3 second test.
The mobile layout item is dropped on purpose.

## Estimated minutes

120, of which the last 30 are polish and can be cut.
