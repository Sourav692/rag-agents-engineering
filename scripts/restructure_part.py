"""Copy one v2 course part out of course/ and theory/ into the per-part layout, leaving both untouched.

    uv run python scripts/restructure_part.py p07_advanced_agents

curriculum.v2.yaml drives the copy: a v2 module's `previous_num` names the v1 module it continues,
a lesson's `previous` ("24.5") names the v1 lesson whose page it takes, and an item's
`previous_path` names the v1 file it copies. Layout written at the repo root:

    <part>/README.md                          course/<v1 part>/README.md of the part's first module
    <part>/<module>/README.md, lab/, assets/, projects/   module-level files of the v1 module
    <part>/<module>/mandatory/notebook/       mandatory items, and helper files from v1 notebooks/
    <part>/<module>/optional/notebook/        other items, and helper files from v1 optional/, exercises/
    <part>/<module>/mandatory/theory/         module page, index.html, module diagrams, and the pages of
                                              lessons with a mandatory notebook (or no notebook at all)
    <part>/<module>/optional/theory/          pages of lessons whose notebooks are all optional

Relative paths in .md, .ipynb, .html and .py files are re-pointed (a target inside the copy goes to
its copy, any other target keeps pointing at its original location), then module codes and lesson
numbers are rewritten to v2. Existing files under lab/ are never overwritten.
"""
from __future__ import annotations

import os
import re
import shutil
import sys
import urllib.parse
from pathlib import Path
from typing import Callable

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import curriculum_lib as cl  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEXT = {".md", ".ipynb", ".html", ".py"}
SKIP = {".ipynb_checkpoints", "__pycache__", ".DS_Store"}
TIER_OF = {"notebooks": "mandatory", "optional": "optional", "exercises": "optional"}
TIER_DIRS = ("mandatory/theory", "mandatory/notebook", "optional/theory", "optional/notebook")
# A Markdown link target, an HTML href/src, or a bare ../ path inside code.
REF = re.compile(r"""(\]\(\s*<?)([^)\s>]+)|((?:href|src|data-src)=["'])([^"']+)|((?:\.\./)+[\w./-]*)""")
BARE = re.compile(r"(?:\.\./)+[\w./-]*")
# Not SVG path data ("M24 10", "M24,10").
MODULE_CODE = re.compile(r"\bM(\d{2})\b(?![\s,]*-?\d)(?!\.\d)")
# Lesson numbers only after "Lesson(s) " (a list such as "lessons 26.1 and 26.4" counts), as a whole
# table cell, or at the start of a link text.
NO = r"\d+\.\d+(?!\d)"
LESSON_NO = re.compile(rf"(\b[Ll]essons? |\|[ \t]*|\[)({NO}(?:(?:,? and |, | to | or |\u2013|-){NO})*)")


def load_v2(path: Path = ROOT / "curriculum.v2.yaml") -> dict:
    return yaml.safe_load(path.read_text())


def _v1() -> dict[int, dict]:
    return {m["num"]: m for m in cl.load()["modules"]}  # cl.load() also sets v1 part folders for theory_dir


def _v1_of(m: dict) -> int:
    """The v1 module a v2 module continues; a new module counts as its first lesson's v1 module."""
    return m.get("previous_num") or int(m["lessons"][0]["previous"].split(".")[0])


def _items(m: dict) -> list[dict]:
    return [it for l in m["lessons"] for it in l["items"]] + m.get("lab_items", [])


def maps(v2: dict) -> tuple[dict[int, int], dict[str, str]]:
    """v1 to v2 module numbers and lesson numbers."""
    modules = {m["previous_num"]: m["num"] for m in v2["modules"] if m.get("previous_num")}
    lessons = {l["previous"]: f"{m['num']}.{j}" for m in v2["modules"] for j, l in enumerate(m["lessons"], 1)}
    return modules, lessons


