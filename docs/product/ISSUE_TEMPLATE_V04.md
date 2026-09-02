# v0.4 issue body source

This file mirrors the intended public v0.4 milestone issue so the plan remains reviewable in Git history.

## User result
Turn an explicit failed GitHub Actions run into a portable, redacted FixBundle evidence ZIP without copying logs by hand.

## Acceptance
- [ ] `fixbundle github --repo owner/repo --run <id>` read-only capture path
- [ ] exact repo/commit/workflow/run/job/step identity
- [ ] bounded failed-job logs
- [ ] secret/token/path redaction
- [ ] relevant diff/config context
- [ ] checksum + AI_HANDOFF output
- [ ] remote capture does not require a local checkout
- [ ] synthetic/recorded fixture tests
- [ ] one real public failed-run demo
- [ ] Linux/macOS/Windows CI where applicable

## Non-goal
Do not duplicate GitHub Copilot's “Explain error”. The output must be portable evidence usable outside GitHub.
