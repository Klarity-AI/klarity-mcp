---
name: klarity-agent-builder-skill-discovery
description: Load when the skill track needs candidate skill cards discovered from a team's workspace evidence — utterances reach it through the conductor, not directly (the track has already set the scope, the runner, and the approved systems). Reads processes, observations, and activity timelines, then surfaces a small set of plain-language candidate cards for the user to triage. NOT for expanding a chosen card into a plan (that is skill-outline), NOT for building the final bundle (that is skill-build), and NOT for general automation opportunities across the org (that is diagnose).
---

# Skill discovery

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="skill_discovery")`.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.
