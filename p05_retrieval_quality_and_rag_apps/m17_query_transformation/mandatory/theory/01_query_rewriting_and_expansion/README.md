# M17.1 Theory: Query rewriting and expansion

*[M17 theory](../README.md) · Lesson 17.1 · Notebooks: [`01a_query_expansion.ipynb`](../../notebook/01a_query_expansion.ipynb), [`01b_query_transformations_rag_techniques.ipynb`](../../../optional/notebook/01b_query_transformations_rag_techniques.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: A question rarely looks like its answer, so change the question before you search -->
<!-- format: approved -->

## Query–document asymmetry

> **What you'll learn**
>
> - **Explain** the two ways a question differs from the passage that answers it: vocabulary and shape.
> - **Trace** how query expansion sends one text to the retriever and another to the answer prompt.
> - **Match** each M17 transformation to the gap it closes and the calls it costs.
> - **Choose** plain retrieval when no transformation can help.

M16 improved the retriever: two kinds of search, fused, filtered and de-duplicated. Every one of those techniques still searches with exactly what the user typed. M17 changes what is searched for.

A retriever compares the question with each chunk and returns the closest. That works when the two look alike, and a question rarely looks like its answer. In the M10 index, *What happens if my server goes down?* scores 0.000 against both chunks that answer it. Its top three are `reboot` (0.416), `sizing` (0.389) and `export` (0.217), all matched on the word "server". No value of `k` fixes that: the evidence is not low in the ranking, it is absent from it.

**Query–document asymmetry** is the name for this mismatch. It has two parts:

- **Vocabulary**: the user's words are not the handbook's words. The answering chunks say "outage", "availability" and "incident" and never "down".
- **Shape**: a question is short and interrogative; a chunk is long, declarative and dense with terms. Notebook `05a` pairs a nine-word question, *What is LangSmith, and why do we need it?*, with a 400-token passage that answers it. Even with a good embedding model, the question's vector sits closer to other questions than to the passage.

Here are two Larkspur questions beside the chunks that answer them:

| Query (what the user typed) | Chunk that answers it |
|---|---|
| What happens if my server goes down? | Larkspur guarantees 99.95% monthly availability. If an outage pushes availability below that, you receive service credits on the next invoice. |
| How long does a refund take? | Refunds go back to the original payment method and take 5 to 10 business days to appear on your statement. |

*Table 1: Two questions and their evidence. The words barely overlap.*

The second pair shows the vocabulary gap at its smallest. The M10 TF-IDF index does not stem, so "refund" in the question never meets "Refunds" in the chunk, and the timing chunk scores 0.000 too. Embeddings (M13) close part of this gap, because they place paraphrases near each other, and the rest of this module closes more of it at query time.

## Rewriting and expansion

Plain RAG from M10 sends one text everywhere: the question as typed is both the search key and the question the model answers.

```mermaid
flowchart LR
    Q[/Question/] --> R[Retriever]
    R --> A["Answer prompt<br/>chunks + question"]
    Q --> A
```

*Figure 1: Plain retrieval. The same text searches and gets answered: a vocabulary gap goes straight into the search.*

**Query expansion** closes the vocabulary gap with one LLM call. Notebook `01a` asks the model to "expand the following query to improve document retrieval by adding relevant synonyms, technical terms, and useful context", and the expanded text goes to the retriever. The original question still goes to the answer prompt:

```mermaid
flowchart LR
    Q[/Question/] --> X["LLM expands it<br/>synonyms, terms"]
    X --> R[Retriever]
    R --> A["Answer prompt<br/>chunks + original question"]
    Q -- unchanged --> A
```

*Figure 2: Expansion. The retriever sees the enriched text; the model answers the question the user asked.*

The split matters. The expansion exists to find chunks, and an answer prompt built on it would answer a longer, slightly different question.

### One question through notebook 01a

The notebook wires this split into one chain. Here is what each stage holds for its first question:

<div class="walkthrough learning-widget" data-stepper id="expansion-walkthrough">
<p class="widget-intro">Step through one question in notebook 01a, from the index to the answer prompt.</p>
<div class="step-controls" hidden role="group" aria-label="Stages of the expansion chain"><button type="button" data-step="0" aria-pressed="false" aria-controls="expand-step-0">1. Index</button><button type="button" data-step="1" aria-pressed="false" aria-controls="expand-step-1">2. Expand</button><button type="button" data-step="2" aria-pressed="false" aria-controls="expand-step-2">3. Retrieve</button><button type="button" data-step="3" aria-pressed="false" aria-controls="expand-step-3">4. Answer</button></div>
<div class="step-panels"><section id="expand-step-0" class="step-panel" aria-labelledby="expand-heading-0"><h4 id="expand-heading-0">1. Index</h4><dl><dt>Chunks</dt><dd>a text file on LangChain and CrewAI, split into 300-character chunks with 50 characters of overlap</dd><dt>Vectors</dt><dd><code>all-MiniLM-L6-v2</code> embeddings in a FAISS store</dd></dl></section><section id="expand-step-1" class="step-panel" aria-labelledby="expand-heading-1"><h4 id="expand-heading-1">2. Expand</h4><dl><dt>Input</dt><dd><em>What types of memory does LangChain support?</em></dd><dt>Call</dt><dd>one <code>o4-mini</code> call with the expansion prompt: add synonyms, technical terms and useful context</dd><dt>Output</dt><dd>a longer query; its wording changes from run to run</dd></dl></section><section id="expand-step-2" class="step-panel" aria-labelledby="expand-heading-2"><h4 id="expand-heading-2">3. Retrieve</h4><dl><dt>Search key</dt><dd>the expanded text, not the question</dd><dt>Retriever</dt><dd>maximal marginal relevance over the FAISS store, top 5 chunks</dd></dl></section><section id="expand-step-3" class="step-panel" aria-labelledby="expand-heading-3"><h4 id="expand-heading-3">4. Answer</h4><dl><dt>Prompt</dt><dd>the 5 chunks as context, and the <em>original</em> question in the question slot</dd><dt>Calls so far</dt><dd>2 LLM calls and 1 retrieval for one question</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

The notebook's second question, *CrewAI agents?*, is two words long. It is the kind of short query expansion was built for.

`01a` names the two costs. Every retrieval now waits for an LLM call. And expansion can **dilute** the query: each added term pulls the query vector toward more of the corpus, until it is near everything and close to nothing. Three or four well-chosen terms help; a paragraph of synonyms hurts.

The optional notebook `01b` shows the neighbouring moves on one example: a rewrite that makes the query more specific, a step-back query that makes it broader, and decomposition into two to four sub-queries. Each gets its own lesson below.

## Which transformation closes which gap

Every technique in this module adds calls in front of retrieval, and each targets a different gap:

| Technique | Lesson | What it changes | Gap it closes | LLM calls, retrievals |
|---|---|---|---|---|
| Plain RAG | M10 | nothing | none | 1, 1 |
| Rewrite or expand | 17.1 | one query, more terms | vocabulary | 2, 1 |
| Multi-query | 17.2 | 3 phrasings, flat union | vocabulary | 2, 3 |
| RAG-Fusion | 17.3 | 5 phrasings, ranks fused | vocabulary, plus ranking | 2, 5 |
| Step-back | 17.4 | a broader question, searched with the original | a narrow or false premise | 2, 2 |
| HyDE | 17.5 | a hypothetical answer is the search key | shape | 2, 1 |
| Decomposition | 17.6 | 3 independent sub-questions | several needs in one question | 5, 3 |
| Self-query | 17.8 | a semantic query plus a metadata filter | facts an embedding cannot compare | 2, 1 |

*Table 2: The M17 transformations. Counts are per question, answer call included, from each notebook's own code.*

HyDE's retrieval embeds the hypothetical answer instead of the question, at the same cost as embedding the question.

When a question arrives, a short chain of checks picks the transformation:

```mermaid
flowchart TD
    Q[/Question/] --> A{"More than one<br/>need in it?"}
    A -- yes --> D["Decompose<br/>18.6"]
    A -- no --> B{"A condition on a fact:<br/>a date, a plan, a number?"}
    B -- yes --> SQ["Self-query filter<br/>18.8"]
    B -- no --> C{"Specific, or built<br/>on a premise?"}
    C -- yes --> SB["Step-back<br/>18.4"]
    C -- no --> E{"Short, or worded<br/>unlike the docs?"}
    E -- yes --> MQ["Variants or HyDE<br/>18.2, 18.3, 18.5"]
    E -- no --> P["Plain retrieval"]
```

*Figure 3: Pick a transformation by the question's gap. The lesson numbers in the boxes read 18.x; they mean lessons 17.2 to 17.8 of this module.*

Plain retrieval is a valid exit. We call the opposite habit **transform everything**: running a technique on all traffic because it helped some of it.

> **Pitfall: transform everything.** The M10 lab already retrieves both evidence chunks for *Can I export my data after I cancel my plan?* at `k = 2`. Every transformation on that question adds an LLM call and gains nothing. A router (lesson 17.7) makes the choice per question.

## In practice: Larkspur's three golden questions

The three M10 golden questions each fall in a different box of Figure 3:

<div class="learning-widget evidence-switcher" data-comparison id="golden-switcher">
<p class="widget-intro">Choose a golden question to see its gap and the exit it takes in Figure 3.</p>
<div class="mode-controls" hidden role="group" aria-label="Golden question">
<button type="button" data-mode="refund" aria-pressed="false" aria-controls="golden-refund">Refund timing</button>
<button type="button" data-mode="outage" aria-pressed="false" aria-controls="golden-outage">Server goes down</button>
<button type="button" data-mode="export" aria-pressed="false" aria-controls="golden-export">Export after cancel</button>
</div>
<section id="golden-refund" class="mode-panel" data-announcement="Refund question selected. Variants or expansion."><h4>How long does a refund take?</h4><dl><dt>Gap</dt><dd>vocabulary: "refund" never meets "Refunds" in the unstemmed index, and the timing chunk scores 0.000</dd><dt>Exit</dt><dd>variants or expansion (17.2, 17.3)</dd></dl></section>
<section id="golden-outage" class="mode-panel" data-announcement="Outage question selected. Variants with fusion."><h4>What happens if my server goes down?</h4><dl><dt>Gap</dt><dd>vocabulary: both evidence chunks score 0.000; the top three match only on "server"</dd><dt>Exit</dt><dd>variants, with fusion to order the results (17.3)</dd></dl></section>
<section id="golden-export" class="mode-panel" data-announcement="Export question selected. Plain retrieval."><h4>Can I export my data after I cancel my plan?</h4><dl><dt>Gap</dt><dd>none: both evidence chunks are retrieved at <code>k = 2</code></dd><dt>Exit</dt><dd>plain retrieval; any transformation adds a call and gains nothing</dd></dl></section>
<p class="switch-status" aria-live="polite"></p>
</div>

Lesson 17.2 starts on the first two with the simplest variant technique: ask the question three ways.

## Limits

- **Two different indexes.** The 0.000, 0.416 and 0.389 scores come from the M10 TF-IDF index of the Larkspur handbook. Notebook `01a` searches its own LangChain and CrewAI text with MiniLM embeddings, and prints expansions, not scores.
- **No recall measurement.** Neither notebook compares retrieval with and without expansion on a labelled set. The dilution warning is a mechanism, not a measured threshold; measure on your own golden questions before keeping expansion on.
- **Model output varies.** The expanded text comes from `o4-mini` and differs between runs. This page describes it rather than quoting it.
- **Call counts are from the code.** Table 2 counts the calls each notebook makes per question, not the latency or price of those calls.

## References

1. Jagerman et al., [Query expansion by prompting large language models](https://arxiv.org/abs/2305.03653), 2023.
2. Wang, Yang and Wei, [Query2doc: query expansion with large language models](https://arxiv.org/abs/2303.07678), 2023.
3. Ma et al., [Query rewriting for retrieval-augmented large language models](https://arxiv.org/abs/2305.14283), 2023.

## Key Takeaways

- A question rarely looks like its answer: it differs in vocabulary (the user's words against the handbook's) and in shape (short and interrogative against long and declarative).
- Expansion sends an LLM-enriched query to the retriever and the original question to the answer prompt. It costs one LLM call per retrieval, and too many added terms dilute the query.
- Match the transformation to the gap, and keep plain retrieval as an exit. Running one technique on all traffic (transform everything) adds cost where nothing is missing.

## Check yourself

<details>
<summary>1. Why does "What happens if my server goes down?" score 0.000 against both Larkspur chunks that answer it?</summary>

The vocabulary differs. The answering chunks say "outage", "availability" and "incident" and never "down", so a term matcher finds no overlap; the top three, `reboot`, `sizing` and `export`, match only on "server". Embeddings close part of this gap, and query expansion adds the handbook's words to the query.

</details>

<details>
<summary>2. In the expansion chain, which text goes to the retriever and which goes to the answer prompt, and why?</summary>

The expanded text goes to the retriever; the original question goes to the answer prompt. The expansion exists only to find the chunks, and the model should answer what the user asked. The cost is one LLM call before every retrieval, and a risk of diluting the query if too many terms are added.

</details>

<details>
<summary>3. Should you apply a query transformation to "Can I export my data after I cancel my plan?" on the Larkspur index?</summary>

No. The M10 lab already retrieves both its evidence chunks at `k = 2`, so every transformation adds cost with nothing to gain. Plain retrieval is a valid exit, and a router (lesson 17.7) can make that choice per question.

</details>

---
*Previous: [M17 overview](../README.md). Next: [17.2 Multi-query retrieval](../02_multi_query_retrieval/README.md).*
