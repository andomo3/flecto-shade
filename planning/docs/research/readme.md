---
title: What the seven recon scoring criteria mean and how to apply them
type: research
status: done   # open | in-progress | done | dropped
owner: abba   # one word handle of the teammate doing the research
updated: 2026-09-05
---

# What the seven recon scoring criteria mean and how to apply them

## Answer

Every idea in [the scoring file](hackathon-recon-scoring.md) is scored on the same seven criteria, each from 1 to 5.
Under the current v2 weighting Demoable and Buildable count twice, Freshness and Prior art are converted to points that peak at raw 4 and raw 3, and the maximum is 45.
The earlier v1 weighting, maximum 40, is described below for the record.
The criteria come from the `hackathon-recon` skill under `.claude/skills/`, and they exist because expo judges spend two or three minutes per table, are often less technical than the builders, and skip anything they do not grasp at once.
The score is a check the team reads before the meeting.
It does not choose the idea.

## Where the criteria come from

The recon skill's Step 4 defines the seven criteria and says to weight them to match the event's published rubric.
HackMIT 2026 has not published one.
The 2025 day-of site listed creativity, technical difficulty, design, and usefulness, unweighted, with expo judging in a science fair format.
When there is no weighted rubric and judging is head to head, the skill says to double Demoable, because the watched moment is the unit of comparison.

The seven criteria map onto those four 2025 criteria roughly like this.

| HackMIT 2025 criterion | Recon criteria that cover it |
|---|---|
| Creativity | Freshness, Prior art |
| Technical difficulty | Buildable as the ceiling, Prize surface through Most Technically Impressive |
| Design | Demoable |
| Usefulness | Number, Track fit |

If a weighted rubric appears in the week of the event, re-weight to match it and re-score.

## The seven criteria

Each section gives the question, what a 1 and a 5 look like, how to find the evidence, how it has been applied so far, and the mistake to avoid.
The example scores are from the scoring file as of 2026-09-05.

### 1. Demoable, counted twice

**The question.** Can a judge see it work in 90 seconds?

**What a 1 looks like.** A slide deck, a dashboard of numbers, or anything that needs a lecture before the judge knows what they saw.

**What a 3 looks like.** It works, but the moment is small, or the judge needs a sentence of setup first.

**What a 5 looks like.** Physical, visible, understood without words, repeatable every time, and with more than one possible outcome so the judge is watching to find out.

**How to score it.** Write the demo path for the hour 24 artifact, not for the vision.
Count the seconds, and count the words you must say before the judge understands.
Ask whether the demo answers a question or confirms something obvious.

**How it has been applied.** The impact insert scored 5 because a mass drops and two traces appear side by side, and nobody needs the word auxetic explained to see one is smaller.
The canopy scored 4 because the leaves visibly curl shut in five seconds, but a closed roof letting in less light is the outcome the judge expected.
The gecko foot scored 3 because the physics needs a sentence before the moment lands.
The tensegrity scored 3 because the feasible build is one prism moving between two poses, a small moment.

**Why it counts twice.** Expo judging is head to head across a room of tables.
The team whose thing visibly worked beats the team whose thing was cleverer.

**The mistake.** Scoring the idea you can picture at full scale instead of the one on the table at hour 24.

### 2. Number

**The question.** Does it produce a figure you can say out loud?

**What a 1 looks like.** No measurement at all.

**What a 2 looks like.** A measurement that means nothing to a non-engineer, such as centimetres of twist.

**What a 3 looks like.** A number you can say, but it is unsurprising or needs context, such as a transmitted-light ratio or a pull-off angle envelope.

**What a 5 looks like.** A comparison against a control that the judge remembers, such as percent reduction in peak g against foam.

**How to score it.** Try to say the result in one sentence that contains the word "than".
If there is no control, you have a reading, not a result.

**How it has been applied.** The insert and the evolved structures both scored 5 because each produces a percent better than a control.
The canopy scored 3 because "the shade state transmits X percent of the control reading" is sayable but nobody doubted it.
The tensegrity scored 2 because a height change in centimetres carries no meaning at a table.

**The mistake.** Treating a sensor reading as a number.
A number is a comparison.

### 3. Track fit

**The question.** Does it map cleanly to a track's stated criteria?

