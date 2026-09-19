# Run

The build status the README dashboard renders from.
Keep the lines below and the Features table in this exact shape, then run `/sync-state`.
Statuses are real, stubbed, fixture, planned, or cut, and a feature only ever moves down that ladder during the event.

Phase: pre-event, the engineers' build plan adopted as the MVP on 2026-09-18, software skeleton and dataset due before Saturday
Clock: hacking 11:00 Saturday 2026-09-19 to submission 11:00 Sunday 2026-09-20, venue closed 01:00 to 07:00, judging from 12:00
Freeze: 01:00 Sunday, the venue closure, nothing new after it
Demo path: one miniature foam board bus stop under an LED sun, on a servo mount if the build allows and fixed if not, the judge presses play and the app fast forwards one real Houston day from the dataset as LED brightness, the photoresistor sees it and three leaves on one backbone buckle open together from one servo with no hinge and relax at sunset, and the screen shows the light reaching the bench against the incident light
The number: light at the bench as a percent of the incident light, said as "X percent of the light reaches the bench with the leaves open, against Y percent closed", temperature secondary, backup "N of N light triggered cycles"

## Features

| Feature | Status | Owner | Note |
|---|---|---|---|
| Leaf variants, two or three backbone and lamina thicknesses from 2 mm and 0.5 mm, hand tested | planned | Mechanism | hours 0 to 2, prints queued first, best combination picked at hour 2 |
| One leaf on one servo through a pull wire or rigid link | planned | Mechanism | hours 2 to 4, repeatable across several cycles |
| Three leaves on one shared backbone, one servo | planned | Mechanism | hours 4 to 6, last point to drop to two leaves |
| Foam board rig: bus stop frame, LED sun mount, mount points | planned | Structure and rig | hours 6 to 8, in parallel, LED has line of sight to the photoresistor |
| Flex sensor on the backbone, logged against servo position | planned | Electronics | hours 8 to 9, an indicator and never a control input |
| Photoresistor and threshold firmware: bright light, leaves flare open | planned | Firmware | hours 9 to 12, hard checkpoint at hour 12 |
| Bench light sensor under the canopy | planned | Electronics | by hour 12, the primary number comes from here |
| Temperature sensors under the canopy and at an open control spot | planned | Electronics | hours 12 to 14, secondary, shown if it reads |
| Integration into the rig and debugging | planned | Team lead and integrator | hours 12 to 15, first full end to end test in the rig |
| Manual override or backup trigger | planned | Firmware | hours 16 to 16:30, for ambient light in the judging room |
| Ideal: LEDs on a servo mount so the sun moves | planned | Structure and rig | depends on time and parts at the venue, the pivot is the fixed LED mount |
| Backup: fixed roof with its own bench sensor | planned | Structure and rig | 1 h of foam board, only if time allows, makes the number adaptive against fixed |
| App: sets the LED brightness and the sun angle, shows light, flex, and temperature live, fixture replay | planned | Software and data | before Saturday, runs with no serial port and no network |
| Fast forward day: the sunniest Houston day from the PVGIS file drives the sun in about a minute | planned | Software and data | before Saturday, the data moves the sun and only the photoresistor moves the leaves |
| Pivot: replay mode, the app commands the leaves from the day's data | planned | Software and data | only if the threshold is unreliable at hour 12, said out loud in the pitch |

## Decisions

Logged during the event with the clock time, one line each, what was decided and why.

## Rules used

Which rule from the `hackathon-build` skill fired, and what it did.
