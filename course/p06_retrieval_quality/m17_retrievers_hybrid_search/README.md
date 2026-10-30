# M17 — Retrievers & Hybrid Search

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VI · Retrieval Quality Engineering** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 2 optional

## Why it matters

Dense vectors miss exact terms such as IDs, names and codes; keyword search misses paraphrase. Production retrieval usually combines both.

## Theory

Read the [theory page](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Fusing BM25 and dense rankings](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/03_fusion_retrieval_score_normalisation_vs_rank_fusion/interactive/hybrid-fusion-lab.html) (open the file in a browser)

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
| 17.1 | The retriever interface and its search modes ([theory](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/01_the_retriever_interface_and_its_search_modes/README.md)) | [`01a_retrievers.ipynb`](notebooks/01a_retrievers.ipynb) | — |
| 17.2 | Dense + sparse hybrid retrieval with BM25 and EnsembleRetriever ([theory](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/02_dense_sparse_hybrid_retrieval_with_bm25_and_ensembleretriever/README.md)) | [`02a_dense_sparse_hybrid_retrieval.ipynb`](notebooks/02a_dense_sparse_hybrid_retrieval.ipynb) | [`02b_hybrid_search_rag.ipynb`](optional/02b_hybrid_search_rag.ipynb) *(extension)* |
| 17.3 | Fusion retrieval: score normalisation vs rank fusion ([theory](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/03_fusion_retrieval_score_normalisation_vs_rank_fusion/README.md)) | [`03a_fusion_retrieval.ipynb`](notebooks/03a_fusion_retrieval.ipynb) | — |
| 17.4 | Maximal Marginal Relevance for diversity ([theory](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/04_maximal_marginal_relevance_for_diversity/README.md)) | [`04a_maximal_marginal_relevance.ipynb`](notebooks/04a_maximal_marginal_relevance.ipynb) | — |
| 17.5 | Multi-faceted filtering ([theory](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/05_multi_faceted_filtering/README.md)) | [`05a_multi_faceted_filtering.ipynb`](notebooks/05a_multi_faceted_filtering.ipynb) | — |
| 17.6 | Retriever patterns compared; hybrid + rerank on Databricks Vector Search ([theory](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/06_retriever_patterns_compared_hybrid_rerank_on_databricks_vector_search/README.md)) | [`06a_advanced_retriever_patterns.ipynb`](notebooks/06a_advanced_retriever_patterns.ipynb) | [`06b_hybrid_search_and_reranking_databricks.ipynb`](optional/06b_hybrid_search_and_reranking_databricks.ipynb) *(platform-specific)* |

## Hands-on lab

Hybrid upgrade: add BM25 to the vector retriever, tune the fusion weights on the golden set, and find three queries that only hybrid search answers. Details: [lab/README.md](lab/README.md).

## Key concepts

[Dense vs sparse](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/02_dense_sparse_hybrid_retrieval_with_bm25_and_ensembleretriever/README.md#dense-vs-sparse) · [BM25](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/02_dense_sparse_hybrid_retrieval_with_bm25_and_ensembleretriever/README.md#bm25) · [Reciprocal Rank Fusion](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/03_fusion_retrieval_score_normalisation_vs_rank_fusion/README.md#reciprocal-rank-fusion) · [MMR λ](../../../theory/p06_retrieval_quality/m17_retrievers_hybrid_search/04_maximal_marginal_relevance_for_diversity/README.md#mmr-λ)

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
