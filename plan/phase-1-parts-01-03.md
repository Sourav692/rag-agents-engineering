# Phase 1: v2 Parts I to III (M01 to M09)

Parts: `p01_ai_engineering_foundations`, `p02_prompt_engineering`, `p03_llm_application_frameworks`. Depends only on [Phase 0](phase-0-foundations.md). Branch: `restructure/phase-1`.

### Task 1.1: Restructure the three parts

**Files:** Create the three part folders above.

- [ ] **Step 1: Copy.** Run `uv run python scripts/restructure_part.py <part>` for each part. Expected: `N files copied, 0 skipped` for each.
- [ ] **Step 2: Review the report.** For each unresolved `../` target, decide whether it is a run-time output folder (leave it, note it in the PR) or a missed input (fix the copy by hand). For each old item name still present, fix the reference in the copy.
- [ ] **Step 3: Check.** `uv run pytest -q && uv run python scripts/check_links.py`; Expected: PASS, 0 broken links. `git diff --stat course theory curriculum.yaml` prints nothing.
- [ ] **Step 4: Commit.** `git add p01_* p02_* p03_* && git commit -m "content: copy v2 Parts I to III into the part-folder layout"`

M01's `optional/notebook/04b_mysql_connection.ipynb` and `04c_postgresdb_connection.ipynb` hold live database credentials, and the copy duplicates them. Do not fix that here (see README, Not in this plan), but name it in the PR description.

### Tasks 1.2 to 1.10: one lab per module

Each row is one task. Follow the [lab recipe](README.md#lab-recipe-every-module-lab-task-follows-it). Paths are under `<part>/<module>/lab/`.

| Task | Module | `data/` contents | Run with | The solution must show |
|---|---|---|---|---|
| 1.2 | M01 Python & Data Toolkit Refresher | `churn_prediction.csv` copied from the module's `assets/` (sampled to 5 MB if larger) | default | the CSV in pandas and in SQLite (`sqlite3`, in memory); five questions answered both ways with equal results asserted; one answer served by a Flask route, called with `app.test_client()` (no server left running) |
| 1.3 | M02 LLM Provider APIs & Model Selection | `larkspur/` | default; `HF_TOKEN` | 20 golden questions (`lookup` and `numeric`), each given its evidence spans as context; a fast model, a reasoning model at two effort levels and an open model via the Hugging Face Inference API; accuracy against `reference_answer`, latency and cost per answer in one table (prices from the provider's page, dated) |
| 1.4 | M03 Hugging Face Models & Gradio Demos | `larkspur/` | `hf` group | an open embedding model from the Hub (`sentence-transformers/all-MiniLM-L6-v2`) behind a Gradio app that returns the top 3 handbook passages for a typed query; the search function called directly for three golden questions; `demo.launch(prevent_thread_lock=True)` then `demo.close()` |
| 1.5 | M04 Prompt Engineering Patterns | `larkspur/`, `grading_pairs.jsonl` (30 rows: `question`, `passage`, `label`; relevant passages hold an evidence span, the others are top TF-IDF passages without one; labels written by the author by reading) | default | three grading prompts; each prompt's agreement with the labels (accuracy and Cohen's kappa from `sklearn.metrics`) |
| 1.6 | M05 Multimodal Prompting | one chart-heavy page rendered to PNG from a public-domain PDF in `data/sample` (for example a CRS report such as `IF10244.pdf`; confirm it has charts and is public domain, else draw a Larkspur chart page with matplotlib), and `questions.jsonl` (five questions, answers read off the page by hand) | default | the page image sent to a multimodal model with each question; answers checked against the hand-read answers |
| 1.7 | M06 LangChain Core: Models, Prompts & Parsers | `larkspur/` | default | a prompt template and a Pydantic parser that turn a question plus three passages into `{"answer": str, "citations": [str]}`; run on 10 golden questions; count of parse failures and of citations that point at a passage without an evidence span |
| 1.8 | M07 LCEL, Runnables & Chains | `larkspur/` | default | one legacy chain from the module's notebooks (from `langchain_classic`) rebuilt in LCEL; a `RunnableBranch` that routes inputs under and over a length threshold differently; both versions' outputs side by side on 10 golden questions |
| 1.9 | M08 LangGraph Core: Graphs, State & Control Flow | `larkspur/` | default | a `StateGraph` that classifies a question (billing, technical, general), routes to one of two answer nodes and returns a structured answer; the graph drawn with `get_graph().draw_mermaid()`; routing shown for 10 golden questions |
| 1.10 | M09 LangGraph Runtime: Persistence, HITL & Streaming | `larkspur/` | default | the M08 graph rebuilt inline, compiled with `MemorySaver` and `interrupt_before` the answer node; a run that stops, is approved, and resumes from the checkpoint; `stream_mode="updates"` output printed |

### Task 1.11: Close the phase

- [ ] **Step 1:** Add `"p01_ai_engineering_foundations", "p02_prompt_engineering", "p03_llm_application_frameworks"` to `DONE_PARTS` in `tests/test_labs.py`.
- [ ] **Step 2: Check.** `uv run pytest -q && uv run python scripts/check_links.py`; Expected: PASS, 0 broken links.
- [ ] **Step 3: Commit, push, PR.** `git commit -am "tests: v2 Parts I to III labs complete" && git push -u origin restructure/phase-1 && gh pr create --fill`; Expected: CI green.
