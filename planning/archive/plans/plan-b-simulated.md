# Plan B: the simulated demo

> **SUPERSEDED on 2026-09-19 at about 16:45. This file is the record of the bus stop canopy, and nothing is built from it.**
> The current plan is the simulated louvre roof over three crops.
> Read `AGENTS.md` and `CHECKLIST.md` at the repo root, then `planning/plans/plan-d-louvre-roof.md`.
> If you are a build agent and you arrived here, stop, and go back to those files.

Applies when the gate in `README.md` is not passed at 17:00 Saturday.
The judge watches a simulated roof, built from the team's own CAD and real solar data, and everything on screen is said as simulated.
The story, the hero, the screen, and the closing line do not change.

## The MVP

A virtual board.
`SimSource` stands where the Arduino would, runs the same control law, and prints the same eleven fields of `../firmware/SERIAL_FORMAT.md` version 2.
Where the real board would read a light sensor, the simulator computes the light from the sun's real position and the shape of the roof.

```text
real Houston day --> sun position, direct and diffuse irradiance
                          |
CAD meshes --> ray cast --> shade table: fraction of light reaching the bench,
                          |  for each sun elevation, azimuth, and leaf pose
                          v
SimSource: light --> threshold with hysteresis --> leaf angle --> bench light --> v2 line
```

In: the shade table from the CAD, the virtual board with the control law, the scene on screen posed from the leaf angle, a fixed slab roof as a third bar, one interaction that proves it is not a script, the result card for one day, and the typical year result.
In if time allows, in this order: diffuse light, the laptop camera as a real light sensor, a CAD render as the scene, the city picker.
Out: a buckling or stress simulation of the leaf, a 3D viewer, anything that needs a network at the table.

What the simulation is and is not.
It is geometry: which rays from the sun reach the bench past the roof.
It is not mechanics: it does not show that the leaf buckles, how much force it takes, or how long it lasts, and the pitch never says it does.

## What the engineers supply

They have the CAD, and these exports are their whole build in Plan B, so their hands are free for a physical leaf if any material turns up.

| Item | Format | Note |
|---|---|---|
| The stop: posts, beam, bench, ground | One STL or OBJ, millimetres, Z up, the bench centre at the origin | The bench top is named or its height is given, because rays are cast at it |
| The leaves, resting | One mesh, same frame | |
| The leaves, fully bent | One mesh, same frame | If the CAD holds only the resting shape, see the fallback below |
| The leaves at 25, 50, and 75 percent | Three meshes | Optional, and the shade fraction is interpolated between poses without them |
| A fixed slab roof with the same footprint as the bent leaves | One mesh | This is the conventional shelter, and it is ten minutes of CAD |
| [The CAD tool and its export format] | | Not yet known, ask first |

Fallback when no bent mesh exists: the leaf is generated in code as a rib on an arc with a flat sheet rotated about it by up to 90 degrees, one parameter from 0 to 1.
It is an approximation of the Flectofin motion and the result card says "simplified leaf geometry".

## The build, after the shared core

The shared core, C1 to C9 in `README.md`, comes first and is identical to Plan A.
The new dependencies are `trimesh` 5.1.0 and `rtree` 1.4.1, both confirmed on PyPI on 2026-09-19, neither yet tried on the demo laptop, and both cited in the submission.

| ID | Build | Done when |
|---|---|---|
| B1 | `sim/meshes.py`: load the meshes, check units, frame, and that each is watertight enough to cast against | A test loads every mesh, prints its bounding box in millimetres, and fails loudly on a mesh in the wrong frame |
| B2 | `sim/shade.py`: for one sun direction and one roof mesh, cast a grid of rays from the bench top toward the sun and return the fraction that escape | Three hand checks in a test: no roof gives 1.0, a slab with the sun overhead gives about 0.0, and a sun below the horizon gives no light |
| B3 | `sim/table.py`: run B2 over sun elevation 0 to 90 and azimuth 0 to 360 in 5 degree steps, for each leaf pose and the slab, and write `processed/shade-table.csv` | The script runs offline, the table has no gaps, and bent is never brighter than resting at high sun |
| B4 | `SimSource` in `sources.py`: on each tick take the sun from `day.py`, map irradiance to `light` on 0 to 1000, run the threshold with hysteresis and a servo step limited to the real four second bend, look up `bench` and `fixed`, and print a v2 line | `python -m canopy serve --source sim` plays the day, the leaves bend after sunrise and rest after sunset, and C1's parser accepts every line |
| B5 | The proof interaction: a cloud the judge drags across the sun on the page, which POSTs `/cloud` and cuts `light` in the simulator | Dragging the cloud over the sun at noon rests the leaves, and removing it bends them again, within the same delays as the real control law |
| B6 | `sim/year.py`: run the full 8,760 hour PVGIS typical year through the table for three roofs, always resting, the fixed slab, and adaptive | It writes one small CSV and prints, for each roof, the share of the year's direct light that reaches the bench, split into the hot months and the cool months |
| B7 | The result card for Plan B: three figures for the day, and one line from B6 for the year, under the words "Simulated from our CAD and public solar data" | State 5 renders from a recorded sim run with no network |
| B8 | The page in simulated mode: a banner in words, "Simulation: no hardware is connected", and the third bar always present | The banner shows whenever the source is `sim`, in every state |
| B9 | Record one clean sim run into `fixtures/` | It replays through `FixtureSource` and gives the same result card |

