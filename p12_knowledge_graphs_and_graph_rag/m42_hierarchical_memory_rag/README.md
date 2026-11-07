# M42 — Hierarchical & Memory-Augmented Retrieval

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part XII · Knowledge Graphs & GraphRAG** · **Level:** Expert · **Time:** ~4 h · **Notebooks:** 2 mandatory, 1 optional

## Why it matters

Questions like 'what are the main themes of this book?' have no single matching chunk. Trees and memory let retrieval work at several levels of abstraction.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Search the leaves or the whole tree](mandatory/theory/01_raptor_clustering_and_recursive_summarisation/interactive/collapsed-tree-lab.html) (open the file in a browser)

## Learning objectives

- Build a recursive tree of abstractive summaries (RAPTOR) and retrieve across its levels
- Use a global memory model that drafts clues to guide retrieval over long documents (MemoRAG)
- Index entities and relations in a lightweight graph with dual-level retrieval (LightRAG)

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 42.1 | RAPTOR: clustering and recursive summarisation ([theory](mandatory/theory/01_raptor_clustering_and_recursive_summarisation/README.md)) | [`01a_raptor.ipynb`](mandatory/notebook/01a_raptor.ipynb) | — |
| 42.2 | MemoRAG: global memory and clue-guided retrieval *(optional lesson)* ([theory](optional/theory/02_memorag_global_memory_and_clue_guided_retrieval/README.md)) | — | [`02a_memorag.ipynb`](optional/notebook/02a_memorag.ipynb) *(extension)* |
| 42.3 | LightRAG: low-level and high-level graph retrieval ([theory](mandatory/theory/03_lightrag_low_level_and_high_level_graph_retrieval/README.md)) | [`03a_light_rag.ipynb`](mandatory/notebook/03a_light_rag.ipynb) | — |

## Hands-on lab

Global-question test: ask ten 'summarise / compare across the whole corpus' questions and compare flat RAG, RAPTOR and LightRAG. Details: [lab/README.md](lab/README.md).

## Key concepts

[Abstraction levels](mandatory/theory/01_raptor_clustering_and_recursive_summarisation/README.md#abstraction-levels) · [Collapsed-tree retrieval](mandatory/theory/01_raptor_clustering_and_recursive_summarisation/README.md#collapsed-tree-retrieval) · [Global memory](optional/theory/02_memorag_global_memory_and_clue_guided_retrieval/README.md#global-memory) · [Dual-level retrieval](mandatory/theory/03_lightrag_low_level_and_high_level_graph_retrieval/README.md#dual-level-retrieval)

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
| `mandatory/notebook/01a_raptor.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/07_hierarchical_retrieval_raptor/notebooks/01_raptor.ipynb` |
| `optional/notebook/02a_memorag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/08_memory_augmented_and_light_rag/notebooks/01_memorag.ipynb` |
| `mandatory/notebook/03a_light_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/08_memory_augmented_and_light_rag/notebooks/02_light_rag.ipynb` |
