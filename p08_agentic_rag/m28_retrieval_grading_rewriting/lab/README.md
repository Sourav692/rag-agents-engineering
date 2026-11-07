# Lab: M28 Agentic RAG Foundations: Grading & Query Rewriting

## Brief

Grader loop: add a relevance grader and a two-retry rewrite loop to your Part V system and log how often each path fires on the golden set.

## Solution

[`solution/m28_solution.ipynb`](solution/m28_solution.ipynb) rebuilds the Part V system inline, adds a relevance grader and a rewrite loop capped at two retries as a LangGraph graph, runs the 30 golden questions and counts how often each path fires.

## Approach

- A grader is an LLM call with structured output that reads the retrieved text beside the question; a conditional edge turns its verdict into the next node (M28 theory).
- A retriever returns `k` chunks for every query, relevant or not, so without the grader the model answers from whatever came back.
- A rewrite loop needs a counter in state. Lesson 28.3's graph allows 2 rewrites per question, and so does this one; after the second failed grade the graph refuses.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter); no extra group and no Docker.
- Keys, read from the repository's `.env`: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), and `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the embeddings (`get_embeddings()` defaults to `databricks-gte-large-en`).
- Open [`solution/m28_solution.ipynb`](solution/m28_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m28_solution.ipynb --output /tmp/m28_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m28_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| Path | lookup (15) | multi_hop (6) | numeric (4) | out_of_corpus (5) | all (30) |
|---|---|---|---|---|---|
| Answered, first retrieval | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| Answered after 1 rewrite | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| Answered after 2 rewrites | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| Refused after 2 rewrites | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
