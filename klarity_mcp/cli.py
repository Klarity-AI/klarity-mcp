"""CLI for klarity-mcp: regenerate or check the public plugin manifests."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from klarity_mcp.builders import build_manifest_texts
from klarity_mcp.metadata import KLARITY_MCP_METADATA, REPO_ROOT


_REMEDIATION_HINT = (
    "Generated manifests are out of date. Run `python -m klarity_mcp --write` "
    "from the repo root and commit the result."
)


def _write(texts: dict[Path, str]) -> int:
    written = 0
    for path, text in texts.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_text(encoding="utf-8") == text:
            continue
        path.write_text(text, encoding="utf-8")
        rel = path.relative_to(REPO_ROOT)
        print(f"wrote {rel}")
        written += 1
    if written == 0:
        print("no changes; manifests already up to date")
    return 0


def _check(texts: dict[Path, str]) -> int:
    drift: list[Path] = []
    for path, text in texts.items():
        if not path.exists():
            drift.append(path)
            continue
        if path.read_text(encoding="utf-8") != text:
            drift.append(path)
    if not drift:
        print("manifests are in sync")
        return 0
    for path in drift:
        rel = path.relative_to(REPO_ROOT)
        print(f"drift: {rel}", file=sys.stderr)
    print(_REMEDIATION_HINT, file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="klarity_mcp")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="regenerate the public manifests")
    group.add_argument("--check", action="store_true", help="exit 1 if any committed manifest is stale")
    args = parser.parse_args(argv)

    texts = build_manifest_texts(KLARITY_MCP_METADATA)

    if args.write:
        return _write(texts)
    return _check(texts)


if __name__ == "__main__":
    raise SystemExit(main())
