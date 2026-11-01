# M16 — Advanced Indexing Strategies

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part V · The Ingestion & Indexing Pipeline** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 2 optional

## Why it matters

What you embed does not have to be what you return. Decoupling the search key from the payload fixes many precision and context problems.

## Theory

Read the [theory page](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Search small, return large](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/02_parent_document_retrieval_in_memory_and_on_postgres/interactive/search-small-return-large-lab.html) (open the file in a browser)

## Learning objectives

- Embed summaries but return full documents (multi-representation / multi-vector indexing)
- Embed small child chunks but return their parent (parent-document retrieval), with a persistent docstore
- Build two-tier hierarchical indices and search top-down
- Generate hypothetical questions at index time (HyPE, document augmentation)
- Prepend document context to chunks before embedding (contextual chunk headers, contextual retrieval)

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 16.1 | Multi-representation indexing: search summaries, return documents ([theory](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/01_multi_representation_indexing_search_summaries_return_documents/README.md)) | [`01a_multi_representation_indexing.ipynb`](notebooks/01a_multi_representation_indexing.ipynb) | — |
| 16.2 | Parent-document retrieval, in memory and on Postgres ([theory](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/02_parent_document_retrieval_in_memory_and_on_postgres/README.md)) | [`02a_parent_document_retrieval.ipynb`](notebooks/02a_parent_document_retrieval.ipynb) | [`02b_parent_document_retriever_postgres.ipynb`](optional/02b_parent_document_retriever_postgres.ipynb) *(platform-specific)* |
| 16.3 | Hierarchical indices: summary tier and detail tier ([theory](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/03_hierarchical_indices_summary_tier_and_detail_tier/README.md)) | [`03a_hierarchical_indices.ipynb`](notebooks/03a_hierarchical_indices.ipynb) | — |
| 16.4 | Question-side indexing: HyPE and document augmentation ([theory](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/04_question_side_indexing_hype_and_document_augmentation/README.md)) | [`04a_hypothetical_prompt_embeddings.ipynb`](notebooks/04a_hypothetical_prompt_embeddings.ipynb) | [`04b_document_augmentation.ipynb`](optional/04b_document_augmentation.ipynb) *(alternate)* |
| 16.5 | Context-aware chunks: contextual headers and contextual retrieval ([theory](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/05_context_aware_chunks_contextual_headers_and_contextual_retrieval/README.md)) | [`05a_contextual_chunk_headers.ipynb`](notebooks/05a_contextual_chunk_headers.ipynb)<br>[`05b_contextual_retrieval_rag_system.ipynb`](notebooks/05b_contextual_retrieval_rag_system.ipynb) | — |

## Hands-on lab

Index redesign: apply parent-document retrieval and contextual chunk headers to the baseline and report the change in hit rate and answer quality. Details: [lab/README.md](lab/README.md).

## Key concepts

[Search key vs payload](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/01_multi_representation_indexing_search_summaries_return_documents/README.md#search-key-vs-payload) · [Docstore](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/02_parent_document_retrieval_in_memory_and_on_postgres/README.md#docstore) · [HyPE](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/04_question_side_indexing_hype_and_document_augmentation/README.md#hype) · [Contextual retrieval](../../../theory/p05_ingestion_and_indexing/m16_advanced_indexing/05_context_aware_chunks_contextual_headers_and_contextual_retrieval/README.md#contextual-retrieval)

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
| `notebooks/01a_multi_representation_indexing.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/01_multi_representation_indexing.ipynb` |
| `notebooks/02a_parent_document_retrieval.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/02_parent_document_retrieval.ipynb` |
| `optional/02b_parent_document_retriever_postgres.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/03_parent_document_retriever_postgres.ipynb` |
| `notebooks/03a_hierarchical_indices.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/04_hierarchical_indices.ipynb` |
| `notebooks/04a_hypothetical_prompt_embeddings.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/05_hypothetical_prompt_embeddings.ipynb` |
| `optional/04b_document_augmentation.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/06_document_augmentation.ipynb` |
| `notebooks/05a_contextual_chunk_headers.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/07_contextual_chunk_headers.ipynb` |
| `notebooks/05b_contextual_retrieval_rag_system.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/02_contextual_retrieval_rag_system.ipynb` |
