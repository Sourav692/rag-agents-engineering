# Phase 6: the switch

Makes the v2 part folders the course. `curriculum.yaml` becomes the v2 curriculum, every build script and test reads the part-folder layout, the generated READMEs and `index.html` pages are rebuilt from v2, and `course/` and `theory/` are deleted last. Read [README.md](README.md) first; its Global Constraints apply, except that this phase is the one allowed to replace `curriculum.yaml` and delete `course/` and `theory/` (approved by the owner, 8 November 2026).

Branch: `restructure/phase-6`, one PR.

## Decisions

- **`curriculum.yaml` becomes v2 and is hand-maintained again.** `plan/switch_v2.py curriculum` writes it once from `curriculum.v2.yaml`: it drops `previous_path` (a `course/` path that stops existing), rewrites each item's `folder` to where the file now lives, and replaces the draft header. `curriculum.v2.yaml` is deleted. `plan/make_curriculum_v2.py` is retired: its input was the v1 `curriculum.yaml`, so it now exits with a message instead of writing, like `scripts/migrate.py`. `CURRICULUM.v2.md` stays as the record of what v2 changed.
- **Provenance kept in `curriculum.yaml`:** `source` on every item, `previous_num` on modules, `previous` on lessons and `previous_title` on parts. The slug mapping below uses them.
- **Item `folder` values** name the folder the file is in: `mandatory/notebook`, `optional/notebook` (exercises included), `projects`, or one of the first two plus a subfolder (`mandatory/notebook/05_training`). `Item.dest` stays `<module dir>/<folder>/<file>`.
- **Layout:** module dir `<part folder>/<module folder>`; module page `<module dir>/mandatory/theory/README.md`; lesson page `<module dir>/<tier>/theory/<NN>_<slug>/README.md`, where the tier is `optional` only when the lesson has items and none is mandatory.
- **Generated in the new layout:** `<part>/README.md`, `<part>/<module>/README.md`, `<part>/<module>/mandatory/theory/index.html`, `THEORY.md` (the theory index that was `theory/README.md`), `capstones/**/README.md`, `CURRICULUM.md`, `NOTICE.md`, `docs/site/index.html`, `docs/agentic-architecture-coverage.md`, `docs/combined-repo.md` and their `docs/site/` pages. `course/README.md` is not replaced: the root `README.md` and `CURRICULUM.md` list the parts.
- **Never written by the build:** `lab/**` (README, `solution/`, `data/`), theory pages, diagrams and interactive labs.
- **forwarddeployedprep.com slugs:** modules and lessons are keyed by module `key` and lesson title, which v2 keeps, so every published slug stays. The three lessons that moved into M26 (`previous` 24.5, 37.4, 37.6) take their slug entries from `react` and `multiagentapps` to a new `deepagents` entry. M26 itself gets new module, overview and interview slugs. The new parts `advagents` and `multiagent` get new track slugs; the v1 tracks `ingest` and `apps` stay in the file, unused, so their slugs are never reused (the site needs redirects for them). Track codes are display labels and are re-sequenced in v2 part order.
- **Retired with the old trees:** `scripts/restructure_part.py` and `tests/test_restructure.py` (they copy out of `course/` and `theory/`).

## Tasks

### Task 6.1: content in the part folders stops pointing at the old trees

**Files:** Create `plan/switch_v2.py` (`content` step); text files under the part folders, `src/rag_paths.py`, `docs/ai-system-design/index.html` (link paths only).

**Interfaces:** `switch_v2.py content` builds the union of `restructure_part.plan()` over all 13 parts (every old file to its new path) and:
- re-points each relative reference that resolves into `course/` or `theory/` (`theory/README.md` goes to `THEORY.md`);
- rewrites GitHub URLs `blob/main/course/...` and `blob/main/theory/...` by the same map;
- sets each module page's meta line to the v2 part numeral and title, with links to the module README (`../../README.md`) and `THEORY.md` and the title line of M33, M45 and M46 to the v2 module title;
- rewrites v1 lesson numbers inside parentheses in theory pages, only where every number in the parentheses is a v1 lesson (`(16.1, 16.3)`); `gpt-4.1` and `Llama 3.2` stay.

