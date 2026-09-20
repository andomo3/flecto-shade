# Release checklist

The shared workflow is [CONTRIBUTING.md](CONTRIBUTING.md).
Track current owners, branches, blockers and acceptance criteria in [GitHub Issues](https://github.com/andomo3/flecto-shade/issues).
The old package specifications in `planning/plans/packages/` provide historical context, not branch or directory restrictions.

## Every PR

- [ ] Linked issue with one owner and a concrete outcome.
- [ ] Small `feat/` or `fix/` branch, or an existing branch being completed.
- [ ] Reviewed diff against current `main`, with overlapping work coordinated.
- [ ] Relevant lint, syntax and automated checks pass.
- [ ] Changed user interactions checked in the browser; untested gaps stated.
- [ ] A teammate reviewed; all required checks and conversations are resolved.
- [ ] No credentials, dependency directories or disposable build artifacts added.
- [ ] README, data provenance and model assumptions match the behavior.

## Before submission

- [ ] Intended farmer-selected rain-event flow is merged and works on `main`.
- [ ] Public demo URL opens without a team login and matches the submitted revision.
- [ ] README includes that URL, a current hero screenshot and a working demo recording.
- [ ] Local setup works from a fresh checkout using the documented commands.
- [ ] Desktop and physical-phone checks pass.
- [ ] Offline cold start, reduced motion and WebGL fallback are checked.
- [ ] Pitch and slides match the demonstrated behavior and reproduce any numeric claims.
- [ ] Observations, modeled inputs, simulation and physical assumptions are distinguished.
- [ ] Team contributions, source credits and license are accurate.
- [ ] At least two timed rehearsals and an accessible fallback recording are complete.

## GitHub owner setup

- [ ] Protect `main` with reviewed PRs and required CI; disallow force pushes.
- [ ] Create the shared labels and assign the initial issues.
- [ ] Connect the approved deployment provider to `main`.
- [ ] All teammates and active agents have read the merged workflow.

Unchecked items are requirements, not evidence of failure or a claim that a check has run.
