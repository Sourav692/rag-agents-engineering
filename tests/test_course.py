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
from curriculum_lib import COURSE_DIR, TIERS, items, lesson_folder, load, theory_dir  # noqa: E402

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


def test_architecture_coverage_refs_are_placed():
    """Every notebook (by source path) and module key in docs/agentic-architectures.yaml exists in curriculum.yaml."""
    import yaml

    data = yaml.safe_load((ROOT / "docs/agentic-architectures.yaml").read_text())
    placed = {f"{it.repo}:{it.source_path}" for it in ITEMS}
    keys = {m["key"] for m in CUR["modules"]}
    missing = [s for a in data["architectures"] for s in a["notebooks"] if s not in placed]
    missing += [k for c in data["course_only"] for k in c["modules"] if k not in keys]
    assert not missing, missing


def test_fde_site_slugs_cover_the_curriculum():
    """docs/fde-site-slugs.yaml gives every part, module and lesson one valid, unique site slug."""
    import yaml

    data = yaml.safe_load((ROOT / "docs/fde-site-slugs.yaml").read_text())
    slug = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
    bad = [f"part {p['id']}: no track" for p in CUR["parts"] if p["id"] not in data["tracks"]]
    bad += [f"module {m['key']}: no slug" for m in CUR["modules"] if m["key"] not in data["modules"]]
    for m in CUR["modules"]:
        lessons = data["modules"].get(m["key"], {}).get("lessons", {})
        bad += [f"{m['key']}: lesson {les['title']!r} has no slug" for les in m["lessons"] if les["title"] not in lessons]
    # the site keys lessons by slug alone, so lesson slugs are unique across every module
    lessons = [s for m in data["modules"].values() for s in (m["overview"], m["interview"], *m["lessons"].values())]
    for kind, values in (("track", [t["slug"] for t in data["tracks"].values()]),
                         ("module", [m["slug"] for m in data["modules"].values()]), ("lesson", lessons)):
        bad += [f"duplicate {kind} slug {s}" for s, n in Counter(values).items() if n > 1]
    every = [*(v for t in data["tracks"].values() for v in (t["slug"], t["section"])),
             *(m["slug"] for m in data["modules"].values()), *lessons]
    bad += [f"invalid slug {s}" for s in every if not slug.match(s) or len(s) > 80]
    assert not bad, bad


def test_theory_pages_mirror_the_course_layout():
    """theory/ mirrors course/: module pages at theory/<part>/<module>/, lesson pages in <NN>_<slug of lesson title>/.

    Every key concept has a `##` heading on exactly one of the module's pages, the module page links each lesson
    page, and every lab is linked from the page beside it.
    """
    known = {theory_dir(m): m for m in CUR["modules"]}
    bad = []
    for readme in sorted((ROOT / "theory").glob("**/README.md")):
        rel = readme.relative_to(ROOT).parent.as_posix()
        if rel == "theory" or rel in known:
            continue
        parent = readme.parent.parent.relative_to(ROOT).as_posix()
        m = known.get(parent)
        if not m or readme.parent.name not in {lesson_folder(n, les["title"]) for n, les in enumerate(m["lessons"], 1)}:
            bad.append(f"{rel}: not a module of curriculum.yaml or a lesson folder of one")
    for d, m in known.items():
        page = ROOT / d / "README.md"
        if not page.exists():
            continue
        md = page.read_text(encoding="utf-8")
        lessons = [ROOT / d / lesson_folder(n, les["title"]) / "README.md" for n, les in enumerate(m["lessons"], 1)]
        lessons = [p for p in lessons if p.exists()]
        bad += [f"{d}: lesson page not linked: {p.parent.name}" for p in lessons if f"{p.parent.name}/README.md" not in md]
        heads = Counter(h for p in [page, *lessons] for h in re.findall(r"^## (.+?)\s*$", p.read_text(encoding="utf-8"), re.M))
        bad += [f"{d}: '## {c}' on {heads[c]} pages, want 1" for c in m["concepts"] if heads[c] != 1]
    for lab in sorted((ROOT / "theory").glob("**/interactive/*.html")):
        beside = lab.parent.parent / "README.md"
        if not beside.exists() or f"interactive/{lab.name}" not in beside.read_text(encoding="utf-8"):
            bad.append(f"{lab.relative_to(ROOT)}: not linked from {beside.relative_to(ROOT)}")
    assert not bad, bad


def test_theory_module_pages_have_a_current_index_html():
    """Every module page has the index.html that build_theory_html.py renders from it and its lesson pages."""
    import build_theory_html

    mods = [m for m in CUR["modules"] if (ROOT / theory_dir(m) / "README.md").exists()]
    pages = {f"{theory_dir(m)}/README.md": f"{theory_dir(m)}/index.html" for m in mods}
    stale = [theory_dir(m) for m in mods
             if not (ROOT / theory_dir(m) / "index.html").exists()
             or (ROOT / theory_dir(m) / "index.html").read_text() != build_theory_html.render(m, pages)]
    assert not stale, f"run scripts/build_curriculum.py: {stale}"
