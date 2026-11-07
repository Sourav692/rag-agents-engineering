# Lab: M18 Post-Retrieval Optimisation & Reranking

## Brief

Precision stack: add a cross-encoder reranker over a top-50 hybrid retrieval and measure the gain at top-5, plus the latency budget it consumes.

## Approach

- Retrieval runs in two stages. The hybrid retriever (BM25 with the dense retriever, as in M16) scores every chunk and returns a wide candidate list; a cross-encoder reads each question and candidate together and reorders it. Stage 1 is judged on recall at depth 50, stage 2 on precision in the top 5.
- The reranker only reorders what stage 1 returned, so recall at 50 caps everything after it. The solution prints both.
- Reranking cost grows with the number of candidates: a cross-encoder runs one forward pass per question and chunk pair. Latency is measured on the machine that runs the notebook, so record it with the run.
- The 500-character split gives the handbook about 30 chunks, fewer than 50; the solution splits at 200 characters so the top-50 stage is meaningful. Its numbers are not comparable cell by cell with the 500-character baseline.

## How to run

The worked solution is [solution/m18_solution.ipynb](solution/m18_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the `hf` group: `uv run --group hf jupyter lab`. The first run downloads the cross-encoder from the Hugging Face Hub.

Keys, as environment variables in the `.env` file at the repo root: `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`). The notebook also creates the chat model (`EXPERIENTIALLABS_API_KEY`), though this lab makes no chat call.

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date, embedding model and machine | *pending run* |
| Hit rate and MRR at top 5 without reranking | *pending run* |
| Hit rate and MRR at top 5 with reranking | *pending run* |
| Recall at depth 50 (the ceiling) | *pending run* |
| Rerank latency per query: mean, p50, p95 | *pending run* |

Back to the module: [README.md](../README.md)
