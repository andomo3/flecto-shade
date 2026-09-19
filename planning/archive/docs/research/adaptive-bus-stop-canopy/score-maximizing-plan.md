---
title: How the adaptive bus-stop canopy can maximize its HackMIT score
type: research
status: done
owner: team
updated: 2026-09-07
---

# How the adaptive bus-stop canopy can maximize its HackMIT score

## Answer

The canopy can be a strong Sustainability-track entry if it is presented as a measured, responsive shade prototype for transit riders—not as a miniature smart city or a finished bus shelter. Its highest-scoring version gives a judge three things in the first minute: a named user (a person waiting for transit in direct sun), a physical before-and-after (leaves open, then shade), and an honest number (the change in transmitted light under a fixed lamp).

The critical path is reliable motion and a controlled comparison. A polished dashboard, AI control, individually addressed leaves, or full-scale architectural claims do not improve the core score if they make the mechanism or measurements less dependable.

## Target score

The current v2 convention counts Demoable and Buildable twice, maps Freshness and Prior art toward their useful middle scores, and has a maximum of 45.
The plan as written targets **30/45**.
A fixed-canopy comparison across a lamp arc can raise Demoable to 5 and Number to 4 for **33/45**.
A controlled thermal comparison can then raise Track fit to 5 for a conditional **34/45**.
The printer and flexure test protect the build and its visual identity, but they do not erase existing prior art by themselves.

| Criterion | Raw | v2 points | What earns it |
| --- | ---: | ---: | --- |
| Demoable | 4 | 8 | A judge triggers the lamp response, sees the leaves move, and sees a repeatable reading change. |
| Number | 3 | 3 | Show raw readings and the transmitted-light ratio for unshaded, open, and shade conditions. |
| Track fit | 4 | 4 | Frame the measured light-control prototype as climate adaptation for people waiting at public transit. |
| Prize surface | 3 | 3 | Sustainability and Most Creative are plausible, while sponsor challenges are still unpublished. |
| Freshness | 3 | 3 | The transit and compliant-leaf combination is memorable, but light-responsive servo mechanisms and kinetic facades are familiar. |
| Buildable | 4 | 8 | Three leaves, one servo, two sensors, and a manual foam-board fallback keep the measured MVP bounded. |
| Prior art | 1 | 1 | A named Arduino, light-sensor, servo, and cardboard-canopy project already matches the functional MVP. |
| **Total** |  | **30/45** | |

## How to maximize each criterion

### Demoable, 4/5

Make the whole interaction legible from a few feet away. Put a small bus-stop sign and waiting figure beneath the canopy; label the two positions `OPEN` and `SHADE`; use large, high-contrast leaves; and give the judge one obvious trigger: turn on or aim the fixed lamp. The canopy should move in under five seconds, pause, and then be manually reversible with one button if the threshold input misbehaves.

Do not make a judge wait for calibration, connect to Wi-Fi, read a phone, or infer the difference from a subtle leaf angle. The physical state change is the demo, and the display only proves it.

The result is still expected, so Demoable does not reach 5 until a same-area fixed canopy and the adaptive canopy face the same moving lamp and either design could win across the tested arc.

### Number, 3/5

Measure what the model actually does. Fix the lamp, canopy, and sensor positions with tape marks. Take at least five sheltered-sensor readings for each of three conditions: `unshaded` (leaves removed or no canopy), `open`, and `shade`. Show the full readings and calculate:

`transmitted-light ratio = mean sheltered reading / mean unshaded reading`

Lead with the shade-state result in plain language: “Under this fixed lamp, the shade state transmitted X% of the unshaded reading.” Also show ten open-to-shade-to-open cycles and any failures. A narrow, auditable result is more persuasive than a temperature, energy, or health claim the setup cannot test.

This is a valid reading but an unsurprising comparison, so Number reaches 4 only when the same-area adaptive canopy is compared with a fixed canopy across several marked lamp angles.

### Track fit, 4/5

Use one sentence consistently: “We are exploring responsive shade for people waiting at transit stops during direct sun exposure.” It identifies the user, environmental pressure, intervention, and Sustainability-track connection without overstating impact.

