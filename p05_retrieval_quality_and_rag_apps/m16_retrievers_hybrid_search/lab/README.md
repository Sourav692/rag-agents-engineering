# Lab: M16 Retrievers & Hybrid Search

## Brief

Hybrid upgrade: add BM25 to the vector retriever, tune the fusion weights on the golden set, and find three queries that only hybrid search answers.

## Approach

- Dense retrieval compares embedding vectors and matches paraphrase; sparse retrieval (BM25) scores shared tokens and matches exact terms. Each misses what the other finds, so production retrieval usually runs both.
- `EnsembleRetriever` fuses ranked lists with Reciprocal Rank Fusion, adding `weight / (60 + rank)` per list. RRF uses ranks, not scores, so the two retrievers' score scales do not matter; the weight sets how much each list counts.
- LangChain's `BM25Retriever` splits on whitespace only, so `application.` and `application` are different tokens. Keep that in mind when a question with an exact term still misses.
- The weight is tuned on the same 25 golden questions it is reported on, so the best weight is optimistic; treat it as a starting value for new questions.
- If the golden set has fewer than three questions that only hybrid search answers, the solution scores five lab-local questions from `data/extra_questions.jsonl` and labels them as such.

## How to run

The worked solution is [solution/m16_solution.ipynb](solution/m16_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`.

Keys, as environment variables in the `.env` file at the repo root: `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`). The notebook also creates the chat model shared by the Part V cell (`EXPERIENTIALLABS_API_KEY`), though this lab only retrieves.

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. `data/extra_questions.jsonl` holds five lab-local questions in the golden-set schema, used only if the golden set has fewer than three questions that only hybrid search answers. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date and embedding model | *pending run* |
| Hit rate, recall and MRR for BM25 weights 0 to 1 | *pending run* |
| Best weight | *pending run* |
| Questions only hybrid search answers (and whether lab-local questions were needed) | *pending run* |

Back to the module: [README.md](../README.md)
