---
name: klarity-agent-builder-skill-outline
description: Load when the skill track has a chosen candidate card and needs the full plan expanded and approved before anything is built — the conductor invokes this after Gate 1 with the chosen card plus its internal context. Produces a user-facing outline (the Gate 2 artifact) plus a machine-readable technical spec. Needs web search to verify current integration install paths. NOT for discovering candidate cards (that is skill-discovery), NOT for the critic pass, NOT for shipping the final bundle (that is skill-build), NOT for general automation opportunities (that is diagnose/propose).
---

# Skill outline

This step of the Klarity agent-building lifecycle is served from the Klarity Architect MCP. Do not improvise the methodology — fetch it.

1. Call `get_agent_builder_instructions(step="skill_outline")`.
2. Follow the returned instructions exactly. They include a **resource manifest** — a list of references/primitives/templates this step needs.
3. For each manifest entry, call `get_agent_builder_resource(type=..., key=...)` and use the returned content. Fetch on demand; do not skip.
4. Write outputs to the project directory as the instructions specify.
