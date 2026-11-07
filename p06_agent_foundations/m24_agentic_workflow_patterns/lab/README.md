# Lab: M24 Agentic Workflow Patterns

## Brief

Pattern mapping: rebuild query decomposition (M17) as orchestrator–worker and an answer-quality check as evaluator–optimizer, then compare latency and cost with the chain versions.

## Approach

- In a workflow, code fixes the path through the LLM calls; in an agent (M23), the model picks its next step. Each pattern here hands the model one decision at most: how many sub-questions, or whether an answer passes.
- A fan-out lasts as long as its slowest branch. Orchestrator-worker runs one worker per sub-question in parallel with LangGraph's `Send`, then pays one more call to synthesise; the chain version answers once from all passages.
- Every loop gets a cap in code. LCEL cannot loop, so the evaluator-optimizer cycle lives in LangGraph; at `MAX_ITERATIONS = 3` it makes at most six LLM calls per question. The counter is bumped in the generator node, because a conditional edge's state writes are discarded.
- The 10 questions are the 6 multi-hop golden questions and 4 lookups. Cost is reported as LLM calls and tokens per question; set `PRICE_IN_PER_1M` and `PRICE_OUT_PER_1M` in the notebook from the provider's price page to get dollars.

## How to run

The worked solution is [solution/m24_solution.ipynb](solution/m24_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`.

Keys, as environment variables in the `.env` file at the repo root: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`). The notebook's prices are `None` until you fill them in from the provider's price page on the run date.

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date, models and price date | *pending run* |
| Decomposition: seconds, LLM calls and tokens per question (chain, orchestrator-worker) | *pending run* |
| Quality check: seconds, LLM calls and tokens per question (chain, evaluator-optimizer) | *pending run* |
| Mean evaluator-optimizer iterations | *pending run* |
| Cost per question (if prices are set) | *pending run* |

Back to the module: [README.md](../README.md)
