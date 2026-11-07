# Lab: M31 RAG as an Agent Tool

## Brief

Two-tool agent: give an agent a private-docs RAG tool and a web-search tool, and tune the tool descriptions until it picks the right one on 20 mixed questions.

## Solution

[`solution/m31_solution.ipynb`](solution/m31_solution.ipynb) gives the model a private-docs RAG tool and a Tavily web-search tool, measures which tool it calls first on 20 labelled questions under three rounds of tool descriptions (printed in the notebook), and runs the full `create_agent` loop on two questions with the last round's descriptions.

## Approach

- All the model knows about a tool is its name, its description and its argument schema (M31 theory), so the rounds change only the descriptions.
- Tune descriptions like any retrieval setting: on a labelled set, then on questions held out from it. The 20 questions here are the tuning set; hold some back before you trust a description.
- Longer descriptions cost tokens on every model call.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter); no extra group and no Docker.
- Keys, read from the repository's `.env`: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), and `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the embeddings (`get_embeddings()` defaults to `databricks-gte-large-en`); `TAVILY_API_KEY` for the web tool.
- Open [`solution/m31_solution.ipynb`](solution/m31_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m31_solution.ipynb --output /tmp/m31_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m31_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| Round | Tool-choice accuracy (20) | docs correct (10) | web correct (10) |
|---|---|---|---|
| 1 | *pending run* | *pending run* | *pending run* |
| 2 | *pending run* | *pending run* | *pending run* |
| 3 | *pending run* | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
