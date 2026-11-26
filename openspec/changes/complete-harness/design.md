## Context

The workstation installation and existing security CI are already in use.

## Decisions

Store native role files in each assistant's discovery directory. Keep domain procedures in shared skills and use short role prompts to select them. Configure advisory roles to report findings without modifying the implementation. OpenCode denies shell and edits for those roles. Codex roles inherit the parent session's sandbox.

Use a local pre-commit hook that invokes the existing pinned Gitleaks installation against the index. Keep full history scans explicit because imported history already has findings. Preserve existing CI checks.

## Risks

A clean checkout must be trusted by the assistant before project settings are loaded. Local hook activation is per Git installation and CI retains the independent remote check.
