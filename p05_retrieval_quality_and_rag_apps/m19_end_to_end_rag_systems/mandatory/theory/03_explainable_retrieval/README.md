# M19.3 Theory: Explainable retrieval

*[M19 theory](../README.md) · Lesson 19.3 · Notebooks: [`03a_explainable_retrieval.ipynb`](../../notebook/03a_explainable_retrieval.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: An explanation written after the ranking describes the text, not why it was ranked -->

## Explaining a retrieved chunk

> **What you'll learn**
>
> - **Trace** an explainable retriever: one search, then one explanation call per chunk.
> - **Diagnose** an explanation that rationalises a ranking error.
> - **Separate** explaining a chunk to a user from debugging a ranking.
> - **Redesign** the explainer as a relevance grader.

Lesson 19.2 linked each answer to the chunks that support it. A user can still ask the step before that: why did the system pick these chunks at all?

Notebook `03a` answers with an **explainable retriever**. It wraps a FAISS index with `k = 5` and, for every chunk it returns, makes one more LLM call that writes a paragraph on why the chunk fits the query. The output is a list of pairs: the chunk's content and its explanation.

```mermaid
flowchart LR
    Q[/Query/] --> R["FAISS retriever<br/>k = 5"]
    R --> C1["chunk 1"] --> E1["LLM call:<br/>explain chunk 1"]
    R --> C2["chunk 2"] --> E2["LLM call:<br/>explain chunk 2"]
    R --> CK["chunk k"] --> EK["LLM call:<br/>explain chunk k"]
```

*Figure 1: One retrieval, then one explanation call per chunk.*

Three properties of this design decide where it is useful.

## It costs one call per chunk

The loop calls the explanation chain `k` times, one after another. At `k = 5` a single search becomes five model calls before any answer is written:

| Explained chunks | Explanation calls | With the answer call |
|---|---|---|
| All 5 retrieved | 5 | 6 |
| Only the 2 the answer cites | 2 | 3 |
| Only the one a user expands | 1, on demand | 1 + 1 |

*Table 1: Calls per question for three explanation policies.*

Run the calls as one batch to cut the wait, or explain only what a reader will look at.

## It explains the text, not the ranking

The prompt says "Explain why this context is relevant to the query". The model never sees the similarity score or the other chunks, and it is not offered "this chunk is not relevant" as an answer.

On the Larkspur handbook that matters. In the M10 TF-IDF index, *What happens if my server goes down?* ranks the `reboot` chunk first, on the shared word "server" ([M10.2](../../../../../p04_rag_foundations/m10_rag_lifecycle/mandatory/theory/02_indexing_from_scratch_with_tf_idf_and_nearest_neighbours/README.md#top-k)). Asked why `reboot` is relevant, with no way to say it is not, the model's likely reply is a reason:

| Retrieved chunk | Why it ranked first | Likely explanation (*Illustrative*) |
|---|---|---|
| `reboot`: "You can reboot a server from the console…" | Shares "server" with the question (TF-IDF 0.416) | "Rebooting is one way to recover a server that has gone down." |

*Table 2: An explanation for a ranking error (illustrative reply).*

That reads as an explanation and is a rationalisation of a ranking error. We call it the **rationalised miss**. The chunk was ranked by similarity between two vectors; the paragraph is the model's reading of the query and the chunk side by side, written after the fact.

> **Key distinction:** an explanation can guide a user and mislead an engineer. To debug retrieval, print the scores and the rank of the chunk you expected, never the explanation.

## Ask a question that can say no

A version that helps both readers changes the question:

| `03a` asks | Ask instead |
|---|---|
| Why is this context relevant? | Is this context relevant to the query? Answer yes or no, then quote the sentence that decides it. |
| One free-text paragraph | A structured result: relevant or not, a verbatim evidence quote, and the retriever's score |
| Every retrieved chunk | Only the chunks the answer used, or the ones a user expands |

*Table 3: From explainer to relevance grader.*

The yes-or-no form is a **relevance grader**. On the `reboot` chunk it can return "no", with the score beside it, which is the signal the explainer could never give. [M28](../../../../../p08_agentic_rag/m28_retrieval_grading_rewriting/mandatory/theory/README.md) uses it to filter chunks and rewrite the query, and [M32.1](../../../../../p08_agentic_rag/m32_reliability_feedback/mandatory/theory/01_reliable_rag_relevance_checks_hallucination_checks_source_highlighting/README.md#relevance-grading) adds a hallucination check and source highlighting on top.

Two notes on running `03a` today. Its retriever call uses a method that the current LangChain core no longer has, so it raises an attribute error; the current call is the retriever's standard invoke. And the demo indexes three sentences with `k = 5`; FAISS returns all three, so each query gets three explanations, including two for texts about photosynthesis and global warming when the question is why the sky is blue. That is forced top-k (lesson 16.1) again, now with a paragraph defending each forced pick.

## In practice: explanations for Larkspur agents

1. **Explain on demand**: a support agent clicks a source to see why it is there; no call is spent otherwise.
2. **Grade, then explain**: ask the yes-or-no question first, and show the verbatim evidence quote as the explanation.
3. **Show the score** beside every explanation, so a weak match is visible as weak.
4. **Debug with ranks**, logged per query, never with explanation text.

Lesson 19.4 leaves free text: Larkspur's server catalogue is a table, and a table row needs its own representation before it can be retrieved.

## Key Takeaways

- An explainable retriever adds one LLM call per chunk. Batch the calls, or explain only the chunks the answer cites or a user expands.
- A prompt that asks why a chunk is relevant gets a reason even for a ranking error (the rationalised miss). The paragraph explains the text, not the ranking, so debug retrieval with scores and ranks.
- Ask a yes-or-no relevance question with a verbatim quote and the retriever's score instead. That turns the explainer into a relevance grader that can say no.

## Check yourself

<details>
<summary>1. The explainable retriever runs with k = 5. How many LLM calls does one question cost before the answer, and how would you reduce them?</summary>

Five, one explanation per retrieved chunk, made one after another. Batch them to cut the wait, and explain only the chunks the answer cites, or only the one a user expands, to cut the count.

</details>

<details>
<summary>2. For "What happens if my server goes down?", the explainer says the reboot chunk is relevant because rebooting recovers a server. Why should an engineer distrust this?</summary>

It is a rationalised miss. TF-IDF ranked `reboot` first only because it shares the word "server", and the prompt asked why the chunk is relevant with no option to say it is not. The paragraph describes the text after the fact; the score and the rank of the expected chunks show what actually happened.

</details>

<details>
<summary>3. How do you change the explainer so it can flag the reboot chunk as a bad retrieval?</summary>

Ask a yes-or-no question instead: is this context relevant, then quote the sentence that decides it. Return a structured result with the verdict, the verbatim evidence and the retriever's score. That relevance grader can answer "no" for `reboot`, which the "why is this relevant" prompt never could.

</details>

---
*Previous: [19.2 Answers with sources and per-claim citations](../02_answers_with_sources_and_per_claim_citations/README.md). Next: [19.4 RAG over structured data: CSV and JSON](../04_rag_over_structured_data_csv_and_json/README.md).*
