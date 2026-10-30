# M32 — Reliability, Feedback Loops & Diversity

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part IX · Agentic & Self-Correcting RAG** · **Level:** Advanced · **Time:** ~3 h · **Notebooks:** 2 mandatory, 1 optional

## Why it matters

A RAG system in production must show where an answer came from, detect when it is unsupported, and improve from user feedback.

## Theory

Read the [theory page](../../../theory/p09_agentic_rag/m32_reliability_feedback/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p09_agentic_rag/m32_reliability_feedback/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [The feedback flywheel](../../../theory/p09_agentic_rag/m32_reliability_feedback/02_retrieval_with_a_user_feedback_loop/interactive/feedback-flywheel-lab.html) (open the file in a browser)

## Learning objectives

- Add relevance checks, hallucination checks and source highlighting
- Re-score documents from user feedback and refresh the index periodically
- Balance relevance and diversity with Dartboard RAG

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 32.1 | Reliable RAG: relevance checks, hallucination checks, source highlighting ([theory](../../../theory/p09_agentic_rag/m32_reliability_feedback/01_reliable_rag_relevance_checks_hallucination_checks_source_highlighting/README.md)) | [`01a_reliable_rag.ipynb`](notebooks/01a_reliable_rag.ipynb) | — |
| 32.2 | Retrieval with a user-feedback loop ([theory](../../../theory/p09_agentic_rag/m32_reliability_feedback/02_retrieval_with_a_user_feedback_loop/README.md)) | [`02a_retrieval_with_feedback_loop.ipynb`](notebooks/02a_retrieval_with_feedback_loop.ipynb) | — |
| 32.3 | Dartboard RAG: relevance and diversity together *(optional lesson)* ([theory](../../../theory/p09_agentic_rag/m32_reliability_feedback/03_dartboard_rag_relevance_and_diversity_together/README.md)) | — | [`03a_dartboard_rag.ipynb`](optional/03a_dartboard_rag.ipynb) *(extension)* |

## Hands-on lab

Feedback flywheel: simulate 100 thumbs-up / thumbs-down events and show the effect on ranking for the affected queries. Details: [lab/README.md](lab/README.md).

## Key concepts

[Hallucination detection](../../../theory/p09_agentic_rag/m32_reliability_feedback/01_reliable_rag_relevance_checks_hallucination_checks_source_highlighting/README.md#hallucination-detection) · [Source highlighting](../../../theory/p09_agentic_rag/m32_reliability_feedback/01_reliable_rag_relevance_checks_hallucination_checks_source_highlighting/README.md#source-highlighting) · [Implicit vs explicit feedback](../../../theory/p09_agentic_rag/m32_reliability_feedback/02_retrieval_with_a_user_feedback_loop/README.md#implicit-vs-explicit-feedback) · [Diversity-aware selection](../../../theory/p09_agentic_rag/m32_reliability_feedback/03_dartboard_rag_relevance_and_diversity_together/README.md#diversity-aware-selection)

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
| `notebooks/01a_reliable_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/06_retrieval_feedback_and_reliability/notebooks/01_reliable_rag.ipynb` |
| `notebooks/02a_retrieval_with_feedback_loop.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/06_retrieval_feedback_and_reliability/notebooks/02_retrieval_with_feedback_loop.ipynb` |
| `optional/03a_dartboard_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/06_retrieval_feedback_and_reliability/notebooks/03_dartboard_rag.ipynb` |
