# Project Brief - Adaptive bus stop canopy

> **SUPERSEDED on 2026-09-19 at about 16:45. This file is the record of the bus stop canopy, and nothing is built from it.**
> The current plan is the simulated louvre roof over three crops.
> Read `AGENTS.md` and `CHECKLIST.md` at the repo root, then `planning/plans/plan-d-louvre-roof.md`.
> If you are a build agent and you arrived here, stop, and go back to those files.

**Event:** HackMIT 2026, Saturday 19 to Sunday 20 September, 24 hours of hacking, submissions expected to close around 11:15 on Sunday.
**Tracks:** Sustainability, plus the Most Creative team challenge.
**Team:** three people, two engineers build the hardware and abba builds the software.
Names against roles live in `AGENTS.md`.
**Scope source:** the engineers' build plan, adopted in [the 2026-09-18 meeting note](docs/meetings/2026-09-18.md), which overrides every earlier version of this brief.

## One sentence

A tabletop bus stop roof made of hingeless leaves that buckle open on their own when the sun comes out, so the bench underneath stays shaded.

## The 90 seconds

1. The judge sees one miniature foam board bus stop with three leaves on a shared backbone over the bench, an LED sun above it, on a servo mount if the build allows and in a fixed mount if not, and two light readings on the screen, the incident light and the light at the bench.
   The opening line: "Picture Rosa. It is three in the afternoon in July, in Houston, and her bus is twelve minutes away."
   The story, the scripts, and the storyboard are in `pitch/`, and the screen follows `software/ui-brief.md`.
2. The judge presses play, and the app fast forwards one real Houston summer day from the dataset in about a minute.
   The hourly irradiance sets the LED brightness, and the sun's position sets the angle of the servo mount when it exists.
3. As the sun climbs the photoresistor sees the light and the three leaves buckle into their flared, shading state together, from one servo, with no hinge anywhere, and they relax again at sunset.
   The data moves the sun and only the photoresistor moves the leaves, so a hand over the sensor proves it is not a script.
   This is the moment the project wins or loses.
4. "With the leaves flared the bench gets X percent of the light, against Y percent with them resting."

## Build list

Only what the 90 seconds requires, in the engineers' order.
The hours are venue hours from the 11:00 Saturday start.

| Feature | Why the demo needs it | Venue hours |
|---|---|---|
| Leaf variants: two or three backbone and lamina thickness combinations, starting at 2 mm and 0.5 mm, with a built in resting curve, hand tested | The clean buckle is the whole demo, and printing is the biggest passive time sink, so it starts first | 0 to 2 |
| One leaf on one servo through a pull wire or rigid link, travel and speed tuned | Servo actuation must reproduce the hand buckle without stalling | 2 to 4 |
| Three leaves on one shared backbone, one servo | The canopy the judge sees, with a drop to two leaves as the last simplification | 4 to 6 |
| Foam board rig: the bus stop frame, the LED sun mount, the mount points | The scene, built in parallel by whoever is free | 6 to 8 |
| Flex sensor on the backbone, logged against the commanded servo position | A rough indicator that the bend happened, never a control input | 8 to 9 |
| Photoresistor and threshold firmware: bright light, leaves flare open | The automatic response, with the hard checkpoint at hour 12 | 9 to 12 |
| Integration into the rig, the bench light sensor, the secondary temperature sensors, wiring secured | The number comes from the bench light sensor | 12 to 14 |
| Debugging the move from the bench to the rig | Mounting stress and sensor alignment always shift | 14 to 15 |
| Fine tuning: three to five back to back runs, servo pacing, the manual override, the rehearsal | It cannot fail at the table | 15 to 17 |
| Software, built by abba before and alongside: the one page app that sets the LED brightness and the sun angle and shows the light, flex, and temperature readings live, with fixture replay | The readings a judge can see from a metre away | before Saturday |

Seventeen venue hours against eighteen available.
If a mechanical step runs long, time comes out of the software layer first: a hand triggered canopy that buckles reliably beats an automated one that does not.

## Cut list

Everything considered and rejected.
Written down so it stays rejected at 3am.

- The five marked positions and a hand swung lamp.
- A two sensor tracker, the control law is a threshold.
- The flex sensor as a control input, it is an indicator only.
- Individually addressed leaves, one servo and one backbone move together.
- Any machine learning or language model in the control loop.
- A weatherproof or full scale shelter, wind, rain, and structure are not tested.
- Cloud dashboard, Wi-Fi, or a phone app, the display runs on the demo laptop from a serial cable.
- The EdgeShade, QuietLeaf, and RackLeaf variants, one sentence each on the placard, no hardware.
- Auth, settings, onboarding, responsive layout, tests: always cut.

Ideal, with a pivot: the LEDs on a servo mount so the sun moves, depending on build time and parts at the venue.
The pivot is an LED in a fixed mount, and everything else works unchanged.

Backup: a fixed roof beside the canopy with its own bench sensor, an hour of foam board, built only if time allows.
It turns the number into adaptive against fixed.

The fast forward day is built by abba before Saturday from the PVGIS hourly file, see [the dataset choice](docs/research/adaptive-bus-stop-canopy/dataset-choice.md), so it costs the engineers no venue hours.
Stretch: a second city or a chosen stop.

