# Shade house pitch

One sentence: A grower chooses soil areas; a simulated shade-house roof combines circular flap openings to water them and explains any shortfall.

Proposed booth roles, confirm before presenting: Abba speaks and drives the page; Ameya answers CAD and weather questions; Shannon answers roof-layout questions. The story is in [story.md](story.md); figures come from [results.md](results.md).

## 30 seconds

Imagine a grower in Central Florida who wants rain on two growing areas, while the neighbouring soil stays dry. Our shade-house simulation starts with that choice. Select two footprints, apply a rain event, and watch individual roof flaps open, water the selected soil, and close. The demo reaches every selected target and shows the water accounting. This is a software model using our team's CAD, with explicit aperture assumptions. Next, we want to test its predicted footprints against a physical roof.

## 60 seconds

Imagine a shade-house grower near Apopka, Florida. Rain is arriving, but only two growing areas need water. The question is: which roof openings can reach those areas without wetting their neighbours?

Our simulation lets the grower make that choice directly. I select two footprints, then press Simulate rain. Watch these individual flaps open. Each opening projects an assumed circular footprint onto the soil. Where footprints overlap, a cell receives rain once.

With the default ten-millimetre event, the chosen soil starts at twenty and targets twenty-five millimetres. All forty-two selected cells meet that target; the model reports zero delivery outside them. The openings then close while the remaining rain is excluded.

These are results at the small CAD prototype scale. We do not claim crop yield, water savings, or a functioning physical roof. The next experiment is to compare the idealized footprints with actual rain, including obstruction from the overlapping flap layers and base. We are looking for a grower to help shape that test.

## Three-minute booth run

Target 2:40 plus pauses. The live interaction lasts about 40 seconds. Do not rush to fill three minutes.

| Time | Say | Show |
|---|---|---|
| 0:00–0:25 | “Imagine a grower near Apopka. Rain is coming, but only two areas need water. Opening a roof is a decision about every piece of soil beneath that opening. How can the grower ask for water in just those areas?” | Deck 1–2. State that the grower is illustrative. |
| 0:25–0:40 | “We built a shade-house simulation that begins with that request. Choose the soil first; let the controller work out a permitted combination of openings.” | Open the page already loaded. |
| 0:40–1:20 | Use the [demo storyboard](demo.md). Say “Watch these two flaps” before clicking. Pause during animation. “The roof closes once the selected soil reaches its target. We can inspect both the result and the sequence that produced it.” | Preset → Simulate rain → results. This is the main reveal. |
| 1:20–1:50 | “Forty-two selected targets met, about twenty-one millilitres delivered, zero outside delivery in this example. Those volumes are small because we use the CAD prototype's real scale. If an opening would wet a protected neighbour, the controller can refuse it and explain why. That limit is part of the product.” | Results and opening sequence; deck 4 if needed. |
| 1:50–2:15 | “This is deterministic browser software with a WebGL view of the team's CAD. Overlapping open footprints never multiply the rain. We account separately for admitted, excluded, stored, outside, and overflow water. There is no learned controller or live sensor in this demonstration.” | Deck 3, keep architecture to one sentence. |
| 2:15–2:40 | “The CAD has twenty-two flaps in overlapping layers. We assume independent circular apertures; real obstruction and folding mechanics still need testing. Next: verify actual footprints, ask a grower where the selection workflow fails, then connect a small actuator and sensor experiment. Help us find the grower for that first comparison.” | Deck 5–6. Point to the repository link and stop. |

**Opening to memorize:** “Rain is coming, but only two growing areas need water.”

**Closing to memorize:** “Help us compare the grower's choice with what a real roof delivers.”

## Recovery lines

- App fails: “Here is the recorded run of the same selection and rain event.” Play the latest passing recording; do not claim it is live.
- Venue network fails: “This copy runs locally.” Use the already-running local page; if unavailable, use the downloaded deck and recording.
- Animation is slow: “The controller has already calculated the result. We can jump to it.” Click **Show result now**.
- Forgot a line: “The grower chooses the soil; the roof has to respect that choice.” Resume the next click.
- Unknown answer: “We have not measured that. We would test it by comparing the predicted and observed rain footprints.”

## Judge Q&A

1. **Who is it for?** Shade-house growers considering different rain decisions for areas under one roof. Apopka is our motivating setting, not a validated customer site.
2. **What is different?** Soil-area selection drives combinations of individual apertures. Existing environmental controls and moving roofs already exist; we make no uniqueness or patentability claim.
3. **Did growers validate it?** No grower interviews or adoption evidence are established here. That is our next validation step.
4. **Built versus mocked?** The interactive page, controller, geometry adapter, accounting, tests, and team CAD are implemented. Water transport and opening motion are simulations; no operating roof is claimed.
5. **A hundred users?** Calculations run independently in each browser. Static hosting serves files, but we have not load-tested hosting or low-end devices.
6. **Where is the AI?** AI tools assisted development. The runtime controller uses written deterministic rules and flap-ID tie breaking.
7. **API failure?** The primary flow needs no external API. Its local static assets must load; missing assets show an error. Keep the local server and backup recording ready.
8. **Where is data stored?** Selection and results stay in browser memory. The user can download JSON. There is no application account or backend persistence in this flow; hosting logs depend on the host.
9. **Why this stack?** Plain HTML/CSS/JavaScript and WebGL reuse the team geometry with no frontend build. Node runs controller checks and generates figures; Python serves files and supports the separate weather pipeline.
10. **What would you cut?** Keep the selection/rain/result loop. Move region shortcuts and weather replay out of the spoken demo.
11. **What comes next?** Measure occlusion and footprint geometry, interview a grower, then prototype control of a small physical section. Provisioning and physical experiments are separate from software iteration.
12. **First users?** Start with one grower willing to compare this interface with their actual decisions. No customer pipeline or conversion estimate is claimed.
13. **Who owned what?** Abba: integration and software direction; Ameya: weather/simulation and supplied CAD; Shannon: roof layout, per the project team record. Devin assisted code and validation. Confirm speaker assignments with the team.
14. **Hardest bug?** Integrating a resizable orbit camera with the soil/rain overlay initially clipped the scene; fitting the full scene bounds fixed it. Browser testing also caught a Reset button shadowing the native form reset method, fixed by renaming the control.
15. **Can I try it?** Yes, on the local laptop or this session's authenticated preview. The repository and PR are review entry points; no permanent public demo deployment is claimed.
