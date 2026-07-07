# Agent Builder — Tools

Two read-only MCP tools drive Klarity agent-building work. They serve
methodology from the Klarity Architect MCP; they never mutate workspace state.
No methodology ships in this skill — fetch it at runtime instead of improvising
it.

| Tool | What it does |
|---|---|
| `get_agent_builder_instructions` | Fetches the instructions relevant to the Agent Builder process. Call this first and follow what it returns — it self-guides from there. |
| `get_agent_builder_resource` | Fetches a resource used while building. Call it when the current instructions reference a resource the work needs. |

The client writes all durable outputs to the local project directory.
