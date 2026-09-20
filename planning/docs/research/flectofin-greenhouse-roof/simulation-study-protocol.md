# The protocol for the simulation study, written before the study is run

Written by the planner on 2026-09-20, from `software/h1/build.py` as it stands on `main` and from the "Assumptions" section of `data/README.md`.

This document extends section 3 of [`simulation-and-field-test-plan.md`](simulation-and-field-test-plan.md), which says which kind of simulation the project needs and why it is Monte Carlo sampling over a time stepped model rather than a discrete event tool.
That document settles the method.
This one settles the experiment: the questions it answers, the factors and the responses, the design, how many runs and why that many, how the output is read, and what result would change a decision.
It is written first, before any of it is built, so that the study cannot be bent afterwards to fit whatever it happens to find.

**This document holds no result.**
The study has not been run.
Every figure below is a setting, a range or a threshold that was chosen in advance, and none of it is an output.
Where a difference from section 3 appears, it is marked, because section 3 is the standing document and a difference is abba's to settle.

A note on what the simulation is, carried over so that nothing here is read as more than it is.
The rain is a gauge observation from the Orlando Executive Airport record for 2023.
The sun and the air temperature are modelled, from NASA POWER, which is a satellite and reanalysis product.
Everything the model writes is a simulated output, and every constant in the table below is an assumption.
Nothing in this study, at any sample size, can say anything about crop yield, soil restoration, water saved or how a real fin behaves.
That is what the validation ladder in section 5 of the simulation plan is for, and none of its rungs has been climbed.

## 1. The questions, in order

- **Q1. Does the demo's claim survive our own assumptions?**
  The claim the page and the pitch make is that on 3 June 2023 the three zones give three different answers to one storm.
  The question is whether that remains true when every assumed constant is moved.
- **Q2. Which assumed constants drive the outputs, and so deserve a real source first?**
  The project has twelve guesses and limited time, and the study should say which two or three to spend it on.
- **Q3. Do the results survive a different year, and the weather station on site?**
  This is layer B of section 3, and it is scoped here but not designed in detail.
- **Q4. What happens when a part fails?**
  A stuck actuator, a drifting sensor and a storm in wind are out of scope for the first study.
  They are named here so that nobody later thinks they were forgotten.

## 2. The factors, and the three kinds they fall into

Three kinds of factor are kept apart, because mixing them is the commonest error in a study of this shape.
A constant we guessed and a choice a grower makes are not the same thing, and neither is the weather.

| Kind | What it covers | How the study treats it |
|---|---|---|
| Uncertain constants | The twelve entries of `ASSUMED_CONSTANTS` in `software/h1/build.py` | Sampled, as section 3 specifies |
| Exogenous inputs | The hourly sun, rain and air temperature for the year | Layer A holds them fixed at 2023; layer B varies the year and the record |
| Decision variables | Each zone's crop profile, light rule, light target, and whether it may admit rain | Held at the page's three zones; a grower chooses these, so they are scenarios and never random draws |

The two entries of `RECALLED_CONSTANTS`, `MAKKINK_C` at 0.65 and `LATENT_HEAT_MJ_PER_KG` at 2.45, are not sampled.
Both were confirmed at source on 2026-09-19 and recorded in `data/README.md`, so they are published values rather than guesses.

## 3. The constants, their ranges, and what would replace the guess

Every row below is read from `ASSUMED_CONSTANTS` in `software/h1/build.py`, by name and by value.
The rule from section 3 is uniform sampling, 20 percent either side of the value, because there is no evidence for any other shape and inventing a bell curve would be less honest than saying so.
Where physics bounds a constant the range is bounded too, and where a constant is an integer it is drawn from integers.

