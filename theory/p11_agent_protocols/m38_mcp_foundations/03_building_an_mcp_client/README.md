# M38.3 Theory: Building an MCP client

*[M38 theory](../README.md) · Lesson 38.3 · Notebooks: [`03a_creating_an_mcp_client.ipynb`](../../../../course/p11_agent_protocols/m38_mcp_foundations/notebooks/03a_creating_an_mcp_client.ipynb) · [All theory pages](../../../README.md)*

## MCP server / client

MCP names three roles. The **host** is the application the user talks to, here the chatbot with its LLM. The **client** is the piece inside the host that holds one connection to one server. The **server** offers tools, resources and prompts. A host that uses three servers holds three clients, and the model never talks to any server directly: it sees definitions and asks for calls, and the host decides which client sends them.

Notebook 03a wraps the 38.1 loop in an `MCP_ChatBot` class and adds the client:

```python
server_params = StdioServerParameters(command="uv", args=["run", "research_server.py"], env=None)

async with stdio_client(server_params) as (read, write):      # starts the server as a subprocess
    async with ClientSession(read, write) as session:          # one session, one server
        await session.initialize()
        response = await session.list_tools()
        self.available_tools = [{"name": t.name, "description": t.description,
                                 "input_schema": t.inputSchema} for t in response.tools]
        await self.chat_loop()                                 # calls session.call_tool(...)
```

With `stdio` the client owns the server's life: `stdio_client` starts the process, and leaving the `async with` block ends the session and stops it. Nothing has to be running beforehand.

Here is the session the client opens against the Larkspur handbook server, recorded over stdio with SDK 1.30.0. Sizes are the compact JSON of each message.

| Message | Direction | What it carries | Size |
|---|---|---|---|
| `initialize` request | client to server | `protocolVersion: "2025-11-25"`, the client's capabilities (none) and `clientInfo` | 152 |
| `initialize` result | server to client | the agreed version, capabilities for `tools`, `resources` and `prompts`, `serverInfo` | 276 |
| `notifications/initialized` | client to server | no id and no reply: the session is open | 54 |
| `tools/list` request | client to server | nothing but the method | 46 |
| `tools/list` result | server to client | one definition, `search_handbook`, with input and output schemas | 608 |
| `tools/call` request | client to server | `{"name": "search_handbook", "arguments": {"query": "How long does a refund take?"}}` | 135 |
| `tools/call` result | server to client | `refund-window` and `refund-timing` as text, the same text in `structuredContent`, `isError: false` | 835 |

Three details in that trace matter when you debug:

- **The handshake fixes what the session can do.** The server declared `tools`, `resources` and `prompts`, each with `listChanged: false`, so this client will not be told if the tool list changes; it has to list again.
- **Requests and replies pair by `id`.** The client numbers its requests 0, 1, 2 and the server echoes the id; the notification carries none because nothing answers it.
- **`serverInfo.version` was `1.30.0`**, the SDK version, because the server did not set one. Pass a version of your own if clients should be able to tell your releases apart.

The client also translates for the model. Notebook 03a's live code runs on OpenAI and wraps each MCP definition as `{"type": "function", "function": {"name": ..., "description": ..., "parameters": tool.inputSchema}}`; the Anthropic version kept in comments uses `input_schema: tool.inputSchema`. Both read the same `inputSchema`, so one server serves either model. On the way back the Anthropic version passes `result.content` as the `tool_result`, and the OpenAI version passes `result.content[0].text` as the `tool` message.

## Check yourself

<details>
<summary>1. A host uses three MCP servers. How many clients does it hold, and does the model ever talk to a server directly?</summary>

Three clients, each holding one connection to one server. The model never talks to a server: it sees definitions and asks for calls, and the host decides which client sends them.

</details>

<details>
<summary>2. In the recorded Larkspur session, the notifications/initialized message gets no reply. How do replies pair with requests, and why is this message different?</summary>

Requests and replies pair by `id`: the client numbers its requests 0, 1, 2 and the server echoes the id. `notifications/initialized` is a notification, so it carries no id and nothing answers it; it tells the server the session is open.

</details>

<details>
<summary>3. The server's tool list changes while a client is connected, and the client keeps offering the old list. What in the handshake explains this?</summary>

The server declared its capabilities with `listChanged: false` in the `initialize` result, so this client will not be told when the list changes. The handshake fixes what the session can do. The client has to call `tools/list` again to see the change.

</details>

---
*Previous: [38.2 Building an MCP server](../02_building_an_mcp_server/README.md). Next: [38.4 Connecting to reference servers](../04_connecting_to_reference_servers/README.md).*
