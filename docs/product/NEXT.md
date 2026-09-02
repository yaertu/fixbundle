# Next move

## v0.6 candidate — Cross-source Evidence Compare

**User result:** two FixBundle artifacts in, a deterministic “what changed?” report out.

v0.5 closes the production-ingestion gap with OTLP. The next useful problem is no longer “collect more logs.” It is comparing a known-good/baseline incident against a broken/current incident without forcing the engineer to manually jump between Git, CI, telemetry and support bundles.

## Research boundary
Do not build another generic log diff or vendor error-grouping engine.

- Sentry already owns vendor-specific issue grouping/fingerprints.
- Existing log comparison products can compare two log sets and highlight new/missing/spiking events.
- Git already owns source-level diff/bisect.
- SRE discussions still repeatedly identify “what changed?” and switching among GitHub/observability/tickets/docs as painful.

The FixBundle-specific wedge is **cross-source artifact comparison**: compare the normalized evidence we already capture from local commands, historical Git, GitHub Actions and OTLP production incidents.

## Proposed CLI

```bash
fixbundle compare baseline.zip incident.zip
```

Optional machine output:

```bash
fixbundle compare baseline.zip incident.zip --format json
```

## Deterministic comparison layers
1. Bundle/schema/capture-mode identity.
2. Failure signature changes without pretending to replace Sentry grouping.
3. Exception type/message presence and trace/service identity drift.
4. Service/release/environment/deployment changes.
5. Command exit-code and failed job/step changes.
6. Git commit/diff evidence when present.
7. Stack/runtime/dependency evidence changes when present.
8. Missing evidence explicitly reported instead of guessed.

## Non-goals
- no LLM required for the core diff,
- no “root cause guaranteed” claim,
- no fuzzy merging of unrelated traces/incidents,
- no raw line-by-line dump as the primary result,
- no Sentry fingerprint clone.

## Definition of done
- compare two valid FixBundle ZIPs read-only,
- validate checksums before comparison,
- reject unsafe ZIP paths / malformed manifests / incompatible unsupported schema,
- normalize evidence across different capture modes,
- emit deterministic JSON plus human-readable Markdown/text,
- clearly separate added / removed / changed / unavailable evidence,
- tests for local↔local, GitHub↔GitHub and GitHub/OTLP cross-source cases,
- reproducible before/after demo,
- existing historical, live GitHub and OTLP gates remain green.

## Why this could matter
FixBundle becomes more useful on the **second incident**, not only the first. That is directly aligned with the adoption gate that matters most: somebody choosing to use the tool again because prior evidence became a baseline.

Research notes are intentionally conservative: “what changed?” is a real incident-response problem, but comparison itself is not novel. The product value must come from a portable, normalized, integrity-checked artifact boundary across sources.
