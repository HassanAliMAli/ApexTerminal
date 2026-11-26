# FINOS Workspace documentation site

This website was created with Docusaurus 3, and it renders the pages in `docs/`.

- `website/` holds the Node and React code that builds the site.
- `website/docusaurus.config.ts` holds the Docusaurus configuration.
- `website/static/` holds images and other static assets, which the site serves from its root.
- `docs/` holds the Markdown and MDX pages. Their folders and file names give the pages their addresses.

## Local run

The site needs Node 26.12.1 and a Python 3.13 environment with the locked backend dependencies installed. Set `BACKEND_PYTHON` to the absolute path of that environment's Python executable if it is outside your PATH.

```bash
cd website
npm ci --ignore-scripts
npm run reference
npm start
```

The reference pages are generated from data that the backend, the agent and the web app write. Git does not track that data, and `npm run reference` writes it. For the backend, it runs the Python exporter in the backend directory with the reference settings from `pytest.ini`. For the agent and the web app, it runs `npm ci` in `agent` and in `frontend`, which replaces their `node_modules`. The page *How to regenerate the reference data* describes each part. `npm start` serves the site at `http://localhost:3100`, a port that the local stack does not use, so both can run at the same time. Run `npm run typecheck`, `npm test` and `npm run build` before you push. The build fails on a broken link or anchor.

The bundler writes the files that it reads into a folder that it generates, and those files hold the absolute paths of the machine that wrote them, so a run that reads the files of another run cannot resolve them and every page fails to compile. The site therefore keeps the files of the development server in `website/.docusaurus-dev` and the files of the build in `website/.docusaurus`, and the build removes its own folder before it starts.

## Docs CI

The Docs workflow in `.github/workflows/docs.yml` generates reference data, checks types, runs site tests, builds the site and validates `llms.txt` and the table of contents. Run `npm run serve` to preview the built site locally.

## Website dependency updates

The file `osv-scanner.toml` excludes the website's dependencies from OSV scans, because the website is never shipped to users. Delete the file to include them, which FINOS does not recommend. Docusaurus patches often arrive weeks or months after the vulnerable dependencies are found, so automated tools such as Dependabot cannot fix them quickly.
