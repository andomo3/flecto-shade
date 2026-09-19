---
name: hackathon-recon
description: Research a hackathon before it starts and decide what to build. Studies past winning projects in the target tracks, identifies which ideas are saturated, scores candidate ideas against the actual rubric, and writes a one-page project brief that the build skill consumes. Use this whenever the user mentions an upcoming hackathon, asks what to build for one, is choosing between hackathon ideas, is reading a hackathon rubric or sponsor prize list, or says anything like "HackMIT", "what should we build", "is this idea good enough to win". Run it days or weeks before the event, never during - once hacking has started or a deadline clock is running, hackathon-build owns the decisions.
---

# Hackathon Recon

Decide what to build, using evidence instead of enthusiasm.

Judges spend very little time per project, are often less technical than the builders, and will skip anything whose use case they don't grasp immediately. That makes idea selection worth more than execution quality, and it is the only part of a hackathon with no time pressure. Do it early and do it properly.

The output is one file: `project-brief.md`. Everything here exists to produce it.

## When to run

Days or weeks before the event. If the hackathon has started, stop — the answer is now "build what you already have," and the hackathon-build skill owns that decision.

## Timebox

One evening. Recon is the phase most likely to become procrastination with a research budget. Cap the corpus at 20 projects and the candidate list at 3 ideas. If more research feels necessary, it isn't.

---

## Step 1 — Read the rules

Pull from the event site and its submission platform - Devpost, or the event's own portal. Big events often run their own (HackMIT uses Plume, not Devpost), and their sites are often JS-only pages that return nothing to a plain fetcher, so use a real browser. If the user is logged into the event's registration portal, check it: it can hold facts the public site doesn't, like admission status and unpublished deadlines.

Capture:

- Track list and which tracks the user is eligible for
- Judging criteria **and their weights** — these drive every later decision
- Sponsor prizes and what each one requires
- Submission requirements (video length, repo, demo format, deadline)

Judges check submission requirements first, and a surprising number of entries fail on them. Capture them verbatim.

If any of this isn't published yet, note the gap and proceed — last year's version is usually close enough.

## Step 2 — Study the winners

Fetch the project galleries for the last two or three editions of this hackathon. On Devpost, winning projects carry a winner banner and sort to the top of the gallery, so they're easy to isolate.

Build a table of ~20 winners across the user's target tracks:

| Project | Track | One-line pitch | Stack | The demo moment | Why it won |
|---|---|---|---|---|---|

"The demo moment" is the single thing a judge watched happen. Fill it in even if you have to infer it from the video or writeup — it's the most useful column.

Then state in 3–5 bullets what the winners have in common. Look for: a concrete number in the pitch, an unglamorous problem, a visible live result, a narrow scope executed fully.

## Step 3 — Name what's saturated

From the same corpus plus the current year's obvious defaults, list the ideas that half the room will build. Every AI hackathon produces a cluster of near-identical projects; judges remember the angle they haven't seen.

Output an explicit avoid-list of 4–6 idea shapes, each one sentence. Do this **before** generating candidates, so the user doesn't get attached to something already on the list.

## Step 4 — Score three candidates

Generate or collect exactly three candidate ideas. Score each 1–5:

| Criterion | Question |
|---|---|
| Demoable | Can a judge see it work in 90 seconds? |
| Number | Does it produce a figure you can say out loud? |
| Track fit | Does it map cleanly to a track's stated criteria? |
| Prize surface | How many sponsor prizes does it touch? |
| Freshness | How far from the avoid-list? |
| Buildable | Real in the hours available, at the team's actual skill level? |
| Prior art | Does it already exist on Devpost or GitHub? (score inverted) |

Weight the criteria to match the event's published rubric rather than this default ordering. If there is no published rubric - pairwise or expo-style judging is common at large events - weight Demoable double and say so: head-to-head comparison makes the watched moment the deciding unit.

Prior art is a search, not a guess: check Devpost and GitHub for each candidate before scoring it, and name what you found.

Report the scores, name the winner, and say plainly why the other two lost. Do not soften a low score to be encouraging — a bad idea found now is the cheapest possible save.

## Step 5 — Write the brief

Fill in `brief-template.md` and save it as `project-brief.md` in the project repo.

Write the demo path **first**, before any feature list. The features are whatever those 90 seconds require; everything else goes on the cut list. Working in the other direction produces a feature list that no demo can carry.

Hand off to the hackathon-build skill, which treats the brief as read-only once the event starts.

---

## Hard rules

- Three candidates, not ten. More options make the choice worse, not better.
- The brief is one page. If it doesn't fit, the scope is wrong.
- Never recommend a stack the team doesn't already know or hasn't practiced before the event.
- If the user can't explain the idea in one sentence, it isn't ready, regardless of its score.

## After the event

One metric matters: **what share of the brief's planned features shipped as real?** If it's under half, the hour estimates in Step 4 are optimistic — record the multiplier and apply it next time.

Add a lesson to this file only if it would have changed a decision. Delete any rule here that hasn't been used in two consecutive events.
