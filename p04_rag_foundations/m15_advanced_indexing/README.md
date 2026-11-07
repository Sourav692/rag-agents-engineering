# M15 — Advanced Indexing Strategies

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part IV · RAG Foundations: Ingestion & Indexing** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 2 optional

## Why it matters

What you embed does not have to be what you return. Decoupling the search key from the payload fixes many precision and context problems.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Search small, return large](mandatory/theory/02_parent_document_retrieval_in_memory_and_on_postgres/interactive/search-small-return-large-lab.html) (open the file in a browser)

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
| 15.1 | Multi-representation indexing: search summaries, return documents ([theory](mandatory/theory/01_multi_representation_indexing_search_summaries_return_documents/README.md)) | [`01a_multi_representation_indexing.ipynb`](mandatory/notebook/01a_multi_representation_indexing.ipynb) | — |
| 15.2 | Parent-document retrieval, in memory and on Postgres ([theory](mandatory/theory/02_parent_document_retrieval_in_memory_and_on_postgres/README.md)) | [`02a_parent_document_retrieval.ipynb`](mandatory/notebook/02a_parent_document_retrieval.ipynb) | [`02b_parent_document_retriever_postgres.ipynb`](optional/notebook/02b_parent_document_retriever_postgres.ipynb) *(platform-specific)* |
| 15.3 | Hierarchical indices: summary tier and detail tier ([theory](mandatory/theory/03_hierarchical_indices_summary_tier_and_detail_tier/README.md)) | [`03a_hierarchical_indices.ipynb`](mandatory/notebook/03a_hierarchical_indices.ipynb) | — |
| 15.4 | Question-side indexing: HyPE and document augmentation ([theory](mandatory/theory/04_question_side_indexing_hype_and_document_augmentation/README.md)) | [`04a_hypothetical_prompt_embeddings.ipynb`](mandatory/notebook/04a_hypothetical_prompt_embeddings.ipynb) | [`04b_document_augmentation.ipynb`](optional/notebook/04b_document_augmentation.ipynb) *(alternate)* |
| 15.5 | Context-aware chunks: contextual headers and contextual retrieval ([theory](mandatory/theory/05_context_aware_chunks_contextual_headers_and_contextual_retrieval/README.md)) | [`05a_contextual_chunk_headers.ipynb`](mandatory/notebook/05a_contextual_chunk_headers.ipynb)<br>[`05b_contextual_retrieval_rag_system.ipynb`](mandatory/notebook/05b_contextual_retrieval_rag_system.ipynb) | — |

## Hands-on lab

Index redesign: apply parent-document retrieval and contextual chunk headers to the baseline and report the change in hit rate and answer quality. Details: [lab/README.md](lab/README.md).

## Key concepts

[Search key vs payload](mandatory/theory/01_multi_representation_indexing_search_summaries_return_documents/README.md#search-key-vs-payload) · [Docstore](mandatory/theory/02_parent_document_retrieval_in_memory_and_on_postgres/README.md#docstore) · [HyPE](mandatory/theory/04_question_side_indexing_hype_and_document_augmentation/README.md#hype) · [Contextual retrieval](mandatory/theory/05_context_aware_chunks_contextual_headers_and_contextual_retrieval/README.md#contextual-retrieval)

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
| `mandatory/notebook/01a_multi_representation_indexing.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/01_multi_representation_indexing.ipynb` |
| `mandatory/notebook/02a_parent_document_retrieval.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/02_parent_document_retrieval.ipynb` |
| `optional/notebook/02b_parent_document_retriever_postgres.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/03_parent_document_retriever_postgres.ipynb` |
| `mandatory/notebook/03a_hierarchical_indices.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/04_hierarchical_indices.ipynb` |
| `mandatory/notebook/04a_hypothetical_prompt_embeddings.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/05_hypothetical_prompt_embeddings.ipynb` |
| `optional/notebook/04b_document_augmentation.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/06_document_augmentation.ipynb` |
| `mandatory/notebook/05a_contextual_chunk_headers.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/06_indexing_strategies/notebooks/07_contextual_chunk_headers.ipynb` |
| `mandatory/notebook/05b_contextual_retrieval_rag_system.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/02_contextual_retrieval_rag_system.ipynb` |
