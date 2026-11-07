# Phase 5: v2 Part XIII (M45, M46) and the closing check

Part: `p13_design_decisions`. Depends only on [Phase 0](phase-0-foundations.md) for its own work; Task 5.4 runs after every other phase has merged. Branch: `restructure/phase-5`.

### Task 5.1: Restructure the part

Same steps as [Task 1.1](phase-1-parts-01-03.md#task-11-restructure-the-three-parts), for this part. M45 comes from v1 M04 (Part I) and M46 from v1 M45 (Part XIII): check that M45 keeps its lesson subfolders (`mandatory/notebook/01_why_finetune/` and the rest) and its `assets/`, and that its pages now say M45 where they said M04. Commit message: `content: copy v2 Part XIII into the part-folder layout`.

### Tasks 5.2 and 5.3: labs

Follow the [lab recipe](README.md#lab-recipe-every-module-lab-task-follows-it).

| Task | Module | `data/` contents | Run with | The solution must show |
|---|---|---|---|---|
| 5.2 | M45 Fine-Tuning & Model Adaptation | `larkspur/`, `train.jsonl` (question and answer pairs written from the handbook, at least 100, none copied from `golden.jsonl`) | `hf` group | one narrow task (refund and billing questions); the M10-style RAG baseline (`lab_kit` retrieval plus an LLM) against a small model fine-tuned on `train.jsonl` (a CPU-sized seq2seq model such as `google/flan-t5-small`, a few epochs); both scored on the golden questions of that task; a written verdict on which wins and why, which M46 uses |
| 5.3 | M46 Architecture Synthesis: Choosing a System Design | `larkspur/` | default | a worked two-page design document for capstone A (`capstones/A_enterprise_knowledge_assistant/README.md`): one table row per component with the simpler alternative and why it was not enough, the RAG or fine-tune choice argued from the M45 verdict, and a Mermaid diagram of the design. Code cells only where a claim needs a check, using `lab_kit.baseline` for the "is plain RAG enough" row |

Then add `"p13_design_decisions"` to `DONE_PARTS` and commit.

### Task 5.4: Closing check (after phases 1 to 4 have merged)

- [ ] **Step 1: All 13 parts present.** `ls -d p[0-9][0-9]_* | wc -l`; Expected: `13`. `DONE_PARTS` lists all 13.
- [ ] **Step 2: Every lab has a solution.** `ls p*/m*/lab/solution/m*_solution.ipynb | wc -l`; Expected: `46`.
- [ ] **Step 3: Every v2 item is present.** For each item in `curriculum.v2.yaml`, the path `<part>/<module>/<tier>/notebook/<subfolder>/<file>` exists (a one-off check in the PR, from the same mapping as `plan()`). Expected: 414 of 414.
- [ ] **Step 4: Nothing old changed.** `git diff --stat <phase-0 merge commit> -- course theory curriculum.yaml`; Expected: no output.
- [ ] **Step 5: Full checks.** `uv run pytest -q && uv run python scripts/check_links.py`; Expected: PASS, 0 broken links.
- [ ] **Step 6: Hand-off.** Add a "Status" section to `plan/README.md`: phases done with their PR numbers, unresolved run-time paths found during the restructures, and the next step (the Phase 6 switch plan).
- [ ] **Step 7: Commit, push, PR.** `git commit -am "plan: record the v2 restructure and labs status" && git push -u origin restructure/phase-5 && gh pr create --fill`; Expected: CI green.
