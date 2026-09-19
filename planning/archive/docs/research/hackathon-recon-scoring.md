---
title: How the three finalists rank under the HackMIT recon criteria
type: research
status: done   # open | in-progress | done | dropped
owner: abba   # one word handle of the teammate doing the research
updated: 2026-09-07
---

# How the three finalists rank under the HackMIT recon criteria

## Answer

Under the team's v2 weighting, the evidence-normalized order is impact liner lab at 39/45, termite-inspired passive heat-rejection testbed at 35/45, and adaptive bus-stop canopy at 30/45.
The impact liner lab wins the scoring check because it combines the clearest live action, the strongest comparison number, and an inventory-compatible fallback without relying on a printer.
The mound remains the strongest Sustainability entry, but it loses four points to the insert because its thermal signal and heater implementation are untested and its result cannot visibly develop during a 90-second pitch.
The canopy loses because the current experiment measures an expected light-blocking result rather than heat or adaptation against a fixed-canopy control, and because its sensor-servo MVP has exact prior art.
This ranking supersedes the old 40/36/30 comparison as the current scoring check, but it does not record a team choice.
The team still chooses in a meeting.

## Evidence-normalized finalist scores, 2026-09-07

Raw scores are 1 to 5, with a higher Prior art score meaning less similar work exists.
The v2 total is `2 x Demoable + Number + Track fit + Prize surface + mapped Freshness + 2 x Buildable + mapped Prior art`.
The [criteria readme](readme.md) defines the point maps and explains why raw Freshness 4 and raw Prior art 3 are the scoring peaks.

### Raw scores

| Criterion | Impact liner lab | Termite testbed | Bus-stop canopy |
|---|---:|---:|---:|
| Demoable | 5 | 4 | 4 |
| Number | 5 | 5 | 3 |
| Track fit | 3 | 5 | 4 |
| Prize surface | 3 | 3 | 3 |
| Freshness | 4 | 4 | 3 |
| Buildable | 4 | 3 | 4 |
| Prior art | 3 | 2 | 1 |

### Points under v2

| Criterion | Impact liner lab | Termite testbed | Bus-stop canopy |
|---|---:|---:|---:|
| Demoable, x2 | 10 | 8 | 8 |
| Number | 5 | 5 | 3 |
| Track fit | 3 | 5 | 4 |
| Prize surface | 3 | 3 | 3 |
| Freshness, mapped | 5 | 5 | 3 |
| Buildable, x2 | 8 | 6 | 8 |
| Prior art, mapped | 5 | 3 | 1 |
| **Total, of 45** | **39** | **35** | **30** |

### Why each raw score is not one point higher

#### Impact liner lab

- Demoable is already 5 because a drop and two traces form an immediate physical comparison with more than one possible result.
- Number is already 5 because repeated paired trials produce a percent difference against a matched control.
- Track fit is 3, not 4, because the current plan explicitly does not validate a helmet, protection, injury risk, or any clinical outcome, so Healthcare depends on the future application story.
- Prize surface is 3, not 4, because Healthcare and Most Technically Impressive are plausible but no published sponsor challenge fits yet.
- Freshness is 4, not 5, because hackathon helmet sensors and commercial impact sensing are familiar even though the controlled liner-geometry comparison is unusual.
- Buildable is 4, not 5, because the chosen IMU's usable rate and range and the hand release's repeatability remain untested on the actual parts.
- Prior art is 3, not 4, because auxetic helmet liners have academic prior art and hackathon helmet sensors exist, although no exact measured folded-cell comparison was found.

#### Termite-inspired passive heat-rejection testbed

- Demoable is 4, not 5, because the cutaway, live readings, and prediction check are legible, but the rigs must be pre-warmed and the thermal result will not visibly emerge during the pitch.
- Number is already 5 because repeated matched-power runs can state how many degrees cooler one tested geometry was than ordinary ventilation.
- Track fit is already 5 because passive heat rejection for building design is directly legible as Sustainability.
- Prize surface is 3, not 4, because Sustainability and a team challenge are plausible but no applicable sponsor challenge is published.
- Freshness is 4, not 5, because termite-inspired cooling has appeared at maker events, while the matched-power comparative design lab remains uncommon.
- Buildable is 3, not 4, because the exact resistor stock, safe heater assembly, thermal signal size, cooldown time, and repeatability are still unproven.
- Prior art is 2, not 3, because TermiCool Pro and Bamboo House are direct hackathon or maker precedents for termite-inspired cooling.

