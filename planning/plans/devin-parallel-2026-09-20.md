# Two Devins in parallel, Sunday 2026-09-20

Written by the planner at 08:30, on abba's instruction.
Submission is at 11:00, and nothing touches the page after 10:00.
This file supersedes the ordering in `devin-todo-2026-09-20.md`, and keeps that file's working rules.

## The to-do list

| # | Work | Owner | Branch | Pull request open by |
|---|---|---|---|---|
| 0 | Merge pull requests 8, 9, 10, 11 into `main` | abba | - | 08:40 |
| W1 | The hero landing section | abba's Devin | `feat/hero-landing` | 09:10 |
| W2 | The simulation interface, one screen | abba's Devin | `feat/simulation-interface`, from W1 | 09:50 |
| W3a | The design component, with a plan drawing | Ameya's Devin | `feat/roof-designer` | 09:20 |
| W3b | The design component drives the 3D roof | Ameya's Devin | `feat/roof-designer-3d`, from W3a | 09:50 |
| R | Review every pull request, run the full suite, check it in a browser | planner | - | as each opens |
| M | Merge, deploy, README screenshot, video | abba | - | 10:00 to 10:45 |

W3b and the second half of W2 are stretch.
A pull request that is not open by its time is cut, and the page ships without it.
Cutting is cheap here, because every row above is a working increment by itself.

## Who may touch what

Two agents work on one page at once, so the files are divided, and the division is the whole point of this plan.

| File | abba's Devin | Ameya's Devin |
|---|---|---|
| `software/page/index.html` | everything above the comment `<!-- 5. configuration -->` | one new `<section id="designer">` directly before `<footer class="foot">`, one `<link>`, one `<script>` |
| `software/page/style.css` | yes | no |
| `software/page/app.js`, `console.js` | yes, the placing of nodes only, no simulation logic | no |
| `software/page/build_day.py`, `day.json` | yes, W2 only | no |
| `software/page/designer.js`, `designer.css` | no | yes, new files |
| `software/page/scene.js` | no | W3b only |
| `software/tests/test_page.py` | the hero and layout tests | the one line that adds `designer.js` to `SCRIPTS` |
| `software/tests/test_designer.py` | no | yes, a new file |
| `software/h1/`, `software/api/`, `data/`, `rules.js`, `flectofin.js` | no | no |

If a task turns out to need a file outside its column, stop and say so on the pull request.
Do not widen the scope silently.

## Traps the test suite sets, read before writing a word

- `test_no_figure_for_cost_yield_energy_or_water_saved` searches the page and its scripts for substrings.
  One of them is `roi`, so a class name or a word such as "heroic" fails the suite.
  The word "hero" is safe.
- `test_there_is_no_decorative_top_bar` forbids any `<header` tag.
  The hero is a `<section>`, so that test stays as it is.
- `test_the_screen_is_the_five_regions_the_console_needs` needs the five markers it names, with the overview before the inspector.
- `test_console_type_never_drops_below_eighteen_pixels` and `test_touch_targets_stay_at_least_forty_eight_pixels` read `style.css`.
  `designer.css` follows the same two rules even though the test does not read it.
- `test_the_page_fetches_nothing`: no `http://` or `https://` in a served file outside a comment, no font from a network, no CDN.
- Run `python -m pytest software/tests -q` in full, and `node --check` on every changed script, before every pull request.
- An expected value that does not match is reported, never edited to make a test pass.

## W1. The hero landing section

About 35 minutes.

- **Why.** A judge decides in three seconds what this is.
  Today the page opens straight onto a 3D roof with no name on it.
- **Do.** A `<section class="hero" id="hero" aria-labelledby="hero-title">` as the first child of `<main>`.
  It holds the mark from `favicon.svg` inline, the name "Flecto Shade" as the page's only `h1` with `id="hero-title"`, and the tagline "A simulated shade house roof that gives every bed its own light and rain."
  Under it, one sentence of proof taken from `day.json`, written by `app.js` when the day loads: the date, the number of zones, and that they gave different answers to the same storm.
  Three badges, each a glyph and words as well as a colour: "Simulated", "Sun: NASA POWER, modelled. Rain: NOAA gauge, 2023", "Built with Devin, by Cognition".
  One primary button, "See the roof decide", which moves focus and scroll to the stage.
  One quiet link, "Design your own roof", to `#designer`, which Ameya's Devin is building.
  The stage's title becomes an `h2` and keeps `id="stage-title"`.
- **The checklist it must pass.** `.claude/skills/hackathon-ui-polish/references/ui-checklist.md`, read through this project's own palette and type rules, which outrank its Tailwind defaults.
  Three colours at most, one type family, one primary action, visible focus, contrast of 4.5 to 1 for text, no sideways scroll at 390 px, and the three second test: name, what it does, and what to press.
