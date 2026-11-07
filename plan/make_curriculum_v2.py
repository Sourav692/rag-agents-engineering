"""Build curriculum.v2.yaml (AI Engineering framing) from curriculum.yaml, and its review page CURRICULUM.v2.md.

    uv run python plan/make_curriculum_v2.py

Every lesson item of v1 is placed exactly once in v2; the script asserts it. Each v2 module records
`previous_num`, each lesson `previous` ("24.5"), and each item `previous_path` (its v1 path under course/),
so scripts/restructure_part.py can copy the old files into the v2 layout.
Production topics (evaluation, observability, guardrails, security) are not in v2: they belong to the
Production AI Engineering track, outlined in CURRICULUM.production-ai.md.
"""
import copy
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import curriculum_lib as cl  # noqa: E402

v1 = cl.load()  # also fills curriculum_lib's part-folder table for module_dir()
mods = {m["num"]: copy.deepcopy(m) for m in v1["modules"]}

# Record v1 provenance before anything moves.
for m in v1["modules"]:
    for i, l in enumerate(mods[m["num"]]["lessons"], 1):
        l["previous"] = f"{m['num']}.{i}"
        for it in l["items"]:
            it["previous_path"] = f"{cl.module_dir(m)}/{it['folder']}/{it['file']}"
    for it in mods[m["num"]].get("lab_items") or []:
        it["previous_path"] = f"{cl.module_dir(m)}/{it['folder']}/{it['file']}"

V1_KEYS = Counter(f"{it['source']}|{it['previous_path']}" for m in mods.values() for l in m["lessons"] for it in l["items"])

# (id, title, level, folder, summary, [old module numbers or new keys])
PARTS = [
    ("aifound", "AI Engineering Foundations", "foundation", "p01_ai_engineering_foundations",
     "Python and data tools, LLM provider APIs and model choice, and open models from the Hugging Face Hub.", [1, 2, 3]),
    ("prompting", "Prompt & Context Engineering", "foundation", "p02_prompt_engineering",
     "Prompt patterns, reasoning prompts and multimodal prompting across providers.", [5, 6]),
    ("frameworks", "LLM Application Frameworks: LangChain & LangGraph", "foundation", "p03_llm_application_frameworks",
     "LangChain models, prompts, parsers and LCEL; LangGraph state, routing, persistence, interrupts and streaming.", [7, 8, 9, 10]),
    ("found", "RAG Foundations: Ingestion & Indexing", "core", "p04_rag_foundations",
     "Why retrieval exists, a measured baseline, and the ingestion pipeline: loaders, metadata, chunking, embeddings, vector stores and index design.", [11, 12, 13, 14, 15, 16]),
    ("retrieval", "Retrieval Quality & RAG Applications", "core", "p05_retrieval_quality_and_rag_apps",
     "Hybrid search, query transformation and reranking, then complete RAG applications with citations, structured data, images and LlamaIndex.", [17, 18, 19, 20, 21, 22]),
    ("agents", "Agent Foundations", "core", "p06_agent_foundations",
     "The agent loop and tool calling by hand, ReAct with create_agent and middleware, and the five agentic workflow patterns.", [23, 24, 25]),
    ("advagents", "Advanced Agents", "advanced", "p07_advanced_agents",
     "Planning, reflection and search over reasoning paths; coding, computer-use and deep agents; human approval and applied single-agent builds.", [26, "deepagents", 27]),
    ("agentic_rag", "Agentic RAG", "advanced", "p08_agentic_rag",
     "Retrieval inside a control loop: grading and rewriting, CRAG and Self-RAG, adaptive routing, RAG as a tool, and feedback loops.", [28, 29, 30, 31, 32]),
    ("memory", "The Memory Layer", "advanced", "p09_memory_layer",
     "Short-term conversation state and context trimming, then long-term semantic, episodic and procedural memory for agents.", [33, 34]),
    ("multiagent", "Multi-Agent Systems", "expert", "p10_multi_agent_systems",
     "When several agents beat one, the five architectures, supervisors, swarms, blackboards and parallel agents, and applied multi-agent builds.", [35, 36, 37]),
    ("protocols", "Agent Protocols: MCP & A2A", "advanced", "p11_agent_protocols",
     "Expose tools, data and whole agents as services with the Model Context Protocol and Agent-to-Agent.", [38, 39, 40, 41]),
    ("graph", "Knowledge Graphs & GraphRAG", "expert", "p12_knowledge_graphs_and_graph_rag",
     "Hierarchical and memory-augmented retrieval, knowledge graphs in Neo4j, and GraphRAG for global and multi-hop questions.", [42, 43, 44]),
    ("capstone", "Design Decisions: Model Adaptation & Architecture", "expert", "p13_design_decisions",
     "Two decisions that close the course: whether to fine-tune or retrieve, then which architecture to build for the capstone and why each component beats a simpler one.", [4, 45]),
]
ROMAN = "I II III IV V VI VII VIII IX X XI XII XIII".split()