#### Adaptive bus-stop canopy

- Demoable is 4, not 5, because the motion is immediate and repeatable but the current open-to-shade result has one obvious outcome.
- Number is 3, not 4, because the current control is unshaded space rather than a fixed canopy across a sun arc and the sensor measures light rather than the heat claim.
- Track fit is 4, not 5, because responsive shade is a clear Sustainability story but the prototype does not measure heat or thermal comfort.
- Prize surface is 3, not 4, because Sustainability and Most Creative are plausible but no applicable sponsor challenge is published.
- Freshness is 3, not 4, because light sensors driving servos and responsive facade models are common even if the transit framing is memorable.
- Buildable is 4, not 5, because the foam-board fallback protects the measured MVP but printer access, TPU, and the visible compliant flexure remain unresolved.
- Prior art is 1, not 2, because an Arduino, light sensor, servo, and cardboard canopy that closes in bright light already exists as a named project, alongside extensive adaptive-facade work.

## Changes from the 2026-09-05 comparison

- Impact moves from 40 to 39 because its audited inventory-only artifact is a benchtop geometry experiment rather than a validated protective or healthcare device, so Track fit moves from raw 4 to 3.
- The mound moves from the original 36 to 35 because direct maker prior art and unverified sponsor fit cost three points, while the audited physical cutaway and honest prediction-versus-measurement demo earn two Demoable points.
- The canopy remains 30 after correcting its former 32/40 score-maximizing note to the current v2 definitions of Number, Track fit, and Prior art.
- The official 2026 site still publishes no weighted judging rubric or sponsor-challenge list, so the v2 weighting remains in force.
- The old full-field table below remains for decision history and should not be used as the current finalist ranking.

## Event facts, HackMIT 2026

- Saturday 19 and Sunday 20 September 2026, 24 hours of hacking, Johnson Athletic Center, over 1000 hackers.
- Four tracks: Entertainment, Education, Sustainability, Healthcare.
  A project submits to at most one track, and submitting to a track is optional.
- Prizes: three general prizes, one beginner prize, four track prizes, and team challenge prizes such as Most Creative and Most Technically Impressive that are separate from tracks.
  The site claims over 100k dollars in prizes across everything.
- Judging criteria are not published for 2026.
  The 2025 day-of site listed creativity, technical difficulty, design, and usefulness, unweighted, with expo judging in a science fair format, a few minutes per team per small group of judges, then top teams go to sponsor and panel judging.
  Submissions closed at 11:15 on Sunday and expo judging ended at 13:00.
- A valid submission needs every field of the form filled in.
  A title and a code link alone is rejected.
- Hardware: "We will provide hardware that you can borrow for your projects."
  The public site says nothing about bringing your own hardware or materials, so the no-brought-items rule assumed in the gecko and tensegrity plans is unverified and needs an organiser answer.
- 2026 sponsors visible on the site include SendCutSend, PCBWay, hackster.io, ASUS, OpenAI, Modal, ElevenLabs, Deepgram, Meta, Firecrawl, and a long list of trading firms.
  The first three are hardware fabrication and maker brands, which is a hint that hardware sponsor prizes are likely, but the 2026 sponsor challenges are not published yet.

Because there is no weighted rubric and judging is expo style head to head, the scoring below weights Demoable double, as the recon skill prescribes.

## What past winners look like

The corpus is fourteen winners across 2023 to 2025, not the twenty the skill asks for.
The 2024 and 2025 Plume galleries are JavaScript only and the browser extension blocks those domains, so 2024 and 2025 come from press and university write-ups.

