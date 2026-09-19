# Submission draft

This follows the fields HackMIT and Devpost style forms have used, and it is checked against the real 2026 form as soon as abba has it open.
A title and a code link alone is rejected, so every field gets real sentences.
Square brackets are filled in at the event.
Every simulation figure is provisional, from the planner's run in `../plans/packages/H1-zones-light-rain-soil.md`, and is replaced from `data/processed/headline.json` before the form is sent.
Owner: abba.

## Fields

**Project name:** [undecided]

**Track:** [The team confirms it.
Sustainability was the track chosen for the bus shelter plan, and no file written since the change of plan restates it.]
Sponsor challenges entered: [the ones the team adopts, each checked against its own text.
The meeting note of 2026-09-19 leaves this open.
The hardware challenge is out, because there is no hardware.
A public data challenge is in reach only if its text fits a year of NASA and NOAA weather.
Cognition's, if it has one, because Devin wrote the code.]

**Tagline, one line:** A simulated shade house roof of small hingeless fins that gives three crops three different answers to the same sky.

**Inspiration**

A grower with three crops under one shade house roof gives all three the same sky.
Today one motor moves up to 50,000 square feet of roof, so every plant under it gets one decision.
But a Boston fern is at its best from 8 mol of light a day, and a hydrangea from 12.
We asked what a roof would do if it could decide bed by bed.

**What it does**

Everything here is simulated, and nothing physical was built.
It simulates a roof of many small fins over three crop zones near Apopka, Florida, hour by hour through 2023.
Each zone's fins open and shut by nine written rules, in the priority night, then rain, then light.
Each zone gets its own light, and lets the rain through only when its soil is dry, only in daylight, and only if its crop has opted in.
One page plays one real day, 3 June 2023, in about forty seconds: the fern's zone shuts by eleven, the hydrangea's by noon, the blueberries stay open, and then an afternoon storm gets three different answers, each with its reason in words.
The day ends on a result card, and then the year by month.
Over the simulated year, the rain supplied about [54] percent of the hydrangea zone's water and about [17] percent of the blueberry zone's, and the fern was held to its light target on about [354] of 365 days.

**What is ours, and what is not**

Not ours: the fin, which is the Flectofin, by ITKE at the University of Stuttgart, patented as EP2320015.
Not ours: watering by the sun's energy and holding a daily light target, which greenhouse computers from Ridder, Hoogendoorn, Argus, and Priva already do.
Not ours: a moving roof over crops, which Cravo and Sun'Agri already sell.
Ours: the resolution, zone by zone, and the simulation over a real year of weather.
We found no prior proposal to put a Flectofin over crops, which is an absence in our searches and not proof.

**How we built it**

A Python simulation with pandas and numpy reads one year of hourly rain from a NOAA gauge and the sun for the same place and year from NASA POWER.
It turns the sun into a daily light sum per zone, keeps a soil water bucket per zone with the grower's own irrigation as the backstop, and applies the nine rules each hour.
Two runs give identical bytes, and no AI or learned model is in the roof's control loop.
The page is plain HTML, CSS, and JavaScript, with no framework and no build step, and it reads files the simulation wrote and adds no physics.
Every spoken and printed figure comes from one file the build writes, `headline.json`.
It builds and runs with no network.
The code was written by Devin, a build agent, from work packages whose expected values were computed from the real data before any code existed, and a gate runner checked every package.

**Challenges we ran into**

[Written at the event, from what actually happened.
One candidate: a typical solar year joined to a real year of rain made rainy hours brighter than dry ones, so the sun was taken again for the same place and year as the rain.
Another: the project changed direction four times on Saturday.]

**Accomplishments we are proud of**

[The simulated figures, from `headline.json`.]
A demo a judge runs with one button.
Saying what is not ours before anyone asks.

**What we learned**

[Written at the event.]

**What is next**

A conversation with a grower near Apopka about where the rules are wrong, a soil bucket sized for containers, and wind, which the simulation does not model.

**What is simulated, and what is not claimed**

Simulated: each zone's light, soil water, and fin state, every hour of 2023.
Real input: one rain gauge's hourly record.
Modelled input: the sun and the temperature, a satellite product.
Assumed: the soil bucket's sizes, two crop coefficients, the roof's transmission, and the rain rule's drying time and hard rain cap, each a named constant and a row in the README's table of assumptions.
Not claimed: yield, cost, water saved, safety from disease, wind, hail, or a built roof.
Shading blueberries is not Florida practice, and that figure is from Washington State.

**Built with**

Python 3.13, pandas, numpy, pytest, HTML, CSS, JavaScript, [the CAD tool, only if the roof layout used one].

**Open source, data, crop figure sources, and AI tools, cited as the rules require**

- pandas 2.2.3, numpy 2.2.3, and pytest 9.0.2.
  [Add each licence when the README is written.]
- NASA POWER: "The data was obtained from National Aeronautics and Space Administration (NASA) Langley Research Center's Prediction Of Worldwide Energy Resources (POWER) project funded through the NASA Earth Science Division."
- "The data was obtained from the POWER Project's Hourly 2.10.2 version on 2026/09/19."
  No licence text was found on NASA's referencing page, and the submission says so.
- NOAA NCEI Global Hourly, Integrated Surface Database, station 72205312841, Orlando Executive Airport, 2023.
  [Believed public domain, to be confirmed.]
- NOAA NCEI 1991 to 2020 normals, station USW00012841.
- Purdue Extension HO-238-W, Table 2, for the fern's and the hydrangea's daily light sums.
- Washington State University fact sheet on reducing heat damage in blueberries, for the shade share.
- University of Florida IFAS: the Mid-Florida Research and Education Center, the tropical foliage breeding program, and EDIS documents EP149, EP550, and HS742.
- FAO Irrigation and Drainage Paper 56, for the crop coefficients and the evaporation equations.
- Noriega Gardea et al. 2021, Atmosfera 34(3), for the light conversion.
- UMass fact sheets on retractable roof greenhouses and shadehouses, and on selecting a screen system.
- The Flectofin: patent EP2320015, Universitaet Stuttgart and Albert Ludwigs Universitaet Freiburg, inventors Schleicher, Lienhard, Knippers, Poppinga, Masselter, and Speck; and Lienhard et al. 2011, Flectofin, https://iopscience.iop.org/article/10.1088/1748-3182/6/4/045001.
- AI tools: Devin, from Cognition, wrote the code from the team's work packages.
  Claude, from Anthropic, was used for planning, research, and drafting the pitch documents.
  [Add any other tool a teammate used.]
- The addresses for every source are in the README.

**Prior work statement**

Before the event we did research and planning only, in a public repository linked here: https://github.com/andomo3/hack-mit.
That repository holds a labelled throwaway prototype for an earlier idea, none of which was copied.
The project changed direction during the event, four times on Saturday: a bus shelter roof, a simulated one, a leaf design tool, and at about 16:45 this one.
The planning record is copied into the event repo under `planning/`, Markdown only, and the commit history shows every change.
All code in this submission was written during the hacking period.

**Links**

- Repo: [event repo URL]
- Video: [YouTube URL]
- Planning repo: https://github.com/andomo3/hack-mit

**Team:** Abba, Ameya, and Shannon.
[Full names as the form asks.]

## Checked at the freeze, 01:00 Sunday, and again at 10:00

- [ ] Every field has real sentences.
- [ ] Exactly one track.
- [ ] The word "simulated" is in the tagline and in the opening sentence of "What it does", because the submission gate asks for it in the opening paragraph.
- [ ] Every link opens in a private window.
- [ ] Every figure matches `headline.json` and the "Simulated, not built" card.
- [ ] Every library, every dataset, every source for a crop figure, and every AI tool is cited.
- [ ] The prior work statement links the planning repo and says the project changed direction during the event.
- [ ] Read once against the list of words the team never says.
- [ ] Submitted with thirty minutes to spare, because the form will be slow at 10:55.

## Where each figure came from

| Figure | File |
|---|---|
| 50,000 square feet a motor, and the makers | `../docs/research/flectofin-greenhouse-roof/market-and-differentiation.md` |
| 8 and 12 mol, 54 and 17 percent, 354 days, eleven and noon, the citations | `../plans/packages/H1-zones-light-rain-soil.md`, the simulation figures provisional until `headline.json` exists |
| The NASA POWER citation lines | `../plans/packages/S1-solar-2023.md` |
| The patent, the universities, and the inventors | `../docs/research/flectofin-design-tool/sector-choice.md` |
| What the submission must contain | the submission gate in `../plans/gates.md` |
