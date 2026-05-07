"""Public manifest builders for Klarity MCP plugin distribution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from klarity_mcp.metadata import (
    CLAUDE_MCP_CONFIG_PATH,
    CLAUDE_PLUGIN_DIR,
    GEMINI_EXTENSION_PATH,
    KLARITY_MCP_METADATA,
    KlarityMCPMetadata,
)


def build_claude_plugin_manifest(
    metadata: KlarityMCPMetadata = KLARITY_MCP_METADATA,
) -> dict[str, Any]:
    """Output: .claude-plugin/plugin.json (Claude Code plugin manifest)."""
    return {
        "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
        "name": metadata.plugin_name,
        "version": metadata.plugin_version,
        "description": metadata.plugin_description,
        "author": {
            "name": metadata.author_name,
            "email": metadata.author_email,
            "url": metadata.author_url,
        },
        "homepage": metadata.homepage_url,
        "repository": metadata.repository_url,
        "license": metadata.license_spdx,
        "keywords": list(metadata.keywords),
        "mcpServers": "./.mcp.json",
    }


def build_claude_mcp_config(
    metadata: KlarityMCPMetadata = KLARITY_MCP_METADATA,
) -> dict[str, Any]:
    """Output: .mcp.json at the repo root (Claude Code MCP server config, HTTP transport).

    Lives at the plugin root (not under `.claude-plugin/`) because Claude's plugin
    loader resolves `mcpServers: "./.mcp.json"` from the plugin root.
    """
    return {
        "mcpServers": {
            metadata.mcp_server_key: {
                "type": "http",
                "url": metadata.mcp_url,
            }
        }
    }


def build_gemini_extension_manifest(
    metadata: KlarityMCPMetadata = KLARITY_MCP_METADATA,
) -> dict[str, Any]:
    """Output: gemini-extension.json (Gemini CLI extension manifest).

    Uses the consolidated `url` key (not `httpUrl`) per Gemini CLI PR #13762.
    """
    return {
        "name": metadata.plugin_name,
        "version": metadata.plugin_version,
        "description": metadata.plugin_description,
        "mcpServers": {
            metadata.mcp_server_key: {
                "url": metadata.mcp_url,
            }
        },
        "contextFileName": "skills/klarity-process-context-graph/SKILL.md",
    }


def build_manifest_payloads(
    metadata: KlarityMCPMetadata = KLARITY_MCP_METADATA,
) -> dict[Path, dict[str, Any]]:
    return {
        CLAUDE_PLUGIN_DIR / "plugin.json": build_claude_plugin_manifest(metadata),
        CLAUDE_MCP_CONFIG_PATH: build_claude_mcp_config(metadata),
        GEMINI_EXTENSION_PATH: build_gemini_extension_manifest(metadata),
    }


def render_manifest(payload: dict[str, Any]) -> str:
    """Serialize a manifest payload to JSON text. Trailing newline is significant."""
    return json.dumps(payload, indent=2, ensure_ascii=True) + "\n"


def build_manifest_texts(
    metadata: KlarityMCPMetadata = KLARITY_MCP_METADATA,
) -> dict[Path, str]:
    return {
        path: render_manifest(payload)
        for path, payload in build_manifest_payloads(metadata).items()
    }
