# M22 — Reliability, Feedback Loops & Diversity

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VI · Agentic & Self-Correcting RAG** · **Level:** Advanced · **Time:** ~3 h · **Notebooks:** 2 mandatory, 1 optional

## Why it matters

A RAG system in production must show where an answer came from, detect when it is unsupported, and improve from user feedback.

## Learning objectives

- Add relevance checks, hallucination checks and source highlighting
- Re-score documents from user feedback and refresh the index periodically
- Balance relevance and diversity with Dartboard RAG

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 22.1 | Reliable RAG: relevance checks, hallucination checks, source highlighting | [`01a_reliable_rag.ipynb`](notebooks/01a_reliable_rag.ipynb) | — |
| 22.2 | Retrieval with a user-feedback loop | [`02a_retrieval_with_feedback_loop.ipynb`](notebooks/02a_retrieval_with_feedback_loop.ipynb) | — |
| 22.3 | Dartboard RAG: relevance and diversity together *(optional lesson)* | — | [`03a_dartboard_rag.ipynb`](optional/03a_dartboard_rag.ipynb) *(extension)* |

## Hands-on lab

Feedback flywheel: simulate 100 thumbs-up / thumbs-down events and show the effect on ranking for the affected queries. Details: [lab/README.md](lab/README.md).

## Key concepts

Hallucination detection · Source highlighting · Implicit vs explicit feedback · Diversity-aware selection

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_reliable_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/06_retrieval_feedback_and_reliability/notebooks/01_reliable_rag.ipynb` |
| `notebooks/02a_retrieval_with_feedback_loop.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/06_retrieval_feedback_and_reliability/notebooks/02_retrieval_with_feedback_loop.ipynb` |
| `optional/03a_dartboard_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/06_retrieval_feedback_and_reliability/notebooks/03_dartboard_rag.ipynb` |
