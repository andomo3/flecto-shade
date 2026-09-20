# Handoff: the landing page, Sunday 2026-09-20

For whoever picks this up next, human or machine, with no memory of the session that
built it. The spec is `landing-page-2026-09-20.md` in this directory and it still
governs. This file records what was built against it, what was deliberately left out,
and the five decisions that are not mine to make.

Read the spec before this file. This is the delta, not a replacement.

## Where the work is

Branch `feat/landing-page`, cut from `b1e97a5` (which is `origin/main`).
**Nothing is committed.** The change sits in the working tree. Why not is the first
open decision below, and it matters more than it sounds.

Three files changed, all of them in `software/page/`:

| File | What changed |
|---|---|
| `index.html` | `<main class="console">` became `<main>` wrapping three new sections plus `<div class="console" id="console">`. The stage's `<h1 id="stage-title">` became `<h2 id="stage-title" tabindex="-1">The simulated roof</h2>`. |
| `style.css` | One new block, `/* the lede */`, sitting above `/* the panels */`. Two stage rules retargeted from `h1` to `h2`. One phone pass added inside the existing `max-width: 720px` query. One pre-existing comment reworded — see "The failure that was already there". |
| `app.js` | One function, `handOverToTheRoof()`, called before the `fetch("day.json")` boot. |

Nothing under `software/h1/`, `software/api/`, `data/`, `rules.js` or `flectofin.js`
was touched, as the spec requires.

## What was built

The three blocks, in the spec's order, above the untouched console.

**Block 1, the lede.** Inline mark, eyebrow ("Simulated. Built at HackMIT 2026."), the
correction device (below), the page's only `h1`, one sentence, one primary button
("See the roof decide"), the quiet line down to block 2, and a three-item provenance
strip where each item carries a word and a glyph, never colour alone.

**Block 2, `.motive`.** Story, then the bridge, then nothing. Story and bridge are both
22 px, both `--ink`, inside one bordered card. The bridge is not smaller, not grey, and
not below the fold. That is the whole point of the block and it should survive any
future edit.

**Block 3, `.does`.** The three sentences from the spec, verbatim.

### The correction device

Added at the user's request during the build, not in the original spec: the page reads
**Green house** with "Green" struck through and "Shade" written above it, so the eye
lands on "Shade house".

Markup is `.swap` → `.swap-stack` → `.swap-out` (struck) + `.swap-in` (absolute,
rotated −4°). Both are `aria-hidden`, and a `.reader-only` span carries "Not a green
house. A shade house." so a screen reader gets a sentence rather than two orphan words.

One trap, already hit and fixed once: if `.swap-in`'s `bottom` is too small, the
strikethrough on "Green" runs straight through "Shade" and the correction reads as
struck out too. It is at `.62em` with `padding-top: .95em` reserving the space above.
If you change the font size, re-check that the strike clears the written word.

## Verified, and how

Full suite, not a subset: `.venv/bin/python -m pytest software/tests -q` → **144 passed**.
`node --check` on all six served scripts → clean.

Measured in a real browser at 1440×900 and at 390×844, not eyeballed:

- Hero is **58.5%** of the viewport at 1440×900, inside the spec's 60% ceiling.
- No horizontal scroll at 390 px; the primary button's bottom edge is at 392 px against
  an 844 px viewport, so it is in view without scrolling; it is 48 px tall.
- Block order at 390 px is lede, motive, does, console.
- Contrast on all fourteen new text elements is between 4.87:1 and 13.91:1. Lowest is
  the primary button's white on moss at 4.87:1. All pass AA.
- Every new font size is ≥ 18 px.
- Clicking the button scrolls to the stage and moves focus onto `CANVAS.stage-canvas`,
  so a keyboard user is handed to the roof rather than left at the top.
- Tab order is skip link → primary button → quiet story link → stage canvas → console.
- `scroll-behavior` is `auto` globally, so nothing in CSS overrides the reduced-motion
  branch in `handOverToTheRoof()`.

**Not verified, and you should not claim it is:**

- The three-second test. It needs a person who has not seen the page. Nobody has run it.
- `prefers-reduced-motion`. The code branches on `matchMedia` and there is no CSS smooth
  scroll to fight it, but the branch was checked by reading it, not by emulating the
  media query in a browser.

## The failure that was already there

Before any of this work, `test_gate_f5_labels.py::test_measured_appears_only_in_the_rain_source_line`
was already failing on the working tree: a comment in `style.css` ended "Every ratio
noted below was measured", and gate F5 scans every served file for that word. It is now
"Every contrast ratio below was checked".

That is a one-word fix to a comment in a file this work already edits, and the suite
could not go green without it. It is not part of the landing page. Say so in the PR.

## The five open decisions

None of these are blockers for the code. All of them are somebody's call, not mine.

### 1. The commit is entangled, and that is why nothing is committed

The working tree this was built on carries a large, unrelated, uncommitted migration
from Apopka to Boston — roughly 44,000 deleted lines of processed data, plus in-flight
edits to `index.html`, `style.css`, `console.js`, `scene.js`, `day.json`, `build_day.py`
and six test files. The landing page edits sit **in the same three files** as some of
that work. There is no clean `git add -p` that separates them.

