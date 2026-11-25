---
name: apex-service-change
description: Use for ApexTerminal API contracts, authorization, migrations, distributed state, cache, or operational changes.
---

- Trace the entry point through its permission check, data ownership, persistence and response. Record the affected request and response fields in OpenSpec. Preserve old clients and rows through a staged migration when required.
- Threat-model actor, asset and trust boundary. Derive identity server-side, test tenant and role boundaries, and bound requests and retries. Avoid sensitive values in logs, metrics labels and trace attributes.
- Decide the idempotency key, transaction boundary, invalidation policy and recovery path before changing a retried workflow. Check failure between writes and after network timeout.
- Use the repository's [migration guide](../../../docs/tutorials/contribute/add-a-database-migration.md) for schema changes. Record rollout order, rollback limits and observable success criteria in the OpenSpec design.
- Verify local lint and types, the affected error paths and any requested integration checks. Use structured outcomes and bounded trace attributes to diagnose latency. Report dependency findings with direct package ownership or a transitive path.
