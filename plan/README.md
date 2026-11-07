# v2 part folders and lab solutions: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the AI Engineering course of `curriculum.v2.yaml` ([curriculum.yaml](../curriculum.yaml) since Phase 6) as 13 part folders at the repo root (`<part>/<module>/{mandatory,optional}/{theory,notebook}`), and give every module lab a `solution/` notebook with the data it needs in `lab/data/`.

**Architecture:** `scripts/restructure_part.py` reads `curriculum.v2.yaml` and copies one v2 part out of the v1 trees (`course/`, `theory/`), using the `previous_num`, `previous` and `previous_path` fields that `plan/make_curriculum_v2.py` writes. It re-points relative paths and rewrites module and lesson numbers to v2. Lab work happens only in the new layout. A shared fictional corpus and golden set (`data/larkspur/`) and a small offline helper (`src/lab_kit.py`) keep the 46 solutions consistent, and each lab carries its own copy of the data it reads. Phase 0 builds the shared pieces; phases 1 to 5 each restructure their parts and write their labs, and depend only on Phase 0.

**Tech Stack:** Python 3.12, uv, pytest, Jupyter (`jupyterlab`, `nbconvert`, `nbstripout` from the `dev` group), LangChain 1.x, LangGraph, scikit-learn; per lab as noted (Docker for pgvector and Neo4j; the `protocols`, `llamaindex` and `hf` uv groups).

**Spec:** the owner's requests of 7 November 2026 (quoted under [Request](#request)) and the approved v2 structure in [CURRICULUM.v2.md](../CURRICULUM.v2.md). Production topics are out of scope: they belong to the Production AI Engineering track, outlined separately in [CURRICULUM.production-ai.md](../CURRICULUM.production-ai.md).

## Request

1. Restructure into 13 part-wise folders like the trial p01 copy, following the v2 curriculum.
2. Fix the lab part: each lab gets a solution folder with a solution notebook, and a data folder inside the lab when it needs data.
3. Phases of 3 parts each, every phase doing both the restructure and the lab work, so each can run independently.

## Global Constraints

- Nothing under `course/`, `theory/` or `curriculum.yaml` is deleted or edited. Deleting them is Phase 6, a separate plan, after the owner approves the new layout.
- Part, module and lesson names, numbers and folders come from `curriculum.v2.yaml`. Regenerate it with `uv run python plan/make_curriculum_v2.py`; never edit it by hand.
- Every module has all four folders: `mandatory/theory`, `mandatory/notebook`, `optional/theory`, `optional/notebook`. An empty one holds `.gitkeep`.
- The solution folder is `lab/solution/` (lower case, as every folder in this repo is; macOS ignores case and CI does not). Its notebook is `lab/solution/m<NN>_solution.ipynb` with the v2 module number, for example `m10_solution.ipynb`.
- Lab data lives in `lab/data/` with a `README.md` naming each file's source and licence, at or under 5 MB per lab.
- A solution reads data only from `../data/`. It may import from `src/` (`sys.path.insert(0, str(Path("../../../../src").resolve()))`); it never reads `data/`, `course/`, `theory/` or another module's folder.
- A solution never depends on another lab's output. When a brief says "your M08 graph" or "your Part V system", the solution rebuilds the minimal version inline, with `lab_kit` where it fits.
- Solutions ship with outputs cleared (`uv run nbstripout <file>`).
- Numbers in a lab README come only from a real run of its solution, with the date and the models used.
- Copy follows the `no-ai-slop` rules used for theory pages: no en or em dashes, no closing aphorisms.
- `uv run pytest -q` and `uv run python scripts/check_links.py` (0 broken links) pass at the end of every task.

## Target layout

```
<part>/                                   v2 part folder, e.g. p07_advanced_agents/
  README.md                               copy of the v1 part README (stale until Phase 6 regenerates it)
  <module>/                               v2 module folder, e.g. m26_coding_computer_use_and_deep_agents/
    README.md                             copy of the v1 module README, numbers rewritten
    assets/  projects/                    from the v1 module, where it has them
    lab/
      README.md                           brief, how to run, data, results (hand-maintained from here on)
      data/                               sample data, only if the lab needs it (with README.md)
      solution/
        m<NN>_solution.ipynb              (plus docker-compose.yml or small .py files the solution needs)
    mandatory/
      theory/                             module page, index.html, module diagrams, mandatory lesson pages
      notebook/                           mandatory items and their helper files
    optional/
      theory/                             pages of lessons whose notebooks are all optional
      notebook/                           optional and exercise items
```

