# Submission text

The working copy, edited from `planning/pitch/submission.md` for what is actually built.
Square brackets are still open.
Owner: the team lead.

## Fields

**Project name:** flecto-stop

**Tagline:** A bus stop roof with no hinges that bends into shade when the sun hits it.

**Track:** Sustainability.
Sponsor challenges entered: [the ones the team adopts].

**Inspiration**

In the summer of 2023, researchers measured seventeen bus stops in Houston, and found the worst shelter was hotter than standing in the open.
Only about one in six stops in that city has a shelter at all.
A fixed roof is built for one angle of a sun that moves all day.
We wanted a roof that moves with it, and we found the mechanism in the bird of paradise flower, which bends open with no hinge.

**What it does**

A tabletop bus stop with a roof of three hingeless leaves.
A light sensor on the roof feels the sun, and one small motor bends a shared spine so all three leaves flip into shade together.
A second sensor on the bench measures the light that reaches the rider.
The laptop plays one real Houston summer day, 2013-06-03, as an LED sun, in about a minute, and shows the two readings pulling apart as the leaves bend.
Cover the roof sensor with a hand and the leaves relax: nothing scripts them.

**How we built it**

[Leaves: material, thickness, how they were made.]
[Rig: foam board, the LED sun, fixed or on a servo.]
An Arduino [board] runs a light threshold with hysteresis, steps the servo, and prints one line of eleven fields ten times a second, in a versioned serial format that every part of the system speaks.
A Python and FastAPI app reads that line over USB, derives the bench share and the leaf state, and streams it to a single static page over server sent events.
The same app plays the solar day to the board, records every line it receives unchanged so the run can be replayed exactly, and runs with no network and no build step.
The page is one HTML file: no framework, no CDN, no fonts fetched at run time.

**Challenges we ran into**

[Written at the event.]

**Accomplishments we are proud of**

[The measured numbers, X against Y, and the cycle count.]
A demo a judge operates with one button and one hand.
A screen that never shows a number without saying where it came from, and says "not fitted" instead of zero.

**What we learned**

[Written at the event.]

**What is next**

A full size leaf in a weatherproof material, a week of outdoor measurement with a real heat stress instrument, and one transit agency willing to try one stop for one summer.

**What we measured, and what we did not**

Measured: light at the bench as a share of light at the roof, leaves bent against leaves resting, [N] readings each, on a table under an LED sun.
Modelled: the sun itself, which is a public solar dataset driving an LED, and anything the shade simulation reports.
Not measured: temperature or heat stress, wind, rain, durability, cost, or rider demand.

**Built with**

Python 3.13, FastAPI, uvicorn, pyserial, pandas, pvlib, Arduino, C++, HTML, CSS, JavaScript, [CAD tool], [printer or cutter].

**Open source and data we used, cited as the rules require**

- FastAPI, uvicorn, Starlette, pydantic, pyserial, pandas, pvlib, pytest, httpx.
- PVGIS v5.2 typical meteorological year for 29.76 N, 95.37 W, (c) European Union, CC BY 4.0, downloaded 2026-09-19.
- Servo library for Arduino.
- The Flectofin bending principle, from research at the University of Stuttgart.
- Lanza, Ernst, Watkins and Chen, 2025, Transportation Research Part D, doi 10.1016/j.trd.2025.104653.
- City of Houston bus stop layer, 2022.
- AI coding tools: [named, if the form asks].

**Prior work statement**

Before the event we did research and planning only, in a public repository: https://github.com/andomo3/hack-mit.
It contains a labelled throwaway prototype of our serial format, none of which was copied.
All code and hardware in this submission were made during the hacking period, and the commit history shows it.

**Links**

- Repo: https://github.com/andomo3/flecto-stop
- Video: [YouTube URL]
- Planning repo: https://github.com/andomo3/hack-mit

**Team:** [three names]

## Checked at the freeze

- [ ] Every field has real sentences.
- [ ] Exactly one track.
- [ ] Every link opens in a private window.
- [ ] Every number matches the "Measured today" placard and the result card.
- [ ] Every library and dataset is cited.
- [ ] Submitted with thirty minutes to spare.