| Project | Year, prize | One-line pitch | Demo moment | Why it won |
|---|---|---|---|---|
| Griddy | 2025, Sustainability track | Micro-grid prototype with homemade iron-air batteries | Physical batteries powering a small grid | Hardware that measures an outcome, energy loss |
| EyeCraft | 2025, Entertainment track | Minecraft played with mouth, eye, and wink gestures | Someone plays hands free | "How well the demo worked and how everything flowed" |
| Kava | 2025, EigenCloud sponsor | Upload damage photos, get a complete insurance claim | A claim appears from photos | Sponsor API used for a real need |
| Mentra handyman | 2025, Mentra sponsor track | Smart glasses guide assembly and repair | Judge watches a dresser and a LEGO set being assembled from glasses prompts | Physical props, "real-world applicability", the only team to link two glasses |
| Get Away | 2024, Best Beginner | Mark unsafe streets, get safer routes | A route reroutes around a marked spot | Concrete civic use, worked everywhere |
| Unnamed | 2024, Sustainability grand prize plus three sponsor prizes | Backend on Palantir Foundry | Unknown | Stacked sponsor prizes on one project |
| Muse | 2023, grand prize | Search MIT OpenCourseWare lectures for where a concept is explained | Type a concept, jump to the lecture second | Polished, useful to the judges themselves |
| lettuce | 2023, general prize | Scan receipts, track expiry, cut food waste | Receipt to expiry list | Unglamorous problem, complete |
| BeeMovr | 2023, general prize | Helping beekeepers save their bees | Hive data to action | Narrow user, full execution |
| Handwriting Teacher | 2023, Education track | Refine handwriting with AI | Write, get corrected | Clear before and after |
| Fluxus | 2023, InterSystems first | Natural language medical data workspace | Ask, get a chart | Sponsor stack used deeply |
| Echo | 2023, Interactive Media track | Biometric multi-factor auth for gig workers | Log in with a face and a voice | Named a specific, overlooked user |
| Pathosense, PantryPuzzle, Catmosphere, InSightAI | 2023, track and sponsor prizes | Emotion in tech, food sustainability, cozy game, curiosity tool | Various | Each finished a narrow thing |

What they have in common:

- The demo worked, every time, and the write-ups say so explicitly for EyeCraft and Mentra.
- A named user with an unglamorous problem: beekeepers, gig workers, students, someone assembling a dresser.
- A visible before and after inside a minute.
- Hardware winners are rare, and the two that won, Griddy and Mentra, both put a physical object in the judge's hands and paired it with a measured or visible outcome.
- Sponsor prizes stack: the 2024 Sustainability winner also took three sponsor challenges.

## What is saturated

Avoid these shapes, half the room will build one:

1. A language model over a document or lecture corpus with search or summaries, the Muse, Lola, summar.ai, InSightAI cluster.
2. An AI tutor or coach that corrects something you upload, handwriting, essays, speech.
3. Scan a photo or receipt and generate a form, a claim, or a list.
4. Accessibility input for games or apps via webcam gestures.
5. A smart glasses or wearable assistant that narrates the world.
6. The team's own named anti-pattern: an AI app with a sensor bolted on, where the physical part is a prop rather than the point.

None of the six live ideas is on this list.
The evolved structures idea brushes against it if the loop becomes a language model generating designs with no physical test.
The canopy brushes against it from the other side: a light sensor moving a servo is the canonical first Arduino project, and the physical part has to be the point, not a prop.

## Historical full-field scores, 2026-09-05

Raw scores are 1 to 5 as assessed, Prior art inverted so raw 5 means nothing similar exists.
The weighting and the point maps are defined in [the criteria readme](readme.md).
Termite builder is the idea as written in the idea file.
Termite mound is the analog the termite research recommends instead.

### Raw scores

| Criterion | Impact insert | Evolved structures | Bus stop canopy | Gecko foot | Morphing tensegrity | Termite builder | Termite mound |
|---|---|---|---|---|---|---|---|
| Demoable | 5 | 3 | 4 | 3 | 3 | 3 | 3 |
| Number | 5 | 5 | 3 | 3 | 2 | 2 | 5 |
| Track fit | 4 | 3 | 4 | 1 | 2 | 1 | 5 |
| Prize surface | 3 | 4 | 3 | 2 | 2 | 3 | 4 |
| Freshness | 4 | 3 | 3 | 4 | 4 | 4 | 4 |
| Buildable | 4 | 3 | 4 | 3 | 2 | 2 | 3 |
| Prior art | 3 | 2 | 1 | 3 | 3 | 3 | 3 |

