---
title: Which one sector a Flectofin sizing tool should serve, from five candidates checked against sources
type: research
status: done
owner: abba
updated: 2026-09-19
idea: flectofin-design-tool
---

# Which one sector a Flectofin sizing tool should serve, from five candidates checked against sources

## Answer

Thermal louvers for small satellites.
It is the one sector where the real part is the size of the fin on the table, the loads the model ignores do not exist, the buyer is a single role, and the numbers to design against are published.
The planner's first pick, car grille shutters, was made from memory and did not survive the sources: the documented pain there is ice, which a hingeless vane does not fix, and the governing load is air pressure at speed, which the model ignores.
The mechanism itself is not the team's and is not new in any sector, so the claim is the sizing tool and never the flap.

Facts below were found by a research agent that opened each source on 2026-09-19.
The planner opened two of them again, the NASA page and the patent, and they matched.
Anything marked unverified was seen only in a search snippet and is not to be said out loud.

## The test each sector was put to

1. Is the real part near tabletop size, so the display fin is the product and not a model of it?
2. Are the loads the beam model ignores, wind, weight, and air pressure, small there?
3. Is the buyer one clear role?
4. Is the hinge, the bearing, or the lubricant a documented pain, with money behind it?

## Prior art, said first

- The mechanism is patented by its inventors: EP2320015, "Hingeless, infinitely deformable folding mechanism", Universitaet Stuttgart and Albert Ludwigs Universitaet Freiburg, inventors Schleicher, Lienhard, Knippers, Poppinga, Masselter, and Speck, granted 2020-09-23.
- Its stated fields are "shading and privacy systems in architecture, ventilation flaps, opening or closing flaps, as well as adaptive folding mechanisms for aerospace engineering, engines and vehicle technology, medicine, process engineering, and interior decoration or furniture".
- Google Patents shows it as lapsed in most European countries for unpaid renewal fees.
  That is a database entry and not legal advice, and nobody on the team says anything about freedom to use it.
- So in every sector below the flap is prior art, and the team's contribution is a tool that sizes one.

## The five sectors

| Sector | Near tabletop size | Ignored loads small | One clear buyer | Hinge pain documented | Verdict |
|---|---|---|---|---|---|
| Small satellite thermal louvers | Yes, blades of roughly 100 to 200 mm | Yes: no wind, no air pressure, no weight in orbit | Yes, the spacecraft thermal engineer | In general for space mechanisms, not for louvers by name | Claim this |
| Hygienic and washdown equipment | Yes | No, washdown jets load the part | Partly, no named buyer of flaps was found | Yes, hinges and lubricant are named as contamination risks | A second line, as a hypothesis |
| Building facade shading | No, 20 to 100 times larger | No, wind governs | Yes, the facade engineer | Yes, "wear out" | The origin of the idea, never the market |
| Car grille shutters | Yes | No, air pressure at speed governs | Yes, a supplier's aero or thermal engineer | The documented pain is ice, not hinges | Do not claim |
| HVAC and data centre dampers | No, metre scale | No, pressure difference governs | Yes | Linkages work loose, with no rates given | Do not claim |

### 1. Small satellite thermal louvers

What they are: rows of blades over a radiator that open when the spacecraft runs hot and close when it runs cold, with no power and no electronics.

- Sierra Space sells Passive Thermal Louvers with "decades of NASA/JPL flight heritage", nearly 100 flight units, on Juno, New Horizons, Rosetta, Parker Solar Probe, and QuickBird.
- Its figures: pivoting aluminium blades, frames up to 20.95 by 15.63 by 2.48 inches, a 20 blade unit with 1,600 cm2 of radiating area and at most 1,290 g, rated for 20,000 cycles, a set point anywhere from -20 to +50 C, fully closed to fully open over about 20 C, and an effective emissivity of 0.14 closed and 0.74 open.
- NASA Goddard built a CubeSat version, "about four inches on a side", with aluminium flaps, a back plate in a white, highly emissive paint, and bimetallic springs a quarter of an inch across that "uncurl if one of the metals gets too hot, forcing the flaps to open".
  It ran "more than 12,900 cycles" on the bench between 91 and 131 F, and was planned to fly on Goddard's Dellingr 6U CubeSat.
- Why small satellites need it, in NASA's words: "Electronic thermal-control devices add weight and consume valuable space, making them less appropriate for small satellites."
- The hinge pain is documented for space mechanisms in general and not for louvers by name.
  A research firm under contract to ESA lists bearings among the contacts at risk of cold welding in vacuum, and attributes the 1991 failure of Galileo's high gain antenna to it.
  The step from that to "louver pivots are a risk" is the team's own inference, and it is said as one.
- No compliant, hingeless louver product was found, and the patent's scope already names aerospace.

### 2. Hygienic and washdown equipment

- The European hygienic design guide, EHEDG Document 8, never names hinges, and does say "dead areas, gaps and crevices... must be avoided", that lubricants must not touch product, and that polymers such as polypropylene and PEEK are acceptable.
- A conveyor maker's blog says closed hinge designs "trap product residue inside the hinge cavity where no sanitizer can reach", which is a vendor's claim and medium trust.
- No flap product, no named buyer of flaps, and no dimensions were found, and its cost figures were not traced to their origin, so none is quoted.

### 3. Building facade shading

- The One Ocean pavilion, Yeosu 2012: 108 kinetic lamellas in glass fibre reinforced polymer, between 3 and 13 m high, driven by servomotor screw spindles at the top and bottom of each, architect soma, facade engineering by Knippers Helbig, biomimetic research by ITKE Stuttgart.
- The later Flectofold paper says conventional hinges "wear out".
- It is 20 to 100 times the team's scale, wind governs, and professionals already did it with finite element models.

