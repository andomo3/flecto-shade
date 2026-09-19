---
title: Can we 3D print at HackMIT or must parts be printed before the event
type: research
status: done   # open | in-progress | done | dropped
owner: abba   # one word handle of the teammate doing the research
updated: 2026-09-15
---

# Can we 3D print at HackMIT or must parts be printed before the event

## Answer

Yes, HackMIT 2026 provides onsite 3D printing through a help desk next to hardware checkout, first come first served, with the queue closing Saturday night.
The printer question no longer triggers the pivot, but the queue means the flexure coupons and one spare leaf are still printed at home before the event, and every event print is submitted by Saturday afternoon.

## Findings

- The organisers' September email announces onsite 3D printing: submit a file through an online form, the 3D Printing Help Desk next to hardware checkout logs it and sends it to the queue, and the team is pinged when the print is ready for pickup, see [the logistics email](../sources/2026-09-15-hackmit-logistics-email.md).
- The queue is first come first served and prints are limited by time and filament.
- Failed prints are not reprinted, so the geometry has to be simple and the walls reasonable.
- Print submissions close Saturday night, so nothing can be printed on Sunday.
- The email does not say which filaments are stocked, so TPU for the flexures is not confirmed onsite.
- The email does not rule on parts fabricated before the event, so the question of pre-printed competition parts is still unanswered in writing.
- The [HackMIT 2026 hardware list](hackmit-hardware-availability.md) still lists no printer, filament, or TPU, so the email is the only source.

## Implications for the build

- The printer half of the pivot trigger is resolved: there is a printer at the event.
  The flexure coupon test due 2026-09-16 remains the trigger on its own.
- TPU flexure coupons and one complete spare leaf are printed at home before the event, because TPU stock onsite is unconfirmed and the queue is shared with every hardware team.
- Any part printed at the event is submitted to the queue on Saturday afternoon at the latest, and the build order in [the demo backwards plan](adaptive-bus-stop-canopy/demo-backwards-plan.md) needs the print submissions moved ahead of the Saturday evening closure.
- Keep event prints small and simple, since a failed print costs a queue slot and is not reprinted.
- Ask help@hackmit.org one narrower question: whether parts printed before the event may be used, and whether TPU is stocked at the help desk.

## Sources

- [HackMIT 2026 logistics email](../sources/2026-09-15-hackmit-logistics-email.md), September 2026, the 3D printing section and the schedule.
- [Load Paths artifact](../sources/2026-09-02-load-paths-artifact.md), constraint 01, print budget, and bring-your-own sections.
