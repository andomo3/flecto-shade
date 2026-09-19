# R1: research how to simulate and render the stop in 3D

The build agent's first task, written 2026-09-19, when Plan B began to look certain.
It is research with small throwaway spikes, and its output is a decision, not a feature.
It is time boxed to 90 minutes, and it stops at the box even if a question is still open.

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

## What may be written

- Spikes are allowed, because a viability question is answered by trying it.
- They live under `spikes/R1/` on a branch named `research/R1`, which is never merged.
- A spike is under 100 lines, has no tests, and is deleted or left on the branch.
- Nothing is installed into the project's environment: use a scratch virtual environment.
- No file under `planning/` is touched, and nothing is read from the `hack-mit` prototype directories.

## The deliverable

One Markdown file, `research/R1-simulation.md`, on the branch, and its text pasted in the reply.

1. The answer in three lines: what to build, what not to build, and the one risk.
2. A table with a row for each of the 14 questions: the answer, the evidence, and "verified by running", "verified by reading", or "assumed".
3. The recommended stack, every dependency with its version, its licence, its size, and proof it exists.
4. The leaf shape decision: route 1, 2, or 3, with the reason, and what the engineers must export, in what format, by when.
5. A proposed list of work packages to follow, each with a one line goal, a check, and minutes, so the planner can turn them into specs.
   Expected: the vendored renderer, the mesh loader and pose blend, the sun and shadow, the link to the simulator's `angle` and sun position, and the fallback flipbook.
6. What to say and what never to say about the simulation, in the pitch's honesty terms: light is simulated with geometry, the leaf's shape is from whichever route was used, nothing is measured.
7. Every source, as a link.

## Done when

- The file exists and answers all 14 questions, each marked verified or assumed.
- Questions 3 and 10 carry a measured number from the demo laptop, or a plain statement that the agent could not run on it and who must.
- Question 6 is answered by a person, or marked blocked, and never guessed.
- No claim about the Flectofin papers appears without a link.
- The 90 minute box was kept.

## Rules of evidence

Separate what was run from what was read from what is assumed.
Never invent a library, a function, a file format capability, or a number.
If a CAD tool's capability cannot be confirmed from its own documentation, say so.
