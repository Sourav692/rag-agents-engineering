"""Check that relative links in Markdown files and notebook markdown cells resolve inside the repo.

    uv run python scripts/check_links.py

docs/source/ holds archived copies of the source repos' docs; their links point at the
source repos' layout, so they are not checked.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".git", ".venv", ".ipynb_checkpoints", "__pycache__", "node_modules"}
ARCHIVED = ("docs/source/",)
MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
IMG_TAG = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.I)


def markdown_of(p: Path) -> str:
    if p.suffix == ".md":
        return p.read_text(encoding="utf-8", errors="ignore")
    try:
        nb = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    return "\n".join("".join(c.get("source", [])) for c in nb.get("cells", []) if c.get("cell_type") == "markdown")


def broken_links() -> list[str]:
    out = []
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT).as_posix()
        if not p.is_file() or p.suffix not in (".md", ".ipynb") or SKIP & set(p.relative_to(ROOT).parts):
            continue
        if rel.startswith(ARCHIVED):
            continue
        md = markdown_of(p)
        for target in MD_LINK.findall(md) + IMG_TAG.findall(md):
            if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#)", target, re.I):
                continue
            path = urllib.parse.unquote(target.split("#")[0].split("?")[0])
            if path and not (p.parent / path).resolve().exists():
                out.append(f"{rel}: {target}")
    return out


if __name__ == "__main__":
    bad = broken_links()
    print("\n".join(bad) or "all relative links resolve")
    print(f"{len(bad)} broken link(s)")
    sys.exit(1 if bad else 0)
