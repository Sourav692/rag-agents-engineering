# Phase 0: shared foundations

Builds what every later phase uses: a safe restructure script, the Larkspur corpus and golden set, the `lab_kit` helper and the lab tests. No part folder is restructured here. Read [README.md](README.md) first; its Global Constraints apply to every task.

Branch: `restructure/phase-0`.

### Task 0.1: Drive the restructure script from curriculum.v2.yaml

**Files:**
- Modify: `scripts/restructure_part.py`
- Test: `tests/test_restructure.py`

**Interfaces:**
- Consumes: `curriculum.v2.yaml` fields `parts[].folder`, `modules[].{num, part, folder, previous_num, lessons}`, `lessons[].previous` (`"24.5"`), `items[].{folder, file, tier, previous_path}` and `lab_items`; v1 paths from `curriculum_lib` (`load()`, `module_dir()`, `theory_dir()`, `lesson_folder()`); the existing `repoint()`.
- Produces:
  - `load_v2(path: Path = ROOT / "curriculum.v2.yaml") -> dict`
  - `plan(part: str, v2: dict) -> dict[Path, Path]`, mapping every source file to its destination:
    - each item's `previous_path` (a file, or every file under it when it is a folder) to `<part>/<module>/<mandatory|optional>/notebook/<subfolder>/<file>`, where the tier is `mandatory` for tier `mandatory` and `optional` otherwise, and `<subfolder>` is the item's `folder` without its first component (`notebooks/05_training` keeps `05_training`);
    - every other file in the v1 module's `notebooks/`, `optional/` and `exercises/` folders (helper files) to the same tier folder of the module whose `previous_num` owns that v1 module;
    - every other file under the v1 module folder (`README.md`, `assets/`, `lab/`, `projects/`) to the v2 module root;
    - each lesson page folder `theory_dir(v1 module)/lesson_folder(b, title)/**` for lesson `previous: "a.b"` to `<part>/<module>/<tier>/theory/lesson_folder(j, title)/**`, where `j` is the lesson's v2 index and the tier is `optional` only when the lesson has items and none is mandatory;
    - the v1 module theory files that are not lesson folders (`README.md`, `index.html`, `diagrams/`) to `<part>/<module>/mandatory/theory/`;
    - `course/<v1 part>/README.md` of the v1 part holding the first module to `<part>/README.md`.
  - `renumber_prose(text: str, modules: dict[int, int], lessons: dict[str, str]) -> str`: rewrites `M<NN>` codes by `modules` (v1 to v2 number) and lesson numbers by `lessons` (`"24.5"` to `"26.1"`) only in these contexts: after `Lesson ` or `lesson ` or `lessons `, as a whole Markdown table cell (`| 24.5 |`), and at the start of a link text (`[24.5 `). Anything else is left alone.
  - `copy_all(moves: dict[Path, Path], v2: dict, protect: Callable[[Path], bool]) -> tuple[int, int]` returning `(copied, skipped)`: text files (`.md`, `.ipynb`, `.html`, `.py`) go through `repoint()` and then `renumber_prose()`; a destination for which `protect(dst)` is true and that already exists is skipped.
  - `is_lab_file(dst: Path) -> bool`: true when `"lab"` is one of `dst`'s parts below the part folder.
  - `ensure_tiers(module_dir: Path) -> None`: creates the four tier folders, each with `.gitkeep` when empty.
  - `report(part: str, v2: dict) -> list[str]`: every bare `../` target in the copied `.ipynb` and `.py` files that does not exist, and every v1 file name of a renamed item still present in a copied file.
  - CLI: `uv run python scripts/restructure_part.py <v2 part folder>` prints `N files copied, M skipped into <part>/`, then the report.

- [ ] **Step 1: Write the failing tests**

```python
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
    assert rp.renumber_prose("[24.5 Applied ReAct](https://example.com)", mods, lessons) == "[26.1 Applied ReAct](https://example.com)"
    for keep in ("gpt-4.1 and Llama 3.2", "1.5 million rows", "v24.5 of the SDK"):
        assert rp.renumber_prose(keep, mods, lessons) == keep

def test_copy_all_skips_protected_existing(tmp_path):
    a, b = tmp_path / "a.md", tmp_path / "lab" / "README.md"
    a.write_text("new"); b.parent.mkdir(); b.write_text("hand-written")
    assert rp.copy_all({a: b}, V2, protect=lambda d: True) == (0, 1)
    assert b.read_text() == "hand-written"

def test_ensure_tiers(tmp_path):
    rp.ensure_tiers(tmp_path)
    for t in ("mandatory/theory", "mandatory/notebook", "optional/theory", "optional/notebook"):
        assert (tmp_path / t / ".gitkeep").exists()
```

- [ ] **Step 2: Run them to verify they fail**

Run: `uv run pytest tests/test_restructure.py -v`
Expected: FAIL with `AttributeError: module 'restructure_part' has no attribute 'load_v2'`.

