# Copilot agent rules

Read [Copilot agent rules](../docs/ai-engineering/COPILOT_AGENT_RULES.md) before changing this directory. The guide retains the protocol and multi-user requirements. Commands, architecture and tool inventory are in [README.md](README.md).

- Keep the harness thin. Route structurally by tool source. The Workspace owns MCP connections. Preserve one stream per iteration, the SSE round-trip contract, and continuation state across re-POSTs.
- Keep the current turn in model context. Recall earlier turns on demand. Advertise only registered tools and keep internal decoration under `x-agent-*`.
- Use strict, erasable TypeScript and Zod input schemas. Keep state-bound tools in the agent. Put stateless, heavy, or cold-start tools in the MCP server.
- Derive identity from the authenticated principal and scope persistent state by user and conversation. Verify signatures at the receiving boundary. Keep shared caches bounded and honor Workspace authorization decisions outside the model.
- Use the approved URL-fetch boundary and preserve output neutralization against unwanted requests. Keep logs free of conversations, files and credentials. Enforce input sizes, resource limits and subprocess deadlines for untrusted bytes.
- Run `npm run typecheck` and `npm test` with the repository's Node version. Check the detailed guide for the affected protocol before making changes.
