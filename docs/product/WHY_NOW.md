# Why FixBundle exists

FixBundle is built around a boring failure mode: when a bug reaches another developer or a coding agent, the useful evidence is usually scattered across a terminal, Git history, logs, runtime details and a handful of source files.

The support-bundle pattern itself is established. GitHub Enterprise documents support bundles as compressed diagnostic archives used to give support engineers the environment and sanitized logs they need to troubleshoot an instance:
- https://docs.github.com/en/enterprise-server@3.18/admin/monitoring-and-managing-your-instance/monitoring-your-instance/about-support-bundles
- https://docs.github.com/en/enterprise-server@3.17/support/contacting-github-support/providing-data-to-github-support

The newer gap is coding-agent context. Recent developer discussions repeatedly point at:
- runtime/config context being more useful than longer prompts,
- context drift across long coding sessions,
- handoff context getting trapped in one agent/session,
- older incidents being debugged against a codebase that has already moved on.

FixBundle does not claim to solve agent memory. It solves a narrower piece: **produce a bounded, inspectable, redacted evidence packet tied to the code state where the failure happened.**

## Product test
The idea is not considered proven because the repo exists. Product-market fit requires external evidence: installs/downloads, stars/watchers, issues from unrelated users, repeat usage, integration requests and people willing to pay for team/hosted convenience.
