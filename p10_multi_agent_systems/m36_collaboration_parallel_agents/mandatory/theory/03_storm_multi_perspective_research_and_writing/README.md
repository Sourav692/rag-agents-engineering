# M36.3 Theory: STORM: multi-perspective research and writing

*[M36 theory](../README.md) · Lesson 36.3 · Notebooks: [`03a_storm.ipynb`](../../notebook/03a_storm.ipynb) · [All theory pages](../../../../../theory/README.md)*

## STORM

A broad Larkspur research article needs complementary questions before it needs polished sections. You will run the perspective, interview, extraction and outline stages, then count the calls and inspect where the facts came from.

### Step 1: Plan distinct research perspectives

STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective question asking; Shao et al., NAACL 2024, [arXiv:2402.14207](https://arxiv.org/abs/2402.14207)) writes a long article on a topic the writer knows little about. A single "write an article about X" prompt tends to give one generic angle. STORM researches first, from several perspectives, and writes only from what the research found:

```mermaid
flowchart LR
    T[/Topic/] --> P["Perspectives<br/>P editor personas"]
    P --> I["Interviews<br/>one per persona, T turns"]
    I --> O["Outline<br/>one merged structure"]
    O --> D["Drafts<br/>one per section"]
    D --> A[/Article/]
```

1. **Perspective generation.** One structured-output call proposes `P` distinct editor personas, each a different professional lens on the topic.
2. **Simulated interviews.** For each persona, a persona-editor asks one focused question at a time and an expert answers, for `T` turns; both roles are the same model with different system prompts. A third call extracts the transcript's facts into a typed list.
3. **Outline synthesis.** An editor-in-chief call merges every persona's facts into one ordered outline of 4 to 6 sections.
4. **Section drafting.** A writer call drafts each section from the research notes. A last call writes the title.

Debate (lesson 36.2) uses opposing perspectives to decide. STORM uses complementary ones to research.

### Step 2: Carry extracted findings rather than whole transcripts

Each stage consumes the previous stage's typed object (`PerspectiveList`, `ResearchFindings`, `ArticleOutline`), produced with `with_structured_output`, so no stage parses free text. Only the extracted facts travel into the outline and the drafts; the transcripts stay for audit, so you can trace which question surfaced which fact. Two steps decide quality:

- **Persona design.** Three reworded generalists produce redundant research. If the personas overlap, tighten the perspective prompt, for example by listing the disciplines to draw from.
- **Outline synthesis.** This is where `P` research threads become one narrative. An outline with one section per persona is a concatenation, and the synthesis prompt needs to ask for a merged structure.

### Step 3: Identify the missing retrieval boundary

The example's expert is the model playing a knowledgeable role, with no retrieval, so its "facts" are only as reliable as the model's memory. That is the pattern's main weakness. Swapping the expert's plain call for a tool-using agent grounds it without changing any later stage. On the Larkspur handbook the expert would answer from a handbook retriever: for an article on what happens to an account when a customer cancels, a billing persona would surface the 30-day refund window and the 5 to 10 business days a refund takes, and a data persona the 30 days of retention before deletion, each fact traceable to its chunk.

### Step 4: Calculate the research budget before running it

The cost is fixed by the parameters before the run starts: one call for the perspectives, `2T + 1` per interview (`T` questions, `T` answers, one extraction), one for the outline, one per section and one for the title.

```
calls = 1 + P × (2T + 1) + 1 + S + 1
```

| Perspectives `P` | Turns `T` | Calls | With `S` = 4 to 6 sections |
|---|---|---|---|
| 3 | 2 | 18 + S | 22 to 24 (this configuration) |
| 3 | 3 | 24 + S | 28 to 30 |
| 5 | 2 | 28 + S | 32 to 34 |
| 5 | 3 | 38 + S | 42 to 44 |

The example attaches a callback that counts every chat-model call, structured-output calls included, and compares the count with this arithmetic. Capping `P` (`perspectives[:NUM_PERSPECTIVES]`) and `S` (`MAX_SECTIONS = 6`) keeps the cost bounded when the model returns more than it was asked for.

Latency is a different number from cost. The interviews are independent of each other, but the example runs them in a Python `for` loop, so their waits add up. Dispatching one branch per persona with `Send` (lesson 36.5's map-reduce) puts them in one superstep: the same calls, with the interview stage taking about as long as its slowest interview. The section drafts are independent in the same way.

### Try it yourself

Choose three perspectives and two interview turns each. With four to six written sections, check the total of twenty-two to twenty-four calls. Now inspect a factual claim from the expert: if the expert has no retrieval tool, its confident answer is still model memory. Specify what source evidence must accompany it.

### Practice notebook

Run the complete implementation from the practice material after checking the trace or calculation above. Use its stated environment for live model or server calls; recorded model choices and timings are observations, not guaranteed outputs.

- [Storm](../../notebook/03a_storm.ipynb).

### Continue learning

- [lesson 36.5](../05_parallel_agents_async_nodes_and_streaming/README.md#map-reduce--async).

## Key Takeaways

- STORM researches before it writes. `P` personas each run a `T`-turn interview, their extracted facts merge into one outline, and each section is drafted from what the research found.
- Quality rests on distinct personas and an outline that merges the research threads. One section per persona is a concatenation, and an expert with no retrieval is only as reliable as the model's memory.
- Cost is fixed before the run at `1 + P × (2T + 1) + 1 + S + 1` calls, 22 to 24 in the recorded configuration. Dispatch the interviews with `Send` so the stage takes about as long as the slowest interview.

## Check yourself

<details>
<summary>1. In STORM, why do only the extracted facts travel into the outline and the drafts, while the interview transcripts stay behind?</summary>

Each stage consumes the previous stage's typed object (`PerspectiveList`, `ResearchFindings`, `ArticleOutline`), so no stage parses free text. The facts list is the payload; the transcripts are kept for audit, so you can trace which question surfaced which fact.

</details>

<details>
<summary>2. How many model calls does a STORM run make with 5 perspectives, 2 interview turns and 5 sections?</summary>

33 calls: 1 for the perspectives, 5 × (2 × 2 + 1) = 25 for the interviews, 1 for the outline, 5 for the sections and 1 for the title. The table's row for `P` = 5 and `T` = 2 gives 28 + S, which is 33 at `S` = 5.

</details>

<details>
<summary>3. A STORM outline comes back with exactly one section per persona. What has gone wrong, and where do you fix it?</summary>

The outline is a concatenation of the research threads, not a synthesis. Outline synthesis is where `P` threads become one narrative, so fix the editor-in-chief's synthesis prompt to ask for a merged structure. If the sections also repeat each other, the personas overlap, and the perspective prompt needs tightening.

</details>

---
*Previous: [36.2 Debate](../../../optional/theory/02_debate/README.md). Next: [36.4 Meta-controllers, ensembles and emergent systems](../../../optional/theory/04_meta_controllers_ensembles_and_emergent_systems/README.md).*