- [ ] **Step 3: Implement the interfaces above in `scripts/restructure_part.py`**, keeping `repoint()`. `plan()` builds `modules` and `lessons` maps for `renumber_prose()` from `previous_num` and `previous`. `main()` runs `plan`, `copy_all(..., protect=is_lab_file)`, `ensure_tiers` on every module of the part, then prints `report`.

- [ ] **Step 4: Run the tests and a real copy**

Run: `uv run pytest tests/test_restructure.py -v`
Expected: 6 PASS.
Run: `rm -rf p01_ai_engineering_foundations && uv run python scripts/restructure_part.py p07_advanced_agents`
(the `rm` removes the untracked v1 trial copy, which is laid out on v1 parts). Expected: a copy count, `0 skipped`, and a report; `ls p07_advanced_agents` prints the three module folders `m25_*`, `m26_*`, `m27_*`; `uv run python scripts/check_links.py` prints 0 broken links. Run the script again: expect `3 skipped` (the three lab READMEs). Then `rm -rf p07_advanced_agents`; Phase 3 makes the real copy.

- [ ] **Step 5: Commit**

```bash
git add scripts/restructure_part.py tests/test_restructure.py plan/make_curriculum_v2.py curriculum.v2.yaml CURRICULUM.v2.md CURRICULUM.production-ai.md
git commit -m "scripts: restructure parts from curriculum.v2.yaml, renumbering prose"
```

### Task 0.2: Larkspur corpus and golden set

**Files:**
- Create: `data/larkspur/handbook/<NN>_<slug>.md` (12 to 15 files), `data/larkspur/golden.jsonl`, `data/larkspur/README.md`
- Test: `tests/test_lab_kit.py` (golden-set checks)

**Interfaces:**
- Produces:
  - Handbook: one Markdown file per section of the fictional Larkspur Cloud handbook (billing, refunds, plans, outages and status, backups, data export, account deletion, security, API limits, support tiers, regions, SLA credits, onboarding). Each file starts with `# <Section title>`. The 12 chunks hard-coded in v1's `theory/p04_rag_foundations/m11_rag_lifecycle/02_indexing_from_scratch_with_tf_idf_and_nearest_neighbours/interactive/top-k-retrieval-lab.html` appear verbatim, so theory pages and labs agree.
  - `golden.jsonl`: exactly 30 rows, fields `id` (`g01` … `g30`), `question`, `type`, `evidence_spans` (list of exact substrings of the handbook; empty for `out_of_corpus`), `reference_answer`. Types: 15 `lookup`, 6 `multi_hop` (spans from two or more files), 4 `numeric`, 5 `out_of_corpus`. The three lab questions ("How long does a refund take?", "What happens if my server goes down?", "Can I export my data after I cancel my plan?") are `g01` to `g03`.
  - Evidence is a text span, not a chunk id, so any chunker can be scored: a retrieved chunk is a hit when it contains a span after whitespace normalisation.

- [ ] **Step 1: Write the failing tests**

```python
GOLD = load_jsonl(ROOT / "data/larkspur/golden.jsonl")

def test_golden_shape():
    assert len(GOLD) == 30
    assert [g["id"] for g in GOLD] == [f"g{i:02d}" for i in range(1, 31)]
    assert Counter(g["type"] for g in GOLD) == {"lookup": 15, "multi_hop": 6, "numeric": 4, "out_of_corpus": 5}

def test_golden_spans_are_in_the_handbook():
    text = normalise(" ".join(p.read_text() for p in sorted((ROOT / "data/larkspur/handbook").glob("*.md"))))
    for g in GOLD:
        assert (g["type"] == "out_of_corpus") == (not g["evidence_spans"]), g["id"]
        for s in g["evidence_spans"]:
            assert normalise(s) in text, (g["id"], s)
```

- [ ] **Step 2: Run to verify they fail**: `uv run pytest tests/test_lab_kit.py -v`; Expected: FAIL (`FileNotFoundError` / `ImportError`).
- [ ] **Step 3: Write the handbook and the golden set.** Write each `reference_answer` from the handbook text only. Write `data/larkspur/README.md`: fictional content written for this course, the file list, the golden-set fields and type counts, and "copy, never edit, inside a lab".
- [ ] **Step 4: Run to verify they pass** (after Task 0.3 provides `load_jsonl` and `normalise`); Expected: PASS.
- [ ] **Step 5: Commit**: `git add data/larkspur tests/test_lab_kit.py && git commit -m "data: Larkspur handbook corpus and 30-question golden set"`

### Task 0.3: `lab_kit` helper

**Files:**
- Create: `src/lab_kit.py`
- Test: `tests/test_lab_kit.py`

