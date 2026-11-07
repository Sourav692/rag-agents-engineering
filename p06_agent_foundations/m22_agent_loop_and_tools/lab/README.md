# Lab: M22 The Agent Loop & Tool Calling

## Brief

Retriever as a tool, by hand: wrap your Part V retriever as a tool, run it through your own tool loop with no framework, and log every tool call and error.

## Approach

- The loop has one rule: while the model's reply holds tool calls, run them and call the model again; a reply with no tool calls is the answer. Cap the rounds.
- A tool reaches the model only as a schema: a name, a description and typed parameters. The solution writes that schema by hand, the way the module's raw-API notebooks do.
- Tool results go back as one `tool` message per call, matched by `tool_call_id`.
- A tool error has to reach the model as a message, or the run crashes. The solution catches bad JSON, unknown tools and exceptions inside the tool, returns each as an error message, and logs it. One run injects a bad argument to show that path.
- "No framework" applies to the loop. The tool body reuses the Part V retriever (FAISS with the course embeddings), built inline in the notebook.

## How to run

The worked solution is [solution/m22_solution.ipynb](solution/m22_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`.

Keys, as environment variables in the `.env` file at the repo root: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`). The loop calls `https://api.experientiallabs.ai/v1` with the `openai` client, using the same key.

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date and models | *pending run* |
| Call log: run, round, tool, arguments, ok or error, milliseconds | *pending run* |
| Rounds per run | *pending run* |
| Forced-error run: the error message and what the model did next | *pending run* |

Back to the module: [README.md](../README.md)