It runs first, while `restructure_part.py`, the v1 `curriculum.yaml` and `curriculum.v2.yaml` can still map every old path. It also lists any old file without a copy (expected: only the three v1 part READMEs, which are regenerated).

- [ ] **Step 1: Failing check.** A scan for: relative references from the part folders into `course/` or `theory/`. Expected: about 700.
- [ ] **Step 2: Implement and run.**
- [ ] **Step 3: Verify:** the scan finds 0. Links to `THEORY.md` and the new M26 README stay broken until Task 6.4 builds them.
- [ ] **Step 4: Commit** `switch: re-point part-folder content off course/ and theory/`.

### Task 6.2: `curriculum.yaml` becomes v2; `curriculum_lib.py` reads the part-folder layout

**Files:**
- Modify: `plan/switch_v2.py` (one-time steps, kept as history; created in Task 6.1)
- Modify: `curriculum.yaml` (written by the script), `plan/make_curriculum_v2.py` (retired), `scripts/curriculum_lib.py`, `tests/test_labs.py`
- Delete: `curriculum.v2.yaml`

**Interfaces:**
- `uv run python plan/switch_v2.py curriculum`: writes `curriculum.yaml`, asserts every item's `dest` exists, deletes `curriculum.v2.yaml`.
- `curriculum_lib`: `module_dir(m) -> "<part>/<module>"`, `theory_dir(m) -> "<module dir>/mandatory/theory"`, `lesson_dir(m, n) -> "<module dir>/<tier>/theory/<lesson_folder>"`, `lesson_pages(m) -> dict[int, str]` (existing lesson pages by lesson number), `lesson_tier(lesson) -> "mandatory" | "optional"`, `PART_GLOB = "p[0-9][0-9]_*"`. `COURSE_DIR`, `THEORY_DIR` and `source_root` go.

- [ ] **Step 1: Failing test.** In `tests/test_course.py`, `test_every_curriculum_item_exists` and `test_tiers_and_folders_agree` expect folders `mandatory/...`, `optional/...` or `projects`. Run `uv run pytest -q tests/test_course.py -k "exists or folders"`. Expected: FAIL (v1 folders).
- [ ] **Step 2: Implement** the script and the library functions above; `test_labs.py` reads `curriculum.yaml`.
- [ ] **Step 3: Verify.** `uv run python plan/switch_v2.py curriculum`, then the two tests and `uv run pytest -q tests/test_labs.py`. Expected: PASS.
- [ ] **Step 4: Commit** `switch: curriculum.yaml becomes v2`.

### Task 6.3: `build_theory_html.py` renders the part-folder theory pages

**Files:** Modify `scripts/build_theory_html.py`.

**Interfaces:** `render(m, pages)` and `main()` keep their signatures. Lesson pages come from `lesson_pages(m)` (both tier folders), labs from both tiers' `*/interactive/*.html`, and the page's index link points to `THEORY.md`.

- [ ] **Step 1: Failing test.** `test_theory_module_pages_have_a_current_index_html` (now over the part folders). Expected: FAIL (stale v1 pages).
- [ ] **Step 2: Implement.**
- [ ] **Step 3: Verify** after Task 6.4's build: the test passes.
- [ ] **Step 4: Commit** with Task 6.4.

### Task 6.4: `build_curriculum.py` writes the part-folder READMEs and `THEORY.md`

**Files:** Modify `scripts/build_curriculum.py`, `scripts/site/theory.template.html` (index link text only, if needed).

**Interfaces:** `module_readme(m)` writes `<module dir>/README.md` only (never `lab/`); `part_readme(p)` writes `<part>/README.md`; `theory_index()` writes `THEORY.md`; `course_readme()` goes. The module README's folder-layout section names the tier folders, `lab/solution/` and `lab/data/`.

- [ ] **Step 1: Failing test.** `uv run python scripts/check_links.py` after a build on the old code shows the new pages missing. Expected: broken links.
- [ ] **Step 2: Implement.**
- [ ] **Step 3: Verify.** Build twice; the second run gives no diff (`git status --porcelain` unchanged).
- [ ] **Step 4: Commit** `switch: build the part-folder READMEs and theory pages`.

