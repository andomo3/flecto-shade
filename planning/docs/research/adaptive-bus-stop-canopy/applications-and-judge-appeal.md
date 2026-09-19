---
title: Which other applications and sponsor angles make the canopy more appealing to judges without changing the build
type: research
status: done   # open | in-progress | done | dropped
owner: abba   # one word handle of the teammate doing the research
updated: 2026-09-11
idea: adaptive-bus-stop-canopy
---

# Which other applications and sponsor angles make the canopy more appealing to judges without changing the build

## Answer

Keep the bus stop as the thing on the table and the thing in the first sentence, and show breadth on one placard titled "Same leaf, other roofs" with three or four applications at one sentence each.
Judges in the recon corpus rewarded a named user and a concrete number, and the bus stop has both, a person on a bench and the Houston heat study, while every alternative trades that away for a sponsor logo.
Of the three sponsor variants the team wrote on 2026-09-07, EdgeShade is the one worth a sentence on the placard because ASUS is a listed sponsor and the mechanism is unchanged, QuietLeaf changes the physics to acoustics, and RackLeaf needs a fan that is not on the hardware list.
Sponsor fit stays framing until a 2026 challenge is published.

## Findings

### What the judges reward, applied to the applications question

- The expo format gives a few minutes per team, so the first sentence must name a person and a problem.
  "A person waiting for a bus in the sun" does that, "an outdoor edge computer" needs a second sentence.
- Winners in the corpus had one number and one moment.
  Adding a second application to the table adds a second moment and halves the rehearsal time for each.
- The Houston study gives the pitch a public health number a judge can repeat, and it belongs to the bus stop alone.
- Breadth still helps, but as an answer to "where else does this go", which comes after the demo, not before it.

### The applications, scored on whether they help the pitch

| Application | Same mechanism | Named user | Number available | Sponsor on the list | Verdict |
|---|---|---|---|---|---|
| Bus stop, the demo | yes | rider on a bench | Houston heat stress, transmitted light | none needed | The table and the first sentence |
| Schoolyard and playground shade | yes | children at recess | same light number, heat illness in children is well documented | none | Placard, one sentence |
| Outdoor seating at clinics and hospitals | yes | patients waiting outside | same light number | none | Placard, one sentence |
| Crop and greenhouse shade, agrivoltaic style | yes, larger | a grower | shade fraction against yield is in the literature | none | Placard, one sentence, strongest "why leaves not a roof" answer |
| EdgeShade, outdoor edge computer shell | yes, plus a vent state | a kiosk or box | peak internal temperature | ASUS, Arduino | Placard, one sentence, the only sponsor facing variant to name |
| QuietLeaf, voice kiosk baffle | no, acoustics | a kiosk user | word error rate | Deepgram, ElevenLabs | Not on the placard, a different project |
| RackLeaf, server rack airflow | partly, needs a fan | a data centre | peak temperature | ASUS, Modal | Not on the placard, fan not on the list |

The three placard applications share the bus stop's physics exactly, so a judge who asks "does this scale" gets a yes with no hand waving.
EdgeShade earns its sentence because it turns the same leaves toward a listed sponsor with one extra state, and the team already wrote it up.

### Sponsor angle, a little but not so much

- The 2026 sponsor challenges are not published, so nothing here is a qualified prize, see [the rescoring](../hackathon-recon-scoring.md).
- The controller is an Arduino or an ESP32 either way, so Arduino and Espressif cost nothing to name if a challenge appears.
- The leaves are a natural flat part, so a SendCutSend challenge would fit with about two hours of redrawing.
- ASUS is the one application sponsor that maps to the mechanism, through EdgeShade, and one sentence on the placard covers it.
- The model API sponsors, OpenAI, Modal, ElevenLabs, and Deepgram, do not fit the physics, and adding a model to a tracker loop would cost Buildable points for no gain, see [the score maximizing plan](score-maximizing-plan.md).
- Recheck the sponsor list at hour 0 and only then decide whether any two hour sponsor step is worth it.

### What makes the demo itself more appealing, ranked

1. The fixed roof next to the adaptive one, so the demo has two possible outcomes, plus three points under v2.
2. The judge moves the lamp, so the response is theirs to trigger.
3. A hinge the judge can see bending, so the Flectofin story is visible and the hobby prior art is not what they are looking at.
4. The heat probe, if the halogen test passes, so the number is about heat and matches the pitch.
5. The "Measured today" and "Not yet claimed" cards, so the Sustainability claim survives a sceptical judge.

## Implications for the build

- No hardware changes for any application, the placard is the only artefact.
- The EdgeShade, QuietLeaf, and RackLeaf idea files stay proposed and are not researched further unless a sponsor challenge names their domain.
- The pitch script gets one line after the number: "the same leaves work over a schoolyard, a clinic bench, a crop row, or an outdoor edge computer".

## Sources

- [EdgeShade](../../ideas/edgeshade-edge-enclosure.md), [QuietLeaf](../../ideas/quietleaf-voice-kiosk.md), [RackLeaf](../../ideas/rackleaf-ai-cooling.md), ameya, 2026-09-07.
- [Finalist rescoring and winner corpus](../hackathon-recon-scoring.md), the sponsor list and what winners share.
- [Score maximizing plan](score-maximizing-plan.md), team, 2026-09-07.
- [UTHealth Houston bus stop heat study, 2025](https://phys.org/news/2025-05-bus-relief-result-higher-temps.html).
- [Frontrunner tweaks](../frontrunner-tweaks.md), the SendCutSend flat part note.