**The 2026 tracks.** Entertainment, Education, Sustainability, Healthcare.
A project submits to at most one, and submitting to a track is optional.

**What a 1 looks like.** No 2026 track fits.

**What a 3 looks like.** A track fits if you tell a story, and the story goes beyond what the prototype measures.

**What a 5 looks like.** The judge names the track for you before you do.

**How to score it.** Use the team's own track relevance research where it exists, such as the sustainability files for the tensegrity, the canopy, and the impact liner.
Score the fit of what the prototype demonstrates, not of the application diagram behind it.

**How it has been applied.** The insert scored 4 for Healthcare as injury prevention.
The canopy scored 4 for Sustainability as heat adaptation at transit stops, the clearest track story in the repo, held back from 5 because the prototype measures light rather than heat.
The gecko foot scored 1 because no 2026 track fits it.

**The mistake.** Stretching a story past the evidence.
Both the tensegrity and the impact liner sustainability files warn against exactly this, and judges notice it.

### 4. Prize surface

**The question.** How many prizes could this plausibly touch?

**The 2026 structure.** Three general prizes, one beginner prize, four track prizes, team challenge prizes such as Most Creative and Most Technically Impressive, and sponsor prizes that are not yet published.

**What a 1 looks like.** One long shot.

**What a 3 looks like.** A track prize plus one challenge or sponsor prize.

**What a 5 looks like.** A track prize, a challenge prize, and two or more sponsor prizes on the same build.

**How to score it.** List the prizes by name and say what each one would require.
Past winners stack: the 2024 Sustainability winner also took three sponsor prizes.

**How it has been applied.** The evolved structures scored 4 because the loop touches sponsor compute and model APIs, Most Technically Impressive, and Sustainability.
The canopy scored 3 for Sustainability, Most Creative on the look, and SendCutSend if the leaves are flat cut.
The gecko foot and tensegrity scored 2 for Most Technically Impressive at best.

**The mistake.** Counting sponsor prizes that have not been announced as if they were certain.

### 5. Freshness

**The question.** How far is it from the avoid list?

**The avoid list.** The scoring file names six shapes half the room will build: a language model over a corpus, an AI tutor that corrects an upload, scan a photo and generate a form, webcam gesture input, a wearable that narrates the world, and the team's own anti-pattern of an AI app with a sensor bolted on.

**What a 1 looks like.** It is on the list.

**What a 3 looks like.** Not on the list, but a shape judges have seen many times, such as a light sensor moving a servo.

**What a 5 looks like.** Nothing like it has been built at a hackathon.

**How to score it.** Ask what the judge will have seen at the previous ten tables.
Freshness is about this room this weekend.
Prior art, below, is about what exists anywhere.

**How it has been applied.** The insert and the gecko foot scored 4 because no hackathon project like either was found.
The canopy and the evolved structures scored 3, the canopy because a sensor driving a servo is the canonical first Arduino project, the evolved structures because AI generated anything is the default shape at an AI hackathon.

**The mistake.** Confusing Freshness with Prior art and penalising the same thing twice.

### 6. Buildable

**The question.** Is it real in the hours available, at the team's actual skill level?

**The team's constraints.** Three CAD and hardware engineers and one software engineer, 24 hours, hardware from the HackMIT list, and printer access unconfirmed.

**What a 1 looks like.** A research project.

**What a 2 looks like.** Blocked on materials or on a step the team has never done.

**What a 3 looks like.** Plausible, with one unproven step on the critical path.

**What a 4 looks like.** A plan that reaches a measured MVP with margin and has a fallback for its riskiest part.

**What a 5 looks like.** Could be built tonight with parts already in hand.

**How to score it.** Read the feasible build plan and find the gate that has never been passed.
Score for a first attempt by this team, not for a team that has built one before.

**How it has been applied.** The canopy scored 4, the highest, because one servo, two sensors, and a threshold rule reach a measured MVP by hour seven in the plan, with a foam board fallback.
The tensegrity scored 2 because the team's own research calls the base robot blocked without stiff struts and low creep cord.
The insert scored 3 on its original TPU lattice plan, and Shannon's inventory-only foam board plan would raise that on a re-score.

**The mistake.** Scoring the effort rather than the risk.
A long plan with no unproven step is more buildable than a short plan with one.

