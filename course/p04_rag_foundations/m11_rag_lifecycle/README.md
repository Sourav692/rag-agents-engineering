# M11 — Why RAG & the RAG Lifecycle

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part IV · RAG Foundations** · **Level:** Foundation · **Time:** ~4 h · **Notebooks:** 4 mandatory, 0 optional

## Why it matters

Before tuning anything you need a working pipeline and a number to beat. This module builds both, first by hand and then with LangChain.

## Theory

Read the [theory page](../../../theory/p04_rag_foundations/m11_rag_lifecycle/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p04_rag_foundations/m11_rag_lifecycle/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Top-k and the baseline](../../../theory/p04_rag_foundations/m11_rag_lifecycle/02_indexing_from_scratch_with_tf_idf_and_nearest_neighbours/interactive/top-k-retrieval-lab.html) (open the file in a browser)

## Learning objectives

- Explain the knowledge problem RAG solves: stale training data, private data, hallucination, and context-window limits
- Compare RAG with fine-tuning and with simply using a long context window
- Build an index from scratch so 'indexing' and 'nearest neighbour' are concrete
- Run the full lifecycle (load → split → embed → store → retrieve → generate) and record baseline metrics

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 11.1 | The knowledge problem: hallucination, freshness, context-window growth, RAG vs fine-tuning vs long context ([theory](../../../theory/p04_rag_foundations/m11_rag_lifecycle/01_the_knowledge_problem_hallucination_freshness_context_window_growth_rag_vs_fine_tuning_vs_long_context/README.md)) | *Lecture / discussion* | — |
| 11.2 | Indexing from scratch with TF-IDF and nearest neighbours ([theory](../../../theory/p04_rag_foundations/m11_rag_lifecycle/02_indexing_from_scratch_with_tf_idf_and_nearest_neighbours/README.md)) | [`02a_indexing_from_scratch.ipynb`](notebooks/02a_indexing_from_scratch.ipynb) | — |
| 11.3 | Semantic retrieval with embedding similarity ([theory](../../../theory/p04_rag_foundations/m11_rag_lifecycle/03_semantic_retrieval_with_embedding_similarity/README.md)) | [`03a_retrieval_strategies.ipynb`](notebooks/03a_retrieval_strategies.ipynb) | — |
| 11.4 | Your first LangChain RAG with Chroma ([theory](../../../theory/p04_rag_foundations/m11_rag_lifecycle/04_your_first_langchain_rag_with_chroma/README.md)) | [`04a_langchain_rag_quickstart.ipynb`](notebooks/04a_langchain_rag_quickstart.ipynb) | — |
| 11.5 | The RAG lifecycle and a measured baseline ([theory](../../../theory/p04_rag_foundations/m11_rag_lifecycle/05_the_rag_lifecycle_and_a_measured_baseline/README.md)) | [`05a_rag_lifecycle_and_baseline.ipynb`](notebooks/05a_rag_lifecycle_and_baseline.ipynb) | — |

## Hands-on lab

Baseline pipeline: build the canonical lifecycle notebook end to end on the course corpus and save its retrieval and answer metrics. Every later module reports its improvement against this baseline. Details: [lab/README.md](lab/README.md).

## Key concepts

[Parametric vs non-parametric knowledge](../../../theory/p04_rag_foundations/m11_rag_lifecycle/01_the_knowledge_problem_hallucination_freshness_context_window_growth_rag_vs_fine_tuning_vs_long_context/README.md#parametric-vs-non-parametric-knowledge) · [Indexing vs retrieval vs generation](../../../theory/p04_rag_foundations/m11_rag_lifecycle/05_the_rag_lifecycle_and_a_measured_baseline/README.md#indexing-vs-retrieval-vs-generation) · [Top-k](../../../theory/p04_rag_foundations/m11_rag_lifecycle/02_indexing_from_scratch_with_tf_idf_and_nearest_neighbours/README.md#top-k) · [Baseline-first optimisation](../../../theory/p04_rag_foundations/m11_rag_lifecycle/05_the_rag_lifecycle_and_a_measured_baseline/README.md#baseline-first-optimisation)

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
| `notebooks/02a_indexing_from_scratch.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/01_introduction_to_rag/notebooks/01_indexing_from_scratch.ipynb` |
| `notebooks/03a_retrieval_strategies.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/01_introduction_to_rag/notebooks/02_retrieval_strategies.ipynb` |
| `notebooks/04a_langchain_rag_quickstart.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/01_introduction_to_rag/notebooks/03_langchain_rag_quickstart.ipynb` |
| `notebooks/05a_rag_lifecycle_and_baseline.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/01_introduction_to_rag/notebooks/04_rag_lifecycle_and_baseline.ipynb` |
