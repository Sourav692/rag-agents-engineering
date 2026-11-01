---
name: theory-module
description: Create or update the theory content for one course module, or for one lesson or topic inside it, in this repo's format (module page and lesson pages in Markdown with Mermaid and SVG diagrams, animated SVG diagrams, a Hallmark lab embedded in the page, and the generated index.html). Use when asked to write, add or extend theory, concepts, diagrams or labs for a module ("theory for M14", "create content for embeddings", "add theory for lesson 11.3", "cover semantic chunking in M13").
argument-hint: <module number, key or name> [lesson number or topic]
---

# Theory module

Writes the theory for a module the way M11 is written: `theory/p04_rag_foundations/m11_rag_lifecycle/` is the reference build. Match it in structure, voice, diagram style, lab design and verification. `CLAUDE.md` → Theory pages holds the rules; this skill is the procedure.

The input is `$ARGUMENTS`:

- **Module mode:** a module only (`14`, `M14`, `embeddings`, `"embeddings and model selection"`). Create every page the module needs, or fill the gaps in one that exists.
- **Topic mode:** a module plus a lesson or topic (`11.3`, `M13 4`, `chunking "semantic chunking"`). If the module has no module page yet, run module mode first; then write or extend that lesson's page and update the module page around it.

Never invent a number, quote, benchmark or API. Every figure on a page comes from a notebook, a lab you built and verified, or a cited source. The running example is the fictional Larkspur Cloud handbook (pricing, refunds, exports, outages, server sizing), shared with M11 to M13.

## 0. Set up

