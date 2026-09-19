# pitch - local memory

> **SUPERSEDED on 2026-09-19 at about 16:45. This file is the record of the bus stop canopy, and nothing is built from it.**
> The current plan is the simulated louvre roof over three crops.
> Read `AGENTS.md` and `CHECKLIST.md` at the repo root, then `planning/plans/plan-d-louvre-roof.md`.
> If you are a build agent and you arrived here, stop, and go back to those files.

Owner: the pitch role, not assigned yet.
With three people it most likely falls to abba, alongside the submission.
Writing the pitch before the event is planning and is allowed.
Use the `hackathon-pitch`, `hackathon-readme`, and `hackathon-testing` skills, which are built from the playbook.

## Where the pitch lives

`story.md` is written first and every script is a cut of it.
`script.md` holds the 30 second, 60 second, and 3 minute versions, each inside the playbook's word target, checked with the skill's `pitch_timer.py`.
`storyboard.md` is the demo beat by beat, and its screen column is the source for `../software/ui-brief.md`.
The hero is an illustrative rider, the villain is the roof that does not move, and the closing line is "We cannot move the sun. So we built the roof that moves instead."
Every study figure is read once more at its source before it is said out loud.
`questions.md` is the Q&A bank, `video.md` is the two video plan with its clock and shot list, `placards.md` is the four cards, `checklist.md` is rehearsal and the table routine, and `submission.md` is the form draft with the citations and the prior work statement.
The safety take of the video is filmed Saturday between 23:00 and 00:45, and cut while the venue is closed.

## The story, locked on 2026-09-18

- One sentence: a tabletop bus stop roof made of hingeless leaves that buckle open on their own when the sun comes out, so the bench underneath stays shaded.
- The user is a person on a bench in the Houston sun, introduced as an illustrative rider, and the opening line is "Picture Rosa. It is three in the afternoon in July, in Houston, and her bus is twelve minutes away."
- The watched moment: the judge presses play, one real Houston day runs in about a minute, the sun climbs, and three leaves buckle together from one servo with no hinge.
- The number, said out loud: "X percent of the light reaches the bench with the leaves flared, against Y percent resting."
  If the backup fixed roof is built, the same number is also said adaptive against fixed.
- The proof it is not a script: cover the light sensor with a hand and the leaves respond.

## Changes on 2026-09-19, at the event

- The lens is impact on human life, from the keynote and a challenge, and `story.md` has the rules for it: Rosa stays the one hero, and the farmworker on a rest break and the grower appear once, in the vision beat and on card 3.
- The study's own cause for the hot shelter is trapped heat in closed acrylic and metal walls, not the moving sun.
  Every script and the storyboard now say the trapped heat first and the moving sun second, as our argument and not the study's.
- The rain answer is in `questions.md` under question 5: sensing is solved, water shedding is untested, a clear sheet under the leaves is the fallback, and the farmworker's summer is nearly rainless.
- Ten more questions judges can pry on are in `questions.md`, the sharpest being "why not leave it bent all summer".
- California's Title 8 section 3395 requires shade above 80 F, enough to "sit in a normal posture fully in the shade", read at the source on 2026-09-19.
- Still to verify at a source before it is said: the Central Valley's nearly rainless summer, and any number about Houston METRO's ventilated shelters.
- The data finding for the Voloridge challenge, if it ships, comes from `../docs/research/adaptive-bus-stop-canopy/voloridge-datasets.md` and is said as modelled.

## Plan B, chosen 2026-09-19

The team can demo the flapping leaf and nothing else, so the stop is simulated and the simulation drives the real leaf.
`script-plan-b.md` is the script that is rehearsed, all three lengths inside their word targets, and `script.md` is kept as the record of the live version.
Nothing is called measured, the closing line says "designed" where it said "built", and "nothing tells the leaves what to do" is gone because the simulation now does.
The number is two numbers: [X] against [Y] for the harsh hours, which a fixed roof could match, and [W], the winter sun the open leaves give back, which it cannot.
Still to rewrite for Plan B, from the list in `../plans/plan-b-simulated.md`: the storyboard's table and screen columns, cards 1 and 2, the video plan, and the submission's first paragraph.

## Honesty rules

- Only what was measured on the table today is claimed as measured.
- Shade hours per year and anything from the dataset are said as modelled.
- Temperature is secondary and is mentioned only if it reads.
- If replay mode is in use, the pitch says so: "the app is driving the leaves from the data right now."
- Open source libraries and the dataset are cited in the submission, because the rules require it.

## Questions judges will ask, to answer in `questions.md`

- How does it know where the sun is?
  It does not, it reacts to the light it sees, and that is the point.
- Is the app just playing a script?
  The data moves the sun, the sensor moves the leaves, cover the sensor and watch.
- Why not a bigger fixed roof?
- Why no hinges, and what is the leaf made of?
- What did you measure and what did you model?
- What did you build in the 24 hours?
  Everything in the submitted repo, and the planning repo is linked and public.
- What would a full size one cost, and what about wind and rain?
  Not tested, and the placard says so.
- Why Houston, and does it work elsewhere?
  The city picker, if it ships.

## Files to write, and when

| File | When |
|---|---|
| `name.md`, the project name and the one sentence | the name is not decided yet |
| `script.md`, the ninety second script | a draft before Saturday is allowed, the number stays X and Y until the measurement run |
| `questions.md` | before Saturday |
| `placards.md`: "Measured today", "Not yet claimed", "Same leaf, other roofs" | Saturday |
| `video.md`, where the backup video lives | recorded after the first clean run, Sunday 08:00 at the latest |
| `submission.md`, every field of the form | drafted Saturday, checked at the freeze |

## Pivots that change the words

- No servo mounted sun: "the sun gets brighter and dimmer through the day" replaces "the sun moves".
- Replay mode: say it.
- The bench sensor shows no difference: the number becomes "N of N light triggered cycles".
- The rig breaks: the backup video, then the fixture replay on the laptop.
