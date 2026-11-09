# M17 — Query Transformation & Routing

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part V · Retrieval Quality & RAG Applications** · **Level:** Core · **Time:** ~7 h · **Notebooks:** 9 mandatory, 6 optional

## Why it matters

Users write short, vague or compound questions. Rewriting the query before retrieval is often the cheapest large gain available.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Query variants and rank fusion](mandatory/theory/03_rag_fusion_with_reciprocal_rank_fusion/interactive/query-variant-fusion-lab.html) (open the file in a browser)

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
| 17.1 | Query rewriting and expansion ([theory](mandatory/theory/01_query_rewriting_and_expansion/README.md)) | [`01a_query_expansion.ipynb`](mandatory/notebook/01a_query_expansion.ipynb) | [`01b_query_transformations_rag_techniques.ipynb`](optional/notebook/01b_query_transformations_rag_techniques.ipynb) *(alternate)* |
| 17.2 | Multi-query retrieval ([theory](mandatory/theory/02_multi_query_retrieval/README.md)) | [`02a_multi_query_retrieval.ipynb`](mandatory/notebook/02a_multi_query_retrieval.ipynb) | [`02b_multiquery_retrieval_walkthrough.ipynb`](optional/notebook/02b_multiquery_retrieval_walkthrough.ipynb) *(alternate)*<br>[`02c_better_queries.ipynb`](optional/notebook/02c_better_queries.ipynb) *(alternate)* |
| 17.3 | RAG-Fusion with Reciprocal Rank Fusion ([theory](mandatory/theory/03_rag_fusion_with_reciprocal_rank_fusion/README.md)) | [`03a_rag_fusion.ipynb`](mandatory/notebook/03a_rag_fusion.ipynb) | — |
| 17.4 | Step-back prompting ([theory](mandatory/theory/04_step_back_prompting/README.md)) | [`04a_step_back_prompting.ipynb`](mandatory/notebook/04a_step_back_prompting.ipynb) | — |
| 17.5 | HyDE: embed a hypothetical answer ([theory](mandatory/theory/05_hyde_embed_a_hypothetical_answer/README.md)) | [`05a_hyde.ipynb`](mandatory/notebook/05a_hyde.ipynb) | [`05b_hyde_walkthrough.ipynb`](optional/notebook/05b_hyde_walkthrough.ipynb) *(alternate)*<br>[`05c_hyde_rag_techniques.ipynb`](optional/notebook/05c_hyde_rag_techniques.ipynb) *(alternate)* |
| 17.6 | Query decomposition for multi-hop questions ([theory](mandatory/theory/06_query_decomposition_for_multi_hop_questions/README.md)) | [`06a_query_decomposition.ipynb`](mandatory/notebook/06a_query_decomposition.ipynb) | [`06b_query_decomposition_walkthrough.ipynb`](optional/notebook/06b_query_decomposition_walkthrough.ipynb) *(alternate)* |
| 17.7 | Routing: LLM classifier and semantic routing ([theory](mandatory/theory/07_routing_llm_classifier_and_semantic_routing/README.md)) | [`07a_routing_with_llm_classifier.ipynb`](mandatory/notebook/07a_routing_with_llm_classifier.ipynb)<br>[`07b_semantic_routing.ipynb`](mandatory/notebook/07b_semantic_routing.ipynb) | — |
| 17.8 | Self-querying: natural language to metadata filter ([theory](mandatory/theory/08_self_querying_natural_language_to_metadata_filter/README.md)) | [`08a_self_querying_retrieval.ipynb`](mandatory/notebook/08a_self_querying_retrieval.ipynb) | — |

## Hands-on lab

Query-transformation matrix: run multi-query, RAG-Fusion, HyDE and decomposition on the same 30 questions and record which question types each one helps, which it hurts, and the added latency and cost. Details: [lab/README.md](lab/README.md).

## Key concepts

[Query–document asymmetry](mandatory/theory/01_query_rewriting_and_expansion/README.md#querydocument-asymmetry) · [RRF](mandatory/theory/03_rag_fusion_with_reciprocal_rank_fusion/README.md#rrf) · [HyDE](mandatory/theory/05_hyde_embed_a_hypothetical_answer/README.md#hyde) · [Logical vs semantic routing](mandatory/theory/07_routing_llm_classifier_and_semantic_routing/README.md#logical-vs-semantic-routing)

## Folder layout

- `mandatory/notebook/`: the mandatory track, plus the helper files those notebooks import
- `optional/notebook/`: alternate, platform-specific, extension and exercise notebooks
- `mandatory/theory/`: the module page, its `index.html` and the pages of lessons with a mandatory notebook
- `optional/theory/`: the pages of lessons whose notebooks are all optional
- `projects/`: runnable sub-projects (for example MCP servers and clients), where the module has them
- `assets/`: images and data used by this module's notebooks, where it has them
- `lab/`: the module lab brief, its solution notebook in `solution/` and its data in `data/`

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `mandatory/notebook/01a_query_expansion.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/09_query_expansion.ipynb` |
| `optional/notebook/01b_query_transformations_rag_techniques.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/14_query_transformations_rag_techniques.ipynb` |
| `mandatory/notebook/02a_multi_query_retrieval.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/01_multi_query_retrieval.ipynb` |
| `optional/notebook/02b_multiquery_retrieval_walkthrough.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/12_multiquery_retrieval_walkthrough.ipynb` |
| `optional/notebook/02c_better_queries.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/13_better_queries.ipynb` |
| `mandatory/notebook/03a_rag_fusion.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/02_rag_fusion.ipynb` |
| `mandatory/notebook/04a_step_back_prompting.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/03_step_back_prompting.ipynb` |
| `mandatory/notebook/05a_hyde.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/04_hyde.ipynb` |
| `optional/notebook/05b_hyde_walkthrough.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/11_hyde_walkthrough.ipynb` |
| `optional/notebook/05c_hyde_rag_techniques.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/15_hyde_rag_techniques.ipynb` |
| `mandatory/notebook/06a_query_decomposition.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/05_query_decomposition.ipynb` |
| `optional/notebook/06b_query_decomposition_walkthrough.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/10_query_decomposition_walkthrough.ipynb` |
| `mandatory/notebook/07a_routing_with_llm_classifier.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/06_routing_with_llm_classifier.ipynb` |
| `mandatory/notebook/07b_semantic_routing.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/07_semantic_routing.ipynb` |
| `mandatory/notebook/08a_self_querying_retrieval.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/08_query_transformation/notebooks/08_self_querying_retrieval.ipynb` |