### Task 6.5: `build_docs.py` describes the new layout

**Files:** Modify `scripts/build_docs.py`.

- [ ] **Step 1:** grep its output for `course/` and `theory/`. Expected: hits.
- [ ] **Step 2: Implement:** the layout tree, the top-level table and the module detail use `<part>/<module>/{mandatory,optional}/{theory,notebook}`, `lab/` and `THEORY.md`; `docs/agentic-architectures.yaml` keeps resolving by source path and module key.
- [ ] **Step 3: Verify:** build; `test_architecture_coverage_refs_are_placed` passes; no `course/` path in `docs/combined-repo.md` outside its history section.
- [ ] **Step 4: Commit** `switch: reference docs on the part-folder layout`.

### Task 6.6: site export on v2 with frozen slugs

**Files:** Modify `scripts/export_site_curriculum.py`, `docs/fde-site-slugs.yaml`, `docs/fde-site-copy.yaml`, `docs/fde-site-mistakes.yaml`.

**Interfaces:** `export()` unchanged; lesson pages from `lesson_pages(m)`; `source` paths `01_Concept_Tutorials/RAG_Agents_Engineering/<part>/<module>/<file>.md`.

- [ ] **Step 1: Failing test.** `test_fde_site_slugs_cover_the_curriculum`, `test_fde_site_mistakes_cover_every_module`, `test_site_curriculum_export_is_complete_and_stable`. Expected: FAIL (no `deepagents`, `advagents`, `multiagent`).
- [ ] **Step 2: Implement** the slug moves in Decisions; new slugs for M26, its overview and interview, and the two tracks; copy for the two tracks from their part summaries; M26 mistakes from its Check yourself questions (moving the ones that came from lessons 24.5, 37.4 and 37.6); module numbers in the mistakes file's comments to v2.
- [ ] **Step 3: Verify:** the three tests pass; `export()` gives the same bytes twice; no published slug changed (`git diff docs/fde-site-slugs.yaml` shows only moves and additions).
- [ ] **Step 4: Commit** `switch: site export on v2, slugs kept`.

### Task 6.7: tests and CI on the new layout

**Files:** Modify `tests/test_course.py`, `tests/test_lab_kit.py` (paths), `.github/workflows/ci.yml`. Delete `scripts/restructure_part.py`, `tests/test_restructure.py`.

- [ ] **Step 1:** the test module lists notebooks under `p*/m*/` outside `lab/`; the theory-layout test checks that every theory README is a module page or a lesson page in its tier folder; labs are found under both tiers.
- [ ] **Step 2:** CI's generated-files check becomes `git diff --exit-code` plus an empty `git status --porcelain` after the build.
- [ ] **Step 3: Verify:** `uv run pytest -q` passes.
- [ ] **Step 4: Commit** `switch: tests and CI on the part folders`.

### Task 6.8: docs describe the new layout

**Files:** `CLAUDE.md`, `README.md`, `LESSON_COVERAGE.md`, `plan/README.md`, `.claude/skills/theory-module/**`, `.agent/skills/theory-module/**` (paths only).

- [ ] **Step 1:** rewrite CLAUDE.md "Theory pages" and "Part folders" sections, the generated/hand-maintained table and the counts (computed from `curriculum.yaml`); README paths and counts; LESSON_COVERAGE.md regenerated in v2 numbers; plan status.
- [ ] **Step 2: Verify:** `check_links.py` 0 broken; counts match a script run.
- [ ] **Step 3: Commit** `docs: describe the part-folder course`.

### Task 6.9: delete `course/` and `theory/`

- [ ] **Step 1:** check that every file under `course/` and `theory/` either has a copy in the part folders or is a generated README / index.
- [ ] **Step 2:** `git rm -r course theory`.
- [ ] **Step 3: Verify:** build idempotent, `uv run pytest -q`, `check_links.py` 0 broken, `git grep -n 'course/\|theory/'` finds only provenance (`docs/source/`, `docs/content-inventory.csv`, `CURRICULUM.v2.md`, `plan/`, history sections).
- [ ] **Step 4: Commit** `switch: delete course/ and theory/`, push, open the PR, check CI.
