# Lab: M41 A2A: Agent-to-Agent Protocol

## Brief

Agent as a service: put your agentic RAG graph behind A2A and call it from an agent built in a different framework.

Solution: [solution/m41_solution.ipynb](solution/m41_solution.ipynb).

## Approach

MCP gives an agent tools; A2A lets one agent hand a task to another agent it knows only by its Agent Card.

- **Server.** A LangGraph agentic RAG graph over the Larkspur handbook: retrieve, grade the passages with a typed yes or no, rewrite the query at most once (`MAX_REWRITES = 1`), then generate or say the handbook has no answer. An `AgentExecutor` adapts it to A2A, `DefaultRequestHandler` with an `InMemoryTaskStore` handles requests, and `A2AStarletteApplication` serves it with its Agent Card, following notebook `02a_langgraph_agent_over_a2a.ipynb`. Uvicorn runs in a background thread on port 10141.
- **Client.** A customer-success agent written with the OpenAI Python SDK and no agent framework, the role the plain-LLM agent plays in notebook `03a_cross_framework_agent_interop.ipynb`. The `protocols` group installs no second agent framework, so the contrast is LangGraph on one side and a hand-written tool loop on the other. It fetches the Agent Card with `A2ACardResolver`, builds its one tool's description from the card, and sends each call with `A2AClient.send_message`.

What to watch:

- The executor runs the synchronous graph with `asyncio.to_thread`, so the A2A server stays responsive while the graph works.
- The reply is a task whose status message carries the answer. `reply_text` reads the last text part, so it also works if a server replies with a plain message.
- `g27` is out of corpus: the graph's grade step should send it to the refusal, and the client agent should pass the refusal on instead of answering from its own knowledge.
- a2a-sdk 0.3 serves the card at `/.well-known/agent-card.json`; older servers used `/.well-known/agent.json`.

## How to run

- Environment: `uv sync --group protocols` (`a2a-sdk[http-server]`, `uvicorn`; the OpenAI SDK is a default dependency).
- Keys: `EXPERIENTIALLABS_API_KEY`, used by both sides: the graph through `get_experientiallabs_llm()`, the client agent through the OpenAI SDK pointed at the same endpoint.
- No Docker. The notebook starts the A2A server on `localhost:10141` and stops it in its last code cell.
- Run `solution/m41_solution.ipynb` top to bottom from the `solution/` folder.

## Data

See [data/README.md](data/README.md): the shared `larkspur/` copy.

## Results

Not run yet. The table is filled from a real run of the solution, with its date and model.

| Question | Type | A2A calls | Client answer matches reference |
|---|---|---|---|
| g05: Does a reboot change my server's IP address? | lookup | *pending run* | *pending run* |
| g19: EU data residency and daily backups, which plan and region? | multi_hop | *pending run* | *pending run* |
| g27: Does Larkspur offer a managed Kubernetes service? | out_of_corpus | *pending run* | *pending run* |

Run date: *pending run*. Model: *pending run*.

Back to the module: [README.md](../README.md)
