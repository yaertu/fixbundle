# Adoption scoreboard

FixBundle does not use vanity claims before there are users. This file records the public adoption state and the evidence gates that can justify continuing the product.

> Last checked: 2026-09-02

## Public baseline

- GitHub stars: 0
- forks: 0
- public repository: yes
- public v0.6.0 release: published
- open non-PR issues: 1 (`#10`, maintainer distribution gate)
- open pull requests: 0
- PyPI: not yet published
- unrelated-user feedback: none yet
- unrelated real captures: 0
- retained external baselines: 0
- repeat-use compares: 0

Latest main CI after the validation-gate merge: run `33594019142`, 10/10 jobs PASS, including the `Live GitHub failure evidence` invariant.

## Why the scoreboard changed

The earlier scoreboard treated stars and install counts as early proof gates. The 2026-09-02 market re-audit found that major parts of the workflow already exist in DebugBundle, GitHub Agentic Workflows, TestSprite and support-bundle ecosystems.

Therefore the primary question is no longer “can we attract attention?” It is:

> **Does portable cross-source evidence comparison create behavior that platform-native tools do not already satisfy?**

Stars remain useful distribution telemetry, but they are not product validation.

## Stage A — Problem/evidence validation

Run 10 qualified public field cases under `VALIDATION.md`.

Record for each case:

- did the evidence comparison add a material new fact,
- did it narrow the regression window,
- did it distinguish different failure identities hidden behind overall-red status,
- did it reveal environment/runtime/dependency drift,
- did it identify a concrete missing evidence class,
- was the finding already explicit in the issue.

Working interpretation:

- **STRONG:** ≥5/10 material findings
- **WEAK:** 3–4/10
- **FAIL:** <3/10

These are product-learning thresholds, not statistical claims.

## Stage B — External response

Cap the first outreach set at 5 high-quality, evidence-first maintainer contacts.

Measure:

- useful response,
- correction accepted/disputed,
- investigation direction changed,
- maintainer asks how evidence was produced,
- maintainer attempts install/capture.

Warning signal: 0 useful responses or capture attempts after 5 genuinely qualified contacts.

## Stage C — Activation

Activation requires an unrelated person generating a valid FixBundle from their own real failure.

Target learning state: 3 unrelated real captures.

For each activation record:

- install path,
- install → first valid bundle elapsed time if known,
- capture mode,
- command/token friction,
- privacy/redaction concern,
- artifact size,
- what evidence the user actually inspected.

Do not count stars, clones, our fixtures or our own repositories as activation.

## Stage D — Retention

A retained baseline is stronger than an install.

Count only when the unrelated user intentionally keeps or later references the artifact because they expect another incident/run to be comparable.

Target: at least 1 real retained external baseline.

## Stage E — Repeat-use compare

North-star event:

```text
external capture #1
      ↓
artifact retained
      ↓
real incident #2
      ↓
fixbundle compare
      ↓
concrete user-reported reduction in evidence reconstruction,
uncertainty or tool switching
```

Target: 1 unrelated same-user repeat-use compare before v0.7 feature work.

## Competitive displacement metric

For every activated user, capture the answer to one practical question:

> Why was the native platform not enough for this incident?

Candidate answers may involve:

- cross-source comparison,
- historical source identity,
- local/offline workflow,
- portable handoff across tools,
- privacy/no instrumentation,
- integrity/checksum requirements.

If users cannot name a concrete reason, the product boundary is weak.

## Secondary distribution telemetry

Track, but do not optimize ahead of retention:

- GitHub stars,
- forks,
- release downloads when observable,
- issues/discussions from unrelated users,
- external links/mentions,
- repeat visitors or package installs if a trustworthy source becomes available.

No paid/incentivized starring. No fabricated download numbers.

## Kill signals

- fewer than 3 material findings after 10 qualified field cases,
- 0 useful response/capture attempts after 5 evidence-first outreaches,
- no artifact retention after 3 unrelated real captures,
- native tools erase the cross-source/offline wedge,
- users consistently want this only as an embedded feature inside another tool.

If a kill signal lands, do not answer with more features. Narrow, pivot or archive.

## 200k-star reality check

A huge star count is not a plan. FixBundle is in a narrower and increasingly competitive developer-tool market. Exceptional distribution would require a job that is both broadly repeated and dramatically clearer than platform-native alternatives.

Until repeat-use exists, the only honest KPI is **learning rate per real external failure**.
