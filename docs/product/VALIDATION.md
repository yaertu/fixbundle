# v0.6 Market Reality & Falsification Protocol

> Status: ACTIVE
> Started: 2026-09-02
> Code freeze: v0.7 feature work is blocked until this protocol produces evidence.

## 1. Decision we are trying to make

The question is not whether FixBundle can be engineered further. It can.

The question is whether **portable cross-source failure evidence + deterministic before/after comparison** is valuable enough to deserve a standalone product and repeated user behavior.

This protocol is designed to falsify that thesis quickly.

## 2. Current thesis

Candidate job-to-be-done:

> **I have a known-good state and a failing state. Give me a trustworthy, portable answer to “what evidence changed?” before an AI or human starts guessing causality.**

Candidate differentiators:

1. **Cross-source:** local command, historical Git, GitHub Actions and OTLP file evidence share one comparison model.
2. **Portable:** the result is an inspectable ZIP/JSON artifact, not a dashboard-only view.
3. **Offline compare:** two retained artifacts can be compared without an account, cloud backend or LLM.
4. **Integrity first:** checksum validation and fail-closed ZIP handling happen before evidence is interpreted.
5. **Non-causal contract:** compare reports observed deltas and unavailable evidence instead of manufacturing root-cause confidence.

Every one of these is a hypothesis until an unrelated user values it.

## 3. Known market facts that weaken the thesis

### Direct overlap exists

- DebugBundle already markets deterministic, agent-ready production debug bundles through SDK, CLI, API, MCP and dashboard surfaces.
- TestSprite already ships self-consistent failure bundles and a two-run `test diff` command.
- GitHub Agentic Workflows already provides CI failure investigation and workflow-run audit/diff capabilities.
- Product-specific support-bundle ecosystems already normalize/redact diagnostics into archives.

Therefore the following claims are prohibited:

- “Nobody has done this.”
- “First AI debugging bundle.”
- “Unique failure bundle format.”
- “Only tool that compares failed runs.”
- “The market is empty.”

### Category pull is not proven

A direct competitor existing is not proof that customers care. At the 2026-09-02 audit, the public `debugbundle/debugbundle` repository had 6 stars and 0 forks. That is evidence of active competition, not evidence of broad pull.

Likewise, FixBundle currently has no unrelated-user retention signal.

## 4. What must be true for FixBundle to continue

### H1 — Evidence delta adds material information

For qualified public failures, FixBundle-style evidence comparison must surface at least one fact that materially narrows the investigation beyond “the workflow is red.”

Examples of material information:

- an overall-red run actually failed for a different job/step than the incident under investigation,
- the alleged suspect commit is already present in a later green run,
- the first actual red occurs later than the issue author believes,
- environment/runtime/dependency identity changed while source did not,
- a production trace belongs to a different release/deployment than the current source tree,
- a required evidence class is absent, making a causal claim unjustified.

Non-material output:

- reformatting the same stack trace,
- restating the issue title,
- generic AI root-cause suggestions,
- a giant diff without a narrowed evidence question.

### H2 — Portability matters

At least one unrelated user must prefer retaining a portable artifact because the investigation crosses tool boundaries: GitHub → local IDE/agent, production telemetry → repository, vendor support → engineering, or one AI tool → another.

If everyone is satisfied with the native platform view, portable ZIPs are a feature looking for a market.

### H3 — Retention creates second-use value

At least one unrelated user must intentionally keep a first artifact and later compare it with a second real incident/run.

This is the north-star proof.

A star, clone, install or one-off compliment does not satisfy H3.

### H4 — FixBundle beats “just use the platform” somewhere

For at least one repeated workflow, the user must be able to state why GitHub-native CI diagnosis, TestSprite, DebugBundle, Sentry/observability AI, or manual log comparison is insufficient or more cumbersome.

If there is no crisp answer, FixBundle has no defensible product boundary.

## 5. Qualification filter for public field cases

A field case counts only when all mandatory criteria are true:

- opened by a human maintainer/contributor, not a reporting bot,
- currently unresolved or still useful as a live investigation,
- contains a real failure identity: run, job, command, trace, exception or reproducible event,
- has at least two states worth comparing or a credible missing-baseline problem,
- FixBundle-style analysis can be performed read-only before outreach,
- the resulting note adds evidence rather than promotion.

Preferred cases:

- last-green / first-red uncertainty,
- “works locally, fails in CI,”
- repeated overall-red runs with uncertain failure identity,
- dependency/environment drift,
- production incident tied to historical code,
- CI vs production mismatch,
- recurring incident where a retained baseline would matter.

Reject:

- already-bisected issues with exact root cause and fix,
- bot-generated diagnosis reports,
- giant projects where a drive-by note adds noise,
- cases requiring private data we cannot inspect,
- issues where the only contribution would be a FixBundle link.

## 6. Field experiment ladder

### Experiment A — 10 evidence-first public cases

Goal: test H1 before asking anyone to install anything.

For 10 qualified cases, record:

- repository + issue,
- human/bot qualification,
- baseline state,
- incident state,
- evidence classes available,
- evidence classes missing,
- exact new fact found,
- whether the new fact changes the suspect window or next debugging step,
- whether the same conclusion was already explicit in the issue.

Working pass threshold:

- **PASS:** at least 5/10 produce a material new fact or a precise missing-evidence finding.
- **WEAK:** 3–4/10.
- **FAIL:** fewer than 3/10.

This is a product-learning threshold, not a statistical claim.

### Experiment B — Evidence-first outreach

Only after a case has a useful read-only result.

