---
name: apex-financial-data
description: Use for ApexTerminal changes to market data, timestamps, numeric calculations, or live streaming.
---

- Identify each input's source, instrument, currency, unit, precision, event time and freshness policy. Preserve venue and source timestamps separately from receipt time. Normalize storage timestamps to UTC and use venue calendars for market sessions.
- Confirm the API rounding contract and use explicit decimal or scaled integer arithmetic for exact values. Check negative values, zero, extremes and aggregation order. Round at the boundary named by the contract.
- Label live, delayed, simulated, stale and unavailable results. Keep historical revisions and provenance traceable. Confirm redistribution rights before exporting a feed or storing its data.
- Use sequence IDs or stable event keys for deduplication. Define how gaps and out-of-order events trigger replay or a fresh snapshot. Use capped reconnect backoff with jitter and honor upstream rate limits.
- Verify unit conversions, time changes, stale state, reconnect, duplicate and gap recovery with deterministic fixtures. Evaluate sustained update throughput and render lag locally. Keep financial APIs read-only until write access is explicitly authorized.
