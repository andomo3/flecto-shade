# R1: research how to simulate and render the stop, 2D or 3D, and where its geometry comes from

The build agent's first task, written 2026-09-19, when Plan B began to look certain.
It is research with small throwaway spikes, and its output is a decision, not a feature.
It is time boxed to 120 minutes, and it stops at the box even if a question is still open.

## Why this comes first

The team wants to show the bus stop in 3D, reacting to the sun, "using physics".
That sentence hides three different simulations, and they differ by a factor of a hundred in cost.
R1 exists so nobody builds the expensive one by accident.

| Layer | The physics | The planner's view before any research |
|---|---|---|
| Light | Which rays from the sun reach the bench past the roof, and the shadows on the ground | Viable, and already planned as B1 to B4 in `../plan-b-simulated.md`. Geometry and ray casting, exact for direct light |
| Control | Light sensor, threshold with hysteresis, a servo that takes four seconds | Viable and trivial: it is the firmware's control law run on the laptop, B4 |
| Leaf mechanics | The lamina buckling sideways as the backbone bends: large deflection, thin shell, an instability | Not viable live. A real time nonlinear shell solver is a research project. Viable only offline, in a tool built for it, or as an honest approximation |

So the working answer is: simulate the light with real physics, simulate the control exactly, and do not simulate the leaf's mechanics live.
The leaf's shape at each pose comes from one of the three sources below, and R1 finds out which one is reachable today.

1. **Offline physics, from the engineers' CAD tool.**
   A nonlinear static study of one leaf, run once, with the deformed shape exported at a few load steps.
   The page then blends between those shapes.
   This is the only route that lets the team say "the bent shape is from a physics simulation of our own leaf".
2. **A kinematic model from the published Flectofin work.**
   The lamina's deflection angle as a function of the backbone's bend, taken from the Stuttgart papers, applied to the CAD's resting shape.
   Said as "a kinematic model after the published principle".
3. **A plain parametric approximation.**
   A rib on an arc and a sheet rotated about it by up to 90 degrees, one parameter from 0 to 1.
   Said as "simplified leaf geometry".

One boundary that R1 does not reopen: the leaves react to how bright the light is, through a threshold, and have two states.
They do not track where the sun is.
A roof that steers toward the sun would be a different product from the one in the CAD, and showing it would misdescribe what the team designed.
"Reacting to the sun's position" on screen means the sun moves along its real path, the shadows move with it, the light on the sensor changes, and the threshold does the rest.

## Questions to answer, each with evidence

### A. Rendering in the browser

The page is one HTML file with vanilla JavaScript, no build step, no CDN, and no network at the table.

1. Can three.js be vendored as local ES module files and imported with an import map, with no bundler and no network?
   Name the exact files needed for the core, an STL or glTF loader, and orbit controls, and their total size.
2. STL or glTF from the CAD: which is better here, given that blending between poses needs the same vertex order in every pose?
   State whether STL exports of different poses keep a consistent vertex order, and what to do if they do not.
3. Shadows: does a directional light with a shadow map give a readable moving shadow on the bench at laptop integrated graphics frame rates?
   Measure frames per second on the demo laptop with a stand in mesh of about 50,000 triangles.
4. Blending between leaf poses: morph targets in glTF, or interpolating vertex positions by hand.
   Which is simpler without a build step?
5. The fallback if WebGL is poor on the demo laptop: pre rendered frames from the CAD tool, one image per pose and sun position, shown as a flipbook.
   How many frames, and how large?

### B. The leaf's shape

6. Which CAD tool do the engineers use, and can it run a nonlinear static study with large displacement on a thin part?
   [The team has not said which tool. Ask, and do not guess.]
7. Can that tool export the deformed shape as a mesh at several load steps, and does the mesh keep its vertex order between steps?
8. From the published Flectofin papers, Lienhard and others at the University of Stuttgart, is there a stated relation between the backbone's bend and the lamina's deflection angle?
   Quote it with its source, or say it was not found. Never invent it.
9. How long would route 1 take the engineers, honestly, and what is the chance it does not converge?
   Buckling studies often fail to converge, and the imperfection that seeds the buckle, the built in resting curve in `../../hardware/leaves/CLAUDE.md`, has to be in the model.

