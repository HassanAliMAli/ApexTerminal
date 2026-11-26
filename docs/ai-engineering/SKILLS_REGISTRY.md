# Shared skills

| Skill | Canonical source | Load when |
|---|---|---|
| OpenSpec core workflows | `.agents/skills/openspec*` | Propose, explore, apply, update, sync or archive a substantial change |
| Apex financial data | `.agents/skills/apex-financial-data` | Market data, decimal precision, provenance, market sessions or streaming |
| Apex frontend review | `.agents/skills/apex-frontend-review` | UI, design-system reuse, accessibility, charts or rendering performance |
| Apex service change | `.agents/skills/apex-service-change` | API design, authorization, migrations, caching, distributed state or operations |
| Superpowers verification before completion and receiving code review | `~/.local/share/apex-ai/superpowers-7.0.2` | Confirm evidence before completion or evaluate review findings |

Both agents have documented discovery for the shared `.agents/skills` convention. Workstation Superpowers entries link from `~/.agents/skills`. The two selected skills are instruction files. Upstream bootstrap hooks and plugin integration remain separate. OpenSpec owns the durable artifacts, and the [agent workflow](AGENT_WORKFLOW.md) connects methodology to those artifacts.

Project-specific install, administration, deployment, plugin and contribution playbooks already live alongside these skills. Leave them scoped to their documented workflows.
