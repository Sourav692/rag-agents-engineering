"""Copy one course part into the per-part layout, leaving course/ and theory/ untouched.

    uv run python scripts/restructure_part.py p01_ai_engineering_foundations

Layout written at the repo root:

    <part>/README.md                      course/<part>/README.md
    <part>/<module>/README.md, lab/, assets/   module-level files from course/<part>/<module>/
    <part>/<module>/mandatory/notebook/   course/<part>/<module>/notebooks/**
    <part>/<module>/optional/notebook/    course/<part>/<module>/{optional,exercises}/**
    <part>/<module>/mandatory/theory/     module page, index.html, module diagrams, and the pages of
                                          lessons with a mandatory notebook (or no notebook at all)
    <part>/<module>/optional/theory/      pages of lessons whose notebooks are all optional

Relative paths in .md, .ipynb, .html and .py files are re-pointed: a target inside the copied
part goes to its copy, any other target keeps pointing at its original location.
"""
from __future__ import annotations

import os
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import curriculum_lib as cl  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEXT = {".md", ".ipynb", ".html", ".py"}
SKIP = {".ipynb_checkpoints", "__pycache__", ".DS_Store"}
# A Markdown link target, an HTML href/src, or a bare ../ path inside code.
REF = re.compile(r"""(\]\(\s*<?)([^)\s>]+)|((?:href|src|data-src)=["'])([^"']+)|((?:\.\./)+[\w./-]*)""")


def plan(part: str) -> dict[Path, Path]:
    """Map every source file of the part to its destination."""
    mods = [m for m in cl.load()["modules"] if cl.theory_dir(m).split("/")[1] == part]
    if not mods:
        sys.exit(f"no modules in part {part!r}")
    course, out = ROOT / "course" / part, ROOT / part
    moves: dict[Path, Path] = {}

    def add_tree(src: Path, dst: Path) -> None:
        for f in src.rglob("*") if src.is_dir() else [src]:
            if f.is_file() and not SKIP & set(f.parts):
                moves[f] = dst / f.relative_to(src) if src.is_dir() else dst

    add_tree(course / "README.md", out / "README.md")
    for m in mods:
        cm, tm, om = course / m["folder"], ROOT / cl.theory_dir(m), out / m["folder"]
        for child in cm.iterdir():
            tier = {"notebooks": "mandatory", "optional": "optional", "exercises": "optional"}.get(child.name)
            add_tree(child, om / tier / "notebook" if tier else om / child.name)
        lessons = {cl.lesson_folder(i, l["title"]): l for i, l in enumerate(m["lessons"], 1)}
        for child in tm.iterdir():
            l = lessons.get(child.name)
            optional = bool(l and l["items"] and all(it["tier"] != "mandatory" for it in l["items"]))
            add_tree(child, om / ("optional" if optional else "mandatory") / "theory" / child.name)
    return moves


def repoint(text: str, src: Path, dst: Path, moves: dict[Path, Path]) -> str:
    def fix(match: re.Match) -> str:
        g = match.groups()
        pre, target = (g[0], g[1]) if g[1] else (g[2], g[3]) if g[3] else ("", g[4])
        if re.match(r"[a-z][a-z0-9+.-]*:|[#/]", target):  # URL, anchor or absolute path
            return match.group(0)
        path, sep, frag = re.match(r"([^#?]*)([#?]?)(.*)", target).groups()
        old = (src.parent / urllib.parse.unquote(path)).resolve()
        if not path or not old.exists() or ROOT != old and ROOT not in old.parents:
            return match.group(0)
        if old in moves:
            new = moves[old]
        else:  # a directory: follow it when its files moved, otherwise keep the original
            inside = next((f for f in moves if old in f.parents), None)
            new = moves[inside].parents[len(inside.relative_to(old).parts) - 1] if inside else old
        rel = Path(os.path.relpath(new, dst.parent)).as_posix() + ("/" if path.endswith("/") else "")
        return f"{pre}{urllib.parse.quote(rel) if '%' in path else rel}{sep}{frag}"

    return REF.sub(fix, text)


def main() -> None:
    part = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    moves = plan(part)
    for src, dst in moves.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in TEXT:
            dst.write_text(repoint(src.read_text(), src, dst, moves))
        else:
            shutil.copy2(src, dst)
    print(f"{len(moves)} files copied into {part}/")


if __name__ == "__main__":
    main()