- **Done when.**
  - At 1440 by 900 the hero and the top of the roof are both in view, so the page invites the scroll. The hero is at most 60 percent of the viewport's height.
  - At 390 px wide the hero fits one screen with its button in view.
  - The button lands on the stage and the run control is reachable by keyboard from there.
  - With `prefers-reduced-motion` the scroll is instant.
  - A new test, `test_the_hero_says_what_this_is`, checks the `h1`, the tagline, the word "Simulated", one primary button, and no `<header`.
- **Never said.** No figure for the year, no claim about yield, soil, water or cost.

## W2. The simulation interface

About 40 minutes, from the W1 branch.

- **Why.** Running the day is the demo.
  The control, the roof, the hour and the three answers must be one thing a judge sees at once, not four panels down a scroll.
- **Do, in this order, and stop where the clock says.**
  1. The storm plays in 5.0 seconds an hour: task T1 of `devin-todo-2026-09-20.md`, unchanged. About 15 minutes, and it is the part that must land.
  2. At 1200 px and wider, a grid: the stage in the centre and largest, the hour slider and its readout directly under the roof, the zone overview as a column on the right. The inspector and the configuration stay below.
  3. When the run ends, the overview column shows a plain success state: the date, one row a zone with its roof position and its reason, and "Play again".
     Every figure on it comes from `day.json`. No figure for the year.
- **Done when.**
  - At 1440 by 900, scrolled to the stage, with no further scrolling: the run button, the whole roof, the hour slider, and the roof position and reason of all three zones are in view.
  - A full run plays to 23:00, the storm shows three different answers, and the browser console shows no errors.
  - Every control keeps its `id`.
  - Below 1200 px the order is unchanged from `main`.

## W3a. The design component, with a plan drawing

About 50 minutes. New files only, plus three lines in `index.html` and one in `test_page.py`.

- **Why.** The release checklist asks for a flow the farmer drives.
  Today a farmer can set what a zone wants, and cannot set what the roof is.
- **What the farmer adjusts.** The number of beds, 1 to 4. The bays across each bed, 2 to 5. The bays along the house, 2 to 8.
  The bay's size is read from `ShadeHouse.planStructure(zoneCount).cell`, never typed.
  Each control is a labelled stepper of 48 px with its limits announced.
- **What changes in answer, at once and with no network.**
  - A plan drawing in inline SVG: beds, bays, one circle a module, zone dividers, a scale bar in metres.
  - Design arithmetic, labelled "design arithmetic, not a performance result": modules in total, modules a bed, roof area in square metres, bed area in square metres.
  - For the simulated day already loaded, the rain each bed admitted as a volume: the simulated millimetres from `day.json` times the bed's area, in litres, labelled "simulated".
  - One honest line: "The simulated day is worked out for each square metre of bed, so a larger house changes how much area each answer covers, and does not change the answer."
- **Shape of the code.** `designer.js` exposes `root.Designer = { plan: plan, mount: mount }`.
  `plan(design, cell)` is a pure function returning the counts, the areas and the module centres, so it runs under `node` in the test.
  `mount(host, day)` builds the controls and the drawing.
  It dispatches a `designchange` event on `document` carrying the design, and does nothing else to the rest of the page.
- **Done when.**
  - `software/tests/test_designer.py` runs `plan` under `node` for three designs and checks the counts and areas by hand arithmetic, checks the limits refuse a value outside them, and checks `designer.js` and `designer.css` against the substring and network rules above.
  - Every stepper works by keyboard, and the drawing has a text alternative that states the same counts.
  - At 390 px there is no sideways scroll.
- **Never said.** No cost, no yield, no water saved, no claim about a physical roof.
- **Pull request 5.** Its `watering-model.js` is a different model of the same farmer flow, and it conflicts with `main`.
  Read it for ideas and copy nothing from it without saying so in the pull request.

## W3b. The design drives the 3D roof

Stretch, from the W3a branch, only if W3a is open by 09:20.

- `scene.js` holds `BAY_COLUMNS_PER_ZONE` and `BAY_ROWS` as constants.
  Make them fields of the scene's state with those values as defaults, add `setDesign({ bayColumnsPerZone, bayRows })` to the object `create` returns, and rebuild the structure the way a change of zone count already does.
  `app.js` listens for `designchange` and calls it. That one listener is the only line this task adds outside its own files, and it is agreed here.
- **Done when.** Every existing test passes unchanged, the default design renders a roof identical to `main`, and each limit of the steppers renders a whole roof with the camera still framing it.
- If it is not working by 09:45, close the branch and say so. W3a stands without it.

## How each pull request is handed back

The title uses `feat:`, `ui:` or `fix:`.
The body follows `.github/pull_request_template.md`, states the commands run with their real output, names what was not tested, and attaches a screenshot at 1440 by 900 and one at 390 px.
The planner reviews it, runs the full suite and the page, and abba merges.
