# Lesson shape

Every lesson page uses this shape, in every mode. The model is `standalone/references/example-lesson.md` (rendered as `example-lesson.html`, the visual target), with one rule changed: **no code**. Where that page shows a code block and its `#### OUTPUT ####`, a page written now shows a traced table, a results table or a figure, and the notebooks keep the code.

The page reads like an engineer walking a colleague through a problem they will hit: a concrete failure, the idea that fixes it, the evidence, the trade-off, and where it breaks. Sections carry **descriptive headings** ("Pattern 2: ReAct planning", "Where one round breaks", "Planted failure: the runaway loop"). Never write `### Step N:` headings; when order matters, use a numbered list inside a section or a sequence diagram.

## Sections, in order

| Section | What it holds | Course README | Standalone |
|---|---|---|---|
| Title + subtitle | Plain title; one line naming what the page resolves | `# M22.1 Theory: <title>`, header line, then `<!-- subtitle: … -->` | frontmatter `title`, `subtitle` |
| **What you'll learn** | Callout, 3 to 5 bullets, each opening with a bold verb (**Explain**, **Compare**, **Diagnose**, **Choose**) | first thing inside the first `##` section | right after the `# Title` |
| Recap | 2 to 4 sentences linking the previous lesson | first paragraph of the first section (no heading) | `## Recap` |
| The problem | The running example failing in a concrete way; the one-line reason; the jobs the rest of the page must do. Usually a shared-skeleton figure | descriptive `##` heading, or the first concept heading | `## The problem` |
| What we show, and what we claim | Only when the page reports runs: the pieces in the order we need them (`- **Short label**: what it is.`), numbered claims the page will settle, and a map table (Table 1) of the options | optional | optional |
| Concept sections | One per idea (course: one per `concepts:` entry, exact text, plus any extra sections). See below | `## <exact concept>` | `## <Pattern N: …>` |
| Choosing / trade-offs | A decision flowchart and a comparison table (rows: reach, cost, main risk…) | descriptive `##` | `## Choosing …` |
| In practice | The running example (Larkspur) through the idea, as a short numbered walkthrough plus a callout on what changes in the next lesson | `## In practice: <Larkspur case>` | same |
| Verdicts | Claims table: # · Claim · Verdict (**Holds** / **Fails** / **Open**) · Evidence. Only when the page made claims | optional | optional |
| Limits | What the evidence did not test, then "left out, and when to add it" bullets | optional | optional |
| References | Numbered, linked, dated. Only cited sources | `## References`, before Key Takeaways | `## References` |
| Summary | "So overall, …" paragraph + 3 to 5 bullets | `## Key Takeaways`: 3 bullets (4 when the page has four or more concepts), no paragraph | `## Summary` |
| Questions | Course: `## Check yourself` (three `<details>`, contracts.md). Standalone: `## Talking points`, 4 to 8 `- **Label:** question` bullets | `## Check yourself`, last section | `## Talking points` |
| Next | One line naming the next lesson | the previous/next footer | `## Next` |

Course READMEs keep every contract in `contracts.md` (header line, exact concept headings, Key Takeaways right before Check yourself, the footer). Inside those, follow this table. Avoid generic headings ("The problem", "Recap", "Summary") on course pages: `index.html` joins all lesson pages of a module into one page with one table of contents, so name each section for its content.

## Inside a concept section

Choose the order that fits the idea; most sections use most of these:

1. **Define** the term in one bold sentence, then the intuition in plain words.
2. **Show the mechanism** in prose and one figure (sequence diagram for calls over time, state diagram for a loop, flowchart for a pipeline or a check order).
3. **Trace an example** through it as a table: what went in, what came out, what changed. Real values from a notebook run, or labelled *Illustrative*.
4. **Plant a failure.** A table of bad inputs (malformed call, unknown name, missing argument, runaway loop, lenient critic…) with what the system returned and why. Each guard gets one planted case.
5. **Name the failure mode** in bold the first time (*one-shot blindness*, *runaway loop*, *context creep*, *stringly-typed answer*) and reuse the name.
6. **Do the arithmetic** for any cost, token, latency or size claim, in a small table with stated assumptions.
7. **Close with a bridge**: one sentence that sets up the next section, as a statement.

## Code becomes evidence

| In the example | Write instead |
|---|---|
| A function or class definition | A sentence on what it does and why, plus a figure of where it sits; name identifiers only when the reader will meet them in the notebook |
| A code block and its `#### OUTPUT ####` | A traced table (Round · Call · Observation) or a results table (Input · Returned · Why), with a `*Table N: …*` caption |
| Planted-failure code | A planted-failures table, one row per guard |
| Raw JSON or protocol tags | A table of the fields and what each one decides |
| "Run it in the notebook" exercises | A conceptual question in Check yourself or Talking points |

## Figures, tables and callouts

- Introduce each figure or table with one sentence ending in a colon, then the artefact, then a caption on its own line: `*Figure 3: Validate in this order. Each failure becomes a specific message the model can act on.*` or `*Table 2: Input tokens resent per ReAct round (illustrative).*` Number figures and tables separately, in page order, and refer to them by number.
- Length: at most 2,500 words as the site counts them (forwarddeployedprep.com `check:content`, ENH-25, blocks the push). Aim for 1,500 to 2,300 in the exported `.md`; cut repeated caveats and illustrative tables before cutting a concept.
- A concept lesson has 3 to 7 figures. One idea per figure, at most 12 nodes, labels of 4 words or fewer.
- Callouts, at most one per ~400 words, plain bold label, no emoji: `> **Key distinction:** …`, `> **Pitfall: <name>.** …`, `> **Interview tip:** …`.
- Comparison tables may use ✓ and ✗.
