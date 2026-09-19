---
title: How the software demo works, sensor tracking with data replay, and how it hits both sponsor challenges
type: research
status: in-progress   # open | in-progress | done | dropped
owner: abba   # one word handle of the teammate doing the research
updated: 2026-09-15
idea: adaptive-bus-stop-canopy
---

# How the software demo works, sensor tracking with data replay, and how it hits both sponsor challenges

## Answer

The leaves react to the lamp through the light sensor, and public solar and weather data sets the scene: the five lamp positions, the time of day on the display, and the shade hours number.
One input seam feeds the servo target from either the incident sensor (track mode) or a real Houston day from the dataset (replay mode), and both modes log to the same serial format, the same display, and the same bench sensors.
That design keeps the judge-operable moment, the measured number, and both published sponsor challenges, Voloridge Signal in the Noise and Arduino Touch Grass, for about two extra hours of software.
The team decides on 2026-09-16 whether to adopt it.

## Findings

### The two challenges and what each rewards

- Voloridge, Signal in the Noise: build with one or more real public datasets from a curated set covering climate, earth observation, transportation, and more, and show thoughtful use of data, see [the sponsor challenges](../../sources/2026-09-15-sponsor-challenges.md).
  The curated datasets are provided at the event, so the pipeline is built this week against a stand-in public dataset with the same shape and swapped at hour zero if a curated one fits.
- Arduino, Touch Grass: use the Arduino UNO Q, pull raw data from the physical environment, and transform it rather than just visualise it.
  The UNO Q is on the [HackMIT hardware list](../hackmit-hardware-availability.md), so it replaces the "Uno or ESP32" line in the brief's stack.
- Neither challenge changes the mechanism, the frame, or the rig.
  Both are software and framing.

### Why the fin keeps reacting to light rather than only replaying data

- The photoresistor is the cheapest sensor in the build, one resistor on an analog pin, and the control law is a threshold or a difference between two readings.
  The complexity is in the arc rig and calibration, which a data-only demo needs anyway if the judge is to see the leaves move against a sun.
- A servo replaying a schedule reads as an animation, and the first judge question, "how does it know where the sun is", gets the answer "we told it", which undercuts the word adaptive.
- Touch Grass requires sensor data in the loop.
  Playback has none.
- The measured number, transmitted light at the bench for the fixed roof against the adaptive one, needs the two bench sensors regardless of what drives the servo.
  Without them the pitch has no evidence.

### Where the data fits

- Sun position is astronomy, not weather, so it is deterministic and offline.
  A solar position library gives the real azimuth and elevation for a real Houston stop at any hour, which sets the five lamp marks and the time labels on the display.
- Hourly irradiance and cloud cover add a second beat: on a cloudy hour the leaves relax flat because tracking buys nothing, and the display shows shade hours per day for the fixed roof against the adaptive one computed over a real week.
- A transit dataset picks a real stop, which gives the map and search beat the teammate suggested, running on the laptop with no network.
- A weather API on an ESP32 works but needs venue Wi-Fi during judging, an API key, and live requests, which the brief's cut list rejects.
  The downloaded dataset gives the same beat and is what Voloridge actually rewards.

### The two modes

| Mode | Servo target comes from | What the judge sees | When it runs |
|---|---|---|---|
| Track | The incident light sensor | Leaves follow the lamp as the judge swings it | The live demo |
| Replay | A real Houston day from the dataset, stepped by time | Leaves move through a day with real times on screen, no lamp needed | Stage insurance if the rig or the incident sensor fails, and the software fixture before hardware exists |

- Both modes write the same serial log line, feed the same two bars, and measure with the same bench sensors.
- Replay mode is the same code path as the fixture replay the software needs anyway, so it costs one switch and one dataset loader.
- The fan on a servo the teammate suggested stays a stretch item, a second physical input after the light loop works.

### What this changes in the brief, for the meeting note

- Stack: Arduino UNO Q instead of "Uno or ESP32".
- Build list: one row added, the dataset pipeline that sets lamp positions and computes shade hours, estimated two hours, owned by the software and data role.
- Sponsor prizes in reach: Voloridge and Arduino Touch Grass replace the "if posted" rows.
- Cut list: the Wi-Fi line stays, with the note that all data is downloaded before the event.
- Event: 18 hours in the room, not 24, because the venue closes 1 AM to 7 AM Sunday, see [the logistics email](../../sources/2026-09-15-hackmit-logistics-email.md).
  Submission is 11 AM Sunday and judging starts at 12 PM.

## Implications for the build

- Firmware gains a mode switch and a replay input, and the serial format gains a mode field and a simulated time field.
- Software gains the dataset pipeline: download, compute solar position and irradiance for the chosen stop, write a small processed CSV, and feed the replay mode and the display.
- The display shows time of day and the shade hours number next to the two live bars.
- The five lamp marks on the arc rig are placed from the computed sun elevations, so the structure role needs those numbers from the software role before taping the marks.
- Liability waiver and media release are due Thursday 2026-09-17 for all four teammates, or nobody hacks.

## Sources

- [Sponsor challenges](../../sources/2026-09-15-sponsor-challenges.md), Voloridge and Arduino, transcribed 2026-09-15.
- [HackMIT 2026 logistics email](../../sources/2026-09-15-hackmit-logistics-email.md), the schedule, venue hours, and printing.
- [Demo backwards plan](demo-backwards-plan.md), abba, 2026-09-11, the workstreams and the control law fallback ladder.
- [Project brief](../../../project-brief.md), the demo path, build list, and cut list this research proposes to amend.
- [Build phase repo design](../../superpowers/specs/2026-09-15-build-phase-repo-design.md), the six roles the meeting votes on.
