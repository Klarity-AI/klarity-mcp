---
name: klarity-agent-builder-objective
description: Set up a new automation project by capturing the things the data cannot tell us: the outcome the user wants, what kind of value matters, where to focus, which tools are allowed, what is off-limits, and who owns it. Writes project.md and manifest.md. Use when the user says "start a project," "set an objective," "new engagement," or when no project exists for the workspace.
---

# Objective

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="objective")`.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.
