# Lab: M21 Framework Fluency: LlamaIndex

## Brief

Port one of your Part V pipelines (hybrid + rerank) to LlamaIndex and confirm the metrics match.

## Approach

- A LlamaIndex Node is a chunk with an id, metadata and links to its source and neighbours. By default the metadata string is part of what gets embedded; the solution excludes it so both pipelines embed the same text.
- `QueryFusionRetriever` makes 4 queries (3 of them written by the LLM) unless you set `num_queries=1`. The port sets it, so both sides fuse the same two ranked lists.
- Postprocessors run in list order on the retrieved nodes; `SentenceTransformerRerank` with `cross-encoder/ms-marco-MiniLM-L-6-v2` is the same model the LangChain side calls through `sentence_transformers.CrossEncoder`.
- Read what each object actually holds before trusting a port. The notebook prints every question where the two pipelines disagree and where the evidence first appears in each stage-1 list, which is how a gap gets explained.

## How to run

The worked solution is [solution/m21_solution.ipynb](solution/m21_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the `llamaindex` and `hf` groups: `uv run --group llamaindex --group hf jupyter lab`. The first run downloads the cross-encoder.

Keys, as environment variables in the `.env` file at the repo root: `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`), used by both pipelines. The notebook also creates the chat model (`EXPERIENTIALLABS_API_KEY`); no chat call is made, and LlamaIndex gets a `MockLLM`.

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date, embedding model and reranker | *pending run* |
| LangChain: hit rate, recall and MRR at 4 (25 questions with evidence) | *pending run* |
| LlamaIndex: hit rate, recall and MRR at 4 (25 questions with evidence) | *pending run* |
| Questions where the two differ, and the stage the gap starts in | *pending run* |

Back to the module: [README.md](../README.md)
