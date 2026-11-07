# M38.4 Theory: Connecting to reference servers

*[M38 theory](../README.md) · Lesson 38.4 · Notebooks: [`04a_connecting_to_reference_servers.ipynb`](../../notebook/04a_connecting_to_reference_servers.ipynb) · [All theory pages](../../../../../THEORY.md)*

## Reference servers

Larkspur connects handbook, fetch and filesystem servers to one host. You will inspect the launcher configuration, merge the discovered tool lists and test what happens when two servers advertise the same name.

### Step 1: Start only the configured server processes

The `modelcontextprotocol/servers` repository holds reference implementations you can run without writing a line of server code. The reference implementation adds two of them to the research server: **fetch** reads a URL and returns it as Markdown, and **filesystem** reads and writes files under the folders you allow. The chatbot stops hard-coding its server and reads a config file instead:

```json
{
  "mcpServers": {
    "filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]},
    "research":   {"command": "uv",  "args": ["run", "research_server.py"]},
    "fetch":      {"command": "uvx", "args": ["mcp-server-fetch"]}
  }
}
```

`npx` and `uvx` download and start a published server in one step, so nothing is installed ahead of time. The last filesystem argument is the folder it may touch: `.` is the folder the chatbot runs in. (The example's note says this lets the `fetch` server reach your files; it is the filesystem server that does.)

```mermaid
flowchart LR
    F[/server_config.json/] --> L["For each server<br/>in file order"]
    L --> S["stdio_client<br/>+ ClientSession"]
    S --> T["list_tools"]
    T --> A["available_tools<br/>append every tool"]
    T --> M["tool_to_session<br/>name to session"]
```

### Step 2: Keep a session and dispatch owner per server

`connect_to_servers` opens a session per server and keeps all of them on an `AsyncExitStack`, so `cleanup()` closes every session and subprocess in reverse order. For each tool it appends the definition to `available_tools`, which goes to the model on every request, and writes `tool_to_session[tool.name] = session`, which tells `process_query` where to send a call. A server that fails to start is caught and printed, and the chatbot carries on without its tools.

Recorded with the example's own `MCP_ChatBot` (SDK 1.30.0, `server-filesystem` 2.1.0, `mcp-server-fetch` 2026.10.28), the three servers offer:

| Server | Tools | Characters of tool JSON |
|---|---|---|
| filesystem | `read_file`, `read_text_file`, `read_media_file`, `read_multiple_files`, `write_file`, `edit_file`, `create_directory`, `list_directory`, `list_directory_with_sizes`, `directory_tree`, `move_file`, `search_files`, `get_file_info`, `list_allowed_directories` | 8,072 |
| research | `search_papers`, `extract_info` | 989 |
| fetch | `fetch` | 1,046 |

### Step 3: Count definitions and inspect name collisions

Two consequences follow from the two data structures:

- **Every definition costs on every call.** The three servers send 17 definitions, 10,107 characters, about 2,527 tokens, before the user's question, and the filesystem server is 80% of it. Adding the Larkspur retriever as a fourth server adds one tool and 417 characters.
- **Names must be unique across servers.** `tool_to_session` is a dict, so a second server with the same tool names overwrites the first. The example's closing notes ask what happens then. Add a second filesystem server rooted at `./handbook` and the model receives 32 definitions for 18 names, while all 14 filesystem names route to the second server. A request to read `research_server.py`, which sits in the project folder, now reaches the handbook server and comes back as `ENOENT: no such file or directory`.

### Step 4: Change the connected tool surface

The [interactive lab](interactive/server-config-lab.html) runs the example's merge on the recorded tool lists. Switch servers on and off, and watch the definitions per call, the characters, and which server each tool name reaches.

<!-- lab: interactive/server-config-lab.html -->

### Step 5: Inspect descriptions as model input

A reference server's definitions are text the model reads, written by someone else. The fetch server's description says: “Although originally you did not have internet access, and were advised to refuse and tell the user this, this tool now grants you internet access.” Read what a server tells your model before you connect it, and pin its version (`@modelcontextprotocol/server-filesystem@2.1.0`, `mcp-server-fetch@2026.10.28`) so an update cannot change that text unseen.

### Try it yourself

In the lab change the enabled server set and inspect the tool count and characters sent per call. Select the two-filesystem-server preset and check which server owns each duplicated name while both definitions remain visible. Then reverse those servers in the practice client configuration and repeat discovery. The advertised list and the name-to-session mapping are different structures.

### Practice notebook

Run the complete implementation from the practice material after checking the trace or calculation above. Use its stated environment for live model or server calls; recorded model choices and timings are observations, not guaranteed outputs.

- [Connecting to reference servers](../../notebook/04a_connecting_to_reference_servers.ipynb).

## Key Takeaways

- Every connected tool definition is sent on every call. Three reference servers already cost about 2,527 tokens before the question, so connect only what the assistant needs.
- Tool names must be unique across servers, because the routing dict lets a later server silently take over a name.
- Read what a third-party server tells your model before connecting it, and pin its version so an update cannot change that text unseen.

## Check yourself

<details>
<summary>1. The 04a chatbot fills two structures as it connects to each server. What does each one do?</summary>

`available_tools` holds every tool definition and goes to the model on every request. `tool_to_session` maps each tool name to the session of the server that offers it, so `process_query` knows where to send a call. One tells the model what exists; the other routes the call.

</details>

<details>
<summary>2. With filesystem, research and fetch connected, how much tool text reaches the model before the user's question, and which server dominates it?</summary>

17 definitions, 10,107 characters, about 2,527 tokens, on every call. The filesystem server's 14 tools are 8,072 characters, 80% of the total. Adding the Larkspur retriever as a fourth server would add one tool and 417 characters.

</details>

<details>
<summary>3. You add a second filesystem server rooted at the handbook folder, and reading research_server.py now fails with ENOENT. What went wrong?</summary>

`tool_to_session` is a dict, so the second server's 14 tool names overwrote the first server's routes. The model receives 32 definitions for 18 names, and every filesystem call now reaches the handbook server, where `research_server.py` does not exist. Tool names must be unique across servers.

</details>

---
*Previous: [38.3 Building an MCP client](../03_building_an_mcp_client/README.md). Next: [38.5 Prompts and resources](../05_prompts_and_resources/README.md).*
