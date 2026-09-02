# v0.4 live GitHub Actions evidence

Date: 2026-09-02

## What this proves
FixBundle v0.4 can read a real completed failed GitHub Actions run with read-only permissions, identify failed jobs/steps, download the real failed-job logs, redact them, include commit/workflow context, generate checksums and produce a portable evidence ZIP without a local checkout.

## Source incident
Repository: `yaertu/fixbundle`

- Actions run id: `33587184675`
- workflow run number: `41`
- conclusion: `failure`
- source commit: `d2799007f5d1ab7833d501ab830ec57cd59c795c`
- failed jobs: Windows / Python 3.10, 3.12 and 3.13
- failed step: `Historical demo`
- real log markers: `UnicodeEncodeError` and `cp1252`

The incident was not manufactured for v0.4. It happened during FixBundle's own development and was later repaired by the Windows stdout encoding hardening.

## Live proof run
- Actions run id: `33589138174`
- workflow run number: `63`
- proof commit: `d15385a7f9ecd0a0dbd1c67b0caad6f7aa21bb95`
- conclusion: `success`
- permissions shown by runner: `Actions: read`, `Contents: read`, `Metadata: read`

Live CLI:

```bash
fixbundle github --repo yaertu/fixbundle --run 33587184675 --output .fixbundle-live --lang en
```

Observed CLI result:

```text
FixBundle GitHub evidence bundle created [OK]
Repo: yaertu/fixbundle
Run: 33587184675
Failed jobs: 3
Redactions/path masks: 6
```

Independent verifier output:

```text
PASS live_run=33587184675
PASS failed_jobs=3
PASS log_files=3
PASS failed_step=Historical demo
PASS real_failure=UnicodeEncodeError/cp1252
PASS checksums=9
PASS token_not_serialized
```

The same run completed the platform matrix successfully:

```text
Ubuntu  / Python 3.10 PASS
Ubuntu  / Python 3.12 PASS
Ubuntu  / Python 3.13 PASS
Windows / Python 3.10 PASS
Windows / Python 3.12 PASS
Windows / Python 3.13 PASS
macOS   / Python 3.10 PASS
macOS   / Python 3.12 PASS
macOS   / Python 3.13 PASS
Live GitHub failure evidence PASS
```

## Bugs found by the live gate
The live gate justified itself twice before turning green.

1. Initial live capture received HTTP 403 even though the runner had Actions/Contents read permissions. Root cause was the GitHub job-log endpoint redirecting to a signed blob URL while Python `urllib` could forward a normal Authorization header. FixBundle now attaches Bearer auth as an unredirected header and has a regression test proving the redirect target receives no Authorization header.
2. The next live run successfully created the ZIP, but the verifier incorrectly expected the step name `Historical demo` inside raw log text. Step identity belongs in `jobs.json`; exception markers belong in logs. The verifier was corrected to check each evidence layer semantically.

## Security invariants
- GitHub token is used for the request but never written to the output manifest/bundle.
- Authorization is not forwarded to signed log-download redirect targets.
- Remote capture requires no local checkout.
- Only failed-job logs are captured.
- Captured text is bounded and passed through the redactor.
- No automatic upload occurs.

## Reproduction
The live gate is part of `.github/workflows/ci.yml` and is therefore rerun after changes. `scripts/verify_live_github.py` performs the ZIP-member, incident-identity, failed-step, real-log, checksum and token-serialization assertions.