The v2 parts: `p01_ai_engineering_foundations`, `p02_prompt_engineering`, `p03_llm_application_frameworks`, `p04_rag_foundations`, `p05_retrieval_quality_and_rag_apps`, `p06_agent_foundations`, `p07_advanced_agents`, `p08_agentic_rag`, `p09_memory_layer`, `p10_multi_agent_systems`, `p11_agent_protocols`, `p12_knowledge_graphs_and_graph_rag`, `p13_design_decisions`.

## Lab recipe (every module lab task follows it)

- [ ] **1. Read the brief and its sources.** The brief is the module's `lab:` text in `curriculum.v2.yaml` (already in v2 numbers). Open the mandatory notebooks it builds on in the module's `mandatory/notebook/` and note the APIs they use; the solution uses the same ones.
- [ ] **2. Prepare `lab/data/`** if the lab needs data, per the row in its phase file. For the Larkspur corpus, copy it unchanged: `cp -R data/larkspur <part>/<module>/lab/data/larkspur`. Lab-specific files go beside it, never into the canonical copy. Write `lab/data/README.md`.
- [ ] **3. Write `lab/solution/m<NN>_solution.ipynb`.** Cells: title and brief; setup (imports, `load_dotenv()`, the `src` path); one section per part of the brief, each ending in a printed result; a results table; a short "what this shows" section. Use `get_experientiallabs_llm()` and `get_embeddings()` from `src/helpers/utils.py` unless the brief names another model.
- [ ] **4. Run it top to bottom.** `uv run jupyter nbconvert --to notebook --execute <path> --output /tmp/m<NN>_run.ipynb` (with the uv group from the phase file). Expected: exit code 0.
- [ ] **5. Rewrite `lab/README.md`.** Keep the brief. Replace the generic "How to report it" with how to run the solution, the data it reads, and a results table copied from the run in step 4 (date, models). Link `solution/m<NN>_solution.ipynb` and `data/README.md`.
- [ ] **6. Clear outputs and check.** `uv run nbstripout <path>`, then `uv run pytest -q tests/test_labs.py` and `uv run python scripts/check_links.py`. Expected: PASS, 0 broken links.
- [ ] **7. Commit.** `git add <part>/<module>/lab && git commit -m "content: M<NN> lab solution"`.

## Phases

| Phase | File | v2 parts | v2 modules | Depends on |
|---|---|---|---|---|
| 0 | [phase-0-foundations.md](phase-0-foundations.md) | none | none | nothing |
| 1 | [phase-1-parts-01-03.md](phase-1-parts-01-03.md) | I, II, III | M01 to M09 (9) | Phase 0 |
| 2 | [phase-2-parts-04-06.md](phase-2-parts-04-06.md) | IV, V, VI | M10 to M24 (15) | Phase 0 |
| 3 | [phase-3-parts-07-09.md](phase-3-parts-07-09.md) | VII, VIII, IX | M25 to M34 (10) | Phase 0 |
| 4 | [phase-4-parts-10-12.md](phase-4-parts-10-12.md) | X, XI, XII | M35 to M44 (10) | Phase 0 |
| 5 | [phase-5-part-13.md](phase-5-part-13.md) | XIII | M45, M46 (2), plus the closing check | Phase 0 |

13 parts do not split evenly into threes, so Phase 5 holds the last part and the cross-part closing check. Phase 2 is the largest (15 modules) because v2 Parts IV and V are the six-module RAG parts; split it into 2a (Part IV) and 2b (Parts V and VI) if one branch is too big to review.

Each phase runs on its own branch (`restructure/phase-<N>`) and lands as one PR. Phases can run in parallel: they write disjoint part folders, and the only shared line they edit is `DONE_PARTS` in `tests/test_labs.py`.

