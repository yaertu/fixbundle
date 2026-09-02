# Competitive landscape

FixBundle should not pretend the surrounding problems are unsolved. Several strong tools already cover adjacent pieces. The product boundary is deliberately narrower: **portable failure evidence**, not generic repository packing or generic agent memory.

## Repomix
Repository: https://github.com/yamadashy/repomix

Repomix is the mature reference for **codebase → LLM-friendly context**. It packs local/remote repositories, counts tokens, supports compression and MCP integrations, and has a substantial user base.

FixBundle should not compete by becoming a worse repo packer.

**Different job:** FixBundle packages a *failure event*: command output/exit state, exact Git identity, incident-vs-current revision, environment/stack evidence, selected source/config, redaction and checksums.

## temporal-debug-skill
Repository: https://github.com/MeherBhaskar/temporal-debug-skill

This agent skill independently validates the temporal-debugging pain: production incidents may belong to an older commit, and temporary Git worktrees are safer than checking out over current work.

FixBundle v0.3 overlaps on isolated worktree lifecycle. We should acknowledge that overlap instead of claiming novelty.

**Different job:** the skill teaches an agent *how to inspect history*. FixBundle creates a standalone, inspectable archive that can cross agent/vendor/support boundaries and carries logs, environment, source/config snapshots, redaction and integrity metadata.

## GitHub Actions + Copilot
GitHub can explain failed workflow checks with Copilot and exposes downloadable workflow logs.

**Different job:** FixBundle v0.4 should not merely re-explain the same log. It should normalize a failed CI run into the same portable evidence schema used locally, tie it to commit/diff/config context, sanitize it, and make the archive usable outside GitHub Copilot.

## Product boundary
FixBundle wins only if this stays true:

> **Repomix packages code. Temporal Debug navigates time. Copilot explains a GitHub failure. FixBundle packages the evidence of a failure so any debugger can work from the same facts.**

If a new feature does not strengthen that result, it probably does not belong in the core.
