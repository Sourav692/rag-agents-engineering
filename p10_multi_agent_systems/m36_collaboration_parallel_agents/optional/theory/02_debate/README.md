# M36.2 Theory: Debate

*[M36 theory](../../../mandatory/theory/README.md) · Lesson 36.2 · Notebooks: [`02a_debate.ipynb`](../../notebook/02a_debate.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Two agents arguing opposite sides and a judge who reasons past both earn their seven calls on trade-offs, never on facts -->

## Debate

> **What you'll learn**
>
> - **Explain** the debate loop: two fixed sides, a round counter and a judge with a structured verdict.
> - **Compare** the debate this lesson builds with the other research setup that shares its name.
> - **Diagnose** a debate that adds nothing: parallel monologues, a lopsided persona, a biased judge.
> - **Choose** between debate, a single call and retrieval by asking whether the question has one correct answer.

Lesson 36.1's specialists cooperated on one board. Here two agents disagree on purpose, and the reader of the result sees the strongest case for each side before a decision.

Larkspur's product team asks the support assistant: *should we stop retrieving and put the whole handbook in a long-context prompt?* One model call returns a tidy recommendation. It may be right, but it shows one framing of a question with real costs on both sides: cost per call, accuracy on facts buried mid-context, and access control (the fifth interview question on the [M10 module page](../../../../../p04_rag_foundations/m10_rag_lifecycle/mandatory/theory/README.md#interview-spotlight-5-questions-you-might-get-asked)). The team wants the counter-case argued properly before it commits.

In a **debate** two agents argue opposite sides of a question over several rounds. Each reads the whole transcript and rebuts the other's latest point. A neutral **judge** then writes the verdict:

```mermaid
flowchart LR
    S([Start]) --> A["Side A<br/>rebuts, then argues"]
    A --> B["Side B<br/>rebuts, then argues"]
    B --> R[advance_round]
    R -- more rounds --> A
    R -- done --> J["Judge<br/>structured verdict"]
```

*Figure 1: The round-robin debate graph. Only the two sides and the judge call a model.*

Two research setups share the name:

- **MAD** (Liang et al., EMNLP 2024): fixed affirmative and negative sides, and a judge that reads the debate and extracts the answer. MAD's judge may also end the debate early. The notebook follows MAD but always runs every round.
- **Multiagent debate** (Du et al., 2023): every agent gets the same prompt, answers on its own, then reads the others' answers and revises until they converge. There are no assigned sides and no judge.

The notebook's own question is a classic trade-off: should a six-person team building a new B2B SaaS product start with microservices or a monolith.

## A bounded round-robin

The control flow is a small graph with one counter in state. After side B speaks, an `advance_round` node adds one to the counter, and a routing function sends the graph back to side A or on to the judge. That function is plain Python, and the notebook checks it without a model call. A scratch run of that check gives:

| After round | Counter now | Route |
|---|---|---|
| 1 | 2 | Side A |
| 2 | 3 | Side A |
| 3 | 4 | Judge |

*Table 1: The routing check with `MAX_ROUNDS = 3`, run in the scratchpad. Three rounds, then the judge.*

A counter in code bounds the debate. No agent decides when to stop, so the loop cannot run away the way a blackboard controller can.

## What makes a debate worth reading

Three rules carry the pattern. Each one guards against a named failure:

- **Sides that engage.** Each persona argues its side without inventing facts. After its opening turn it must rebut the opponent's strongest recent point before adding one or two of its own, in at most 120 words in this configuration. Without that rule the debate turns into **parallel monologues**: two cases stated side by side, and nothing for the judge to weigh.
- **A judge that reasons past the debate.** The judge fills a `DebateVerdict`: the strongest point from each side, the weak or overstated claims, a final recommendation and a confidence. Its prompt asks it not to name a winner. The recommendation may be conditional, such as "start with a monolith, split out services when a named pressure appears".
- **A baseline beside it.** The notebook asks the same question in one call with a neutral prompt and prints both answers. A capable model often hedges on its own, and then the debate adds little.

Three weaknesses remain, and the rules above only reduce them:

| Planted weakness | What happens | Why |
|---|---|---|
| **Shared blind spot** | Neither side raises a consideration | Neither persona was primed to look for it |
| **Lopsided debate** | One side wins every exchange | Its persona prompt is stronger than the other's |
| **Biased judge** | The verdict leans one way regardless of the transcript | The judge is one model call and a single point of bias |

*Table 2: Failures the debate pattern does not remove, from the notebook's own analysis.*

> **Pitfall: treating the verdict as ground truth.** A judged recommendation is an argued opinion. When both sides miss a consideration, the judge cannot weigh it.

## Counting the calls

Each round costs two debater turns, and the judge adds one call at the end:

| Approach | LLM calls | What you get |
|---|---|---|
| Single call | 1 | One answer, often already balanced |
| Debate, `N` rounds | `2N + 1` | A transcript, the strongest point from each side, a judged recommendation |
| Debate, `N = 3` (this configuration) | 7 | Six turns and one verdict |

*Table 3: The cost of a debate against a single call. The `advance_round` node makes no model call.*

Latency grows with the calls too, because every turn waits for the one before it. The deliverable is the auditable trail: what each side said, what the judge found strongest and what it rejected.

## Choosing when to debate

Debate earns its cost on questions with legitimate trade-offs and no single correct answer, such as architecture choices, build or buy, and policy. For a factual question with one correct answer, the single call or retrieval is the better choice:

```mermaid
flowchart TD
    Q{"Does the question have<br/>one correct answer?"} -- yes --> H{"Is it in the<br/>handbook?"}
    H -- yes --> R["Retrieve it"]
    H -- no --> S["Single call"]
    Q -- no --> D["Debate<br/>two sides and a judge"]
```

*Figure 2: Route facts to retrieval or one call, and keep debate for trade-offs.*

On the Larkspur handbook that line is clear. "How long does a refund take?" has one answer, 5 to 10 business days, and belongs to retrieval. "Should the support assistant stop retrieving and use a long-context prompt?" is a trade-off, and a transcript with a judged verdict is a useful input to that decision.

A third case looks like a debate and is not one. When two retrieved chunks disagree, for example an old and a new refund policy, one of them is out of date. Fix the index first with version metadata and a filter (M11) rather than asking two agents to argue about which one is current.

## In practice: the long-context question

1. **Frame the question** as a trade-off with two sides: keep retrieval, or move the whole handbook into the prompt.
2. **Write two personas** of equal strength, each told to argue honestly and to rebut before adding a point.
3. **Run three rounds**: six turns and one judge call, seven calls in all.
4. **Run the single-call baseline** and read both answers side by side. Look for what the judge adds: named conditions, a staged path, or a counter-argument the single answer never raised.
5. **List what neither side raised** before treating the verdict as a decision.

Lesson 36.3 keeps several perspectives but makes them cooperate: STORM uses them to research an article instead of arguing.

## Key Takeaways

- A debate runs two opposing sides over `N` rounds, each rebutting the other's latest point, then a judge fills a structured verdict. It costs `2N + 1` calls, 7 at three rounds, against 1 for a single call.
- Require each side to rebut before adding its own points, or the debate becomes parallel monologues. Ask the judge for the strongest point from each side and a recommendation rather than a winner.
- Debate questions with real trade-offs, such as build or buy. Send factual questions like the refund time to retrieval, and fix disagreeing chunks in the index with version metadata.

## Check yourself

<details>
<summary>1. Why must each debater rebut the opponent's strongest recent point before adding one or two of its own?</summary>

Without the rebuttal rule the debate turns into parallel monologues, and the judge has nothing to weigh. Engagement is what lets the judge's verdict name the strongest point from each side and the weak or overstated claims.

</details>

<details>
<summary>2. How many LLM calls does the three-round debate cost against a single call, and what do the extra calls buy?</summary>

`2N + 1` calls, which is 7 for `N = 3` (six turns and one verdict), against 1. They buy a transcript, the strongest point from each side and a judged recommendation. A capable model often hedges on its own, and the single call is the baseline to compare against.

</details>

<details>
<summary>3. Two retrieved Larkspur chunks give an old and a new refund policy. Should two agents debate which one is current?</summary>

No. Fix the index first with version metadata and a filter (M11). Debate earns its cost on trade-offs with no single correct answer. A factual question such as how long a refund takes (5 to 10 business days) belongs to retrieval.

</details>

---
*Previous: [36.1 Blackboard architectures](../../../mandatory/theory/01_blackboard_architectures/README.md). Next: [36.3 STORM: multi-perspective research and writing](../../../mandatory/theory/03_storm_multi_perspective_research_and_writing/README.md).*
