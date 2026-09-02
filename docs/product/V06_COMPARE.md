# v0.6 Cross-source Evidence Compare

## User result

```bash
fixbundle compare baseline.zip incident.zip
fixbundle compare baseline.zip incident.zip --format json
```

Two FixBundle artifacts become one deterministic, integrity-checked **what changed?** report. Compare does not claim root cause and does not send evidence to an LLM or network service.

## Supported inputs
- `fixbundle/0.3`: local + historical Git evidence
- `fixbundle/0.4`: GitHub Actions failure evidence
- `fixbundle/0.5`: OTLP production evidence

## Integrity before interpretation
Compare treats a ZIP as untrusted input. Before parsing `manifest.json` or evidence JSON it:
1. validates member paths,
2. rejects absolute paths, Windows drive paths, `..`, backslashes and NULs,
3. rejects duplicate members, symlink members and encrypted members,
4. enforces member-count, per-member and total uncompressed-size bounds,
5. parses `SHA256SUMS.txt` strictly,
6. requires exact checksum coverage for every file except `SHA256SUMS.txt` itself,
7. hashes every covered member and fails closed on mismatch,
8. accepts only known FixBundle schemas.

The implementation never extracts the input archives and never mutates them.

## Normalized evidence fields
Fixed-order comparison currently covers:
- bundle schema + capture mode
- project / repository / workflow / run identity
- incident commit + current head
- changed files
- failed local commands
- failed GitHub jobs + steps
- production exceptions
- service/version/environment/deployment identity
- trace IDs + span names
- detected stacks + Python/platform runtime identity

## Status semantics
- `changed`: both inputs provide the field and values differ
- `added`: baseline lacks the field, incident provides it
- `removed`: baseline provides the field, incident lacks it
- `unavailable`: neither input provides the field
- equal fields are counted as `unchanged` but omitted from the detailed change list

These are evidence-availability/value semantics, not causal claims. In cross-source comparisons, `removed` can simply mean that the incident source does not carry that evidence type.

## Determinism
- fixed field order
- canonical sorting/deduplication for list/dict evidence
- no timestamp in compare output
- JSON output uses stable key sorting
- same two valid artifacts produce the same report

## Verification
`tests/test_compare.py` covers local↔local, GitHub↔GitHub, GitHub↔OTLP, checksum tampering, traversal, duplicate members, symlinks and unsupported schemas.

`tests/test_compare_cli.py` runs the real CLI subprocess and verifies JSON output + fail-closed invalid ZIP behavior.

`scripts/demo_compare.py` creates two real v0.5 OTLP FixBundle artifacts, validates their checksums through compare, and proves service version, exception and trace drift. CI runs this demo on Ubuntu, Windows and macOS across Python 3.10 / 3.12 / 3.13.

## Non-goals
- no root-cause guarantee
- no fuzzy incident joining
- no generic line-by-line log diff
- no Sentry fingerprint clone
- no automatic upload
- no input extraction or mutation
