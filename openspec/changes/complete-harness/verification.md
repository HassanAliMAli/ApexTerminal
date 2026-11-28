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

These were the outstanding checks on November 26. Native startup and test instructions now live in `docs/tutorials/build-from-source/`, `docs/tutorials/contribute/`, and `frontend/TESTING.md`.

## Follow-up on 2026-11-28

| Check | Result |
|---|---|
| Local discovery | `opencode debug agents` listed all 10 project roles. A Codex reviewer ran independently on the working-tree diff. Both roles directories matched by name, all 16 project skill headers matched their directory, and all 15 Superpowers skills resolved to pinned version 7.0.2. |
| OpenCode MCP | The warm client reported Context7 and Playwright connected. The status command retries an empty cold catalog. Fixture checks verified successful retry, bounded failure for a persistently empty catalog, and preservation of a Codex failure. A model-driven verification on the real checkout still requires a provider and permitted data scope. |
| Staged gate | A disposable repository accepted a benign staged change and rejected one synthetic token. The token value did not appear in the output. |
| Dependency scan | A fresh cache downloaded the public OSV databases for npm and PyPI. The offline scan of all four lockfiles reported no issues under the existing `osv-scanner.toml` exclusions. |
| Clean dependency installation | `npm ci` completed in isolated frontend, agent, and website directories. Frontend and agent both reported Hono 4.13.23 and `@hono/node-server` 2.1.11, matching their locks. The frontend runtime build completed. |
| Independent review | The reviewer ran 32 focused frontend tests and compared validation results and diagnostic messages across 54 fixture cases. The review also identified stale native setup instructions in four playbooks, which were corrected. |
| Patched Node dependencies | The clean agent suite passed all 2,300 tests, including SQL isolation. All 79 tests across the eight affected frontend files passed with the default per-test timeout on the clean install. The wider frontend run on the pre-existing install passed 4,611 tests with three skipped. The frontend and agent typechecks and the scoped Biome check passed. |
| Documentation | Native reference export, docs typecheck, five docs tests, Docusaurus build, and the table-of-contents check passed in the isolated checkout. |
| Native application acceptance | Three separate HTTPS launches started MySQL, Valkey, API, worker, agent, MCP server, and Nginx from native executables. Chromium sign-in, invalid credentials, and session reload passed. Dashboard persistence passed in Chromium and Firefox. The first WebKit launch lacked host libraries. The WebKit retry passed sign-in setup and both dashboard tests after adding the libraries to the project-local browser runtime. Final shutdown left no listeners on the four fixed test ports and removed generated test settings. The browser checks used disposable databases and a stub model. |

## Main-branch transition

OpenCode’s `nemotron-3.5-lightning-free` model reviewed an allowlisted export of public ApexTerminal revision `a8fa58d`. The standalone process used a temporary home without workstation configuration or credentials. Its two completed read-tool calls inspected `AGENTS.md` and `.github/workflows/local-security.yml`. It correctly reported the prior `develop` trigger and the `--redact=100` scan. The run reported zero model cost.

GitHub reported zero deployments and zero environments. The repository workflows and documentation identify no active deployment target. A deployment managed outside GitHub remains unverified until its inventory is confirmed.

The independent working-tree review was completed before opening the feature-branch PR. CI and review evidence will be recorded with the PR.
