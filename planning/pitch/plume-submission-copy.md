# Plume submission copy, ready to paste

Written 2026-09-20 at 09:35, from the Plume page abba exported.
Submission closes at about 10:59.
Everything below is checked against the repository, and nothing in it is a claim the project cannot support.

## What Plume already has

- Track: **Sustainability**.
- Name on Plume: **FlectoShade**. The repository, the page title and every pitch document say **Flecto Shade**, two words. **Pick one and make them match**, because a judge comparing the page to the submission will notice. The planner recommends two words, since the live page's title and the README already use it and the URL does not depend on it.
- Table: **50, Johnson Track**.
- Sponsor challenges are listed on the page. Which ones to enter is below.
- Inspiration, What it does and How we built it are already written.
- Individual Contributions has Shannon's only.

## The four empty sections

### Challenges we ran into

The hardest one was giving up the build. We came to make a physical roof, and by Saturday evening it was clear we could not: no materials, no actuators, and not enough hours left to do it honestly. Choosing to simulate instead meant throwing away the plan we had defended for a week, and it cost us most of a day to admit.

The data fought us next. We joined a typical meteorological year of sun to one real year of rain, and the join quietly manufactured a signal: rainy afternoons came out brighter than dry ones, a ratio of 1.11. Nothing in our tests caught it, because the annual means were fine.

Our build agent fought us twice. It read our planning folder, found an idea we had set aside but never deleted, and built nine packages of the wrong product. Later, a second attempt replaced our page instead of adding to it, dropping the scripts that draw the roof and introducing a second rain model beside our shared rules. We did not merge it.

And we ran out of time on a flaw we already understood. Crop water use in our model is multiplied by how far the roof is open, so under a shut roof it falls to zero. A shaded plant transpires less, never nothing. Fixing it moves every soil figure and every expected value we test against, so we chose to name it publicly rather than patch it in the last hours and ship something we had not checked.

### Accomplishments that we're proud of

We came to HackMIT to build a greenhouse. We left having simulated one, and that pivot is the accomplishment I am proudest of.

The fin came first. Shannon modelled the Flectofin in Onshape and rendered it in Solidworks: two rectangular laminae on a central backbone, buckling the way the bird of paradise flower does. It was a real artifact, drawn by hand, and it was beautiful. But a model that only moves is a model that only moves - it cannot tell a grower whether opening the roof at three o'clock was the right call.

That was the moment we had to choose. Admittedly, abandoning the build we had come for was hard; we had the drawings, we had the intent, and we had a day already spent. The problem, though, did not care about our plan. Different beds under one roof want different light and different rain, and no amount of geometry answers that on its own. So we pushed through the pivot rather than around it.

What we built supplements the CAD rather than replacing it. The geometry Shannon drew is the roof you watch move in the browser - tessellated once and committed, not an artist's impression. Around it we built the part that was missing: nine written rules, a real year of Central Florida weather, and a reason in plain words for every decision the roof makes. One storm, three beds, three answers, and each bed says why.

Moreover, we held a line we could have quietly crossed. No AI and no learned model sits in the loop; the fins never chase the sun; two runs of the same day produce byte for byte identical output. Our own tests fail the build if the page ever claims a saving in water, cost, or energy, and one of our commits exists precisely because a code comment tripped that gate. Every figure on the screen says where it came from, and what is not ours is credited first and unprompted: the fin is ITKE's, patented as EP2320015, and the control logic is standard practice in greenhouse computers.

Ultimately, the pivot is what made the project honest. We stopped trying to show a roof, and started trying to show a decision.

### What we learned

We arrived intending to build a greenhouse, and we learned instead how to simulate one.

In hindsight, the constraint taught us more than the build would have. We did not have the materials, the actuators, or the hours. What we did have was a real problem and a way to interrogate it, so we asked a narrower question: "if the roof could decide bed by bed, what would it actually decide?" Answering that needs no hardware at all. It needs weather you can trust, rules a stranger can read, and the discipline to label every number.

