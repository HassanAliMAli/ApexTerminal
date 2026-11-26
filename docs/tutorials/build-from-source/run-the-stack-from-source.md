---
title: Run the stack from source
sidebar_position: 1
---

# Run the stack from source

Use Python 3.13, Node 26.12.1, MySQL 8 and Valkey. Provision a dedicated application database, a database account scoped to it, and a cache instance on loopback. The database account needs schema privileges on the application database for migrations. Keep the database and cache listeners private.

## Configure the backend

From `backend-api/backend`, create a Python 3.13 virtual environment and install the locked backend dependencies with Poetry. Run the following with that environment active:

```bash
python -m pip install --require-hashes -r poetry-requirements.txt
poetry install --only main
```

Create `envs/.env` from `envs/.env.example` if it does not already exist, and restrict file access to your account. Set the following values before running migrations:

- `DB_HOST`, `DB_PORT`, `DB_NAME`, and the read and write database credentials for the dedicated database.
- `REDIS_HOST`, `REDIS_PORT`, and `REDIS_PASS` for Valkey.
- `APPURL` and `FRONTENDURL` to `http://127.0.0.1:1420`, `SELFURL` to `http://127.0.0.1:8000`, and `BACKEND_CORS_ORIGINS` to the exact frontend origin.
- Distinct random secrets for `JWT_SECRET`, `WORKSPACE_AES_KEY` and `LOCAL_STORAGE_SECRET_KEY`. Generate the AES key with `python -c 'import secrets; print(secrets.token_urlsafe(32))'`.
- `MODE=production` for a server other people can access. Keep the configuration private.

If `scripts/cfgs/config.toml` does not already exist, create administrator configuration with `python -m scripts.create_local_env --config-only --no-extra-admins --admin-email you@example.com`. Confirm the database points at the intended instance, then run:

```bash
python -m alembic upgrade head
python -m scripts.init_users
```

## Set the administrator password {#set-the-administrators-password}

Run `python -m scripts.init_users --new-password you@example.com` and enter the password when prompted.

## Start the services

Run these in separate terminals or under your process supervisor:

| Directory | Command |
|---|---|
| `backend-api/backend` | `python -m uvicorn main:app --host 127.0.0.1 --port 8000` |
| `backend-api/backend` | `python base_workers.py` |
| `frontend` | `npm ci --ignore-scripts`, then `VITE_BACKEND_URL=http://127.0.0.1:8000 npm exec -- vite --host 127.0.0.1` |

Check `curl -fsS http://127.0.0.1:8000/health`, then open `http://127.0.0.1:1420`. The commands bind to loopback. For access from another machine, serve the built frontend and API through your HTTPS reverse proxy and set the URLs and CORS origin to the actual published address.

## Build the docs

From `website`, run `npm ci --ignore-scripts`, `npm run reference`, and `npm run build`. If the backend virtual environment is not on PATH, set `BACKEND_PYTHON` to its absolute interpreter path before running the reference command.
