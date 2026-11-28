# Shared skills

| Skill | Canonical source | Load when |
|---|---|---|
| OpenSpec core workflows | `.agents/skills/openspec*` | Propose, explore, apply, update, sync or archive a substantial change |
| Apex financial data | `.agents/skills/apex-financial-data` | Market data, decimal precision, provenance, market sessions or streaming |
| Apex frontend review | `.agents/skills/apex-frontend-review` | UI, design-system reuse, accessibility, charts or rendering performance |
| Apex service change | `.agents/skills/apex-service-change` | API design, authorization, migrations, caching, distributed state or operations |
| Superpowers skill library | `~/.local/share/apex-ai/superpowers-7.0.2` | Brainstorming, planning, implementation, debugging, review, testing, and verification |

Both agents have documented discovery for the shared `.agents/skills` convention. All fifteen Superpowers skill directories link from `~/.agents/skills`. This installation exposes the skills through the native skill loader. OpenSpec owns the durable artifacts, and the [agent workflow](AGENT_WORKFLOW.md) connects methodology to those artifacts.

Project-specific install, administration, deployment, plugin and contribution playbooks already live alongside these skills. Leave them scoped to their documented workflows.
