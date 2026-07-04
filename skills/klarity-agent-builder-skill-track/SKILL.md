---
name: klarity-agent-builder-skill-track
description: Conductor for the skill track — turns how a team already works into a reusable, installable skill. Use when the user says "build skills," "make a skill for my team," "turn this process into a skill," or arrives from the start gate's "Build skills" door. NOT for finding general automation opportunities (that is diagnose), NOT for spec'ing an agent or automation (that is propose), NOT for expanding or building a single bundle directly (the stage skills skill-discovery, skill-outline, and skill-build do that under this conductor).
---

# Skill track

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="skill_track")`.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.

This skill is the client-side CONDUCTOR: it fetches its step instructions but runs the gates and durable project-directory I/O on the client. The tool returns the instructions; this skill runs the loop.
