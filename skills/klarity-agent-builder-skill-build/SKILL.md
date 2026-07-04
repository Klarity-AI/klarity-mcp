---
name: klarity-agent-builder-skill-build
description: Load when the skill track has an approved outline and needs the final installable bundle produced — the conductor invokes this after Gate 2 (utterances that reach it: "build it", "generate the bundle", "ship this skill", "make the install steps"). Emits the hub-and-spoke skill bundle, a web-verified install wizard, and a first-run smoke test drawn from the team's real evidence. Needs web search to verify the current install UI against vendor docs. NOT for discovering candidates (that is skill-discovery), NOT for drafting or approving the outline (that is skill-outline), and NOT for any generic non-skill build (there is intentionally no generic build skill).
---

# Skill build

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="skill_build")`.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.
