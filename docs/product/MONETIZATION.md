# FixBundle monetization: only after the free core earns usage

The CLI should not be paywalled just because it can collect evidence. A paid layer only makes sense where teams pay to remove operational friction.

## Free core
- local bundle generation
- redaction/path masking
- stack detection
- historical Git capture
- public schema
- local adapters that do not require hosted infrastructure

## Plausible paid layer after demand exists
1. **Encrypted share links** with expiry/revocation and team access.
2. **Hosted GitHub Actions / Sentry connectors** that build bundles from selected incidents/runs.
3. **Team policies** for allow/deny paths, retention and required evidence fields.
4. **Bundle history + regression compare** across incidents.
5. **Enterprise support / self-hosted gateway** for controlled environments.

## What not to do yet
- no fake Pro tier before users ask for team features,
- no telemetry hidden in the CLI,
- no affiliate clutter in README before there is meaningful audience,
- no claim that a bundle guarantees an AI will fix the bug.

## Demand gates
Monetization work starts only when external usage supplies a reason: recurring unrelated users, repeated integration requests, teams asking for sharing/history/policy, or sponsors approaching the project. Until then the priority is usefulness, evidence and distribution.
