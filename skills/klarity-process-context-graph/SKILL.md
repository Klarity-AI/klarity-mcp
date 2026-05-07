---
name: klarity-process-context-graph
description: Ground answers in how the user's organization actually runs by querying their Klarity workspace — a living map of how work happens, captured from real sessions and structured into a process index plus context graph linking processes to systems and teams. Use when the user asks about THEIR organization's processes, not generic best practices. Trigger phrases include "how does our [process] work today", "walk me through our [workflow] for X", "where is this policy or control documented", "show me our SOP for X", "what changed recently in our processes", "what observations show how Y runs", "what feeds X" / "what depends on X" / "what breaks if we change Y", "find duplication or improvement opportunities in our [P2P / O2C / close / value stream]", "where can we automate", "where is risk not covered by controls", "show me our process index", "what value streams do we have". Skip for generic best-practices, hypothetical, or public-knowledge questions that don't reference the user's specific organization.
---

# Klarity

Use this skill when a customer asks an AI assistant to understand how work actually happens in their Klarity workspace.

Klarity follows the Discover -> Structure -> Improve loop. Companion and Interviewer capture how work happens, the Process Index / Context Graph organizes that knowledge into a living map, and Advisor-style analysis helps customers improve with evidence.

## Core Journey

1. Start by identifying the right part of the Process Index. For process-focused questions, call `search` with the user's workflow, value stream, team, policy, control, handoff, exception, system, or business outcome.
2. Fetch the selected process. Use `fetch` with the process ID returned by `search` to read the citable process summary, version metadata, inputs, outputs, steps, policies, and dependencies.
3. Drill deeper when the standard summary is not enough. Use process hierarchy and process detail tools to inspect hierarchy nodes, attributes, tasks, sub-tasks, linked artifacts, and recent changes.
4. Gather evidence before answering. Pull observations, activity timelines, artifacts, screenshots, or artifact text when the user needs support for what changed, what happened, or why a process behaves a certain way.
5. Traverse the Context Graph when the question is relational. Use graph tools to find entities, communities, relationships, upstream sources, downstream dependencies, supporting chunks, and connected claims.
6. Recurse across related processes or graph nodes until the answer has enough context. Stop when additional traversal is duplicative, low-confidence, or outside the user's scope.
7. Synthesize in business language. Separate observed facts from inference, cite Klarity evidence when available, and call out gaps when the workspace does not contain enough support.

## Common User Stories

- A customer asks what a process is or how it works: search for the process, fetch the matching process, then summarize the flow at the user's requested level of detail.
- A customer asks where a policy, control, or operating rule is supported: identify the relevant process and artifacts, inspect the supporting content, then explain the evidence.
- A customer asks what changed recently: review recent process changes and observations, then connect those changes to specific processes, sessions, artifacts, or graph evidence.
- A customer asks about dependencies or impact: start from the relevant entity, community, or process, trace upstream and downstream relationships, then summarize the dependency chain.
- A customer asks for improvement opportunities: gather process details, observations, deviations, graph relationships, and source artifacts before forming recommendations.

## AI Transformation User Stories

The Klarity MCP is the surface where a customer's AI agents pull organization-specific context at runtime. The customer's people interact with this skill **through their agents** — Claude, ChatGPT, Cursor, Workato, Agentforce, or an internal LLM. Common transformation-flavored patterns, organized by who the agent is ultimately serving:

### Helping process performers do their job

- **Outcome: do the task the way my team actually does it, not the way ChatGPT thinks it's done.** A process performer (AP lead, ops manager, recruiter, analyst) asks their agent to do task X — vendor reconciliation, invoice approval, candidate screening, ERP migration prep, audit readiness. Pull the customer's existing process for X via `search` + `fetch` BEFORE improvising. Use the customer's actual approach.
- **Outcome: notice if my org already does this somewhere else.** A user suspects duplication mid-task. Search across teams, geographies, or business units for similar processes; traverse the context graph for related entities. Surface the duplicate set with process IDs.

