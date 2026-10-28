# M09 — Post-Retrieval Optimisation & Reranking

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part III · Retrieval Quality Engineering** · **Level:** Core · **Time:** ~4 h · **Notebooks:** 5 mandatory, 2 optional

## Why it matters

Bi-encoders are fast but coarse. Retrieving wide and then reranking, compressing or expanding the context gives precision without losing recall.

## Learning objectives

- Design two-stage retrieval: high-recall first stage, precise second stage
- Rerank with cross-encoders and with LLMs and compare cost and quality
- Compress chunks to only the query-relevant sentences
- Restore surrounding context with enrichment windows and relevant segment extraction

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 9.1 | Two-stage retrieval: retrieve wide, rerank narrow | [`01a_two_stage_reranking.ipynb`](notebooks/01a_two_stage_reranking.ipynb) | — |
| 9.2 | Cross-encoder reranking in a RAG chain | [`02a_cross_encoder_reranking.ipynb`](notebooks/02a_cross_encoder_reranking.ipynb) | [`02b_reranking_cross_encoder_walkthrough.ipynb`](optional/02b_reranking_cross_encoder_walkthrough.ipynb) *(alternate)* |
| 9.3 | LLM reranking vs cross-encoder reranking | [`03a_reranking_methods.ipynb`](notebooks/03a_reranking_methods.ipynb) | — |
| 9.4 | Contextual compression | [`04a_contextual_compression.ipynb`](notebooks/04a_contextual_compression.ipynb) | — |
| 9.5 | Context enrichment windows | [`05a_context_enrichment_window.ipynb`](notebooks/05a_context_enrichment_window.ipynb) | — |
| 9.6 | Relevant segment extraction *(optional lesson)* | — | [`06a_relevant_segment_extraction.ipynb`](optional/06a_relevant_segment_extraction.ipynb) *(extension)* |

## Hands-on lab

Precision stack: add a cross-encoder reranker over a top-50 hybrid retrieval and measure the gain at top-5, plus the latency budget it consumes. Details: [lab/README.md](lab/README.md).

## Key concepts

Bi-encoder vs cross-encoder · Recall@50 → precision@5 · Lost in the middle · Context budget

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_two_stage_reranking.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/09_post_retrieval_and_reranking/notebooks/02_two_stage_reranking.ipynb` |
| `notebooks/02a_cross_encoder_reranking.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/09_post_retrieval_and_reranking/notebooks/01_cross_encoder_reranking.ipynb` |
| `optional/02b_reranking_cross_encoder_walkthrough.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/09_post_retrieval_and_reranking/notebooks/03_reranking_cross_encoder_walkthrough.ipynb` |
| `notebooks/03a_reranking_methods.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/09_post_retrieval_and_reranking/notebooks/04_reranking_methods.ipynb` |
| `notebooks/04a_contextual_compression.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/09_post_retrieval_and_reranking/notebooks/05_contextual_compression.ipynb` |
| `notebooks/05a_context_enrichment_window.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/09_post_retrieval_and_reranking/notebooks/06_context_enrichment_window.ipynb` |
| `optional/06a_relevant_segment_extraction.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/09_post_retrieval_and_reranking/notebooks/07_relevant_segment_extraction.ipynb` |