The weather taught us the first lesson. We joined a typical year of sun to a real year of rain, which is a standard move, and it produced rainy afternoons brighter than dry ones: a ratio of 1.11. That cannot happen outdoors. Taking the sun from the same place and the same year gave 0.627, and that check is now written into our build so it cannot drift back. Hence the habit we intend to keep: find a relationship whose sign you already know, and ask the data whether it agrees. Our annual means had looked perfect the whole time.

The agent taught us the second. Devin built the wrong product because our planning folder still held an idea we had set aside; it replaced our page because we described a feature instead of naming the files it was allowed to touch. Every failure was a failure of context, not of capability - and that distinction changed how we write, both for machines and for each other.

The pivot taught us the third, and it is the one I will carry. A real problem survives the loss of your preferred solution. We could not build the roof; the beds still want different light, the storm still falls on the wet one and the dry one alike, and the grower still moves the plant to change what it receives. Thus the work was never the hardware. It was the decision underneath it, and that we could build.

### What's next for our project

Three things, and the most sceptical one is first.

We stress our own model. We have twelve constants that we chose rather than measured, and we have written the protocol for a Monte Carlo study over all twelve before running any of it, so the study cannot be bent afterwards to fit what it finds. The question it answers is whether our headline claim, that three zones give three different answers to one storm, survives our own guesses.

We check our inputs against the ground. The University of Florida runs a weather station at Apopka, and our own research already found that swapping the modelled satellite sky for a station on site changes what the roof does in about a fifth of daylight hours. That is a finding about our fragility, and it needs no hardware to pursue.

Then the roof starts keeping a record. A roof that decides bed by bed knows what every bed was given, hour by hour. Paired with soil sensors, that record is the part that outlives the roof, and it is where a question about soil health becomes something that can actually be computed.

Before any of that, we fix the flaw we already know about, because a study over a wrong model measures the wrong thing.

## Individual Contributions, the two that are missing

Shannon's is already on the page and is correct.

**Abba Ndomo.** Problem research and sourcing, the simulation rules and their expected values, the data provenance and the honesty gates, the integration and review of every pull request, and the pitch.

**Ameya Tanikella.** The weather and data engineering, the simulation pipeline, the CAD rendering in the browser and the operating console the grower uses.

Abba and Ameya both check and reword their own line before it is pasted, because nobody else describes another person's contribution.

## Which sponsor challenges to enter

| Challenge | Enter? | Why |
|---|---|---|
| **Cognition: best use of Devin** | Yes | The brief is written, at `sponsors/cognition.md`. Seven pull requests, three merged, and the four that did not merge are the stronger story |
| **Voloridge: signal in the noise** | Yes | The brief is written, at `sponsors/voloridge.md`. A false signal we made and then caught |
| **Long Lake: convince a non-believer** | Yes, and it may be the best fit of the three | The whole project is built to survive a sceptic. It concedes what is not ours before being asked, it names its own worst flaw, and it refuses every claim it cannot support. A brief is worth writing if there is time |
| Hackster: create what's next | Only if a judge asks | Nothing in the project is built for Hackster, and the entry would be generic |
| Arduino: touch grass | No | It asks for something that understands the real world through hardware. Nothing physical was built, and we say so everywhere |
| OpenAI: the fifth teammate | No | Our project's own claim is that no AI and no learned model is in the loop. Entering a challenge about an AI teammate would sit badly beside that, unless the challenge means the coding assistant, which is Cognition's territory here |
| SpaceXAI: make it legendary | No | No xAI product was used |
| **Ramp: save time, save money** | No, and this one is a trap | Our test suite fails the build if the page claims a saving in cost or energy, and our research dropped exactly those claims because the sources contradicted them. Entering a challenge about saving money would push the team toward the one thing it has spent two days refusing to say |

## Two more things the Plume page needs

- **A thumbnail.** Use `assets/hero-storm-three-answers.jpg` from the repository: the live page at 15:00 on the simulated day, with the hydrangea's roof open in the rain and the other two shut. It shows the claim rather than describing it.
- **The demo link**, in the Links section: <https://page-five-kappa.vercel.app>

## "How we built it", rewritten to carry the architecture

The version on Plume covers the CAD and stops there.
This keeps Shannon's paragraph and adds the systems design, because "how we built it" is where a technical judge looks for the decisions rather than the tools.

### The copy

