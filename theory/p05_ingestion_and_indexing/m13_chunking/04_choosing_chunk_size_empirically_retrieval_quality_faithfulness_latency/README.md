# M13.4 Theory: Choosing chunk size empirically: retrieval quality, faithfulness, latency

*[M13 theory](../README.md) · Lesson 13.4 · Notebooks: [`04a_choosing_chunk_size.ipynb`](../../../../course/p05_ingestion_and_indexing/m13_chunking/notebooks/04a_choosing_chunk_size.ipynb), [`04b_choose_chunk_size_llamaindex.ipynb`](../../../../course/p05_ingestion_and_indexing/m13_chunking/optional/04b_choose_chunk_size_llamaindex.ipynb) (optional) · [All theory pages](../../../README.md)*

## Choosing chunk size

No chunk size is right in general. It depends on how dense the facts are, how specific the questions are, the embedding model, the document's structure, and `k` with the token budget, since `chunk_size × k` has to fit the prompt. The notebook replaces the habit of copying 1000/200 or 512/50 with a procedure:

1. Build a small labelled set: a question plus a string that must appear in a correct chunk. Real user queries are the best source. The notebook uses 14 questions over 8 policy sections.
2. Sweep chunk size with everything else fixed. The notebook tries 64 to 768 tokens with `from_tiktoken_encoder`, overlap at 15% of the size and `k = 3`.
3. Score each setting with `hit@k` and a **margin**, how much closer the best correct chunk is to the question than the best wrong one. `hit@k` saturates at 1.0; the margin keeps separating settings after that. A question whose gold string no chunk contains counts as a failure, because the splitter cut it.
4. Put cost in the same table: index tokens (paid once), tokens per query (`chunk_size × k`, paid on every request) and the chunk count.
5. Take the plateau, not the peak. Keep every size within 3% of the best margin, then pick the cheapest of those.
6. Re-score the top three sizes on random halves of the labelled set. If the winner changes between halves, the sizes are indistinguishable at this sample size, so pick on cost.

Sweep overlap afterwards, at the chosen size. It moves the curve far less than size does and grows the index linearly; the notebook keeps 10 to 20% of `chunk_size` as cheap insurance against a fact straddling a boundary. A flat curve is a finding too. It means chunk size is not the bottleneck, so stop tuning it and look at retrieval, query rewriting or reranking.

The optional LlamaIndex notebook measures the answer side instead. GPT-4o judges the faithfulness and relevancy of answers at chunk sizes 128 and 256, and the notebook records response time. LLM judges cost a model call per question per setting, so use the deterministic sweep to narrow the range and the judges to confirm it.

If small chunks win on precision and large ones win on completeness, stop looking for one number. Index small chunks and return their larger parent (M16 parent-document retrieval) or expand to neighbouring chunks after retrieval (M19).

## Choosing a strategy

| Strategy | Boundaries come from | Index-time cost | Best for | Watch out for |
|---|---|---|---|---|
| Recursive character | Separators + size | None | Default for prose | Facts cut at boundaries |
| Token | Tokenizer + size | None | Hard model limits | Cuts mid-sentence |
| Structure-aware | Markup | None | Markdown, HTML, code, manuals | Oversized sections |
| Semantic | Embedding distance | One embedding per sentence | Long prose with topic shifts, no markup | Relative threshold; unbounded chunk size |
| Propositions | An LLM | 1 or 2 LLM calls per chunk | Dense, high-stakes facts | Invented or dropped details without grading |

---
*Previous: [13.3 Proposition chunking with LLM quality checks](../03_proposition_chunking_with_llm_quality_checks/README.md). Next: [M13 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
