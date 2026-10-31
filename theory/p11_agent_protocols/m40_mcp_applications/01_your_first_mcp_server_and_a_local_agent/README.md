# M40.1 Theory: Your first MCP server and a local agent

*[M40 theory](../README.md) · Lesson 40.1 · Notebooks: [`01_build_your_first_mcp_server`](../../../../course/p11_agent_protocols/m40_mcp_applications/projects/01_build_your_first_mcp_server), [`02_mcp_servers_and_local_agent`](../../../../course/p11_agent_protocols/m40_mcp_applications/projects/02_mcp_servers_and_local_agent) · [All theory pages](../../../README.md)*

## A local agent over MCP

The first project serves two FastMCP servers over streamable HTTP: `demo-server` with one `add` tool, and `weather` with `get_weather` and `get_forecast`, which call the public wttr.in API. Each comes with a plain client that lists the tools and calls one. `client_fastmcp.py` uses FastMCP's `Client` on `http://127.0.0.1:8000/mcp`; `client_mcp.py` uses the SDK's `streamablehttp_client` and `ClientSession`, and prints the session id before and after `initialize`: `None`, then a 32-character hex id the server assigned during the handshake ([M39](../../m39_building_mcp_servers_and_clients/README.md) covers that header).

The second project hands the same servers to an agent that runs on your machine. `mcp_use` reads a server map in the shape Claude Desktop uses, starts or connects to each server, and gives their tools to a LangChain chat model:

```python
client = MCPClient.from_config_file("mcp-http.json")       # or MCPClient.from_dict(config)
llm = ChatOllama(base_url="http://localhost:11434", model="gpt-oss:20b")
agent = MCPAgent(llm=llm, client=client, max_steps=30, use_server_manager=True)
await agent.run("What's the weather in New York and the 3-day forecast? Also, what's 12 multiplied by 342?")
```

The project's two config files show the two ways a host reaches a server:

| Config | Entry | Who starts the server |
|---|---|---|
| `mcp.json` | `"command": "uv", "args": ["run", "--directory", "…/servers", "weather_server.py"]` | The agent, as a stdio subprocess |
| `mcp-http.json` | `"url": "http://localhost:8001/mcp"` (weather), `:8000/mcp` (math) | You, in another terminal, before the agent runs |

Two `MCPAgent` settings change what the model does, and both have defaults worth knowing in mcp-use 1.7.1:

- **`max_steps`** caps the agent loop. The default is 5; both clients raise it to 30. The advanced query needs at least three tool calls (weather, forecast, multiply), so a low cap ends the run before the answer.
- **`use_server_manager=True`** stops the model from seeing the servers' tools directly. It gets five management tools instead (`list_mcp_servers`, `connect_to_mcp_server`, `get_active_mcp_server`, `search_mcp_tools`, `disconnect_from_mcp_server`) and must connect to a server before it can call `multiply`. That keeps the prompt small when many servers are configured, at the price of extra model turns.

The models are local Ollama models (`qwen3:8b` in `agentic_client.py`, `gpt-oss:20b` in the advanced client), so the whole loop runs without an API key. The weather tools still call wttr.in over the internet.

## Return types are part of the contract

FastMCP builds a tool's output schema from its return annotation. In fastmcp 3.4.11, `add(a: int, b: int) -> int` lists as:

```json
{"inputSchema":  {"properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}, "required": ["a", "b"], "type": "object", "additionalProperties": false},
 "outputSchema": {"properties": {"result": {"type": "integer"}}, "required": ["result"], "type": "object", "x-fastmcp-wrap-result": true}}
```

A call to `add` with 5 and 7 returns the text `12` and the structured content `{"result": 12}`. The client keeps the output schema and checks every structured result against it.

The math server's `divide` breaks its own schema. It is annotated `-> float` and returns the string `"Error: Division by zero"` when `b` is 0. The server sends that result; the mcp 1.30.0 client rejects it:

```
RuntimeError: Invalid structured content returned by tool divide: 'Error: Division by zero' is not of type 'number'
```

The friendly message never reaches the model. The host gets an exception from its own client library instead of a tool result it could show the model. Two fixes keep the error inside the protocol, both checked against fastmcp 3.4.11:

- **Raise instead of returning.** `raise ToolError("Division by zero")` comes back as a result with `isError: true` and the text `Division by zero`. Without the check, `1 / 0` raises `ZeroDivisionError`, which also comes back with `isError: true`, as `Error calling tool 'divide': division by zero`.
- **Annotate what you return.** `-> float | str` makes the string valid, and moves the job of telling numbers from error messages to every client.

## Check yourself

<details>
<summary>1. What does use_server_manager=True change about what the model sees, and what does it trade?</summary>

The model no longer sees the servers' tools directly. It gets five management tools (`list_mcp_servers`, `connect_to_mcp_server`, `get_active_mcp_server`, `search_mcp_tools`, `disconnect_from_mcp_server`) and must connect to a server before it can call `multiply`. That keeps the prompt small when many servers are configured, at the price of extra model turns.

</details>

<details>
<summary>2. The advanced query asks for New York's weather, its 3-day forecast and 12 times 342. Why do both clients raise max_steps from its default of 5 to 30?</summary>

`max_steps` caps the agent loop. The query needs at least three tool calls (weather, forecast, multiply), and with the server manager on the model also spends turns connecting to servers, so a low cap ends the run before the answer.

</details>

<details>
<summary>3. Calling divide with b equal to 0 gives the host a RuntimeError about invalid structured content instead of a tool result. Why, and how do you fix it?</summary>

`divide` is annotated `-> float` but returns the string `"Error: Division by zero"`, and the mcp 1.30.0 client checks structured results against the output schema, so it raises. Use `raise ToolError("Division by zero")`, which comes back with `isError: true`, or annotate `-> float | str`, which moves the job of telling numbers from errors to every client.

</details>

---
*Previous: [M40 overview](../README.md). Next: [40.2 MCP servers with Claude Desktop](../02_mcp_servers_with_claude_desktop/README.md).*
