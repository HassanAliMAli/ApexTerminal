# Verification on 2026-11-26

Ubuntu, Nushell 0.117.0, OpenCode 2.4.1, Codex 0.171.0-alpha.13.2. The private native runtime returned Node 26.12.1 and Python 3.13.14.

| Check | Evidence |
|---|---|
| OpenCode roles | `opencode --standalone debug agents` returned all ten Apex roles as subagents. |
| Codex discovery | Native prompt-input diagnostics included the reviewer and all three Apex domain skills. All ten TOML definitions parsed with matching names and required fields. |
| Codex MCP | Context7 returned public OpenCode library IDs. Playwright navigated to a synthetic page and returned the expected title. |
| OpenCode MCP | Both the normal and standalone MCP listing returned no servers. The config source diagnostic found the global config. A temporary project with one known local Context7 launcher showed the same symptom. |
| Local hook | Pinned pre-commit installed and `setup-hook` succeeded on a second run. A clean staged fixture passed. One synthetic GitHub token failed the hook and its value did not appear in output. |
| OpenSpec | The `complete-harness` change passed strict validation. |
| Semgrep | Two local rules scanned 836 tracked targets with zero findings. The constrained session needed temporary Semgrep settings and log paths. |
| Lighthouse | Local fixture accessibility score was 1.0. |
| fast-check and Hypothesis | Both passed on synthetic integer properties. |
| StrykerJS | The command runner killed all five mutants on a temporary arithmetic fixture. The constrained sandbox denied the launcher’s logging listener, so the smoke used an approved native run. |
| Type checking | Frontend passed with Node 26. The agent typecheck could not find `tsc` in the current agent installation. |

## Remaining work

Fresh model-driven delegation in both assistants and independent cross-review are still open. OpenCode MCP needs further investigation. GitHub MCP stays disabled without a dedicated token. Tool fixtures did not measure ApexTerminal behavior. The checkout contains private native runtime artifacts, but the current branch has no tracked native startup procedure. The repository’s full backend suite uses Testcontainers and was outside the requested container-free execution. No application feature code changed.
