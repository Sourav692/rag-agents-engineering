# Lab: M25 Planning, Reflection & Reasoning Patterns

## Brief

Verified answers: add chain-of-verification to your RAG answer step and measure how many unsupported claims it removes on the golden set.

## Solution

[`solution/m25_solution.ipynb`](solution/m25_solution.ipynb) answers the 25 answerable golden questions with the plain answer step and with chain-of-verification, and counts unsupported claims in both with a judge prompt the notebook prints.

## Approach

- Chain-of-verification drafts an answer, plans one verification question per claim, answers each one in a fresh call that never sees the draft, and revises the draft to keep what the checks support. It costs 1 + 1 + N + 1 calls for N verification questions (M25 theory).
- It removes unsupported claims; it does not add missing ones. A revision that says less also lowers the count, so the results table keeps the number of claims beside the number of unsupported ones.
- The judge is a model too. Read the claims it flags before trusting the totals.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter); no extra group and no Docker.
- Keys, read from the repository's `.env`: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), and `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the embeddings (`get_embeddings()` defaults to `databricks-gte-large-en`).
- Open [`solution/m25_solution.ipynb`](solution/m25_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m25_solution.ipynb --output /tmp/m25_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m25_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| Answer step | Questions | Claims | Unsupported claims | Answers with an unsupported claim |
|---|---|---|---|---|
| Baseline | 25 | *pending run* | *pending run* | *pending run* |
| Chain-of-verification | 25 | *pending run* | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