### Points under the v2 weighting, maximum 45

| Criterion | Impact insert | Evolved structures | Bus stop canopy | Gecko foot | Morphing tensegrity | Termite builder | Termite mound |
|---|---|---|---|---|---|---|---|
| Demoable, x2 | 10 | 6 | 8 | 6 | 6 | 6 | 6 |
| Number | 5 | 5 | 3 | 3 | 2 | 2 | 5 |
| Track fit | 4 | 3 | 4 | 1 | 2 | 1 | 5 |
| Prize surface | 3 | 4 | 3 | 2 | 2 | 3 | 4 |
| Freshness, mapped | 5 | 3 | 3 | 5 | 5 | 5 | 5 |
| Buildable, x2 | 8 | 6 | 8 | 6 | 4 | 4 | 6 |
| Prior art, mapped | 5 | 3 | 1 | 5 | 5 | 5 | 5 |
| **Total, of 45** | **40** | **30** | **30** | **28** | **26** | **26** | **36** |
| v1 total, of 40, for reference | 32 | 26 | 26 | 22 | 21 | 21 | 30 |

The v1 reference total for the insert uses its v1 Buildable of 3.
The section headings below carry the v2 points.

### Impact insert, 40 of 45

- Demoable 5: drop a mass, two pressure maps or two g traces side by side, lattice against foam. Nobody needs the word auxetic explained to see one trace is smaller.
- Number 5: peak g, and percent reduction against the foam control.
- Track fit 4: Healthcare, as concussion and injury prevention. The catalog's eyeglass frame mount gives a wearable safety framing.
- Prize surface 3: Healthcare track, Most Technically Impressive, and the language model safety report touches OpenAI, ElevenLabs, or Deepgram sponsor prizes if those are offered.
- Freshness 4: no hackathon project found with an auxetic lattice and a live drop test. Commercial helmet impact sensors exist.
- Buildable 4, raised from 3 on 2026-09-05: Shannon's impact liner plan is inventory-only, foam board folded cells, an IMU on a platen, and a hand released drop, so the print risk the 3 rested on is gone. The remaining unproven gate is whether the chosen IMU samples fast enough to resolve a foam board impact without clipping, and the plan has a lower-the-release fallback for it. Not a 5 because a hand release has to be shown repeatable across ten paired trials. The original TPU lattice version stays a 3 until a printer is confirmed.
- Prior art 3: auxetic helmet liners are an active research topic, so the novelty claim must be the live measured comparison, not the material.

### Termite mound testbed, 36 of 45

The analog the termite research recommends in place of the builder: four foam board mounds with different chimney geometry, a heater in each, temperature probes at several heights, and an INA219 so the rise is normalised per watt.
Full rationale, hardware mapping, and prior art are in [the termite research](termite/feasible-build-plan.md).

- Demoable 3: four temperature traces climbing on one screen with one mound staying lower. A screen, lifted by the physical mounds on the table, and lifted to 4 if the restricted thermal camera is approved.
- Number 5: degrees cooler per watt than the sealed control.
- Track fit 5: passive cooling for buildings is Sustainability with no story needed.
- Prize surface 4: Sustainability, Most Technically Impressive on the surrogate design loop that proposes geometry five, and a model API sponsor.
- Freshness 4: nobody else in the room measures a termite mound.
- Buildable 3: every sensor is on the list and there is no printer or robot, but the signal size, whether a 2 to 3 W heater in foam board gives a geometry dependent difference in thirty minutes, is untested, and the list has no power resistor.
- Prior art 3: PNAS 2015 and the 2025 Royal Society Interface review are the science, and no hobby or hackathon testbed was found.

### Evolved structures, 30 of 45

