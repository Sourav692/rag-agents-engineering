# M17.6 Theory: Retriever patterns compared; hybrid + rerank on Databricks Vector Search

*[M17 theory](../README.md) · Lesson 17.6 · Notebooks: [`06a_advanced_retriever_patterns.ipynb`](../../../../course/p06_retrieval_quality/m17_retrievers_hybrid_search/notebooks/06a_advanced_retriever_patterns.ipynb), [`06b_hybrid_search_and_reranking_databricks.ipynb`](../../../../course/p06_retrieval_quality/m17_retrievers_hybrid_search/optional/06b_hybrid_search_and_reranking_databricks.ipynb) (optional) · [All theory pages](../../../README.md)*

## Choosing a retriever pattern

`06a` runs four retriever patterns over the same eight topic-tagged documents in Chroma with `text-embedding-3-small`. Each fixes a different failure and costs something different:

| Pattern | Fixes | Extra cost per question | How `06a` sets it up |
|---|---|---|---|
| `MultiQueryRetriever` | Wording that misses the documents | 1 LLM call, then one search per generated variant | Base retriever `k = 2`, `gpt-4o-mini` at temperature 0.3 |
| `ContextualCompressionRetriever` + `LLMChainExtractor` | Chunks full of text the question does not need | 1 LLM call per retrieved chunk | Base retriever `k = 4` |
| `EnsembleRetriever` (BM25 + dense) | Exact terms the dense retriever misses | One more search; no LLM call | `k = 3` each, weights 0.4 BM25 and 0.6 dense |
| `ParentDocumentRetriever` | Small chunks that match well but lack context | A docstore lookup | Children of 200 characters (20 overlap) inside parents of 800 (100 overlap), `InMemoryStore` |

The ensemble demo uses three questions chosen to separate the halves: *ACID transactions* (keyword-heavy, BM25 should help), *How do I store AI model outputs for later retrieval?* (worded unlike any document, dense should help), and *fast similarity lookup for embeddings* (mixed). It prints the top result from BM25, dense and the ensemble for each question, side by side. Build your own comparison the same way, with golden questions of each kind.

Because every pattern is a retriever, they nest. `06a`'s last demo wraps multi-query inside compression and feeds the result to a prompt:

```mermaid
flowchart LR
    Q[/Question/] --> MQ["MultiQueryRetriever<br/>LLM writes variants"]
    MQ --> VS["Chroma<br/>k = 3 per variant"]
    VS --> X["LLMChainExtractor<br/>keeps relevant text"]
    X --> G["Prompt +<br/>gpt-4o-mini"]
    G --> A[/Answer/]
```

Multi-query widens the pool for recall and compression narrows each chunk for precision, so the two pull in opposite directions on purpose. The LLM calls add up: one for the variants, one per chunk in the union for extraction, one for the answer.

`06b` moves hybrid search and reranking into the vector store. On a Databricks Vector Search index it embeds the question with `BAAI/bge-large-en-v1.5` (1,024 dimensions, normalised) and makes one call per mode, with `num_results=5`:

| Mode | Arguments added to `index.similarity_search` |
|---|---|
| Vector only | `query_vector` |
| Hybrid | `query_text=query`, `query_type="hybrid"` |
| Hybrid + rerank | and `reranker=DatabricksReranker(columns_to_rerank=["text"])` |

Hybrid in the store and `EnsembleRetriever` in the application do the same job in different places. The store keeps the keyword side next to the vectors and fuses on the server in one round trip. `BM25Retriever` holds its index in application memory and is built from the full document list with `from_documents`, so a changed corpus means rebuilding it. The ensemble is easier to inspect and tune; the store version is easier to run at scale.

`06b` describes the reranker as about 15% better in quality for 1 to 1.5 seconds of extra latency. The notebook states these figures without measuring them; measure your own on the golden set before you pay that latency. [M19](../../m19_reranking_post_retrieval/README.md) covers rerankers and the retrieve-wide, rerank-narrow design.

## Key Takeaways

- Each pattern fixes one failure at its own cost. Multi-query fixes wording, compression trims noisy chunks at one LLM call each, an ensemble catches exact terms, and parent documents restore missing context.
- Patterns nest because each is a retriever, but LLM calls add up across the stack. Count them before you combine.
- Hybrid search in the store fuses on the server in one round trip; an application-side ensemble is easier to inspect. Measure any reranker's gain and latency on your golden set before enabling it.

## Check yourself

<details>
<summary>1. In the nested pipeline, why do multi-query and compression pull in opposite directions, and what do they cost in LLM calls?</summary>

Multi-query widens the pool for recall; compression narrows each chunk for precision. Together they cost one LLM call for the variants, one per chunk in the union for extraction, and one for the answer, so the call count grows with the size of the union.

</details>

<details>
<summary>2. Small 200-character chunks match Larkspur questions well, but the passages that reach the model lack context. Which pattern fixes that, and at what cost?</summary>

`ParentDocumentRetriever`. It searches the small child chunks (200 characters with 20 overlap in `06a`) and returns their 800-character parents. The extra cost is a docstore lookup, with no LLM call.

</details>

<details>
<summary>3. Notebook 06b says the Databricks reranker is about 15% better for 1 to 1.5 seconds of extra latency. Should you turn it on for Larkspur on that basis?</summary>

Not on that basis. The notebook states the figures without measuring them. Measure the quality gain and the added latency on your own golden set before you pay that latency; M19 covers rerankers in depth.

</details>

---
*Previous: [17.5 Multi-faceted filtering](../05_multi_faceted_filtering/README.md). Next: [M17 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
