# Tutorial-first teaching format

This reference controls the learner-facing prose. `format.md` and `CLAUDE.md` control exact headings, metadata lines, navigation, concept mapping and the HTML build. Never break those contracts for a nicer-looking article.

## Teaching goal

Make each theory lesson a self-contained technical tutorial that a beginner can follow from a concrete problem to a tested observation. Maintain Staff-level accuracy without assuming that the reader already knows the framework vocabulary.

## Reader journey

Follow this sequence inside the existing lesson-page structure. Adapt length to the topic rather than manufacturing sections with no teaching value:

1. **Problem and goal.** Begin inside the first required `## <exact concept>` heading with a short, concrete situation from the module's running example. Say what the learner will be able to explain, build, debug or decide. Do not begin with notebook IDs, earlier-module codes or long prerequisites.
2. **Small mental model.** Explain only the vocabulary needed for the next step. Use one simple Mermaid diagram when it makes the flow easier to see. Follow the diagram with a short interpretation.
3. **Step-by-step walkthrough.** Use `### Step 1: ...`, `### Step 2: ...` under the required concept heading. Steps should have a learner action or observation, not just another label on an essay. Keep numbering within the concept, or continue it consistently within the lesson.
4. **Working example.** Where code matters, give the smallest correct snippet with imports and assumptions. Prefer one evolving example across steps. Put expected output directly after the snippet, marked **Expected output**, and explain what to notice. Never invent outputs; derive them from a notebook, a tested snippet or an explicitly labeled illustrative case. When code is not useful, use an exact input/output trace, data table, API call, decision walkthrough or failure scenario.
5. **Experiment or contrast.** Change one input, configuration, or failure mode. Tell the learner what to try, what should change, and why. A static comparison suffices when an interactive lab does not help. Keep the original lab requirements when a lab is warranted.
6. **Decision and trade-off.** Include a production consequence, boundary condition, common mistake or decision rule appropriate to the topic. Distinguish classroom examples from production recommendations.
7. **Try it yourself.** Give a short exercise with a clear objective, input or scenario, and a way to check work. Keep the mandatory three `## Check yourself` expandable questions at the end of the lesson, after `## Key Takeaways`.
8. **Practice and resources.** Introduce the relevant notebook or lab in a small `### Practice notebook` subsection within the last relevant concept. Group additional links in a `### Continue learning` subsection, without adding a new conflicting top-level `##` heading.

## Link hygiene

- The page must make sense even if the reader does not open a link.
- No multi-link sentences. At most one supporting link in an explanatory paragraph; if several are needed, move them to a resource list.
- Never use opaque references like `05a`, `T9.1`, `M23` as the sole explanation of what to read. Use human-readable link text such as "Tool-loop error notebook" or "Earlier lesson: tool routing".
- Keep mandatory notebook links in the build-sensitive italic lesson metadata line. That is repository navigation, not explanatory prose. Do not repeat that list inside the introductory paragraph.
- Put prerequisites in a small **Before you start** paragraph only when essential. Explain required ideas briefly before linking back.
- Cite external sources near claims that genuinely require them, without overwhelming the main narrative. Put broader further reading in the last resource subsection.
- Keep the required inline link to a lab beside its `<!-- lab: ... -->` marker, even though other links are consolidated; this is a build/test contract.

## Writing and presentation

- Use descriptive subheadings that state what the learner will do or learn.
- Default to 2 to 4 sentences per paragraph. Split sentences with multiple concepts. Use bullets for genuine sets of actions, conditions or alternatives, not every sentence.
- Explain a technical term in plain language at first use, then use the precise term.
- One main example per lesson where possible. Reuse the established fictional Larkspur Cloud scenario and golden questions when they fit.
- Explain code before or immediately after showing it. Include version-specific caveats where they matter, without inventing API signatures.
- Prefer short tables for configurations, outcomes and trade-offs. Diagram workflows, not facts better conveyed in a sentence.
- Include what a failure looks like and how to diagnose it where relevant. Differentiate tool failure, model decision, and application-level recovery.
- Use measured numbers only from verified notebook output, tested lab or cited source. For conceptual examples, say "Illustrative" and never present fabricated measurements as experiment results.
- The voice is precise, conversationally readable and free of marketing language. Apply `no-ai-slop`: no grandiose introductions, filler, forced epiphanies, excessive bolding, invented benchmarks or decorative closing slogans.

## Example pattern: tool errors

Under the *exact curriculum concept heading*, a good section would read:

### Step 1: Call a tool with valid input

Show the smallest verified tool call and its expected result. Explain what a successful tool message means.

### Step 2: Trigger a controlled failure

Change the server ID to a nonexistent one. Show the actual or verified expected exception.

### Step 3: Configure error handling

Compare default, `True`, and `False` using the behavior supported by the installed LangGraph version. Explain how a `ToolMessage` differs from an escaped exception.

### Step 4: Inspect the agent's next action

Show a trace or table for retry, clarification or stop. Do not imply that turning errors into messages guarantees recovery.

### Step 5: Evaluate the tool call

Separately inspect tool choice, argument values and use of returned data. Include a short deterministic check or walkthrough.

### Try it yourself

Give one bad-input scenario and the expected recovery decision, with a way to check the answer.

### Practice notebook

Link the relevant notebook by descriptive name, followed by one or two purposeful experiments. Do not insert a run of notebook and previous-lesson links into the explanatory text.

## Module overview

Keep the module overview's mandatory sections and exact `Lessons` table. Make the introduction a concrete problem and promise of learning. Use `## Mental model` to orient the learner and `## Lessons` as a logical route through the tutorials. Reserve the module's `## Interview Spotlight` for the existing five applied production scenarios. Do not transform the module overview into a long newsletter, nor duplicate all lessons in it.

## Quality gate

Before finalizing, inspect each lesson and confirm:

- [ ] The first required concept section opens with a specific learner problem, not references.
- [ ] All exact curriculum `##` concept headings still exist on exactly one lesson page.
- [ ] Steps advance the same example and provide observable outputs or decisions.
- [ ] Snippets, APIs and quantitative claims are grounded in notebooks, verified execution or cited sources.
- [ ] There is an experiment or meaningful contrast, and relevant troubleshooting or trade-off guidance.
- [ ] A learner can follow the lesson without opening a notebook or previous lesson.
- [ ] Notebook, lab and related reading links are clearly grouped; mandatory metadata and lab markers remain intact.
- [ ] The required takeaways, three expandable checks, footer, module table, interview questions, animations and lab contracts remain intact.
- [ ] HTML build, tests, link checks, responsive diagram checks and editorial lint from `SKILL.md` have run for pages changed.

Do not change `scripts/resolve.py`, curriculum paths or the site's parsing conventions to achieve tutorial tone. Edit the instructional content, not the loader contract.
