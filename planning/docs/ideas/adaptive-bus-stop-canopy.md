---
title: Adaptive bus stop canopy
type: idea
status: shortlisted   # proposed | researching | shortlisted | rejected | chosen
owner: team   # team, or one word handle if a single person is driving it
updated: 2026-09-19
---

# Adaptive bus stop canopy

## Problem

People waiting for a bus in a hot city stand in direct sun, and a fixed roof shades the bench for only part of the day.
A Houston study of 17 stops measured heat stress high enough to be dangerous at unshaded stops, found tree shade cut it noticeably, and found some enclosed shelters trapped heat and made it worse.
The idea is a canopy of leaves that curl closed when the light is strong and open again when it is not, so the waiting spot stays shaded as the sun moves.
The mechanism is borrowed from Flectofin, the hingeless shading fin from the University of Stuttgart that bends the way a bird-of-paradise petal does.

## The demo moment

A tabletop canopy sits over a marked waiting spot with a light sensor in it and a second sensor out in the open.
A lamp switches on, or swings across like the sun.
Three to five printed leaves curl closed on one servo, with no pin hinges anywhere.
The transmitted light reading under the roof drops on screen next to the unshaded control reading.
The lamp dims and the leaves open again.

## Hardware needed

- PLA or PETG frame and leaf faces with TPU flexure strips at the leaf roots, all 3D printed, printer access unconfirmed.
- One SG90 class servo on a crank and pushrod, with an external 5 V supply.
- Two light sensors, one incident and one under the canopy, on an ESP32 or Arduino from the hardware list.
- Fallback if printing fails: a foam board frame with taped flexures, which shows the motion but not the compliant hinge.

## Software needed

- Firmware: a threshold controller, a manual override button, and serial logging of both sensors and the servo state.
- A simple local chart of the transmitted-light ratio per state.
- No AI is needed for the result.

## Sponsor and track fit

- The clearest event fit is the Sustainability track because the prototype explores responsive shade as climate-adaptation infrastructure.
- Arduino or Espressif hardware can perform the sensing and real-time servo control, but the controller is supporting hardware rather than the central innovation.
- SendCutSend or PCBWay could be relevant if the leaves and linkage are fabricated through a published sponsor challenge.
- The 2026 sponsor challenges are not published, so none of these sponsor opportunities should be counted as qualified prizes yet.

## Open questions

- Printer, TPU, and rigid filament access at hour 0, see [3D printing access](../research/3d-printing-access.md), which is load bearing for this idea.
- Which TPU flexure thickness survives ten open and close cycles without tearing, untested.
- Whether to add a fixed canopy control so the demo answers "why adaptive" instead of "does it close", see the [recon scoring](../research/hackathon-recon-scoring.md).

## Sources

- [Feasible build plan](../research/adaptive-bus-stop-canopy/feasible-build-plan.md), team research, 2026-09-05.
- [Sustainability track fit](../research/adaptive-bus-stop-canopy/sustainability-relevance.md), team research, 2026-09-05.
- [University of Stuttgart, Flectofin](https://www.uni-stuttgart.de/en/university/news/all/First-Gips-Schuele-Research-Prize-for-bionic-facade-shading-systems/) and [FlectoLine](https://www.uni-stuttgart.de/en/university/news/all/FlectoLine-Facades-in-motion/).
- [UTHealth Houston bus stop heat study, 2025](https://phys.org/news/2025-05-bus-relief-result-higher-temps.html), heat stress at 17 Houston stops.
