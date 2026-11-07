# Lab: M13 Embeddings & Model Selection

## Brief

Embedding shoot-out: compare one hosted and two open-source models on a 30-question golden set and pick one, writing down the cost and latency per 1,000 chunks.

## Approach

- Check the norm before you choose a metric. OpenAI returns unit-length vectors, for which cosine, dot product and Euclidean distance rank identically; sentence-transformers does not normalise by default. The solution normalises the open models and ranks by cosine for all three.
- Dimensions are a cost paid on every query: `text-embedding-3-small` returns 1,536 numbers. Compare that with the open models' vector size in the results.
- Domain fit is measured on your own golden set, not read off a leaderboard. The same model must embed documents and queries; a mismatch raises no error and returns noise.
- Cost per 1,000 chunks uses `tiktoken` token counts and a price constant in the notebook (`PRICE_PER_1M`); confirm the price on the provider's page on the run date. Latency for the open models depends on the machine, so record it with the run.

## How to run

The worked solution is [solution/m13_solution.ipynb](solution/m13_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the `hf` group: `uv run --group hf jupyter lab`. The first run downloads the two open models from the Hugging Face Hub.

Keys, as environment variables in the `.env` file at the repo root: `OPENAI_API_KEY` for `text-embedding-3-small`. The open models need no key.

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date, machine and price date | *pending run* |
| Hit rate, recall and MRR at k = 4 (3 models) | *pending run* |
| Seconds per 1,000 chunks (3 models) | *pending run* |
| USD per 1,000 chunks (hosted model) | *pending run* |
| The pick and its reason | *pending run* |

Back to the module: [README.md](../README.md)
