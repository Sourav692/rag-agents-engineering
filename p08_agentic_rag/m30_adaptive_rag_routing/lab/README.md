# Lab: M30 Adaptive RAG & Query Routing

## Brief

Support desk router: route billing, technical and general questions to separate knowledge bases, escalate negative-sentiment tickets, and report routing accuracy.

## Solution

[`solution/m30_solution.ipynb`](solution/m30_solution.ipynb) triages 40 tickets with one structured call (route and sentiment), escalates negative tickets to a human, answers the rest from the routed knowledge base in a LangGraph graph, and reports routing accuracy and escalation precision and recall.

## Approach

- A router is a classifier in front of retrieval: one LLM call with structured output that must return a label from a fixed set (M30 theory).
- A misroute hides the answer, because retrieval only searches the knowledge base the router picked. The confusion table shows which pair of knowledge bases the router mixes up.
- Escalation is checked before the category: a negative ticket goes to a person whatever it is about.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter); no extra group and no Docker.
- Keys, read from the repository's `.env`: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), and `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the embeddings (`get_embeddings()` defaults to `databricks-gte-large-en`).
- Open [`solution/m30_solution.ipynb`](solution/m30_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m30_solution.ipynb --output /tmp/m30_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m30_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| Metric | Value |
|---|---|
| Routing accuracy (40 tickets) | *pending run* |
| Escalation precision | *pending run* |
| Escalation recall | *pending run* |

Back to the module: [README.md](../README.md)
