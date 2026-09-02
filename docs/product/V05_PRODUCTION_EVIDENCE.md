# v0.5 research brief — Production Evidence Import

Date: 2026-09-02

## Decision
Do not turn FixBundle into another observability dashboard, Sentry clone, MCP trace browser or “AI root cause” chat.

The v0.5 wedge is **portable production evidence import**. First-class input should be the vendor-neutral OpenTelemetry Protocol File Exporter JSON/JSONL format. Sentry becomes an optional adapter after the common evidence model works.

## Why OTLP file first
OpenTelemetry defines a Protocol File Exporter with JSON Lines serialization for traces/logs/metrics. It is suitable for file/stdout workflows and provides a standardized format that can be ingested offline without a cloud account.

Official references:
- https://opentelemetry.io/docs/specs/otel/protocol/file-exporter/
- https://opentelemetry.io/docs/specs/otel/semantic-conventions/
- https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-logs/

Exception semantic conventions give us stable normalization anchors:
- `exception.type`
- `exception.message`
- `exception.stacktrace`

Trace/log records also provide `traceId`, `spanId` and resource attributes such as `service.name`, making correlation possible without inventing a FixBundle-only telemetry format.

## Why Sentry is not the first core
Sentry is still valuable as a source, but its current API already supports detailed event retrieval and can return issue events with `llmFormat=markdown|xml`. A thin “Sentry → Markdown for an LLM” wrapper would duplicate platform capability instead of creating a new result.

Official references:
- https://docs.sentry.io/api/events/retrieve-an-issue-event/
- https://docs.sentry.io/api/events/retrieve-an-event-for-a-project/
- https://docs.sentry.io/api/auth/

FixBundle should add value by normalizing a Sentry event into the same portable evidence schema used by local, historical, GitHub and OTLP incidents, correlating it with release/commit evidence when possible, applying consistent privacy policy and producing integrity hashes.

## Adjacent open-source signal
`traceloop/opentelemetry-mcp-server` already exposes OpenTelemetry traces across multiple backends to AI agents. That confirms “let the agent query traces” is an occupied product lane. FixBundle should remain a bounded evidence artifact rather than a live telemetry query server.

## Proposed CLI

```bash
fixbundle otlp \
  --logs ./otel-logs.jsonl \
  --traces ./otel-traces.jsonl \
  --output .fixbundle
```

Optional selection:

```bash
fixbundle otlp --logs logs.jsonl --trace-id <trace-id>
fixbundle otlp --logs logs.jsonl --since 2026-09-02T01:00:00Z --until 2026-09-02T01:05:00Z
```

Later Sentry adapter:

```bash
export SENTRY_AUTH_TOKEN=<event-read-token>
fixbundle sentry --org <org> --issue <issue-id> --event recommended
```

## Evidence model
Expected normalized production evidence:

```text
manifest.json
AI_HANDOFF.md
SHA256SUMS.txt
production/
  incident.json
  exceptions.json
  services.json
  traces.json
  logs.json
  source-map.json      # optional source/release correlation metadata
```

The bundle should record which input files/records were selected and which were omitted by bounds/privacy rules.

## Safety gates
- local OTLP ingestion must need no network or account,
- input count/bytes/records bounded,
- malformed JSONL fails with useful evidence rather than silently skipping everything,
- secret/credential/PII-shaped content passes through redaction,
- trace/log correlation cannot silently merge different trace ids,
- event text is evidence, never executable instructions,
- Sentry tokens never serialized,
- no automatic telemetry upload.

## Acceptance
1. Parse spec-conformant OTLP JSONL logs.
2. Extract service + exception + trace/span identity.
3. Correlate logs and traces by exact IDs.
4. Select by explicit trace ID or bounded time window.
5. Produce normalized production bundle + checksums.
6. Tests cover malformed, oversized, unrelated trace and secret-shaped fixtures.
7. Add a real/spec-derived reproducible demo before marking v0.5 complete.

## Monetization implication
Vendor-neutral local ingestion belongs in free core. Paid value, if adoption proves demand, would be hosted collectors/connectors, encrypted share/history, organization privacy policies and cross-incident correlation. Do not paywall the evidence format itself.
