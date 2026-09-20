# Demo storyboard — one request, one rain event

**Target: 40–50 seconds, below 90 seconds.** Use the primary page, not the weather replay. No account or typing is needed.

## Preflight

Serve `software/page` over HTTP. Load the page completely before judging. At desktop width, the CAD and event controls share the hero; the soil map and result are below. At phone width they stack. Click **Reset**, then **Select two footprints**. Defaults: rain 10 mm, starting soil 20 mm, target 25 mm, outside watering disabled.

Verify the motion preference before recording. Reduced motion intentionally completes the event immediately; use the prerecorded normal-motion run if animation is unavailable. Never present animation speed as physical actuator or storm timing.

| Time | Action | Say before clicking |
|---|---|---|
| 0–8 s | Point to selected cells; if needed click Select two footprints. | “The grower wants these two growing areas watered.” |
| 8–12 s | Point to event controls. | “A ten-millimetre event, with five millimetres needed by this soil.” |
| 12–22 s | Click Simulate rain; stay on CAD. | “Watch these two openings admit rain to their footprints, then close.” **Main reveal.** |
| 22–35 s | Scroll to results and selected map. | “All forty-two selected targets are met. The model reports no outside delivery.” |
| 35–45 s | Open Opening sequence; point to assumption banner. | “The result is accounted for and inspectable. Real cross-layer blockage is still an experiment we need to run.” |

Volume, if asked: about **21.1 mL**, at the small CAD scale. This is neither a farm yield nor a water-saving comparison. Refer to generated `results.md` for full accounting.

## Optional questions after the core demo

- Region buttons choose all projected footprints of a CAD region; they are selection shortcuts, not four independently simulated crops in this flow.
- Click one cell to show strict protection can block a flap. Turn on outside watering only when explaining the tradeoff.
- Select all to reveal gaps in the assumed circular coverage.
- Download JSON to inspect inputs, geometry assumptions, phase order, and all cell results.
- Open the separate Florida replay only if asked about earlier weather work; its outputs must not be mixed into the event-water claims.

## Recovery

Use **Show result now** to skip animation. **Reset** clears selected cells and restores inputs, cancelling an active event. Changing inputs also cancels a run. Each run starts from the input soil value; it does not continue the previous run's water storage.

Keep the latest passing recording and screenshots downloaded on the presentation laptop. If the page cannot load, play the recording, name it as recorded, then use `presentation.html` locally. The static deck is self-contained; no server is needed for it.