### Giving managers insight on the processes they own

- **Outcome: state-of-my-team report.** A team manager wants insight on what's happening across the processes they own — what's running, what's changing, where deviations are emerging, what's worth their attention. Walk the team's part of the hierarchy, summarize recent process changes and observations, and surface the highest-signal items.
- **Outcome: ramp a new joiner (or a fresh agent) on how this team operates.** Walk the team's process index, fetch top processes, surface dependencies and recent changes. Ground the new person / agent in the customer's operational reality, not in generic role-based assumptions.
- **Outcome: prove our control or compliance coverage.** An auditor, SOX owner, or risk lead asks "where is control X supported?" or "what's our evidence for policy Y?" Pull the relevant processes, surface the policies attached to the current version, and cite the supporting observations and activity timelines.

### Driving transformation

- **Outcome: find the highest-leverage automation / transformation opportunities across our org.** A platform lead, AI architect, or transformation owner asks "where in our [P2P / O2C / close cycle / value stream] can we automate?" Walk the hierarchy under the value stream (often in parallel across many leaves), look for high-volume manual steps, exception patterns, and cross-process duplication. Surface a ranked candidate set with citable evidence.
- **Outcome: form a transformation thesis on a specific process or value stream.** The customer has zeroed in on a target. Build current-state, blast-radius, and dependency understanding; identify intervention points; ground the thesis in observations and graph relationships.
- **Outcome: continue in-flight transformation work without restarting.** The customer has an existing Advisor objective ("shorten close from 7 to 3 days", "find duplicate invoice processing across geographies"). Pull `get_objective_context_bundle` to load prior findings, actions, activity, and agent state — then build on it instead of starting cold.

See `tools.md` for end-to-end worked scenarios that compose many tools together for each of these outcomes.

## Operating Principles

- Prefer read-only tools for customer-facing analysis.
- Use `search` and `fetch` as the default process discovery and citation path for ChatGPT/Codex company-knowledge-style requests.
- Use workspace switching only when the customer explicitly asks to change the active Klarity workspace.
- Do not invent process facts. If the Process Index, artifacts, observations, or Context Graph do not support a claim, say what is missing.
- Do not expose internal IDs unless the user needs them for a follow-up action.
- Keep answers grounded in the authenticated Klarity session and the customer's current workspace.

## Good Outcomes

Help customers answer questions such as:

- "How does this workflow actually run today?"
- "Which process and artifact explain this control?"
- "What observations show the current-state behavior?"
- "What changed recently in this part of the Process Index?"
- "Which upstream teams, systems, or steps feed this process?"
- "What downstream processes would be affected if this handoff changed?"

## How Klarity Fits a Customer's Transformation Loop

Klarity runs the **Discover -> Structure -> Improve** loop continuously (replacing one-time "transformation projects" that take months and have a 30% success rate). When a customer's agent uses this MCP, it is plugging into that loop:

- **Discover**: Companion (ambient capture from sessions) and Interviewer (AI-guided structured capture) generate the raw process knowledge. Agents read this via process / observation / artifact tools.
- **Structure**: The Process Index and Context Graph are the living, queryable map of the customer's organization. Agents navigate this via `search` / `fetch` / hierarchy / graph tools.
- **Improve**: Advisor analyzes thousands of processes simultaneously to surface improvement opportunities; Signals give individual-level feedback. Agents read in-flight transformation work via objective tools.

The customer's question almost always maps to one of these stages. Use the catalog in `tools.md` to pick the right tool for the goal.

## Tool Catalog

The full PROD-allowed tool list, organized by use case with selection guidance, lives in `tools.md` (alongside this file). Read it when you need to pick a specific tool — it covers all 51 tools the Klarity MCP exposes in production and gives explicit "if the user asks X, call Y" patterns.
