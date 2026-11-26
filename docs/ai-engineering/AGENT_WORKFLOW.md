# Agent workflow

Use OpenCode for implementation and Codex for independent review by default. Either agent can own either role. Read the repository's AGENTS.md and load only the skills needed for the current change.

- **Trivial changes.** Inspect the relevant code, make the smallest compatible edit, and run targeted checks.
- **Standard changes.** Use OpenSpec to record the proposal, requirements, acceptance scenarios, design and tasks. Use Superpowers procedures to clarify scope and sequence implementation. Keep the execution plan in the same OpenSpec change.
- **High-risk changes.** Add a threat assessment, compatibility and rollback decisions, measurable budgets, and independent review. Verify failure modes and migrations on isolated environments.

Search the smallest relevant symbol set with Serena and inspect structural matches with ast-grep before editing. For unfamiliar framework APIs, upgrades and external integrations, send Context7 the public package name, required version and a focused question. Use versioned upstream documentation when results are unavailable or disagree with the locked dependency.

Validate contracts, authorization and data boundaries before relying on UI controls. Run applicable lint, types, builds and requested tests. Use isolated browser verification for frontend behavior. Use local scans and review their findings before changing dependencies. Re-run affected checks after review and attach evidence to the OpenSpec change.

## Handoff

Put the handoff in the OpenSpec change or share a file from the implementation worktree. Include the branch and commit, and identify any uncommitted files the reviewer needs. Use separate worktrees if both agents need write access at the same time.

```markdown
# Handoff
- Objective and OpenSpec change
- Acceptance criteria
- Architecture and security constraints
- Modified files and implementation decisions
- Checks run and evidence
- Known limitations and remaining tasks
- Branch, commit and worktree
```

Ask the reviewer to inspect the exact revision, prioritize correctness and regression risks, and return findings with file references and supporting evidence. Resolve confirmed findings and repeat verification before archiving.
