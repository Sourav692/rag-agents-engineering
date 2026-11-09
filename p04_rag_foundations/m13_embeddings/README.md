# M13 — Embeddings & Model Selection

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part IV · RAG Foundations: Ingestion & Indexing** · **Level:** Core · **Time:** ~4 h · **Notebooks:** 4 mandatory, 4 optional

## Why it matters

The embedding model defines what 'similar' means for your corpus. Choosing one is a measurable decision that trades quality, cost, latency and data residency.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Cosine, dot and Euclidean](mandatory/theory/01_embedding_fundamentals_similarity_metrics_and_model_selection/interactive/similarity-metrics-lab.html) (open the file in a browser)

## Learning objectives

- Explain dense embeddings, dimensions and cosine / dot-product / Euclidean similarity
- Generate embeddings with OpenAI and open-source Hugging Face / sentence-transformers models
- Batch and cache embeddings with `CacheBackedEmbeddings` to cut cost and re-index time
- Benchmark candidate models on your own data and track runs with MLflow

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 13.1 | Embedding fundamentals, similarity metrics and model selection ([theory](mandatory/theory/01_embedding_fundamentals_similarity_metrics_and_model_selection/README.md)) | [`01a_embeddings_and_model_selection.ipynb`](mandatory/notebook/01a_embeddings_and_model_selection.ipynb) | — |
| 13.2 | Hosted embeddings: OpenAI models and dimensions ([theory](mandatory/theory/02_hosted_embeddings_openai_models_and_dimensions/README.md)) | [`02a_openai_embeddings.ipynb`](mandatory/notebook/02a_openai_embeddings.ipynb) | [`02b_openai_embeddings_tutorial.ipynb`](optional/notebook/02b_openai_embeddings_tutorial.ipynb) *(alternate)* |
| 13.3 | Open-source embeddings with Hugging Face ([theory](mandatory/theory/03_open_source_embeddings_with_hugging_face/README.md)) | [`03a_huggingface_embeddings.ipynb`](mandatory/notebook/03a_huggingface_embeddings.ipynb) | [`03b_huggingface_embeddings_tutorial.ipynb`](optional/notebook/03b_huggingface_embeddings_tutorial.ipynb) *(alternate)*<br>[`03c_embedding_models.ipynb`](optional/notebook/03c_embedding_models.ipynb) *(alternate)* |
| 13.4 | Production concerns: batching, caching and similarity behaviour ([theory](mandatory/theory/04_production_concerns_batching_caching_and_similarity_behaviour/README.md)) | [`04a_embeddings_deep_dive.ipynb`](mandatory/notebook/04a_embeddings_deep_dive.ipynb) | — |
| 13.5 | Benchmarking embedding models with MLflow (Databricks) *(optional lesson)* ([theory](optional/theory/05_benchmarking_embedding_models_with_mlflow_databricks/README.md)) | — | [`05a_compare_embedding_models_databricks.ipynb`](optional/notebook/05a_compare_embedding_models_databricks.ipynb) *(platform-specific)* |

## Hands-on lab

Embedding shoot-out: compare one hosted and two open-source models on a 30-question golden set and pick one, writing down the cost and latency per 1,000 chunks. Details: [lab/README.md](lab/README.md).

## Key concepts

[Vector dimensionality](mandatory/theory/02_hosted_embeddings_openai_models_and_dimensions/README.md#vector-dimensionality) · [Cosine similarity](mandatory/theory/01_embedding_fundamentals_similarity_metrics_and_model_selection/README.md#cosine-similarity) · [Embedding cache](mandatory/theory/04_production_concerns_batching_caching_and_similarity_behaviour/README.md#embedding-cache) · [Domain fit](mandatory/theory/03_open_source_embeddings_with_hugging_face/README.md#domain-fit)

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
| `mandatory/notebook/01a_embeddings_and_model_selection.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/01_embeddings_and_model_selection.ipynb` |
| `mandatory/notebook/02a_openai_embeddings.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/05_openai_embeddings.ipynb` |
| `optional/notebook/02b_openai_embeddings_tutorial.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/06_openai_embeddings_tutorial.ipynb` |
| `mandatory/notebook/03a_huggingface_embeddings.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/03_huggingface_embeddings.ipynb` |
| `optional/notebook/03b_huggingface_embeddings_tutorial.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/04_huggingface_embeddings_tutorial.ipynb` |
| `optional/notebook/03c_embedding_models.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/02_embedding_models.ipynb` |
| `mandatory/notebook/04a_embeddings_deep_dive.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/07_embeddings_deep_dive.ipynb` |
| `optional/notebook/05a_compare_embedding_models_databricks.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/04_embeddings/notebooks/08_compare_embedding_models_databricks.ipynb` |
