---
name: hackathon-build
description: Run a hackathon build against the clock using the HackMIT playbook's Build Fast Framework - the 24 hour, 12 hour, and 6 hour phase plans, the hourly checkpoint system with green, yellow, and red, the parallel workflow for 2 to 4 people, the tech debt decisions on what to skip and keep, save points and commit rules, the scope creep emergency brake and reduction ladder, the demo first rule, and the pivot decision tree. Use this whenever hacking has started or a deadline clock is running, when the user mentions hours left, being behind, what to cut, a feature that is not working, scope creep, "should we add X", whether to pivot, or how to split the work between teammates during the event. This is the during-the-event skill; for choosing what to build before an event use hackathon-recon. Built from the Build Fast Framework and Problem Selection Engine sections of the playbook.
---

# Hackathon build

Every hackathon has the same arc: excitement in hour one, confusion in hour two, panic in hour five, and either triumph or regret at the end.
The difference between those outcomes is not talent, it is a system.
This skill is that system.

| Need | Read |
|---|---|
| The 6, 12, and 24 hour plans, the checkpoint table, the parallel workflow tables, tech debt, the boring middle, save points, the scope creep brake and ladder, speed hacks, the fallback system, the demo first rule | `references/build-fast-framework.md` |
| The pivot decision tree, the signs to pivot and not to pivot, the 4 hour rule, the validation checklist and scorecard | `references/problem-selection.md` |

If the project has a brief or a written MVP, read it first and treat the demo path in it as fixed.
The build serves the demo, not the other way round.

## The demo first rule

Build the demo path first, not last.
If the full app is built and the demo does not work, there is nothing to show.
If the demo is built first, there is always something.

1. Build the screen the judge sees first.
2. Build the action the judge sees second.
3. Build the result the judge sees third.
4. Make that three step flow perfect.
5. Add everything else around it.

## The plan for the hours available

Pick the plan that matches the clock and write it down where the team can see it.
The 24 hour shape from the playbook:

| Hours | Phase | Goal |
|---|---|---|
| 0 to 2 | Plan aggressively | Architecture decided, UI sketched, data shape written before code, sleep planned |
| 2 to 6 | Build the skeleton | Every screen exists, even empty; clickable but hollow |
| 6 to 12 | Fill in the core | The main feature works with real data |
| 12 to 18 | Polish and extend | UI refinement, error handling, extras only if the core works, docs |
| 18 to 22 | Test and fix | Full flow testing, bugs, cross browser, security |
| 22 to 24 | Deploy and present | Final deploy, pitch, rehearsal, recording, roles |

Adjust the windows to the venue, since venues close and submissions land before the nominal end.
Whatever the plan says, deploy something by hour three, because a deploy discovered in the last hour is a project lost.

## Checkpoints, every hour

Set an alarm.
When it rings, answer the checkpoint question for that hour and colour it.

| Checkpoint | Green | Yellow | Red |
|---|---|---|---|
| MVP locked and stack decided? | Written down | Mostly decided | Still arguing |
| Scaffold runs? | Shows something | Starts, blank | Will not start |
| Any data on screen? | Mock data renders | Connected, no display | Nothing |
| Core flow end to end? | Main action completes | Partially | Broken |
| Looks like a product? | Clean, mobile friendly | Functional, ugly | Debug screens |
| Deployed and demo ready? | Live URL works | Deployed, buggy | Not deployed |

Yellow is recoverable by focusing on the next milestone.
Red means cut scope immediately: remove the least important feature, simplify, get to green by the next hour.

## Parallel work

The biggest waste is two people waiting on the same person.
The reference has tables for two, three, and four person teams by hour.
The rules that make the split hold:

- Each person works in their own directory.
- One shared definitions file so everyone agrees on data shapes.
- Commit every thirty minutes so nothing is lost.
- Do not merge to main without a quick check, since a broken main blocks everyone.
- One channel for "I'm stuck" moments.

Sync points at the phase boundaries, not continuously.

## Tech debt

Skip, nobody will notice: edge case validation, comprehensive logging, migrations, a CI pipeline, unit tests, accessibility audits beyond the basics, performance work unless visibly slow, code docs, internationalisation, caching.

Keep, it saves the demo: error handling on API calls, loading states, mobile responsiveness, environment variables, basic auth if accounts exist, validation on the critical path, frequent commits, and the core user flow working perfectly.

The litmus test before any shortcut: will it fail the demo, will a judge notice, will it make the code unreadable in two hours? Any yes, do not skip. Otherwise skip.

## Save points

Commit like a video game: every time something works that did not before, before anything risky, every thirty minutes regardless, before switching tasks or people, before deploying.
Prefixes: `feat:`, `fix:`, `style:`, `refactor:`, `docs:`.
Before each commit: the app runs, no secrets exposed, no `node_modules` or `.env` staged.

## Scope creep

The number one hackathon killer arrives as "we should also add", "it would be cool if", "the judges would love", "while we're at it", and "let me just".
When one is heard, pull the brake:

1. Does it replace an existing feature? Cut the old one first.
2. Does it take more than thirty minutes? Defer to nice to have.
3. Does it strengthen the core demo? If not, do not build it.
4. Can the demo run without it? Then skip it.

Behind schedule, cut in this order: nice to haves, secondary flows, real time (replace with refresh), complex AI (replace with a simpler call or a mock), custom charts (replace with tables), custom auth (use a provider).
If the app has more than three pages, it probably has too much.

## The boring middle

Hours three to six are where projects die: the rush fades, the bugs are not fun, and the gap between the imagined and the built feels huge.
Focus on the next thirty minutes, not the finish line.
Pair when stuck, switch tasks after twenty minutes of fighting one bug, eat, walk five minutes, and say the small wins out loud.

## When to pivot

Use the decision tree in the problem selection reference rather than gut feel.
Pivot when the core problem stopped being real, when a technical blocker has no simpler approach, when four hours passed with no clear path, when the demo needs more than two minutes of explanation, or when the team cannot say what it is building.
Do not pivot when the blocker is setup rather than concept, when six or more hours are in with a partial demo working, or when frustration is the only evidence.
The worst outcome is not a bad idea, it is no finished project.

## The rule

A shipped simple project beats an incomplete ambitious project every time.
When asked to add something, say what it costs in hours and what it displaces, then offer the smaller version.
