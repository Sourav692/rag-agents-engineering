# M15 — Vector Stores & Index Operations

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part V · The Ingestion & Indexing Pipeline** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 4 optional

## Why it matters

A vector store is a database. You need to create, update, delete, persist and filter, and keep it in sync with sources that change.

## Theory

Read the [theory page](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [The record manager and cleanup modes](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/05_incremental_indexing_indexing_api_and_record_manager/interactive/record-manager-lab.html) (open the file in a browser)

## Learning objectives

- Run CRUD and persistence operations through LangChain's common vector store interface
- Use embedded stores (Chroma, FAISS) and managed stores (Astra DB, Pinecone), and know when to pick each
- Combine semantic search with metadata filters on Postgres + pgvector
- Keep an index in sync with its sources using the Indexing API and a record manager

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 15.1 | Index operations: create, query, update, delete, persist ([theory](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/01_index_operations_create_query_update_delete_persist/README.md)) | [`01a_vector_stores_and_index_operations.ipynb`](notebooks/01a_vector_stores_and_index_operations.ipynb) | [`01b_vector_database_operations.ipynb`](optional/01b_vector_database_operations.ipynb) *(alternate)*<br>[`01c_other_vector_stores.ipynb`](optional/01c_other_vector_stores.ipynb) *(extension)* |
| 15.2 | Embedded stores: Chroma and FAISS ([theory](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/02_embedded_stores_chroma_and_faiss/README.md)) | [`02a_chromadb.ipynb`](notebooks/02a_chromadb.ipynb)<br>[`02b_faiss.ipynb`](notebooks/02b_faiss.ipynb) | [`02c_vector_stores_in_practice.ipynb`](optional/02c_vector_stores_in_practice.ipynb) *(alternate)* |
| 15.3 | Managed stores: Astra DB and Pinecone ([theory](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/03_managed_stores_astra_db_and_pinecone/README.md)) | [`03b_pinecone.ipynb`](notebooks/03b_pinecone.ipynb) | [`03a_astra_db.ipynb`](optional/03a_astra_db.ipynb) *(platform-specific)* |
| 15.4 | Postgres + pgvector with metadata-filtered search ([theory](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/04_postgres_pgvector_with_metadata_filtered_search/README.md)) | [`04a_filtered_search_pgvector.ipynb`](notebooks/04a_filtered_search_pgvector.ipynb) | — |
| 15.5 | Incremental indexing: Indexing API and record manager ([theory](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/05_incremental_indexing_indexing_api_and_record_manager/README.md)) | [`05a_indexing_api.ipynb`](notebooks/05a_indexing_api.ipynb) | — |

## Hands-on lab

Living index: stand up pgvector with Docker, ingest the M12 corpus, then change, add and delete source files and show that the record manager re-indexes only what changed. Details: [lab/README.md](lab/README.md).

## Key concepts

[ANN search](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/02_embedded_stores_chroma_and_faiss/README.md#ann-search) · [Collections and namespaces](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/03_managed_stores_astra_db_and_pinecone/README.md#collections-and-namespaces) · [Metadata filters](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/04_postgres_pgvector_with_metadata_filtered_search/README.md#metadata-filters) · [Idempotent re-indexing](../../../theory/p05_ingestion_and_indexing/m15_vector_stores/05_incremental_indexing_indexing_api_and_record_manager/README.md#idempotent-re-indexing)

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
| `notebooks/01a_vector_stores_and_index_operations.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/05_vector_stores/notebooks/01_vector_stores_and_index_operations.ipynb` |
| `optional/01b_vector_database_operations.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/05_vector_stores/notebooks/02_vector_database_operations.ipynb` |
| `optional/01c_other_vector_stores.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/05_vector_stores/notebooks/05_other_vector_stores.ipynb` |
| `notebooks/02a_chromadb.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/05_vector_stores/notebooks/03_chromadb.ipynb` |
| `notebooks/02b_faiss.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/05_vector_stores/notebooks/04_faiss.ipynb` |
| `optional/02c_vector_stores_in_practice.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/05_vector_stores/notebooks/08_vector_stores_in_practice.ipynb` |
| `optional/03a_astra_db.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/05_vector_stores/notebooks/06_astra_db.ipynb` |
| `notebooks/03b_pinecone.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/05_vector_stores/notebooks/07_pinecone.ipynb` |
| `notebooks/04a_filtered_search_pgvector.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/12_langchain_rag_implementations/notebooks/01_filtered_search_pgvector.ipynb` |
| `notebooks/05a_indexing_api.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/12_langchain_rag_implementations/notebooks/02_indexing_api.ipynb` |
