# M42 — Hierarchical & Memory-Augmented Retrieval

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part XII · Hierarchical, Memory & Graph RAG** · **Level:** Expert · **Time:** ~4 h · **Notebooks:** 2 mandatory, 1 optional

## Why it matters

Questions like 'what are the main themes of this book?' have no single matching chunk. Trees and memory let retrieval work at several levels of abstraction.

## Theory

Read the [theory page](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Search the leaves or the whole tree](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/01_raptor_clustering_and_recursive_summarisation/interactive/collapsed-tree-lab.html) (open the file in a browser)

## Learning objectives

- Build a recursive tree of abstractive summaries (RAPTOR) and retrieve across its levels
- Use a global memory model that drafts clues to guide retrieval over long documents (MemoRAG)
- Index entities and relations in a lightweight graph with dual-level retrieval (LightRAG)

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 42.1 | RAPTOR: clustering and recursive summarisation ([theory](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/01_raptor_clustering_and_recursive_summarisation/README.md)) | [`01a_raptor.ipynb`](notebooks/01a_raptor.ipynb) | — |
| 42.2 | MemoRAG: global memory and clue-guided retrieval *(optional lesson)* ([theory](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/02_memorag_global_memory_and_clue_guided_retrieval/README.md)) | — | [`02a_memorag.ipynb`](optional/02a_memorag.ipynb) *(extension)* |
| 42.3 | LightRAG: low-level and high-level graph retrieval ([theory](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/03_lightrag_low_level_and_high_level_graph_retrieval/README.md)) | [`03a_light_rag.ipynb`](notebooks/03a_light_rag.ipynb) | — |

## Hands-on lab

Global-question test: ask ten 'summarise / compare across the whole corpus' questions and compare flat RAG, RAPTOR and LightRAG. Details: [lab/README.md](lab/README.md).

## Key concepts

[Abstraction levels](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/01_raptor_clustering_and_recursive_summarisation/README.md#abstraction-levels) · [Collapsed-tree retrieval](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/01_raptor_clustering_and_recursive_summarisation/README.md#collapsed-tree-retrieval) · [Global memory](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/02_memorag_global_memory_and_clue_guided_retrieval/README.md#global-memory) · [Dual-level retrieval](../../../theory/p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/03_lightrag_low_level_and_high_level_graph_retrieval/README.md#dual-level-retrieval)

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
| `notebooks/01a_raptor.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/07_hierarchical_retrieval_raptor/notebooks/01_raptor.ipynb` |
| `optional/02a_memorag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/08_memory_augmented_and_light_rag/notebooks/01_memorag.ipynb` |
| `notebooks/03a_light_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/08_memory_augmented_and_light_rag/notebooks/02_light_rag.ipynb` |