**Interfaces:**
- Produces (pure Python plus scikit-learn, offline):
  - `load_jsonl(path: str | Path) -> list[dict]`
  - `load_handbook(path: str | Path) -> list[dict]`: one `{"source": <file name>, "title": <H1>, "text": <body>}` per file, sorted by name.
  - `normalise(text: str) -> str`: lower case, whitespace collapsed to single spaces.
  - `is_hit(chunk: str, spans: list[str]) -> bool`
  - `hit_rate(results: dict[str, list[str]], golden: list[dict]) -> float`, `recall_at_k(...) -> float`, `mrr(...) -> float`: `results` maps question id to retrieved chunk texts in rank order; questions with no spans are skipped. Recall is the share of a question's spans found in any retrieved chunk, averaged.
  - `tfidf_retriever(chunks: list[str], k: int = 4) -> Callable[[str], list[str]]`
  - `baseline(corpus_dir: str | Path, k: int = 4, chunk_size: int = 500, chunk_overlap: int = 50) -> dict`: recursive split (`langchain_text_splitters.RecursiveCharacterTextSplitter`), TF-IDF top-k over `<corpus_dir>/handbook`, scored on `<corpus_dir>/golden.jsonl`; returns `{"k", "n", "hit_rate", "recall_at_k", "mrr"}`.

- [ ] **Step 1: Write the failing tests**

```python
GOLDEN = [{"id": "q1", "evidence_spans": ["refunds take 5 days"]},
          {"id": "q2", "evidence_spans": ["status page"]},
          {"id": "q3", "evidence_spans": []}]
RESULTS = {"q1": ["Intro.", "Refunds take 5 days to clear."], "q2": ["Pricing."], "q3": ["x"]}

def test_metrics():
    assert hit_rate(RESULTS, GOLDEN) == 0.5
    assert recall_at_k(RESULTS, GOLDEN) == 0.5
    assert mrr(RESULTS, GOLDEN) == 0.25

def test_baseline_runs_offline():
    b = baseline(ROOT / "data/larkspur")
    assert b["n"] == 25 and b["k"] == 4
    assert 0.0 <= b["hit_rate"] <= 1.0
```

- [ ] **Step 2: Run to verify they fail**: `uv run pytest tests/test_lab_kit.py -v`; Expected: FAIL with `ModuleNotFoundError: lab_kit` (tests add `src` to `sys.path`).
- [ ] **Step 3: Implement the functions in `src/lab_kit.py`.**
- [ ] **Step 4: Run to verify they pass**: Expected: all of `tests/test_lab_kit.py` PASS. Record the printed `baseline()` numbers in `data/larkspur/README.md` as "TF-IDF reference, k=4".
- [ ] **Step 5: Commit**: `git add src/lab_kit.py tests/test_lab_kit.py data/larkspur/README.md && git commit -m "src: lab_kit metrics and offline TF-IDF baseline"`

### Task 0.4: Lab tests

**Files:**
- Create: `tests/test_labs.py`

**Interfaces:**
- Produces: `DONE_PARTS: set[str] = set()` at the top of `tests/test_labs.py`. Each phase's last task adds its part folder names. Tests run over every part folder at the repo root that exists (`p[0-9][0-9]_*`).

- [ ] **Step 1: Write the tests**

```python
def test_every_module_has_tiers_and_a_lab_readme(): ...
    # for each module dir: the four tier dirs exist; lab/README.md exists
def test_done_parts_have_one_solution_per_module(): ...
    # for part in DONE_PARTS: every module has exactly one lab/solution/m<NN>_solution.ipynb, NN = module number
def test_solutions_are_clean(): ...
    # nbformat.read(..., as_version=4) succeeds; every code cell has outputs == [] and execution_count is None;
    # no match for r"sk-[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,}" in the file
def test_solutions_read_only_their_own_data(): ...
    # every relative path in the notebook source (r"(?:\.\./)+[\w./-]+"), resolved from lab/solution/,
    # lands inside that module's lab/ folder or inside src/; ../data/larkspur/x passes, ../../assets/x fails
def test_lab_data_has_readme_and_fits(): ...
    # each lab/data/ has README.md; total size <= 5 * 1024 * 1024 bytes
def test_larkspur_copies_match_canonical(): ...
    # every lab/data/larkspur/ tree is byte-identical to data/larkspur/ (same file list, same bytes)
```

- [ ] **Step 2: Run**: `uv run pytest tests/test_labs.py -v`; Expected: PASS with `DONE_PARTS` empty and no part folder present.
- [ ] **Step 3: Prove each check bites.** Temporarily add `p01_ai_engineering_foundations` to `DONE_PARTS`; Expected: `test_done_parts_have_one_solution_per_module` FAILS (the part folder is missing, so M01 to M03 have no solution). Revert.
- [ ] **Step 4: Commit**: `git add tests/test_labs.py && git commit -m "tests: lab layout, clean solutions and lab data rules"`

### Task 0.5: Document the layout and open the PR

**Files:**
- Modify: `CLAUDE.md` (a short "Part folders (migration in progress)" section after "Theory pages": that `curriculum.v2.yaml` (generated by `plan/make_curriculum_v2.py`) defines the new course and `curriculum.yaml` stays the build source until Phase 6, the target layout from README.md, that `course/` and `theory/` stay untouched, that `lab/` is hand-maintained in the new layout, and the lab data rules)

- [ ] **Step 1: Write the section; run** `uv run pytest -q && uv run python scripts/check_links.py`; Expected: all pass, 0 broken links.
- [ ] **Step 2: Commit and open the PR**: `git commit -am "docs: describe the part-folder layout" && git push -u origin restructure/phase-0 && gh pr create --fill`; Expected: CI green.
