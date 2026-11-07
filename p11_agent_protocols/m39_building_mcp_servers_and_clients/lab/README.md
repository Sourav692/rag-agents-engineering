# Lab: M39 Building MCP Servers & Clients

## Brief

Two servers, one client: put your retriever and a web-search tool in separate MCP servers and route between them from one client.

Solution: [solution/m39_solution.ipynb](solution/m39_solution.ipynb) (the client), [solution/retriever_server.py](solution/retriever_server.py) and [solution/web_server.py](solution/web_server.py) (the servers).

## Approach

Each server is a `FastMCP` app with one tool: `search_handbook` over the Larkspur handbook (offline TF-IDF, the M38 lab's server rebuilt here) and `search_web` over Tavily. The client follows the multi-server client of lesson 39.4: it opens one `ClientSession` per server inside an `AsyncExitStack`, merges the tool lists, keeps a map from tool name to the session that owns it, and forwards each tool call the model makes to that session.

What to watch:

- The routing decision is the model's tool choice, driven by the two tool descriptions and the system prompt. The client records it as `tool@server`, so a wrong route is visible per question.
- A stdio server starts with only the environment the client passes. The web server needs `TAVILY_API_KEY`, so the client passes it with `PATH`; the retriever server gets no keys.
- Tool names must be unique across servers, because the client looks the owner up by name. Two servers that both expose `search` would need prefixed names.

## How to run

- Environment: `uv sync --group protocols` (the `mcp` SDK; `tavily-python` is a default dependency).
- Keys: `EXPERIENTIALLABS_API_KEY` (chat model, through `get_experientiallabs_llm()`) and `TAVILY_API_KEY` (web server).
- No Docker.
- Run `solution/m39_solution.ipynb` top to bottom from the `solution/` folder; it starts and stops both servers.

## Data

See [data/README.md](data/README.md): the shared `larkspur/` copy.

## Results

Not run yet. The table is filled from a real run of the solution, with its date and model.

| Question | Expected tool | Routed to | As expected |
|---|---|---|---|
| g04: How many servers can a Starter account run? | `search_handbook` | *pending run* | *pending run* |
| g10: What does the API return when I go over the rate limit? | `search_handbook` | *pending run* | *pending run* |
| g22: What monthly availability does Larkspur guarantee? | `search_handbook` | *pending run* | *pending run* |
| Latest stable Python release | `search_web` | *pending run* | *pending run* |
| Who maintains the MCP specification | `search_web` | *pending run* | *pending run* |

Run date: *pending run*. Model: *pending run*.

Back to the module: [README.md](../README.md)
