"""One-time steps of the Phase 6 switch (plan/phase-6-switch.md), kept as history.

    uv run python plan/switch_v2.py content [--dry-run]   # Task 6.1: re-point part-folder content off course/ and theory/
    uv run python plan/switch_v2.py curriculum            # Task 6.2: curriculum.yaml becomes v2

`content` needs the v1 trees, the v1 curriculum.yaml and curriculum.v2.yaml, so it runs before
`curriculum`; both refuse to run once their input is gone.
"""
from __future__ import annotations

import os
import re
import sys
import urllib.parse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GH = re.compile(r"(https://github\.com/Sourav692/rag-agents-engineering/(?:blob|tree)/main/)((?:course|theory)(?:/[^\s\"'<>)#?]*)?)")
NO = r"\d{1,2}\.\d{1,2}"
PAREN = re.compile(rf"\(({NO}(?:(?:, and |, | and | or | to |–){NO})*)\)")
NOTEBOOK = re.compile(rf"(\bnotebooks? )({NO})\b(?!\.\d)|(\bthe )({NO})(?=(?:'s)? notebook)")
OLD = ("course", "theory")


def old_tree(p: Path) -> bool:
    try:
        return p.relative_to(ROOT).parts[:1] in (("course",), ("theory",))
    except ValueError:
        return False


