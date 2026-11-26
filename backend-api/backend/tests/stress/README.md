# Stress / load tests

Run the multi-user load simulator against a dedicated, loopback API instance. Start the API using the [native setup guide](../../../../docs/tutorials/build-from-source/run-the-stack-from-source.md). Set the API worker count when starting Uvicorn. Use a fresh test database and administrator.

Run from this directory with the backend's Python environment active:

```bash
export BASE_URL=http://127.0.0.1:8000
export ORIGIN=http://127.0.0.1:1420
USERS=80 DURATION=20 RAMP=5 ./run_stress.sh
```

Provide `ADMIN_EMAIL` and `ADMIN_PASSWORD` through your local secret environment. To simulate more users from one address, enable `RATE_LIMIT_EXEMPT_ENABLED` only on the isolated test deployment and provide its `WORKSPACE_AUTH_TOKEN`. Set `MCP_USERS` to add MCP-only users and `API_MCP=0` to exclude MCP from the API users' traffic.

## What it does

Each simulated user logs in, opens a bridge WebSocket (an auto-answering "browser tab"), and loops a
weighted mix of real endpoints: `validate-and-sync` (once, the dashboard-open aggregation),
`dash/sync` (save), the read endpoints (`api-source`, `apps`, `shared`, `resource-permissions`),
`display-settings`, and FINOS Workspace MCP tool calls over `/mcp`. A `--mcp-users` pool can add MCP-only
load to isolate the MCP server's impact on the rest of the API.

## Reading the output

The simulator prints, per action: count, `ok%`, p50/p95 latency, and HTTP status distribution.
Then it reports the live runtime gauges scraped from `/metrics`:

- `db_pool_connections` — checked-out connections per engine pool (n/a for SQLite — `StaticPool`).
- `threadpool_tokens` — worker thread-pool occupancy.
- `event_loop_lag_seconds` — event-loop scheduling delay (the main "something is blocking the loop"
  signal).
