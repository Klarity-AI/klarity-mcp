---
name: klarity-agent-builder-diagnose
description: Turn the project objective and the validated current-state baseline into a set of evidence-backed, scored opportunities. Generates hypotheses against the objective, investigates each one with parallel subagents, scores them on transparent evidence-based axes, and writes a findings report. Runs after current-state. Use when the user says "diagnose," "find opportunities," or "what should we automate."
---

# Diagnose

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="diagnose")`.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.
