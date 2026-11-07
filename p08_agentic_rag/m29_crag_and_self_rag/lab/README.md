# Lab: M29 Self-Correcting RAG: CRAG & Self-RAG

## Brief

Out-of-corpus stress test: send questions the corpus cannot answer and compare the baseline, CRAG and Self-RAG on refusals, web fallbacks and hallucinated answers.

## Solution

[`solution/m29_solution.ipynb`](solution/m29_solution.ipynb) runs the baseline, CRAG (per-passage grading, web fallback) and Self-RAG (retrieve gate, relevance filter, groundedness and usefulness checks) on 15 out-of-corpus questions, and counts refusals, web fallbacks and hallucinated answers with a judge prompt the notebook prints.

## Approach

- CRAG puts a retrieval evaluator between retrieval and generation and searches the web when the retrieved chunks fail it. Self-RAG makes four judgments: retrieve or not, is this chunk relevant, is the answer supported, is it useful (M29 theory).
- The groundedness check is the hallucination guard. M29 notes that in notebook 02a it passes without a call when there are no documents; this solution refuses when no passage survives the relevance filter.
- Larkspur is fictional, so the web holds nothing about it. Every question here is out of corpus, so any direct answer counts as hallucinated, whatever its source.
- Correction is paid in LLM calls; the M29 theory measures how many.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter); no extra group and no Docker.
- Keys, read from the repository's `.env`: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), and `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the embeddings (`get_embeddings()` defaults to `databricks-gte-large-en`); `TAVILY_API_KEY` for the web search.
- Open [`solution/m29_solution.ipynb`](solution/m29_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m29_solution.ipynb --output /tmp/m29_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m29_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| System | Questions | Refusals | Web fallbacks | Hallucinated answers |
|---|---|---|---|---|
| Baseline | 15 | *pending run* | *pending run* | *pending run* |
| CRAG | 15 | *pending run* | *pending run* | *pending run* |
| Self-RAG | 15 | *pending run* | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