### C. The light simulation

10. `trimesh` 5.1.0 and `rtree` 1.4.1 are confirmed to exist.
    Install them in a scratch environment and time a ray cast of 10,000 rays against a 50,000 triangle mesh, with and without `embreex`.
    State whether the shade table in B3, about 1,400 sun directions by 6 meshes, finishes in minutes or hours.
11. Is there a reason to do the ray cast in the browser and not in Python? The planner's view is no: the table is computed once, offline, and the page only looks values up.
12. Diffuse light: is a sky view factor from a hemisphere of rays enough, as B10 proposes, and how many rays make it stable to two decimal places?

### D. Whether the 3D scene replaces the drawn scene

13. `../../software/ui-brief.md` asks for one drawn scene, from the front, that passes a 3 second test at a metre.
    Does a 3D view help that, or compete with it?
    Propose where the 3D view lives: as the scene itself, as a second view the speaker switches to, or only in the video.
14. What is the smallest version that is still worth showing: a fixed camera, the sun on its arc, the shadow moving, three leaves blending between two poses.

### E. A 2D simulation or a 3D one

Two different things are being asked, and they have different answers, so keep them apart.

- The **computation**: how the light on the bench is worked out.
- The **picture**: what the judge sees.

The planner's view, to be tested and not taken on trust:

- The computation should be 3D.
  The sun moves in two angles, elevation and azimuth, so a flat cross section is only right when the sun happens to sit in that plane.
  A 3D ray cast against simple meshes is cheap, because it runs once, offline, into a table.
- The picture should be 2D first.
  `../../software/ui-brief.md` already specifies one drawn scene, from the front, in SVG, that reads in three seconds from a metre away, and `../../software/mockup-prompt.md` has a 28 row scorecard for it.
  A 2D scene driven by the 3D table is honest, fast, and cannot fail on a weak graphics chip.
- A 3D picture is the stretch: a second view, or only the video.

15. Test that view against the alternatives, and recommend one: 2D computation with a 2D picture, 3D computation with a 2D picture, or 3D computation with a 3D picture.
    For each give the build time in hours, what can break at the table, and what a judge sees in the first three seconds.
16. If the computation were 2D, how wrong would it be?
    Take the demo day, 5 July 2013 in Houston, a stop facing a stated direction, and compare the shaded fraction from a front view cross section against the 3D ray cast at 09:00, 13:00, and 17:00 local.
    A rough spike is enough, and the point is the size of the error, not its third decimal.
17. In the 2D picture, how do the leaves, the shadow band on the bench, and the light shafts get drawn from the table's numbers, so that what is drawn never disagrees with what is computed?
    A shadow drawn by eye that contradicts the bar beside it is worse than no shadow.
18. Which way does the stop face?
    It changes every number, and nobody has decided it.
    Propose a default, give the reason, and show how much the day's result moves if it faces the other three ways.

### F. Whether the team can develop the CAD for the simulation

The engineers have a CAD model, and what it contains is not known: possibly one leaf, possibly the rig, probably not a whole bus stop with a bench at real proportions.
The simulation needs five meshes in one frame of reference: the stop, the leaves resting, the leaves bent, a few poses between, and a fixed slab.

There are two ways to get them, and the second one does not depend on the engineers at all.

- **From the engineers' CAD tool**, exported as STL or glTF.
  It carries the team's real leaf, and it carries the vertex order problem from question 2.
- **Generated in code**, by the build agent.
  The stop is a handful of boxes and cylinders.
  The leaf is a parametric surface, a grid of points on a rib and a sheet, bent by one parameter from 0 to 1.
  Because every pose comes from the same grid, the vertex order is identical in every pose, so blending is free, and the leaf's dimensions are constants the engineers can read and correct.
  Its weakness is honesty: it is the agent's geometry and not the team's CAD, unless its dimensions are taken from the CAD and the engineers sign them off.

19. Compare three ways to generate geometry in code, each checked for a Python 3.13 wheel on Windows before anything is recommended: plain `numpy` grids exported with `trimesh`; `cadquery` 2.8.0 or `build123d` 0.12.0, which exist on PyPI but whose geometry kernel may not have a Python 3.13 wheel; and OpenSCAD, which is a separate program.
    The planner expects plain `numpy` with `trimesh` to win, because it adds no dependency and gives full control of the vertex order.
