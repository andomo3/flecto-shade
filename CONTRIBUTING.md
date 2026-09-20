# Working together on Flecto Shade

## One workflow for humans and agents

1. Find or create a [GitHub issue](https://github.com/andomo3/flecto-shade/issues).
   Name one owner, the user-visible outcome, acceptance checks and any dependencies.
   Link the branch and PR as soon as they exist.
2. Fetch current `main`, then branch:

   ```bash
   git fetch origin
   git switch -c feat/soil-moisture origin/main
   ```

   Use `feat/<short-task>` for new work and `fix/<short-task>` for fixes.
   Existing `pkg/` and `devin/` branches can finish through their current PRs.
   Do not discard local changes when switching; use an isolated worktree if needed.
3. Commit small, working increments with `feat:`, `fix:`, `ui:`, `docs:`, `refactor:` or `chore:`.
   Push frequently so teammates can inspect progress.
   Open a draft PR early for unfinished work and state what remains.
4. Before review, fetch again and integrate changes from `origin/main` into your branch.
   A merge is fine; do not rewrite another person's branch.
   Rerun affected checks, review the complete diff, and record results in the PR.
5. A teammate reviews the change; Abba coordinates merges while the team works in parallel.
   Merge only complete, tested increments with passing required checks.
   Review merge opportunities at least every two hours, but never merge broken or incomplete work to meet that interval.
6. Close the linked issue with the merged PR and a short outcome.
   If blocked, add `blocked` and explain what is needed and from whom.

Never push or force-push directly to `main`, including hotfixes.
Start on a branch rather than working uncommitted on `main`.
No fixed directory locks or one-commit quotas apply.
Agree interface changes and overlapping files with the current issue owner before integrating them.
At the halfway check-in, cut or defer issues that are not necessary for the demo.

## Issues and labels

Use the task form for features, bugs and presentation work.
Set a real GitHub assignee; the owner field also helps when someone's account is not assignable yet.
Labels must be created in the repository before they can be applied.

| Label | Color | Meaning |
| --- | --- | --- |
| `urgent` | `D73A4A` | Required before the demo |
| `backend` | `0075CA` | Data, simulation or backend work |
| `frontend` | `2DA44E` | Browser application |
| `design` | `A371F7` | Visual design and CAD presentation |
| `pitch` | `FBCA04` | Research, story and presentation |
| `blocked` | `D87613` | Needs an explicit dependency resolved |

Initial issue candidates, to claim with the relevant teammate:

- Integrate the farmer-selected watering flow from PR #5: Abba, with Ameya reviewing frontend integration.
- Finish frontend polish and provide the final hero screenshot: Ameya.
- Publish the approved demo and rehearse the submission: Abba.
- Validate agricultural claims and replace unsupported water-loss assumptions: Abba.

These are handoff candidates, not a claim that issues or assignments have already been created.
GitHub Issues becomes the live board; old package tables under `planning/` are historical context.

## Run the app

The checked-in static page needs only Python's file server.
From the repository root:

```bash
python -m http.server --directory software/page 8000
```

Open `http://localhost:8000`.
No API keys, `.env`, database or Docker are required.

## Development checks

For data builds and tests, use Python 3.13 and the pinned dependencies:

```bash
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on macOS/Linux, or `.venv\Scripts\Activate.ps1` in PowerShell.

```bash
python -m pip install -r software/requirements.txt
python -m pip install ruff==0.13.2
python -m ruff check data software --select E9,F63,F7,F82
python -m pytest software/tests -q
```

The S1/H1 tests require both raw weather files described in [data/README.md](data/README.md).
CI downloads and checksums these public inputs before running tests; the tests themselves verify offline builds.
On Windows, install `tzdata==2025.2` if Python cannot find `America/New_York`.

Use Node 22 to syntax-check browser scripts; it is a development tool, not an app server:

```bash
node --check software/page/app.js
```

Run any additional tests or generators introduced by your feature.
CI also runs the watering controller tests when they are present.
Run the figure checks documented in PR #5 when working on that feature.
There is currently no TypeScript typecheck command or npm application build.
UI changes also need a browser check of the affected interaction; attach evidence and identify the tested revision.
CI does not verify visual rendering, physical hardware or agricultural outcomes.

## Repository hygiene

- Never commit credentials, `.env` files, `node_modules/`, virtual environments or caches.
- If a feature introduces configuration, commit only an `.env.example` with placeholders.
- Keep disposable build output ignored. Existing processed CSVs and runtime JSON are intentional versioned inputs for offline operation.
- Regenerate data through its builder rather than manually editing generated values.
- Keep the README accurate for merged code; label previews and unmerged features explicitly.
- Retain the MIT license and third-party credits; a software license does not grant rights to someone else's patented mechanism.

## Owner setup still needed

File changes do not configure GitHub settings or create issues automatically.

1. In [repository rules](https://github.com/andomo3/flecto-shade/settings/rules), protect `main`: require a PR, one teammate approval, resolved conversations and the `Checks` CI result; block force pushes and branch deletion.
   Select the check after this workflow has run at least once.
2. Create the six labels above in [Labels](https://github.com/andomo3/flecto-shade/labels), then create and assign the initial issues.
3. Connect the approved static host to `main`.
   For Vercel, use `software/page` as the root, the Other framework preset, an enabled but empty Build Command override, and `.` as the output directory.
   See Vercel's [static build instructions](https://vercel.com/docs/builds/configure-a-build#skip-build-step).
   Record the actual public URL in the README only after verifying it.
   Host auto-deployment is not configured by this PR; CI runs tests but does not deploy.
4. Merge the workflow PR and ask all active sessions to fetch `main` and read `AGENTS.md`.
   Preserve this workflow when resolving overlaps with older PRs #3, #5 and #6.

With an authenticated GitHub CLI and repository write access, create the labels without replacing existing ones:

```bash
gh label create urgent --color D73A4A --description "Required before the demo" --repo andomo3/flecto-shade
gh label create backend --color 0075CA --description "Data, simulation or backend work" --repo andomo3/flecto-shade
gh label create frontend --color 2DA44E --description "Browser application" --repo andomo3/flecto-shade
gh label create design --color A371F7 --description "Visual design and CAD presentation" --repo andomo3/flecto-shade
gh label create pitch --color FBCA04 --description "Research, story and presentation" --repo andomo3/flecto-shade
gh label create blocked --color D87613 --description "Needs a dependency resolved" --repo andomo3/flecto-shade
```

Existing labels can be kept; do not use `--force` to overwrite another team's labels.
