# Examples backend

One backend serves the three example plugins, so that a single connection gives a dashboard every widget type and the widgets work on the same data. It is a native Starlette application with optional Postgres data. It answers for two plugin backends, the SQL explorer's and the AgGrid plugin's.

| Path | Answers | For |
|---|---|---|
| `/widgets.json` | The definitions of the widgets below. | The web app, which adds them as a connection. |
| `/plotly/sales`, `/plotly/trend`, `/plotly/signal`, `/plotly/correlation` | A Plotly figure, drawn in the template of the `theme` the app sends. `/plotly/sales?raw=true` answers with its rows. | The `plotly-charts` plugin. |
| `/ag-grid/explicit`, `records`, `columns`, `split`, `dates`, `grouped`, `multicolumn`, `stream` | One table in each of the shapes the `aggrid-table` type accepts. `stream` moves every five seconds, so the plugin applies the difference as a transaction. | The `ag-grid` plugin, widget *AgGrid table*. |
| `/ag-grid/live`, and the WebSocket `/ws/ticks` | The columns and a first snapshot of 24 instruments, and a socket that sends a `snapshot` and then `upsert` messages by row id, so the rows keep their order. | The `ag-grid` plugin, widget *AgGrid live grid*, type `aggrid-livegrid`. |
| `/ssrm/trades` | Nothing the widget reads: the widget of type `aggrid-ssrm` gets its rows from the plugin's own backend. | The `ag-grid` plugin, widget *AgGrid server-side table*. The plugin's *AgGrid SQL* widget needs no entry here: it is in Add widget on its own. |
| `/sql/chart` | The first column of the `sql` parameter's query as categories and the others as bars, as a Plotly figure. | The `plotly-charts` plugin. |
| `/.workspace/identity`, `/.workspace/health`, `/.workspace/routes/<route>` | The requests of a plugin backend. | The API, for the `sql-explorer` plugin. |
| `/plugins/ag-grid/.workspace/...` | The same requests for the `ag-grid` plugin, whose routes also page, sort, filter, group and pivot `demo.trades`. | The API, under the AgGrid path. |

## How the plugins work together

- The generated example files, `sales.csv`, `deals.csv`, `readings.parquet` and `stations.csv`, hold the data of the charts and grids. The SQL explorer's Files source, the *AgGrid SQL* widget and the *SQL chart* all read them with the same read-only DuckDB, so a query written in the explorer gives the same rows in the grid and in the chart.
- *AgGrid SQL* is a widget of the AgGrid plugin: the explorer's own editor, with its tables and its DuckDB completion, and the result in AgGrid in the same card, with the row group, pivot and column panels. *SQL chart* is a widget of type `plotly` that the Plotly plugin draws from `/sql/chart`.
- *Trades, server-side* shows `demo.trades`, 200,000 rows in the Postgres, through the AgGrid plugin's backend: every page, sort, filter, row group, aggregate and pivot is a query.
- *Live prices* declares `data.streamEndpoint: "/ws/ticks"`: the web app opens that WebSocket through the API, which connects to the example backend as it does for the widget's endpoint, and passes the messages to the AgGrid plugin. Nothing in the plugin's policy changes.
- The SQL explorer declares the parameter `sql` and writes it when a query on its Files source has run. Put the explorer and the *SQL chart* on one dashboard and add their `sql` parameters to one group (the link beside the parameter, then +): the editor with its completion is then the input of the chart.
- *Sales by region* has `raw` and `data.rawType: "aggrid-table"`, so the database button of its card shows its rows in the AgGrid plugin ([the widgets.json contract](../../reference/schemas/widgets-json.mdx)).

## Run locally

Build the [SQL explorer](../sql-explorer/README.md) and [AgGrid](../ag-grid/README.md) packages first. Set `SQL_EXPLORER_PACKAGE` and `AG_GRID_PACKAGE` to the absolute directories of the built versions. From this directory:

```bash
python3.14 -m venv .venv
.venv/bin/pip install --require-hashes -r requirements.txt
export SQL_EXPLORER_DATA="$PWD/.venv/example-data"
.venv/bin/python -c 'import os, data; data.write_files(os.environ["SQL_EXPLORER_DATA"])'
export PYTHONPATH="$SQL_EXPLORER_PACKAGE/backend:$AG_GRID_PACKAGE/backend"
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 7798
```

Add `http://127.0.0.1:7798` under Connections in the local workspace. The chart and file-backed grid examples use generated sample data. The Postgres-backed trade demo needs a separate local Postgres database seeded with the script in `postgres/`.

This example exposes its plugin RPC routes on loopback for development. Keep it private and use disposable data and credentials.

## Test

```bash
python3 -m venv .venv
```

```bash
.venv/bin/pip install -r requirements-test.txt
```

```bash
.venv/bin/python -m pytest -q tests
```

The tests exercise the native application with temporary data and plugin fixtures.
