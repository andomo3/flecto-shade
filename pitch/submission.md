# Shade house — choose where the rain goes

## Inspiration

A shade-house grower may want different rain decisions for neighbouring growing areas. We wanted to make that spatial choice visible and testable with the team's roof CAD.

## What it does

The farmer selects cells below a roof, sets a rain event and target soil-water depth, then sees combinations of circular flaps open and close. The deterministic controller admits rain over the union of open footprints, replans when targets are reached, and explains uncovered cells, protection conflicts and insufficient rain. Results include selected/outside delivery, stored water, overflow and excluded rain, with a downloadable JSON record.

## How we built it

Static HTML/CSS/JavaScript, WebGL team-CAD rendering, a pure JavaScript controller, Node acceptance checks and reproducible pitch figures. Python supports the earlier Florida weather pipeline and local static serving. No Docker or runtime external API is required.

The team supplied a STEP assembly, compared against Ameya's H2 mesh. We map 22 flap instances to assumed 25 mm circular apertures at the small CAD scale. The earlier real-weather demonstration remains a separate page.

## What was validated

See [generated results](results.md), [the acceptance checklist](checklist.md) and [PR #5](https://github.com/andomo3/flecto-stop/pull/5). The two-footprint example reaches 42/42 selected targets at default inputs, with about 21.1 mL delivered and zero outside delivery in the model. This is a reproducible software result, not a measured irrigation or crop result.

## Limits and next steps

The independent-aperture model does not include cross-layer/base occlusion, wind, runoff redistribution, actuator dynamics or physical folding mechanics. The CAD establishes geometry, not hydraulic performance. Next: measure real footprints, interview a grower, then test a small actuated section.

## Credits and prior work

Abba: integration/software direction. Ameya: weather/simulation and CAD handoff. Shannon: roof layout, per the team record.
Devin (Cognition) assisted code, documentation and validation; Claude (Anthropic) assisted earlier planning/research. No learned model runs in the controller.

Mechanism inspiration: ITKE Flectofin, patent EP2320015; no rights to that mechanism or novelty claim are implied.
Earlier replay sources: NASA POWER and NOAA ISD, documented in `planning/docs/research/` and generated replay metadata. They do not supply the manually configured rain event in the primary flow.

The team's prior research/planning repository is https://github.com/andomo3/hack-mit. This submission's software and current simulation are in https://github.com/andomo3/flecto-stop.