So a `feat/landing-page` commit made right now would drag somebody else's unfinished
migration in with it, under the wrong branch name and the wrong review.

Whoever picks this up: land the Boston migration through its own PR, then rebase this
on top, then commit the landing page alone. Do not commit both together to save a step.

### 2. Central Florida is now Boston

The spec's block 1 sentence says "one real day of Central Florida weather". The code no
longer does: `day.json` carries `Boston Logan International Airport gauge, Boston,
Massachusetts`, and the sources are NASA POWER for sun and NOAA ISD station 72509014739
for rain.

The page says **Greater Boston**, matching the data it actually plays. If the Apopka
data is coming back, this one sentence and the provenance strip change with it.

### 3. There is no figure, on purpose

The spec points every figure at
`planning/docs/research/flectofin-greenhouse-roof/why-water-placement-matters.md`, and
says only a figure rated STRONG may appear. **That file does not exist.** So block 2
ships with the story and the bridge and no number, which the spec calls an acceptable
outcome rather than a failure.

The placeholder markup is sitting in `index.html` as an HTML comment inside
`.motive-block`, with the three rules written next to it. When the research lands, drop
the text in there. Note the third rule especially: `test_the_page_fetches_nothing`
forbids any `http://` or `https://` in a served file, so **the source cannot be a link**.
Cite the organisation, document and year in words, and leave the URL in the research file.

### 4. The story has a gap, and it is Ameya's to fill

The spec is explicit that the family story is Ameya's to word and that nobody else edits
it. `planning/pitch/script.md` carries Ameya's approved wording with a marked gap:
"My grandmother farmed [where, and Ameya says what they grew]."

The page carries the sentence with the gap **left out**, not guessed at:

> My grandmother lost a hundred acres, because she could not get water to it.

Attributed on the page to "Ameya, who built this page". If Ameya wants the place and the
crop in, Ameya writes that clause. Nobody else, including you.

The bridge underneath it is the spec's exact wording and should be treated as fixed.

### 5. The spec's own "Done when" contradicts its block order

The spec asks for "the hero and the top of the roof are both in view" at 1440×900, and
separately for block order 1, 2, 3, then the console.

Those cannot both hold. Blocks 2 and 3 sit between the hero and the roof, so the roof
starts at y≈1227 on a 900 px viewport. The only way to get both is to reflow blocks 2
and 3 into side-by-side columns on desktop — and the spec also says this change "adds
three blocks above them and changes nothing else", so that reflow was not done.

What was implemented is the enforceable half: hero ≤ 60% of viewport, and the page
visibly invites the scroll. Somebody who owns the spec should decide which of the two
requirements wins. Do not quietly reorder the blocks to satisfy the other one.

## Traps in this repository, for anyone editing this page

Every one of these is a test that fails the build. Two of them were tripped during this
build and cost real time.

- **`"<header"` is forbidden as a raw substring** in `index.html`. Not the tag — the
  substring. A comment explaining why you avoided the tag will fail the test. It did.
- **`.why` was already taken.** `console.js` renders the inspector's reason card as
  `<div class="why">`, and `style.css` has six rules for it. The new section is
  `.motive` for that reason. Check any new class name against `console.js` before using
  it; that collision silently repainted block 2 with `--leaf-soft` for several minutes.
- **`roi` as a substring** fails `test_no_figure_for_cost_yield_energy_or_water_saved`,
  along with "water saved", "energy saved", "cost saving", "yield increase",
  "per cent more" and "payback". Class names count.
- **`first` as a whole word** fails `test_no_figure_claims_an_instrument`, with
  "maintenance free" and "weatherproof".
- **`measured`** may appear only inside the rain source line. See above.
- **No `http://` or `https://`** in any served file outside a `//`, `/*` or `*` line.
  This is why inline SVG in `index.html` carries no `xmlns` attribute. Do not add one.
- **Every hex colour lives in `:root`** and nowhere else, and no token may be declared
  and left unused. The new block adds no colour and no token.
- **Nothing below 18 px, no control below 48 px**, and at least five controls sharing
  the 48 px target.
- `id="overview"` must appear before `id="inspector"` in the document.

## Commands

```bash
.venv/bin/python -m pytest software/tests -q
```

```bash
for f in software/page/*.js; do node --check "$f"; done
```

```bash
.venv/bin/python -m http.server 8200 --directory software/page
```

The static server shows a 404 on `/api/health`. That is expected and by design: the
console falls back to its offline state and the demonstration still runs.

## What the PR has to say

Per `AGENTS.md`: record the checks that were run and the behaviour that was not tested.
Concretely — full suite 144 passed, `node --check` clean on six scripts, measurements at
1440×900 and 390×844 as listed above; three-second test not run, reduced motion checked
by reading the code and not by emulating the media query; and the gate F5 comment fix
was a pre-existing failure, not part of this work.

Do not mark the unrun checks as passing.