def plan(part: str, v2: dict) -> dict[Path, Path]:
    """Map every source file of the v2 part to its destination."""
    folder = {p["id"]: p["folder"] for p in v2["parts"]}
    mods = [m for m in v2["modules"] if folder[m["part"]] == part]
    if not mods:
        sys.exit(f"no modules in part {part!r}")
    v1, out = _v1(), ROOT / part
    moves: dict[Path, Path] = {}

    def files(src: Path) -> list[Path]:
        return [f for f in (src.rglob("*") if src.is_dir() else [src]) if f.is_file() and not SKIP & set(f.parts)]

    def add_tree(src: Path, dst: Path) -> None:
        for f in files(src):
            if f not in claimed:
                moves.setdefault(f, dst / f.relative_to(src) if src.is_dir() else dst)

    # Files placed by an item anywhere in v2 are copied only by that item.
    claimed = {f for m in v2["modules"] for it in _items(m) for f in files(ROOT / it["previous_path"])}
    v1_part = cl.module_dir(v1[_v1_of(mods[0])]).split("/")[1]
    moves[ROOT / "course" / v1_part / "README.md"] = out / "README.md"

    for m in mods:
        om = out / m["folder"]
        for it in _items(m):
            first, *sub = it["folder"].split("/")
            base = om / "projects" if first == "projects" else om / TIER_OF[first if it["tier"] == "mandatory" else "optional"] / "notebook"
            src, dst = ROOT / it["previous_path"], base.joinpath(*sub, it["file"])
            for f in files(src):
                moves[f] = dst / f.relative_to(src) if src.is_dir() else dst
        for j, l in enumerate(m["lessons"], 1):
            a, b = map(int, l["previous"].split("."))
            src = ROOT / cl.theory_dir(v1[a]) / cl.lesson_folder(b, v1[a]["lessons"][b - 1]["title"])
            optional = bool(l["items"]) and all(it["tier"] != "mandatory" for it in l["items"])
            dst = om / ("optional" if optional else "mandatory") / "theory" / cl.lesson_folder(j, l["title"])
            if src.is_dir():
                for f in files(src):
                    moves[f] = dst / f.relative_to(src)
        if not m.get("previous_num"):
            continue
        claimed |= set(moves)
        old = v1[m["previous_num"]]
        cm, tm = ROOT / cl.module_dir(old), ROOT / cl.theory_dir(old)
        for child in sorted(cm.iterdir()):
            tier = TIER_OF.get(child.name)
            add_tree(child, om / tier / "notebook" if tier else om / child.name)
        pages = {cl.lesson_folder(i, l["title"]) for i, l in enumerate(old["lessons"], 1)}
        for child in sorted(tm.iterdir()) if tm.is_dir() else []:
            if child.name not in pages:
                add_tree(child, om / "mandatory" / "theory" / child.name)
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


def renumber_prose(text: str, modules: dict[int, int], lessons: dict[str, str]) -> str:
    """Rewrite M<NN> codes and, in marked contexts only, lesson numbers from v1 to v2."""
    text = MODULE_CODE.sub(lambda mt: f"M{modules.get(int(mt[1]), int(mt[1])):02d}", text)

    def lesson(mt: re.Match) -> str:
        pre, no = mt[1], mt[2]
        if pre.startswith("|") and not re.match(r"[ \t]*\|", text[mt.end():]):
            return mt[0]  # a table cell must hold only the number
        if pre == "[" and not re.match(r"[\s\]]", text[mt.end():mt.end() + 1]):
            return mt[0]
        return pre + re.sub(NO, lambda n: lessons.get(n[0], n[0]), no)

    return LESSON_NO.sub(lesson, text)


def copy_all(moves: dict[Path, Path], v2: dict, protect: Callable[[Path], bool]) -> tuple[int, int]:
    modules, lessons = maps(v2)
    copied = skipped = 0
    for src, dst in moves.items():
        if protect(dst) and dst.exists():
            skipped += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in TEXT:
            dst.write_text(renumber_prose(repoint(src.read_text(), src, dst, moves), modules, lessons))
        else:
            shutil.copy2(src, dst)
        copied += 1
    return copied, skipped


def is_lab_file(dst: Path) -> bool:
    return "lab" in dst.resolve().relative_to(ROOT).parts[1:]


def ensure_tiers(module_dir: Path) -> None:
    for t in TIER_DIRS:
        d = module_dir / t
        d.mkdir(parents=True, exist_ok=True)
        if not any(d.iterdir()):
            (d / ".gitkeep").touch()


def report(part: str, v2: dict) -> list[str]:
    """Bare ../ targets that do not exist, and v1 names of renamed items still present, in the copy."""
    out, root = [], ROOT / part
    copied = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in TEXT)
    for p in copied:
        if p.suffix in (".ipynb", ".py"):
            for target in sorted(set(BARE.findall(p.read_text()))):
                if not (p.parent / target).resolve().exists():
                    out.append(f"unresolved: {p.relative_to(ROOT)}: {target}")
    folder = {x["id"]: x["folder"] for x in v2["parts"]}
    renamed = {Path(it["previous_path"]).stem: it["file"] for m in v2["modules"] if folder[m["part"]] == part
               for it in _items(m) if Path(it["previous_path"]).name != it["file"]}
    for p in copied:
        text = p.read_text()
        for old, new in sorted(renamed.items()):
            if old in text:
                out.append(f"old name: {p.relative_to(ROOT)}: {old} (now {new})")
    return out


def lab_stub(m: dict) -> str:
    return (f"# Lab: M{m['num']:02d} {m['title']}\n\n## Brief\n\n{m['lab']}\n\n"
            "Back to the part: [README.md](../../README.md)\n")  # a new module has no README until Phase 6


def main() -> None:
    part = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    v2 = load_v2()
    moves = plan(part, v2)
    copied_to = set(moves.values())
    copied, skipped = copy_all(moves, v2, protect=is_lab_file)
    folder = {p["id"]: p["folder"] for p in v2["parts"]}
    for m in (m for m in v2["modules"] if folder[m["part"]] == part):
        md = ROOT / part / m["folder"]
        ensure_tiers(md)
        lab = md / "lab" / "README.md"
        if lab.exists():
            skipped += lab not in copied_to
        else:  # a module new in v2 has no v1 lab page
            lab.parent.mkdir(parents=True, exist_ok=True)
            lab.write_text(lab_stub(m))
            copied += 1
    print(f"{copied} files copied, {skipped} skipped into {part}/")
    print("\n".join(report(part, v2)) or "report: nothing to review")


if __name__ == "__main__":
    main()
