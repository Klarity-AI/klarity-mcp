---
name: klarity-agent-builder-propose
description: Fitness-check a candidate, extract pain points, match tools, and produce an interactive HTML recommendation artifact. Use when the user says "propose," "spec this out," "what should the agent do," or "recommend for X."
---

# Propose

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="propose")`.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.

This step produces a visual HTML artifact; the fetched instructions include a Rendering section — follow it (fetch the template, inject data into the JSON data-islands, write the file, tell the user to open it).
