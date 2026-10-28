# M42 — Hierarchical & Memory-Augmented Retrieval

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part XII · Hierarchical, Memory & Graph RAG** · **Level:** Expert · **Time:** ~4 h · **Notebooks:** 2 mandatory, 1 optional

## Why it matters

Questions like 'what are the main themes of this book?' have no single matching chunk. Trees and memory let retrieval work at several levels of abstraction.

## Learning objectives

- Build a recursive tree of abstractive summaries (RAPTOR) and retrieve across its levels
- Use a global memory model that drafts clues to guide retrieval over long documents (MemoRAG)
- Index entities and relations in a lightweight graph with dual-level retrieval (LightRAG)

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 42.1 | RAPTOR: clustering and recursive summarisation | [`01a_raptor.ipynb`](notebooks/01a_raptor.ipynb) | — |
| 42.2 | MemoRAG: global memory and clue-guided retrieval *(optional lesson)* | — | [`02a_memorag.ipynb`](optional/02a_memorag.ipynb) *(extension)* |
| 42.3 | LightRAG: low-level and high-level graph retrieval | [`03a_light_rag.ipynb`](notebooks/03a_light_rag.ipynb) | — |

## Hands-on lab

Global-question test: ask ten 'summarise / compare across the whole corpus' questions and compare flat RAG, RAPTOR and LightRAG. Details: [lab/README.md](lab/README.md).

## Key concepts

Abstraction levels · Collapsed-tree retrieval · Global memory · Dual-level retrieval

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
