# M39 — Building MCP Servers & Clients

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part XI · Agent Protocols: MCP & A2A** · **Level:** Advanced · **Time:** ~4 h · **Notebooks:** 7 mandatory, 3 optional

## Why it matters

Production MCP work means several servers, your own clients and the right transport. These sub-projects are runnable code rather than notebooks.

## Theory

Read the [theory page](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Sessions on the wire](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/04_your_own_client_and_a_multi_server_client/interactive/session-wire-lab.html) (open the file in a browser)

## Learning objectives

- Build single-server MCP projects with tools and resources
- Combine several servers behind one client
- Write your own MCP client
- Use SSE and streamable HTTP transports

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 39.1 | Single-server MCP, with resources ([theory](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/01_single_server_mcp_with_resources/README.md)) | [`01_single_server_mcp`](projects/01_single_server_mcp)<br>[`02_single_server_mcp_with_resources`](projects/02_single_server_mcp_with_resources) | — |
| 39.2 | Multi-server MCP ([theory](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/02_multi_server_mcp/README.md)) | [`03_multi_server_mcp`](projects/03_multi_server_mcp) | — |
| 39.3 | An MCP server as a Databricks App *(optional lesson)* | — | [`04_databricks_apps_mcp_server`](projects/04_databricks_apps_mcp_server) *(platform-specific)* |
| 39.4 | Your own client and a multi-server client ([theory](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/04_your_own_client_and_a_multi_server_client/README.md)) | [`01_build_your_own_server_client`](projects/01_build_your_own_server_client)<br>[`02_multi_server_client`](projects/02_multi_server_client) | — |
| 39.5 | Transports: SSE and streamable HTTP ([theory](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/05_transports_sse_and_streamable_http/README.md)) | [`03_sse_transport_server_client`](projects/03_sse_transport_server_client)<br>[`04_streamable_http_client`](projects/04_streamable_http_client) | — |
| 39.6 | Licence and references for the client projects *(optional lesson)* | — | [`License`](projects/License) *(extension)*<br>[`Reference_link.md`](projects/Reference_link.md) *(extension)* |

## Hands-on lab

Two servers, one client: put your retriever and a web-search tool in separate MCP servers and route between them from one client. Details: [lab/README.md](lab/README.md).

## Key concepts

[Multi-server](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/02_multi_server_mcp/README.md#multi-server) · [Client sessions](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/04_your_own_client_and_a_multi_server_client/README.md#client-sessions) · [SSE](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/05_transports_sse_and_streamable_http/README.md#sse) · [Streamable HTTP](../../../theory/p11_agent_protocols/m39_building_mcp_servers_and_clients/05_transports_sse_and_streamable_http/README.md#streamable-http)

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `projects/` — runnable sub-projects (e.g. MCP servers and clients), where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `projects/01_single_server_mcp` | `ai-engineering-demystified-10-agent-protocols` | `modules/02_building_mcp_servers/projects/01_single_server_mcp` |
| `projects/02_single_server_mcp_with_resources` | `ai-engineering-demystified-10-agent-protocols` | `modules/02_building_mcp_servers/projects/02_single_server_mcp_with_resources` |
| `projects/03_multi_server_mcp` | `ai-engineering-demystified-10-agent-protocols` | `modules/02_building_mcp_servers/projects/03_multi_server_mcp` |
| `projects/04_databricks_apps_mcp_server` | `ai-engineering-demystified-10-agent-protocols` | `modules/02_building_mcp_servers/projects/04_databricks_apps_mcp_server` |
| `projects/01_build_your_own_server_client` | `ai-engineering-demystified-10-agent-protocols` | `modules/03_building_mcp_clients/projects/01_build_your_own_server_client` |
| `projects/02_multi_server_client` | `ai-engineering-demystified-10-agent-protocols` | `modules/03_building_mcp_clients/projects/02_multi_server_client` |
| `projects/03_sse_transport_server_client` | `ai-engineering-demystified-10-agent-protocols` | `modules/03_building_mcp_clients/projects/03_sse_transport_server_client` |
| `projects/04_streamable_http_client` | `ai-engineering-demystified-10-agent-protocols` | `modules/03_building_mcp_clients/projects/04_streamable_http_client` |
| `projects/License` | `ai-engineering-demystified-10-agent-protocols` | `modules/03_building_mcp_clients/projects/License` |
| `projects/Reference_link.md` | `ai-engineering-demystified-10-agent-protocols` | `modules/03_building_mcp_clients/projects/Reference_link.md` |
