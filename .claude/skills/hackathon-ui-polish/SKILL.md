---
name: hackathon-ui-polish
description: Make a hackathon UI look finished in thirty minutes using the HackMIT playbook - the three colour, one font design system, the 8 item essential checklist, the five minute premium shortcuts, the ugly to premium pipeline, the 3 second test, the mobile first checklist, the accessibility quick wins, the five ready palettes, and the copy paste Tailwind component inventory. Use this whenever the user mentions UI, UX, styling, "make it look good", "looks like a hackathon project", a dashboard or landing page that needs polish, mobile layout, loading or empty or error states, colours, fonts, spacing, or a screenshot worthy screen, even when they are mid build and only ask for "a quick pass". Built from the UI/UX Fast Track and UI Checklist sections of the playbook.
---

# Hackathon UI polish

Good UI is not decoration, it is comprehension.
A judge gives a project about ten seconds, and the interface is what buys those seconds.
You do not need a designer, you need this checklist and consistency.

| Need | Read |
|---|---|
| The design system setup, the 8 item checklist with copy paste starters, the premium shortcuts, the component inventory, breakpoints, accessibility quick wins | `references/ui-checklist.md` |
| The fifteen Tailwind components in full, five palettes, the mobile first checklist, the 3 second rule, visual hierarchy, the ugly to premium pipeline step by step | `references/ui-fast-track.md` |

## Set the system before touching a screen, ten minutes

Most hackathon UIs look amateur because of inconsistency, not bad taste.
Decide these three things once and apply them everywhere:

- **Colours, three maximum.** One primary, one accent, one neutral scale.
  The playbook's default: primary blue-600, accent violet-600, gray-50 to gray-900, plus green, orange, and red reserved for success, warning, and error.
  Or pick one of the five palettes in the fast track reference.
- **Type, one family.** Inter or Geist.
  Two heading sizes and one body size, nothing smaller than 14px, line height 1.5 to 1.75.
- **Spacing, multiples of 4.** Page padding `px-4 sm:px-6 lg:px-8`, sections `space-y-8`, cards `p-6`, inputs `px-4 py-2`.
  If something looks off, it is almost always spacing.

## The 8 item checklist

Every item skipped makes the app look amateur.
Work down the list, and copy the starters from the checklist reference rather than writing components from scratch.

1. **Hero above the fold.** One headline of six to ten words that says what the app does, one subheadline, one large contrasting call to action, nothing else.
2. **Main action visible immediately.** The user knows what to do within three seconds, no hamburger menu hiding core features.
3. **Spacing and hierarchy.** The 4px grid, clear section separation, headings visibly distinct from body.
4. **Mobile layout, tested now.** Tap targets 44 by 44, single column, forms stack, no horizontal scroll. Judges pull demos up on their phones.
5. **Loading state.** Skeletons rather than spinners, shown within 200 ms, buttons disabled while loading, progress for anything over two seconds. A blank screen reads as broken.
6. **Success state.** A confirmation, a visual indicator, a next step. No raw JSON.
7. **Error state.** Human sentences with a suggested fix and a retry. "We couldn't save your changes. Check your connection and try again." Never "Error 500".
8. **Screenshot ready.** No lorem ipsum, no placeholder images, no console errors, a favicon, a descriptive title, an OG image.

## Premium shortcuts, five minutes each

The details that separate "hackathon project" from "real product":

- Subtle shadows instead of borders: `rounded-xl shadow-md`.
- One border radius everywhere: cards `rounded-xl` or `rounded-2xl`, buttons and inputs `rounded-lg`, avatars `rounded-full`. Sharp corners read as 2015.
- `transition duration-200` with a hover lift on everything interactive.
- One gradient, on the hero or a feature highlight only, never the whole page.
- One icon library, Lucide, Heroicons, or Phosphor, at 20, 24, and 32px.
- Generous whitespace: double the padding on cards and add margin between sections.

## The 3 second test

Open the app fresh, count to three, and ask whether a stranger can tell what it does.
If not: make the headline say what the app does rather than a slogan, make the primary button the most prominent element, remove anything that does not answer "what do I do first", and use whitespace to point at the main action.
If everything is big, nothing is big.

## The ugly to premium pipeline

When a screen is already built and looks wrong, run the pipeline in the fast track reference in order: reset the defaults, pick the palette, apply the spacing scale, fix the typography, add the shadows and radius, add the transitions, then run the 3 second test again.
Each step is two or three minutes and the order matters, because spacing fixes hide most of what looked like colour problems.

## Accessibility, ten minutes

Five things cover eighty percent: alt text on every image, a label on every input, contrast of at least 4.5 to 1, visible focus rings with working tab order, and a skip link.
The test: can you tab through the whole app with only the keyboard?

## What not to do

Do not build a design system from scratch, do not fight the CSS, do not use three fonts, do not add a chart unless it explains something, and do not polish a screen the demo never shows.
Function before form early in the build, form before function in the last stretch.
