"""Canonical product and manifest metadata for Klarity MCP (public factory)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


_KLARITY_MCP_DEFAULT_DESCRIPTION = (
    "Bring your organization's processes and operational knowledge into your AI "
    "assistant. The Klarity MCP connects to your Klarity workspace so you "
    "can query your organization's processes, explore the process index knowledge "
    "graph linking processes to systems and teams, and ground answers in how your "
    "business actually runs — not generic guesses."
)


@dataclass(frozen=True)
class KlarityMCPMetadata:
    product_name: str
    app_display_name: str
    plugin_name: str
    plugin_version: str
    author_name: str
    author_email: str
    author_url: str
    homepage_url: str
    privacy_policy_url: str
    terms_of_service_url: str
    support_email: str
    category: str
    brand_color: str
    mcp_server_key: str
    mcp_url: str
    oauth_resource: str
    plugin_description: str
    app_description: str
    interface_short_description: str
    interface_long_description: str
    keywords: tuple[str, ...]
    capabilities: tuple[str, ...]
    default_prompts: tuple[str, ...]
    submission_test_prompts: tuple[str, ...]
    license_spdx: str
    repository_url: str
    # All skill directory names bundled under skills/. Ships across every client.
    skills: tuple[str, ...]
    # The single entry-point skill Gemini's `contextFileName` points at. Gemini's
    # extension schema accepts exactly one context file, so it cannot enumerate
    # every skill the way Codex/Claude do; this designates the one that loads.
    gemini_context_skill: str


KLARITY_MCP_METADATA = KlarityMCPMetadata(
    product_name="Klarity",
    app_display_name="Klarity",
    plugin_name="klarity",
    plugin_version="1.0.0",
    author_name="Klarity Intelligence, Inc.",
    author_email="hello@klarity.ai",
    author_url="https://www.klarity.ai/",
    homepage_url="https://www.klarity.ai/",
    privacy_policy_url="https://www.klarity.ai/product-privacy-policy",
    terms_of_service_url="https://www.klarity.ai/terms-of-service-2025",
    support_email="hello@klarity.ai",
    category="Business",
    brand_color="#FF6C14",
    mcp_server_key="klarity",
    mcp_url="https://api.klarity.ai/mcp",
    oauth_resource="https://api.klarity.ai",
    plugin_description=_KLARITY_MCP_DEFAULT_DESCRIPTION,
    app_description=_KLARITY_MCP_DEFAULT_DESCRIPTION,
    interface_short_description="Explore your org's processes",
    interface_long_description=_KLARITY_MCP_DEFAULT_DESCRIPTION,
    keywords=(
        "klarity",
        "mcp",
        "process-intelligence",
        "process-index",
        "context-graph",
        "knowledge-graph",
    ),
    capabilities=("Read", "Analyze"),
    default_prompts=(
        "Find me the invoice intake process in my Klarity Workspace.",
        "How does my invoice intake process work?",
        "Show me the procure-to-pay process and its dependencies in my Klarity Workspace.",
    ),
    submission_test_prompts=(
        "Find me the invoice intake process in my Klarity Workspace.",
        "How does my invoice intake process work?",
        "Show me the procure-to-pay process and its dependencies in my Klarity Workspace.",
    ),
    license_spdx="Apache-2.0",
    repository_url="https://github.com/Klarity-AI/klarity-mcp",
    skills=(
        "klarity-process-context-graph",
        "agent-builder",
    ),
    gemini_context_skill="agent-builder",
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_PLUGIN_DIR = REPO_ROOT / ".claude-plugin"
# Lives at the repo root (not under .claude-plugin/) because Claude Code's plugin
# loader resolves the manifest's `mcpServers` string from the plugin root, which
# is the directory containing `.claude-plugin/`. Putting the file under
# `.claude-plugin/.mcp.json` causes Claude to silently register zero servers.
CLAUDE_MCP_CONFIG_PATH = REPO_ROOT / ".mcp.json"
# Marketplace manifest must live at `.claude-plugin/marketplace.json` for
# `/plugin install <plugin>@<owner>/<repo>` to resolve this repo as a marketplace.
CLAUDE_MARKETPLACE_PATH = CLAUDE_PLUGIN_DIR / "marketplace.json"
GEMINI_EXTENSION_PATH = REPO_ROOT / "gemini-extension.json"
# Codex plugin manifest lives at `.codex-plugin/plugin.json` per OpenAI's Codex
# plugin spec (mirrors Claude's `.claude-plugin/plugin.json`). The Codex loader
# also resolves `mcpServers: "./.mcp.json"` from the plugin root, so the shared
# `.mcp.json` at the repo root works for both Claude and Codex.
CODEX_PLUGIN_DIR = REPO_ROOT / ".codex-plugin"
# Codex's marketplace lookup (codex-rs/core-plugins/src/marketplace.rs) probes
# `.agents/plugins/marketplace.json` first, then `.claude-plugin/marketplace.json`
# as a fallback. The Codex-native location avoids ambiguity with Claude's schema.
CODEX_MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
SKILLS_DIR = REPO_ROOT / "skills"