- Demoable 3: a dashboard of generations is a screen, not a moment. The crush or drop test of the printed winner against a control is the moment, and it only works if a coupon prints in twenty minutes as the catalog claims.
- Number 5: load held per gram, percent better than the control.
- Track fit 3: Sustainability via less material for the same strength is arguable, not clean.
- Prize surface 4: sponsor compute and model APIs, Most Technically Impressive, Sustainability.
- Freshness 3: language model plus evolutionary design is a known research direction, and AI generated anything is the default shape at an AI hackathon. The physical rig in the loop is the fresh part and must be real.
- Buildable 3: software heavy, which suits the team's one software engineer. Needs a printer, a load cell, and a scorer that is either a real simulation or the physical rig. Degrades gracefully to three pre-printed generations.
- Prior art 2: topology optimisation, genetic lattice design, and language model to CAD loops all exist in the literature.

### Adaptive bus stop canopy, 30 of 45

- Demoable 4: a lamp comes on, the leaves curl shut with no hinges, the number under the roof drops, the lamp dims and they open. Understood in five seconds, physical, repeatable, and the whole sequence fits in thirty seconds. Not a 5 because the outcome is the one the judge expects. The insert's drop test has two possible answers, the canopy's has one.
- Number 3: the transmitted-light ratio, "the shade state transmits X percent of the control reading". Sayable, but unsurprising, and a light ratio is not the heat or comfort claim the pitch is about. It becomes a 4 with a fixed canopy control across a lamp arc, because then the number compares two designs instead of a roof against no roof.
- Track fit 4: Sustainability, as climate adaptation and heat resilience at transit stops. The clearest track story in the repo, and the team's own research rates it 4 of 5 with measurements. Not a 5 because the prototype measures light rather than heat, and the Houston study found some enclosed shelters made heat stress worse, so "shade means cooler" stays a claim.
- Prize surface 3: Sustainability track, Most Creative on the look, SendCutSend if the leaves are flat cut. Not Most Technically Impressive, because one servo and a threshold rule is first-week firmware.
- Freshness 3: not one of the six saturated shapes, but a light sensor moving a servo is the canonical first Arduino project, and light-responsive kinetic facades are an architecture studio staple. It stays at 3 rather than 2 because hardware is rare at HackMIT and nobody else in the room will bring this.
- Buildable 4: the highest in the set. One servo, two sensors, a threshold rule, and the team's plan has the MVP measured by hour seven with all three hardware people busy and nothing on the software critical path. Not a 5 because the version worth looking at needs printer access, still open, and the TPU flexure thickness is untested. The foam board fallback shows motion but loses the compliant hinge that is the whole point.
- Prior art 1: the Light-Based Canopy System on GitHub is an Arduino Uno, a light dependent resistor, an SG90 servo, and a cardboard canopy that closes when the light is bright, which is this MVP exactly. Flectofin and FlectoLine are the mechanism at full scale from Stuttgart, light-responsive kinetic facade prototypes are a published genre, and bus stop shade products already exist, ShadeBlade in Los Angeles and the UCLA and KDI shade shelter in Oasis. What is new is the combination of a compliant leaf, a bus stop, and a measured comparison, and that is framing, not invention.

What would move it:

- Build two canopies of the same leaf area, one adaptive and one fixed, and sweep the lamp across an arc over a marked waiting spot. The number becomes "the adaptive canopy kept the spot under X percent transmitted light across the whole arc, the fixed one for Y percent of it". That gives the demo a question, the number a comparison, and answers the judge's obvious "why not a bigger roof". Demoable 5, Number 4, total 29.
- Make the compliant hinge visible. If a judge cannot see that the leaf bends instead of pivoting, the canopy reads as the hobby project it resembles.

### Gecko foot, 28 of 45

- Demoable 3: a foot on a panel, a pull at changing angles, a slip warning. The physics needs a sentence of explanation before the judge knows what they saw, and the audit concluded the team cannot recreate gecko adhesion, only a load path bench.
- Number 3: a failure envelope of pull-off force against angle means something to an engineer and nothing to an expo judge.
- Track fit 1: no 2026 track.
- Prize surface 2: Most Technically Impressive at best.
- Freshness 4: nothing on Devpost or GitHub as a hackathon project.
- Buildable 3: the inventory-only plan is the deepest research in the repo, but it needs four sensing modalities including a strain gauge and lists many hardware pain points.
- Prior art 3: incipient slip detection exists as academic work.

