---
name: hackathon-team
description: Organise a hackathon team using the HackMIT playbook - team size trade-offs, the four roles (Builder, Designer, Pitch Lead, Integrator) with the RACI matrix and hour by hour duties, role switching for smaller teams, the stand-up and blocker escalation protocols, decision making rules, conflict scripts, the team health check, the rules that work, and the pre-start checklist. Use this whenever the user mentions roles, who does what, team organisation, assigning work, a teammate who disappeared or keeps changing the idea, a framework argument, stand-ups, or forming a team, and also when a hackathon plan lists tasks with no owners. Built from the Team Building and Team Roles sections of the playbook.
---

# Hackathon team

Hackathons are won by teams that figure out their dynamics before the clock starts.
The best idea in the room loses to a worse idea with better teamwork.
This skill assigns roles, sets the protocols, and hands the team the scripts for the conflicts that will happen.

| Need | Read |
|---|---|
| Team size trade-offs, communication tools, the three conflict scenarios, role switching, remote coordination, the health check, when to remove someone, the rules that work, the checklist, what to look for in teammates | `references/team-building.md` |
| The four role definitions, the RACI matrix, hour by hour duties per role, stand-ups, blocker escalation, code review rules, decision protocol, conflict scripts, the 2 and 3 person adaptations, the role quiz | `references/team-roles.md` |

## Assign roles first

Ambiguity kills velocity, so every person leaves the first conversation able to say their role in one sentence.
The four roles, from the roles reference:

| Role | Owns |
|---|---|
| Builder, the tech lead | The codebase, architecture decisions, unblocking technical problems |
| Designer | The user experience, components, palette, spacing, and the demo flow and slides |
| Pitch Lead | The story, the script, Q&A prep, the demo coordination, the clock |
| Integrator | The glue: frontend to backend, API contracts, deployment, git, the README |

Map people to roles from evidence, what each has actually built or written, not from titles.
The playbook's quiz is a tiebreak: excited by architecture is Builder, notices 12px versus 16px is Designer, has won or bombed a speech contest is Pitch Lead, sets up CI for fun is Integrator, notices all of it is the team lead and takes Integrator plus lead.

Fewer than four people: use the role switching tables in the roles reference.
Two people is Builder plus Integrator and Designer plus Pitch Lead.
Three people is Builder, Designer, and Integrator plus Pitch Lead, since both of those own communication.
Four people: pair intentionally, two on the core feature and two on infrastructure and polish, with the integrator merging constantly.

Fill in the RACI for the twenty tasks in the reference only when a team is arguing about who signs off.
For most teams the one owner per area rule is enough.

## Protocols

- **Stand-ups every two to three hours, ten minutes.** Each person answers three questions in thirty seconds: what did I just finish, what am I on next, am I blocked.
- **Blocker escalation.** Fifteen minutes alone, then the Integrator, then the Builder if it is architecture, then a five minute huddle where someone owns the fix.
- **Decisions.** Technical to the Builder, design to the Designer, presentation and anything touching the timeline to the Pitch Lead, ties settled fast.
  Write every decision down; if it is not in writing, it did not happen.
- **Code review.** Nothing to main without a look, the reviewer finds bugs rather than rewriting, a review over five minutes is too big, hotfixes go straight to main with a comment.
- **Away rule.** Away from the keyboard for more than thirty minutes, post a line in the channel. Assume technical difficulty before malice when someone goes quiet.
- **Tools.** Discord if remote, WhatsApp if in person, whatever the team already uses either way. Do not spend the first hour on tooling.

## The rules that work

One owner per area.
Short check-ins only.
Decisions are visible.
The MVP is sacred.
Integrate early and often.
Rehearse the demo at least twice.
Protect people's sleep.
No negative energy left unaddressed.

## Conflict scripts

Use the playbook's lines verbatim; they are short on purpose.

- Framework argument: "We're not shipping a framework. We're shipping a product. Use what you know fastest." The person writing the code picks; if both are, whoever has a working prototype first.
- Someone disappeared: "Hey, just checking in, are you stuck on anything? We can help." Assign a buddy to text them.
- The idea keeps changing: "I love the ambition. Let's get the core thing working first, then we'll have time for extras." Then write the MVP on a whiteboard and cut anything not on it.
- Architecture disagreement: write both options with pros and cons, five minutes, Builder decides, no grudges.
- Designer versus Builder on UI: ship the Builder's version now, polish later. Function before form at hour 8, form before function at hour 18.
- Morale at hour 16: "We're tired, but we're 60 percent done. Fifteen minutes, food, fresh eyes."

## The health check

Around hour 8 to 12, ask four questions honestly: energy, is anyone going through the motions; scope, are we still building what we agreed; integration, does everyone's code actually work together; communication, has anyone been silent for over an hour.
Fix what it finds in fifteen minutes, reassign, cut, or talk it through, because those fifteen minutes save hours later.

## Before the clock starts

Every box, from the team checklist:

- [ ] Everyone knows the problem
- [ ] Everyone knows the MVP
- [ ] Everyone knows their primary role
- [ ] Everyone knows the backup plan
- [ ] Everyone knows the demo order and timing
- [ ] Everyone has access to the repo, deploy environment, and shared docs
- [ ] Everyone knows the communication tool and norms
- [ ] Everyone has agreed on the stack
- [ ] Everyone knows the deadline and what the final hour looks like
- [ ] Everyone has eaten, hydrated, and knows when they are sleeping

## Choosing teammates

Skills matter less than chaos reduction.
Look for people who respond quickly, explain simply, do not overthink, stay calm when things break, accept imperfection, and take ownership unasked.
Avoid people who need consensus for everything, over-engineer, go silent under stress, blame others, or care more about the tech than the user.
