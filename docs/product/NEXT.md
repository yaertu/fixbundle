# Next move

## v0.4 single highest-value milestone
**Failed GitHub Actions run → portable FixBundle evidence packet.**

Do not begin Sentry, cloud accounts, dashboards or agent plugins before this vertical slice is independently verified.

### Definition of done
- accepts an explicit repository + Actions run identifier,
- reads only bounded, documented GitHub resources,
- identifies failed jobs/steps and exact commit,
- stores normalized failure metadata + redacted logs,
- includes enough repository/diff/config context to make the bundle useful outside GitHub,
- produces the existing FixBundle schema family rather than a separate ad-hoc export,
- integration tests use recorded/synthetic fixtures without leaking credentials,
- one real public failed-run demo is captured and documented,
- README/demo updated only after the evidence passes.

### Distribution hypothesis to test
A CI-native workflow gives FixBundle a natural GitHub discovery loop: a failure happens inside GitHub, the evidence artifact is produced inside GitHub, and the maintainer can attach the same artifact to an issue or hand it to any debugging agent. If unrelated users do not care about this flow, do not blindly build v0.5.