| Constant | Value in the code | Range sampled | Why that range | What would replace the guess |
|---|---|---|---|---|
| `PAR_FRACTION` | `0.45` | 0.36 to 0.54 | The plain 20 percent rule. Note that the published range of global solar that is photosynthetic light is 0.44 to 0.55, so the lower half of this draw sits below the evidence. That is deliberate: a wider range is the harder test of the claim | A quantum sensor paired with a pyranometer on site, or the measured ratio for this climate from the source already cited in `data/README.md` |
| `T_STRUCT` | `0.90` | 0.72 to 1.00 | The 20 percent rule, clipped at 1 because a structure cannot pass more light than falls on it | The shade house maker's own transmittance figure, or rung 2 of the validation ladder: a quantum sensor under the structure against an open sky reference |
| `T_CLOSED` | `0.0` | 0.00 to 0.10 | 20 percent of zero is zero, so a percentage range would sample nothing. A shut fin that leaks a little light is the realistic alternative, and 0.10 is a generous ceiling | Rung 2: one fin on a bench, swept shut, measured against open sky at several sun angles |
| `SOIL_CAPACITY` | `60.0` | 48.0 to 72.0 mm | The 20 percent rule | A water release curve for the substrate actually used, and the open team decision on whether the bucket is a container or ground soil |
| `SOIL_DRY_BELOW` | `30.0` | 0.40 to 0.60 of the drawn capacity | Sampled as a share of capacity, not as an absolute, so that the ordering holds by construction. The code's value is 0.50 of capacity, and the 20 percent rule applies to that share | Soil moisture probes at two depths through a season, rung 3, against the crop's own wilting behaviour |
| `SOIL_FULL_AT` | `54.0` | 0.72 to 1.00 of the drawn capacity | The code's value is 0.90 of capacity, and 20 percent either side is 0.72 to 1.08, clipped at 1 because the latch cannot turn off above the bucket's size | The same probes, rung 3: where the substrate stops accepting water and starts draining |
| `SOIL_IRRIGATE_BELOW` | `18.0` | 0.24 to 0.36 of the drawn capacity | The code's value is 0.30 of capacity, with the 20 percent rule on that share | The grower's own irrigation trigger, which is a real number that a real nursery already uses |
| `SOIL_START` | `54.0` | 0.72 to 1.00 of the drawn capacity | The code's value is 0.90 of capacity, with the 20 percent rule on that share | Properly, nothing: the right fix is a spin-up period whose output is discarded, so that the first hour of the year stops mattering. Until then it is sampled |
| `HARD_RAIN_MM` | `25.0` | 20.0 to 30.0 mm in the hour | The 20 percent rule | A catch cup test under one fin with a fan for wind, rung 2, plus whatever rate a grower says is too much for a bed |
| `DRYING_HOURS` | `3` | The integers 2, 3 and 4 | The constant counts rows in an hourly table, so it cannot take a fractional value. Three integers straddle the code's value | A leaf wetness sensor through a season, rung 3, read against the fern guide's requirement that foliage dries during the day |
| `HEAT_SHADE_C` | `32.2` | 25.8 to 38.6 C | The plain 20 percent rule, applied to the Celsius figure. See the objection below the table | A measured canopy temperature response for the crop, rather than the fact sheet's 90 F air temperature trigger reused as a shading trigger |
| `HEAT_SHADE_OPEN` | `0.60` | 0.48 to 0.72 | The 20 percent rule. The clip at 1 is not binding here | Rung 2: a light sweep under one fin, turned into a curve of admitted light against opening, read against the 30 to 50 percent shade the fact sheet recommends |

Twelve constants, which is every entry of `ASSUMED_CONSTANTS`.

Three points about the table that the executor should not quietly decide alone.

- **The ordering holds without rejection.**
  The three soil thresholds are drawn as shares of the drawn capacity, and their share ranges do not overlap: 0.24 to 0.36, then 0.40 to 0.60, then 0.72 to 1.00.
  So `SOIL_IRRIGATE_BELOW < SOIL_DRY_BELOW < SOIL_FULL_AT <= SOIL_CAPACITY` holds in every draw by construction, and `SOIL_START <= SOIL_CAPACITY` with it.
  This matters more than it looks: rejecting draws that violate the ordering would quietly change the distribution the study promised to sample from, and the report would then describe a sampling scheme that was not used.
- **A percentage range on a Celsius temperature is arbitrary.**
  Celsius has an arbitrary zero, so 20 percent of 32.2 C is not 20 percent of anything physical, and the same constant in Fahrenheit or kelvin would give a different range.
  The table follows the blanket rule for now.
  A defensible alternative is a fixed window of about 5 C either side, and this is flagged for abba rather than changed here.
- **The thirteenth constant.**
  Step S0 in part 10 adds a floor to crop water use under a shut roof, marked ASSUMED.
  When it exists it joins this table and is sampled with the rest, and the study is not complete until it does.

## 4. The responses