20. Write down, as a table the engineers can fill in ten minutes, every dimension the generated stop and leaf need: post height, roof width and depth, bench height and length, leaf length, rib thickness, sheet thickness and width, the spacing of the three leaves, the resting curve, and the bend and the sheet's rotation at full flare.
    Mark each as "from the team's CAD", "from a published source, linked", or "assumed".
21. Can the two routes be combined: the stop generated in code, and only the leaf taken from the engineers' export?
    State what that needs from them, and by when.
22. What does the result card have to say about the geometry under each route, in one line, so that the pitch stays honest: "from our CAD", "generated from our CAD's dimensions", or "simplified geometry"?

## What may be written

- Spikes are allowed, because a viability question is answered by trying it.
- They live under `spikes/R1/` on a branch named `research/R1`, which is never merged.
- A spike is under 100 lines, has no tests, and is deleted or left on the branch.
- Nothing is installed into the project's environment: use a scratch virtual environment.
- No file under `planning/` is touched, and nothing is read from the `hack-mit` prototype directories.

## The deliverable

One Markdown file, `research/R1-simulation.md`, on the branch, and its text pasted in the reply.

1. The answer in three lines: what to build, what not to build, and the one risk.
2. A table with a row for each of the 22 questions: the answer, the evidence, and "verified by running", "verified by reading", or "assumed".
3. The recommended stack, every dependency with its version, its licence, its size, and proof it exists.
4. The leaf shape decision: route 1, 2, or 3, with the reason, and what the engineers must export, in what format, by when.
5. A proposed list of work packages to follow, each with a one line goal, a check, and minutes, so the planner can turn them into specs.
   Expected: the vendored renderer, the mesh loader and pose blend, the sun and shadow, the link to the simulator's `angle` and sun position, and the fallback flipbook.
6. What to say and what never to say about the simulation, in the pitch's honesty terms: light is simulated with geometry, the leaf's shape is from whichever route was used, nothing is measured.
7. Every source, as a link.

## Done when

- The file exists and answers all 22 questions, each marked verified or assumed.
- Questions 3 and 10 carry a measured number from the demo laptop, or a plain statement that the agent could not run on it and who must.
- Question 6 is answered by a person, or marked blocked, and never guessed.
- No claim about the Flectofin papers appears without a link.
- The 120 minute box was kept.

## Rules of evidence

Separate what was run from what was read from what is assumed.
Never invent a library, a function, a file format capability, or a number.
If a CAD tool's capability cannot be confirmed from its own documentation, say so.

## The prompt to paste to the build agent

```text
CONTEXT
You are working in the repo flecto-stop, the HackMIT 2026 submission. Read AGENTS.md at
the root first and follow it, then planning/plans/plan-b-simulated.md. Never read or copy
code from the planning repo github.com/andomo3/hack-mit: its firmware/canopy,
firmware/host_test, software/canopy, and tests directories are an off-limits prototype.

TASK
Carry out research package R1, specified in
planning/plans/packages/R1-simulation-research.md. It is research with small throwaway
spikes, time boxed to 120 minutes. Its output is a decision document, not a feature.
Work autonomously through all 22 questions, in sections A to F.
The engineers' CAD tool is: [NAME, or "not known yet: mark questions 6, 7, and 9 as
blocked and carry on with the rest"].

CONSTRAINTS
- Build nothing outside spikes/R1/ on the branch research/R1. Never merge that branch.
- Use a scratch virtual environment. Install nothing into the project.
- Separate what you ran from what you read from what you assume. Never invent a library,
  a function, a file format capability, or a number. No claim about the Flectofin papers
  without a link.
- The planner's views in the package are hypotheses to test. Say plainly where you
  disagree, with evidence.
- The leaves react to light through a threshold and have two states. Do not design a
  roof that tracks the sun's position. Do not simulate the leaf's buckling live.
- Stop at 120 minutes even if a question is open, and say which.

FORMAT
Write research/R1-simulation.md on the branch, in the seven sections the package lists,
and paste its full text in your reply. Lead with the answer in three lines: what to build,
what not to build, and the one risk.
```