### Morphing tensegrity, 26 of 45

- Demoable 3: a structure that morphs is striking, but the team's own feasibility research scopes it down to one three-strut prism with one servo cable moving between two poses. That is a small moment.
- Number 2: a height or twist change in centimetres.
- Track fit 2: the team's own research rates the Sustainability fit at 2 of 5.
- Prize surface 2: Most Technically Impressive.
- Freshness 4: no hackathon prior art found.
- Buildable 2: blocked, in the team's own words, without stiff struts and low creep cord, and the catalog warns the kinematics will eat the night for a first-time tensegrity team. CMA-ES in MuJoCo plus hardware transfer in 24 hours is a research project.
- Prior art 3: NASA Super Ball Bot, the NASA Tensegrity Robotics Toolkit, Yale's differentiable engine, and an open source three-bar tensegrity robot paper.

### Termite builder, 26 of 45

The idea as written: small robots or a placer putting blocks into a structure by local rules, TERMES style.
Full rationale and the three variants are in [the termite research](termite/feasible-build-plan.md).

- Demoable 3: a placer building a shape the judge chose is a moment, but at hour 24 the two rover version is a rover and a slide, and a single arm loses the "they cannot talk to each other" line.
- Number 2: blocks placed, which nobody remembers.
- Track fit 1: no 2026 track, and the disaster shelter story is the stretch the tensegrity research rejected.
- Prize surface 3: Most Technically Impressive and a model API sponsor through the rule compiler.
- Freshness 4: nothing like it in the room.
- Buildable 2: block pickup by a rover has never been done by this team and the catalog says it consumes the night. The single placer variant reaches 3.
- Prior art 3: TERMES and the collective construction field are academic, SMARTArm on Devpost stacks blocks with an arm, and no hobby replication was found.

## Why the others lose

- Tensegrity loses on buildable and number. The team's own two research files say the base robot is blocked on materials and a weak track fit.
- Gecko loses on track fit and the ten second story. It is the best researched idea in the repo and the hardest to explain at an expo table.
- Evolved structures loses only on the live moment, which is why the merge with the insert is the recommendation rather than a rejection.
- The canopy loses to the insert on the story and on novelty, not on execution.
  It was the strongest Sustainability entry before the mound replacement was audited.
  Chosen over the tensegrity, it keeps the shade story the tensegrity research wanted and drops the coupled tendon problem.

- The termite builder loses on Buildable and Track fit, the two things the team said matter most.
  Its ceiling as a single placer is about 31.
  The mound testbed keeps the termite story and scored 36 in this historical snapshot.

## Changes since the first scoring

- 2026-09-05, meeting: the team closed the field to the impact insert, the termite mound testbed, and the bus stop canopy, and adopted the v2 weighting for all further scoring. See [the meeting note](../meetings/2026-09-05.md).
- 2026-09-05, later: the team narrowed to the insert, the canopy, and the termite structure, and set the v2 weighting, Buildable doubled, Prior art peaking at raw 3, Freshness peaking at raw 4. Every idea was re-totalled, the insert's Buildable was raised on Shannon's plan, and the termite idea was researched and scored in three variants.
- Shannon's impact liner plan, 2026-09-05, makes the insert inventory-only: foam board folded cells, an IMU, and a hand released drop, with no printer and no TPU. That removes the print risk the insert's Buildable 3 rests on, so its score would move up, not down, on a re-score. It also narrows the claim from auxetic material to folded-cell geometry. The insert is not re-scored here.
- The same plan means the canopy is no longer the only idea the team can finish without a printer. It is the one that needs a printer most.

## Gaps in this research

- Judging criteria and sponsor challenges for 2026 are unpublished. Re-score when the day-of site goes live in the week of the event.
- The winners corpus is fourteen, not twenty, and the 2024 grand prize winners are unnamed. The Plume galleries need a logged-in browser.
- Whether teams may bring their own materials is unanswered by the public site and still affects the canopy's best mechanism. Email help@hackmit.org.
- The canopy's fixed canopy control is a proposal in this file, not in any build plan. Whether a second canopy fits inside the hour seven MVP is unmeasured.

