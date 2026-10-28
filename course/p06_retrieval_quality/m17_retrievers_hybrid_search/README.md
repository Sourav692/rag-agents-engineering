# M17 — Retrievers & Hybrid Search

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VI · Retrieval Quality Engineering** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 2 optional

## Why it matters

Dense vectors miss exact terms such as IDs, names and codes; keyword search misses paraphrase. Production retrieval usually combines both.

## Learning objectives

- Use the retriever interface: similarity, score threshold, MMR, multi-query, compression, ensemble
- Combine dense and sparse (BM25) retrieval and build a RAG chain on top
- Fuse rankings with normalised scores and with Reciprocal Rank Fusion
- Trade relevance against diversity with Maximal Marginal Relevance
- Filter by metadata, similarity threshold, keywords and diversity together

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 17.1 | The retriever interface and its search modes | [`01a_retrievers.ipynb`](notebooks/01a_retrievers.ipynb) | — |
| 17.2 | Dense + sparse hybrid retrieval with BM25 and EnsembleRetriever | [`02a_dense_sparse_hybrid_retrieval.ipynb`](notebooks/02a_dense_sparse_hybrid_retrieval.ipynb) | [`02b_hybrid_search_rag.ipynb`](optional/02b_hybrid_search_rag.ipynb) *(extension)* |
| 17.3 | Fusion retrieval: score normalisation vs rank fusion | [`03a_fusion_retrieval.ipynb`](notebooks/03a_fusion_retrieval.ipynb) | — |
| 17.4 | Maximal Marginal Relevance for diversity | [`04a_maximal_marginal_relevance.ipynb`](notebooks/04a_maximal_marginal_relevance.ipynb) | — |
| 17.5 | Multi-faceted filtering | [`05a_multi_faceted_filtering.ipynb`](notebooks/05a_multi_faceted_filtering.ipynb) | — |
| 17.6 | Retriever patterns compared; hybrid + rerank on Databricks Vector Search | [`06a_advanced_retriever_patterns.ipynb`](notebooks/06a_advanced_retriever_patterns.ipynb) | [`06b_hybrid_search_and_reranking_databricks.ipynb`](optional/06b_hybrid_search_and_reranking_databricks.ipynb) *(platform-specific)* |

## Hands-on lab

Hybrid upgrade: add BM25 to the vector retriever, tune the fusion weights on the golden set, and find three queries that only hybrid search answers. Details: [lab/README.md](lab/README.md).

## Key concepts

Dense vs sparse · BM25 · Reciprocal Rank Fusion · MMR λ

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `projects/` — runnable sub-projects (e.g. MCP servers and clients), where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_retrievers.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/07_retrievers_and_hybrid_search/notebooks/01_retrievers.ipynb` |
| `notebooks/02a_dense_sparse_hybrid_retrieval.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/07_retrievers_and_hybrid_search/notebooks/02_dense_sparse_hybrid_retrieval.ipynb` |
| `optional/02b_hybrid_search_rag.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/07_retrievers_and_hybrid_search/notebooks/03_hybrid_search_rag.ipynb` |
| `notebooks/03a_fusion_retrieval.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/07_retrievers_and_hybrid_search/notebooks/04_fusion_retrieval.ipynb` |
| `notebooks/04a_maximal_marginal_relevance.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/07_retrievers_and_hybrid_search/notebooks/05_maximal_marginal_relevance.ipynb` |
| `notebooks/05a_multi_faceted_filtering.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/07_retrievers_and_hybrid_search/notebooks/06_multi_faceted_filtering.ipynb` |
| `notebooks/06a_advanced_retriever_patterns.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/07_retrievers_and_hybrid_search/notebooks/07_advanced_retriever_patterns.ipynb` |
| `optional/06b_hybrid_search_and_reranking_databricks.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/07_retrievers_and_hybrid_search/notebooks/08_hybrid_search_and_reranking_databricks.ipynb` |
