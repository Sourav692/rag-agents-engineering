# Lab: M33 Short-Term Memory & Conversation State

## Brief

Follow-up test: write 15 three-turn conversations and compare retrieval hit rate on turns two and three with and without history-aware query rewriting.

## Solution

[`solution/m33_solution.ipynb`](solution/m33_solution.ipynb) retrieves for every turn of 15 three-turn conversations twice, with the turn's text alone and with a history-aware rewrite (the contextualise prompt of `create_history_aware_retriever`), and compares hit rate at k=4 on turns two and three.

## Approach

- A follow-up such as "How long do I have?" names no subject, so the retriever searches for the wrong thing (M33 theory).
- A history-aware retriever asks the model for a standalone question first. It costs an LLM call per follow-up and cannot fix a vocabulary mismatch.
- Appending earlier questions to the query is the cheaper alternative the M33 lab measures; it recovers turn 2 but drowns a change of topic on turn 3.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter); no extra group and no Docker.
- Keys, read from the repository's `.env`: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), and `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the embeddings (`get_embeddings()` defaults to `databricks-gte-large-en`).
- Open [`solution/m33_solution.ipynb`](solution/m33_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m33_solution.ipynb --output /tmp/m33_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m33_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| Turn | Turns | Hit rate without rewriting | Hit rate with rewriting |
|---|---|---|---|
| 1 | 15 | *pending run* | *pending run* |
| 2 | 15 | *pending run* | *pending run* |
| 3 | 15 | *pending run* | *pending run* |
| 2 and 3 | 30 | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
