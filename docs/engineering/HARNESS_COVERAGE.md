# Phase 0 harness coverage

The original engineering harness brief defined the Superpowers workflows and 33 broad skills domains. The follow-up brief specified the specialist responsibilities and project-specific skills. This crosswalk uses one architecture responsibility for architecture, technical leadership, and task orchestration. It groups professional UI/UX with preventing generic interfaces, and Git with release verification. The resulting 15 responsibilities and 36 areas retain each named topic.

## Specialist routing

Both assistants use the role names below. The [routing guide](../ai-engineering/AGENT_WORKFLOW.md#specialist-routing) describes permissions and handoff. The [audit](HARNESS_AUDIT.md#assistants-and-project-context) records native discovery, Codex delegation to a reviewer, and OpenCode delegation on a synthetic project. Live OpenCode delegation on ApexTerminal requires an authorized model and data boundary.

| Responsibility | Primary role | Scope |
|---|---|---|
| Architecture, technical leadership, task orchestration | `apex-architecture` | Contracts, options, dependencies, sequencing |
| Frontend engineering | `apex-frontend` | React, TypeScript, interactions |
| Backend engineering | `apex-service` | FastAPI and API contracts |
| Database engineering | `apex-service` | SQLAlchemy, persistence, migrations |
| DevOps engineering | `apex-operations` | Native runtime, CI, deployment |
| Financial charting | `apex-quant` | Market-data semantics and chart checks |
| Canvas/WebGL | `apex-quant` | Rendering budgets and chart correctness |
| Quantitative engineering | `apex-quant` | Numerical precision and financial calculations |
| Security | `apex-review` | Authorization, boundaries, regression risk |
| Performance | `apex-quality` | Measurable time, throughput, and rendering budgets |
| QA | `apex-quality` | Acceptance criteria, fixtures, verification |
| Independent code review | `apex-review` | Scoped findings on the supplied revision |
| Professional UI/UX | `apex-design` | Hierarchy, usability, responsiveness |
| Systematic debugging | `apex-debug` | Reproduction and verified causes |
| Documentation | `apex-documentation` | Verified docs and handoff records |

## Shared skill areas

Use the [skills registry](../ai-engineering/SKILLS_REGISTRY.md) and load only the relevant procedure. A source or procedure in this crosswalk establishes written coverage. Actual discovery, tool and application verification remain subject to the evidence in the [audit](HARNESS_AUDIT.md).

| Area | Procedure and verification |
|---|---|
| Architecture | Use OpenSpec to trace contracts and dependencies. Record alternatives, tradeoffs, rollout, and rollback. Review the design against measurable acceptance scenarios. |
| Repository exploration | Start from the entry point. Use Serena for definitions and references, then ast-grep for structural matches. Confirm the target against a bounded read of the owning source. |
| Test-driven development | Reproduce the missing behavior with a focused test. Confirm it fails for the intended reason. Implement the smallest fix, then run related tests with the focused test. |
| Systematic debugging | Capture a minimal reproduction and record configuration and versions. Measure the failing path, test one hypothesis at a time, and confirm the fix with the original reproduction. |
| Code review | Supply a scoped revision and acceptance criteria. Require independent findings with impact, references, and evidence. Verify review feedback before implementing it. |
| Safe refactoring | Identify call sites, entry points and persisted inputs. Characterize current behavior with targeted checks before changing structure. Use the same checks after the change and inspect the diff for contract drift. |
| OHLCV validation | Validate timestamp units and order, duplicates, finite prices, candle high/low bounds, and nonnegative volume when required by the source contract. Verify invalid, partial, and missing bars with deterministic fixtures. |
| Financial mathematics | Define input units, conventions, and expected results from a reference case. Check sign, zero, extremes, and aggregation order using the financial-data skill. |
| Indicators | Specify window alignment, warm-up, missing-value policy, and whether incomplete bars enter calculations. Compare to deterministic values and check incremental updates against recomputation. |
| Time-series processing | Preserve event and receipt timestamps. Define ordering, interval boundaries, late events, gap handling, and resampling. Test both historical and live updates. |
| Trading calendars | Use the instrument venue's calendar with UTC storage. Exercise market closures, daylight-saving transitions, and short sessions with fixed fixtures. |
| Numerical precision | Apply the contract's decimal or scaled representation and rounding boundary. Verify precision at ingress, arithmetic, aggregation and egress. |
| Professional UI/UX and preventing generic interfaces | Prioritize the user's task, meaningful hierarchy, dense-data readability and genuine loading, empty and error states. Review a screenshot and a completed interaction against adjacent product patterns. |
| Canvas/WebGL | Check resize and device pixel ratio, frame time at representative density, and memory or resource disposal. For WebGL, verify context-loss recovery where supported. Provide a keyboard-accessible or text alternative for chart information. |
| Design systems | Inspect and reuse adjacent frontend components, tokens and interactions. Compare responsive and interactive states in representative stories or pages. |
| Responsive layouts | Exercise narrow and wide viewports, wrapping, overflow, navigation and focus recovery. Verify resizing a dense table or chart. |
| Accessibility | Combine axe with keyboard interaction, visible focus, accessible names, and chart alternatives. Verify the actual flow and review issues the automated checker cannot assess. |
| Rendering optimization | Measure updates and input latency on representative data. Profile expensive work and validate gains against the original workload and a correctness check. |
| FastAPI | Follow the service-change skill. Trace route validation, dependencies, authorization, and error responses. Exercise success, invalid input, and unauthorized cases. |
| SQLAlchemy | Trace session lifetime, ownership filters and transaction boundaries. Test rollback and concurrent writes where applicable, with existing records as well as new ones. |
| Migrations | Use the repository migration guide. Verify supported dialects and an upgrade from existing data. Record rollout order and realistic rollback constraints. |
| Asynchronous concurrency | Identify ownership and cancellation boundaries. Exercise timeout, retry, cancellation, overlapping operations, and failure after partial work. |
| API contracts | Record input and output changes in OpenSpec, then verify SDK or frontend consumers and compatibility with existing clients. |
| Caching | Define scope, expiry, invalidation and failure behavior. Test stale entries, tenant isolation, retry and recovery when the cache is unavailable. |
| WebSockets | Verify authorization and message bounds, reconnect backoff, expiry, replay, duplicate events, and gap recovery. Exercise a disconnection and reconnect on authorized local data. |
| Browser testing | Use isolated Playwright contexts and authorized fixtures. Assert an actual interaction and observable result, then inspect failures and browser errors. |
| Property-based testing | Use fast-check or Hypothesis with domain invariants and bounded generators. Record a reproducible seed or minimized counterexample. |
| Regression testing | Retain the failing input or scenario, verify the failure on the affected revision and the pass after the fix, then run adjacent checks. |
| Performance testing | Define the workload, dataset size, concurrency and measured threshold. Run k6 only against an authorized local or staging target and report latency, throughput and errors. |
| Visual testing | Capture deterministic loading, error and data states at representative sizes. Check layout and visible differences with stable data, fonts and animation state. Keep review artifacts free of credentials and personal data. |
| Acceptance testing | Map each criterion to a command or end-to-end observation. Record its result, revision and environment. Mark unrun cases with their actual reason. |
| Threat modeling | Use the service-change skill to identify actors, assets, trust boundaries, misuse paths and mitigations. Verify server-side authorization and tenant separation. |
| Dependency auditing | Resolve direct and transitive ownership from the lockfile. Check dated advisory data, identify a compatible fix, compare the exact lock diff, then repeat the scan and affected tests. |
| Secret management | Use redacted staged and history scans. Limit credentials to authorized scopes and private configuration, and verify that new values cannot appear in logs, reports or Git. |
| Native Linux deployment | Use the native install and deployment playbooks. Verify versions, service ownership, isolated startup, application health, restart state and shutdown. Use remote checks only with authorization. |
| Git and release verification | Follow the contribution playbook and project branch rules. Inspect the exact diff and applicable CI results, sign off authorized commits, and verify the intended revision before an authorized merge or release. |

The earlier brief's broad domains reuse these routes. Enterprise software engineering and requirements engineering use OpenSpec, contract scenarios and the shared workflow. Distributed systems and authentication use service change, concurrency, caching, streaming and threat modeling. DevOps, CI/CD and production readiness use native deployment, release verification and hosted checks. Observability uses bounded traces and structured outcomes from the service-change skill, with the telemetry fixture and limits recorded in the audit. Technical documentation uses the OpenSpec evidence record and the documented handoff.

## Superpowers workflows

The workstation has the two pinned instruction-only skills recorded in the [tool registry](../ai-engineering/TOOL_REGISTRY.md). The equivalent repository workflows below use the shared change record and keep planning artifacts in OpenSpec.

| Original workflow | Current mechanism | Verification |
|---|---|---|
| Requirements clarification | OpenSpec explore and propose | Prior OpenSpec fixture passed creation, status and validation. Specific Superpowers activation remains unverified. |
| Brainstorming | OpenSpec explore with alternatives and tradeoffs | Shared procedure available. Specific Superpowers activation remains unverified. |
| Architecture planning | OpenSpec design and architecture specialist | Design artifact and specialist discovery observed. Specific Superpowers activation remains unverified. |
| Implementation planning | OpenSpec tasks and apply | Active tasks and validation observed. Specific Superpowers activation remains unverified. |
| Test-driven development | Focused reproduction, then targeted verification | Shared procedure available. Specific Superpowers activation remains unverified. |
| Subagent-driven development | Native task-scoped specialist delegation | Codex real-checkout reviewer and OpenCode synthetic reviewer observed. OpenCode real-checkout run remains subject to provider and data authorization. |
| Systematic debugging | Debug specialist and measured root-cause analysis | Shared procedure and specialist definition available. Specific Superpowers activation remains unverified. |
| Independent code review | Reviewer role and installed `receiving-code-review` | Prior Codex review observed. The pinned workflow file resolves. On-demand activation in both clients remains unverified. |
| Verification before completion | Installed `verification-before-completion` | Codex usage recorded. On-demand OpenCode activation remains unverified. |
| Git worktree isolation | Native Git worktrees and scoped handoff | Shared procedure available. Specific Superpowers activation remains unverified. |

The full upstream Superpowers plugin and hooks were outside the installed two-skill scope. They remain unverified. Equivalent workflow coverage does not establish native activation of an upstream skill.
