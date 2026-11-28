---
name: contribute
description: 'Covers changing FINOS Workspace and opening a pull request into main: finding or opening an issue, branching off origin/main as feature/<short-name>, the CI checks of each area with the commands and tool versions CI uses, narrowing test runs, the task guides, NOTICE and SBOM rules, signing off with git commit -s, fixing a failing DCO check, and the pull request, review and merge rules. Use for requests such as "open a pull request", "make a PR", "run the checks before I push", "what does CI run", "fix the DCO check", "sign off my commits", "start a feature branch", "run the backend tests", "regenerate the widgets schema", "regenerate the reference data".'
---

# Contribute

## 1. Find or open an issue

1. Search open and closed issues; with no match, open one with the problem and the proposed change. `gh` prints the issue URL:
   ```bash
   gh issue list --state all --search "<words>"
   gh issue create --title "<problem>" --body "<problem and proposed change>"
   ```
2. Answer the questions raised in the issue before starting a large change.

## 2. Branch off main

1. Check the branch; on `main`, create a feature branch, with `<short-name>` lowercase and hyphenated. Confirm `git branch --show-current` then prints `feature/<short-name>`:
   ```bash
   git branch --show-current
   git fetch origin && git switch --no-track -c feature/<short-name> origin/main
   ```

- Use short-lived feature branches and open pull requests into `main`. Merge after the applicable checks pass and delete the feature branch.
- Without push access to the repository, push the branch to a fork, as `CONTRIBUTING.md` describes. Before changing `agent/`, read the section "Agent rules (`agent/`)" in `AGENTS.md`.

## 3. Match the CI toolchain

| Tool | Version | Set in |
|---|---|---|
| Node | 26.12.1 | `node-version` of every workflow; `engines` of `frontend/package.json` and `website/package.json`. Ignore the v22.13.1 in `frontend/.nvmrc` |
| Python | 3.13; 3.14 for `docs/examples/` | `backend-checks.yml`, `docs.yml`, `python = "~3.13"` in `backend-api/backend/pyproject.toml`; `examples.yml` |
| Poetry | 2.3.2 | `backend-checks.yml`, `docs.yml` |
| Ruff | 0.15.22 | `backend-checks.yml`, `backend-api/backend/poetry.lock` |
| Biome | 2.4.8 | `frontend/package-lock.json` |

- Backend tests start native MySQL and Valkey. Use a separate checkout so the API settings and administrator bootstrap files stay isolated. See `docs/tutorials/contribute/run-the-tests.md` for native binary versions and overrides.
- Reference generation uses the locked Python environment and native Node. See `docs/tutorials/contribute/regenerate-reference-data.md`.

## 4. Run the checks of each area changed

| Check (workflow / job) | Runs on | Directory | Command |
|---|---|---|---|
| Backend checks / Ruff | every PR | `backend-api` | `pip install ruff==0.15.22`, `ruff check backend` |
| Backend checks / Tests | every PR | `backend-api/backend` | `pip install poetry==2.3.2`, `poetry install --with dev`, `poetry run pytest tests -q` |
| Frontend checks / Biome | every PR | `frontend` | `npm ci --ignore-scripts`, `npx biome ci .` |
| Frontend checks / Types | every PR | `frontend` | `npm run typecheck` |
| Frontend checks / Unit tests | every PR | `frontend` | `npm run test:unit` |
| Frontend checks / Spelling | every PR | repository root | `typos --config frontend/_typos.toml frontend/src frontend/CHANGELOG.md` |
| PR Build Check (Frontend) | `frontend/**` | `frontend` | `npm run build` |
| Agent checks / Types, Tests | `agent/**` | `agent` | `npm ci`, `npm run typecheck`, `npm test` |
| Agent checks / Dependency audit | `agent/**` | `agent` | `npm audit --omit=dev --audit-level=critical` |
| Docs | every PR | `website` | `npm ci --ignore-scripts`, `npm run reference`, `npm run typecheck`, `npm test`, `npm run build` |
| End-to-end tests | `frontend/**`, `backend-api/backend/**`, `agent/**`, `scripts/ci/native-test-tools.sh`, `.github/workflows/e2e.yml` | `backend-api/backend` | prepare the frontend build as `frontend/TESTING.md` shows, then run `python -m tests.run_browser -- --project=chromium --project=firefox --project=webkit` |
| Example plugins | `docs/examples/**` | `docs/examples/<name>` | `npm ci --ignore-scripts`, `npm run build`, `npm test`; the Python jobs as `.github/workflows/examples.yml` runs them |
| PR description | every PR | | a description that is not blank |

