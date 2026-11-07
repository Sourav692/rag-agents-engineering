# Lab: M23 ReAct Agents & LangChain create_agent

## Brief

ReAct research agent: give a `create_agent` agent your RAG retriever and a web-search tool, add a middleware that blocks off-topic questions, and compare its answers with your Part V system.

## Approach

- ReAct interleaves reasoning and tool calls, and reads every observation before choosing the next step. `create_agent(model, tools, system_prompt=...)` returns that loop as a compiled LangGraph graph on native tool calls.
- Middleware hooks run before and after the agent and each model call. The solution's `before_agent` guard classifies the question once and jumps to the end with a fixed reply when it is off topic, so a blocked question never reaches the tools. `ModelCallLimitMiddleware` bounds each run.
- The comparison is with the inline Part V system (retrieve 4, answer with citations). The interesting rows are the out-of-corpus questions, where the Part V system should refuse and the agent can reach for the web.
- What to watch: count both guard errors (off-topic questions let through, customer questions blocked), and compare tool calls and latency per question, since every loop round rereads the whole message list.

## How to run

The worked solution is [solution/m23_solution.ipynb](solution/m23_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`.

Keys, as environment variables in the `.env` file at the repo root: `EXPERIENTIALLABS_API_KEY` for the chat model, `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings, and `TAVILY_API_KEY` for the web-search tool.

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. `data/off_topic.jsonl` holds the five off-topic questions. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date and models | *pending run* |
| Correct answers on the in-corpus golden questions: agent and Part V system | *pending run* |
| Out-of-corpus golden questions: what each system did | *pending run* |
| Off-topic questions blocked (of 5) | *pending run* |
| Golden questions blocked by mistake | *pending run* |
| Tool calls and latency per question | *pending run* |

Back to the module: [README.md](../README.md)
