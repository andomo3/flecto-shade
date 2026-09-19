---
name: hackathon-readme
description: Turn a hackathon repo into the product page judges and recruiters actually read, using the HackMIT playbook - the README section by section, the README template, the 10 second test, the license choice, the issue label set, the branch and commit conventions, and the pre-submission checklist. Use this whenever the user mentions a README, the repo looking good, judges reviewing the code, a project page, a submission link, screenshots or GIFs for the repo, a license, or "how judges review repos", and also when a hackathon project is close to submission and nobody has touched the README yet. Built from the GitHub for Hackathons and README Template sections of the playbook.
---

# Hackathon README

Judges form an opinion of a repo within ten seconds.
An empty README says the team ran out of time, and a README with a live link, a screenshot, and three setup commands says they are professionals.
This skill makes the repo work as hard as the code.

| Need | Read |
|---|---|
| The branch strategy, commit prefixes, the no-go rules, README anatomy with what each section does, licenses, the CI example, issue labels, how judges actually review repos | `references/github-for-hackathons.md` |
| The full README template with every bracket explained, and the checklist before submission | `references/readme-template.md` |
| The template body alone, ready to copy and fill | `assets/README-template.md` |

## The 10 second test

Before writing anything, open the repo the way a judge does: in an incognito window, cold.
Can a stranger tell what the project does, see it working, and read the tech stack within ten seconds?
If not, the README is the work, and the order below is the order judges scan.

## Write the README in this order

Start from `assets/README-template.md` and replace every bracket.
Delete sections that do not apply, but try to keep them all, because judges check for them.

1. **Title and one liner.** What it is and why anyone should care, no jargon.
   A memorable name beats "Team 7's project".
2. **Live demo link and the best screenshot.** At the very top.
   The screenshot is the most impressive screen, not the landing page and not the login.
   If there is a video, link it here too.
3. **Problem.** One or two sentences plus a relatable scenario or a stat.
   Judges score problem relevance separately from execution, so this section is not optional.
4. **What we built.** Scannable bullets, each one a feature visible in the demo.
   Judges review twenty to forty projects and do not read paragraphs.
5. **Tech stack.** Breadth without a wall.
   Name any sponsor API here, sponsors notice.
6. **Architecture diagram.** Hand drawn and photographed is fine.
   It needs to exist more than it needs to be pretty.
7. **Setup.** Clone, install, run, three commands at most.
   If it takes more, the setup is overcomplicated and that is worth flagging.
8. **Screenshots and GIFs.** A GIF of the core interaction is worth more than any description.
9. **What's next.** Three checkboxes.
   This is the product thinking signal.
10. **Team and contributions.** Who did what, with handles.
    Recruiters check individual contributions.
11. **License.** MIT is the hackathon default.
    No license means all rights reserved, which looks amateur.

Then run `python scripts/check_readme.py README.md`.
It flags brackets left unfilled, missing sections, a missing license file, anything that looks like a secret, and links that are obviously placeholders.
The README is not done until the script passes, with the license line the only allowed failure while the file is still being added.

## Write only what the code supports

The first test runs of this skill invented routes, a cron job, a schema file, a timeline, and a data retention claim that the brief never mentioned, and presented them as fact.
A judge who opens one invented path and finds nothing trusts nothing else in the README, and a dead internal link is worse than a missing section.

- Every technical specific, a route, a file, a job, a library, a number, comes from the repo or from the brief.
  Read the code when it is available rather than reconstructing it from the stack list.
- When the code is not available, write the section from what is known and put every guess in a short "verify before judging" list at the end of the fixes, with the file or line the team should check.
- Statistics in the problem section carry a source or are marked to cite.
- Screenshot paths match files that exist, or the fixes list says to rename them.

## Repo hygiene that judges see

From the GitHub reference, the things judges look at after the README:

- **Commit history.** "fix", "fix again", "FINAL FINAL fix" tells them the team did not know what it was doing.
  Use the prefixes: `feat:`, `fix:`, `ui:`, `docs:`, `refactor:`, `chore:`.
- **A `.gitignore` that works.** No `node_modules/`, no `__pycache__/`, no build artifacts, and never a `.env`.
  Ship a `.env.example` with placeholders instead.
- **Meaningful commits from multiple people.** Judges look at who contributed.
- **Never force push to main.** Ever.

If the repo has none of these yet, fix them before polishing the README, because a committed API key undoes everything above it.

## Issues, the minimum system

If the team is tracking work verbally, set up the playbook's label set: `urgent`, `backend`, `frontend`, `design`, `pitch`, `blocked`.
Three to five issues for the core features, each with an owner, closed with a one line comment.
At the halfway point, review every open issue and cut what is not critical.
If it is not an issue, it does not exist.

## Before submission

Work through the checklist at the end of the README template reference: every bracket replaced, screenshots render, every link works, no secrets, setup instructions tested on a fresh machine, the diagram is accurate, the team section is complete, and the README reads well on a phone, because many judges review on one.

A broken demo link during judging is the single most damaging thing in this list.
Check it last, from a different device.
