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

Our hardest problems were not the simulation. They were the data and the agent.

First, we made a false signal and nearly shipped it. An early build joined a typical meteorological year of sun to one real year of rain, which is a standard move. It produced rainy afternoons that were brighter than dry ones, a ratio of 1.11, which cannot happen outdoors. Taking the sun from the same place and the same year as the rain gives 0.627. That number is now an acceptance check in our build, so it cannot drift back.

Second, our build agent read our planning folder and built the wrong product from it. We had set an earlier idea aside but left its files in the repository, and Devin found them and built that instead, nine packages of it. We rewrote every planning file that night, because to an agent a stale document is not neutral, it is an instruction.

Third, a later agent pull request replaced our page instead of adding to it. It dropped the scripts that draw the roof and run the console, and it introduced a second rain model beside our shared rules. We did not merge it. After that we stopped describing features to the agent and started naming the exact files a task was allowed to touch.

Fourth, we know our model's worst flaw and we did not have time to fix it safely. Crop water use is multiplied by how far the roof is open, so under a shut roof it is zero. A shaded plant transpires less and never nothing. Fixing it changes every soil figure and every expected value we test against, so it is the first job after the event rather than a change made in the last hours.

### Accomplishments that we're proud of

The roof is dumb on purpose, and we can prove it. Nine written rules, in the priority night, then rain, then light. No AI and no learned model is in the loop, the fins never follow the sun's position, and two runs of the same day produce byte for byte identical output, which a test asserts.

Every number on the screen says where it came from. Our tests enforce it: one gate asserts that the word "measured" appears nowhere on the page except the single line where it is true of the rain gauge, and another asserts that every constant we assumed is declared with its value in our data documentation. A third fails the build if the page ever claims a saving in water, cost, energy or yield. One of our own commits exists because a code comment tripped that gate.

The whole demonstration runs offline, from local files, with no network call. That is deliberate, because the thing most likely to break at a crowded venue is the network.

And we say what is not ours, first and unprompted. The fin is ITKE's Flectofin, from the University of Stuttgart with Freiburg, patented as EP2320015. The control logic is standard practice in greenhouse computers. What is ours is the size of the decision: a bed, and not a building.

### What we learned

Every failure we had with our build agent was a failure of context, not of capability. It built the wrong product because our planning folder still contained the old one. It replaced our page because we described a feature instead of naming the files it could touch. It solved a problem that had stopped existing because it held the world as it was when its session started. None of those were the agent being incapable, and all of them were fixable by changing what it could see.

We also learned to check data against a relationship whose sign we already know. Our false solar signal passed every sanity check we had, because annual means looked correct. It only appeared when we asked whether rainy hours were darker than dry ones, which is a question with a known physical answer. That is the first check we would run on any new dataset now.

And we learned that conceding a limit early buys more credibility than defending it later. Our project simulates something nobody has built, so we say so in the first twenty seconds, and every figure carries its label.

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

## One correction to make in the existing copy

"How we built it" says the fin has "two rectangular laminae connected to a central backbone that can bend to create that buckling behavior seen in the Bird of Paradise of flower."
There is a typo: "Bird of Paradise of flower" should read "bird of paradise flower".
The sentence is otherwise good, and it answers the question the stage script left open for Shannon.
