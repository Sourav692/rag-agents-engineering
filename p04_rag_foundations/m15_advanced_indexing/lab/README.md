# Lab: M15 Advanced Indexing Strategies

## Brief

Index redesign: apply parent-document retrieval and contextual chunk headers to the baseline and report the change in hit rate and answer quality.

## Approach

- The search key and the payload can differ. The key is whatever gets embedded (a small child chunk, or a chunk with context prepended); the payload is what the model reads (a parent chunk, or the original chunk). An id stored with each key points at its payload.
- Parent-document retrieval searches small and returns large. Parent size is a cost dial: larger parents hold whole answers more often and send more tokens per question, so the solution reports the mean context size beside the hit rate.
- Context in the chunk fixes chunks that never name their subject: the contextual header puts the document and section name into the embedded text.
- Compare both against the Part V baseline built inline in the notebook (the same split as `lab_kit.baseline`, embedded and searched with FAISS).

## How to run

The worked solution is [solution/m15_solution.ipynb](solution/m15_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`.

Keys, as environment variables in the `.env` file at the repo root: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`).

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date and models | *pending run* |
| Hit rate, recall and MRR at k = 4 (baseline, parent-document, contextual headers) | *pending run* |
| Mean context characters per question | *pending run* |
| Correctness and faithfulness (25 questions each) | *pending run* |
| Out-of-corpus refusals | *pending run* |

Back to the module: [README.md](../README.md)
