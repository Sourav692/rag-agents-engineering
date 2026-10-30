"""Shared helpers for reading curriculum.yaml.

Every script in scripts/ and every test goes through this module, so the rules for
where a file comes from and where it lands live in one place.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "curriculum.yaml"
COURSE_DIR = "course"
THEORY_DIR = "theory"
TIERS = ("mandatory", "alternate", "platform", "extension")


@dataclass(frozen=True)
class Item:
    """One source file (notebook, script or folder) placed in one lesson."""

    module: dict
    lesson_no: int  # 0 for the module lab notebook
    lesson_title: str
    repo: str  # source repo key, e.g. "05"
    source_path: str  # path relative to the source repo root
    tier: str
    folder: str  # notebooks | optional | exercises
    file: str

    @property
    def dest(self) -> str:
        """Path of the copied file relative to the course repo root."""
        return f"{module_dir(self.module)}/{self.folder}/{self.file}"

    @property
    def optional(self) -> bool:
        return self.tier != "mandatory"

    @property
    def is_notebook(self) -> bool:
        return self.source_path.endswith(".ipynb")

    @property
    def source_dir(self) -> str:
        """Folder holding the source file; its other files travel with it."""
        return self.source_path.rsplit("/", 1)[0]


_PART_FOLDER: dict[str, str] = {}


def load(path: Path = CURRICULUM) -> dict:
    cur = yaml.safe_load(path.read_text())
    _PART_FOLDER.clear()
    _PART_FOLDER.update({p["id"]: p["folder"] for p in cur["parts"]})
    return cur


def module_dir(module: dict) -> str:
    return f"{COURSE_DIR}/{_PART_FOLDER[module['part']]}/{module['folder']}"


def theory_dir(module: dict) -> str:
    """theory/ mirrors course/: theory/<part folder>/<module folder>."""
    return f"{THEORY_DIR}/{_PART_FOLDER[module['part']]}/{module['folder']}"


def lesson_folder(n: int, title: str) -> str:
    """A lesson's theory folder: lesson number and slugged title, e.g. 03_numpy_pandas_and_matplotlib."""
    return f"{n:02d}_{re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')}"


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


def source_root(cur: dict, sources_dir: Path, repo: str) -> Path:
    return sources_dir / cur["sources"][repo]["repo"]


def source_module(path: str) -> str:
    """Top-level grouping of a source path: the module folder, or e.g. 'solutions'."""
    parts = path.split("/")
    return parts[1] if parts[0] == "modules" else parts[0]
