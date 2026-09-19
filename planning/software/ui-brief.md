# UI brief, derived from the story

The screen is the second storyteller at the table.
It shows Rosa's day and Rosa's bench, and it is never a dashboard.
This brief is derived from `../pitch/story.md` and `../pitch/storyboard.md`, and it replaces the earlier dashboard framing of the mockup.
It is a design brief, so it is planning and not code.

## The one idea

Two bars that pull apart.
The sun climbs, the bench follows it up, the leaves bend, and the bench drops away while the sun keeps climbing.
That widening gap is the product, and every design decision either sharpens that moment or gets out of its way.

## The screen follows the emotional arc

| Story beat | Screen state | What dominates | What is absent |
|---|---|---|---|
| Setup and tension, 0:00 to 0:25 | Opening | The one line headline, a night sky, a small seated figure on a bench, the Play button | Every number. A judge who sees zeroes reads "broken", and a judge who sees figures stops listening |
| The invitation, 0:25 | Opening | The Play button, the only interactive thing on the page | Sliders, settings, anything else to press |
| Sunrise, 0:30 | Day running | The sky strip warming, the sun marker, the real date and hour | The result |
| The wow moment, 0:40 | Day running | The two bars pulling apart, the leaf badge flipping, the figure falling into shadow | Any animation that competes with the physical leaves: the judge should look at the table first and the screen second |
| The proof, 0:50 | Day running | The sun bar collapsing under the judge's hand, live | Smoothing. The bar must react within a quarter second or the proof is lost |
| Sunset, 1:05 | Day running | The sky cooling | |
| The number, 1:15 | Result card | Two figures, bent against resting, and the words "measured today on this table" | The live bars, which have done their job |
| The close, 1:25 | Result card | Stillness | Anything new |

## Design consequences

- **A scene, not a grid of tiles.**
  The top two thirds is one picture: a sky that changes colour through the day, a sun on an arc or a strip, a simple front view of the stop with three leaves, and a seated figure on the bench who is lit or shaded.
  The front view is the view the judge has of the rig, and it is the view where the gaps between the leaves open and close.
  The leaves in the picture follow the `angle` field, so the screen mirrors the table.
- **Colour tells the time.**
  The palette is the day itself: deep blue before dawn, warm amber at noon, cooling at dusk.
  Three colours still: sky, sun, shade.
  Green, orange, and red stay reserved for status.
- **The figure is Rosa.**
  A plain seated silhouette, no face, no name on screen, because the speaker names her.
  Lit when the bench reading is high, shaded when it drops.
- **Numbers arrive late.**
  Live values sit small beside the bars while the day runs.
  The big figures appear only on the result card.
- **Honesty is part of the layout.**
  "Measured today on this table" sits under the result.
  The dataset line reads "Sun: PVGIS typical year, Houston, real date".
  Anything modelled says "modelled".
  Replay mode is a banner in words, never a subtle icon.
- **Controls are backstage.**
  Brightness, sun angle, source, and replay mode live in a drawer opened with a key, because the judge presses exactly one button.
  "Reset the day" is in the drawer and on a key, for the five seconds between judges.
- **Secondary things stay secondary.**
  Temperature is a small line under the scene that vanishes when the fields are empty.
  The fixed roof is a third bar that exists only when its field is present.
  The flex trace is a thin line under the leaf badge.
- **Not fitted is a state.**
  For the first twelve hours only the sun sensor exists, and the scene must still look deliberate: the bench bar reads "not fitted" in muted text and the figure stays neutral.
- **Read from a metre away.**
  The headline, the badge, and the result figures pass the 3 second test at a metre, and nothing on the page is under 18 px.

## States to design

1. Opening, before play.
2. Day running, morning, leaves resting, bars rising together.
3. Day running, midday, leaves bent, bars apart: the hero frame, and the screenshot for the README.
4. The hand over the sensor.
5. The result card.
6. Waiting for the first reading, skeletons.
7. Only the sun sensor fitted.
8. The board stopped sending: "The board stopped sending readings. Check the USB cable, or switch to this morning's recorded run."
9. Replay mode banner.
10. Optional pieces on: fixed roof bar, temperature line, sun on an arc.
11. The drawer open.
12. The city picker, if it ships: a quiet selector beside the date, Houston first.

## What to change in the mockup prompt

This section is done: the full prompt, with the scene, the roof drawing, and the scorecard, now lives in `mockup-prompt.md`, and that file is the one to paste from.
The lines below are kept as the record of what changed.

Replace the TASK section's numbered page contents with the scene above, and add these lines to the CONSTRAINTS.

```text
This is not a dashboard. It is one scene: a sky that changes colour through the day, a sun
moving across it, a simple front view of a bus stop with three leaves, and a seated figure on
the bench who is lit or falls into shade. Two bars, "Sun" and "Bench", sit beside the scene.
The design's hero moment is those two bars pulling apart when the leaves bend.

Before Play is pressed, show no numbers at all: a headline, the night scene, and one large
Play button. Numbers stay small while the day runs. The big figures appear only on the final
result card, above the words "Measured today on this table".

The judge presses exactly one button. Every other control lives in a hidden drawer.
The screen must never out-animate the physical model on the table: motion is slow, and the
only fast thing is the Sun bar reacting when a hand covers the sensor.

Design the twelve states listed below, and mark state 3 as the hero frame.
```

## Acceptance, from the playbook's UI checklist

The 3 second test at a metre, the main action visible at once, hierarchy on a 4 px grid, a skeleton loading state, a success state that is the result card, a human error state, and a screenshot ready hero frame with real figures.
The mobile layout item is dropped on purpose, because the page lives on one laptop.
