---
title: Which applications a Flectofin design tool could optimise for, and whether Dimensional fits
type: research
status: open
owner: abba
updated: 2026-09-19
idea: adaptive-bus-stop-canopy
---

# Which applications a Flectofin design tool could optimise for, and whether Dimensional fits

## Answer

The tool is worth building only as the same simulation engine pointed at three applications, not many: the bus stop, the farmworker's rest shade, and a grower's crop shade.
All three are driven by light, which is the one thing the planned simulation computes properly, and Rosa stays the demo.
Applications driven by air flow or temperature need physics the team does not have, and they belong on a card, not in the tool.
Dimensional is a robotics framework, so it does not fit a design tool, and its one honest use here would be driving the real leaf, which needs checking before an hour is spent on it.
This is an idea under discussion on 2026-09-19, and the team has not decided it.

## The tool, stated so it can be checked

"For [application] at [place], the best [decision variables] are [values], because they score [objective] over a typical year, within our model."

The words "within our model" are part of the sentence.
The model is geometry and sunlight, so "optimal" means the best of the candidates we tried under that model, and never the best design in the world.

### What a Flectofin actually controls

A Flectofin is a flap with no hinge, and a flap changes two things: how much area blocks the sun, and how much area is open to the air.
So it acts on radiation and on air flow.
Temperature is a result of those two, and the leaf does not control it directly.
That matters for the inputs abba listed, heat, temperature, and air flow:

| Input | Can it trigger the leaf? | Can our model score it? |
|---|---|---|
| Sunlight | Yes, it is the current design, a light threshold | Yes, this is the ray cast and the solar data |
| Air temperature | Yes, as a second threshold, for example open the vents when outside is cooler than inside | Only as a trigger. We cannot compute what the leaf does to temperature |
| Air flow | Yes, as a trigger, for example feather edge on in high wind | Only crudely, as open area through a standard orifice formula. No real flow simulation is possible this weekend |
| Heat, meaning heat stress on a person | No sensor for it | No. It needs radiation, air temperature, humidity, and wind together, which is what the Houston study measured with instruments |

### The decision variables, the same for every application

1. Which way the array faces.
2. The spacing of the leaves, which sets how much sky is open at rest.
3. The light level at which the leaves bend, and the gap between bending and resting.
4. The leaf's length and the sheet's width.
5. How far the sheet turns at full flare.

Five variables at four or five values each is a few thousand candidates, and each is scored by running the year through the shade table.
That is a grid search, it is cheap, it is honest, and it is a small extension of package B6.

## The applications

Scored on whether the planned simulation can do them, whether "best" has a clear meaning, and whether they keep the pitch's lens of human life.

### Driven by light: the model can do these

| Application | The person | What "best" means | Data | Verdict |
|---|---|---|---|---|
| Bus stop or any outdoor wait | Rosa, the rider | Least direct sun on the bench in the harsh hours, while keeping a stated share of the cool months' sun | PVGIS, already downloaded | In. The demo, and the first sentence |
| Farmworker's rest shade | A picker on her break | The bench fully shaded for the most minutes above 80 F, the threshold in California's Title 8 section 3395 | SOLRAD Hanford and Hanford temperature, already downloaded | In. The law gives the objective its number |
| Crop shade, agrivoltaic style | A grower | Keep the crop's daily light inside a target band: shade above it, open below it | PVGIS, and a published daily light target for one named crop, still to be sourced | In, if one crop's target is found at a source. The cleanest meaning of "best" of all of them |
| Building facade | Someone behind a west window | Least solar gain while keeping daylight | PVGIS | Card only. It is what Flectofin was invented for, so it is the least original |
| Playground, schoolyard queue, market stall, car park | Children, vendors | The same as the bus stop | PVGIS | Card only. They are the bus stop again with another name |
| Livestock shade | A rancher | Shade in the hours above a heat stress index for cattle | PVGIS, and a published index, not sourced | Card only. It is further from the lens of human life |

### Driven by air or temperature: the model cannot do these

| Application | Why it tempts | Why it stays out |
|---|---|---|
| Night cooling vents on a building, open when outside is cooler than inside | Temperature is a clean trigger, and a hingeless damper has nothing to seize | The benefit is a room's temperature, which needs a thermal model of the room |
| The shelter that vents its own trapped heat | It answers the Houston study's real cause directly | Same: we can show the roof is open, and we cannot compute the cooling |
| Outdoor computer enclosure, the EdgeShade idea already in this repo | Shade and vent in one part | Needs internal temperature, which needs hardware |
| Server rack air flow, the RackLeaf idea already in this repo | A sponsor angle | Needs a fan and a flow model, and was rejected for that reason |
| Greenhouse vents, duct and car vents | Air flow is the whole job | No flow simulation is possible this weekend |
| Storm mode, leaves edge on in high wind | Already in the rain answer | It is a control rule, not something to optimise |

The honest place for these is one line on card 3: "The same leaf can vent as well as shade. We modelled only the light."

## Why three and not many

- The playbook's rule of three, and its scope creep brake: a new application is in only if it strengthens the core demo.
- Each application needs its own meaning of "best", its own data, and its own honest sentence, and those are the expensive parts, not the code.
- The pitch has one hero.
  Three applications fit the vision beat that is already written, the rider, the farmworker, and the grower.
  Ten would turn the pitch into a catalogue.
- A tool that claims to optimise for ten things with a geometry model invites the question "how do you know", ten times.

## Dimensional

What was found, by one web search on 2026-09-19 and nothing more: Dimensional, `dimos`, describes itself as "the agentic operating system for physical space", a Python framework for commanding robots, humanoids, quadrupeds, and drones, in natural language, with agents that subscribe to sensor streams and drive actuators.
Its documentation was not read, and whether it sponsors HackMIT or has a challenge is not known here.

- It does not fit a design tool.
  It is for controlling hardware, and the tool is an offline search over designs.
- Its one honest fit is the real leaf: the servo as an actuator and the photoresistor as a stream, with an agent that takes a goal in words, "shade the bench in harsh sun, keep the winter sun", and sets the threshold.
- That keeps a rule the team already made.
  The cut list in `../../../project-brief.md` rejects any language model in the control loop.
  An agent that chooses the settings, with the threshold still running the loop, stays inside that rule, and an agent that moves the leaf directly does not.
- Unknown and to be checked before any hour is spent: whether it has a prize and what its text asks for, whether it installs on Windows with Python 3.13, how heavy it is, and whether it can drive a plain serial device that is not a robot.

## Implications for the build

- Nothing already planned is wasted: the shade table, the year run, the data pipeline, and the gates all carry over, and the tool is B6 run many times with a score.
- It is a stretch, after the 23:00 checkpoint, and never before the demo plays end to end.
- If it is adopted it becomes three packages: the scoring functions for the three applications, the grid search with its result table, and one screen that shows the best candidate beside the default.
- The pitch gains one sentence and no more, and the honesty rule is "the best of the designs we tried, within a geometry model".
- A research package for the build agent, R2, thirty minutes, would settle the Dimensional unknowns.

## Open questions

- Is Dimensional a sponsor with a prize, and what does its challenge ask for?
- Which crop, and where is its daily light target published?
- Does the team want this at all, given nothing is built yet and seventeen hours remain?

## Sources

- [dimensionalOS/dimos on GitHub](https://github.com/dimensionalOS/dimos), found by search, README summary only.
- [California Code of Regulations, Title 8, section 3395](https://www.dir.ca.gov/title8/3395.html).
- [The project brief](../../../project-brief.md), the cut list.
- [Plan B](../../../plans/plan-b-simulated.md), packages B3 and B6.
