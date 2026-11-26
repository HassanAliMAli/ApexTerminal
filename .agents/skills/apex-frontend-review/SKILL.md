---
name: apex-frontend-review
description: Use when implementing or reviewing ApexTerminal tables, charts, navigation, forms, layout, or other accessible React UI.
---

- Inspect adjacent components, tokens and stories. Reuse the app's table, chart and filter behaviors. Design around the primary decision or action and include loading, empty, error and disconnected states where the data can enter them.
- For dense data, preserve meaningful headings, units and visible focus. Verify scroll and resize behavior at a narrow and wide viewport. Measure rendering on representative row counts before adding virtualization.
- Use an isolated Playwright context and a representative fixture. Inspect screenshots, console errors and failed network requests. Check names, keyboard navigation, focus recovery and chart text alternatives alongside axe.
- See [frontend checks](../../../frontend/TESTING.md) and the [engineering setup](../../../docs/ai-engineering/AI_ENGINEERING_SETUP.md).
