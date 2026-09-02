# v0.4 design brief — GitHub Native failure evidence

## User result
A failed GitHub Actions run should become the same kind of portable FixBundle evidence packet as a local failure, without requiring the user to copy logs by hand.

## Not the goal
GitHub already provides workflow logs and Copilot can explain failed checks. FixBundle should not build another “explain this error” chat button.

## The gap
A workflow failure is more useful when the evidence stays portable outside GitHub and is normalized with:
- repository + commit identity,
- failed workflow/run/job/step identity,
- bounded failed-job logs,
- event/PR metadata that is safe to disclose,
- relevant diff/config snapshot,
- stack/environment hints,
- redaction report,
- checksums,
- `AI_HANDOFF.md`.

## Proposed interfaces
Local/authenticated CLI first:

```bash
fixbundle github --repo owner/repo --run <run-id>
```

Later, optional GitHub Action:

```yaml
- uses: yaertu/fixbundle@v0
  if: failure()
```

## Safety gates
- read-only GitHub permissions by default,
- never serialize `GITHUB_TOKEN` or secret values,
- do not fetch unavailable fork/PR secrets,
- bounded logs and artifacts,
- record exactly which GitHub resources were read,
- fail closed if redaction/output assumptions cannot be met,
- no automatic public upload of the produced bundle.

## Acceptance evidence
- fixture or test repository with a deliberately failed workflow,
- bundle contains exact run/job/commit identity,
- failure text is present,
- injected secret-shaped fixture is redacted,
- current local repository is not required for remote capture,
- tests + CI cover normalization/redaction code,
- README shows a real failed-run → bundle demo.
