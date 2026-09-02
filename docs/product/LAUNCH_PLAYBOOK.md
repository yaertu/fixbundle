# FixBundle launch playbook

No “revolutionary AI platform” copy. Show the failure, show the command, show the resulting evidence.

## GitHub title/description
**FixBundle — package a failure, not just a repository**

Description:
`Package a broken repo, failed command, or historical Git commit into a redacted AI-ready debugging bundle.`

## Show HN draft
**Title**
`Show HN: FixBundle – package a software failure into portable AI debugging evidence`

**Body**
`FixBundle is a small local-first CLI for a debugging handoff problem: the failure log is in one terminal, the relevant Git state is somewhere else, and by the time someone or a coding agent looks at the bug the code may already have moved on.`

`It captures Git identity/diff, selected source/config text, runtime info and only the test/build/runtime commands you explicitly ask it to run. Common secret patterns and absolute user paths are redacted before it creates a checksum-verified ZIP.`

`v0.3 adds historical incident capture. With --commit <sha>, FixBundle opens a detached temporary Git worktree for the old revision instead of checking it out over the current workspace. The repo includes a reproducible demo that creates a buggy commit, fixes main, leaves uncommitted work in place, and verifies that the old failure is captured while current HEAD stays untouched.`

`This overlaps with temporal-debugging agent skills on the Git worktree idea. The intended difference is the output: FixBundle produces a standalone evidence archive that can move between agents, CI systems and human support instead of teaching one agent how to inspect history.`

`MIT, Python 3.10+, no account and no telemetry.`

## Reddit / developer forum draft
**Title**
`Testing a local CLI that packages the actual failure evidence instead of making you paste half a repo into an AI chat`

**Body**
`A bug handoff often arrives with the wrong mix of evidence: a stack trace but no commit SHA, source files but no environment info, or a production failure from a revision that is no longer checked out.`

`FixBundle collects those pieces into one redacted ZIP. You choose any test/build/runtime commands it should capture. v0.3 also supports --commit <sha>; it uses an isolated Git worktree so it can reproduce an older incident without replacing the current working tree.`

`This is not trying to replace Repomix or an agent memory tool. The unit being packaged is the failure: command output, Git identity, environment, relevant text/config, redaction metadata and checksums.`

`There is a reproducible demo in the README and scripts/demo.py. The useful feedback at this point is concrete: when a bug gets handed to you, what evidence do you repeatedly have to ask for because it was missing?`

## Short post
`A repository snapshot is not the same thing as a bug report. FixBundle packages the failure itself: command output, exact Git state, environment hints, relevant source/config, redaction and checksums. v0.3 can also capture an older incident commit in an isolated worktree without touching current HEAD.`

## Distribution rules
- Post the demo, not a feature dump.
- Ask one concrete question: “What evidence is missing from your real bug handoffs?”
- Do not mass-cross-post identical copy.
- Do not invent adoption numbers, novelty claims or user stories.
- Name adjacent tools when comparison is useful instead of pretending the category is empty.
- Reply to technical criticism with code/tests, not marketing language.
- Update the README from repeated feedback, not from one-off requests.
