# M40 — MCP Applications & RAG over MCP

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part XI · Agent Protocols: MCP & A2A** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 5 mandatory, 3 optional

## Why it matters

MCP pays off when real applications share it: local agents, Claude Desktop, data analysis, retrieval over MCP and a LangGraph research assistant.

## Learning objectives

- Run MCP servers behind a local agent and in Claude Desktop
- Combine tools, resources and prompts in one server
- Serve retrieval over MCP with LangChain
- Build a research assistant with MCP and LangGraph, and deploy a server to EC2

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 40.1 | Your first MCP server and a local agent | [`01_build_your_first_mcp_server`](projects/01_build_your_first_mcp_server)<br>[`02_mcp_servers_and_local_agent`](projects/02_mcp_servers_and_local_agent) | — |
| 40.2 | MCP servers with Claude Desktop *(optional lesson)* | — | [`03_mcp_servers_with_claude_desktop`](projects/03_mcp_servers_with_claude_desktop) *(platform-specific)* |
| 40.3 | MCP servers for data analysis *(optional lesson)* | — | [`04_mcp_servers_for_data_analysis`](projects/04_mcp_servers_for_data_analysis) *(extension)* |
| 40.4 | Tools, resources and prompts together | [`05_mcp_tools_resources_and_prompts`](projects/05_mcp_tools_resources_and_prompts) | — |
| 40.5 | RAG over MCP with LangChain | [`06_mcp_rag_with_langchain`](projects/06_mcp_rag_with_langchain) | — |
| 40.6 | Research assistant with MCP and LangGraph | [`07_research_assistant_with_mcp_and_langgraph`](projects/07_research_assistant_with_mcp_and_langgraph) | — |
| 40.7 | Deploying an MCP server on EC2 *(optional lesson)* | — | [`08_deploy_mcp_server_on_ec2`](projects/08_deploy_mcp_server_on_ec2) *(platform-specific)* |

## Hands-on lab

Shared retrieval: connect the RAG-over-MCP server to two different clients (a LangGraph agent and Claude Desktop or a local agent) and compare answers. Details: [lab/README.md](lab/README.md).

## Key concepts

MCP + LangGraph · RAG over MCP · Claude Desktop · Deployment

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
| `projects/01_build_your_first_mcp_server` | `ai-engineering-demystified-10-agent-protocols` | `modules/04_mcp_applications/projects/01_build_your_first_mcp_server` |
| `projects/02_mcp_servers_and_local_agent` | `ai-engineering-demystified-10-agent-protocols` | `modules/04_mcp_applications/projects/02_mcp_servers_and_local_agent` |
| `projects/03_mcp_servers_with_claude_desktop` | `ai-engineering-demystified-10-agent-protocols` | `modules/04_mcp_applications/projects/03_mcp_servers_with_claude_desktop` |
| `projects/04_mcp_servers_for_data_analysis` | `ai-engineering-demystified-10-agent-protocols` | `modules/04_mcp_applications/projects/04_mcp_servers_for_data_analysis` |
| `projects/05_mcp_tools_resources_and_prompts` | `ai-engineering-demystified-10-agent-protocols` | `modules/04_mcp_applications/projects/05_mcp_tools_resources_and_prompts` |
| `projects/06_mcp_rag_with_langchain` | `ai-engineering-demystified-10-agent-protocols` | `modules/04_mcp_applications/projects/06_mcp_rag_with_langchain` |
| `projects/07_research_assistant_with_mcp_and_langgraph` | `ai-engineering-demystified-10-agent-protocols` | `modules/04_mcp_applications/projects/07_research_assistant_with_mcp_and_langgraph` |
| `projects/08_deploy_mcp_server_on_ec2` | `ai-engineering-demystified-10-agent-protocols` | `modules/04_mcp_applications/projects/08_deploy_mcp_server_on_ec2` |
