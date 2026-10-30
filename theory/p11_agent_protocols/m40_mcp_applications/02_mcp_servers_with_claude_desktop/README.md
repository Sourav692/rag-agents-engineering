# M40.2 Theory: MCP servers with Claude Desktop

*[M40 theory](../README.md) · Lesson 40.2 · Notebooks: [`03_mcp_servers_with_claude_desktop`](../../../../course/p11_agent_protocols/m40_mcp_applications/projects/03_mcp_servers_with_claude_desktop) (optional) · [All theory pages](../../../README.md)*

## Claude Desktop

Claude Desktop is an MCP host: it owns the model, the chat window and one client per server. You give it servers through `claude_desktop_config.json`, a map under `mcpServers` from a name to the command that starts the server. The project's config is the course's whole MCP toolbox in one file, thirteen entries:

| Launcher | Entries | What it starts |
|---|---|---|
| `uv` | 5 | The course's own servers: `weather`, `math_server`, `job_search` (40.4), `chroma_db_rag` (40.5), `research_server` (40.6) |
| `npx` | 5 | Published Node packages: `playwright`, `airbnb`, `notionApi`, `filesystem`, and `remote-research-server` through `mcp-remote` |
| `uvx` | 2 | Published Python packages: `ppt`, and `sqlite` straight from a Git URL |
| `cmd` | 1 | `excel`, as `cmd /c npx --yes @negokaz/excel-mcp-server`, which only runs on Windows |

A Larkspur entry for the handbook server looks like the course's own:

```json
"larkspur-handbook": {
  "command": "uv",
  "args": ["--directory", "/ABSOLUTE/PATH/TO/larkspur-handbook", "run", "server.py"]
}
```

What the file teaches beyond its syntax:

- **Paths are absolute, and `--directory` sets the working directory.** Every course entry ships with an `/ABSOLUTE/PATH/TO/…` placeholder to replace. The 40.4 server writes to `Path(".") / "jobs"`; `uv --directory` makes that resolve inside the project, where it would otherwise land wherever the host starts the process.
- **Secrets go in `env`, per server.** `notionApi` gets `NOTION_TOKEN` and nothing else does. `excel` sets a paging limit, `EXCEL_MCP_PAGING_CELLS_LIMIT`, to 4000 cells.
- **Some entries fetch code at launch.** `@playwright/mcp@latest` takes whatever version is current, and the `sqlite` entry installs from a Git repository each time `uvx` needs it. Pin versions for anything you depend on.
- **A remote server needs a bridge.** The config reaches the EC2 server from lesson 40.7 through `npx mcp-remote http://<EC2 address>:8000/mcp --allow-http`, a local stdio process that forwards to the remote URL. mcp-remote 0.15.2's README says `--allow-http` "should only be used in secure private networks where traffic cannot be intercepted"; here it points at a public address.

Thirteen servers also means thirteen sets of tool definitions on offer to the model; [M38](../../m38_mcp_foundations/README.md) measures what connected servers cost in tokens.

## Stdout belongs to the protocol

Over stdio, the host writes requests to the server's stdin and reads responses from its stdout, one JSON-RPC message per line. Anything else the server writes to stdout arrives in the same stream.

```mermaid
flowchart LR
    H["Host<br/>MCP client"] -- "stdin: requests" --> S["Server process"]
    S -- "stdout: JSON-RPC only" --> H
    S -- "stderr: logs" --> L["Host log"]
```

The 06 server breaks this rule. Its `main()` prints a banner before `mcp.run(transport="stdio")`, and `ingest_pdf` prints progress lines while it works. A probe with mcp 1.30.0's stdio client and a server that prints the same way:

- **Output unbuffered** (`PYTHONUNBUFFERED=1`): every stray line reached the client, which logged `Failed to parse JSONRPC message from server` with the offending text (the banner's `'LangChain Chroma Vector DB Server'` among them), dropped the line and carried on. The tool results still arrived.
- **Default buffering:** Python block-buffers stdout when it is a pipe, so the prints sat in the buffer and nothing reached the client during the short session. The bug was there and did not show.

The Python client is forgiving; another host may not be. Send logs to stderr (`print(..., file=sys.stderr)` or the `logging` module, whose default handler writes there), and keep stdout for the protocol.

---
*Previous: [40.1 Your first MCP server and a local agent](../01_your_first_mcp_server_and_a_local_agent/README.md). Next: [40.3 MCP servers for data analysis](../03_mcp_servers_for_data_analysis/README.md).*
