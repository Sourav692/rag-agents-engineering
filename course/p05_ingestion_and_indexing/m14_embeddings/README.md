# M14 — Embeddings & Model Selection

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part V · The Ingestion & Indexing Pipeline** · **Level:** Core · **Time:** ~4 h · **Notebooks:** 4 mandatory, 4 optional

## Why it matters

The embedding model defines what 'similar' means for your corpus. Choosing one is a measurable decision that trades quality, cost, latency and data residency.

## Learning objectives

- Explain dense embeddings, dimensions and cosine / dot-product / Euclidean similarity
- Generate embeddings with OpenAI and open-source Hugging Face / sentence-transformers models
- Batch and cache embeddings with `CacheBackedEmbeddings` to cut cost and re-index time
- Benchmark candidate models on your own data and track runs with MLflow

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 14.1 | Embedding fundamentals, similarity metrics and model selection | [`01a_embeddings_and_model_selection.ipynb`](notebooks/01a_embeddings_and_model_selection.ipynb) | — |
| 14.2 | Hosted embeddings: OpenAI models and dimensions | [`02a_openai_embeddings.ipynb`](notebooks/02a_openai_embeddings.ipynb) | [`02b_openai_embeddings_tutorial.ipynb`](optional/02b_openai_embeddings_tutorial.ipynb) *(alternate)* |
| 14.3 | Open-source embeddings with Hugging Face | [`03a_huggingface_embeddings.ipynb`](notebooks/03a_huggingface_embeddings.ipynb) | [`03b_huggingface_embeddings_tutorial.ipynb`](optional/03b_huggingface_embeddings_tutorial.ipynb) *(alternate)*<br>[`03c_embedding_models.ipynb`](optional/03c_embedding_models.ipynb) *(alternate)* |
| 14.4 | Production concerns: batching, caching and similarity behaviour | [`04a_embeddings_deep_dive.ipynb`](notebooks/04a_embeddings_deep_dive.ipynb) | — |
| 14.5 | Benchmarking embedding models with MLflow (Databricks) *(optional lesson)* | — | [`05a_compare_embedding_models_databricks.ipynb`](optional/05a_compare_embedding_models_databricks.ipynb) *(platform-specific)* |

## Hands-on lab

Embedding shoot-out: compare one hosted and two open-source models on a 30-question golden set and pick one, writing down the cost and latency per 1,000 chunks. Details: [lab/README.md](lab/README.md).

## Key concepts

Vector dimensionality · Cosine similarity · Embedding cache · Domain fit

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
| `notebooks/01a_embeddings_and_model_selection.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/01_embeddings_and_model_selection.ipynb` |
| `notebooks/02a_openai_embeddings.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/05_openai_embeddings.ipynb` |
| `optional/02b_openai_embeddings_tutorial.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/06_openai_embeddings_tutorial.ipynb` |
| `notebooks/03a_huggingface_embeddings.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/03_huggingface_embeddings.ipynb` |
| `optional/03b_huggingface_embeddings_tutorial.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/04_huggingface_embeddings_tutorial.ipynb` |
| `optional/03c_embedding_models.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/02_embedding_models.ipynb` |
| `notebooks/04a_embeddings_deep_dive.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/07_embeddings_deep_dive.ipynb` |
| `optional/05a_compare_embedding_models_databricks.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/08_compare_embedding_models_databricks.ipynb` |