### 4. Car grille shutters

- A maker, confirmed from its own page: Roechling Automotive. Other names were seen only in a press release that could not be opened.
- The documented pain is ice: a General Motors service bulletin for the 2016 to 2017 Chevrolet Volt says snow or ice "could prevent the active aero shutters from opening or closing", and the fix is a software recalibration with a "break free routine", with the instruction "Do Not replace the active shutters for snow and/or ice build up".
  Ice bridges the vanes, so a hingeless vane ices up the same.
- A Subaru patent already puts a "flexible member" in the linkage.
- The money is real: US rule 40 CFR 86.1869-12 gives emissions credits for active aerodynamic improvements.
- Air pressure at speed governs the design, and the model ignores it.

### 5. HVAC and data centre dampers

- An industry article from a damper maker's product director describes the dampers and says supply dampers "must open in seconds" and generator exhaust can reach 260 C.
- A fire safety site names obstruction, linkages that "work loose over time or break", and failed actuators, with no rates.
- One dramatic closure statistic was seen in a snippet only and is not used.
- Pressure difference governs, blades are metre scale, and fire dampers are safety rated metal.

## Implications for the build

The tool becomes "size a hingeless louver blade for a small satellite radiator", and the sector hands it its parameters:

| Parameter | Where it comes from |
|---|---|
| Blade length, about 100 mm for a CubeSat face and up to about 200 mm | The Goddard and Sierra figures above |
| Set point temperature, and the span from closed to open, about 20 C | Sierra |
| Cycle life, 20,000 as the industry rating | Sierra, with Goddard's 12,900 as a second point |
| Heat rejected closed and open | The radiator law, area times emissivity times the Stefan-Boltzmann constant times temperature to the fourth, with 0.14 and 0.74 as the benchmark to match |
| Mass per radiating area, about 8 kg per m2 as the benchmark to beat | Sierra, 1,290 g over 1,600 cm2 |
| Material stiffness and strain limit, for aluminium, a spring steel, and a space rated polymer | To be sourced, row by row, never from memory |
| What drives it | A bimetallic element, which gives a turning force, where the fin needs a push along its axis |

The demo gains a second panel that a thermal engineer would recognise: the radiator's heat rejection closed and open, from the blade the tool chose.

What the team must say without being asked:

- The flap is ITKE's, patented, and the tool is ours.
- The display fin is PLA at room temperature, and PLA is not a flight material.
- Polymers outgas in vacuum, stiffness changes across -20 to +85 C, and nothing was tested in vacuum or cold.
- A bimetallic spring turns, and the fin needs a push, so the coupling between them is an open design problem and the tool does not solve it.
- The cold welding argument is about space mechanisms in general.

The honest line for the pitch: "A sizing tool for hingeless louver blades at CubeSat scale. The mechanism is published and patented by its inventors. Our model is exact for the rib, silent on the sheet, and untested in vacuum."

## Sources

- [NASA, thermal control technology for CubeSats](https://www.nasa.gov/missions/small-satellite-missions/nasa-repurposes-passive-thermal-control-technology-for-cubesats/), opened by the planner as well.
- [Sierra Space, Passive Thermal Louvers datasheet](https://www.sierraspace.com/wp-content/uploads/2024/01/THERMAL-CONTROL-SYSTEMS-Passive-Thermal-Louvers.pdf).
- [NASA Small Spacecraft State of the Art, thermal control](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/).
- [AAC, cold welding in space engineering](https://www.aac-research.at/cold-welding-an-underestimated-problem-in-space-engineering/).
- [EP2320015 on Google Patents](https://patents.google.com/patent/EP2320015A3/en), opened by the planner as well.
- [Lienhard et al. 2011, Flectofin](https://iopscience.iop.org/article/10.1088/1748-3182/6/4/045001), abstract.
- [Flectofold, Smart Materials and Structures](https://iopscience.iop.org/article/10.1088/1361-665X/aa9c2f), abstract.
- [One Ocean pavilion, e-architect](https://www.e-architect.com/korea/expo-yeosu-pavilion) and [designboom](https://www.designboom.com/architecture/soma-one-ocean-thematic-pavilion-for-yeosu-expo-2012-complete/).
- [GM service bulletin 16-NA-203, via NHTSA](https://static.nhtsa.gov/odi/tsbs/2018/MC-10137278-9999.pdf).
- [Subaru patent US20140290599A1](https://patents.google.com/patent/US20140290599A1/en).
- [40 CFR 86.1869-12](https://www.law.cornell.edu/cfr/text/40/86.1869-12).
- [Roechling Automotive, active grille shutter](https://www.roechling.com/us/automotive/products-solutions/aerodynamics/active-grille-shutter).
- [AMCA, dampers and louvers in data centres](https://www.amca.org/educate/articles-and-technical-papers/amca-inmotion-articles/maintaining-optimal-data-center-environments-with-dampers-and-louvers.html).
- [hvacfirelifesafety.org, failing dampers](https://hvacfirelifesafety.org/failing-dampers/).
- [EHEDG Document 8](https://www.goudsmitmagnetics.com/uploads/pdf/ehedg-doc-eng.pdf).
- [Dorner, harborage points](https://www.dornerconveyors.com/blog/identifying-and-eliminating-listeria-harborage-points-in-ready-to-eat-processing), a vendor blog.
