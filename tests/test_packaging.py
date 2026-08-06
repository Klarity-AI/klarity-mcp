"""Packaging invariants for within-mcp public manifests."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from within_mcp import (
    CLAUDE_PLUGIN_DIR,
    CODEX_PLUGIN_DIR,
    GEMINI_EXTENSION_PATH,
    WITHIN_MCP_METADATA,
    REPO_ROOT,
    SKILLS_DIR,
)
from within_mcp.builders import (
    build_claude_marketplace_manifest,
    build_claude_mcp_config,
    build_claude_plugin_manifest,
    build_codex_marketplace_manifest,
    build_codex_plugin_manifest,
    build_gemini_extension_manifest,
    build_manifest_texts,
    render_manifest,
)


# ---------- 1. Cross-vendor invariants on the canonical metadata ----------

def test_canonical_plugin_name_is_kebab_case() -> None:
    """Single source of truth — guards Claude, Gemini, Microsoft, and Codex names at once."""
    name = WITHIN_MCP_METADATA.plugin_name
    assert re.fullmatch(r"[a-z][a-z0-9-]*", name), (
        f"plugin_name {name!r} must be kebab-case (lowercase alnum + hyphens, "
        f"starting with a letter)"
    )


def test_canonical_mcp_server_key_is_lowercase_alnum() -> None:
    key = WITHIN_MCP_METADATA.mcp_server_key
    assert re.fullmatch(r"[a-z][a-z0-9_]*", key), (
        f"mcp_server_key {key!r} must be lowercase alnum + underscores"
    )


def test_license_is_valid_spdx() -> None:
    # We pin Apache-2.0 by Decision 2.6. If this ever needs to change, update both
    # WITHIN_MCP_METADATA.license_spdx and the LICENSE file in the same PR.
    assert WITHIN_MCP_METADATA.license_spdx == "Apache-2.0"


# ---------- 2. Vendor-specific shape invariants ----------

def test_claude_mcp_manifest_uses_camelcase_and_http_transport() -> None:
    payload = build_claude_mcp_config(WITHIN_MCP_METADATA)
    assert "mcpServers" in payload, "Claude .mcp.json uses camelCase top-level key"
    entry = payload["mcpServers"][WITHIN_MCP_METADATA.mcp_server_key]
    assert entry["type"] == "http"
    assert entry["url"] == WITHIN_MCP_METADATA.mcp_url


def test_claude_plugin_manifest_required_metadata_for_official_submission() -> None:
    payload = build_claude_plugin_manifest(WITHIN_MCP_METADATA)
    for key in ("name", "version", "description", "homepage", "repository", "license", "keywords"):
        assert payload.get(key), f"Claude plugin.json is missing required field: {key}"
    author = payload["author"]
    assert author.get("name"), "Claude plugin.json author.name is required"
    assert author.get("email"), "Claude plugin.json author.email is required"
    assert isinstance(payload["keywords"], list) and payload["keywords"], (
        "keywords must be a non-empty list"
    )


def test_claude_marketplace_has_plugin_with_supported_source_shape() -> None:
    """Each plugin entry's `source` must use one of the shapes Claude Code's
    source parser accepts when the marketplace is consumed directly via
    `/plugin marketplace add owner/repo` (i.e. without Anthropic's curation
    pipeline rewriting the field).

    Supported shapes:
    - String "./<subdir>" pointing at a directory in this repo that holds a
      `.claude-plugin/plugin.json` (only valid when the plugin lives in a
      real subdirectory of the marketplace).
    - Object `{"source": "url", "url": "<git url>"}` for the "whole repo is
      the plugin" pattern. The URL must match this repo's canonical
      repository URL so the install clone is self-referential.

    Bare "." and bare "./" both fail at install time with "source type your
    Claude Code version does not support" — verified empirically.
    """
    payload = build_claude_marketplace_manifest(WITHIN_MCP_METADATA)
    assert payload["name"] == WITHIN_MCP_METADATA.plugin_name
    assert isinstance(payload["plugins"], list) and payload["plugins"]
    for plugin in payload["plugins"]:
        assert plugin.get("name"), "each marketplace plugin must have a name"
        source = plugin.get("source")
        if isinstance(source, str):
            assert source not in (".", "./"), (
                f"plugin {plugin['name']!r} uses bare {source!r} as source — "
                "this is silently rejected by Claude Code's installer. Use the "
                "object form `{'source': 'url', 'url': '<repo>.git'}` instead."
            )
            plugin_root = (REPO_ROOT / source).resolve()
            manifest = plugin_root / ".claude-plugin" / "plugin.json"
            assert manifest.exists(), (
                f"plugin {plugin['name']!r} declares source={source!r}, but "
                f"no plugin manifest exists at {manifest}"
            )
        else:
            assert isinstance(source, dict), (
                "marketplace plugin source must be a string or object"
            )
            assert source.get("source") == "url", (
                "object-form source must use the `url` discriminator"
            )
            expected = f"{WITHIN_MCP_METADATA.repository_url}.git"
            assert source.get("url") == expected, (
                f"object-form url should be {expected!r} (got {source.get('url')!r}) "
                "so the install clone resolves back to this same repo"
            )


def test_codex_plugin_manifest_required_metadata() -> None:
    payload = build_codex_plugin_manifest(WITHIN_MCP_METADATA)
    for key in ("name", "version", "description", "homepage", "repository", "license", "keywords"):
        assert payload.get(key), f"Codex plugin.json is missing required field: {key}"
    assert payload["name"] == WITHIN_MCP_METADATA.plugin_name
    interface = payload["interface"]
    for key in ("displayName", "shortDescription", "longDescription", "category", "brandColor", "defaultPrompt"):
        assert interface.get(key), f"Codex plugin.json interface missing: {key}"
    # Codex caps defaultPrompt to 3 entries (extras are dropped silently).
    assert len(interface["defaultPrompt"]) <= 3, (
        "Codex truncates `defaultPrompt` past 3 entries; keep the canonical list <= 3 "
        "so the rendered prompts match what's declared."
    )


def test_codex_plugin_mcp_servers_path_resolves_to_real_file() -> None:
    """Codex resolves `mcpServers` from the plugin root, same as Claude. Mirror
    the runtime-fidelity test we already have for Claude.
    """
    plugin_manifest_path = CODEX_PLUGIN_DIR / "plugin.json"
    plugin_root = plugin_manifest_path.parent.parent
    manifest = json.loads(plugin_manifest_path.read_text())
    mcp_ref = manifest["mcpServers"]
    assert isinstance(mcp_ref, str)
    mcp_path = (plugin_root / mcp_ref.removeprefix("./")).resolve()
    assert mcp_path.exists(), (
        f"Codex manifest.mcpServers points to {mcp_ref!r}, which resolves to "
        f"{mcp_path}, but no file is committed there."
    )


def test_codex_plugin_skills_path_resolves_to_real_dir() -> None:
    """Codex resolves `skills` from the plugin root. The bundled skill must
    actually exist there or `/plugin install` ships a plugin with no skills.
    """
    plugin_manifest_path = CODEX_PLUGIN_DIR / "plugin.json"
    plugin_root = plugin_manifest_path.parent.parent
    manifest = json.loads(plugin_manifest_path.read_text())
    skills_ref = manifest["skills"]
    assert isinstance(skills_ref, str)
    skills_path = (plugin_root / skills_ref.removeprefix("./")).resolve()
    assert skills_path.exists() and skills_path.is_dir(), (
        f"Codex manifest.skills points to {skills_ref!r}, which resolves to "
        f"{skills_path}, but no directory is committed there."
    )


def test_codex_marketplace_has_plugin_with_supported_source_shape() -> None:
    """Codex's marketplace loader accepts string-local, object-local, `url`,
    and `git-subdir` source shapes (per openai/codex PR #18017). We use the
    `url` shape so the entire repo can act as the plugin without duplicating
    the manifest under `.agents/plugins/`. Guard the shape so the file stays
    parseable.
    """
    payload = build_codex_marketplace_manifest(WITHIN_MCP_METADATA)
    assert payload["name"] == WITHIN_MCP_METADATA.plugin_name
    assert isinstance(payload["plugins"], list) and payload["plugins"]
    for plugin in payload["plugins"]:
        assert plugin.get("name"), "marketplace plugin must have a name"
        source = plugin.get("source")
        assert isinstance(source, dict), (
            "Codex marketplace source must be an object (string-local form is allowed "
            "but we use the explicit object form for the repo-as-plugin pattern)"
        )
        kind = source.get("source")
        assert kind in {"local", "url", "git-subdir"}, (
            f"unsupported source kind {kind!r}; must be local/url/git-subdir"
        )
        if kind == "url":
            assert source.get("url", "").startswith("https://"), (
                "url-shaped sources must point at an https git URL"
            )
        policy = plugin.get("policy")
        assert isinstance(policy, dict)
        assert policy.get("installation") in {"AVAILABLE", "NOT_AVAILABLE", "INSTALLED_BY_DEFAULT"}
        assert policy.get("authentication") in {"ON_INSTALL", "ON_USE"}


def test_gemini_extension_name_matches_canonical_plugin_name() -> None:
    payload = build_gemini_extension_manifest(WITHIN_MCP_METADATA)
    assert payload["name"] == WITHIN_MCP_METADATA.plugin_name, (
        "Gemini extension name must match canonical kebab-case plugin_name"
    )


def test_gemini_extension_mcp_servers_use_url_key() -> None:
    """Gemini CLI consolidated to a single `url` key in PR #13762; `httpUrl` is removed."""
    payload = build_gemini_extension_manifest(WITHIN_MCP_METADATA)
    entry = payload["mcpServers"][WITHIN_MCP_METADATA.mcp_server_key]
    assert "url" in entry, "Gemini mcpServers entry must use `url`"
    assert "httpUrl" not in entry, "Gemini deprecated `httpUrl`; must not appear"
    assert entry["url"] == WITHIN_MCP_METADATA.mcp_url


def test_gemini_extension_context_file_points_at_skill() -> None:
    payload = build_gemini_extension_manifest(WITHIN_MCP_METADATA)
    rel = payload["contextFileName"]
    resolved = REPO_ROOT / rel
    assert resolved.exists() and resolved.is_file(), (
        f"Gemini contextFileName {rel} must point at an existing file in the repo "
        f"(resolved to {resolved})"
    )
    # Sanity: the file must live under skills/ to match the documented pattern.
    assert SKILLS_DIR in resolved.parents, (
        f"contextFileName must live under skills/ (got {resolved})"
    )


def test_declared_skills_resolve_to_real_skill_dirs() -> None:
    """Every skill name in metadata.skills must be a real dir with a SKILL.md.

    These are the skills that ship across Claude, Codex, and Gemini. A typo or a
    missing dir would ship a plugin that references a skill that isn't there.
    """
    missing: list[str] = []
    for skill in WITHIN_MCP_METADATA.skills:
        skill_md = SKILLS_DIR / skill / "SKILL.md"
        if not skill_md.is_file():
            missing.append(skill)
    assert not missing, (
        f"metadata.skills lists names with no skills/<name>/SKILL.md: {missing}"
    )


def test_gemini_context_skill_is_a_declared_skill() -> None:
    """Gemini's single contextFileName must point at one of the bundled skills."""
    assert WITHIN_MCP_METADATA.gemini_context_skill in WITHIN_MCP_METADATA.skills, (
        f"gemini_context_skill {WITHIN_MCP_METADATA.gemini_context_skill!r} "
        f"must be one of metadata.skills"
    )


# ---------- 3. Drift + safety invariants ----------

def test_generated_manifests_match_committed_files() -> None:
    """Byte-compare generated text against committed files. Run `python -m within_mcp --write` to fix."""
    texts = build_manifest_texts(WITHIN_MCP_METADATA)
    mismatches: list[str] = []
    for path, expected in texts.items():
        if not path.exists():
            mismatches.append(f"missing: {path.relative_to(REPO_ROOT)}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            mismatches.append(f"drift: {path.relative_to(REPO_ROOT)}")
    assert not mismatches, (
        "Manifests are out of sync. Run `python -m within_mcp --write` and commit. "
        f"Issues: {mismatches}"
    )


def test_generated_manifests_are_stable_json() -> None:
    """Round-trip: parse → re-render → expect identical bytes (idempotence)."""
    texts = build_manifest_texts(WITHIN_MCP_METADATA)
    for path, text in texts.items():
        parsed = json.loads(text)
        reserialized = render_manifest(parsed)
        assert reserialized == text, f"render is not idempotent for {path}"


def test_no_path_traversal_in_any_generated_manifest() -> None:
    """No field value (string-typed, anywhere) may contain a `..` path segment."""
    texts = build_manifest_texts(WITHIN_MCP_METADATA)

    def walk(node: object, where: str) -> None:
        if isinstance(node, str):
            assert ".." not in node, f"path-traversal substring `..` found in {where}: {node!r}"
        elif isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{where}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{where}[{i}]")

    for path, text in texts.items():
        walk(json.loads(text), str(path.name))


def test_claude_plugin_mcp_servers_path_resolves_to_real_file():
    """Vendor-runtime fidelity: Claude resolves manifest.mcpServers from the plugin
    root. This test mirrors the actual Claude binary's `ms()` loader behavior.
    """
    plugin_manifest_path = CLAUDE_PLUGIN_DIR / "plugin.json"
    plugin_root = plugin_manifest_path.parent.parent  # repo root, two levels up
    manifest = json.loads(plugin_manifest_path.read_text())
    mcp_ref = manifest["mcpServers"]
    assert isinstance(mcp_ref, str), "this test only handles the string-pointer form"
    # Claude's loader joins plugin root + the string. Strip leading './' as a prefix
    # (not via lstrip, which would also strip leading dots from a dotfile like .mcp.json).
    mcp_path = (plugin_root / mcp_ref.removeprefix("./")).resolve()
    assert mcp_path.exists(), (
        f"manifest.mcpServers points to {mcp_ref!r}, which resolves to "
        f"{mcp_path}, but no file is committed there. Claude users would "
        "install this plugin and silently get zero MCP servers registered."
    )
