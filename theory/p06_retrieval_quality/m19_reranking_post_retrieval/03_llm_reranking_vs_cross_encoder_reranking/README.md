# M19.3 Theory: LLM reranking vs cross-encoder reranking

*[M19 theory](../README.md) · Lesson 19.3 · Notebooks: [`03a_reranking_methods.ipynb`](../../../../course/p06_retrieval_quality/m19_reranking_post_retrieval/notebooks/03a_reranking_methods.ipynb) · [All theory pages](../../../README.md)*

## LLM reranker or cross-encoder

An LLM can rerank in two ways, and this module shows both. Lesson 19.1's notebook is **listwise**: one prompt holds all eight numbered candidates and asks for "comma-separated document indices" from most to least relevant. This lesson's notebook is **pointwise**: `rerank_documents` asks `gpt-4o` (temperature 0) to rate one document "on a scale of 1-10", reads the number through structured output (`RatingScore.relevance_score`), repeats for every candidate, then sorts and keeps `top_n=3`. The same notebook's `CrossEncoderRetriever` retrieves 10 and keeps 5 after one `predict` call over the 10 pairs with `cross-encoder/ms-marco-MiniLM-L-6-v2`.

| | Listwise LLM (19.1) | Pointwise LLM (19.3) | Cross-encoder (19.2, 19.3) |
|---|---|---|---|
| Calls per question | 1, holding every candidate | 1 per candidate: 15 in the example, up to 30 in `CustomRetriever` | 1 batched `predict` over all pairs |
| Runs on | A hosted LLM | A hosted LLM | Your own CPU or GPU |
| Output | Text to parse into an order | A score from 1 to 10 per chunk | A score per pair |
| Sees other candidates | Yes | No | No |
| Fails by | Dropping or repeating indices | Ties on a 10-point scale, slow sequential calls | Truncating chunks longer than its input limit |

Each failure shows up in the notebook code:

- **Listwise parsing drops documents.** The 19.1 parser keeps only tokens that are digits, then rebuilds the list from them. A chunk the LLM leaves out of its answer disappears from the result, and nothing reports it. Check that the returned indices are a permutation of the inputs, and append any missing ones at the end.
- **Pointwise scores tie.** If the model answers in whole numbers, 15 candidates on a 10-point scale must include ties. Python's sort is stable, so ties keep their stage-1 order, and the reranker decides less than it appears to.
- **Pointwise latency adds up.** The loop calls the model once per document, one after another. Thirty sequential calls take about thirty times the latency of one `gpt-4o` request. Run them in parallel, or score fewer candidates.

The notebook's last example builds a corpus of five chunks to show why reranking helps. Three are short sentences that repeat the question's words without naming the city ("The capital of France is great."), and two are longer passages about visiting Paris. `compare_rag_techniques` prints the top 2 by plain similarity next to the top 2 from the LLM reranker. The notebook does not save its outputs, so run it to see which chunks each method picks.

For Larkspur's support assistant the choice comes down to traffic and stakes. A cross-encoder runs locally with no per-call fee and no parsing step to fail, so it is the default second stage. An LLM reranker earns its cost on low-volume, high-stakes questions where it can follow an instruction a cross-encoder cannot, such as "prefer the current policy over the archived one". A middle path is to let the cross-encoder cut 50 to 10 and the LLM order the last 10. Whichever you pick, compare them on golden-set precision@5 and p95 latency together.

---
*Previous: [19.2 Cross-encoder reranking in a RAG chain](../02_cross_encoder_reranking_in_a_rag_chain/README.md). Next: [19.4 Contextual compression](../04_contextual_compression/README.md).*
