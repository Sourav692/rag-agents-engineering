# Lab: M10 Why RAG & the RAG Lifecycle

## Brief

Baseline pipeline: build the canonical lifecycle notebook end to end on the course corpus and save its retrieval and answer metrics. Every later module reports its improvement against this baseline.

## Approach

- RAG moves knowledge out of model weights into an index you control, so you can update it, restrict it and cite it. The pipeline has an offline indexing phase (load, split, embed, store) and an online query phase (retrieve, augment, generate); a mistake made at indexing time often shows up only in the generated answer.
- `k` controls how much context the model reads. It trades recall against precision, tokens and latency, and it cannot recover a chunk the retriever scored as irrelevant. The solution fixes `k = 4` so its numbers line up with the TF-IDF reference row in `data/larkspur/README.md`.
- Embeddings match meaning where TF-IDF matches exact words, so the two retrievers miss different questions on the handbook. Read the per-question rows, not only the means.
- The LLM judge grades two things separately: correctness against the reference answer and faithfulness to the passages. Out-of-corpus questions are scored by refusal, not by the judge. Watch the false refusals too: a system that refuses everything scores 5 of 5 on the out-of-corpus questions.
- Build the plain pipeline first, record its numbers on a fixed question set, then change one stage at a time and compare. That is what `baseline.json` is for.

## How to run

The worked solution is [solution/m10_solution.ipynb](solution/m10_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`.

Keys, as environment variables in the `.env` file at the repo root: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`).

The notebook writes `solution/baseline.json` (date, models, retrieval and answer metrics). Commit that file after the first full run; it is the reference baseline for every later lab.

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date and models | *pending run* |
| Hit rate at k = 4 (vector) | *pending run* |
| Recall at k = 4 (vector) | *pending run* |
| MRR (vector) | *pending run* |
| Answer correctness (25 questions) | *pending run* |
| Faithfulness (25 questions) | *pending run* |
| Refusals on the 5 out-of-corpus questions | *pending run* |
| False refusals on the 25 in-corpus questions | *pending run* |
| Mean retrieval and generation latency | *pending run* |

Back to the module: [README.md](../README.md)
