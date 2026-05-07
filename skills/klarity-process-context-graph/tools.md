# Klarity MCP — PROD Tool Catalog

This is the operational reference for every tool the Klarity MCP exposes to a
customer's AI agent in production. **All tools here are read-only**, with one
exception (`switch_mcp_workspace`) needed to change the agent's active
workspace.

The point of this catalog is not to enumerate APIs — it's to help an agent
**pick the right tool for the goal at hand** when working inside a customer's
Klarity workspace.

## How agents should think about Klarity

Klarity is a process intelligence platform that captures **how work
actually happens** inside a customer's organization (Companion + Interviewer),
organizes it into a living **Process Index / Context Graph** (Structure), and
helps customers improve via Advisor + Signals (Improve). When an agent calls
the Klarity MCP, it is reading from that living map.

The agent's job is usually one of:

1. **Understand current state** — what process exists, who runs it, how, with
   what evidence.
2. **Explain or summarize** — answer a customer question grounded in the
   workspace, not generic knowledge.
3. **Trace dependencies / impact** — what feeds this, what is downstream, what
   breaks if it changes.
4. **Find improvement opportunities** — surface duplication, exceptions,
   inconsistencies across processes that humans miss at scale.
5. **Drive transformation** — pull the evidence needed to plan a future state
   (ERP migration, automation, controls coverage, close-cycle reduction, etc.).

All five workflows reduce to: **find the right process(es) → fetch detail →
gather evidence → traverse relationships → synthesize**. The tools below are
grouped by where they fit in that flow.

---

## A. Standard MCP entry points

The default entry path. Most ChatGPT / Claude / standard MCP clients will start
here.

| Tool | When to use |
|---|---|
| `search` | First call for almost any process question. Semantic search over the customer's process index. **Iterate** — single queries rarely cover broad topics, and processes use organization-specific names. |
| `fetch` | Pull full details for one process by ID returned from `search` or hierarchy navigation: placement in the index, current version (steps, policies, inputs/outputs), dependencies, history. Fetch dependency IDs to walk relationships. |

---

## B. Process Index — discover & navigate

Use these when `search` results feel sparse, or when you need richer process
metadata than `fetch` returns.

| Tool | When to use |
|---|---|
| `search_processes` | Like `search` but returns mixed hierarchy-node + process results. Use when a top-level value stream / department might be a better starting point than a leaf process. |
| `search_workspace_processes` | Lookup by **name / objective / team**, not semantic. Use when you have an exact phrase or team filter. |
| `get_process_hierarchy_tree` | Browse the whole index structure. Use when search misses, or to orient before drilling in. |
| `get_process_hierarchy_node_details` | Inspect a single hierarchy node — parent, children, linked process. |
| `get_process_detail` | Flat lookup by resource key or exact name. Light payload (name, objective, team, updated_at, source_url). |
| `get_process_details` | The rich nested payload: `current_version`, `dependencies`, `hierarchy_node`, optional version history. This is what `fetch` reshapes. Use directly when you need the structured shape. |

---

## C. Process change & evidence

Customer asks "what changed?", "what happened?", "why does this run this way?"
Use these to pull the evidence trail behind a process.

| Tool | When to use |
|---|---|
| `get_recent_process_changes` | Workspace-wide version-change feed. "What has been edited recently?" |
| `get_recent_process_observations` | Workspace-wide observations feed. Observations are the **deviations / exceptions** captured by Companion. |
| `get_process_observations` | All observations for one process across versions. Optional version filter. |
| `list_process_observations` | Lighter variant — recent observations for one process. |
| `get_observation_activity_timeline` | The actual session timeline behind an observation: what the user did, when. The most "primary source" evidence Klarity has. |

---

## D. Process visualization

| Tool | When to use |
|---|---|
| `generate_process_diagram` | When the user asks to **see** a process — diagrams, BPMN, flows. Choose `BPMNDiagram` when roles/teams/ownership matter; `ProcessFlowDiagram` for plain step flow. |

---

## E. Artifacts — the source evidence

Artifacts are the underlying documents, recordings, and source files behind
processes (BRDs, SOPs, video recordings, screenshots).

| Tool | When to use |
|---|---|
| `search_artifacts` | Hybrid semantic + lexical search across artifact text chunks. Returns short snippets. **Start here** for artifact discovery. |
| `search_workspace_artifacts` | Lookup by display name. |
| `get_artifact_detail` | Latest artifact matching exact display name or resource key. |
| `get_artifact_details` | ~15k token cap details. |
| `get_artifact_content` | Full text up to ~15k tokens. |
| `get_artifact_lines` | Line-numbered text up to ~5k tokens. Use when you need to cite specific lines. |
| `search_artifact_text` | Within one artifact, find line-numbered matches. |
| `get_artifact_screenshots` | Pull PNG screenshots from a VIDEO artifact at specific timestamps. |
| `sample_video_frames` | Same idea — up to 5 timestamps, returns image files. |

