# M08 — Query Transformation & Routing

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part III · Retrieval Quality Engineering** · **Level:** Core · **Time:** ~7 h · **Notebooks:** 9 mandatory, 6 optional

## Why it matters

Users write short, vague or compound questions. Rewriting the query before retrieval is often the cheapest large gain available.

## Learning objectives

- Rewrite and expand queries with an LLM
- Generate multiple query variants and merge their results (multi-query, RAG-Fusion)
- Retrieve with a more general question (step-back) or a hypothetical answer (HyDE)
- Decompose multi-hop questions into sub-questions
- Route queries with an LLM classifier or by semantic similarity, and turn questions into metadata filters (self-query)

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 8.1 | Query rewriting and expansion | [`01a_query_expansion.ipynb`](notebooks/01a_query_expansion.ipynb) | [`01b_query_transformations_rag_techniques.ipynb`](optional/01b_query_transformations_rag_techniques.ipynb) *(alternate)* |
| 8.2 | Multi-query retrieval | [`02a_multi_query_retrieval.ipynb`](notebooks/02a_multi_query_retrieval.ipynb) | [`02b_multiquery_retrieval_walkthrough.ipynb`](optional/02b_multiquery_retrieval_walkthrough.ipynb) *(alternate)*<br>[`02c_better_queries.ipynb`](optional/02c_better_queries.ipynb) *(alternate)* |
| 8.3 | RAG-Fusion with Reciprocal Rank Fusion | [`03a_rag_fusion.ipynb`](notebooks/03a_rag_fusion.ipynb) | — |
| 8.4 | Step-back prompting | [`04a_step_back_prompting.ipynb`](notebooks/04a_step_back_prompting.ipynb) | — |
| 8.5 | HyDE: embed a hypothetical answer | [`05a_hyde.ipynb`](notebooks/05a_hyde.ipynb) | [`05b_hyde_walkthrough.ipynb`](optional/05b_hyde_walkthrough.ipynb) *(alternate)*<br>[`05c_hyde_rag_techniques.ipynb`](optional/05c_hyde_rag_techniques.ipynb) *(alternate)* |
| 8.6 | Query decomposition for multi-hop questions | [`06a_query_decomposition.ipynb`](notebooks/06a_query_decomposition.ipynb) | [`06b_query_decomposition_walkthrough.ipynb`](optional/06b_query_decomposition_walkthrough.ipynb) *(alternate)* |
| 8.7 | Routing: LLM classifier and semantic routing | [`07a_routing_with_llm_classifier.ipynb`](notebooks/07a_routing_with_llm_classifier.ipynb)<br>[`07b_semantic_routing.ipynb`](notebooks/07b_semantic_routing.ipynb) | — |
| 8.8 | Self-querying: natural language to metadata filter | [`08a_self_querying_retrieval.ipynb`](notebooks/08a_self_querying_retrieval.ipynb) | — |

## Hands-on lab

Query-transformation matrix: run multi-query, RAG-Fusion, HyDE and decomposition on the same 30 questions and record which question types each one helps, which it hurts, and the added latency and cost. Details: [lab/README.md](lab/README.md).

## Key concepts

Query–document asymmetry · RRF · HyDE · Logical vs semantic routing

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_query_expansion.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/09_query_expansion.ipynb` |
| `optional/01b_query_transformations_rag_techniques.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/14_query_transformations_rag_techniques.ipynb` |
| `notebooks/02a_multi_query_retrieval.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/01_multi_query_retrieval.ipynb` |
| `optional/02b_multiquery_retrieval_walkthrough.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/12_multiquery_retrieval_walkthrough.ipynb` |
| `optional/02c_better_queries.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/13_better_queries.ipynb` |
| `notebooks/03a_rag_fusion.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/02_rag_fusion.ipynb` |
| `notebooks/04a_step_back_prompting.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/03_step_back_prompting.ipynb` |
| `notebooks/05a_hyde.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/04_hyde.ipynb` |
| `optional/05b_hyde_walkthrough.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/11_hyde_walkthrough.ipynb` |
| `optional/05c_hyde_rag_techniques.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/15_hyde_rag_techniques.ipynb` |
| `notebooks/06a_query_decomposition.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/05_query_decomposition.ipynb` |
| `optional/06b_query_decomposition_walkthrough.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/10_query_decomposition_walkthrough.ipynb` |
| `notebooks/07a_routing_with_llm_classifier.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/06_routing_with_llm_classifier.ipynb` |
| `notebooks/07b_semantic_routing.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/07_semantic_routing.ipynb` |
| `notebooks/08a_self_querying_retrieval.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/08_self_querying_retrieval.ipynb` |
