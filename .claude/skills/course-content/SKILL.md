---
name: course-content
description: Create or rewrite theory content for the AI Engineering course and forwarddeployedprep.com. Create mode writes a module's theory (module page, lesson pages, Mermaid/SVG/animated diagrams, an embedded Hallmark lab) or one lesson or topic in it; rewrite mode turns existing theory pages into clear, conversational, theory-only prose with every topic and diagram kept (review in chat, or edit); standalone mode writes a lesson for a topic or track outside the course. Every lesson follows one shape (problem, mechanism, traced tables, planted failures, trade-offs, limits) and ships as a Markdown plus HTML pair in the Forward Deployed style. Pages carry no code: notebooks hold it. Use for "theory for M14", "add theory for lesson 11.3", "cover semantic chunking in M13", "rewrite lesson 22.5", "make this page theory-only", "write a lesson on context engineering for the agentic track".
argument-hint: <module | lesson | topic | path | URL> [rewrite [review|edit] | --standalone <track>]
---

# Course content

One skill for all theory writing. The input is `$ARGUMENTS`. `CLAUDE.md` → Theory pages holds the repository rules; this file is the procedure, and the references hold the detail:

| File | Read it for |
|---|---|
| `references/contracts.md` | Load-bearing page shapes (module page, lesson page), Mermaid/SVG/animated-diagram/lab formats, browser verification. Create and rewrite. |
| `references/lesson.md` | The lesson shape: sections in order, what goes inside a concept section, how code becomes tables and figures. Every mode. |
| `references/voice.md` | The reader, the theory-only rule, sentence rules, the quality gate. Every mode. |
| `references/rewrite.md` | Coverage inventory, protected blocks, review vs edit. Rewrite mode. |
| `references/standalone.md` | Frontmatter, the system-design template, the HTML builder, track emphasis. Standalone mode. |

## Pick the mode

| Input | Mode |
|---|---|
| A module (`14`, `M14`, `embeddings`) or a lesson/topic (`11.3`, `M13 4`, `chunking "semantic chunking"`) whose page is missing or has gaps | **create** |
| The same, or a theory README path or site URL, plus `rewrite` (`review` by default, `edit` to change files) | **rewrite** |
| `--standalone <track> <topic>`, or a topic that is not one of the 46 modules | **standalone** |

When a page exists and the user did not say `rewrite`, ask once whether to extend it (create) or rewrite it. If the mode or target is still unclear, ask one question.

**Rules for every mode.** No code blocks and no notebook links in the body (`voice.md` → Theory only). Never invent a number, quote, benchmark or API: every figure comes from a notebook run, a lab you built and verified, or a cited source. The running example is the fictional Larkspur Cloud handbook (pricing, refunds, exports, outages, server sizing).

## 0. Set up

1. Load `napkin` and `no-ai-slop` (plus `hallmark` when building a lab). Read `CLAUDE.md` → Theory pages, `references/lesson.md`, `references/voice.md`, the mode's reference, and skim `standalone/references/example-lesson.html` for the target look.
2. Resolve course targets:
   ```bash
   uv run python .claude/skills/course-content/scripts/resolve.py <module> [<lesson or topic>]
   ```
   It prints the module's `why`, objectives, concepts and which page holds each, lessons with theory folders and notebooks, existing pages, labs and animated diagrams, neighbours, and the matched lesson or concept. No single match: show the closest options and ask. Use its paths; never build folder names by hand.
3. Read what exists: the module's theory pages, `<part>/<module>/README.md`, `lab/README.md`, and the M10 reference (`p04_rag_foundations/m10_rag_lifecycle/mandatory/theory/`: module page, a lesson page, `diagrams/lifecycle.anim.html`, the top-k lab).

Rewrite mode continues in `references/rewrite.md`, then step 7. Standalone mode continues in `references/standalone.md`. Create mode follows steps 1 to 8.

## 1. Ground the content in the notebooks

Open every mandatory notebook the resolver lists, and the optional ones a concept depends on. For each lesson note the mechanisms shown, the numbers the notebook prints or states, the trade-offs, and which `concepts:` it teaches. Notebooks ship without outputs: get numbers by running their deterministic code in the scratchpad. Claims without evidence stay out. The page explains what the code demonstrates; it never reproduces the code.

## 2. Plan, and say the plan before writing

State in a few lines, and wait for approval when writing a whole module:

- **Concept to lesson map.** Each `concepts:` entry goes to exactly one lesson page, the one that teaches it. A lesson with nothing to say beyond its notebook stays *planned* (no folder, a `*planned*` row). A lesson page has at least one `##` section.
- **Diagrams per page.** One mental-model diagram on the module page; one or two per lesson where a picture beats prose. Mermaid first; SVG only for spatial layouts and charts Mermaid cannot draw. Animate only processes over time, usually the mental model plus one more.
- **The lab.** At most one per module unless two lessons each have a parameter worth playing with. It earns its place when one control changes a number the prose argues about. Name its lesson and section.
- **Running example.** The handbook area and golden questions, and one concrete request or failure to follow through each lesson.
- **Per lesson:** the subtitle, the concrete failure it opens on, its sections in `lesson.md` order with their headings, the figures and tables (numbered), the planted failures and their names, any claims it will settle, and the decision rule.

