---
name: hackathon-testing
description: Test a hackathon project the way the HackMIT playbook prescribes - the 80/20 of what to test and what to skip, the 10 minute manual checklist, realistic demo data, "it works on my machine" prevention, bug triage from P0 to P3, the demo day test at 30, 15, and 5 minutes before, and the demo day backup plan with a live URL, a backup deploy, a recording, and a kill switch. Use this whenever the user mentions testing, QA, a bug, the demo breaking or crashing, "works on my machine", demo data or seed data, environment variables missing in production, what to fix versus work around, or the final checks before submitting, even if they do not say the word test. Built from the Testing at Hackathons and Deployment Mastery sections of the playbook.
---

# Hackathon testing

Testing at a hackathon is not about coverage.
It is about confidence: when the team knows the demo works, they can focus on presenting instead of worrying.
The right kind of testing catches the bugs that would ruin the demo and skips everything else.

| Need | Read |
|---|---|
| What to test and skip, the manual checklist, demo data, environment and dependency prevention, browser and API checks, load basics, the demo day test, bug triage, the smoke test script | `references/testing.md` |
| The demo day backup plan, the pre-submit verification, the environment variable checklist, common deployment failures and the debugging flow | `references/deployment.md` |

## The rule that decides everything

Ask: if this bug showed up during the demo, would it embarrass us?
If yes, test it.
If no, skip it.
That one question replaces every debate about coverage.

Always test: the happy path through the main feature, auth if the project has it, that data survives a refresh, the error states when an API is down or input is bad, and the exact demo flow, end to end, repeatedly.

Usually skip: edge cases under one percent, browsers beyond Chrome, Firefox, and Safari, performance unless visibly slow, deep accessibility, pixel perfect mobile, internationalisation, comprehensive logging.

The pyramid from the playbook, top to bottom: manual testing of the demo flow, one end to end test, integration tests on API endpoints, unit tests only for critical logic.
Most hackathon projects need only the top two.

## The 10 minute manual checklist

Run it after every significant change, not once at the end.
The full list is in the testing reference; the short form:

- Auth: sign up, log in, wrong password fails, log out, protected routes redirect, session survives refresh.
- Core: create, read, update, delete, list, required field validation.
- Data: what was saved is still there after a refresh.
- UI: no console errors, no broken images or links, forms submit, loading states show.
- Edge: empty state, one item, many items, very long input, special characters, double click, back button, refresh mid action.

Then the "break your own app" session, thirty minutes: click everything twice, submit empty forms, go backwards, open two tabs, clear cookies, resize, turn the wifi off, watch the console.
And the buddy test: swap with another team for fifteen minutes and let fresh eyes find what yours cannot.

## Demo data

"Test user 1" and lorem ipsum say the project was built twenty minutes ago.
Write a seed script that is idempotent, uses specific names, varied statuses and recent dates, real relationships between records, and five to ten records per collection.
Enough to show it works with multiple items, not so many that a judge scrolls forever.

## It works on my machine

The most dangerous sentence at a hackathon.
Prevent it before it is said:

- Never hardcode configuration. Every key, URL, and flag is an environment variable, and `.env` is never committed.
- Ship `.env.example` with every variable named and no values.
- Pin versions: a lockfile, a runtime version file, requirements documented in the README.
- Add a startup check that fails loudly when a required variable is missing, because the environment variable ghost is the classic production only failure.
- Docker is the nuclear option when nothing else makes it reproducible.

Then the checklist: variables documented, `.env.example` current, dependencies install on a fresh machine, migrations run, seed loads, the app starts clean.

## Bug triage

Not all bugs are equal, so decide in seconds, not minutes.

| Priority | What | Do |
|---|---|---|
| P0 | Crashes, data loss, security, auth completely broken | Fix now |
| P1 | Main feature broken, obvious visual glitch, broken navigation, wrong data shown | Fix before the demo |
| P2 | Minor UI, edge cases, slow, inconsistent styling | Fix if time permits |
| P3 | Cosmetic, rare, non demo features | Work around or ignore |

The fix or workaround decision: will a judge see it? Five minutes to fix, fix it. Two hours, work around it. Can the demo avoid the code path? Then skip it.
Workarounds that are fine: hardcode a value, pre-populate, disable the broken feature, mock the data, redirect to the working page.
Sometimes shipping with a known, documented, minor bug is the right call, because fixing it risks worse.

## The demo day test

Thirty minutes before: run from a clean state, check every feature, verify persistence, check error handling, test on the demo computer.
Fifteen minutes before: clear the cache, close tabs, check the network, prepare the offline fallback, load the demo data.
Five minutes before: breathe, review the script, confirm the backup, test audio and video, open every tab.

## The backup plan

Judges remember "it worked when I clicked it", so plan for failure from the deployment reference:

1. The primary live URL, the one submitted.
2. A backup deploy of the same code on a second host, ten minutes of work that saves demos.
3. A 60 to 90 second recording of the golden path, made after the final deploy, hosted online, not only on a laptop.
4. Three to five screenshots.
5. A seeded demo account, never live sign up during judging.
6. A kill switch: a `?demo=1` parameter or a "load sample data" button that bypasses flaky third party calls with local fixtures.

The ladder when something dies: primary URL, then backup URL, then the recording and screenshots.
Acknowledge the failure once, move on, stay calm.

## Automated testing lite

A ten minute smoke test script that hits the health endpoint and the one create call pays for itself.
Write it before major changes and before demo day, run it when tired.
The API contract check, "is `users` an array and non empty", catches the mismatch that renders everything as undefined.
Skip automation when behind schedule, when the feature is trivial, or when the test would be harder than the code.
