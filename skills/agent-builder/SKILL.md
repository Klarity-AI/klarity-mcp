---
name: agent-builder
description: Entry point for turning how your organization works into skills, agents, and automations. Invoke before responding when the user mentions processes, automation, agents, skills, or building something from how their team works.
---

# Agent Builder

This is the entry point for all Within agent-building work. The methodology is served from the Within MCP — do not improvise it. Fetch it and follow it.

1. Call `get_agent_builder_instructions` and follow what it returns before doing any other agent-building work. It self-guides from there.
2. The returned instructions may reference supporting resources. When the current work needs one, call `get_agent_builder_resource` to fetch it and use the returned content.
3. Write all durable outputs to the local project directory as the instructions specify. The tools are read-only and serve methodology only; the client owns project state.

See `tools.md` for the two tools.