## Sources

- [HackMIT 2026 site](https://hackmit.org/), dates, tracks, FAQ, prizes, hardware answer, sponsor logos, rechecked 2026-09-07.
- [HackMIT 2025 day-of site](https://dayof.hackmit.org/), judging criteria and process, via search snippet, the page itself is JavaScript only.
- [HackMIT 2023 site](https://archive.hackmit.org/2023/), prize structure and team size.
- [HackMIT 2023 Devpost gallery](https://hack-mit-2023.devpost.com/project-gallery), 173 projects, winners banner.
- [Khoury College on the 2025 winners](https://www.khoury.northeastern.edu/khoury-undergrads-win-three-categories-at-prestigious-mit-hackathon), EyeCraft, Griddy, Kava.
- [UVA McIntire on the Mentra track win](https://experience.mcintire.virginia.edu/news/pierce-brookins-earns-top-spot-hackmit-event/).
- [Tec de Monterrey on Get Away](https://conecta.tec.mx/en/news/monterrey/education/tec-student-wins-award-road-safety-project-hackmit-2024).
- [Palantir CTO on the 2024 Sustainability winner](https://x.com/ssankar/status/1836076339691999679).
- [InterSystems on the 2023 challenge winners](https://community.intersystems.com/post/intersystems-hackmit-2023).
- Prior art: [open source three-bar tensegrity robot](https://arxiv.org/html/2511.05798), [NASA Tensegrity Robotics Toolkit](https://github.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim), [MetaScientist metamaterial design](https://arxiv.org/pdf/2412.16270), [force diverting helmet liner lattice](https://scholarworks.indianapolis.iu.edu/items/f95a55b2-1e22-479b-9a26-de566eef981b), [incipient slip detection](https://github.com/amitparag/Incipient-Slip-Detection).
- Canopy prior art, searched 2026-09-05: [Light-Based Canopy System](https://github.com/Rainier-PS/Light-Based-Canopy-System), [IAAC light responsive kinetic facade](https://blog.iaac.net/light-responsive-kinetic-facade/), [Arduino forum kinetic facade prototype](https://forum.arduino.cc/t/kinetic-facade-prototype-academics/1206777), [solar control kinetic facade prototype](https://www.researchgate.net/publication/332752726_Developing_a_kinetic_facade_towards_a_solar_control_facade_design_prototype), [Flectofin](https://www.uni-stuttgart.de/en/university/news/all/First-Gips-Schuele-Research-Prize-for-bionic-facade-shading-systems/), [FlectoLine](https://www.uni-stuttgart.de/en/university/news/all/FlectoLine-Facades-in-motion/), [ShadeBlade bus stop shade](https://www.outfrontjcdecaux.com/sunshade_blade/index.html), [UCLA and KDI shade shelter prototype](https://innovation.luskin.ucla.edu/2022/10/07/new-shade-shelter-prototype-aims-to-keep-transit-riders-cool). No bus stop shade or adaptive canopy project found on Devpost.
- Termite prior art, rechecked 2026-09-07: [TermiCool Pro](https://devpost.com/software/termicool-pro-eqsj1r) and [Bamboo House](https://devpost.com/software/bamboo-house), direct maker-event overlap without the proposed matched-power repeated comparison.
- [UTHealth Houston bus stop heat study, 2025](https://phys.org/news/2025-05-bus-relief-result-higher-temps.html), 17 stops, tree shade lowered heat stress and some enclosed shelters raised it.
- Team research this scoring leans on: [tensegrity feasible build plan](tensegrity/feasible-build-plan.md), [tensegrity sustainability relevance](tensegrity/sustainability-relevance.md), [cohesive gecko plan](gecko/cohesive-gecko-plan.md), [Load Paths catalog takeaways](load-paths-catalog-takeaways.md), [canopy build plan](adaptive-bus-stop-canopy/feasible-build-plan.md), [canopy sustainability fit](adaptive-bus-stop-canopy/sustainability-relevance.md), [impact liner build plan](impact%20helmet/feasible-build-plan.md), [termite research](termite/feasible-build-plan.md), [frontrunner tweaks](frontrunner-tweaks.md).
