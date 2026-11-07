# Lab: M32 Reliability, Feedback Loops & Diversity

## Brief

Feedback flywheel: simulate 100 thumbs-up / thumbs-down events and show the effect on ranking for the affected queries.

## Solution

[`solution/m32_solution.ipynb`](solution/m32_solution.ipynb) simulates 100 thumbs-up and thumbs-down events with seed 42 over the top 4 passages shown for the 25 answerable golden questions, reranks the top 8 candidates by feedback (per query and pooled), and reports the target passage's rank before and after for each affected query.

## Approach

- Notebook 02a reranks with `relevance_score *= average rating / 3`, which keeps every chunk between 0.333 and 1.667 (M32 theory). With thumbs instead of 1 to 5 ratings, this solution multiplies the score by `1 + 0.1 x net votes`, clipped to 0.5 to 1.5.
- In 02a a rating on the answer lands on every chunk in it, so an unrelated chunk can ride a good answer up. Here each event rates one passage, which isolates the reranking effect from that attribution problem.
- Pooled feedback moves queries nobody rated; the results compare it with per-query feedback.
- No model is called; only the embeddings are.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter); no extra group and no Docker.
- Keys, read from the repository's `.env`: `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the embeddings (`get_embeddings()`); the notebook makes no chat-model calls, though the setup cell builds the client and so reads `EXPERIENTIALLABS_API_KEY`.
- Open [`solution/m32_solution.ipynb`](solution/m32_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m32_solution.ipynb --output /tmp/m32_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m32_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| Queries | MRR before | MRR after (per-query) | MRR after (pooled) |
|---|---|---|---|
| Affected | *pending run* | *pending run* | *pending run* |
| Not affected | *pending run* | *pending run* | *pending run* |

The rank of the target passage before and after, for each affected query: *pending run*.

Back to the module: [README.md](../README.md)
