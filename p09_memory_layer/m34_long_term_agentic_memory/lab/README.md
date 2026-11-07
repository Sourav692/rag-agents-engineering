# Lab: M34 Long-Term & Agentic Memory

## Brief

Personal RAG: give your assistant semantic memory of user preferences and show that answers in a new thread use them.

## Solution

[`solution/m34_solution.ipynb`](solution/m34_solution.ipynb) extracts a user's preferences from a first thread into a LangGraph `InMemoryStore` with an embedding index, then answers four questions in a second thread with the memories recalled by similarity, side by side with the same graph for a user who has no memories.

## Approach

- A LangGraph store holds JSON items under a namespace tuple and a key, shared by every thread. The namespace comes from a trusted user id in the run's `context`, never from the model (M34 theory).
- Semantic memory upserts facts under stable keys, so a changed preference replaces the old one; here the key is the memory's topic.
- `search()` returns 10 items unless you pass `limit=`, and every recalled item costs prompt tokens, so the answer node recalls 3 by similarity.
- The expected-word check needs no judge but is crude: read the answers too.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter); no extra group and no Docker.
- Keys, read from the repository's `.env`: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), and `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the embeddings (`get_embeddings()` defaults to `databricks-gte-large-en`).
- Open [`solution/m34_solution.ipynb`](solution/m34_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m34_solution.ipynb --output /tmp/m34_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m34_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| Question | Expected word | Used with memory | Used without memory |
|---|---|---|---|
| Which region should I create our next server in? | Frankfurt | *pending run* | *pending run* |
| How long are our daily backups kept? | 7 days | *pending run* | *pending run* |
| How do I get a copy of last year's invoices? | finance | *pending run* | *pending run* |
| How quickly will support answer our tickets? | 4 hours | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
