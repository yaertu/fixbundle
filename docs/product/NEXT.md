# Next move

## Distribution gate — prove repeat use before v0.7

v0.3–v0.6 now cover the evidence lifecycle:

```text
local / historical / GitHub Actions / OTLP production
                         ↓
                 FixBundle evidence ZIP
                         ↓
               compare baseline incident
                         ↓
              deterministic what-changed
```

The next highest-value move is **not another adapter**. It is proving that an unrelated maintainer can install FixBundle, capture a real failure, keep the ZIP, and use FixBundle again when the incident changes or recurs.

### Definition of done for the distribution gate
- publish a GitHub v0.6.0 release only after main CI is green,
- README first screen explains capture + compare in one glance,
- repository About/topics reflect GitHub Actions, OpenTelemetry and regression comparison,
- provide one copy/paste install path and one copy/paste compare path,
- show reproducible local, historical, live GitHub, OTLP and compare proof without fabricated metrics,
- ask for real issue/discussion feedback around failed CI and production incident handoff,
- record only observed stars/forks/issues/downloads; no vanity projections,
- do not begin v0.7 solely because v0.6 is merged.

### Adoption question
**Would someone keep a FixBundle artifact because comparing it with the next incident saves time?**

If the answer is not demonstrated, improve packaging, docs, discovery and workflow friction before adding more sources.

### Candidate after distribution proof
v0.7 Agent Handoff can add Codex / Claude Code / Cursor export profiles, but only if users need tool-specific handoff beyond the common portable evidence contract.
