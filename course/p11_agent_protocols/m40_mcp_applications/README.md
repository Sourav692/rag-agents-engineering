# M40 — MCP Applications & RAG over MCP

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part XI · Agent Protocols: MCP & A2A** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 5 mandatory, 3 optional

## Why it matters

MCP pays off when real applications share it: local agents, Claude Desktop, data analysis, retrieval over MCP and a LangGraph research assistant.

## Theory

Read the [theory page](../../../theory/p11_agent_protocols/m40_mcp_applications/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p11_agent_protocols/m40_mcp_applications/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [One server, three clients](../../../theory/p11_agent_protocols/m40_mcp_applications/06_research_assistant_with_mcp_and_langgraph/interactive/session-lifetime-lab.html) (open the file in a browser)

## Learning objectives

- Run MCP servers behind a local agent and in Claude Desktop
- Combine tools, resources and prompts in one server
- Serve retrieval over MCP with LangChain
- Build a research assistant with MCP and LangGraph, and deploy a server to EC2

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 40.1 | Your first MCP server and a local agent ([theory](../../../theory/p11_agent_protocols/m40_mcp_applications/01_your_first_mcp_server_and_a_local_agent/README.md)) | [`01_build_your_first_mcp_server`](projects/01_build_your_first_mcp_server)<br>[`02_mcp_servers_and_local_agent`](projects/02_mcp_servers_and_local_agent) | — |
| 40.2 | MCP servers with Claude Desktop *(optional lesson)* ([theory](../../../theory/p11_agent_protocols/m40_mcp_applications/02_mcp_servers_with_claude_desktop/README.md)) | — | [`03_mcp_servers_with_claude_desktop`](projects/03_mcp_servers_with_claude_desktop) *(platform-specific)* |
| 40.3 | MCP servers for data analysis *(optional lesson)* ([theory](../../../theory/p11_agent_protocols/m40_mcp_applications/03_mcp_servers_for_data_analysis/README.md)) | — | [`04_mcp_servers_for_data_analysis`](projects/04_mcp_servers_for_data_analysis) *(extension)* |
| 40.4 | Tools, resources and prompts together ([theory](../../../theory/p11_agent_protocols/m40_mcp_applications/04_tools_resources_and_prompts_together/README.md)) | [`05_mcp_tools_resources_and_prompts`](projects/05_mcp_tools_resources_and_prompts) | — |
| 40.5 | RAG over MCP with LangChain ([theory](../../../theory/p11_agent_protocols/m40_mcp_applications/05_rag_over_mcp_with_langchain/README.md)) | [`06_mcp_rag_with_langchain`](projects/06_mcp_rag_with_langchain) | — |
| 40.6 | Research assistant with MCP and LangGraph ([theory](../../../theory/p11_agent_protocols/m40_mcp_applications/06_research_assistant_with_mcp_and_langgraph/README.md)) | [`07_research_assistant_with_mcp_and_langgraph`](projects/07_research_assistant_with_mcp_and_langgraph) | — |
| 40.7 | Deploying an MCP server on EC2 *(optional lesson)* ([theory](../../../theory/p11_agent_protocols/m40_mcp_applications/07_deploying_an_mcp_server_on_ec2/README.md)) | — | [`08_deploy_mcp_server_on_ec2`](projects/08_deploy_mcp_server_on_ec2) *(platform-specific)* |

## Hands-on lab

Shared retrieval: connect the RAG-over-MCP server to two different clients (a LangGraph agent and Claude Desktop or a local agent) and compare answers. Details: [lab/README.md](lab/README.md).

## Key concepts

[MCP + LangGraph](../../../theory/p11_agent_protocols/m40_mcp_applications/06_research_assistant_with_mcp_and_langgraph/README.md#mcp--langgraph) · [RAG over MCP](../../../theory/p11_agent_protocols/m40_mcp_applications/05_rag_over_mcp_with_langchain/README.md#rag-over-mcp) · [Claude Desktop](../../../theory/p11_agent_protocols/m40_mcp_applications/02_mcp_servers_with_claude_desktop/README.md#claude-desktop) · [Deployment](../../../theory/p11_agent_protocols/m40_mcp_applications/07_deploying_an_mcp_server_on_ec2/README.md#deployment)

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