---

## F. Context Graph — relational map

The Context Graph is the relational layer above the Process Index — entities
(systems, teams, controls), communities (clusters of related work),
relationships (handoffs, dependencies). Use when the question is **relational**:
"what feeds X", "what depends on Y", "where is Z covered".

| Tool | When to use |
|---|---|
| `search_knowledge_graph` | Entry point. Returns starting points (entities, communities, claims, chunks). **Always follow up** with one of the get_* / explore_* tools — do not answer from snippets. |
| `get_entity_details` | Specific entity (system, team, person, control). |
| `get_community_details` | Specific community (cluster of related work). |
| `get_relationship_details` | Between two entities — types and metadata. |
| `get_text_chunk_details` | Full text + metadata for a specific chunk. |
| `explore_graph_neighbors` | N-hop neighbors of an entity or community. Use for impact analysis. |
| `summarize_community_subgraph` | Community summary up to N hops. Good for orientation when the graph area is unfamiliar. |
| `get_upstream_sources` | Recursive upstream trace. "What feeds this?" |
| `get_downstream_dependencies` | Recursive downstream trace. "What breaks if this changes?" |

---

## G. Objectives — Advisor & transformation tracking

Objectives represent **transformation work** the customer is driving with
Klarity Advisor (e.g., "shorten close from 7 to 3 days", "find duplicate
invoice processing across geographies"). Each objective accumulates findings,
actions, activity, and notes over time.

Use these when the customer asks about ongoing transformation work or wants to
build on prior analysis instead of starting from scratch.

| Tool | When to use |
|---|---|
| `get_objective` | Full objective by resource key. |
| `get_objective_action` | One specific action. |
| `get_objective_finding` | One specific finding. |
| `get_objective_note` | One specific note (agent notebook, user context, or run summary). |
| `list_objective_actions` | All actions for an objective. |
| `list_objective_findings` | All findings for an objective. |
| `list_objective_notes` | All notes for an objective. |
| `list_objective_activity` | Append-only activity log for an objective. |
| `get_objective_context_bundle` | The stitched bundle: objective + findings + actions + activity + notes + agent state. **Best one-call for orientation.** |
| `get_objective_analysis_input` | Top-of-run context bundle plus recent workspace evidence — what the Advisor agent itself sees at start of a run. |
| `get_objective_agent_state` | The persisted agent checkpoint. Use when resuming or debugging an Advisor run. |
| `list_objective_items_with_active_steering` | Findings/actions where the user has provided active steering feedback. |

---

## H. Workspace navigation

| Tool | When to use |
|---|---|
| `list_accessible_workspaces` | List the customer's workspaces and which one is currently active. |
| `switch_mcp_workspace` | **Only write tool exposed in PROD.** Switch the active workspace. Only call when the customer explicitly asks. |

---

## I. Database & schema (advanced fallback)

| Tool | When to use |
|---|---|
| `get_schema` | Read the workspace database schema. |
| `execute_query` | Raw SQL against the workspace DB. **Last resort** — prefer the typed tools above. Useful when the customer asks an analytics question no typed tool covers. |

---

## J. Web research

| Tool | When to use |
|---|---|
| `research_web` | Research a topic on the public web. Use sparingly — Klarity's value is grounded in the customer's workspace, not the open web. |

---

## K. Workspace attributes & sessions

| Tool | When to use |
|---|---|
| `get_attribute_configurations` | Workspace-level attribute configs (custom fields, compliance attributes). Use when the customer asks about controls, compliance attributes, or process metadata schema. |
| `search_workspace_activity_or_sessions` | Recent workspace sessions as supporting evidence. |

---

## Tool-selection patterns by goal

**"Tell me about process X"** → `search` → `fetch`. If sparse: `get_process_hierarchy_tree` to browse, then `fetch` the right leaf.

**"What is the evidence for Y?"** → `fetch` (process) → look at policies in current_version + observations → `get_observation_activity_timeline` for the actual session that produced an observation.

**"What changed recently?"** → `get_recent_process_changes` + `get_recent_process_observations` → drill into specific processes via `fetch`.

**"What depends on Z?" / "What is the impact?"** → `search_knowledge_graph` to find Z's entity → `get_downstream_dependencies` (impact) or `get_upstream_sources` (root cause / inputs).

**"Find improvement opportunities in our P2P value stream"** → `get_process_hierarchy_tree` (root: P2P node) → for each leaf: `get_process_details` → look for duplication, exception handling, missing controls. Surface as findings; offer to seed an objective.

**"Continue the transformation work we started"** → `list_accessible_workspaces` (right workspace?) → if there is an existing objective, `get_objective_context_bundle` to load full prior state, then build on it.

---

## Operating principles for agents

1. **Iterate on search.** Single queries miss. Always be willing to refine 2–4
   times before falling back to hierarchy browsing.
2. **Stay grounded.** Cite Klarity evidence when available (process IDs,
   artifact IDs, observation timestamps). Do not invent facts the workspace
   does not support.
3. **Separate observed from inferred.** "Observed: X happens at step 3."
   "Inferred: this is likely a duplication of Y based on similar steps in Z."
4. **Call out gaps.** If the workspace does not have evidence, say so plainly.
   That gap is itself useful information for the customer.
5. **Do not expose internal IDs unless needed for a follow-up.** Resource keys
   are for tool calls, not user-facing prose.
6. **Read-only by default.** `switch_mcp_workspace` is the only PROD write
   tool — only call when explicitly asked.

---

## Worked end-to-end scenarios

Each scenario starts with the **outcome** the agent is trying to achieve, then
shows how to compose tools to get there. Use these as recipes — adapt the
exact sequence to the customer's specific question.

### Scenario 1 — Help a process performer do their job (the customer's actual way)

**Outcome:** "Help me do this task the way my team actually does it, not the
way ChatGPT thinks it's done."

A process performer (AP lead, ops manager, recruiter, analyst) has asked
their agent to do real work — vendor reconciliation, invoice approval, ERP
migration prep, audit walkthrough. Pull the customer's existing process
before improvising.

1. `list_accessible_workspaces` — confirm the agent is in the right
   workspace (or `switch_mcp_workspace` if not).
2. `search` — query the task in the user's words ("vendor invoice
   reconciliation"). Iterate 2–4 times with refined queries — single queries
   rarely cover broad topics.
3. If still sparse: `get_process_hierarchy_tree` — orient on the value
   stream (P2P, O2C, close cycle, etc.) and find the right leaf.
4. `fetch` — pull the matched process. Read steps, policies, inputs,
   outputs, and dependencies.
5. `get_process_details` — go deeper if `fetch`'s shape is not enough
   (e.g., need the full version metadata or all dependency IDs to walk).
6. `get_recent_process_observations` — has anything changed in this
   process recently? Are there new edge cases the user should know about?
7. `get_process_observations` — exception patterns observed for this
   process across versions.
8. `get_observation_activity_timeline` — drill into the most recent or
   most relevant exception session for primary-source evidence of how the
   process actually runs in practice.
9. Optional: `get_upstream_sources` / `get_downstream_dependencies` —
   only if the user's task touches the boundary (e.g., "what should I check
   before I close this out?").
10. Synthesize: "Here's how your team does this, here's the deviation
    pattern from last quarter, here's what to watch for."

### Scenario 2 — Give a manager a state-of-the-team report

**Outcome:** "Give me a state-of-the-team report on the processes we own —
what's running, what's changing, what's deviating, what needs my attention."

A team manager is checking in on the processes their team owns. The agent
should produce a concise, evidence-backed brief that the manager can act on.

1. `list_accessible_workspaces` — confirm workspace.
2. `get_process_hierarchy_tree` (root: their team's value stream node) —
   pull the team's part of the index.
3. `get_recent_process_changes` — what's been edited recently across the
   workspace, filtered to processes under the team's tree.
4. `get_recent_process_observations` — what deviation patterns are
   emerging across the team's processes.
5. For each high-volume or recently-changed process:
   - `get_process_details` — current state, dependencies, version label.
   - `list_process_observations` — recent observation summary (lighter
     than `get_process_observations`).
6. Spot-check the top 2–3 emerging deviations:
   `get_observation_activity_timeline` — drill into the actual session
   for primary-source detail.
7. Optional: `generate_process_diagram` for processes the manager
   wants to share with their team in a 1:1 or team meeting.
8. Synthesize: "Your team owns N processes. M changed in the last 30
   days. K are showing deviation patterns worth your attention. Here are
   the top 3 with evidence."

### Scenario 3 — Find transformation opportunities across the process index

**Outcome:** "Find me the highest-leverage transformation / automation
opportunities across our org (or this value stream). Where should we focus?"

A platform lead, AI transformation owner, or AI architect needs a ranked
candidate set. This is the "spin up multiple agents to scan the entire
process tree" use case — agents should fan out in parallel across the
hierarchy.

1. `list_accessible_workspaces` — confirm workspace.
2. `get_process_hierarchy_tree` — pull the whole tree, or filter to the
   value stream of interest. This becomes the work queue.
3. **In parallel** across leaves (this is where multiple agents pay off):
   - `get_process_details` — current version, steps, dependencies.
     Note step count, manual vs system steps, exception count.
   - `list_process_observations` — exception volume per process.
4. `search_knowledge_graph` — query for common high-leverage patterns:
   "manual approval", "duplicate entry", "data re-keying", "exception
   handling", "swivel-chair workflow".
5. `explore_graph_neighbors` on each pattern entity — see which
   processes and systems touch it.
6. `get_attribute_configurations` — workspace attribute schema (look for
   "automation status", "system of record", "control level" or similar
   metadata that helps rank candidates).
7. `list_objective_findings` — has Advisor already analyzed this area?
   Don't duplicate prior work.
8. If yes: `get_objective_context_bundle` — load prior thinking and
   build on it. If no: surface the candidate set fresh.
9. For each top candidate:
   - `get_process_observations` — confirm the deviation/manual pattern
     with concrete evidence.
   - `get_downstream_dependencies` — first cut at blast radius.
10. Synthesize a ranked candidate set: process IDs, observation counts,
    dependency depth, similarity to known patterns, evidence trail.
11. Optional: `research_web` to cross-check vendor automation tooling
    for the highest-ranked candidates.

### Scenario 4 — Form a transformation thesis on a chosen process or value stream

**Outcome:** "I've zeroed in on process X (or value stream Y). Build me a
transformation thesis: current state, blast radius, dependencies, where to
intervene."

The customer has identified the target. The agent's job is to build deep,
evidence-grounded understanding before recommending changes.

1. `list_accessible_workspaces` — confirm workspace.
2. `search` → `fetch` (or directly `fetch` if the ID is known) — pull
   the target process.
3. `get_process_details` — full nested payload: current version, all
   dependencies, hierarchy node, version history.
4. `get_process_hierarchy_node_details` — context within the index
   (parent value stream, sibling processes that may share patterns).
5. `get_recent_process_changes` (filtered to this process if possible)
   — version evolution. What has the team been changing? In which
   direction?
6. `get_process_observations` — all observations across versions. Look
   for repeated deviation patterns, exception types, manual workarounds.
7. For 3–5 representative observations:
   `get_observation_activity_timeline` — primary-source detail of how
   the process runs in practice (not how it's documented).
8. **Map upstream and downstream:**
   - `get_upstream_sources` — what feeds this process. Root cause /
     input quality matters for transformation viability.
   - `get_downstream_dependencies` — blast radius if we change it.
     Surfacing this early prevents under-scoped transformation
     proposals.
9. `search_knowledge_graph` — find entities (systems, teams, controls)
   that touch this process.
10. `get_entity_details` for the most-connected entities — understand
    them as transformation surfaces.
11. `explore_graph_neighbors` to map the surrounding network.
12. `summarize_community_subgraph` if the process sits in a meaningful
    community — gives a one-call overview of the surrounding work.
13. `list_objective_findings` — any prior Advisor thinking on this
    process or value stream.
14. If yes: `get_objective_context_bundle` — load prior findings,
    actions, steering. Build on them, don't start from scratch.
15. Optional: `generate_process_diagram` — produce a visual of current
    state for the thesis document.
16. Synthesize a transformation thesis:
    - **Current state:** how the process actually runs (cite
      observations).
    - **Blast radius:** upstream feeders + downstream dependents.
    - **Pain pattern:** the deviation / manual / duplication signal,
      with evidence.
    - **Intervention points:** where to change, ranked by leverage and
      risk.
    - **Open questions:** what evidence is missing that would
      strengthen or invalidate the thesis.

### What these scenarios share

- **Iteration is normal.** Every scenario uses 2–4 search refinements before
  drilling. Don't bail after one query.
- **Composition is the value.** No single tool answers a real question. The
  agent's job is to chain reads — search → process → version → observation
  → activity timeline → graph — until it has enough to answer with
  confidence.
- **Always ground synthesis.** Cite process IDs, observation timestamps, and
  graph entity IDs. Never invent.
- **Build on prior work when possible.** `list_objective_findings` +
  `get_objective_context_bundle` save dozens of tool calls when the customer
  has existing Advisor work in flight.
- **Parallelize on transformation scans.** Scenario 3 explicitly benefits
  from multiple agents fanning out across the hierarchy. The MCP is
  stateless per call — there's no penalty for parallel reads.
