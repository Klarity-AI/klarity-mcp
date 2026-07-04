---
name: klarity-agent-builder-using-klarity
description: Entry point for all Klarity work. Establishes the lifecycle, MCP connection, and skill routing. Invoke before any response when the user mentions processes, automation, agents, or ops intelligence.
---

# Using Klarity

This is the entry point for all Klarity agent-building work. The methodology is served from the Klarity Architect MCP — do not improvise it. Fetch it before doing anything else.

1. FIRST, call `get_agent_builder_instructions(step="begin")` and follow it before any other agent-building work. Workspace resolution, the lifecycle model, the two-door gate, and the next-step handoff all come from that call.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.