Stretch, only when B1 to B9 are green.

| ID | Build | Done when |
|---|---|---|
| B10 | Diffuse light: the sky view factor from the bench for each pose, from rays over the whole hemisphere, so `bench` is direct times the beam fraction plus diffuse times the sky view | The overcast hours in the year no longer read as full shade |
| B11 | The laptop camera as a real light sensor: the page reads the camera with `getUserMedia` on localhost, averages the frame brightness, and POSTs it as `light` | The judge covers the camera with a hand and the virtual leaves relax, with the network off |
| B12 | The scene drawn from a CAD render of each pose, in place of the drawn leaves | State 3 still passes the scorecard |

B11 matters more than its place in the list suggests, because it puts one real sensor and one real hand back into the demo.
It is a stretch only because it is untested.

## The real leaf flaps with the simulation

Decided 2026-09-19: the team can demo the flapping leaf and nothing else, so the whole stop, the sun, the sensing, and the reaction are simulated, and the real leaf is driven by the simulation.
The contract already has the command for it: `S 0` to `S 180` sets the leaf servo's angle and turns the override on.
So the simulated stop decides when to bend, and the leaf on the table bends at the same moment as the leaves on the screen.
It is a digital twin run backwards: the model drives the object.

| ID | Build | Done when |
|---|---|---|
| B13 | A minimal sketch, Plan B's only firmware: read `S n` and `P` over serial, step the servo toward `n` a few degrees per tick so the bend takes about four seconds, and print a v2 line ten times a second with `angle` set, `override` 1, and every sensor field empty | Typing `S 120` then `S 0` in a serial monitor bends and rests the leaf, garbage input does nothing, and C1's parser accepts every line. The build agent writes it, and a person flashes it |
| B14 | The twin link in the app: when `--source sim` is given a `--port`, forward the simulator's `angle` to the board as `S` commands ten times a second, and carry on without complaint if the port is absent or the cable is pulled | The leaf on the table follows the leaf on the screen within about a third of a second, pulling the cable leaves the simulation running, and plugging it back in recovers |
| B15 | Stretch, and recommended: the team's one photoresistor on the same board, printed in the `light` field, and used by the simulator as the cloud over its virtual sun | The judge covers the real sensor with a hand, the simulated light drops, the simulated leaves relax, and the real leaf relaxes with them |

B15 is what would put "cover the sensor" back into the demo with real hardware, and it is the only route left to the Arduino challenge, which asks for raw data from the physical world.
Without B15 the Arduino challenge is dropped.

What is said, and never said, about the leaf on the table:

- Said: "This leaf is real. The stop around it is simulated, and the simulation is driving the leaf."
- Never said or implied: that the leaf senses anything, that it was tested under light, or that its motion was measured.
- With B15: "That sensor is real too. Your hand is the cloud."
- The page carries a banner in words whenever the twin link is on: "The simulation is driving the leaf on the table".

## Why the simulation is worth showing

It answers questions the physical model cannot.

- Adaptive against a fixed roof, which on the table needed an extra hour of foam board.
- "Why not leave it bent all summer?", because B6 splits the year into hot and cool months and shows what the open state gives back in winter.
- "What about low sun?", because the table covers every sun angle and the honest answer is visible in it.
- A whole year, not one afternoon.

And it fits "Signal in the Noise" better than the replay did, because it turns 8,760 hours of public solar data into one finding about one roof.
The METRO ridership analysis in `../docs/research/adaptive-bus-stop-canopy/voloridge-datasets.md` then says which stops that finding matters at.
Both are said as modelled, and the question about Voloridge's curated list still has to be asked first.

## The demo, ninety seconds

Beats 1 to 5 and 7 to 9 of `../pitch/storyboard.md` hold.
The table column changes, and beat 6 is replaced.

| Time | Say | The table | The screen |
|---|---|---|---|
| 0:00 | "Picture Rosa." The opening, unchanged | The laptop, and whatever is physical: a leaf the judge can bend, or a printed render | The night scene, one Play button, no numbers, the simulation banner |
| 0:10 | The study, trapped heat, the moving sun | Hands off | Unchanged |
| 0:20 | "We could not build the whole stop this weekend. This leaf is real. The stop around it is simulated, and the simulation drives the leaf." | The real leaf, resting, on its servo | Unchanged |
| 0:30 | "Would you press play?" | The judge presses Play | The sun rises along its real path, the sky warms, three bars climb |
| 0:40 | "The light crosses the threshold. Watch the screen, and watch the leaf." | The real leaf bends, at the same moment | The leaves on screen bend over four seconds, the Bench bar drops away from the Sun bar, and the Fixed roof bar sits between them |
| 0:50 | "Drag that cloud over the sun." Or, with B11: "Put your hand over the camera." | The judge drags, or covers the camera | The Sun bar collapses, the leaves relax, the cloud leaves, they bend again. Caption: "The light moves the leaves, not the clock" |
| 1:05 | "And when the sun goes, the roof opens again." | | The sun sets, the leaves rest |
| 1:15 | "In the harsh hours, the bent leaves cut the sun on the bench to X percent, against Y if they never moved. A fixed roof could do that too. What it cannot do is open: across the cool months our leaves give back W percent of the sun a fixed roof blocks. Those are simulated, and the card says what it leaves out." | | The result card |
| 1:25 | The closing line, unchanged | | Stillness |

