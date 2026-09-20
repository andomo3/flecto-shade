# The landing page, Sunday 2026-09-20

Owner: Ameya builds it.
Written by the planner at 09:40 on abba's instruction, and it supersedes work package W1 in `devin-parallel-2026-09-20.md`, which described a plainer hero.
The story and the figures are the change.

## What this page has to do, in order

1. Tell a stranger in three seconds what this is and what to press.
2. Say why the team built it, with the one true story the project has.
3. Be honest about what it does not do, in the same breath, because the story is about a problem this project does not solve.
4. Hand the visitor to the roof.

Item 3 is not a caveat bolted on at the end.
It is the thing that makes item 2 usable at all, and the section below says why.

## The honesty rule that governs this whole page

Ameya's grandmother lost a hundred acres because she could not get water to it.

This project does not solve that.
A roof that decides bed by bed does not bring water to land that has none, and the pitch already says the irrigation system stays.
A page that tells that story and then shows this product, without a sentence between them, is claiming a relief it cannot give.
A judge, a grower or a journalist will close that gap themselves, and the project's whole case rests on being the team that says the limit first.

So the page makes one honest move, and it is the strongest thing on it:

> This roof would not have saved that land.
> Nothing here delivers water to a farm that has none.
> It decides where the water that does arrive should land, which is the part we could build and test.

That block is not optional and it is not moved below the fold.
It sits directly under the story, in the same visual block, at the same type size as the story.
It is not styled as fine print, a footnote, or a lighter grey.

Three more rules:

- **The family story is Ameya's.** Ameya writes the wording and nobody else edits it. Where the land was, what was grown and when are Ameya's to fill or to leave out. They are never guessed.
- **The statistics are about the wider pattern, never about that farm.** No figure is ever placed next to the hundred acres in a way that implies the figure describes it.
- **Every figure carries its source on the page**, visible, not in a tooltip. The project already labels every number gauge, modelled, simulated or assumed, and these are none of those: they are cited external figures, and the page says so.

## The figures

They are being researched now and land in `../docs/research/flectofin-greenhouse-roof/why-water-placement-matters.md`.
That file rates each figure STRONG, WEAK or UNUSABLE, and gives the quoted sentence, the organisation, the document and the URL.

**Only a figure rated STRONG goes on the page.**
Build the layout now with the placeholder markup below, and drop the text in when the file lands.
If no figure is rated STRONG, the section ships with the story and the bridge and no number at all, and that is an acceptable outcome, not a failure.

Placeholder, so the layout can be built and measured before the words exist:

```
[FIGURE]
[the quoted sentence from the source]
[Organisation, document, year]
```

## The page, block by block

The page keeps its current five console regions below. This adds three blocks above them and changes nothing else.

### Block 1, above the fold: what this is

Passes the three second test on its own, with the story out of the way.

| Element | Content | Notes |
|---|---|---|
| Mark | The existing `favicon.svg`, inline | No new asset |
| Eyebrow | "Simulated. Built at HackMIT 2026." | Sets the lens before any claim, which is the pitch's rule too |
| H1 | "One roof, a different answer for every bed" | The page's only `h1`. The stage title drops to `h2` and keeps `id="stage-title"` |
| One sentence | "A shade house roof of small hingeless fins that gives each bed its own light and rain, played over one real day of Central Florida weather." | |
| Primary action | One button, "See the roof decide", which scrolls and moves focus to the stage | The only primary button on the page |
| Quiet line | "Why we built this: [Ameya]'s grandmother lost a hundred acres when the water never came." as a link down to block 2 | One line only. The story is surfaced here and told below |
| Provenance strip | Three items: "Simulated", "Sun: NASA POWER, modelled", "Rain: NOAA gauge, 2023" | Each gets a word and a glyph, never colour alone |

The hero is at most 60 percent of the viewport height at 1440 by 900, so the top of the roof is visible and the page invites the scroll.

### Block 2: why we built this

The story, then the bridge, then the figure.
That order is deliberate: the bridge comes before the statistic, so nobody reads the statistic as the thing the product fixes.