Outreach format:

1. lead with the exact evidence correction/narrowing,
2. include direct run/job/commit references,
3. separate FACT from HYPOTHESIS,
4. identify the missing evidence required for stronger causality,
5. do not lead with a product link,
6. mention FixBundle only if it is relevant to retaining/capturing that evidence.

Initial cap: **5 contextual outreaches**. No bulk promotion.

Record:

- response / no response,
- correction accepted / disputed,
- did maintainer change investigation direction,
- did maintainer ask how the evidence was produced,
- did maintainer install/capture,
- friction encountered.

Working failure signal: 0 useful responses or capture attempts after 5 genuinely qualified, evidence-first contacts.

### Experiment C — External activation

A user counts as activated only when they generate a valid FixBundle from their own real failure.

Do not count:

- our own repo,
- our own machine-only demos,
- fixture bundles,
- a user merely starring/cloning the repository.

For each activation measure:

- install path used,
- time from install start to first valid bundle,
- capture mode,
- bundle size,
- redaction/preview concern,
- command/token friction,
- whether user could explain what the bundle was for.

Target learning state: 3 unrelated real captures.

### Experiment D — Baseline retention

After a useful first capture, ask one simple behavioral question:

> “Would you keep this ZIP as the baseline for the next time this fails?”

Record actual behavior, not intention.

Retention counts only when the user keeps or references the artifact later.

### Experiment E — Repeat-use compare

This is the north-star test.

Success event:

```text
same unrelated user
    ↓
real incident/run #1 captured
    ↓
artifact intentionally retained
    ↓
real incident/run #2 occurs
    ↓
fixbundle compare baseline incident
    ↓
user reports a concrete reduction in evidence reconstruction,
uncertainty, or tool switching
```

Capture the exact sentence or behavior. Do not translate it into fabricated “minutes saved” unless the user actually measures time.

## 7. User #1 candidate: tanbamboo/rusql#159

Current read-only finding:

```text
M59/M61  2d446a0  mysql-diff PASS
last green 2574725 mysql-diff PASS
M64       ad79f15  mysql-diff PASS
M63       a3d0372  mysql-diff FAIL
later     8f9ba52  mysql-diff FAIL
```

Two overall-red runs listed as the “same failure” actually had `mysql-diff` success and were red because the Rust formatting job failed. The first verified `mysql-diff` failure is the M63 merge run.

The harness also launches `rusql-server` with child stdio ignored, so the current evidence cannot distinguish server panic/exit from a connection/lifecycle failure. That is a concrete evidence gap, not a root-cause guess.

Status: candidate prepared; external contact requires explicit approval.

## 8. Competitive displacement questions

When a user activates, ask only questions tied to actual workflow:

- Why not use the GitHub Actions UI / Copilot / CI Doctor for this case?
- Why not keep the evidence in Sentry/Datadog/other observability backend?
- Would JSON/Markdown alone be enough, or does an inspectable ZIP matter?
- Do you need to compare across different sources, or only two runs from the same platform?
- Is integrity/checksum validation valuable or invisible ceremony?
- Would you install an SDK to get richer evidence, or is “no instrumentation” the point?
- Which evidence field made the comparison useful?

Do not turn every answer into a feature request. Look for repeated independent demand.

## 9. Kill / pivot criteria

FixBundle should be narrowed, pivoted or archived if any of these become true:

### Kill signal K1 — No evidence advantage

After 10 qualified public cases, fewer than 3 produce a material new fact or a precise missing-evidence finding.

### Kill signal K2 — No activation pull

After 5 high-quality evidence-first outreaches, nobody attempts a real capture or asks for the workflow.

### Kill signal K3 — No retention

After 3 unrelated real captures, nobody intentionally retains an artifact or sees a reason to compare later.

### Kill signal K4 — Native platforms erase the wedge

A major existing tool provides the same arbitrary local + historical + CI + telemetry artifact model, offline cross-source compare, comparable integrity/privacy guarantees and lower adoption friction, and target users prefer it.

### Kill signal K5 — Value collapses into a feature

Users consistently like the comparison but only inside another tool they already use. In that case, stop pretending the CLI is the business. Consider a library, GitHub Action, schema/protocol or integration surface instead.

## 10. Pivot hypotheses allowed after failure

These are research directions, not roadmap commitments:

1. **Evidence Diff CLI/library** — strip the product to deterministic run/incident delta generation.
2. **CI artifact action** — failed workflow → redacted evidence artifact, no standalone capture UX.
3. **Support-bundle verifier** — validate/redact/compare third-party diagnostic archives.
4. **Evidence protocol** — schema + integrity tooling that other products embed.
5. **Temporal incident linker** — map old production evidence to exact historical source without mutating the active workspace.

Do not build any of these before the current thesis is tested.

## 11. Change-control during validation freeze

Allowed without unlocking v0.7:

- documentation corrections,
- packaging/install friction fixes that block a real user,
- security/privacy fixes,
- broken release/CI fixes,
- evidence needed to run the validation experiments.

Not allowed without evidence:

- new source adapters,
- dashboard/UI expansion,
- MCP/agent integrations,
- AI root-cause summaries,
- hosted cloud features,
- speculative enterprise controls,
- version-number-driven feature work.

## 12. Decision log

Every meaningful field result should end in one of four labels:

- `THESIS_STRENGTHENED`
- `THESIS_WEAKENED`
- `FRICTION_ONLY`
- `NO_SIGNAL`

The goal is not to protect FixBundle. The goal is to reach a correct product decision faster.
