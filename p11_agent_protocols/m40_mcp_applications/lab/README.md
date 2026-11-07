# Lab: M40 MCP Applications & RAG over MCP

## Brief

Shared retrieval: connect the RAG-over-MCP server to two different clients (a LangGraph agent and Claude Desktop or a local agent) and compare answers.

Solution: [solution/m40_solution.ipynb](solution/m40_solution.ipynb) (both clients) and [solution/rag_server.py](solution/rag_server.py) (the server).

## Approach

`rag_server.py` is a `FastMCP` server in the shape of the module's `06_mcp_rag_with_langchain` server: a `retrieve(query, n)` tool that returns passages with their source files, and a `db_info()` tool that describes the index. The index is offline TF-IDF over the Larkspur handbook, so the server needs no keys. Two clients reach it over stdio:

- **LangGraph agent.** `create_agent` with each MCP tool wrapped as a LangChain `StructuredTool` whose coroutine calls `session.call_tool`. The server's JSON schema is passed through as `args_schema`.
- **Local agent.** A hand-written client loop with no agent framework: `bind_tools` on the MCP schemas, forward each tool call, return a `ToolMessage`. It uses `SECOND_LLM`, the same model by default; point it at a local model (the module's `02_mcp_servers_and_local_agent` project uses Ollama through the `mcp-apps` group) to compare models as well as harnesses.

What to watch:

- The server is written once and imported by neither client. A difference between the two answer columns is a client difference: how often each calls `retrieve`, with which `n`, and how it writes the answer.
- The comparison table's span check is rough. Read the paired answers the notebook prints against the references.

### Optional: Claude Desktop as a third client

Not run by the notebook. Lesson 40.2's theory page explains the file: Claude Desktop reads `claude_desktop_config.json`, a map under `mcpServers` from a name to the command that starts the server, with absolute paths and `uv --directory` to set the working directory. An entry for this server:

```json
{
  "mcpServers": {
    "larkspur-rag": {
      "command": "uv",
      "args": ["--directory", "/ABSOLUTE/PATH/TO/rag-agents-engineering/p11_agent_protocols/m40_mcp_applications/lab/solution",
               "run", "--group", "protocols", "python", "rag_server.py"]
    }
  }
}
```

Restart Claude Desktop, ask the five questions below, and add its answers to the table by hand.

## How to run

- Environment: `uv sync --group protocols` (the `mcp` SDK).
- Keys: `EXPERIENTIALLABS_API_KEY` (chat model, through `get_experientiallabs_llm()`). The server needs none.
- No Docker.
- Run `solution/m40_solution.ipynb` top to bottom from the `solution/` folder; each client starts and stops its own server process.

## Data

See [data/README.md](data/README.md): the shared `larkspur/` copy.

## Results

Not run yet. The table is filled from a real run of the solution, with its date and models.

| Question | LangGraph agent: tool calls | LangGraph agent: span in answer | Local agent: tool calls | Local agent: span in answer |
|---|---|---|---|---|
| g03 | *pending run* | *pending run* | *pending run* | *pending run* |
| g07 | *pending run* | *pending run* | *pending run* | *pending run* |
| g13 | *pending run* | *pending run* | *pending run* | *pending run* |
| g17 | *pending run* | *pending run* | *pending run* | *pending run* |
| g20 | *pending run* | *pending run* | *pending run* | *pending run* |

Run date: *pending run*. Models: *pending run*.

Back to the module: [README.md](../README.md)