1. The story, in Ameya's words, first person, attributed on the page to Ameya by name.
2. The honesty block quoted above, same type size, not greyed.
3. One STRONG figure about the wider pattern, with its source visible beneath it.

No image of a farm, no stock photograph, and no illustration of hardship.
The project has no photograph it owns, and a stock image of someone else's field under this story would be the one dishonest thing on the page.

### Block 3: what it actually does

Three short items, the rule of three, each one sentence, each true today:

- Each bed gets its own answer, from nine written rules, in the priority night, then rain, then light.
- The same storm gets different answers on different beds, because one bed's soil is dry and another's is already wet.
- No AI and no learned model is in the loop, and two runs of the same day produce identical output.

Then the visitor is in the console, which is unchanged.

## The checklist this must pass

From `.claude/skills/hackathon-ui-polish/references/ui-checklist.md`, read through this project's own rules, which outrank the checklist's Tailwind defaults.

- **Three colours at most.** Use the palette already in `style.css`. Add no new colour, and do not introduce the checklist's blue and violet.
- **One type family**, already loaded locally. No font from a network.
- **Two heading sizes and one body size.** Nothing below 18 px, which `test_console_type_never_drops_below_eighteen_pixels` enforces.
- **One primary action on the page.** Everything else is secondary or quiet.
- **Consistent spacing**, on the scale `style.css` already uses.
- **The three second test.** Cover everything below the fold, show it to someone for three seconds, and ask what this is and what they would press. If they cannot say both, block 1 is wrong.
- **Mobile first.** At 390 px wide: no sideways scroll, the primary button in view without scrolling, controls at 48 px, and the order is block 1, block 2, block 3, then the console.
- **Accessibility.** Heading levels in order with exactly one `h1`, the skip link still working, visible focus on every control, contrast of at least 4.5 to 1 for text, and every state carrying a word or a glyph as well as a colour.
- **Reduced motion.** With `prefers-reduced-motion` the scroll from the button is instant and nothing animates on load.

## The traps in this repository

These are tests that will fail the build if they are tripped, and they have caught this team before.

- `test_there_is_no_decorative_top_bar` forbids any `<header` tag. **The hero is a `<section>`.**
- `test_no_figure_for_cost_yield_energy_or_water_saved` searches the page and its scripts for substrings, one of which is `roi`. A word or a class name containing those three letters fails the suite. It also forbids "water saved", "yield increase", "cost saving" and "payback". This page talks about water and land, so read that test before writing the copy.
- `test_the_page_fetches_nothing` forbids any `http://` or `https://` outside a comment in a served file. **A source URL cannot be an anchor href in the page.** Cite the organisation, the document and the year in text, and put the URL in the research file instead.
- `test_the_screen_is_the_five_regions_the_console_needs` needs its five markers, with the overview before the inspector.
- `test_every_served_script_is_loaded_by_the_page` requires every served script to be loaded, and forbids the string "cdn".
- `test_touch_targets_stay_at_least_forty_eight_pixels` reads `style.css`.

Run `python -m pytest software/tests -q` in full, and `node --check` on every changed script, before opening the pull request.
The full suite, never a part of it.

## Done when

- At 1440 by 900: the hero and the top of the roof are both in view, and the three second test passes.
- At 390 px: no sideways scroll, the primary button in view, and the blocks in the order above.
- The story and the bridge are in the same block, at the same type size.
- Every figure on the page is rated STRONG in the research file, or there is no figure.
- Keyboard: tab order follows the blocks, the primary button reaches the stage, and focus is visible throughout.
- The full suite passes, and the pull request states which checks were run and what was not tested.

## Not part of this

The console below, the simulation, the rules, and any figure from the run.
No change to `software/h1/`, `software/api/`, `data/`, `rules.js` or `flectofin.js`.

## Branch and handoff

Branch `feat/landing-page` from `main`.
Small commits with `ui:` or `feat:`.
One pull request, reviewed before merge, and never a push to `main`.
Abba merges.
