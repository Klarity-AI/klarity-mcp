---
name: agent-builder
description: Entry point for all Klarity agent-building work. Guides you from "what should we automate?" through scoping, diagnosis, and a plan to a shipped skill or developer-ready spec. The methodology is served from the Klarity Architect MCP — invoke before any response when the user mentions processes, automation, agents, or ops intelligence.
---

# Agent Builder

This is the single entry point for all Klarity agent-building work. The methodology is served from the Klarity Architect MCP — do not improvise it. Fetch it before doing anything else, and let it route you through the rest of the lifecycle.

1. FIRST, call `get_agent_builder_instructions(step="begin")` and follow it before any other agent-building work. Workspace resolution, the lifecycle model, the two-door gate, and the next-step routing all come from that call.
2. Follow the returned `instructions` exactly. They include a **resource manifest** — references, primitives, and templates the step may draw on.
3. For each manifest entry the current work needs, call `get_agent_builder_resource(type=..., subtype=...)` and use the returned content. Fetch on demand — the manifest is a relevance hint, not a required read.
4. Move through the lifecycle by following each step's prose. There is no `next` field; `begin` routes you to the entry step and each step's instructions say what runs next. Fetch each step (`objective`, `current_state`, `diagnose`, `propose`, `spec`, or the skill track: `skill_track` → `skill_discovery` → `skill_outline` → `skill_build`) as you reach it.
5. Write all durable outputs to the local project directory as the instructions specify. The tools are read-only — they only serve methodology; the client owns project state.

See `tools.md` for the full tool catalog and the lifecycle step list.