Topic mode also states which module-page sections change (Lessons row, TL;DR bullet, mental model, How it connects, interview questions, takeaways); nothing else is rewritten.

## 3. Write the pages

Contracts from `contracts.md`, shape from `lesson.md`, prose from `voice.md`.

- **Module page** `<theory>/README.md`: title, meta line, intro with the "Each idea has a page…" sentence, running-example paragraph, `## TL;DR`, `## Mental model`, `## Lessons`, `## Interactive lab`, `## How it connects`, `## Interview Spotlight: 5 Questions You Might Get Asked`, `## Key Takeaways`, footer.
- **Lesson page** in the folder `resolve.py` gives (`mandatory/theory/` or `optional/theory/`): title, header line and `<!-- subtitle: … -->`, then the `lesson.md` sections with each `## <exact concept>` among them (What you'll learn opens the first section), `## Key Takeaways` (three bullets, four when the page has four or more concepts), `## Check yourself`, footer. No `### Step N` headings.
- **Check yourself:** three `<details>` blocks (`<summary>N. Question?</summary>`, blank line, 2 to 4 sentence answer, blank line, `</details>`): the mechanism, an application to the page's example or numbers, and a diagnosis or decision. Plain-text questions; answers use only the page.
- **Interview Spotlight:** five production scenarios on the running example, never "what is X": at least an incident, a design trade-off, a measurement or monitoring question and an edge case, each with four "What a strong answer covers" bullets.

Topic mode: write or extend only the target lesson page, flip its Lessons row from planned to linked, and change only the module-page sections the plan named. Moving a concept removes its old heading. Keep neighbouring footers pointing at real neighbours.

## 4. Diagrams

Follow `contracts.md` → Mermaid, SVG diagrams, Animated fragment. Readable at 614px: short edge labels, detail inside nodes with `<br/>`, no many-into-one convergence, yes/no chains instead of one question with four long answers. SVGs: own sheet background, Almanac hex palette, `<title>` and `<desc>`, text 13px or more, plotted values computed. Animated fragments: copy `lifecycle.anim.html`'s structure, at most eight steps, the lab's real numbers or none, unique marker ids.

## 5. The lab

Copy the structure and stylesheet of M10's `top-k-retrieval-lab.html`, then design this lab's own control and output. Keep the Hallmark stamp, Almanac tokens, Google Fonts as the only external request, `overflow-x: clip`, eight control states, `:focus-visible`, reduced motion, a live reading paragraph, and embedded mode (`contracts.md` → Lab file). Port small algorithms exactly and compare against the Python library on every control position; keep the comparison result for the report. Every number the prose quotes from the lab must be one the lab prints. Mark the spot with `<!-- lab: interactive/<name>.html -->` and link it inline in that section.

## 6. Edit the prose

Run the `voice.md` quality gate, then `no-ai-slop`, over every page.

## 7. Build and verify

```bash
uv run python .claude/skills/course-content/scripts/protect.py [--rewrite] <changed pages>   # no code blocks; rewrite: diagrams unchanged vs HEAD
uv run python scripts/build_curriculum.py
uv run pytest -q
uv run python scripts/check_links.py
uv run python .claude/skills/course-content/scripts/export_lesson.py <changed lesson pages>     # the .md + .html pair
```

The export writes `site-export/<track>/<module>/<NN>-<lesson>.md` (git-ignored) with frontmatter from `curriculum.yaml` and `docs/fde-site-slugs.yaml`, then renders the `.html` beside it with `standalone/scripts/build_site.py` (`--md-only` skips it; `--out DIR` moves it). Open one `.html` at 1254px and 390px, light and dark, and look at every diagram.

Then the browser check in `contracts.md` → Verification: serve the repo with `python3 -m http.server <port> --bind 127.0.0.1`, open the module's `index.html` at 1280px and 390px, and confirm every Mermaid diagram rendered, none below 75% scale, animations step and autoplay, the lab frame sized itself, no sideways scroll. Lint copies outside the repo (sloplint writes `.hallmark/` beside its input):

```bash
S=<scratchpad>/lint; rm -rf $S && mkdir -p $S && cp -R p[0-9][0-9]_* $S/
cd $S && node ~/.claude/skills/hallmark/scripts/sloplint.mjs <part>/<module>/mandatory/theory/index.html --genre editorial --render
node ~/.claude/skills/hallmark/scripts/sloplint.mjs <part>/<module>/*/theory/*/interactive/*.html --scope app --render
```

`--render` needs `HALLMARK_PUPPETEER` pointing at a `puppeteer-core` install. Fix every FAIL; page-level waivers live in `scripts/site/theory.template.html`. Never hand-edit a generated `index.html`. Stop the server; delete `.playwright-mcp/` and screenshots in the repo. Rewrite in review mode skips this step, except the export: run it with `--out <scratchpad>` on each draft as `<draft>=<lesson README>` so the user can open the HTML.

## 8. Report

Both paths of every exported pair, then what was written or changed (pages, concepts per lesson, diagrams static and animated, the lab and its verification), what stays planned and why, check results, anything unconfirmed, and in rewrite mode the flags from `rewrite.md` → Report. Do not commit unless asked. Record new gotchas in `.claude/napkin.md`.
