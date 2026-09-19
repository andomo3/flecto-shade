# H3: the result card and the figures the pitch says

Written on 2026-09-19 against the output schema in package H1.
Owner: abba. It needs H2 merged.

## Goal

Write `data/processed/headline.json`, the one file every spoken and printed figure comes from, and show it as the result card at the end of the day and as the year by month.
The same run writes an identical copy to `software/page/headline.json`, because `software/page/` is the only folder that is served, on the laptop and on Vercel alike, and the page reads the copy beside `day.json`.
After this package, nobody types a number into a script, a card, or the README by hand.

## Inputs

- `data/processed/sim-apopka.csv` and `data/processed/sim-summary-apopka.csv`, from H1.
- `data/crops.csv`, from H1.

## `headline.json`

```json
{
  "label": "simulated",
  "place": "Orlando Executive Airport gauge, near Apopka, Florida",
  "year": 2023,
  "year_note": "An ordinary year for rain there, 2.4 percent above the 1991 to 2020 normal.",
  "zones": [
    { "zone": "A", "crop": "boston fern", "light_target_mol": 8, "days_target_met": 0,
      "rain_stored_mm": 0.0, "irrigation_mm": 0.0, "rain_share": 0.0 }
  ],
  "months": [ { "month": 1, "zone": "B", "rain_stored_mm": 0.0, "irrigation_mm": 0.0, "days_target_met": 0 } ],
  "demo_day": {
    "date_local": "2023-06-03",
    "rain_mm": 0.0,
    "zones": [ { "zone": "B", "shut_for_light_at_local_hour": 12, "rain_stored_mm": 0.0,
                 "unwanted_light_mol": 0.0, "light_mol_end_of_day": 0.0, "soil_start_mm": 0.0, "soil_end_mm": 0.0 } ]
  },
  "spoken": {
    "share_b_percent": 0, "share_c_percent": 0, "fern_days_met": 0,
    "demo_rain_mm": 0, "demo_unwanted_light_mol": 0
  },
  "never_claimed": ["measured", "yield", "cost", "energy", "water saved", "safety from disease"]
}
```

- `rain_share` is the rain stored over the rain stored plus the irrigation, for the year, and it is not given by month, because a month with no irrigation event would read as 100 percent and mean nothing.
- `unwanted_light_mol` is the light a daily light crop received after it had reached its target, which on the demo day is what opening for the rain cost the hydrangea.
- `spoken` holds the rounded figures, whole numbers, exactly as the speaker says them.

## The result card, at the end of the day

- A heading in words: "3 June 2023, simulated".
- Per zone, one row: the crop, its light against its target, when its fins shut for light, the rain it stored, and its words for the rain: opened, wet enough, or opted out.
- One line for the trade: "Opening for the rain gave the hydrangea [rain stored] mm of water and [unwanted light] mol of light it did not want."
- A "Play again" button, and a second button, "The whole year".

## The year view

- Twelve columns, one a month, and for zones B and C two stacked bars each: rain stored, and the grower's irrigation.
  The wet season and the dry season should be plain to see without reading a number.
- Under it, three sentences, read from `headline.json`: the rain's share for the hydrangea, for the blueberry, and the days the fern met its light target.
- The honesty block, in words: what is modelled, what is measured, which figures rest on assumed constants, and that the blueberry's shade figure comes from Washington State and is not Florida practice.
- Drawn as inline SVG by hand. No chart library.
  When this is polished, the `dataviz` guidance in the playbook applies: one hue per series, direct labels, no legend to decode.

## Steps

1. `software/h3/build_headline.py`, which writes `data/processed/headline.json` and then the identical copy `software/page/headline.json`, in that order, in one run. Check: the tests below, and the two files are the same bytes.
2. The result card replaces H2's end of day table, and `app.js` reads `headline.json` from beside `day.json`, by a relative address. Check: every figure on it equals the one in `data/processed/headline.json`, in a test that reads both.
   If the copy is missing or unreadable the page says "The result file is missing. Run python software/h3/build_headline.py, then reload.", and the day still plays. Check: renaming the copy shows those words.
3. The year view. Check: a person reads three bars against H1's month table.
4. `pitch/figures.md`, generated: the sentences the speaker says, with the figures filled in from `spoken`, under a line that says the file is generated and is never edited by hand.

## Acceptance

- `python software/h3/build_headline.py` exits 0 with the network off.
- `pytest software/tests/test_headline.py` exits 0.
- A person passes the demo gate's beats 6 and 7, and the pitch gate, in `planning/plans/gates.md`.

Test cases, from H1's asserted values, with H1's tolerances:

- `rain_share` for B is 0.545 within 0.03, for C 0.171 within 0.03, and for A exactly 0.
- `days_target_met` for A is 354 within 3, and for B 346 within 3.
- The demo day: `rain_mm` 42.4, B's `rain_stored_mm` 34.9 within 0.3, B's `unwanted_light_mol` 5.96 within 0.2, A's `shut_for_light_at_local_hour` 11, and B's 12.
- `spoken.share_b_percent` is `rain_share` for B times 100, rounded to a whole number, and the same for the others.
- The months for B from April to October hold no irrigation in six months of seven.
- `software/page/headline.json` is byte for byte the same as `data/processed/headline.json`, and the page files name no path outside `software/page/`.
- Every figure in the page's result card and in `pitch/figures.md` appears in `headline.json`, which is gate F8.
- The word "simulated" is on every figure, and the forbidden words are absent, which is gate F5.

## Files

May create: `software/h3/build_headline.py`, `data/processed/headline.json`, its copy `software/page/headline.json`, `software/tests/test_headline.py`, `pitch/figures.md`, and the gate test `software/tests/test_gate_f8_headline.py`.
May change: `software/page/index.html`, `style.css`, and `app.js` for the card and the year view only, and `software/tests/test_gate_f5_labels.py`, only to add the labels of the card and the year view.
Must not touch: `planning/`, `software/h1/`, the rest of `data/`, and anything in `hack-mit`.

## Gates it switches on

F5 in full, F8, the demo gate's beats 6 and 7, and the pitch gate.

## Estimated minutes

75.
