# Lab: M38 MCP Foundations

## Brief

Retriever over MCP: expose your Part V retriever as an MCP tool and call it from an MCP client chatbot.

Solution: [solution/m38_solution.ipynb](solution/m38_solution.ipynb) (the client) and [solution/server.py](solution/server.py) (the server).

## Approach

MCP splits the tool-calling loop in two. The server owns the tool and its JSON schema; the client owns the model, the session and the loop.

- **Server.** `server.py` builds `FastMCP("larkspur-handbook")`, as notebook `02a_creating_an_mcp_server.ipynb` builds its research server, and registers one `@mcp.tool()`, `search_handbook(query, k)`. The retriever is the lab baseline (recursive split, TF-IDF from `src/lab_kit.py`), rebuilt inline so this lab depends on no other. It returns each passage with its source file and runs offline.
- **Client.** The notebook starts the server with `StdioServerParameters` and `stdio_client`, calls `session.initialize()` and `list_tools()`, then runs the chatbot loop of notebook `03a_creating_an_mcp_client.ipynb`: the tool schemas go to `bind_tools`, each tool call the model makes goes to `session.call_tool`, and the result comes back as a `ToolMessage`.

What to watch:

- Step 1 calls the tool with no model at all. If it fails, the problem is the transport or the server, not the model.
- A Jupyter kernel's `sys.stderr` has no file descriptor, so the notebook passes `errlog=open(os.devnull, "w")` to `stdio_client`.
- The loop stops at `MAX_TOOL_ROUNDS = 4`, so a model that keeps calling the tool cannot run forever.

## How to run

- Environment: `uv sync --group protocols` (the `mcp` SDK).
- Keys: `EXPERIENTIALLABS_API_KEY` (chat model, through `get_experientiallabs_llm()`). The server needs none.
- No Docker.
- Run `solution/m38_solution.ipynb` top to bottom from the `solution/` folder; it starts and stops `server.py` itself.

## Data

See [data/README.md](data/README.md): the shared `larkspur/` copy.

## Results

Not run yet. The table is filled from a real run of the solution, with its date and model.

| Question | Tool calls | Seconds | Evidence span in answer |
|---|---|---|---|
| g01 | *pending run* | *pending run* | *pending run* |
| g04 | *pending run* | *pending run* | *pending run* |
| g10 | *pending run* | *pending run* | *pending run* |

Run date: *pending run*. Model: *pending run*.

Back to the module: [README.md](../README.md)
