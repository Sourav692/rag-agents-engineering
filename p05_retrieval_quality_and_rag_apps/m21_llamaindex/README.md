# M21 — Framework Fluency: LlamaIndex

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part VII · Building Complete RAG Applications** · **Level:** Core · **Time:** ~3 h · **Notebooks:** 4 mandatory, 1 optional

## Why it matters

The techniques are framework-independent. Rebuilding them in LlamaIndex proves you understand the idea and not only one API.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Sentence window lab](mandatory/theory/04_sentence_window_retrieval/interactive/sentence-window-lab.html) (open the file in a browser)

## Learning objectives

- Map LangChain concepts to LlamaIndex (Document/Node, Retriever, QueryEngine, NodePostprocessor)
- Build simple PDF and CSV RAG in LlamaIndex
- Use QueryFusionRetriever, LLM and cross-encoder postprocessors, and sentence-window retrieval

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 21.1 | Simple PDF and CSV RAG in LlamaIndex ([theory](mandatory/theory/01_simple_pdf_and_csv_rag_in_llamaindex/README.md)) | [`01a_simple_rag_with_llamaindex.ipynb`](mandatory/notebook/01a_simple_rag_with_llamaindex.ipynb) | [`01b_simple_csv_rag_with_llamaindex.ipynb`](optional/notebook/01b_simple_csv_rag_with_llamaindex.ipynb) *(extension)* |
| 21.2 | Fusion retrieval with QueryFusionRetriever ([theory](mandatory/theory/02_fusion_retrieval_with_queryfusionretriever/README.md)) | [`02a_fusion_retrieval_with_llamaindex.ipynb`](mandatory/notebook/02a_fusion_retrieval_with_llamaindex.ipynb) | — |
| 21.3 | Reranking with node postprocessors ([theory](mandatory/theory/03_reranking_with_node_postprocessors/README.md)) | [`03a_reranking_with_llamaindex.ipynb`](mandatory/notebook/03a_reranking_with_llamaindex.ipynb) | — |
| 21.4 | Sentence-window retrieval ([theory](mandatory/theory/04_sentence_window_retrieval/README.md)) | [`04a_context_enrichment_window_with_llamaindex.ipynb`](mandatory/notebook/04a_context_enrichment_window_with_llamaindex.ipynb) | — |

## Hands-on lab

Port one of your Part VI pipelines (hybrid + rerank) to LlamaIndex and confirm the metrics match. Details: [lab/README.md](lab/README.md).

## Key concepts

[Nodes](mandatory/theory/01_simple_pdf_and_csv_rag_in_llamaindex/README.md#nodes) · [QueryEngine](mandatory/theory/01_simple_pdf_and_csv_rag_in_llamaindex/README.md#queryengine) · [Postprocessors](mandatory/theory/03_reranking_with_node_postprocessors/README.md#postprocessors) · [Sentence window](mandatory/theory/04_sentence_window_retrieval/README.md#sentence-window)

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
