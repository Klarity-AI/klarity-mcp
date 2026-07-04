---
name: klarity-agent-builder-home
description: Renders the Klarity home screen — a single-page HTML artifact showing lifecycle phase progress, current status, and next actions. Invoke when the user says "home," "status," "where am I," or at session start to orient.
---

# Home

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="home")` and follow it.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.

This step produces a visual HTML artifact; the fetched instructions include a Rendering section — follow it (fetch the template, inject data into the JSON data-islands, write the file, tell the user to open it).
