---
title: Run the development stack
sidebar_position: 1
---

# Run the development stack

Follow [Run the stack from source](../build-from-source/run-the-stack-from-source.md) to configure a development database and cache, initialize the administrator, and start the API, worker, and web app. Keep development processes on loopback.

For API hot reload, add `--reload` to the Uvicorn command. Vite refreshes the web app when frontend files change. Restart the worker when changing Python code it imports. Apply migrations with `python -m alembic upgrade head` when the migration chain changes.

Set `WIDGET_PLUGINS_DIR` to an absolute path to the local plugin packages if you are developing plugins. [Deploy a widget plugin](../plugins/deploy-a-plugin.md) describes the expected directory structure.