The placard should distinguish **Measured today** (leaf motion, light readings, cycles) from **Next to validate** (thermal comfort, wind/rain safety, accessibility, durability, maintenance, and lifecycle impact). This makes the climate-adaptation direction credible rather than generic green branding.

Track fit reaches 5 only if a controlled heat test measures the thermal effect that the Sustainability pitch describes.

### Prize surface, 3/5

Submit to Sustainability. Design the electronics and enclosure cleanly enough for a hardware or fabrication challenge if one is announced, but do not let an unannounced sponsor challenge alter the MVP. The strongest optional extension is a compact, readable measurement display—not an AI feature added solely for a sponsor logo.

### Freshness, 3/5

The project should visibly borrow the idea of compliant, hingeless Flectofin motion while being explicit that it is a tabletop material-and-scale adaptation. The memorable combination is an adaptive, biomimetic roof applied to a familiar civic setting, plus an immediate measured effect.

Avoid saying the mechanism is unprecedented. Prior adaptive shading systems are real; the presentation is memorable when its physical response, public-transit use case, and light-control evidence arrive together.

### Buildable, 4/5

Protect the MVP with these gates:

1. Confirm printer access, rigid filament, TPU, and servo power before committing to the mechanism.
2. Test one leaf and flexure by hand before printing the roof.
3. Prove one servo can reach two safe states before connecting all leaves.
4. Add the second sensor only after manual motion works.
5. Collect measurements before decorative finish work.

Use three leaves, one actuator, and a pushrod/common actuation bar. Keep a foam-board or taped-flexure motion fallback, a spare printed leaf and flexure, and a manual override. Do not add machine learning, multiple independent actuators, weatherproofing, or a full shelter.

### Prior art, 1/5

Name the inspiration accurately: Flectofin-inspired adaptive shading.
The claim is not that compliant facade shading is new.
The functional MVP also has direct maker prior art in the Light-Based Canopy System, which uses an Arduino, light sensor, servo, and cardboard canopy that closes in bright light.
The contribution at the expo is the visible compliant mechanism, transit-focused experiment, and transparent measurement protocol rather than invention of responsive shading.

## Judge-facing setup

| Surface | Must show | Why it matters |
| --- | --- | --- |
| Physical model | Miniature waiting zone, labelled open/shade states, visible leaf movement | Delivers the before-and-after without explanation. |
| Measurement card | Raw readings, mean values, transmitted-light ratios, test geometry | Turns a visual effect into evidence. |
| Scope card | `Measured today` and `Not yet claimed` | Prevents overclaiming and makes the sustainability story trustworthy. |
| One-line pitch | “Responsive shade for transit riders, measured under a controlled light test.” | Gives every teammate the same precise opening. |

## 90-second pitch flow

1. **Problem (15 seconds):** “Waiting for transit can mean standing in direct sun with no control over shelter.”
2. **Response (20 seconds):** Turn on the lamp and show the canopy move to shade over the miniature waiting area.
3. **Evidence (25 seconds):** Point to the fixed test setup and the open/shade transmitted-light results, including raw readings.
4. **Design logic (15 seconds):** Show the modular leaf and explain that a damaged leaf is intended to be replaceable.
5. **Honesty and next step (15 seconds):** State that this measures tabletop light transmission; next validation covers thermal comfort, outdoor safety, and lifecycle performance.

## Score-killing mistakes

- A canopy that moves but has no fixed-lamp control or readings.
- A dashboard that becomes the focus while the roof motion is unreliable.
- Claims of cooler temperatures, heat-illness prevention, energy savings, or deployable infrastructure without supporting tests.
- Sensors, wires, or the servo casting a shadow into the measurement area.
- A complex multi-actuator design that reduces the chance of ten successful cycles.

## Sources

- [Feasible build and demonstration plan](feasible-build-plan.md).
- [Sustainability relevance and claim boundaries](sustainability-relevance.md).
- [HackMIT scoring convention and winner patterns](../hackathon-recon-scoring.md).
- [University of Stuttgart: Flectofin hingeless flapping mechanism](https://www.uni-stuttgart.de/en/university/news/all/First-Gips-Schuele-Research-Prize-for-bionic-facade-shading-systems/).
- [Light-Based Canopy System](https://github.com/Rainier-PS/Light-Based-Canopy-System), direct maker prior art for the functional MVP.