- Confirm each command exits with status 0. `npm run lint` in `frontend` applies the fixes Biome can make.
- Docs fails on a generated reference page out of step with the code, a broken link or anchor, a page that no sidebar lists, and a page with headings but no table of contents.
- A new spelling exception goes under `[default.extend-words]` in `frontend/_typos.toml`.

## 5. Narrow a test run

| Scope | Directory | Command |
|---|---|---|
| Backend test | `backend-api/backend` | `poetry run pytest tests/test_auth.py::TestAppLogin::test_login_valid_credentials -v` |
| Backend by name | `backend-api/backend` | `poetry run pytest tests -k <words>` |
| SQLite migrations | `backend-api/backend` | `poetry run pytest tests/test_migration_dialects.py::TestSQLiteMigrations -v` |
| Web app file | `frontend` | `npx vitest run tests/unit/components/General/Avatar.test.tsx` |
| Web app by name | `frontend` | `npx vitest run -t "<name>"` |
| Agent file | `agent` | `node --test --experimental-test-module-mocks --import ./tests/setup.ts tests/unit/scripts/reference.test.ts` |
| Agent by name | `agent` | `node --test --experimental-test-module-mocks --import ./tests/setup.ts --test-name-pattern="<name>" 'tests/**/*.test.ts'` |
| End-to-end file | `frontend` | `npx playwright test tests/e2e/auth.spec.ts` |

## 6. Follow the task guide

| Change | Guide in `docs/tutorials/contribute/` and its commands |
|---|---|
| Database table or column | `add-a-database-migration.md`: with the development stack up, run `python -m alembic revision --autogenerate -m "<message>"` from `backend-api/backend` with the API environment active, then `poetry run pytest tests/test_migration_chain.py tests/test_migration_dialects.py` in `backend-api/backend` |
| Icon | `add-an-icon.md`: edit `frontend/public/assets/icons/sprite.svg`, run `npm run update-icons` and `npm run typecheck` in `frontend` |
| Documentation page | `write-docs.md`: in `website`, `npm run reference` once, then `npm start` and open `http://localhost:3100` |
| Development stack | `run-the-development-stack.md`: start the native API, worker and Vite server |

Change the `widgets.json` contract (`change-the-widgets-contract.md`):

1. Edit `frontend/src/lib/types/widgetsContract.ts`, then in `frontend` write the kit and confirm its test passes:
   ```bash
   node scripts/generate-widgets-schema.ts
   npx vitest run tests/unit/lib/types/widgetsSchemaKit.test.ts
   ```
2. In `backend-api/backend`, rewrite the web app's fixture and the app-builder pages, which also rewrites `agent/mcp-server/src/resources/app-builder`. Pass the `env` block of `pytest.ini`, because the scripts load the settings:
   ```bash
   env $(sed -n 's/^    \([A-Z_]*=.*\)$/\1/p' pytest.ini) poetry run python -m scripts.compose_widgets_schema --plugin test_chart=tests/fixtures/test_chart_definition.json --settings test_chart=tests/fixtures/test_chart_settings.json --id fixture > ../../frontend/tests/mocks/widgets-schema.json
   env $(sed -n 's/^    \([A-Z_]*=.*\)$/\1/p' pytest.ini) poetry run python -m scripts.generate_app_builder_specs
   poetry run pytest tests/test_widgets_schema.py tests/test_app_builder_specs.py -q
   ```
3. Confirm `generate_app_builder_specs` prints `wrote <n> page(s)`, and with `--check` prints `current`. Then regenerate the reference data.

Regenerate the reference data (`regenerate-reference-data.md`):

1. In `website`, write the data of the backend, `agent/` and `frontend/`, then the site's data. `npm run reference` runs the native Python and Node exporters and replaces `node_modules` in `agent` and `frontend`. Confirm `backend-api/backend/reference-data`, `agent/reference-data` and `frontend/reference-data` exist afterwards:
   ```bash
   npm ci --ignore-scripts
   npm run reference
   npm run generate
   ```
