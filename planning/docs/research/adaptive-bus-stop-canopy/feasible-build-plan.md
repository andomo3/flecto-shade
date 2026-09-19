---
title: How to build and demo a Flectofin-inspired adaptive bus-stop canopy
type: research
status: done
owner: shannon
updated: 2026-09-05
idea: adaptive-bus-stop-canopy
---

# How to build and demo a Flectofin-inspired adaptive bus-stop canopy

## Answer

The feasible HackMIT artifact is a tabletop, sensor-responsive canopy with three to five modular shading leaves, not a weatherproof bus shelter.
It should use a rigid printed frame and leaves, TPU only at deliberately compliant flexure zones, one servo-driven linkage, and two light sensors to measure transmitted light beneath the canopy against an unshaded control.

The project is feasible only if the team confirms usable 3D-printer access, TPU, a rigid filament such as PLA or PETG, and enough print time at hour 0.
If dual-material printing is not available, use separately printed TPU flexures mechanically captured by the rigid leaves rather than making the complete canopy from TPU.

## Scope and claim boundary

- The biological and mechanical inspiration is Flectofin: a hingeless, compliant shading mechanism inspired by the folding action of the bird-of-paradise flower.
- The original Flectofin mechanism uses glass-fibre-reinforced composite components; a TPU-and-PLA tabletop model is a material and scale adaptation, not a reproduction of the architectural system.
- The one credible result is: `under a fixed lamp and test geometry, the commanded leaf state changed the measured light transmitted into the model waiting area.`
- Do not claim lower bus-stop temperature, lower city energy use, weather resistance, structural safety, full-scale durability, or net lifecycle benefit.

## Minimum physical design

### Canopy assembly

- Print a rigid U-shaped frame with an approximately 180 to 250 mm wide roof opening and a clearly marked sensor location representing the waiting area.
- Use three leaves for the MVP. Make each leaf a thin, ribbed PLA or PETG plate with a captured TPU strip or a narrow TPU flexure at its root.
- Couple all leaves to one servo using a simple crank and pushrod or a common actuation bar. One consistent open-to-closed movement is more valuable than individually addressable leaves.
- Print one spare leaf and one spare flexure before decorative parts. TPU flexures are the expected fatigue item.
- Place the microcontroller, wiring, and servo outside the measurement aperture so their shadows do not affect the result.

### Material decision

| Part | Preferred material | Why | Fallback |
| --- | --- | --- | --- |
| Frame and leaf faces | PLA or PETG | Holds a stable roof geometry and blocks light | Foam-board frame only if printing fails |
| Flexure / hinge zone | TPU | Provides visible compliant bending without a conventional pin hinge | Thin taped flexure for a motion-only fallback |
| Linkage and servo mount | PLA or PETG | Keeps the actuator load path stiff | Foam-board bracket with zip ties |

- Do not print the entire roof in TPU. It will make leaf angle and shade measurements less repeatable because the leaves can sag or twist.
- Start with a conservative 0.8 to 1.2 mm TPU flexure strip and test a single leaf by hand before committing to the complete print. Thickness, width, infill, and printer settings require tuning on the actual filament.

## Electronics and control

- Mount one light sensor above or beside the lamp-facing side as the control input and one at the marked waiting-area location as the outcome measurement.
- Use an ESP32, Arduino, or equivalent listed microcontroller and an SG90-class servo with a verified external 5 V supply and common ground.
- The base controller is a threshold rule: above a calibrated incident-light threshold, move to `shade`; below it, move to `open`.
- Add a manual button or serial command to force each state. It is both a demo control and a fallback if the input sensor is noisy.
- Log timestamp, incident-light reading, sheltered-light reading, requested state, and servo command. A live dashboard is optional; a serial log or simple local chart is sufficient.

## Verification plan

1. Fix the lamp position, distance, angle, room lighting, sensor locations, and canopy orientation. Mark each location with tape.
2. Measure the sheltered sensor with no canopy or with all leaves removed for five readings. This is the `unshaded` control.
3. Measure five readings each in the commanded `open` and `shade` states after a fixed settling time.
4. Calculate `transmitted-light ratio = mean sheltered reading / mean unshaded reading` for each state and show every raw reading.
5. Run ten open-to-shade-to-open cycles. Record any missed position, flexure damage, servo stall, or sensor reset.

Success is a visible leaf motion, a consistent direction of change between the open and shade transmitted-light ratios, and ten completed cycles without a failed flexure or actuator stall.
The project does not need an AI controller to establish this result.

## Build schedule and gates

| Elapsed time | Work | Gate |
| --- | --- | --- |
| 0:00 to 0:30 | Confirm printer, TPU, rigid filament, nozzle compatibility, and queue time; print one flexure coupon | Pivot to a non-printed concept if no fabrication path is approved |
| 0:30 to 2:00 | CAD and print frame, one leaf, flexure, linkage, and spare flexure | One leaf bends by hand without permanent deformation or tearing |
| 2:00 to 3:30 | Install servo and prove manual open/close motion | Servo reaches two safe, visible states without stalling |
| 3:30 to 5:00 | Add remaining leaves and the two light sensors | All leaves move together without binding |
| 5:00 to 6:00 | Implement threshold control and manual override | Sensor input changes state reliably under the lamp |
| 6:00 to 7:00 | Collect controlled light measurements and ten-cycle reliability data | Data show an auditable open/shade comparison |
| After MVP | Improve visual finish or test several leaf angles | Do not add multi-leaf optimization before the base test passes |

## Likely failure modes

| Symptom | Likely cause | Response |
| --- | --- | --- |
| Leaf sags or twists | All-TPU leaf or insufficient rigid ribs | Use rigid leaf faces; shorten the cantilever |
| Flexure tears or stays bent | Flexure too thin, too narrow, or over-travelled | Use the spare; reduce servo travel; widen the flexure |
| Servo stalls | Linkage binds or leaf load is too high | Decouple leaves, reduce travel, and use fewer leaves |
| Light data are inconsistent | Lamp/sensor geometry changes or room light varies | Fix and mark the setup; take a new unshaded control |
| Sensor sees a wiring shadow | Electronics sit in the aperture | Re-route electronics outside the test area |

## Team fit

- One hardware/CAD teammate owns compliant-leaf geometry and print tuning.
- One hardware/CAD teammate owns frame, linkage, servo mounting, and the motion reliability gate.
- One hardware/CAD teammate owns sensors, power, and the controlled test rig.
- The software teammate owns control logic, logging, and the readable comparison display.

This allocation uses the documented team mix of three hardware/CAD engineers and one software engineer without making inverse kinematics or machine learning a critical path.

## Sources

- [University of Stuttgart: Flectofin hingeless flapping mechanism](https://www.uni-stuttgart.de/en/university/news/all/First-Gips-Schuele-Research-Prize-for-bionic-facade-shading-systems/).
- [University of Stuttgart: FlectoLine adaptive shading system](https://www.uni-stuttgart.de/en/university/news/all/FlectoLine-Facades-in-motion/).
- [HackMIT hardware availability](../hackmit-hardware-availability.md).
- [3D-printing access question](../3d-printing-access.md).
- [Team composition record](../../superpowers/specs/2026-09-01-team-repo-design.md).
