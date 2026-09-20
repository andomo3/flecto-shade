# Final demo checklist

## Verified in software

- [x] Farmer selects areas before running a rain event; no time-of-day timeline in the primary flow.
- [x] Team CAD contains 22 addressed flap instances; all controller mappings checked.
- [x] Conservative mode protects unselected/finished cells; explicit spill mode reports outside delivery.
- [x] Overlap uses a union; conservation identities and deterministic selection pass controller tests.
- [x] Existing Python regression suite passes after the four-region integration.
- [x] Golden path, JSON accounting, shortfall states and reduced motion exercised in browser.
- [x] Reset cancellation, edit cancellation, region shortcuts, drag/keyboard selection, repeat runs, numeric validation, narrow/restored viewport and replay checked in browser on `15ebcfd`.
- [x] Source geometry, idealized rain assumptions and missing physical validation are disclosed.
- [x] Eight controller-derived pitch examples reproduce; generated outputs pass the stale-file check.
- [x] Local documentation links resolve; the 30/60-second scripts contain 81/164 words.

The skill references `scripts/pitch_timer.py` and `scripts/check_readme.py`, which are absent from this checkout. Word counts and local links were checked directly; spoken timing and visual presentation checks remain team actions below.

## Before the table — team actions

- [ ] Review/merge PR #5 and use its final revision for the demo.
- [ ] Load the local page on the actual presentation laptop; verify WebGL and motion setting.
- [ ] If publishing, verify the approved public URL from a second device; no permanent demo URL is established by this PR.
- [ ] Download the passing recording, five screenshots and the self-contained presentation; play them with Wi-Fi off.
- [ ] Confirm Abba/Ameya/Shannon roles; name a backup speaker.
- [ ] Rehearse the 45-second demo three times with a timer; memorize opening and recovery lines.
- [ ] Check the projector, font size, laptop power and notifications.
- [ ] Put the repository/public-demo link or QR on the handout; only use a demo URL after verifying it.

## During the pitch

- [ ] First 15 seconds: name the grower and the choice between two areas.
- [ ] Before 60 seconds: show the product; no framework tour or live input typing.
- [ ] Live scene under 90 seconds: select → rain → flap combination → soil result.
- [ ] Say “simulated” when quoting water; explain the small prototype scale.
- [ ] Do not claim yield, physical water savings, actuator speed, zero leaks or a working roof.
- [ ] Close with the request for a grower and a physical footprint comparison.

## After

- [ ] Save judge feedback and separate crop needs from model limitations.
- [ ] Record which build and inputs were demonstrated.
- [ ] Keep the published version available if publication was approved.

Unchecked items require the team, the venue or physical hardware; software checks do not certify them.
