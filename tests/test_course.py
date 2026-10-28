"""Offline checks: `uv run pytest` must pass on a clean clone with no API keys and no source repos."""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from check_links import broken_links  # noqa: E402
from curriculum_lib import COURSE_DIR, TIERS, items, load  # noqa: E402

CUR = load()
ITEMS = items(CUR)
COURSE_NOTEBOOKS = sorted(
    p.relative_to(ROOT).as_posix() for p in (ROOT / COURSE_DIR).rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts
)


def test_every_curriculum_item_exists():
    missing = [it.dest for it in ITEMS if not (ROOT / it.dest).exists()]
    assert not missing, missing


def test_every_course_notebook_is_in_exactly_one_lesson():
    placed = Counter(it.dest for it in ITEMS if it.is_notebook)
    assert set(COURSE_NOTEBOOKS) == set(placed), set(COURSE_NOTEBOOKS) ^ set(placed)
    assert all(n == 1 for n in placed.values())


def test_tiers_and_folders_agree():
    assert all(it.tier in TIERS for it in ITEMS)
    for it in ITEMS:
        top = it.folder.split("/")[0]
        assert top in ("notebooks", "optional", "exercises", "projects"), it.dest
        if top == "notebooks":
            assert it.tier == "mandatory", it.dest
        if top == "optional":
            assert it.tier != "mandatory", it.dest


def test_modules_are_numbered_in_order():
    assert [m["num"] for m in CUR["modules"]] == list(range(1, len(CUR["modules"]) + 1))


def test_notebooks_are_valid_json():
    bad = []
    for rel in COURSE_NOTEBOOKS:
        try:
            nb = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            assert isinstance(nb.get("cells"), list) and "nbformat" in nb
        except (json.JSONDecodeError, AssertionError):
            bad.append(rel)
    assert not bad, bad


def test_no_paths_left_at_the_source_repo_depth():
    stale = re.compile(r"(?<!\.\./)\.\./\.\./\.\./(?:data|docs|src)/")
    bad = [rel for rel in COURSE_NOTEBOOKS if stale.search((ROOT / rel).read_text(encoding="utf-8"))]
    assert not bad, bad


def test_relative_links_resolve():
    assert broken_links() == []


def test_rag_paths_finds_this_repo_and_its_assets():
    import rag_paths

    assert rag_paths.repo_root(ROOT / COURSE_DIR) == ROOT
    missing = [r for r in rag_paths.ASSET_ROOTS if not (ROOT / r).is_dir()]
    assert not missing, missing


def test_scripts_compile():
    for script in (ROOT / "scripts").glob("*.py"):
        subprocess.run([sys.executable, "-m", "py_compile", str(script)], check=True)
