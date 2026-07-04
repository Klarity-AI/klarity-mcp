---
name: klarity-agent-builder-current-state
description: Build and maintain an accurate, factual map of how work happens in a workspace, plus a customer-ready read-out. Pure factual capture, no opinions or recommendations. Reads the project scope, pulls process data from Klarity in parallel mini-phases, checks the data against reality, and writes a structured baseline plus an HTML report. Use after objective, or when the user says "current state," "map the workspace," "read-out," or "show me how the work runs."
---

# Current state

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="current_state")`.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.

This step produces a visual HTML artifact; the fetched instructions include a Rendering section — follow it (fetch the template, inject data into the JSON data-islands, write the file, tell the user to open it).