### 7. Prior art, inverted

**The question.** Does it already exist on Devpost or GitHub?

**Inverted scale.** A 5 means nothing similar exists.
A 1 means the exact thing exists.

**What a 1 looks like.** The MVP exists as a named project.

**What a 2 looks like.** The principle exists in the literature and as tools.

**What a 3 looks like.** Academic work on the principle, but no built hobby or hackathon version.

**What a 5 looks like.** The search found nothing.

**How to score it.** It is a search, not a guess.
Search Devpost, GitHub, and the open web for the mechanism, the application, and the combination, and name what you found in the scoring file.

**How it has been applied.** The canopy scored 1 because the Light-Based Canopy System on GitHub is an Arduino, a light sensor, a servo, and a cardboard canopy that closes when it is bright, which is the MVP exactly.
The evolved structures scored 2 because topology optimisation and language model to CAD loops exist in the literature.
The other three scored 3 on academic prior art with no built version found.

**What a low score means.** Prior art is not fatal.
It means the novelty claim has to be the measured comparison, not the mechanism.

**The mistake.** Skipping the search.
The first four ideas were scored on a lighter search than the canopy, and the canopy search is what moved its score most.

## Weighting and total

Two weightings have been used.
The scoring file states which one each table uses.

### v1, used 2026-09-05 for the first five ideas

The total is twice the Demoable score plus the other six scores, so the maximum is 40.

### v2, the team's weighting from 2026-09-05 onward

The team set three changes after narrowing to the impact insert, the bus stop canopy, and the termite structure.

1. **Buildable counts double**, alongside Demoable.
   The team's view is that the two things that decide a hackathon are whether it works and whether it can be finished.
2. **Prior art peaks at raw 3, not 5.**
   A raw 5, nothing similar exists, means no reference design to copy and a higher chance of failing to build it.
   A raw 1, the exact thing exists, means the judge has seen it.
3. **Freshness peaks at raw 4.**
   A raw 5 carries the same "nobody has done this because it is hard" risk.

Raw scores stay what they were, 1 to 5 as assessed.
Points are awarded from the raw score by these maps.

| Raw Freshness | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Points | 1 | 2 | 3 | 5 | 4 |

| Raw Prior art, 5 means nothing exists | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Points | 1 | 3 | 5 | 3 | 1 |

Total under v2 is twice Demoable, plus Number, Track fit, Prize surface, Freshness points, twice Buildable, plus Prior art points.
The maximum is 45.

**A caveat worth reading before trusting a v2 total.**
Doubling Buildable already penalises ideas that are hard to build because nobody has built them.
Bending Prior art and Freshness toward the middle counts that same risk a second time.
The side effect is visible in the scoring file: the gecko foot gains points under v2 for having only academic prior art, even though its demo and track fit did not change.
Read the raw table alongside the points table, and when two ideas are close, decide on the raw rows.

A tie is possible and real: under v1 the evolved structures and the canopy both scored 26 for different reasons.
Compare the rows, not just the totals.

## How to score a new idea

1. Write the one sentence pitch.
   If you cannot, the idea is not ready to score.
2. Write the demo path for the hour 24 artifact, not the vision.
3. Search Devpost, GitHub, and the web for prior art, and name what you find.
4. Score each criterion raw, and for each one write a line saying why it is not one point higher.
5. Convert Freshness and Prior art to points with the v2 maps, double Demoable and Buildable, and total out of 45.
6. Add the column to both tables in [the scoring file](hackathon-recon-scoring.md), add a rationale section, and update the answer paragraph.
7. Run `/sync-state` and commit the regenerated index with the change.

## What the score does not do

- It does not pick the idea.
  The team decides in the meeting and the meeting note records why.
- It does not weigh enthusiasm, learning goals, or which idea the team would enjoy building.
- It does not predict a specific judge.
  It predicts what an expo room rewards on average.

## Sources

- `.claude/skills/hackathon-recon/SKILL.md`, Step 4, the criteria table and the weighting rule.
- [The scoring file](hackathon-recon-scoring.md), event facts, the winners corpus, the avoid list, and every example score above.
- [HackMIT 2026 site](https://hackmit.org/), tracks and prize structure, read 2026-09-05.
