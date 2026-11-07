# Lab: M17 Query Transformation & Routing

## Brief

Query-transformation matrix: run multi-query, RAG-Fusion, HyDE and decomposition on the same 30 questions and record which question types each one helps, which it hurts, and the added latency and cost.

## Approach

- Questions and documents differ in vocabulary ("server goes down" against "outage" and "availability") and in shape (a short question against a long passage). Each technique closes one of those gaps, or splits a question that has more than one need.
- Multi-query and RAG-Fusion search with several LLM-written phrasings; RAG-Fusion fuses the lists with RRF, where the constant `k` (60 here) is a real setting.
- HyDE embeds an LLM-written answer instead of the question. It costs one LLM call per query and can mislead on a private corpus the model knows nothing about. Decomposition costs a call to split the question plus one retrieval per sub-question.
- Every method is capped at 4 chunks so the comparison is about which chunks, not how many. Cost is reported as LLM calls and tokens per question; set `PRICE_IN_PER_1M` and `PRICE_OUT_PER_1M` in the notebook from the provider's price page to get dollars.

## How to run

The worked solution is [solution/m17_solution.ipynb](solution/m17_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`.

Keys, as environment variables in the `.env` file at the repo root: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`). The notebook's prices are `None` until you fill them in from the provider's price page on the run date.

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date, models and price date | *pending run* |
| Hit rate and recall per method (25 questions) | *pending run* |
| Change in recall per question type against the baseline | *pending run* |
| Added seconds per question | *pending run* |
| LLM calls and tokens per question | *pending run* |
| Cost per question (if prices are set) | *pending run* |

Back to the module: [README.md](../README.md)
