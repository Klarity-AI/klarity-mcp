# klarity-mcp

> Public plugin/extension distribution for the Klarity MCP server.

`klarity-mcp` packages [Klarity](https://www.klarity.ai/) as an installable
plugin for AI assistant clients that speak the [Model Context Protocol](https://modelcontextprotocol.io/).
Once installed, the plugin lets your assistant query your organization's processes,
explore the Process Index knowledge graph, and ground answers in how your business
actually runs — not generic guesses.

This repository is the canonical public surface for two install paths:

- **Claude Code / Claude** — Anthropic's plugin ecosystem.
- **ChatGPT / Codex** — OpenAI's app ecosystem.
- **Gemini CLI** — Google's CLI extension ecosystem.


## What it does

The plugin connects your AI assistant to the Klarity MCP server at
`https://architect-v2-api.klarity.ai/mcp`. Tools the assistant gets access to
include `search`, `fetch`, process-hierarchy navigation, evidence retrieval, and
Context Graph traversal. The full skill prompt lives at
[`skills/klarity-process-context-graph/SKILL.md`](./skills/klarity-process-context-graph/SKILL.md).

## Install - Claude.ai

Customize -> Connectors -> Search -> Klarity -> Connect

> (NOTE: your organization might have to approve this connector, and you should be added as a user into Klarity for this to work)

## Install - ChatGPT

Apps -> Search -> Klarity -> Connect

> (NOTE: your organization might have to approve this app, and you should be added as a user into Klarity for this to work)

## Install — Claude Code

From a Claude session, run these two commands one after the other.

**1. First**, install the marketplace:

```text
/plugin marketplace add klarity-ai/klarity-mcp
```

**2. Next**, install the plugin:

```text
/plugin install klarity@klarity
```

## Install — Codex

Codex splits this into two steps. First, from your **shell**, register the
Klarity marketplace with Codex:

```bash
codex plugin marketplace add Klarity-AI/klarity-mcp
```

Then, from a **Codex session**, run:

```text
/plugins
```

Search for **Klarity** and install the plugin.

The first request that hits a Klarity tool will prompt you to sign in.

## Install — Gemini CLI

```bash
gemini extensions install https://github.com/klarity-ai/klarity-mcp
```

To login:
```
/mcp auth klarity
```

## Authentication
You will need to be a Klarity customer to access this app.

The first time the plugin connects, your AI client will prompt you to sign in
to Klarity. the MCP will use whatever authentication is configured by your organization for Klarity.

> **Fallback:** If your client does not yet support MCP OAuth, you can issue
> a personal API key from your Klarity workspace settings and configure your
> client to send it as a `Bearer` token. Contact
> [hello@klarity.ai](mailto:hello@klarity.ai) for guidance.

## Repository layout

| Path | What it is |
|---|---|
| `klarity_mcp/` | Python package: metadata + builders + CLI for regenerating manifests |
| `.claude-plugin/plugin.json` | Claude Code plugin manifest (generated) |
| `.claude-plugin/marketplace.json` | Claude Code marketplace catalog (generated) |
| `.codex-plugin/plugin.json` | Codex plugin manifest (generated) |
| `.agents/plugins/marketplace.json` | Codex marketplace catalog (generated) |
| `.mcp.json` | Shared MCP server config (HTTP transport; used by Claude Code and Codex) |
| `gemini-extension.json` | Gemini CLI extension manifest (generated) |
| `skills/klarity-process-context-graph/SKILL.md` | The Klarity skill prompt |
| `tests/test_packaging.py` | Manifest invariants + drift checks |
| `LICENSE` | Apache-2.0 (covers this shim only — see `NOTICE`) |
| `NOTICE` | Trademark + commercial-service notice |

## For Klarity Team - Regenerating Manifests

```bash
pip install -e ".[dev]"
python -m klarity_mcp --write     # regenerates the public manifests
python -m klarity_mcp --check     # CI-side drift check
pytest -v
```

The metadata that drives every manifest lives in
[`klarity_mcp/metadata.py`](./klarity_mcp/metadata.py). Edit there, then re-run
`--write` and commit the result.

## License

This plugin shim is released under the [Apache License 2.0](./LICENSE). The
Klarity service it connects to is a commercial service governed by
Klarity's Terms of Service. See [`NOTICE`](./NOTICE) for details.

## Links

- Klarity: <https://www.klarity.ai/>
- Privacy Policy: <https://www.klarity.ai/product-privacy-policy>
- Terms of Service: <https://www.klarity.ai/terms-of-service-2025>
- Issues / contact: <mailto:hello@klarity.ai>
