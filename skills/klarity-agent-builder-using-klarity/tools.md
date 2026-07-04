# Klarity Agent Builder — Tool Catalog

This is the operational reference for the two MCP tools that drive the Klarity
agent-building lifecycle. **Both tools are read-only** — they serve
methodology (instructions, references, primitives, templates) from the Klarity
Architect MCP. They never mutate workspace state; all durable output is written
to the local project directory by the client.

The point of this catalog is not to enumerate APIs — it's to help an agent
**fetch the right methodology for the current lifecycle step** instead of
improvising it. No methodology ships in the skills; every step's instructions
and resources come from these two calls at runtime.

## How agents should think about the agent-building lifecycle

The Klarity agent-building lifecycle is a sequence of steps. Each step is a thin
client-side skill whose only job is to fetch its instructions from the MCP and
follow them. The instructions come back with a **resource manifest** — a list of
references, primitives, and templates the step needs — which the agent then
fetches on demand.

The steps (each a `step` value for `get_agent_builder_instructions`):

- `begin` — entry point; workspace resolution, lifecycle model, two-door gate,
  next-step handoff.
- `home` — renders the Klarity home screen HTML artifact (phase progress,
  status, next actions).
- `start` — the front-door two-door intent gate.
- `objective` — capture the outcome, value, focus, allowed/off-limits tools,
  owner. Writes project scope.
- `current_state` — factual map of how work happens, plus a customer-ready HTML
  read-out.
- `diagnose` — turn objective + baseline into scored, evidence-backed
  opportunities.
- `propose` — fitness-check a candidate and produce an interactive HTML
  recommendation.
- `spec` — turn an approved non-skill recommendation into an implementation
  spec.
- `skill_track` — client-side conductor for the skill track (runs gates +
  durable project-dir I/O on the client).
- `skill_discovery` — surface candidate skill cards from workspace evidence.
- `skill_outline` — expand a chosen card into an approved plan (Gate 2
  artifact) + technical spec.
- `skill_build` — emit the final installable skill bundle, install wizard, and
  smoke test.

---

## A. Standard entry points

The default entry path. Any agent starting Klarity agent-building work begins
here.

| Tool | When to use |
|---|---|
| `get_agent_builder_instructions` | First call for every lifecycle step. Pass `step` (one of the values above) and optional `track`. Returns `{ instructions, resource_manifest, next }`: the methodology to follow, the list of resources the step needs, and the handoff to the next step. **Always start with `step="begin"`** for a fresh session. |
| `get_agent_builder_resource` | Fetch one resource named in a step's `resource_manifest`. Pass `type` (one of `reference`, `primitive`, `template`) and `key` (the resource slug, e.g. `taxonomy`, `6-managed-agent`, `propose`). Returns `{ content, version, key }`. Fetch on demand — do not skip manifest entries. |

---

## B. Resource types

`get_agent_builder_resource` serves three kinds of methodology by `type`:

| Type | When to use |
|---|---|
| `reference` | Background knowledge a step reasons against (e.g. taxonomies, scoring axes, principles). Fetch when the instructions cite a reference key. |
| `primitive` | A reusable building block the step composes with (e.g. an agent pattern like `6-managed-agent`). Fetch when the manifest lists a primitive. |
| `template` | A concrete scaffold to fill in — typically an HTML artifact template for rendering steps. Fetch, inject data into the JSON data-islands, and write the file. |

---

## Tool-selection patterns by goal

**"Start a Klarity session / the user mentioned processes, automation, or
agents"** → `get_agent_builder_instructions(step="begin")` → follow the returned
handoff to the next step.

**"Do lifecycle step X"** → `get_agent_builder_instructions(step="X")` → for
each entry in the returned `resource_manifest`,
`get_agent_builder_resource(type=..., key=...)` → follow the instructions.

**"Render the home / current-state / propose artifact"** →
`get_agent_builder_instructions(step=...)` → fetch the template resource named
in the manifest → inject data into the JSON data-islands → write the HTML file →
tell the user to open it.

**"Build a skill for my team"** →
`get_agent_builder_instructions(step="skill_track")` (the conductor) → it runs
the gates and drives `skill_discovery` → `skill_outline` → `skill_build` under
it, fetching each stage's instructions and resources.

---

## Operating principles for agents

1. **Fetch, don't improvise.** No methodology ships in these skills. Every
   step's instructions and every reference/primitive/template come from the MCP
   at runtime. If you're generating methodology from memory, you've skipped a
   fetch.
2. **Honor the manifest.** The `resource_manifest` returned with each step lists
   exactly what that step needs. Fetch every entry on demand; do not skip.
3. **Follow the handoff.** Each step returns a `next` — use it to move through
   the lifecycle rather than guessing the order.
4. **The client owns durable state.** The tools return methodology; the client
   writes all outputs to the project directory and runs the gate loops
   (especially in `skill_track`, the client-side conductor).
5. **Read-only tools.** Both tools only serve content; they never mutate
   workspace state.

---

## Note for MCP-only users (no skills installed)

If you are connected to the Klarity MCP without the agent-builder skills
installed, start by calling `get_agent_builder_instructions(step="begin")`. That
call establishes workspace resolution, the lifecycle model, the two-door gate,
and the next-step handoff — everything the skills would otherwise route for you.
From there, follow each step's returned instructions and resource manifest
exactly as described above.
