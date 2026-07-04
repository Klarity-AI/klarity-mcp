---
name: klarity-agent-builder-start
description: The front door. Two-door intent gate at session start. Invoke when the user says "start," "klarity start," "what can you do," "where do I begin," or opens a session with no active project and no explicit intent. Routes to the skill track (Build skills) or the explore path (Explore & decide).
---

# Start

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="start")` and follow it (the two-door gate).
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.
