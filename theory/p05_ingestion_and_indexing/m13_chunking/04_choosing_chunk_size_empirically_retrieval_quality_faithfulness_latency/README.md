# M13.4 Theory: Choosing chunk size empirically: retrieval quality, faithfulness, latency

*[M13 theory](../README.md) · Lesson 13.4 · Notebooks: [`04a_choosing_chunk_size.ipynb`](../../../../course/p05_ingestion_and_indexing/m13_chunking/notebooks/04a_choosing_chunk_size.ipynb), [`04b_choose_chunk_size_llamaindex.ipynb`](../../../../course/p05_ingestion_and_indexing/m13_chunking/optional/04b_choose_chunk_size_llamaindex.ipynb) (optional) · [All theory pages](../../../README.md)*

## Choosing chunk size

Choose the size empirically. Sweep three to five sizes and two overlaps, and score each on the golden set: hit rate for retrieval, faithfulness and correctness for answers, plus index size and latency. If small chunks win on precision and large ones win on completeness, stop looking for one number. Index small chunks and return their larger parent (M16 parent-document retrieval) or expand to neighbouring chunks after retrieval (M19).

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
