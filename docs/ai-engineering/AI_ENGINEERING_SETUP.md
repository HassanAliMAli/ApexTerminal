# ApexTerminal AI engineering setup

The workstation tool directory is `~/.local/share/apex-ai`. It contains pinned npm packages, uv environments, and checksum-verified native binaries. Run `opencode` or `codex` from the project root in WezTerm. Bash utilities can be invoked directly from Nushell.

```bash
bash scripts/ai-engineering/check.sh health
bash scripts/ai-engineering/check.sh config
bash scripts/ai-engineering/check.sh browser
bash scripts/ai-engineering/check.sh mcp
bash scripts/ai-engineering/check.sh init /path/to/new-project
```

OpenCode reads MCP entries under `mcp.servers` in `~/.config/opencode/opencode.json`. Codex reads `mcp_servers` in `~/.codex/config.toml`. Both discover project skills under `.agents/skills`. OpenSpec stores requirements, changes and archives under `openspec/`.

Use Playwright MCP for interaction and the existing frontend Playwright Test suite for repeatable journeys. Use isolated, headless Chrome DevTools MCP for network, console, rendering and performance diagnosis. Start one browser tool at a time. Automated axe scans cover machine-checkable rules. Review keyboard order, focus recovery, accessible announcements and the meaning of chart encodings manually.

Run local quality checks with the `secrets`, `sast`, and `dependencies` commands. The existing CodeQL, frontend, backend, agent and E2E workflows retain their roles. The new pull-request workflow runs Gitleaks and the checked-in local Semgrep rules.

Run the loopback-only load scenario with `k6 run scripts/ai-engineering/health-load.js`. Set `TARGET_URL` to an authorized local HTTP health endpoint. Its fixture thresholds are 250 ms p95, under 1% request failures and over 99% successful checks. Set `LOAD_PROFILE` to `stress` or `spike` for the bounded eight-user profiles. Set application performance budgets from representative runtime measurements.

The application agent already supports console traces with `OTEL_TRACES_CONSOLE=true` and collector export with `OTEL_EXPORTER_OTLP_ENDPOINT`. Use synthetic requests for console tracing and inspect only trace IDs, timings and outcomes. Backend instrumentation, metric baselines and cross-service propagation require separate runtime verification.

See [workflow](AGENT_WORKFLOW.md), [tools](TOOL_REGISTRY.md), [skills](SKILLS_REGISTRY.md), [verification](VERIFICATION_REPORT.md), and [maintenance](MAINTENANCE.md).
