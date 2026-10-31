# M17.1 Theory: The retriever interface and its search modes

*[M17 theory](../README.md) · Lesson 17.1 · Notebooks: [`01a_retrievers.ipynb`](../../../../course/p06_retrieval_quality/m17_retrievers_hybrid_search/notebooks/01a_retrievers.ipynb) · [All theory pages](../../../README.md)*

## Search modes

A LangChain retriever takes a query string and returns a list of `Document`s through `invoke(query)`. That one signature is why retrievers stack: a wrapper that calls another retriever and post-processes its list is itself a retriever, so a chain cannot tell a plain vector search from a hybrid, compressed, multi-query one.

`vectorstore.as_retriever(search_type=..., search_kwargs=...)` turns a vector store into a retriever. `01a` builds a twelve-sentence Chroma store with `text-embedding-3-small` and tries each mode on questions such as *what is the old capital of India?*:

| Mode | How `01a` builds it | What it returns |
|---|---|---|
| Similarity | `search_type="similarity"`, `k=3` | The 3 nearest chunks, however far away they are |
| MMR | `search_type="mmr"`, `k=3`, `fetch_k=10` | 3 of the 10 nearest, chosen to differ from each other ([17.4](../04_maximal_marginal_relevance_for_diversity/README.md)) |
| Score threshold | `search_type="similarity_score_threshold"`, `k=3`, `score_threshold=0.3` | Up to 3 chunks, only those with relevance ≥ 0.3; possibly none |
| Multi-query | `MultiQueryRetriever.from_llm(retriever, llm)` | The union of results for several LLM-written rewordings of the question |
| Contextual compression | `ContextualCompressionRetriever` with `LLMChainExtractor` or `LLMChainFilter` | The same chunks cut down to the relevant sentences, or only the chunks an LLM judges relevant |
| Ensemble | `EnsembleRetriever(retrievers=[...], weights=[0.7, 0.3])` | One list merged from several retrievers by weighted Reciprocal Rank Fusion ([17.3](../03_fusion_retrieval_score_normalisation_vs_rank_fusion/README.md)) |

Similarity search always returns `k` chunks. Ask the twelve-sentence store about something it does not hold and you still get three sentences back; ask the Larkspur handbook index about a product Larkspur does not sell and the model still receives three handbook chunks. A score threshold is the first defence against that, and it is easy to get wrong because stores report scores in two directions:

- `similarity_search_with_score` returns a **distance**: lower is closer. `01a` sets `collection_metadata={"hnsw:space": "cosine"}` because Chroma uses Euclidean distance unless told otherwise.
- `similarity_search_with_relevance_scores`, and the `score_threshold` mode built on it, use a **relevance score**: higher is closer. For cosine, Chroma's `_select_relevance_score_fn()` computes `1 - distance`, so the distance `0.35375` in `01a` becomes a relevance of `0.64625`.

`01a`'s custom retriever does the conversion itself inside a `@chain` function, writes the rounded score into `doc.metadata["score"]`, and keeps chunks above a threshold (`0.51` for *what is the financial capital of India?*). Storing the score in metadata pays off later: you can log it, show it, and tune the threshold from real distributions. A threshold belongs to one embedding model and one distance function; carry it to another model and it means something else.

The wrappers spend LLM calls to fix different problems. Multi-query adds one LLM call per question and several searches to raise recall when the wording is off. Compression adds one LLM call per retrieved chunk to cut tokens and noise. Ensemble adds no LLM call; it costs one extra search per retriever, and in `01a` it merges a compressed retriever with a plain one over the same store, which shows that ensembles are not only for dense plus sparse. [17.6](../06_retriever_patterns_compared_hybrid_rerank_on_databricks_vector_search/README.md#choosing-a-retriever-pattern) compares them side by side.

## Check yourself

<details>
<summary>1. Why can a chain not tell a plain vector search from a hybrid, compressed, multi-query retriever?</summary>

Every retriever has one signature: `invoke(query)` takes a string and returns a list of `Document`s. A wrapper that calls another retriever and post-processes its list is itself a retriever, so retrievers stack and the chain sees the same interface at every depth.

</details>

<details>
<summary>2. Chroma in cosine space reports a distance of 0.35375 for a chunk. What does the score threshold mode compare, and does the chunk pass a threshold of 0.3?</summary>

It compares a relevance score, where higher is closer: for cosine, Chroma computes `1 - distance`, so 0.35375 becomes 0.64625, which passes 0.3. `similarity_search_with_score` reports the distance, where lower is closer; mixing the two directions is the usual threshold mistake.

</details>

<details>
<summary>3. Larkspur users ask about a product Larkspur does not sell, and the model still receives three handbook chunks. Why, and what is the first defence?</summary>

Similarity search always returns `k` chunks, however far away they are. A score threshold is the first defence. Set it from real score distributions, which is why `01a` writes the score into `doc.metadata["score"]`, and remember that a threshold belongs to one embedding model and one distance function.

</details>

---
*Previous: [M17 overview](../README.md). Next: [17.2 Dense + sparse hybrid retrieval with BM25 and EnsembleRetriever](../02_dense_sparse_hybrid_retrieval_with_bm25_and_ensembleretriever/README.md).*
