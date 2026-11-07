"""Offline checks for scripts/restructure_part.py, which copies one v2 part out of course/ and theory/."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import restructure_part as rp  # noqa: E402

V2 = rp.load_v2()
P7, M26 = "p07_advanced_agents", "m26_coding_computer_use_and_deep_agents"
V1_M24 = "course/p08_agent_foundations/m24_react_agents"


def test_plan_moves_a_lesson_between_modules():
    moves = rp.plan(P7, V2)
    assert moves[ROOT / f"{V1_M24}/notebooks/05a_web_research_agent.ipynb"] == \
        ROOT / f"{P7}/{M26}/mandatory/notebook/01a_web_research_agent.ipynb"
    page = "applied_react_web_research_swe_and_computer_use_agents/README.md"
    assert moves[ROOT / f"theory/p08_agent_foundations/m24_react_agents/05_{page}"] == \
        ROOT / f"{P7}/{M26}/mandatory/theory/01_{page}"


def test_plan_maps_tiers_for_an_unmoved_module():
    moves = rp.plan("p01_ai_engineering_foundations", V2)
    t = "theory/p01_ai_engineering_foundations/m01_python_data_refresher"
    lesson = "06_concurrency_threads_processes_the_gil_and_asyncio_22_runnable_scripts"
    assert moves[ROOT / f"{t}/{lesson}/README.md"] == \
        ROOT / f"p01_ai_engineering_foundations/m01_python_data_refresher/optional/theory/{lesson}/README.md"


def test_fine_tuning_leaves_part_one():
    moves = rp.plan("p01_ai_engineering_foundations", V2)
    assert not any("m04_fine_tuning" in str(d) for d in moves.values())


def test_renumber_prose():
    mods, lessons = {24: 23, 45: 46}, {"24.5": "26.1", "45.2": "46.2"}
    assert rp.renumber_prose("See M24 and lesson 24.5.", mods, lessons) == "See M23 and lesson 26.1."
    assert rp.renumber_prose("| 45.2 | RAG ecosystem |", mods, lessons) == "| 46.2 | RAG ecosystem |"
    assert rp.renumber_prose("[24.5 Applied ReAct](https://example.com)", mods, lessons) == \
        "[26.1 Applied ReAct](https://example.com)"
    assert rp.renumber_prose("lessons 24.5 and 45.2", mods, lessons) == "lessons 26.1 and 46.2"
    for keep in ("gpt-4.1 and Llama 3.2", "1.5 million rows", "v24.5 of the SDK", '<path d="M24 10 L5 5"/>', "M24,10"):
        assert rp.renumber_prose(keep, mods, lessons) == keep


def test_copy_all_skips_protected_existing(tmp_path):
    a, b = tmp_path / "a.md", tmp_path / "lab" / "README.md"
    a.write_text("new")
    b.parent.mkdir()
    b.write_text("hand-written")
    assert rp.copy_all({a: b}, V2, protect=lambda d: True) == (0, 1)
    assert b.read_text() == "hand-written"


def test_ensure_tiers(tmp_path):
    rp.ensure_tiers(tmp_path)
    for t in ("mandatory/theory", "mandatory/notebook", "optional/theory", "optional/notebook"):
        assert (tmp_path / t / ".gitkeep").exists()
