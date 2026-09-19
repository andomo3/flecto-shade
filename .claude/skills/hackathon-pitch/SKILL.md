---
name: hackathon-pitch
description: Write and rehearse a hackathon pitch and demo from the HackMIT playbook - the story (the character, the villain, the story spine, the emotional arc, the closing story), the 30 second, 60 second, and 3 minute scripts, the demo storyboard, the judge Q&A bank, the recovery lines for when the demo breaks, and the pre-demo and during-demo checklists. Use this whenever the user mentions a pitch, a demo script, judges, judging, a presentation, slides, storytelling, a narrative, a hook, "what do we say at the table", the closing line, Q&A prep, or rehearsal, and also when they ask how to frame or position a hackathon project, even if they never say the word pitch. Built from the Presentation Winning, Winning Secrets, Win Checklist, and Storytelling sections of the playbook.
---

# Hackathon pitch

A good hackathon pitch is not an essay.
It is a compressed story that helps the judge understand value quickly, and the judge decides in the first thirty seconds whether to keep listening.
This skill turns a project into that story, then drills it until it fits the clock.

The four references are the playbook sections this skill is built from.
Read the one the task needs rather than all four.

| Need | Read |
|---|---|
| The pitch structure, the 3 minute table, the demo scripting rules, the 15 judge questions, delivery | `references/presentation-winning.md` |
| Storytelling, anchoring and priming, the three act structure, what judges notice fast, the 1 percent details | `references/win-secrets.md` |
| The STAR framework, the Pixar story spine, hook story offer, the emotional arc, the five demo moment rules, the character and the villain, the rule of three specifics, the three closes, the three fill in templates, the nine storytelling mistakes | `references/storytelling.md` |
| The pre-demo, during-demo, and post-demo checklists, recovery moves, eye contact, the 30 point self assessment | `references/win-checklist.md` |

## What to produce

Write into `pitch/` in the project repo, or wherever the user keeps pitch material.
Use `assets/pitch-script-template.md` as the skeleton.

0. **The story.** Written first, in `pitch/story.md`, because every script is a cut of it: the character, the villain, the story spine, the emotional arc, three specifics, and the closing story.
   See "Story first" below.
1. **The one sentence.** User, problem, solution, in one line.
   If it cannot be said in one sentence, the scope is too large, and that is worth saying to the user.
2. **Three scripts.** 30 seconds, 60 seconds, and the 3 minute structure, because judging formats change on the day and the team should never be caught with only one length.
3. **The demo storyboard.** Golden path only: one user, one task, under 90 seconds, narrated click by click, with the "wow moment" marked.
4. **The Q&A bank.** The 15 questions judges actually ask, from the presentation reference, each answered in the formula: direct answer, evidence, scope honesty.
5. **The recovery lines.** Rehearsed sentences for the demo crashing, the wifi dying, a forgotten line, and a question nobody can answer.
6. **The checklists.** Pre-demo one hour before, during-demo by timestamp, post-demo, copied from the win checklist and trimmed to what applies.

## Story first

The storytelling reference is the playbook's Section 29, and its claim is that judges vote with their gut and justify with their head, so the story is written before any script.

- **The user is the hero and the problem is the villain.** Never the team, never the technology.
  Give the character a name, a place, and one specific struggle, and make the villain specific enough to picture.
- **Run the story spine once.** Once upon a time, every day, until one day, because of that, because of that, until finally, and ever since then.
  The project is the "until finally".
- **Shape the arc.** Setup, tension, rising action, climax, resolution, call to action.
  Without the low, the high does not land, so the problem gets real time before the product appears.
- **Three specifics per sixty seconds.** Numbers, names, places.
- **The demo is a scene, not a tour.** Narrate the character through it, show the transformation and not the setup, end on an emotional beat, keep it under sixty seconds, and never run it without a backup.
- **Close on the story.** The callback close returns to the character, the vision close paints the future, the emotional close lands one moment.
  No new information, no feature list, no "in conclusion".