| Response | Kind | Why it is measured |
|---|---|---|
| Three distinct answers to the storm of 3 June 2023 | Yes or no for each draw, reported as a share of draws with a Wilson interval | It is the claim the pitch makes, and it is the only response that can settle Q1 |
| Days in the year each zone met its light target | A count, for each zone | It is a figure the page already shows |
| The rain's share of each zone's water | A share, for each zone | It is on the page, and it is the figure that the known flaw in crop water use distorts most |
| Hours in which the roof's state differs from the base run | A count | It measures how far a guess moves the behaviour hour by hour, and not only the annual totals, which can agree while the roof does something different all year |

No response is a figure for yield, cost, energy or water saved.
The study reports the spread of figures the page already shows, and nothing the page does not already claim.

## 5. The design of the experiment

- Latin hypercube sampling over the twelve dimensions, so that each constant's range is covered evenly in far fewer runs than plain random draws would need.
- One fixed seed, `numpy.random.default_rng(20260920)`, so that the same seed gives the same bytes, and a test asserts it.
- The same weather in every draw of layer A.
  That is common random numbers, and it means a difference between two draws comes from the constants and not from the sky.
- The model is deterministic once the constants and the weather are fixed, so one run serves one design point.
  Replications would add nothing at all, and the protocol says so here because an examiner who is used to stochastic simulations will ask why there are none.
- Nothing beyond numpy is needed for any of this, and numpy is already pinned in the repo.

## 6. How many runs, and the rule for stopping

- Start with a pilot of 100 design points.
  Report from the pilot how long one run takes, before promising any number of runs.
- Then compute the half width of the 95 percent interval on each response, and decide from it.
- For the yes or no response, the required sample is at least z squared times p times (1 minus p), divided by h squared.
  At the worst case p of 0.5 and a half width h of 0.05, that is 385, so the plan is 400 points and this sentence is the reason.
- For the percentiles of the counted and shared responses, intervals come from a bootstrap over the draws, which needs no assumption about the shape of the output.
- If the pilot shows a run is slow enough that 400 points will not finish, the report says so and says what was run instead.
  It does not silently run fewer and present the result as planned.

**A difference from section 3, for abba.**
Section 3 of the simulation plan names 300 draws.
This protocol derives the count instead of naming it, and the derivation gives 400 at the worst case for the yes or no response.
The two are not in conflict about method, only about a number, and 300 is a reasonable floor if the clock demands one.
The protocol plans 400 and flags the difference rather than overriding section 3 quietly.

## 7. Analysis of the output

- For each response, report the 5th, 50th and 95th percentile across the draws, and say where the page's own value falls among them.
  A page value near the middle of its own spread is a different story from a page value at the edge of it, and the reader should be able to see which it is.
- **Sensitivity, first pass.**
  Partial rank correlation of each constant with each response.
  It costs nothing beyond the runs already made, and because it works on ranks it handles a response that rises with a constant without rising in a straight line.
- **Sensitivity, second pass, only if the first is unclear.**
  Morris screening to cut the twelve down, then Sobol indices by the Saltelli scheme over the few constants that survive.
  Sobol costs N times (k plus 2) runs, which is why it is not the first pass, and it may bring in a dependency, SALib, which needs abba's approval before it is added.
- **One plot a constant.**
  The response against the constant, as a scatter over the draws.
  A correlation hides a threshold, and a threshold is exactly the thing worth finding: a constant that does nothing until it crosses a value and then changes everything.

## 8. What result changes what decision

Written before the study runs, so that the decisions cannot be chosen after the numbers are seen.

| If the study finds | Then the team does |
|---|---|
| Three distinct answers in 95 percent of draws or more | The pitch may say the demo's claim does not depend on our assumed constants, quoting the share and its interval, and saying how it was obtained |
| Under 95 percent | Name the constant that breaks it, source that constant properly, and say so in the pitch before a judge finds it |
| One constant dominates a response | That constant is sourced first, before any other modelling work, whatever else was queued |
| The known flaw in crop water use dominates the rain's share | Fix the flaw first and run the study again, because a study run over a wrong model measures the wrong thing and its numbers would be worse than none |

## 9. Verification and validation

Verification asks whether the code does what the rules say, and validation asks whether the model describes the world.
Section 4 of the simulation plan lists the verification checks, among them that the water balance closes every hour, that soil and open fraction stay within their bounds, and that the rules in Python and the rules in the browser agree.
Section 5 lists the validation ladder, from the inputs against a sensor on site, through one fin on a bench and one instrumented bed, to a blocked plot trial, which is the only rung that can speak about crops.
This protocol adds nothing to either list and does not repeat them.