2. After a deliberate change to the tools, resources or prompts of the Workspace MCP server, rewrite `backend-api/backend/tests/fixtures/workspace_mcp_sidecar_surface.json` from `backend-api/backend` with the same `pytest.ini` settings as the native backend exporter. Run `python -m scripts.export_workspace_mcp_surface` and commit the fixture.

## 7. Update NOTICE; leave the SBOMs alone

- Record the licence chosen for a new or upgraded dual-licensed dependency under "Dual-Licensed Dependency Selections" in `NOTICE`, and a dependency whose package metadata states no licence under "Licences Not Stated in Package Metadata", with the licence of its LICENSE file. Any other attribution that a dependency's licence requires also goes in `NOTICE`.
- Never edit `sbom/`. Use the current lockfiles for dependency audits.

## 8. Commit with a sign-off

1. Set `git config --global user.name "<your-name>"` and `git config --global user.email "<your-email>"` once. The email must be a public email of the GitHub account.
2. Stage only the files of the change, then commit with `-s`, which adds the committer's own `Signed-off-by`. Add no other trailer lines:
   ```bash
   git status --short
   git add <paths>
   git commit -s -m "<imperative summary>"
   ```
3. Confirm every commit carries exactly one trailer, `Signed-off-by: <your-name> <your-email>`, equal to its author:
   ```bash
   git log --format='%h %an <%ae>%n%(trailers)' origin/main..HEAD
   ```

- Keep commits small and cohesive; put separate contributions in separate commits, ideally separate pull requests. No unrelated whitespace or formatting changes, and no code comments (the Rules section of `AGENTS.md`).
- Never stage `.env` files, `user_create.json`, `backend-api/backend/scripts/cfgs/config.toml`, `local_storage/`, `widget-plugins/`, `reference-data/` or secrets. Git does not ignore `frontend/.env`.

## 9. Fix a failing DCO check

1. List the commits of the branch with their trailers, as in step 8.3, and find the ones without a correct `Signed-off-by`.
2. For the last commit only, run `git commit --amend -s --no-edit`. For several, run `git fetch origin && git rebase -i --signoff origin/main` and save the list unchanged; to drop another trailer, mark that commit `reword` and delete the line.
3. Rewrite the branch on GitHub with `git push --force-with-lease`, then confirm `gh pr checks <pr-number>` shows the DCO check passing.

## 10. Push and open the pull request

1. Before the first push, rebase onto the latest `main` so the pull request merges cleanly: `git fetch origin && git rebase origin/main`.
2. Push: `git push -u origin feature/<short-name>`.
3. Write `<body-file>`: what changed and why, the issue, the checks run, and the checklist of `.github/PULL_REQUEST_TEMPLATE.md`:
   ```markdown
   <what changed and why>

   Issue: #<issue-number>. Checks run: <commands>.

   - [x] I have read the [CONTRIBUTING.md](./CONTRIBUTING.md) file.
   - [x] My commit messages are signed off with the `Signed-off-by` statement (use `--signoff` in the commit).

   By submitting this pull request, I certify that I have read and agree to the terms of the [Developer Certificate of Origin](https://developercertificate.org/).
   ```
4. Open it against `main`. `gh` prints the pull request URL:
   ```bash
   gh pr create --base main --title "<summary>" --body-file <body-file>
   ```
5. Watch the checks with `gh pr checks <pr-number> --watch`, and list the ones that gate the merge with `gh pr checks <pr-number> --required`.
6. Request a review from a Maintainer in `MAINTAINERS.md` other than the author: `gh pr edit <pr-number> --add-reviewer <github-username>`.

## 11. Review and merge rules

| Rule | Source in `CONTRIBUTING.md` |
|---|---|
| Every contribution, a Maintainer's included, goes in as a pull request. | Contribution Rules |
| A Maintainer other than the contributor should review it. A non-trivial one should stay open long enough for every Maintainer to review it; then, with no Maintainer objecting, any Maintainer may merge it. On an objection, the Maintainers seek consensus, and any Maintainer may call a vote; the TSC decides contested pull requests. | same, and TSC Voting |
| A pull request with an unsigned commit is not merged; one that does not merge cleanly is unlikely to be accepted. | DCO, Contribution Guidelines |
| A change to the Maintainers or the TSC Chair in `MAINTAINERS.md` needs a TSC majority vote before the merge, the vote documented in or linked from the pull request, and an email to help@finos.org. | Maintainer and TSC Chair Changes |
