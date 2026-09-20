# How to make the simulation stronger, and how the roof would be tested for real

Written by the planner on 2026-09-20, for the pitch's "how would you know it works" question and for the work after the event.
It was written from `software/h1/build.py` as it is on `main`, and from the FAWN research in `agricultural-data-voloridge.md`.
Nothing in it has been built unless it says so.

## 1. What the simulation is today, stated plainly

- It is a deterministic model that steps one hour at a time through 2023, one zone at a time.
- Its inputs are real: hourly rain from one NOAA gauge, and hourly sun and air temperature from NASA POWER, which is a modelled satellite product.
- Its roof logic is nine written rules in the priority night, then rain, then light.
- Its light model is the sun's energy times a fixed share that is usable by plants, times what the roof lets through.
- Its water model is one bucket of soil water a zone, 60 mm deep, filled by admitted rain and by irrigation, and emptied by the crop's use from the Makkink equation and a crop coefficient.
- Twelve of its constants are marked ASSUMED in the code, among them every size and threshold of the soil bucket.

What is good about it: the rules are readable, two runs give identical output, the weather is real, and every assumption is named.
That is already more than most hackathon simulations can say, and the pitch should say it.

## 2. The weaknesses that matter, in order

1. **A shut roof stops the crop drinking.**
   The crop's water use is multiplied by how far the roof is open, so under a shut roof it is zero.
   A shaded plant transpires less, and never nothing.
   The effect is that a shut zone's soil never dries, which flatters the "wet enough" rule and distorts every figure for the rain's share.
   The README already says the water model cannot support a claim about water.
   The fix is a floor: use under a shut roof is a share of the open figure, marked ASSUMED, with a source sought for shaded container crops.
   It changes every soil figure and every expected value in H1's tests, so it is the leading job after the event and not a job for the last morning.
2. **The assumed constants have never been varied.**
   Nobody knows whether the headline figures survive a soil bucket of 50 mm and not 60.
   Section 3 fixes this, and it is small enough to do now.
3. **One year, one place, one weather record.**
   The FAWN research found that swapping the modelled sky for the station on site changes what the roof does in 20 percent of daylight hours.
   That is a finding about our own fragility, and it should be reproduced in checked-in code.
   Section 4.
4. **The soil is a field bucket, and the crops are in pots.**
   Foliage near Apopka grows in containers of soilless media, which hold little water, drain freely, and are watered daily.
   A container model has a small store, a leaching fraction, and a salt balance, which is also where the project's interest in soil degradation would become something that can be computed.
5. **A zone's roof is one number.**
   The model treats a zone as one open fraction with a sharp edge.
   Real fins pass light at an angle that moves with the sun, light spills between zones, and rain drifts in wind.
6. **No failure is modelled.**
   A stuck actuator, a fin that fatigues, a sensor that drifts, and a storm with wind are all absent, and a grower will ask about every one.
7. **One crop figure is contested.**
   The fern's 8 mol target is from Purdue, and a 2022 HortScience paper recommends about 10 to 12 for the same genus.
   The demo already leans on the rain rule, which does not depend on it.

## 3. The right kind of simulation, and why it is Monte Carlo and not Simio

Simio, Arena, and AnyLogic's process library are discrete event tools.
They model things that queue for resources: patients, parts, trucks.
Our roof has no queue and no entity waiting for a server, so a discrete event tool would add cost and explain nothing.

What we have is a system that moves in fixed steps of time under rules, with uncertain constants and uncertain weather.
The standard method for that is a time stepped model wrapped in Monte Carlo sampling, with a sensitivity analysis on top.
It needs nothing beyond numpy, which the repo already pins.

Three layers, each answering a different question.

| Layer | What is varied | The question it answers | Cost |
|---|---|---|---|
| A. Parameter uncertainty | The twelve ASSUMED constants, drawn together | Do our results survive our own guesses? | 90 minutes, task T4 |
| B. Weather uncertainty | The year, and the weather record | Do our results survive a different year, or the station on site? | A day |
| C. Scenario stress | Failures: a stuck zone, a late sensor, a storm in wind | What happens when it breaks? | Days |

### Layer A, specified

- Draw each ASSUMED constant from a uniform range of 20 percent either side of its value.
  Uniform, because we have no evidence for a shape, and saying so is more honest than a bell curve we made up.
- Draw by Latin hypercube if time allows, because it covers twelve dimensions in far fewer runs than plain random draws, and it is about fifteen lines of numpy.
- Keep the physical ordering of the soil thresholds in every draw.
- 300 draws, one fixed seed, and the same seed gives the same bytes.
- Report, for each zone: the 5th, 50th, and 95th percentile of the rain's share of the zone's water and of the days the light target was met.
- Report the one figure the pitch rests on: the share of draws in which the three zones still give three different answers to the storm of 3 June 2023.
  If that is near 100 percent, the demo's claim does not depend on our guesses, and we can say so.
  If it is not, we have learned which guess the demo depends on, before a judge tells us.
- Report sensitivity as the rank correlation between each constant and each output.
  It is crude next to Sobol indices, it needs no new dependency, and it names the two or three constants worth sourcing properly.

What this is not: it is not a forecast, and it produces no figure for water, cost, or yield.
It is the spread of figures the page already shows.

### Layer B, specified

- NASA POWER and the NOAA gauge both reach back decades, so the same pipeline can build 2001 to 2023 with no new method.
  Twenty three real years are a better ensemble than any synthetic weather, because the wet and dry seasons, the afternoon storms, and the run of dry days are all really in them.
- Where more than the record is wanted, resample whole days within a month, in blocks of several days, so that a storm and the wet soil after it stay together.
- Run the rules over the FAWN station at Apopka, and report where the roof's decisions differ from those under the modelled sky.
  The research already found 20 percent of daylight hours, and that is a result worth showing: it says the roof needs a sensor on site and not a satellite.