It adds three checks that belong to the study itself rather than to the model.

- **The base case reproduces what is committed.**
  A draw that sets every constant to its value in `software/h1/build.py` must reproduce the files in `data/processed/` byte for byte.
  If it does not, the sampling harness has changed the model, and every other number the study produces is about a different model than the one the page shows.
- **An extreme draw behaves as physics says it must.**
  At the top of its range a larger soil capacity must not make a zone irrigate more often, and a shut fin that passes more light must not reduce the days a light target was met.
  These are directional checks and they need no reference figure.
- **One draw is traced by hand for a single day.**
  One person reads one zone's twenty four rows for one day against the nine rules and confirms each one.
  It is slow, it is unglamorous, and it catches the class of error that no automated check was written to look for.

## 10. The order of work, and where the known flaw is fixed

| Step | What is done | What it depends on |
|---|---|---|
| S0 | Fix crop water use under a shut roof, with a floor marked ASSUMED, and rebuild H1's expected values | Nothing. It is the thirteenth constant, and it joins the study |
| S1 | `simulate` and `decide` take a mapping of constants, with the module's values as the defaults. Outputs unchanged byte for byte | S0 |
| S2 | The pilot: 100 points, the time a run takes, the half widths | S1 |
| S3 | Layer A in full, its outputs file, and its tests for the seed, the ordering and the base case | S2 |
| S4 | The sensitivity report, and the decisions of part 8 | S3 |
| S5 | Layer B: 2001 to 2023, then the same rules over the FAWN station at Apopka | S3 |
| S6 | Layer C: failures, as scenarios | After the event, and after S5 |

The known flaw is the one named first in section 2 of the simulation plan.
Crop water use is multiplied by the open fraction, so under a shut roof the crop drinks nothing, and a shaded plant transpires less but never nothing.
A zone that stays shut therefore never dries, which flatters the "wet enough" rule and distorts the rain's share, which is one of this study's four responses.

This order puts the fix before the sampling, and so it differs from task T4 in `../../../plans/devin-todo-2026-09-20.md`, which ran layer A first because the clock during the event demanded it.
After the event the fix comes first, for the reason in the last row of part 8.

**The open question this protocol does not settle, for abba.**
Whether S0 comes before layer A, as written here, or whether layer A runs first over the model as it stands.
Running layer A first gives a number sooner and measures a model we know to be wrong in a way that touches one of the four responses.
Running S0 first costs a rebuild of H1's expected values and delays every number, and it is what the protocol recommends.

## Sources for the methods

Each of these is a citation to be confirmed.
They are written from the planner's memory, none of them has been opened for this document, and nothing is quoted from any of them.
Each is checked at its source before it appears in anything printed, presented or submitted.

- Latin hypercube sampling: McKay, Beckman and Conover, 1979, Technometrics.
  To be confirmed.
- Global sensitivity analysis, including the Saltelli scheme for Sobol indices: Saltelli and others, 2008.
  To be confirmed.
- Screening designs for a model with many uncertain inputs: Morris, 1991.
  To be confirmed.
- Simulation output analysis, including sample size and interval estimation: Law, "Simulation Modeling and Analysis".
  To be confirmed.

Section 7 of the simulation plan carries the sources for the model itself, among them FAO-56 for the water balance, and the same rule applies to all of them.

## Twenty seconds, for the pitch

"We have not tested this on a plant, and we will not pretend we have.
What we can do is stress our own guesses.
There are twelve constants in this model that we chose rather than measured, and they are all named in the repository.
The study we have written up takes every one of them, moves it by a fifth in both directions, runs the whole year several hundred times, and asks whether the three zones still part ways in that storm.
It is written down before it runs, so we cannot go back and pick the question that flatters us.
After that it costs almost nothing to run the same rules against the university's weather station at Apopka, and then it is one fin on a bench, one instrumented bed, and a blocked trial against the movable screens growers can already buy, because that is the comparison that could prove us wrong."

The sentence that says how the study came out is added only once the study has been run, and it carries the figure the run produced.
Until then the pitch says what the study asks, and not what it found.
If the figure turns out poorly, the sentence becomes what we learned from it, which is a better thing to say to a judge than silence.