1. Load the `napkin`, `no-ai-slop` and `hallmark` skills (the user's standing rules for this repo). Read `CLAUDE.md` → Theory pages and `references/format.md` in this skill folder.
2. Resolve the argument:

   ```bash
   uv run python .claude/skills/theory-module/scripts/resolve.py $ARGUMENTS
   ```

   It prints the module's `why`, objectives, concepts, lessons with their theory folders and notebooks, which pages, labs and animated diagrams exist, the neighbouring modules, and the matched lesson or concept in topic mode. If it reports no single match, show the closest options and ask. Use its paths; never build folder names by hand (`lesson_folder()` slugs the full lesson title).
3. Read what exists before writing: the module's theory pages if any, `course/<part>/<module>/README.md`, its `lab/README.md`, and the M11 reference pages (module page, a lesson page, `diagrams/lifecycle.anim.html`, the top-k lab).

## 1. Ground the content in the notebooks

Open every mandatory notebook the resolver lists, and the optional ones a concept depends on. Note for each lesson: the APIs and parameters used, the numbers the notebook prints or states, the trade-offs it shows, and which of the module's `concepts:` it teaches. That note is the plan's evidence; claims without it stay out.

## 2. Plan the module, and say the plan before writing

Decide and state in a few lines:

- **Concept to lesson map.** Each entry in `concepts:` goes to exactly one lesson page, the lesson that teaches it (M11: the seven-step lifecycle table went to 11.5, not 11.4). A lesson can hold several concepts or extra sections (M13.4 has "Choosing chunk size" and "Choosing a strategy"). Lessons with nothing to say beyond the notebook stay *planned*: no folder, a `*planned*` row in the module page's Lessons table. A lesson page always has at least one `##` section.
- **Diagrams per page.** One mental-model diagram on the module page; one or two per lesson where a picture beats prose. Mermaid first. SVG in `diagrams/` only for spatial layouts and charts Mermaid cannot draw. Animate only diagrams that show a process over time (a pipeline, a loop): usually the module's mental model plus one more. Decision trees, comparisons and charts stay static.
- **The lab.** At most one per module unless two lessons each have a parameter worth playing with. A lab earns its place when moving one control changes a number the prose argues about (M11: `k` against recall, precision and tokens). Prefer running the real algorithm in JS when it is small (TF-IDF, recursive splitting, BM25, cosine, MMR); otherwise hand-placed outputs labelled representative. Pick the lesson it belongs to and the section it sits in.
- **Running example.** Which part of the Larkspur handbook carries this module, and the golden questions it uses.

In topic mode also state: which existing sections of the module page change (Lessons row, TL;DR bullet, mental model, How it connects, interview questions, takeaways), and that nothing else is rewritten.

## 3. Write the pages

Follow `references/format.md` exactly: headings, header and footer lines, the Lessons table, the Interview Spotlight shape, link styles. In short:

- **Module page** `theory/<part>/<module>/README.md`: title line, meta line, intro with the "Each idea has a page…" sentence, running-example paragraph, `## TL;DR`, `## Mental model` (diagram, then one paragraph), `## Lessons` table, `## Interactive lab`, `## How it connects`, `## Interview Spotlight: 5 Questions You Might Get Asked`, `## Key Takeaways`, previous/next footer.
- **Lesson page** `<lesson folder>/README.md`: title, header line with module page, lesson number and notebooks, then the `## <concept>` sections (exact `concepts:` text), then `## Key Takeaways` (three bullets, four when the page has four or more concepts: the mechanism, decision rule, trade-off or number to remember, each drawn from the page and none copying a Check yourself answer), then `## Check yourself`, then the footer chaining to the neighbouring lesson pages.
- **Check yourself:** three questions per lesson page, each a `<details>` block (`<summary>N. Question?</summary>`, blank line, a 2 to 4 sentence answer, blank line, `</details>`): one on the core mechanism, one applying it to the page's example or numbers, one diagnosing a failure or making a decision. Answers use only facts on the page. Questions are plain text (no Markdown or module codes: neither GitHub nor the site renders them inside `<summary>`). `test_lesson_pages_end_with_check_yourself` checks the shape.
- **Interview Spotlight:** five production scenarios on this module's running example, never "what is X". Cover at least one incident or debugging question, one design trade-off, one measurement or monitoring question and one edge case. Each has four "What a strong answer covers" bullets.
- **Links:** notebooks by their `course/` path, other modules by number in prose and by relative path to their theory module page when one exists. Relative paths from the file being written; `check_links.py` verifies them.

In topic mode: write or extend only the target lesson page; on the module page change the Lessons row (planned to link), and only the other sections the plan named. Keep each concept heading on one page: moving a concept means removing its old heading. Keep the previous/next footers of the neighbouring lesson pages pointing at their real neighbours.

## 4. Diagrams

- **Mermaid** (`references/format.md` → Mermaid): it must stay readable at 614px wide. Short edge labels, detail inside nodes with `<br/>`, no many-into-one convergence (it puts every leaf on one row), a chain of yes/no questions instead of one question with four long answers.
- **SVG** in `diagrams/*.svg`: its own light sheet background and the Almanac hex palette from `CLAUDE.md`, a `<title>` and `<desc>`, text 13px or more. Compute any plotted values (percentiles, scores); never eyeball them.
- **Animated SVG** in `diagrams/<name>.anim.html`, marked by `<!-- animated: diagrams/<name>.anim.html -->` on the line after its Mermaid block. Copy the structure of `theory/p04_rag_foundations/m11_rag_lifecycle/diagrams/lifecycle.anim.html`: the leading comment, `<figure class="anim sheet">`, an `.anim__canvas` with the SVG, hidden Previous, Play and Next controls, and an `.anim__steps` list whose buttons are short step names, each followed by a `<span>` sentence. Mark elements `in-N` (appears at step N), `mv-N` with `style="--from: translate(…)"` (moves in), `n-N` (node lit while step N is current) and `e-N` (edge lit). For a travelling marker use `<circle class="tok">` and `data-tok="x,y"` on each step button. Colours only through the classes in `scripts/site/theory-anim.css`; at most eight steps (the CSS covers 1 to 8); use the lab's real numbers or none. Unique marker ids per figure (`ah-<name>`).

## 5. The lab

Copy the structure and stylesheet of `theory/p04_rag_foundations/m11_rag_lifecycle/02_indexing_from_scratch_with_tf_idf_and_nearest_neighbours/interactive/top-k-retrieval-lab.html`, then design this lab's own controls and output. Keep:

- The Hallmark stamp block first in the CSS (shape app screen, theme Almanac, the deal seed, signature, critique line), the Almanac tokens, Google Fonts as the only external request, `overflow-x: clip` on `html` and `body`, eight control states, `:focus-visible`, a reduced-motion rule.
- One control that changes what the prose argues about, live numbers, the output object (table, chart or page view), and a dynamic reading paragraph that names what just changed.
- **Embedded mode**, so the module page can frame it: the head script that adds `embedded` to `<html>` inside a frame; `html.embedded` rules that hide the bar and intro, set `overflow-y: hidden`, and order the parts (`display: contents` on the stacks, `order` on the reading and secondary sheets) so the control and its main output share one screen in a 700px column; and the `ResizeObserver` that posts `{ labHeight: document.body.getBoundingClientRect().height + 2 }` to the parent.
- **Verification:** port small algorithms exactly and compare against the Python library on every control position (M13's splitter: 1,061 settings, 0 mismatches; M11's TF-IDF: within 1e-16 of scikit-learn). Write the comparison in the scratchpad and keep its result for the report. Every number the prose quotes from the lab must be one the lab prints.

Mark where it embeds with `<!-- lab: interactive/<name>.html -->` on its own line in the lesson page, in the section whose claims it tests, and link it inline in that section (`The [interactive lab](interactive/<name>.html) …`) so the test finds it. Give the module page's `## Interactive lab` section the lab's name in bold, "open the file in a browser", and two or three things to try that show the payoff.

## 6. Edit the prose

Run the `no-ai-slop` edit over every page before building: no en or em dashes anywhere (write "20 to 50", "M14 to M16"), no "not X, it's Y", no faux-insight setups, no colon reveals, no closing aphorisms, no invented metrics. Keep the voice of the M11 pages: plain declaratives, numbers from the lab, short sections.

## 7. Build and verify

```bash
uv run python scripts/build_curriculum.py       # module README links, theory/README.md, and every module's index.html
uv run pytest -q                                 # includes test_theory_pages_mirror_the_course_layout and the index.html freshness test
uv run python scripts/check_links.py
```

Then check the pages as a reader would (`references/format.md` → Verification): serve the repo with `python3 -m http.server <port> --bind 127.0.0.1` in the background, open `theory/<part>/<module>/index.html` at 1280px and at 390px with Playwright, and confirm every Mermaid diagram rendered to SVG, no diagram shrinks below 75% (`scale` from the viewBox), each animated figure steps through all its steps and autoplays when scrolled into view, the lab frame sized itself with no inner scrollbar, and the page has no sideways scroll. Then lint copies outside the repo, since sloplint writes `.hallmark/` beside its input:

```bash
S=<scratchpad>/lint; rm -rf $S && mkdir -p $S && cp -R theory $S/
cd $S/theory && node ~/.claude/skills/hallmark/scripts/sloplint.mjs <part>/<module>/index.html --genre editorial --render
node ~/.claude/skills/hallmark/scripts/sloplint.mjs <part>/<module>/*/interactive/*.html --scope app --render
```

`--render` needs `HALLMARK_PUPPETEER` pointing at a `puppeteer-core` install (`npm install --prefix <scratchpad>/hm puppeteer-core@23.11.1`, then `export HALLMARK_PUPPETEER=<scratchpad>/hm/node_modules/puppeteer-core`). Fix every FAIL. Page-level waivers live in the stamp of `scripts/site/theory.template.html`; change the template only for a fault every module has, and rebuild all pages after. Stop the server and delete `.playwright-mcp/` and any screenshots in the repo.

## 8. Report

Say what was written (pages, concepts per lesson, diagrams static and animated, the lab and its verification result), what stays planned and why, the check results (tests, links, sloplint), and anything you could not confirm. Do not commit unless asked. Record any new gotcha in `.claude/napkin.md`.