Why the number is said that way: a fixed slab with the same footprint shades the bench as well as the bent leaves do at noon, and it shades all day, so "our leaves against a fixed roof" over a whole day would make the adaptive roof look worse.
The honest claim is the same shade in the harsh hours, and the light, the air, and the winter sun given back in the others.
The result card, package B7, shows X against Y for the harsh hours of the day and W for the cool months, and package B6 must produce all three.
The full scripts are in `../pitch/script-plan-b.md`, each inside its word target.

The judge still touches the project twice: Play at 0:30 and the cloud or the camera at 0:50.
Saying the missing hardware out loud at 0:20, once and without apology, is what keeps the rest believable.

Fallbacks, in order: the recorded sim run through `FixtureSource`, then the screen recording.

## The presentation

### What stays

Rosa, the villain, the lens of human life, the farmworker and the grower in the vision beat, the closing line, the rain answer, and every question in `../pitch/questions.md` that is not about the rig.

### What changes

- **The honesty line.**
  "Measured today on this table" is never said.
  It becomes "simulated from our CAD and public solar data", and nothing is called measured.
- **Card 1** becomes "Simulated today": the three figures, the mesh and the dataset they came from, the ray count, and the step size of the table.
- **Card 2, "Not yet claimed"** gains three lines: that the leaf buckles as drawn, anything about force, fatigue, or the servo, and any measurement at all.
  It also says what the ray cast ignores: reflected light, and diffuse light unless B10 shipped.
- **The scripts** need one new sentence, the 0:20 line above, and the number sentence rewritten.
  Both are checked with `pitch_timer.py` so each length stays inside its word target.
- **The video** is a screen recording with a voice over, plus any footage of a leaf being bent by hand.
- **The submission** says simulated in its first paragraph, drops the Arduino challenge, and cites `trimesh`, `rtree`, `pvlib`, PVGIS, and the build agent.

### New questions to have answers for

- **"So nothing is built?"**
  "The software is built, all of it this weekend, and it would drive the real board unchanged, because the simulator speaks the same serial format the Arduino would. The roof is CAD. We could not source [the parts], and we chose to show an honest simulation over a fake demo."
- **"How do I know the simulation is right?"**
  "Three checks you can run on that laptop: no roof gives full light, a slab under an overhead sun gives none, and the numbers move the right way as the sun drops. It is geometry, not physics, and the card lists what it ignores."
- **"How do you know the leaf really bends like your CAD?"**
  "We do not, from this. The bending principle is published, Flectofin, from the University of Stuttgart. [If a leaf is on the table: and this one bends the same way in your hand.] Proving our leaf does it under a servo is the first thing the parts were for."
- **"Why should a simulation win a hardware track?"**
  "It should not beat a working machine. What we can offer is a finding a tabletop model could not give: a whole year, and adaptive against fixed."

## The clock

| When | What must be true |
|---|---|
| 17:00 Saturday, hour 6 | The gate is decided, the shared core C1 to C7 is green, and the engineers know the export list |
| 19:00, hour 8 | The meshes are exported and B1 passes, or the generated leaf fallback is chosen |
| 21:00, hour 10 | B2 and B3: the shade table exists and passes its hand checks |
| 23:00, hour 12 | The hard checkpoint: `--source sim` plays the day end to end on the page, B4 and B5 |
| 23:00 to 00:45 | B6 and B7, then the safety screen recording |
| 01:00 Sunday | Freeze: nothing new after the venue closes |
| 07:00 to 09:00 | B8, B9, the stretch only if everything is green, cards 1 and 2 rewritten with the real figures |
| 09:00 to 10:30 | Rehearsal with the 0:20 line, the scripts re-timed, the submission checked |
| 11:00 | Submitted |

## Risks

- The meshes arrive late, in the wrong units, or not watertight: B1 exists to catch this at hour 8 and not at hour 12, and the generated leaf is the fallback.
- The pure Python ray caster is slow: the table is computed once, offline, so a slow caster costs minutes and never touches the demo.
- A judge reads a simulated figure as measured: the banner, card 1, and the spoken line all say simulated, and no figure appears without the word.
- The simulation flatters the leaf, because a CAD pose is an ideal: the card says so, and the fixed slab is given the same footprint so the comparison is fair.