MOVES = {(24, 5): "deepagents", (37, 4): "deepagents", (37, 6): "deepagents"}  # (old module, lesson) -> new module
CONCEPT_MOVES = {"Deep-agent harness": (37, "deepagents")}
NEW = {
    "deepagents": dict(
        key="deepagents", folder="coding_computer_use_and_deep_agents",
        title="Coding, Computer-Use & Deep Agents", level="expert", hours=5, stages=["agent"],
        sources=["06:05_react_agents", "08:12_deep_agents"],
        why="Agents that write code, drive a browser or run for hours need a harness: sub-agents, a file system, skills and a tester that checks the work.",
        objectives=["Run ReAct agents in web, code and computer-use environments and see where the loop changes",
                    "Pair a developer agent with a tester agent and iterate until the tests pass",
                    "Build a deep agent with an orchestrator, sub-agents, skills and long-term memory"],
        concepts=[],
        lab="Coding agent: give a deep agent a developer sub-agent and a tester sub-agent, ask it for a small Python function with tests, and log each iteration until the tests pass.",
        lessons=[]),
}
RETITLE = {
    4: "Fine-Tuning & Model Adaptation",
    33: "Short-Term Memory & Conversation State",
    37: "Multi-Agent Applied Builds",
    45: "Architecture Synthesis: Choosing a System Design",
}
FOLDER = {  # module folder slugs that would no longer match the title
    4: "fine_tuning_model_adaptation",
    33: "short_term_memory_conversation_state",
    37: "multi_agent_applied_builds",
}
PRODUCTION_GAPS = {"RAG evaluation", "Production RAG", "Security & governance"}

# Move lessons (highest index first so earlier indexes stay valid).
for (n, i), key in sorted(MOVES.items(), key=lambda kv: (kv[0][0], -kv[0][1])):
    NEW[key]["lessons"].insert(0, mods[n]["lessons"].pop(i - 1))
NEW["deepagents"]["lessons"].sort(key=lambda l: [int(x) for x in l["previous"].split(".")])
for c, (n, key) in CONCEPT_MOVES.items():
    mods[n]["concepts"].remove(c)
    NEW[key]["concepts"].append(c)
mods[24]["hours"] -= 1
mods[37]["hours"] -= 2

order = [(p[0], ref) for p in PARTS for ref in p[5]]
new_num = {ref: i for i, (_, ref) in enumerate(order, 1)}


def renumber_text(s: str) -> str:
    s = re.sub(r"\bM(\d{2})\b", lambda m: f"M{new_num.get(int(m.group(1)), int(m.group(1))):02d}", s)
    return re.sub(r"\bPart VII?\b", "Part V", s)  # old Parts VI and VII merge into Part V


out_modules = []
for part_id, ref in order:
    old = ref if isinstance(ref, int) else None
    m = mods[ref] if old else copy.deepcopy(NEW[ref])
    m["num"], m["part"] = new_num[ref], part_id
    if old in RETITLE:
        m["title"] = RETITLE[old]
    slug = FOLDER.get(old) or (m["folder"].split("_", 1)[1] if old else m.pop("folder"))
    m["folder"] = f"m{m['num']:02d}_{slug}"
    if old:
        m["previous_num"] = old
        for f in ("why", "lab"):
            if isinstance(m.get(f), str):
                m[f] = renumber_text(m[f])
        m["objectives"] = [renumber_text(o) for o in m.get("objectives", [])]
    # File names start with the lesson number: renumber the prefix where the lesson moved.
    for j, l in enumerate(m["lessons"], 1):
        old_i = int(l["previous"].split(".")[1])
        for it in l["items"]:
            if old_i != j and re.match(rf"{old_i:02d}[a-z]", it["file"]):
                it["file"] = f"{j:02d}{it['file'][2:]}"
    out_modules.append(m)

