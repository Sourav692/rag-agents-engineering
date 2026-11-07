"""Shared helpers for reading curriculum.yaml.

Every script in scripts/ and every test goes through this module, so the rules for where a file
lives are in one place. One folder per part at the repo root:

    <part>/<module>/{mandatory,optional}/notebook/   items (`folder` names it) and their helper files
    <part>/<module>/projects/                        runnable sub-projects
    <part>/<module>/mandatory/theory/                module page, index.html, module diagrams, lesson pages
    <part>/<module>/optional/theory/                 pages of lessons whose notebooks are all optional
    <part>/<module>/lab/                             brief, solution/ and data/ (hand-maintained)
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "curriculum.yaml"
PART_GLOB = "p[0-9][0-9]_*"  # the part folders at the repo root
THEORY_INDEX = "THEORY.md"  # generated index of every theory page
TIERS = ("mandatory", "alternate", "platform", "extension")


@dataclass(frozen=True)
class Item:
    """One file (notebook, script or folder) placed in one lesson."""

    module: dict
    lesson_no: int  # 0 for the module lab notebook
    lesson_title: str
    repo: str  # source repo key, e.g. "05"
    source_path: str  # path relative to the source repo root
    tier: str
    folder: str  # mandatory/notebook | optional/notebook (either with a subfolder) | projects
    file: str

    @property
    def dest(self) -> str:
        """Path of the file relative to the repo root."""
        return f"{module_dir(self.module)}/{self.folder}/{self.file}"

    @property
    def optional(self) -> bool:
        return self.tier != "mandatory"

    @property
    def is_notebook(self) -> bool:
        return self.source_path.endswith(".ipynb")


_PART_FOLDER: dict[str, str] = {}


def load(path: Path = CURRICULUM) -> dict:
    cur = yaml.safe_load(path.read_text())
    _PART_FOLDER.clear()
    _PART_FOLDER.update({p["id"]: p["folder"] for p in cur["parts"]})
    return cur


def module_dir(module: dict) -> str:
    return f"{_PART_FOLDER[module['part']]}/{module['folder']}"


def theory_dir(module: dict) -> str:
    """The folder of the module page (README.md, index.html and module diagrams)."""
    return f"{module_dir(module)}/mandatory/theory"


def lesson_folder(n: int, title: str) -> str:
    """A lesson's theory folder: lesson number and slugged title, e.g. 03_numpy_pandas_and_matplotlib."""
    return f"{n:02d}_{re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')}"


def lesson_tier(lesson: dict) -> str:
    """`optional` when the lesson has items and none is mandatory, else `mandatory`."""
    its = lesson["items"]
    return "optional" if its and all(it["tier"] != "mandatory" for it in its) else "mandatory"


def lesson_dir(module: dict, n: int) -> str:
    """Theory folder of lesson n (1-based): <module>/<tier>/theory/<NN>_<slug of title>."""
    les = module["lessons"][n - 1]
    return f"{module_dir(module)}/{lesson_tier(les)}/theory/{lesson_folder(n, les['title'])}"


def lesson_pages(module: dict) -> dict[int, str]:
    """Lesson number -> its theory page, for the lessons that have one."""
    return {n: f"{lesson_dir(module, n)}/README.md" for n in range(1, len(module["lessons"]) + 1)
            if (ROOT / lesson_dir(module, n) / "README.md").exists()}


def items(cur: dict) -> list[Item]:
    out = []
    for m in cur["modules"]:
        for n, lesson in enumerate(m["lessons"], 1):
            for it in lesson["items"]:
                out.append(_item(m, n, lesson["title"], it))
        for it in m.get("lab_items", []):
            out.append(_item(m, 0, "Module lab", it))
    return out


def _item(m: dict, n: int, title: str, it: dict) -> Item:
    repo, path = it["source"].split(":", 1)
    if it["tier"] not in TIERS:
        raise ValueError(f"{it['source']}: unknown tier {it['tier']!r}")
    return Item(m, n, title, repo, path, it["tier"], it["folder"], it["file"])


def source_module(path: str) -> str:
    """Top-level grouping of a source path: the module folder, or e.g. 'solutions'."""
    parts = path.split("/")
    return parts[1] if parts[0] == "modules" else parts[0]