def moves_and_dirs(v2: dict) -> tuple[dict[Path, Path], dict[Path, Path]]:
    """Every old file to its new path, and old module, part and index paths to their new folders."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import curriculum_lib as cl
    import restructure_part as rp

    moves: dict[Path, Path] = {}
    for p in v2["parts"]:
        for src, dst in rp.plan(p["folder"], v2).items():
            moves.setdefault(src, dst)
    v1 = {m["num"]: m for m in cl.load()["modules"]}
    folder = {p["id"]: p["folder"] for p in v2["parts"]}
    dirs = {ROOT / "course": ROOT, ROOT / "theory": ROOT}
    for m in v2["modules"]:
        new = ROOT / folder[m["part"]] / m["folder"]
        if m.get("previous_num"):
            old = v1[m["previous_num"]]
            dirs[ROOT / cl.module_dir(old)] = new
            dirs[ROOT / cl.theory_dir(old)] = new / "mandatory" / "theory"
            dirs.setdefault(ROOT / cl.module_dir(old).rsplit("/", 1)[0], new.parent)
            dirs.setdefault(ROOT / cl.theory_dir(old).rsplit("/", 1)[0], new.parent)
    moves[ROOT / "theory" / "README.md"] = ROOT / "THEORY.md"
    moves[ROOT / "course" / "README.md"] = ROOT / "README.md"
    return moves, dirs


def new_path(old: Path, moves: dict[Path, Path], dirs: dict[Path, Path]) -> Path | None:
    if old in moves:
        return moves[old]
    if old in dirs:
        return dirs[old]
    inside = next((f for f in moves if old in f.parents), None)  # a folder below module level
    if inside:
        return moves[inside].parents[len(inside.relative_to(old).parts) - 1]
    return None


def repoint(text: str, here: Path, moves, dirs, misses: list) -> str:
    import restructure_part as rp

    def fix(match: re.Match) -> str:
        g = match.groups()
        pre, target = (g[0], g[1]) if g[1] else (g[2], g[3]) if g[3] else ("", g[4])
        if re.match(r"[a-z][a-z0-9+.-]*:|[#/]", target):
            return match.group(0)
        path, sep, frag = re.match(r"([^#?]*)([#?]?)(.*)", target).groups()
        old = (here.parent / urllib.parse.unquote(path)).resolve()
        if not path or not old_tree(old):
            return match.group(0)
        new = new_path(old, moves, dirs)
        if new is None:
            misses.append(f"{here.relative_to(ROOT)}: {target}")
            return match.group(0)
        rel = Path(os.path.relpath(new, here.parent)).as_posix() + ("/" if path.endswith("/") else "")
        return f"{pre}{urllib.parse.quote(rel) if '%' in path else rel}{sep}{frag}"

    def gh(match: re.Match) -> str:
        path = match.group(2).rstrip("/")
        new = new_path(ROOT / urllib.parse.unquote(path), moves, dirs)
        if new is None:
            misses.append(f"{here.relative_to(ROOT)}: {match.group(0)}")
            return match.group(0)
        base = match.group(1)
        kind = "tree" if new.is_dir() or not new.suffix else "blob"
        base = re.sub(r"/(?:blob|tree)/main/$", f"/{kind}/main/", base)
        return base + ("" if new == ROOT else new.relative_to(ROOT).as_posix())

    return GH.sub(gh, rp.REF.sub(fix, text))


def renumber_parens(text: str, lessons: dict[str, str]) -> str:
    """v1 lesson numbers in parentheses ("(16.1, 16.3)") and next to "notebook", only when every number is a v1 lesson."""
    def paren(mt: re.Match) -> str:
        nums = re.findall(NO, mt.group(1))
        if not all(n in lessons for n in nums):
            return mt.group(0)
        return "(" + re.sub(NO, lambda n: lessons[n.group(0)], mt.group(1)) + ")"

    text = PAREN.sub(paren, text)
    def notebook(mt: re.Match) -> str:
        pre, no = (mt.group(1), mt.group(2)) if mt.group(1) else (mt.group(3), mt.group(4))
        return pre + lessons.get(no, no)

    return NOTEBOOK.sub(notebook, text)


def module_pages(v2: dict) -> None:
    """Meta line and, for retitled modules, title line of each module page, in v2 wording."""
    parts = {p["id"]: p for p in v2["parts"]}
    titles = {"convmemory": "Short-term memory and conversation state",
              "finetune": "Fine-tuning and model adaptation",
              "architecture": "Architecture synthesis: choosing a system design"}
    for m in v2["modules"]:
        page = ROOT / parts[m["part"]]["folder"] / m["folder"] / "mandatory" / "theory" / "README.md"
        lines = page.read_text().split("\n")
        p = parts[m["part"]]
        index = os.path.relpath(ROOT / "THEORY.md", page.parent)
        assert lines[2].startswith("*Part "), page
        lines[2] = f"*Part {p['num']} · {p['title']} · [Module README](../../README.md) · [All theory pages]({index})*"
        if m["key"] in titles:
            lines[0] = f"# M{m['num']:02d} Theory: {titles[m['key']]}"
        page.write_text("\n".join(lines))


def content(dry: bool) -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import restructure_part as rp

    v2 = rp.load_v2()
    moves, dirs = moves_and_dirs(v2)
    _, lessons = rp.maps(v2)
    files = [p for d in sorted(ROOT.glob("p[0-9][0-9]_*")) for p in d.rglob("*")
             if p.is_file() and p.suffix in (".md", ".ipynb", ".html", ".py") and ".ipynb_checkpoints" not in p.parts]
    files += [ROOT / "docs" / "ai-system-design" / "index.html"]
    misses: list[str] = []
    changed = 0
    for f in files:
        text = f.read_text()
        new = repoint(text, f, moves, dirs, misses)
        if f.suffix == ".md" and "/theory/" in f.as_posix():
            new = renumber_parens(new, lessons)
        if new != text:
            changed += 1
            if not dry:
                f.write_text(new)
    if not dry:
        module_pages(v2)
    print(f"{changed} files {'would change' if dry else 'changed'}; {len(misses)} references not mapped")
    print("\n".join(misses))
    # every old file has a copy (generated READMEs and index pages are rebuilt instead)
    left = [p.relative_to(ROOT).as_posix() for t in OLD for p in (ROOT / t).rglob("*")
            if p.is_file() and p not in moves and p.name not in (".DS_Store",) and ".ipynb_checkpoints" not in p.parts]
    print(f"{len(left)} old files without a copy:")
    print("\n".join(left))


def curriculum() -> None:
    src = ROOT / "curriculum.v2.yaml"
    if not src.exists():
        sys.exit("curriculum.v2.yaml is gone: curriculum.yaml is already v2")
    cur = yaml.safe_load(src.read_text())
    for m in cur["modules"]:
        for it in [it for l in m["lessons"] for it in l["items"]] + (m.get("lab_items") or []):
            del it["previous_path"]
            first, *sub = it["folder"].split("/")
            if first != "projects":
                it["folder"] = "/".join(["mandatory" if it["tier"] == "mandatory" else "optional", "notebook", *sub])
    folder = {p["id"]: p["folder"] for p in cur["parts"]}
    missing = [f"{folder[m['part']]}/{m['folder']}/{it['folder']}/{it['file']}" for m in cur["modules"]
               for it in [it for l in m["lessons"] for it in l["items"]] + (m.get("lab_items") or [])
               if not (ROOT / folder[m["part"]] / m["folder"] / it["folder"] / it["file"]).exists()]
    assert not missing, missing
    header = (
        "# Single source of truth for the course: parts, modules, lessons, and where every file lives.\n"
        "# Each item lives at <part folder>/<module folder>/<folder>/<file>, where <folder> is mandatory/notebook,\n"
        "# optional/notebook (either with an optional subfolder) or projects. `source` records where an item came from in\n"
        "# the archived source repos; `previous_num` (module), `previous` (lesson) and `previous_title` (part) record the v1\n"
        "# curriculum it replaced on 8 Nov 2026 (plan/phase-6-switch.md). Hand-maintained: edit it, then run\n"
        "# scripts/build_curriculum.py, which renders CURRICULUM.md, the part and module READMEs and the docs site.\n"
        "# source format: <repo key>:<path relative to that source repo's root>. tier: mandatory | alternate | platform | extension\n")
    (ROOT / "curriculum.yaml").write_text(header + yaml.safe_dump(cur, sort_keys=False, allow_unicode=True, width=120))
    src.unlink()
    print(f"curriculum.yaml: {len(cur['parts'])} parts, {len(cur['modules'])} modules")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    if cmd == "content":
        if not (ROOT / "course").is_dir() or not (ROOT / "curriculum.v2.yaml").exists():
            sys.exit("the v1 trees or curriculum.v2.yaml are gone: content was re-pointed already")
        content("--dry-run" in sys.argv)
    elif cmd == "curriculum":
        curriculum()
    else:
        sys.exit(__doc__)
