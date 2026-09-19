# Submission draft

The 2026 form is not open yet, so this follows the fields HackMIT and Devpost style forms have used, and it is checked against the real form as soon as it appears.
A title and a code link alone is rejected, so every field gets real sentences.
Square brackets are filled in at the event.
Owner: the team lead.

## Fields

**Project name:** [undecided]

**Track:** Sustainability, and only that one.
Sponsor challenges entered: [the ones the team adopts, each checked against its own requirements].

**Tagline, one line:** A bus stop roof with no hinges that bends into shade when the sun hits it.

**Inspiration**

In the summer of 2023, researchers measured seventeen bus stops in Houston, and found that the worst shelter was hotter than standing in the open.
Only about one in six stops in that city has a shelter at all.
A fixed roof is built for one angle of a sun that moves all day.
We wanted a roof that moves with it, and we found the mechanism in the bird of paradise flower, which bends open with no hinge.

**What it does**

A tabletop bus stop with a roof of three hingeless leaves.
A light sensor on the roof feels the sun, and one small motor bends a shared spine so all three leaves flip into shade together.
A second sensor on the bench measures the light that reaches the rider.
The laptop plays one real Houston summer day from public solar data as the sun, in about a minute, and shows the two readings pulling apart as the leaves bend.
Cover the roof sensor with a hand and the leaves relax: nothing scripts them.

**How we built it**

[Leaves: material, thickness, how they were made.]
[Rig: foam board, the LED sun, fixed or on a servo.]
An Arduino [UNO Q or Uno R3] runs a light threshold with hysteresis, steps the servo, and prints one line of readings ten times a second.
A Python and FastAPI app on the laptop reads that line over USB, streams it to a single static page, and plays the solar day to the LED.
It runs with no network.

**Challenges we ran into**

[Written at the event, from what actually happened. Likely candidates: getting three leaves to buckle alike from one motor, and a light threshold that holds in a bright hall.]

**Accomplishments we are proud of**

[The measured numbers, X against Y.]
[The number of cycles completed without a miss.]
A demo a judge operates with one button and one hand.

**What we learned**

[Written at the event.]

**What is next**

A full size leaf in a weatherproof material, a week of outdoor measurement with a real heat stress instrument, and one transit agency willing to try one stop for one summer.

**What we measured, and what we did not**

Measured: light at the bench as a share of light at the roof, leaves bent against leaves resting, [N] readings each.
Not measured: temperature or heat stress, wind, rain, durability, cost, or rider demand.

**Built with**

Arduino, C++, Python, FastAPI, pyserial, pandas, pvlib, HTML, CSS, JavaScript, [CAD tool], [printer or cutter].

**Open source and data we used, cited as the rules require**

- Servo library for Arduino, [and OneWire and DallasTemperature if the temperature sensors were used].
- FastAPI, uvicorn, pyserial, pandas, and pvlib (BSD 3 clause).
- PVGIS typical meteorological year data, (c) European Union, CC BY 4.0.
- The Flectofin bending principle, from research at the University of Stuttgart. [Confirm with the engineers.]
- Lanza, Ernst, Watkins and Chen, 2025, Transportation Research Part D, doi 10.1016/j.trd.2025.104653.
- City of Houston bus stop layer, 2022.
- [Any AI coding tools used, named, if the form asks.]

**Prior work statement**

Before the event we did research and planning only, in a public repository linked here: [planning repo URL].
It contains a labelled throwaway prototype of our serial format, none of which was copied.
All code and hardware in this submission were made during the hacking period.

**Links**

- Repo: [event repo URL]
- Video: [YouTube URL]
- Planning repo: [URL]

**Team:** [three names]

## Checked at the freeze, 01:00 Sunday, and again at 10:00

- [ ] Every field has real sentences.
- [ ] Exactly one track.
- [ ] Every link opens in a private window.
- [ ] Every number matches the "Measured today" placard.
- [ ] Every library and dataset is cited.
- [ ] Submitted with thirty minutes to spare, because the form will be slow at 10:55.
