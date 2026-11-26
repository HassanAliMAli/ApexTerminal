---
title: Write and preview documentation
sidebar_position: 5
---

# Write and preview documentation

The documentation site is built with Docusaurus. Its pages are Markdown files in `docs/`, in one folder for each kind of page, and the site that renders them lives in `website/`. This guide explains where a new page belongs, how to write it, and how to preview and check the site before you push.

## Choose the folder

Put each page in the one folder that matches its job. A page that tries to do two jobs should become two pages that link to each other.

| Folder | Who reads it | How the title starts | What to leave out |
|---|---|---|---|
| `features/` | A reader who wants to know what a feature does and how to use it. | A short action, such as "Share a dashboard". | Architecture and background. Link to the concept instead. |
| `concepts/` | A reader who wants to understand how something works. | A noun phrase, or "How …" for a process, such as "How theming works". | Steps and exhaustive lists. |
| `tutorials/` | A reader who wants to get something done, step by step. | A short action, such as "Deploy on Kubernetes". | Background and every option. Link to the concept and the reference instead. |
| `reference/` | A reader who needs a fact. | A noun phrase, such as "Plugin proxies and secrets". | Instructions, explanation and opinions. |

Do not start a title with "How to" or "About". The sidebar already says which kind of page it lists.

## Write the page

1. Create `docs/<folder>/<name>.md` with a `title` in its front matter. A page that shows generated values is an `.mdx` page instead, and it imports the components from `@site/src/components/Reference`. Pages that belong together live in a subfolder with a `_category_.json` that gives the sidebar label and position.
2. Write in complete sentences, and keep them short. Begin the page with one sentence that says what the page covers, or what the reader will have at the end. That first sentence is also the page's description in `llms.txt`, as [How CI builds the site](#how-ci-builds-the-site) explains. In a tutorial, number the steps, and give each step one action, the code or the menu path for it, and what the reader should see afterwards.
3. Check every statement against the code before you write it. Name files and functions, and never line numbers.
4. Write marked placeholders such as `<your-email>` and `<API_URL>` where the reader has to choose a value. Do not invent hosts, accounts or companies.
5. Do not write a number, a limit, a name or a list of values that the code defines. A page takes it from a generated component, such as `PluginValue`, `SettingDefault`, `SettingConstant`, `EnvDefault`, `AgentLimit`, `WebAppValue`, `BridgeValue` or `MetricName`, and the build fails when the value does not exist. A component that prints a quantity takes a `unit`, which is `bytes`, `ms`, `s`, `min`, `hours`, `days` or `raw` and says how the stored value is written. Where a page has to explain a part by hand, the generator checks that the page mentions every item of the code, as [Regenerate the reference data](regenerate-reference-data.md) describes.
6. Link to the reference and explanation pages instead of repeating them. Put angle brackets and curly braces inside code spans, because the MDX parser reads them as markup otherwise, and write web addresses as ordinary Markdown links.

## Preview the site

The site needs Node 26.12.1, the version that the repository's images run, and Docker. The reference pages are generated from data that the backend, the agent and the web app write, and git does not track it, so write the data once, as [Regenerate the reference data](regenerate-reference-data.md) describes. Then install the site's dependencies and start the development server:

```bash
cd website
npm ci --ignore-scripts
npm run reference
npm start
```

The development server listens on port 3100, so it runs next to the local stack, whose web app uses port 3000. Open it at `http://localhost:3100`. The command `npm run serve`, which serves the built site, uses the same port.

## Check before you push

Run the type check, the tests of the site's code and the build:

```bash
npm run typecheck
npm test
npm run build
```

The build fails on a broken link, a broken anchor or a page that no sidebar lists, so a build that passes has no dead links inside the site and lists every page in `llms.txt`. Run `npm run serve` after the build to open the built site, which includes `llms.txt`.

## How CI builds the site

The Docs workflow in `.github/workflows/docs.yml` runs for pull requests, merge queue checks, and pushes to `main` that touch the docs, the site, or their reference data sources.

1. Three jobs generate reference data from the backend, the agent and the web app.
2. The build job generates the site data, checks types, runs site tests, builds the site and checks `llms.txt` and the table of contents.

The build also writes `llms.txt` at the root of the site. It is the plain-text index that language models and the tools that feed them read to find pages. The file starts with the site's name and tagline, and then it lists every page under the headings of the navigation bar and the sidebar categories, each with its title, its address and a description. The description is the `description` in the page's front matter when the page has one, and otherwise the first sentence of the rendered page, so the file shows the values that the generated components print. Only the build writes the file, and it fails when a sidebar names a page that does not exist, when a page is listed twice or when a page is in no sidebar.

The file `website/osv-scanner.toml` leaves the site's dependencies out of vulnerability scans, because the site is never shipped to users.
