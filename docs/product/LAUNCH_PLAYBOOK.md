# FixBundle launch playbook

No “revolutionary AI platform” copy. Show the failure, show the command, show the resulting evidence.

## GitHub title/description
**FixBundle — turn a broken repo or old Git commit into a redacted AI debugging bundle**

Description:
`One command turns a broken project or historical Git commit into a redacted, AI-ready debugging bundle.`

## Show HN draft
**Title**
`Show HN: FixBundle – package a broken repo or old Git commit for AI debugging`

**Body**
`FixBundle is a small local-first CLI for a debugging handoff problem: the failure log is in one terminal, the relevant Git state is somewhere else, and by the time someone or a coding agent looks at the bug the code may already have moved on.`

`It captures Git identity/diff, selected source/config text, runtime info and commands you explicitly ask it to run. Common secret patterns and absolute user paths are redacted before it creates a checksum-verified ZIP.`

`The part I wanted most was historical incidents. With --commit <sha>, FixBundle opens a detached temporary Git worktree for the old revision instead of checking it out over your current workspace. The repo includes a reproducible demo that intentionally creates a buggy commit, fixes main, leaves uncommitted work in place, and proves the old failure can still be captured without touching current HEAD.`

`MIT, Python 3.10+, no account and no telemetry.`

## Reddit / developer forum draft
**Title**
`I made a local CLI that packages the actual debugging context instead of making you paste half a repo into an AI chat`

**Body**
`The problem is simple: a bug report usually arrives with the wrong mix of evidence. Maybe there is a stack trace but no commit SHA, a source dump but no environment info, or the production failure happened on a revision that is no longer checked out.`

`FixBundle collects those pieces into one redacted ZIP. You choose any test/build/runtime commands it should capture. v0.3 also supports --commit <sha>; it uses an isolated Git worktree so it can reproduce an older incident without replacing your current working tree.`

`There is a real demo in the README and a one-command reproducer in scripts/demo.py. I would especially like feedback on what evidence is still missing from real bug handoffs, not just feature ideas.`

## Short post
`Debugging an old production incident against today’s checkout is a good way to waste an afternoon. FixBundle v0.3 captures the old commit in an isolated Git worktree, runs the failure you ask for, redacts common secrets/paths and produces one AI-ready ZIP. Local-first, MIT.`

## Distribution rules
- Post the demo, not a feature dump.
- Ask one concrete question: “What evidence is missing from your real bug handoffs?”
- Do not mass-cross-post identical copy.
- Do not invent adoption numbers or user stories.
- Reply to technical criticism with code/tests, not marketing language.
- Update the README from repeated feedback, not from one-off requests.