## Pivots

Every pivot has an hour at which it is decided, agreed before the event so nobody argues it at the venue.
A mechanical overrun takes its time from the software layer first, never the other way round.

| Failure | Decided at | Pivot |
|---|---|---|
| No leaf variant buckles cleanly | hour 2 | Adjust the thickness ratio and reprint the top one or two, and at hour 4 fall back to a foam board or flat cut lamina on the best backbone |
| The servo cannot reproduce the hand buckle | hour 4 | Change the pull wire or link geometry, and at hour 5 the leaf is hand actuated for the demo |
| Three leaves bind or fall out of sync | hour 6 | Two leaves, then one |
| The servo mounted sun has no parts or no time | hour 8 | The fixed LED mount, the app keeps the brightness control and hides the angle control |
| The flex sensor is noisy | hour 9 | Indicator only, or dropped, the contract field stays empty |
| The light threshold is unreliable in room light | hour 12 | A shroud on the photoresistor, then replay mode: the app commands the leaves from the day's data, and the pitch says so out loud |
| The bench light sensor shows no clear difference | hour 13 | Move or shroud the sensor, then the number becomes "N of N cycles" with the flex trace as proof |
| Temperature shows nothing | hour 14 | The tile is hidden, nothing else changes |
| The backup fixed roof | hour 12 | Built only if the core loop is green and someone is free, otherwise never |
| The servo browns out the board | hour 2, first servo test | The servo moves to its own 5 V supply with a common ground, the engineers believe this is already covered |
| The UNO Q does not run the sketch | hour 1 | The Uno R3, the Arduino challenge dropped |
| The serial link is dead at the table | any time | The app replays the recorded fixture and the hardware runs standalone |
| The rig breaks in transport | 07:00 Sunday | The backup video, recorded after the first clean run |

## The number

Primary: the light at the bench as a percent of the incident light, leaves flared against leaves resting, from a second light sensor on the bench.
Said as "X percent of the light reaches the bench with the leaves flared, against Y percent resting".
If the backup fixed roof is built, the same number is also said adaptive against fixed.
Secondary: the temperature under the canopy against the open control spot, shown if it reads, never relied on.
Backup number: "N of N light triggered cycles completed", with the flex sensor trace as the proof of each bend.

## What judging actually rewards

No 2026 rubric is published.
The 2025 day-of site listed creativity, technical difficulty, design, and usefulness, unweighted, judged expo style in a few minutes per team, so the watched moment decides.

| What's rewarded | Evidence | How this project scores on it |
|---|---|---|
| A visible live result | Expo format, past winners such as Griddy and EyeCraft | The sun comes up and three leaves buckle open together with no hinge |
| A number said out loud | Winner pattern in the recon corpus | X percent of the light at the bench against Y percent |
| A named user and an unglamorous problem | Get Away, lettuce, BeeMovr | A person on a bench in the sun, framed by the Houston study |
| Track fit | Sustainability track | Climate adaptation at public transit, claims kept to what was measured |

## Sponsor prizes in reach

| Prize | What it requires | Hours to qualify |
|---|---|---|
| Sustainability track | Submit to the track, keep claims to what was measured today | 0 |
| Most Creative | The hingeless buckling mechanism and the bus stop framing, nothing extra | 0 |
| SendCutSend or PCBWay, if posted | Flat cut leaves or a board, only if a 2026 challenge appears | 2 |
| Arduino or Espressif, if posted | The controller is already one of theirs | 0 |

## Submission requirements

To be copied verbatim once the 2026 form opens.
Verified again at freeze.

- [ ] Every field of the submission form filled in, a title and a code link alone is rejected.
- [ ] Submit to exactly one track, Sustainability.
- [ ] Repo link, demo video if the form asks for one, and the placards photographed.

## Assumptions

- A 2 mm backbone with a 0.5 mm lamina and a built in resting curve buckles cleanly in the intended direction, tested by hand in hours 0 to 2.
- One servo moves three leaves on a shared backbone without stalling or binding, tested by hour 6.
- The flared leaf is the shading state, so bright light means more shade, which is the team lead's reading of the plan and is confirmed with the engineers.
- A second light sensor sits on the bench and reads clearly different with the leaves flared against resting under the LED sun.
- The servo has its own 5 V supply or battery with a common ground, so it cannot reset the board, flagged so the team is aware.
- A servo and a mount for the LEDs are available at the venue, and if not the sun stays fixed.
- Temperature is secondary because an LED radiates little heat and the difference may be too small to show.
- The photoresistor threshold separates the LED sun from the judging room's ambient light, and the manual override covers it if not.
- The team can print or cut the leaf variants at the event.

## Stack

Arduino Uno or UNO Q with Arduino C firmware, one leaf servo and ideally a second for the sun, an incident photoresistor and a bench light sensor, one flex sensor, two DS18B20 temperature sensors or a thermal camera, dimmable LEDs, serial over USB.
Python with pyserial logging to CSV, and a local FastAPI page for the live display with replay from a saved fixture when the hardware is not connected.
Not reopened during the event.
