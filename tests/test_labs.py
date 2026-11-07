"""Offline checks for the v2 part folders: module tiers, lab solutions and lab data.

Each phase's last task adds its part folders to DONE_PARTS. The other tests run over every part
folder that exists at the repo root.
"""
import filecmp
import json
import re
from pathlib import Path

import nbformat
import yaml

DONE_PARTS: set[str] = {
    "p01_ai_engineering_foundations",
    "p02_prompt_engineering",
    "p03_llm_application_frameworks",
    "p04_rag_foundations",
    "p05_retrieval_quality_and_rag_apps",
    "p06_agent_foundations",
    "p07_advanced_agents",
    "p08_agentic_rag",
    "p09_memory_layer",
    "p10_multi_agent_systems",
    "p11_agent_protocols",
    "p12_knowledge_graphs_and_graph_rag",
    "p13_design_decisions",
}

ROOT = Path(__file__).resolve().parent.parent
TIERS = ("mandatory/theory", "mandatory/notebook", "optional/theory", "optional/notebook")
TOKEN = re.compile(r"sk-[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,}")
REL = re.compile(r"(?:\.\./)+[\w./-]+")
PARTS = sorted(p for p in ROOT.glob("p[0-9][0-9]_*") if p.is_dir())
MODULES = sorted(m for p in PARTS for m in p.glob("m[0-9][0-9]_*") if m.is_dir())
SOLUTIONS = sorted(s for m in MODULES for s in (m / "lab" / "solution").glob("*.ipynb"))
LAB_DATA = sorted(d for m in MODULES if (d := m / "lab" / "data").is_dir())


def _files(d: Path) -> list[str]:
    return sorted(p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file() and p.name != ".DS_Store")


def test_every_module_has_tiers_and_a_lab_readme():
    for m in MODULES:
        for t in TIERS:
            assert (m / t).is_dir(), f"{m.relative_to(ROOT)}: no {t}/"
        assert (m / "lab" / "README.md").is_file(), f"{m.relative_to(ROOT)}: no lab/README.md"


def test_done_parts_have_one_solution_per_module():
    v2 = yaml.safe_load((ROOT / "curriculum.yaml").read_text())
    folder = {p["id"]: p["folder"] for p in v2["parts"]}
    for part in sorted(DONE_PARTS):
        for m in (m for m in v2["modules"] if folder[m["part"]] == part):
            sol = ROOT / part / m["folder"] / "lab" / "solution"
            found = sorted(p.name for p in sol.glob("*.ipynb"))
            assert found == [f"m{m['num']:02d}_solution.ipynb"], f"{part}/{m['folder']}: {found}"


def test_solutions_are_clean():
    for s in SOLUTIONS:
        nb = nbformat.read(s, as_version=4)
        for cell in nb.cells:
            if cell.cell_type == "code":
                assert cell.outputs == [] and cell.execution_count is None, f"{s.relative_to(ROOT)}: outputs not cleared"
        assert not TOKEN.search(s.read_text()), f"{s.relative_to(ROOT)}: holds a token"


def test_solutions_read_only_their_own_data():
    for s in SOLUTIONS:
        lab = s.parent.parent.resolve()
        source = "\n".join("".join(c.get("source", [])) for c in json.loads(s.read_text())["cells"])
        for target in REL.findall(source):
            p = (s.parent / target).resolve()
            ok = p == lab or lab in p.parents or p == ROOT / "src" or ROOT / "src" in p.parents
            assert ok, f"{s.relative_to(ROOT)}: {target} is outside lab/ and src/"


def test_lab_data_has_readme_and_fits():
    for d in LAB_DATA:
        assert (d / "README.md").is_file(), f"{d.relative_to(ROOT)}: no README.md"
        size = sum(p.stat().st_size for p in d.rglob("*") if p.is_file())
        assert size <= 5 * 1024 * 1024, f"{d.relative_to(ROOT)}: {size} bytes"


def test_larkspur_copies_match_canonical():
    canon = ROOT / "data" / "larkspur"
    for d in LAB_DATA:
        copy = d / "larkspur"
        if copy.is_dir():
            assert _files(copy) == _files(canon), f"{copy.relative_to(ROOT)}: file list differs"
            for f in _files(canon):
                assert filecmp.cmp(copy / f, canon / f, shallow=False), f"{copy.relative_to(ROOT)}/{f} differs"
