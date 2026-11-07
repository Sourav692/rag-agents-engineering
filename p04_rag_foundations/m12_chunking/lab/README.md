# Lab: M12 Chunking Strategies

## Brief

Chunking bake-off: index the same corpus with recursive, semantic and proposition chunking at three sizes each, and compare hit rate and answer faithfulness against the M10 baseline.

## Approach

- Small chunks retrieve precisely but can cut a fact in two; large chunks keep facts whole but dilute the embedding and cost tokens. The right size comes from measurement on your own corpus, which is why every family runs at three sizes.
- Semantic chunking cuts where neighbouring sentences drift apart in embedding space. The breakpoint threshold is computed from each document's own distances, and the default `percentile` type always produces some cuts.
- Propositions are atomic, self-contained facts written by an LLM. They retrieve sharply, cost an LLM call per chunk, and need checking because an LLM can invent text and a splitter cannot. Because they are rewritten, the solution scores a proposition hit by the base chunk it came from; say so when you compare it with the other rows.
- Compare every row with `lab_kit.baseline` (TF-IDF over recursive 500-character chunks), the reference in `data/larkspur/README.md`.

## How to run

The worked solution is [solution/m12_solution.ipynb](solution/m12_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`.

Keys, as environment variables in the `.env` file at the repo root: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`). The proposition step makes one LLM call per base chunk; the faithfulness pass makes two calls per question per chunking (answer and judge).

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date and models | *pending run* |
| Chunks per chunking (9 rows) | *pending run* |
| Hit rate, recall and MRR at k = 4 (9 rows) | *pending run* |
| Faithfulness (9 rows) | *pending run* |
| `lab_kit.baseline` reference row | *pending run* |

Back to the module: [README.md](../README.md)
