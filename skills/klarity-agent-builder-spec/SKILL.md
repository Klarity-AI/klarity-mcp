---
name: klarity-agent-builder-spec
description: Turn one approved non-skill recommendation into an implementation spec a customer's IT or engineering team can build from. Use when the user says "spec this," "write the build spec," "turn this into a build plan," or after propose hands off a build_candidate whose primitive is not a skill.
---

# Spec

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="spec")`.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.
