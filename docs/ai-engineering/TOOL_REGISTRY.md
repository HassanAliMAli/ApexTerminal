# Tool registry

The user tool prefix is `~/.local/share/apex-ai`. npm tools are under `npm/node_modules`, uv environments under `uv-tools`, and native binaries or uv launchers under `bin`.

| Component | Version or revision | Responsibility |
|---|---|---|
| [Superpowers](https://github.com/obra/superpowers) | 7.0.2, `22f0b463e7a5e579904dd6211a520321035526f7` | Two reviewed shared skill files |
| [Serena](https://github.com/oraios/serena) | 2.1.0 | On-demand semantic navigation |
| [Context7](https://github.com/upstash/context7) | 4.8.0 | Public version-compatible documentation, subject to service quota |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | 2.2.0 | Durable specifications and change lifecycle |
| [Agent Skills](https://agentskills.io/specification) | Shared layout | Canonical, on-demand instructions |
| [ast-grep](https://github.com/ast-grep/ast-grep) | 0.51.3 | Structural search |
| [Semgrep](https://semgrep.dev/docs/getting-started/quickstart) | 1.187.0 | Local static analysis with metrics disabled |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | 8.30.1 | Redacted local and CI secret detection |
| [OSV-Scanner](https://github.com/google/osv-scanner) | 2.7.1 | Offline npm and Poetry advisory comparison |
| [Playwright](https://playwright.dev/) | Frontend lockfile and MCP-bundled 1.66.0-alpha-2026-11-18 | Repeatable browser checks |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | 0.0.86 | Interactive browser verification |
| [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 1.14.0 | Browser diagnosis |
| [axe-core](https://github.com/dequelabs/axe-core) | Playwright adapter 4.14.1 | Automated accessibility checks |
| [GitHub MCP](https://github.com/github/github-mcp-server) | Hosted | Disabled by default, direct read-only smoke passed |
| [GitHub Actions](https://docs.github.com/actions) | Hosted | Existing checks plus redacted local security scan on develop PRs |
| [k6](https://github.com/grafana/k6) | 2.4.0 | Loopback load smoke |
| [OpenTelemetry](https://opentelemetry.io/) | Existing agent lockfile | Trace readiness through console or an authorized OTLP endpoint |

Use the CLI from either agent for native quality checks. Start semantic indexing and browser diagnosis on demand. Current status and constraints are in the [verification report](VERIFICATION_REPORT.md).
