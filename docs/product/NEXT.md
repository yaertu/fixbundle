# Next move

## v0.6 validation freeze — prove a standalone job before v0.7

v0.3–v0.6 already cover the evidence lifecycle:

```text
local / historical / GitHub Actions / OTLP production
                         ↓
                 FixBundle evidence ZIP
                         ↓
               compare baseline incident
                         ↓
              deterministic what-changed
```

The next move is **not another adapter and not Agent Handoff**.

The market re-audit on 2026-09-02 found direct overlap:

- DebugBundle already sells deterministic agent-ready debug bundles for production incidents,
- GitHub Agentic Workflows already investigates failed CI runs and exposes run-diff/audit flows,
- TestSprite already ships failure bundles plus two-run `test diff`,
- support-bundle and temporal-debugging tools already cover adjacent pieces.

That means the old question “can we build this?” is closed. The new question is harder:

> **Will unrelated users repeatedly choose portable, cross-source evidence comparison instead of staying inside the platform that already owns the failure?**

See [`VALIDATION.md`](VALIDATION.md) for the falsification protocol.

## Current candidate positioning

Do not lead with “AI-ready bundle.” That phrase is already occupied.

Candidate result:

> **Capture a known-good state and a failing state. Prove what changed in the evidence before anyone guesses why.**

This is still a hypothesis. Do not harden it into branding until field cases support it.

## Gate sequence

```text
v0.6.0 public release
        ↓
competitive reality audit
        ↓
10 qualified evidence-first field cases
        ↓
≤5 contextual maintainer outreaches
        ↓
first unrelated real capture
        ↓
artifact intentionally retained
        ↓
same user returns with incident #2
        ↓
compare used on retained artifacts
        ↓
user states concrete value
        ↓
ONLY THEN decide whether v0.7 exists
```

## What counts as progress now

- finding a public failure where evidence comparison changes the suspect window,
- proving an alleged “same failure” is actually a different failed job/step,
- proving a suspected commit already existed in a green run,
- finding environment/runtime/dependency drift missed by source-only diagnosis,
- identifying a specific missing evidence class that blocks causality,
- learning why a user would or would not keep the artifact,
- learning why GitHub/TestSprite/DebugBundle/native observability is or is not enough.

## What does not count

- another version number,
- another source adapter,
- a prettier README by itself,
- our own demo bundles,
- our own CI using FixBundle,
- stars without real use,
- a one-off compliment,
- AI-generated root-cause prose with no external behavioral signal.

## Immediate field case

`tanbamboo/rusql#159` currently qualifies as User #1 candidate.

Read-only evidence already narrowed the timeline from several suspected merges to the first verified `mysql-diff` red at the M63 merge, while two earlier overall-red runs actually had `mysql-diff` success and failed on Rust formatting. The harness also drops server child stdout/stderr, so panic-vs-lifecycle causality cannot be proven from the current CI artifact.

That is the kind of contribution FixBundle must repeatedly produce before asking users to install it.

## Decision after the gate

Possible outcomes:

### CONTINUE

Repeat-use proves that portable cross-source compare is a real job. Only then choose the smallest next feature demanded by evidence.

### NARROW

Users like the evidence diff but want it embedded in CI/support tooling. Convert the value into a library, GitHub Action or protocol instead of growing a standalone CLI platform.

### PIVOT

The repeated pain is real, but the winning job is adjacent: support-bundle verification, temporal incident linking, or another evidence workflow discovered in field cases.

### ARCHIVE

The platform-native tools are good enough and users will not retain/compare artifacts. Stop spending engineering time.

The product is allowed to die. That is a successful validation outcome if learned early.