**The fin, by Shannon.** The Flectofin was modelled in Onshape and rendered in Solidworks. The geometry is deliberately simple: two rectangular laminae on a central backbone that buckles, which is the movement the bird of paradise flower makes. That CAD is tessellated once and committed, so the roof you watch move in the browser is the geometry we drew and not an artist's impression.

**The architecture, by Abba: decide in Python, draw in JavaScript.** This was the first decision and it shaped everything after it. Anything that can be decided ahead of time is decided in the Python simulation, and the browser only interpolates between hours and renders. Which words a zone shows, the hour a fin moves, the value on every gauge: all of it is computed once and written into a single 22 KB file, `day.json`. The page reads that file and nothing else.

We chose that seam for three reasons.

1. **The demo cannot fail on a venue's network.** The page makes no request to anything. A test walks every served file and fails the build if it finds an `http://` outside a comment, so the whole thing runs from a folder with the wifi off.
2. **Every figure has exactly one source.** Because the page cannot compute a headline number, it cannot disagree with the simulation. There is no second implementation to drift.
3. **It is testable in Python**, where we had a test suite, rather than in a browser, where we did not.

**The simulation and its contract, by Abba.** The nine rules, their priority of night, then rain, then light, and the soil model live in one Python module. Its expected values were computed from the real weather files and written into the work package *before* any code existed, so an implementation could not pass by agreeing with its own mistake. Every constant we guessed is labelled ASSUMED in the source and declared with its value in the data documentation, and a test fails the build if the two ever disagree.

**The renderer and the console, by Ameya.** The roof is drawn from the committed CAD mesh, with the fin deformation computed per frame from a single actuation value, so the shape has one description and the opening fraction the overlay reports falls out of it. The console around it is a state machine over one day: it owns the selected zone, the hour, and the playback, and it renders the same way whether the hour came from a run, a keypress, or a click on the roof. Ameya also built the weather pipeline that turns the raw NASA POWER and NOAA gauge files into the processed year the simulation reads.

**Where we broke our own rule, and how we made it safe.** A grower adding a zone in the browser has no precomputed baseline, so the nine rules had to exist in JavaScript too. That is a duplicated implementation, which is exactly the thing that drifts. So a test runs the browser's `rules.js` under Node against every committed zone and asserts the two agree on the roof position, the decision word and the reason, with soil and light inside the rounding. The constants arrive from the simulation in `day.json`, so a number edited in the browser file cannot take effect.

**Determinism as a tested property, not a hope.** The simulation is a pure function of its inputs and its constants. Two runs of the same day produce byte for byte identical output, and a test asserts it. That is what lets us say the roof follows nine written rules with no learned model in the loop and have it mean something.

**Honesty enforced by the build.** Five gate tests police the claims: one asserts the word "measured" appears nowhere except the single line where it is true of the rain gauge; one asserts every assumed constant is declared with its value; one fails the build if the page ever claims a saving in water, cost, energy or yield. One of our own commits exists because a code comment tripped that last gate. Writing the rule down was not enough. The rule had to be executable.

**Graceful degradation, by design.** There is a Python API for stored configuration, but the console works without it. When it is absent the page loads the static day, plays it, shows every decision, and displays an explicit offline state rather than an error. A test asserts that path, and it is why the live deployment is a static page and the demo is unaffected.

**One palette, two consumers.** The colours are declared once as custom properties in CSS, and the 3D renderer reads the same values through its own table, so the modelled roof cannot drift from the page around it.

**The stack, and why it is boring.** Plain HTML, CSS and vanilla JavaScript, no framework and no build step. Python 3.13 with pandas and numpy for the simulation. Same reasoning as the seam: the fewer moving parts between a judge and the demo, the fewer ways it fails at a table.

> Abba and Ameya each check their own paragraph before this is pasted. The attribution above is drawn from the repository and from who owned which work package, and nobody should have their contribution described by someone else.

## One correction to make in the existing copy

"How we built it" says the fin has "two rectangular laminae connected to a central backbone that can bend to create that buckling behavior seen in the Bird of Paradise of flower."
There is a typo: "Bird of Paradise of flower" should read "bird of paradise flower".
The sentence is otherwise good, and it answers the question the stage script left open for Shannon.
