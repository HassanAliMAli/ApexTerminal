# Verification report

**2026-11-26, Asia/Karachi.** Ubuntu 26.04.1 x86-64, 7.0 GiB usable RAM, Node 24.22.3, Python 3.14.4, OpenCode 2.4.1, and Codex 0.171.0-alpha.13.2. Tool smoke tests used native installations and local fixtures. No Docker, paid API calls, or production targets were used. The dedicated install occupies about 764 MiB before caches and backups.

| Component | Result and evidence |
|---|---|
| Superpowers | Two instruction-only skills installed from audited paths at the pinned revision. Full native plugin, hook behavior, and model-driven activation remain unverified. |
| Serena | Direct stdio MCP smoke passed using `--agent-interface tools`. TypeScript language server found `useUserResourcePermissions` and referencing symbols. Python is configured. Python symbol lookup and full-project indexing remain unverified. Agent entries are disabled by default. |
| Context7 | OpenCode connected. A direct stdio call to `query-docs` returned Vite `defineConfig` documentation without a supplied API key. |
| OpenSpec | Canonical shared skills generated. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passed for the engineering workflow spec. Initialization, change creation and change status passed in an empty temporary project. |
| Shared skills | Twelve canonical or linked skill frontmatter entries parsed and matched their directory names. Live model-driven discovery in a fresh OpenCode and Codex session remains unverified. |
| ast-grep | `ast-grep run -l ts -p 'export function $NAME($$$ARGS) { $$$BODY }' --files-with-matches frontend/src` returned real frontend matches. |
| Semgrep | `bash scripts/ai-engineering/check.sh sast` scanned 836 tracked files with two local rules and returned zero findings. Rule scope is limited to dynamic JavaScript evaluation and Python variables passed to shell subprocesses. |
| Gitleaks | Redacted history scan returned findings. The last 20 commits contained no matches. Full history scanned 110 commits and reported 89 matches. Values were excluded from the report. The matches need private triage before any disposition. |
| OSV-Scanner | Offline npm and Poetry scanning completed after downloading public vulnerability databases. It returned 17 advisories across seven affected package entries, including one high-severity advisory. |
| Playwright and axe | In an isolated headless Chrome context, navigation and a real button click passed. axe reported zero violations on the synthetic fixture. Application pages and authenticated flows remain unverified. |
| Playwright MCP | OpenCode reported connected. Direct stdio navigation and snapshot returned the expected fixture button. Codex listed the enabled launcher. |
| Chrome DevTools MCP | Direct stdio call opened the isolated fixture and evaluated its title using the page ID. Agent entries are disabled by default. |
| GitHub MCP | Direct hosted MCP handshake and read-only `get_file_contents` retrieved the fork README. The request reused the existing GitHub CLI credential in memory. Both agent entries remain disabled pending a dedicated least-privilege token. |
| GitHub Actions | New workflow parsed as YAML. Hosted execution and GitHub validation remain unverified. |
| k6 | All three profiles passed against a temporary loopback HTTP fixture with zero failed requests. Load recorded 3,513 requests at 3.42 ms p95. Stress recorded 493 at 4.61 ms. Spike recorded 322 at 3.13 ms. Application performance remains unmeasured. |
| OpenTelemetry | Existing versions exported two related synthetic spans into an in-memory exporter. Runtime traces across the application services, metrics, and log correlation remain unverified. |

## Dependency triage

The high-severity match was transitive `dnspython` 2.9.1 in the backend. The advisory identifies 2.9.2 as a fixed version. The agent directly declares `hono` and `@hono/node-server`. Both are transitive in the frontend. The backend directly declares `tornado` and receives `opentelemetry-api` transitively. Review lockfile paths and compatibility before updating. [dnspython advisory](https://osv.dev/GHSA-vvf4-9x63-8xvv)

## Reproduce the local checks

From the repository root, prepend `~/.local/share/apex-ai/bin` and `~/.local/share/apex-ai/npm/node_modules/.bin` to PATH if running tools directly. The wrapper adds both paths automatically.

```bash
bash scripts/ai-engineering/check.sh health
bash scripts/ai-engineering/check.sh config
bash scripts/ai-engineering/check.sh mcp
bash scripts/ai-engineering/check.sh browser
bash scripts/ai-engineering/check.sh sast
bash scripts/ai-engineering/check.sh secrets
bash scripts/ai-engineering/check.sh dependencies
```

For a new OSV cache, download public databases by adding `--download-offline-databases` to the command in the wrapper. For the k6 smoke, start a static page on loopback and set `TARGET_URL` to its path. For browser checks, open a fixture with a labeled button in an isolated context, click it, check the resulting state, and run `AxeBuilder.analyze()`. For Serena, call `find_symbol` and `find_referencing_symbols` with the hook name and `frontend/src/hooks/useUserResourcePermissions.ts`. For Context7, call `query-docs` with `/vitejs/vite` and a public `defineConfig` question.

## Delivery

Both live configuration files parsed after the edits. Codex CLI listed the configured entries. OpenCode confirmed connected status for Playwright and Context7. A model-mediated tool call from a fresh session in each agent was outside these checks.

The checkout started dirty on `chore/native-development`. Existing changes were preserved. ApexTerminal’s `develop` branch was created from its own `main`. The setup was pushed on `feature/apex-ai-engineering` and proposed in [ApexTerminal PR #1](https://github.com/HassanAliMAli/ApexTerminal/pull/1).