out_parts, hours_seen = [], 0
for i, (pid, title, level, folder, summary, refs) in enumerate(PARTS):
    h = sum(next(m["hours"] for m in out_modules if m["num"] == new_num[r]) for r in refs)
    w0 = hours_seen // 8 + 1
    hours_seen += h
    w1 = max(w0, (hours_seen - 1) // 8 + 1)
    old = next((p for p in v1["parts"] if p["id"] == pid), None)
    out_parts.append(dict(id=pid, num=ROMAN[i], title=title, weeks=f"Week {w0}" if w0 == w1 else f"Weeks {w0}–{w1}",
                          level=level, summary=summary, folder=folder,
                          **({"previous_title": old["title"]} if old and old["title"] != title else {})))

v2 = copy.deepcopy(v1)
v2["course"]["title"] = "AI Engineering: LLM Apps, RAG & Agents"
v2["course"]["subtitle"] = ("From Python and your first LLM call to retrieval, advanced agents, a memory layer, "
                            "multi-agent systems and agent protocols")
v2["parts"], v2["modules"] = out_parts, out_modules
for g in v2.get("gaps", []):
    g["detail"] = renumber_text(g["detail"])
    if g["title"] in PRODUCTION_GAPS:
        g["status"] = "Production AI track"
        g["detail"] = "Out of this course by design: taught in the Production AI Engineering track (CURRICULUM.production-ai.md). " + g["detail"]

key = lambda it: f"{it['source']}|{it['previous_path']}"
items = lambda ms: Counter(key(it) for m in ms for l in m["lessons"] for it in l["items"])
assert V1_KEYS == items(v2["modules"]), "item set changed"
assert sum(items(v2["modules"]).values()) == sum(len(l["items"]) for m in v1["modules"] for l in m["lessons"])
assert sum(len(m["concepts"]) for m in v1["modules"]) == sum(len(m["concepts"]) for m in v2["modules"])
assert len(v2["parts"]) == 13 and [m["num"] for m in v2["modules"]] == list(range(1, len(v2["modules"]) + 1))
dests = [f"{m['folder']}/{it['folder']}/{it['file']}" for m in v2["modules"] for l in m["lessons"] for it in l["items"]]
assert len(dests) == len(set(dests)), "two items land on one path"

header = ("# DRAFT v2 of curriculum.yaml (AI Engineering framing). Not used by any build yet.\n"
          "# Generated by plan/make_curriculum_v2.py; curriculum.yaml stays the source of truth until v2 is approved.\n"
          "# previous_num, previous (lesson) and previous_path (item) record where each piece lives in v1.\n")
(ROOT / "curriculum.v2.yaml").write_text(header + yaml.safe_dump(v2, sort_keys=False, allow_unicode=True, width=120))

# ---------- review page ----------
renamed_files = [(it["previous_path"].rsplit("/", 1)[1], it["file"], f"M{m['num']:02d}")
                 for m in v2["modules"] for l in m["lessons"] for it in l["items"]
                 if it["previous_path"].rsplit("/", 1)[1] != it["file"]]
n_items = sum(items(v2["modules"]).values())
L = [f"# Proposed curriculum v2: {v2['course']['title']}", "",
     "Draft for review, 7 November 2026, generated by `plan/make_curriculum_v2.py` into `curriculum.v2.yaml`. "
     "Nothing in `course/`, `theory/` or `curriculum.yaml` has been renamed, moved or deleted.", "",
     f"{len(v2['parts'])} parts, {len(v2['modules'])} modules, {n_items} lesson items: every v1 item placed exactly once.", "",
     "## What changes", "",
     f"- **Framing.** An AI Engineering course in which RAG is one capability among several. Title: \"{v2['course']['title']}\" (was \"{v1['course']['title']}\").",
     "- **RAG in four parts instead of six.** Old Parts IV and V merge into Part IV; old Parts VI and VII merge into Part V. No module or notebook is dropped.",
     "- **New Part VII Advanced Agents.** Old M26 and M27, with a new M26 Coding, Computer-Use & Deep Agents built from lessons 24.5, 37.4 and 37.6.",
     "- **Old Part X splits in two:** Part IX The Memory Layer and Part X Multi-Agent Systems.",
     "- **Part XIII Design Decisions.** Fine-tuning (old M04) ends in a RAG or fine-tune verdict; the architecture capstone (old M45) uses it. Part XIII should be required on the site.",
     "- **Production topics leave the course.** Evaluation, observability, guardrails and security belong to the Production AI Engineering track, outlined in [CURRICULUM.production-ai.md](CURRICULUM.production-ai.md). The course keeps the measurement its labs need (the M10 golden set and baseline, tool-call evaluation in M22, guardrails in M28).",
     "- **Numbers.** M01 to M03 and M27 to M44 keep their numbers; old M05 to M26 drop by one; old M04 becomes M45 and old M45 becomes M46.", "",
     "## Parts", "", "| Part | Title | Was | Modules | Weeks | Level |", "|---|---|---|---|---|---|"]
for p in v2["parts"]:
    ms = [m for m in v2["modules"] if m["part"] == p["id"]]
    was = p.get("previous_title", "same") if any(q["id"] == p["id"] for q in v1["parts"]) else "new"
    L.append(f"| {p['num']} | {p['title']} | {was} | M{ms[0]['num']:02d} to M{ms[-1]['num']:02d} | {p['weeks'].replace('–', ' to ')} | {p['level']} |")
L += ["", "## Modules", ""]
for p in v2["parts"]:
    L += [f"### Part {p['num']}: {p['title']}", "", p["summary"], "",
          "| Module | Was | Lessons | Mandatory / optional notebooks | Hours |", "|---|---|---|---|---|"]
    for m in (m for m in v2["modules"] if m["part"] == p["id"]):
        mand = sum(1 for l in m["lessons"] for it in l["items"] if it["tier"] == "mandatory")
        opt = sum(1 for l in m["lessons"] for it in l["items"] if it["tier"] != "mandatory")
        old_title = next((o["title"] for o in v1["modules"] if o["num"] == m.get("previous_num")), None)
        title = m["title"] + (f" (was \"{old_title}\")" if old_title and old_title != m["title"] else "")
        was = f"M{m['previous_num']:02d}" if m.get("previous_num") else "new"
        L.append(f"| M{m['num']:02d} {title} | {was} | {len(m['lessons'])} | {mand} / {opt} | {m['hours']} |")
    L.append("")
L += ["## Lessons that move or renumber", "", "| v1 lesson | v2 lesson | Title |", "|---|---|---|"]
for m in v2["modules"]:
    for j, l in enumerate(m["lessons"], 1):
        if l["previous"] != f"{m.get('previous_num', 0)}.{j}":
            L.append(f"| {l['previous']} | {m['num']}.{j} | {l['title']} |")
L += ["", "Only the lessons above change position inside or between modules; every other lesson keeps its index in its (renumbered) module. "
      "The concept \"Deep-agent harness\" moves with lesson 37.6.", "",
      "## Notebook files renamed to their new lesson number", "", "| v1 file | v2 file | Module |", "|---|---|---|"]
L += [f"| `{a}` | `{b}` | {c} |" for a, b, c in renamed_files]
L += ["", "## What approval triggers", "",
      "1. The part-folder restructure in `plan/` builds the new layout from `curriculum.v2.yaml`.",
      "2. After the last phase, `curriculum.v2.yaml` replaces `curriculum.yaml` and the old `course/` and `theory/` trees are deleted, as agreed.",
      "3. forwarddeployedprep.com: module and lesson slugs in `docs/fde-site-slugs.yaml` stay frozen; new and merged parts need track slugs and redirects.", ""]
(ROOT / "CURRICULUM.v2.md").write_text("\n".join(L))
print(f"ok: {len(v2['parts'])} parts, {len(v2['modules'])} modules, {n_items} items, {len(renamed_files)} files renamed")
