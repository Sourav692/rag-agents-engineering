# M22 — Framework Fluency: LlamaIndex

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VII · Building Complete RAG Applications** · **Level:** Core · **Time:** ~3 h · **Notebooks:** 4 mandatory, 1 optional

## Why it matters

The techniques are framework-independent. Rebuilding them in LlamaIndex proves you understand the idea and not only one API.

## Learning objectives

- Map LangChain concepts to LlamaIndex (Document/Node, Retriever, QueryEngine, NodePostprocessor)
- Build simple PDF and CSV RAG in LlamaIndex
- Use QueryFusionRetriever, LLM and cross-encoder postprocessors, and sentence-window retrieval

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 22.1 | Simple PDF and CSV RAG in LlamaIndex | [`01a_simple_rag_with_llamaindex.ipynb`](notebooks/01a_simple_rag_with_llamaindex.ipynb) | [`01b_simple_csv_rag_with_llamaindex.ipynb`](optional/01b_simple_csv_rag_with_llamaindex.ipynb) *(extension)* |
| 22.2 | Fusion retrieval with QueryFusionRetriever | [`02a_fusion_retrieval_with_llamaindex.ipynb`](notebooks/02a_fusion_retrieval_with_llamaindex.ipynb) | — |
| 22.3 | Reranking with node postprocessors | [`03a_reranking_with_llamaindex.ipynb`](notebooks/03a_reranking_with_llamaindex.ipynb) | — |
| 22.4 | Sentence-window retrieval | [`04a_context_enrichment_window_with_llamaindex.ipynb`](notebooks/04a_context_enrichment_window_with_llamaindex.ipynb) | — |

## Hands-on lab

Port one of your Part VI pipelines (hybrid + rerank) to LlamaIndex and confirm the metrics match. Details: [lab/README.md](lab/README.md).

## Key concepts

Nodes · QueryEngine · Postprocessors · Sentence window

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
| `notebooks/01a_simple_rag_with_llamaindex.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/13_llamaindex_rag/notebooks/01_simple_rag_with_llamaindex.ipynb` |
| `optional/01b_simple_csv_rag_with_llamaindex.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/13_llamaindex_rag/notebooks/02_simple_csv_rag_with_llamaindex.ipynb` |
| `notebooks/02a_fusion_retrieval_with_llamaindex.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/13_llamaindex_rag/notebooks/03_fusion_retrieval_with_llamaindex.ipynb` |
| `notebooks/03a_reranking_with_llamaindex.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/13_llamaindex_rag/notebooks/04_reranking_with_llamaindex.ipynb` |
| `notebooks/04a_context_enrichment_window_with_llamaindex.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/13_llamaindex_rag/notebooks/05_context_enrichment_window_with_llamaindex.ipynb` |
