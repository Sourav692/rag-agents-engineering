# M18.3 Theory: LLM reranking vs cross-encoder reranking

*[M18 theory](../README.md) · Lesson 18.3 · Notebooks: [`03a_reranking_methods.ipynb`](../../notebook/03a_reranking_methods.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: An LLM can follow instructions a cross-encoder cannot, at a price paid per candidate -->

## LLM reranker or cross-encoder

> **What you'll learn**
>
> - **Compare** listwise LLM, pointwise LLM and cross-encoder reranking by calls, output and failure.
> - **Diagnose** three LLM reranking failures: the silent drop, score ties and serial latency.
> - **Do** the arithmetic on calls and ties for a candidate list of 15.
> - **Choose** a reranker for Larkspur by traffic and stakes.

Lesson 18.2 showed a cross-encoder demoting a near miss by reading question and chunk together. An LLM reads them together too, and it can also follow an instruction. Larkspur's handbook holds an archived refund policy alongside the current one; "prefer the current policy" is an instruction no cross-encoder can take.

An LLM can rerank in two ways, and this module shows both:

- **Listwise**: one prompt holds every numbered candidate and asks for their indices from most to least relevant. Notebook `01a` does this with eight candidates.
- **Pointwise**: one call per candidate rates it on a scale of 1 to 10, read back through structured output; the scores are then sorted. Notebook `03a` does this with an LLM at temperature 0 and keeps the top 3.

Here is how the three rerankers spend their calls on one question:

```mermaid
flowchart TB
    subgraph L["Listwise LLM"]
    direction LR
    L1["1 prompt<br/>all candidates"] --> L2["Parse an order<br/>from text"]
    end
    subgraph P["Pointwise LLM"]
    direction LR
    P1["1 call per<br/>candidate"] --> P2["Sort the<br/>1 to 10 scores"]
    end
    subgraph C["Cross-encoder"]
    direction LR
    C1["1 batched pass<br/>over all pairs"] --> C2["Sort the<br/>scores"]
    end
```

*Figure 1: Three ways to rerank one candidate list.*

`03a` also builds a cross-encoder retriever that retrieves 10 chunks and keeps 5, after one batched scoring call over the 10 pairs with `ms-marco-MiniLM-L-6-v2`. The three compare like this:

| | Listwise LLM (`01a`) | Pointwise LLM (`03a`) | Cross-encoder (`02a`, `03a`) |
|---|---|---|---|
| Calls per question | 1, holding every candidate | 1 per candidate: 15 in the example, up to 30 in `03a`'s custom retriever | 1 batched pass over all pairs |
| Runs on | A hosted LLM | A hosted LLM | Your own CPU or GPU |
| Output | Text to parse into an order | A score from 1 to 10 per chunk | A score per pair |
| Sees other candidates | Yes | No | No |
| Fails by | Dropping or repeating indices | Ties, slow sequential calls | Truncating chunks longer than its input limit |

*Table 1: Three rerankers compared.*

## How each one fails

Each failure in Table 1's last row shows up in the notebook code.

**The silent drop.** `01a`'s parser keeps only the tokens that are digits and rebuilds the list from them. A chunk the LLM leaves out of its answer disappears from the result, and nothing reports it. Check that the returned indices are a permutation of the inputs, and append any missing ones at the end.

**Score ties.** Fifteen candidates scored in whole numbers from 1 to 10 cannot all differ: there are only ten values, so at least six candidates share their score with another candidate. In practice an LLM uses fewer than ten values, so ties are larger. The sort keeps tied chunks in their stage-1 order, so the reranker decides less than it appears to.

**Serial latency.** The pointwise loop calls the model once per document, one after another. The arithmetic, with an assumed 1 second per call:

| Candidates | Sequential calls | Wall-clock, sequential | Wall-clock, 10 in parallel |
|---|---|---|---|
| 15 | 15 | about 15 s | about 2 s |
| 30 | 30 | about 30 s | about 3 s |

*Table 2: Pointwise LLM reranking latency (illustrative: assumes 1 s per call and no rate limits).*

Parallel calls fix the latency, not the cost: 30 calls are billed as 30 whichever way they run.

> **Pitfall: the silent drop.** Any reranker whose output is parsed from text can lose candidates without an error. Assert that every input index comes back exactly once.

`03a`'s last example builds a corpus of five chunks to show why reranking helps. Three are short sentences that repeat the question's words without naming the city ("The capital of France is great."), and two are longer passages about visiting Paris. It prints the top 2 by plain similarity next to the top 2 from the LLM reranker. The notebook ships without outputs, so the comparison has to be run to be read; this page quotes no result from it.

## Choosing for Larkspur

The choice comes down to traffic and stakes:

```mermaid
flowchart TD
    A{"Needs an instruction,<br/>e.g. prefer current policy?"} -- no --> CE["Cross-encoder"]
    A -- yes --> B{"Low volume,<br/>high stakes?"}
    B -- yes --> LLM["LLM reranker<br/>on the top 10"]
    B -- no --> MD["Metadata filter<br/>then cross-encoder"]
```

*Figure 2: Default to a cross-encoder; pay for an LLM only when an instruction matters and traffic is low.*

A cross-encoder runs locally with no per-call fee and no parsing step to fail, so it is the default second stage. An LLM reranker earns its cost on low-volume, high-stakes questions where it can follow an instruction. A middle path is to let the cross-encoder cut 50 candidates to 10 and the LLM order the last 10.

The archived-policy problem has a cheaper answer than either. A `version` filter before ranking (lesson 16.5) removes the old policy outright, so no reranker has to be told to prefer the new one.

## In practice: Larkspur's second stage

1. **Cross-encoder by default**, over 20 hybrid candidates, as lessons 18.1 and 18.2 set up.
2. **Version filter before ranking**, so instructions about freshness are not needed.
3. **LLM reranker for escalations only**: billing disputes routed to a human-review queue, a few dozen a day, on the cross-encoder's top 10.
4. **Compare on precision@5 and p95 latency together** on the golden set; a reranker that wins on one and loses badly on the other does not ship.

Ranking decides which chunks reach the prompt. Lesson 18.4 decides how much of each one does.

## Key Takeaways

- A listwise LLM sends every candidate in one prompt, a pointwise LLM rates each chunk in its own call, and a cross-encoder scores all pairs in one batched pass on your own hardware.
- Listwise parsing can drop candidates silently, pointwise scores tie (15 candidates on a 10-point scale must share values) and add a call per candidate, and cross-encoders truncate long chunks.
- Default to a cross-encoder; use an LLM reranker for low-volume, high-stakes questions that need an instruction, and filter stale versions out before either.

## Check yourself

<details>
<summary>1. A listwise LLM reranker returns its order as text, and one chunk never appears in the final list. What happened, and what check prevents it?</summary>

The silent drop: the parser rebuilds the list only from the indices the model wrote, so a chunk the model left out disappears without an error. Assert that the returned indices are a permutation of the inputs, and append any missing ones at the end.

</details>

<details>
<summary>2. A pointwise LLM reranker scores 15 candidates in whole numbers from 1 to 10. Why must some tie, and what decides their order?</summary>

There are only ten possible values for fifteen candidates, so at least six share their score with another, and an LLM usually uses fewer values. The sort is stable, so tied chunks keep their stage-1 order: the reranker decides less than it appears to.

</details>

<details>
<summary>3. Larkspur wants the reranker to prefer the current refund policy over an archived copy. Which tool do you reach for first?</summary>

A `version` metadata filter before ranking. It removes the archived copy outright, so no reranker has to be instructed. Only if a real instruction remains, on low-volume, high-stakes traffic, does an LLM reranker over the cross-encoder's top 10 earn its per-call cost.

</details>

---
*Previous: [18.2 Cross-encoder reranking in a RAG chain](../02_cross_encoder_reranking_in_a_rag_chain/README.md). Next: [18.4 Contextual compression](../04_contextual_compression/README.md).*