## 4. How the code is kept honest: verification

Verification asks whether the code does what the rules say.
Most of it is cheap, and some is already there.

- **Already there.** Two runs give identical bytes, every state is one of the nine rules' names, no zone opens for rain in the dark, and no zone that opted out takes rain.
- **Add: the water balance closes.** For every zone and every hour, the soil at the end equals the soil at the start, plus rain in, plus irrigation, less the crop's use, to within rounding.
  A model that leaks water cannot say anything about water.
- **Add: bounds.** Soil stays between zero and its capacity, the open fraction between zero and one, and the daily light never falls within a day.
- **Add: properties, over random inputs.** More rain never leaves a zone drier, a lower light target never shuts a roof later, and a zone that opts out of rain stores none.
  These catch the errors that example based tests miss.
- **Add: the rules in two languages agree.** The page recomputes a zone in the browser from `rules.js` when a grower changes a target, and the year is computed in Python.
  `test_api.py` already checks the engine against H1's committed hours for the demo day, and the same check should cover the browser's rules over the whole year.

## 5. How the roof would be tested for real: validation

Validation asks whether the model describes the world.
We have done none, we say so, and this is the ladder we would climb.
Each rung is cheaper than the one above it, and each can end the project honestly if it fails.

### Rung 1. The inputs, against a sensor on site, with no hardware at all

- Compare the modelled sun against FAWN's pyranometer at the Apopka research centre, hour by hour, for a year.
- The research note has the early numbers, among them that half of the apparent error was a clock offset.
- **Pass:** the daily light integral's error is small next to the 4 mol gap between two crops' targets.
  The note found a day to day difference across 21 km of about 4 mol, which already argues for a sensor in each house.

### Rung 2. One fin on a bench

- **Light.** A quantum sensor under one fin, swept from shut to open, at several sun angles, against an open sky reference.
  This replaces two ASSUMED constants, what a shut fin passes and what the structure passes, with a curve.
- **Rain.** A rain simulator or a calibrated nozzle over a fin, with catch cups in a grid beneath, at several openings and with a fan for wind.
  The output is the share of rain admitted, and how evenly it lands, as Christiansen's uniformity coefficient, which irrigation engineers already use.
- **Life.** Cycle the fin open and shut on a motor until its force and deflection curve drifts.
  The roof would cycle a few times a day, so 10,000 cycles stands for many years, and ITKE's own publications give the figures to compare with.
- **Pass:** the admitted light and rain are repeatable to within a few percent, and the fin survives the cycle count without a change in stiffness.

### Rung 3. One bed, instrumented, under a small roof of fins

- Soil moisture probes at two depths, a quantum sensor at canopy height, a leaf wetness sensor, a tipping bucket above the roof and one below it, and a pour through test of the leachate's electrical conductivity each week.
- Run the rules live for a season, and log every decision beside every sensor.
- **What it tests:** whether the model's soil water and daily light track the sensors, hour by hour.
  The model is then calibrated on half of the season and scored on the other half, and never on the data it was tuned with.
- **Pass:** the modelled daily light is within a stated error of the sensor, and the modelled soil water calls for rain on the same days the probes do.

### Rung 4. A plot trial, which is the only rung that can speak about crops

- A randomised complete block design in one shade house: each block holds a bed under the zoned roof, a bed under fixed cloth of the usual grade, and a bed under a whole house movable screen.
- Four to six blocks, one crop to begin with, one season.
- **Outcomes, fixed before the trial starts:** how often the daily light target was met, the number and volume of irrigation events, leachate conductivity over time, hours of leaf wetness, disease incidence scored blind, and the grower's own grade of the crop at sale.
- **Analysis:** a mixed model with block as a random effect, and the comparison stated as an interval and never as a bare yes or no.
- The block count comes from a power calculation on the variance that rung 3 yields, and not from a guess.
- This is where "soil degradation" becomes testable: leachate conductivity and substrate tests over seasons, beside the roof's own log of what each bed was given.

### What would make us stop

- The fin fatigues early, or admits rain too unevenly to water a bed.
- The zoned roof's crops are no better than those under a whole house movable screen, which growers can already buy.
  This is the most likely way for the idea to fail, and it is the comparison an expert will ask for.
- Many small actuators cost more to keep running than the hinges they replace.

## 6. What to say in the pitch, in about twenty seconds

"We have not tested this on a plant, and we will not pretend we have.
What we have done is stress our own guesses: we ran the year hundreds of times with every assumed constant moved by a fifth, and the three zones still part ways in the storm.
The next step costs almost nothing: run the same rules on the university's own weather station at Apopka.
After that it is one fin on a bench, one instrumented bed, and then a blocked trial against the movable screens growers can already buy, because that is the comparison that could prove us wrong."

The second sentence is said only once task T4 has produced the figure, and with the figure it produced.
If the figure is poor, the sentence becomes what we learned from it.

## 7. Sources for the methods

- FAO Irrigation and Drainage Paper 56, for reference evapotranspiration, crop coefficients, and the soil water balance.
- McKay, Beckman, and Conover, 1979, Technometrics 21(2), for Latin hypercube sampling.
- Saltelli and colleagues, Global Sensitivity Analysis: The Primer, Wiley, 2008, for why one at a time sensitivity is weak, and what to do when there is time.
- Christiansen, 1942, Irrigation by Sprinkling, University of California Bulletin 670, for the uniformity coefficient.
- UF/IFAS EDIS EP529, for the leaching fraction, and SS117, for electrical conductivity in container media, both already in `../soil-telemetry-datasets/`.
- The citations above are from the planner's memory and were not opened tonight, so each is checked at its source before it is printed anywhere.