- **End with the offer.** Say what the team wants from this judge.

The playbook's examples invent pilots, quotes, and users who cried in libraries.
A hackathon team has none of those, and the honesty rules below outrank the templates.
So a character is introduced as illustrative, "picture someone" or "imagine", unless a cited source describes that person, the "result" beat is what was measured at the table today, and the "ever since then" beat is said as a vision, never as history.

## How to write the script

Follow the order the playbook gives, because judges follow it too: problem, user, current pain, solution, live demo, why it matters, what is next.

- **Open with a question, a fact, or a story.** Never with "Hi, we're team X".
  The first fact anchors everything after it, so lead with the strongest number or result.
- **Name the user before the solution.** Judges score problem relevance separately from execution, and a named user with an unglamorous problem is what past winners share.
- **Show before you tell.** The demo starts by the 60 second mark in the 3 minute version.
  Pre-fill everything, no live typing, no sign up on stage.
- **One concrete metric in the impact section.** Connect it to a person, not a benchmark.
- **End on the link and stop.** Say the URL, show the QR, do not trail off, do not end on "questions?".
- **Rule of three.** Three problems solved, three features, three next steps.
  Five is forgettable, one is thin.
- **Prime the judge.** If the project is fast, say speed early. If it is measured, say measured early.
  Judges evaluate through whatever lens the opening sets.

Then cut twenty percent.
The playbook's word targets are the check: 30 seconds is 75 to 90 words, 60 seconds is 150 to 180, 2 minutes is 300 to 360, 3 minutes is 450 to 540.
Run `python scripts/pitch_timer.py pitch/script.md` to measure each section, and keep every length inside its range, the 60 second one included.
Cutting below the range to leave room for a demo pause is a trap: the judge hears a thin pitch, not a considerate one.

Three rules of honesty, because the first test runs of this skill broke all three and a judge would have caught each one:

- **Invent nothing about users or evidence.** No quote, reason, statistic, or study attribution goes in the script unless the brief supplied it.
  Where the script needs one, write a bracketed placeholder for the team to fill or verify, and say so at the top of the file.
- **A measured proxy stays a proxy.** If the team measured light, the script says light, and never turns it into a temperature, energy, or health outcome.
  Say out loud what was not measured; the playbook's judges reward directness about scope more than they punish a missing claim.
- **Name the user in the first two sentences.** "You" is not a user.
  A judge scores who has the problem, so the person, the beekeeper, the rider on the bench, the student, is named before the product is.

## Booth or stage

Ask which one, because the advice diverges.

- **Booth, science fair style.** Judges come to the table for three to five minutes.
  Open with the product, not slides.
  Let them touch it within thirty seconds.
  Keep a one pager with the link and QR on the table.
- **Stage, timed pitch.** Slides and a strict clock.
  Memorise the first and last twenty seconds, since those decide recall.
  End ten seconds early, because running over reads as unfinished.

One speaker drives.
Others handle clicks and Q&A in their own area.
Switching speakers mid demo wastes time.

## Rehearsal

The pitch is not done until it has been run out loud with a timer at least three times, and once with the wifi off using only the backup recording and screenshots.
Record one run on a phone and cut filler until it is ten seconds under.

After the last run, score it with the 30 point self assessment in the win checklist reference.
Under 21 means practise more, under 16 means prioritise demo reliability over polish.

## Slides, if there are any

One idea per slide, large text, real screenshots, the result before the implementation.
The slide sequence from the playbook: title, problem, solution, demo, impact, future, and that is the whole deck.
Six slides, not eight; a backup screenshot slide lives at the end and is never shown unless the demo dies.

## What hurts scores

From the win secrets reference, the things that lose points fastest: overengineering a simple problem, vague framing such as "AI for everything", a script that does not match the product, a pitch longer than the demo, no backup when the demo fails, and unfinished features that distract from the core.
When the draft has one of these, say so and fix it before polishing anything else.