## Status (8 Nov 2026)

Phases 0 to 5 are merged into `main`: Phase 0 in #24, Phase 1 in #26, Phase 2 in #27, Phase 3 in #28, Phase 4 in #29 and Phase 5 in #25. Closing check:

- 13 part folders, all 13 in `DONE_PARTS`.
- 46 lab solutions (`lab/solution/m<NN>_solution.ipynb`), all with outputs cleared and none run yet: every lab README reports its results as *pending run*.
- All 414 lesson items of `curriculum.v2.yaml` are present, plus M19's one lab item.
- No change in `course/`, `theory/` or `curriculum.yaml` since the Phase 0 merge (`d42fdee`).
- `uv run pytest -q` passes and `scripts/check_links.py` reports 0 broken links.
- The M35 lab's `kb/` and `tickets.jsonl` are now byte-identical copies of the M30 lab's, so the two routing results compare. The M35 solution reads the M30 field name (`text`).

Run-time paths left as they are, since the folders or files only exist after a notebook runs:

- M15 `03a_hierarchical_indices.ipynb` and `hierarchical_indices.py` write `../vector_stores/`.
- M31 `02a` downloads `attention-is-all-you-need.pdf`. M32 `02a` downloads `feedback_data.json` with `wget`, and its `.py` appends to it.
- M44 `03a_microsoft_graphrag.ipynb` creates `elon.md` and `graphrag/` under `data/sample/rag_techniques/`.
- M26 `03a_simple_coding_agent.py` loads skills from `skills/` beside itself, but they sit in `optional/notebook/03c_skills/`. v1 has the same split. The fix changes the backend root and needs a run to check.

Phase 6, the switch ([phase-6-switch.md](phase-6-switch.md), branch `restructure/phase-6`): `curriculum.yaml` is the v2 curriculum, every build script and test reads the part folders, the part and module READMEs and every `index.html` are regenerated, module pages carry v2 part names and titles, v1 lesson numbers in parentheses are rewritten to v2, and `course/` and `theory/` are deleted. Paths in the phase files above name the v1 trees as they were then.

Next step: owner review of the Phase 6 PR, then running the 46 lab solutions to fill in their results.

## Review Focus

- A notebook path to a folder created at run time (`../vector_stores/`, `../projects/<name>/`) does not exist when a part is copied, so `repoint()` leaves it unchanged and the notebook writes to the wrong folder. Each restructure task reviews the script's unresolved-refs list (Task 0.1 adds `unresolved_refs()`).
- Lesson renumbering must not touch version numbers: `gpt-4.1`, `Llama 3.2` or `1.5 million` are not lessons. Task 0.1 rewrites lesson numbers only in marked contexts and tests that those strings stay unchanged.
- A renamed item (`06c_skills` becomes `03c_skills`) can still be named by a bare relative path, without `../`, inside a sibling file, which `repoint()` does not see. Task 0.1's report lists every old item name still present in a copied file.
- Re-running the restructure after a lab was written would overwrite the hand-maintained `lab/README.md`. Task 0.1 skips existing files under `lab/` and tests it.
- A solution that reads `data/`, `assets/` or another module's files, carries outputs, or holds a token breaks the lab rules quietly. Task 0.4 tests all three, plus byte-identical Larkspur copies.

## Not in this plan

- **Phase 6, the switch** (its own plan, written when phases 1 to 5 have merged): `curriculum.v2.yaml` replaces `curriculum.yaml`; `curriculum_lib.py`, `build_curriculum.py`, `build_theory_html.py`, `export_site_curriculum.py` and the tests move to the part-folder layout; the generated READMEs and `index.html` pages regenerate from v2; and `course/` and `theory/` are deleted. Until then the website and the syllabus site keep reading the old trees.
- Building the Production AI Engineering track ([CURRICULUM.production-ai.md](../CURRICULUM.production-ai.md)) from `Agent_Evaluation_Demystified` and repo 13.
- Rotating the live database credentials in M01's `04b_mysql_connection.ipynb` and `04c_postgresdb_connection.ipynb`; the restructure copies them as they are.
