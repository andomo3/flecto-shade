---
title: Adaptive Bus-Stop Canopy — One-Pager Brief
type: research
status: done
owner: team
updated: 2026-09-06
---

# Adaptive Bus-Stop Canopy

## The idea

A tabletop model of a transit-stop canopy that senses intense light and physically changes from an open roof to a shaded roof. Inspired by the compliant motion of Flectofin, modular roof leaves bend or rotate together to reduce the light reaching a miniature waiting area.

## Why it matters

People waiting for public transit are often exposed to direct sun with little control over when shelter arrives. This project explores responsive shade as a climate-adaptation tool: the canopy provides more shade when the measured light condition calls for it, while retaining a more open configuration when shading is unnecessary.

This is a sustainability fit because it connects a visible environmental condition (direct light exposure) to a physical response at shared public infrastructure. The hackathon prototype will demonstrate light control, not claims about full-scale thermal comfort, energy savings, lifecycle emissions, or outdoor durability.

## Rough build plan

1. **Make the mechanism:** Build a 180–250 mm-wide rigid frame with three modular leaves. Use PLA or PETG for the frame and leaf faces, with small TPU flexure strips at the leaf roots. Print a spare leaf and flexure first.
2. **Add motion:** Link the leaves to one servo through a pushrod or common actuation bar, giving reliable `open` and `shade` positions. Keep the actuator and wires outside the area being measured.
3. **Sense and control:** Use one light sensor to detect incident light and a second below the canopy to measure transmitted light. A simple threshold moves the canopy to shade; a button or serial command provides manual override.
4. **Test honestly:** Keep lamp, canopy, and sensor positions fixed. Record at least five readings for unshaded, open, and shade conditions, then run ten open-to-shade-to-open cycles.

## Demo moment

A judge shines a fixed lamp at the model. The incident-light sensor crosses its threshold, the three canopy leaves close over a miniature waiting area, and a display/serial log shows the sheltered sensor reading fall. The team then opens the canopy again and shows the repeated measurements side by side.

**Evidence shown:** raw light readings, average transmitted-light ratio relative to the unshaded control, and the result of ten motion cycles. A removable leaf can be swapped to illustrate the repairable, modular design direction.

## Definition of success

The canopy visibly and repeatably changes state in response to light, and the shade state produces a lower under-canopy light reading than the fixed unshaded control under the same test setup. The key pitch is: *“We built a responsive shade model for transit waiting areas and measured its tabletop light-reduction effect.”*

## Scope guardrails

Do say the project **explores adaptive shade for transit stops**. Do not say it lowers bus-stop temperature, prevents heat illness, saves city energy, is weatherproof, or is a deployable public-infrastructure product; those require full-scale thermal, structural, accessibility, durability, and lifecycle validation.
