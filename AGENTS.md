# FINOS Workspace

Self-hosted analytics workspace: web app, API, agent, MCP servers, widget plugins, docs site ([workspace.finos.org](https://workspace.finos.org)).

## Layout

| Path | Contents | Stack |
|---|---|---|
| `frontend/` | Web app and admin panel | Vite, React, TypeScript, Biome, Vitest, Playwright, Storybook |
| `backend-api/backend/` | API, worker, migrations (`alembic/`), admin scripts (`scripts/`), Workspace MCP server (`workspace_mcp/`) | Python 3.13, FastAPI, Poetry, Alembic, pytest, Ruff |
| `agent/` | Copilot agent; `mcp-server/` holds its MCP server | Node, TypeScript, Hono, Vercel AI SDK (`ai`), `node --test` |
| `widget-plugins/` | Local plugin install directory read by the API; git-ignored | |
| `docs/` | Documentation source; `docs/examples/` holds example plugins, backends and reference agents | Markdown, MDX |
| `website/` | Docs site | Docusaurus |
| `sbom/` | Existing CycloneDX dependency snapshots | |
| `.github/workflows/` | CI | GitHub Actions |

Read "Agent rules" below before changing `agent/`.

## AI engineering workflow

For substantial changes, follow [the shared agent workflow](docs/ai-engineering/AGENT_WORKFLOW.md). Keep requirements, design decisions, acceptance criteria, and tasks in OpenSpec. Use Superpowers procedures to guide execution and retain verification evidence in the same change. Load only the relevant skill. Use Context7 for unfamiliar APIs or dependency upgrades and Serena for targeted semantic navigation. For tool availability and local checks, run `bash scripts/ai-engineering/check.sh health` and consult [the setup guide](docs/ai-engineering/AI_ENGINEERING_SETUP.md).

## Skills

Task playbooks live in `.agents/skills/<name>/SKILL.md`. Load the one that matches the task.

| Skill | Use for |
|---|---|
| `install-locally` | Run the native development stack on a workstation |
| `develop-plugins` | Build, validate, approve and try a widget plugin against a local stack |
| `contribute` | Branch, run the checks, sign off, open a pull request |

## Commands

| Task | Directory | Command |
|---|---|---|
| Backend lint | `backend-api` | `ruff check backend` |
| Backend tests | `backend-api/backend` | `poetry install --with dev && poetry run pytest tests -q` |
| Web lint | `frontend` | `npx biome ci .` |
| Web types | `frontend` | `npm run typecheck` |
| Web unit tests | `frontend` | `npm run test:unit` |
| Web e2e tests | `frontend` | `npm run test:e2e` |
| Agent types | `agent` | `npm run typecheck` |
| Agent tests | `agent` | `npm test` |
| Reference data | `website` | `npm run reference` |
| Docs site | `website` | `npm run typecheck && npm test && npm run build` |
| Example plugin | `docs/examples/<name>` | `npm ci --ignore-scripts && npm run build && npm test` |

- Node 26.12.1 for `frontend/`, `agent/` and `website/` (`engines` and CI `node-version`). Python 3.13 for the backend (`python = "~3.13"`).
- Install with `npm ci` in `agent/` and `npm ci --ignore-scripts` in `frontend/`, `website/` and the Node examples (`plotly-charts`, `ag-grid`, `sql-explorer`) in `docs/examples/`.
- CI pins Ruff 0.15.22 and Poetry 2.3.2 (`.github/workflows/backend-checks.yml`).
- Backend tests start temporary native MySQL and Valkey processes. See the test guide for binary overrides.
- Move `backend-api/backend/envs/.env` and `backend-api/backend/user_create.json` away before a full backend run and put them back after; the settings read both.
- `npm run test:e2e` needs a running HTTPS stack and `E2E_USER_EMAIL`, `E2E_USER_PASSWORD`: `frontend/TESTING.md`.
- `npm run reference` uses the locked backend Python environment and replaces `node_modules` in `agent/` and `frontend/`. Run it before the docs site checks.
- The `ag-grid` and `sql-explorer` tests also need a `.venv` with the Python test packages and a PostgreSQL: `.github/workflows/examples.yml`.
- Detail per part: `docs/tutorials/contribute/run-the-tests.md`.

## Rules

- Write no comments in code, in any language.
- Do not edit generated reference data by hand; `reference-data/` folders are git-ignored. Regenerate it: `docs/tutorials/contribute/regenerate-reference-data.md`.
- Do not edit generated dependency snapshots in `sbom/` by hand. Use the current lockfiles for dependency audits.
- A new database migration follows `docs/tutorials/contribute/add-a-database-migration.md`.
- A new backend setting is a `Field` with a `description` in `Settings` (`backend-api/backend/utilities/config.py`), which generates the settings reference, and goes in `backend-api/backend/envs/.env.example`.
- A new agent environment variable is described in `agent/src/lib/env-reference.ts`; a test fails without it.
- Never commit `.env` files, `user_create.json`, `backend-api/backend/scripts/cfgs/config.toml`, secrets, `local_storage/` or `widget-plugins/`.
- Keep changes to the files the task needs. No unrelated formatting changes.
- Run the checks for every part you changed before you commit.
- `MODE=local` lets the API accept a private or plain `http` address from any user for a data backend, an agent or an MCP server, and lets a superuser develop a new version of an approved widget plugin in place. Deployments set `MODE=production`.

## Git

ApexTerminal uses `origin/main` as its permanent branch. Keep synchronization with FINOS out of the ordinary development workflow.

- Check the current branch first. Create a short-lived feature branch from the latest `origin/main` for each change.

```bash
git fetch origin && git switch --no-track -c feature/<short-name> origin/main
```

- Name branches `feature/<short-name>`: lowercase, hyphenated.
- Open pull requests into `main` and merge only after applicable checks pass. Delete each feature branch after confirming its changes reached `main`.
- Commit with `git commit -s`. The only trailer is the committer's own `Signed-off-by`; the DCO check fails a pull request with an unsigned commit (`CONTRIBUTING.md`).
- Push and open pull requests only when asked:

```bash
gh pr create --base main
```

- A pull request description must not be empty; `.github/workflows/pr-description.yml` fails on an empty one.

## Copilot agent

Read [the agent instructions](agent/AGENTS.md) before changing `agent/`. They cover the thin harness, tool dispatch, tenant isolation, signed state, URL fetching, resource limits, and verification.
