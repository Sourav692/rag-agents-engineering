# M38 — MCP Foundations

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part XI · Agent Protocols: MCP & A2A** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 11 mandatory, 4 optional

## Why it matters

The Model Context Protocol (MCP) is a standard way to expose tools, resources and prompts to any agent. A retriever behind an MCP server can be reused by every agent and client you build.

## Theory

Read the [theory page](../../../theory/p11_agent_protocols/m38_mcp_foundations/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p11_agent_protocols/m38_mcp_foundations/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Server config lab](../../../theory/p11_agent_protocols/m38_mcp_foundations/04_connecting_to_reference_servers/interactive/server-config-lab.html) (open the file in a browser)

## Learning objectives

- Go from a tool-calling chatbot to an MCP server and client
- Connect to reference servers
- Expose prompts and resources as well as tools
- Create and deploy a remote MCP server

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 38.1 | From a tool-calling chatbot to MCP ([theory](../../../theory/p11_agent_protocols/m38_mcp_foundations/01_from_a_tool_calling_chatbot_to_mcp/README.md)) | [`01a_chatbot_example.ipynb`](notebooks/01a_chatbot_example.ipynb) | [`01b_chatbot_example_openai_walkthrough.ipynb`](optional/01b_chatbot_example_openai_walkthrough.ipynb) *(alternate)* |
| 38.2 | Building an MCP server ([theory](../../../theory/p11_agent_protocols/m38_mcp_foundations/02_building_an_mcp_server/README.md)) | [`02a_creating_an_mcp_server.ipynb`](notebooks/02a_creating_an_mcp_server.ipynb)<br>[`lesson4_research_server`](projects/lesson4_research_server) | — |
| 38.3 | Building an MCP client ([theory](../../../theory/p11_agent_protocols/m38_mcp_foundations/03_building_an_mcp_client/README.md)) | [`03a_creating_an_mcp_client.ipynb`](notebooks/03a_creating_an_mcp_client.ipynb)<br>[`lesson5_mcp_chatbot`](projects/lesson5_mcp_chatbot) | — |
| 38.4 | Connecting to reference servers ([theory](../../../theory/p11_agent_protocols/m38_mcp_foundations/04_connecting_to_reference_servers/README.md)) | [`04a_connecting_to_reference_servers.ipynb`](notebooks/04a_connecting_to_reference_servers.ipynb)<br>[`lesson6_reference_servers_chatbot`](projects/lesson6_reference_servers_chatbot) | — |
| 38.5 | Prompts and resources ([theory](../../../theory/p11_agent_protocols/m38_mcp_foundations/05_prompts_and_resources/README.md)) | [`05a_adding_prompt_and_resource_features.ipynb`](notebooks/05a_adding_prompt_and_resource_features.ipynb)<br>[`lesson7_prompts_and_resources`](projects/lesson7_prompts_and_resources) | — |
| 38.6 | Remote servers and deployment ([theory](../../../theory/p11_agent_protocols/m38_mcp_foundations/06_remote_servers_and_deployment/README.md)) | [`06a_creating_and_deploying_remote_servers.ipynb`](notebooks/06a_creating_and_deploying_remote_servers.ipynb)<br>[`lesson9_remote_research_server`](projects/lesson9_remote_research_server) | — |
| 38.7 | Labs: Wikipedia assistant with tools, resources and prompts *(optional lesson)* | — | [`wikipedia_assistant_1_tools`](projects/wikipedia_assistant_1_tools) *(extension)*<br>[`wikipedia_assistant_2_resources`](projects/wikipedia_assistant_2_resources) *(extension)*<br>[`wikipedia_assistant_3_prompts`](projects/wikipedia_assistant_3_prompts) *(extension)* |

## Hands-on lab

Retriever over MCP: expose your Part VII retriever as an MCP tool and call it from an MCP client chatbot. Details: [lab/README.md](lab/README.md).

## Key concepts

[MCP server / client](../../../theory/p11_agent_protocols/m38_mcp_foundations/03_building_an_mcp_client/README.md#mcp-server--client) · [Tools, resources, prompts](../../../theory/p11_agent_protocols/m38_mcp_foundations/05_prompts_and_resources/README.md#tools-resources-prompts) · [Reference servers](../../../theory/p11_agent_protocols/m38_mcp_foundations/04_connecting_to_reference_servers/README.md#reference-servers) · [Remote transport](../../../theory/p11_agent_protocols/m38_mcp_foundations/06_remote_servers_and_deployment/README.md#remote-transport)

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
| `notebooks/01a_chatbot_example.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/notebooks/01_chatbot_example.ipynb` |
| `optional/01b_chatbot_example_openai_walkthrough.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/notebooks/02_chatbot_example_openai_walkthrough.ipynb` |
| `notebooks/02a_creating_an_mcp_server.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/notebooks/03_creating_an_mcp_server.ipynb` |
| `projects/lesson4_research_server` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/projects/lesson4_research_server` |
| `notebooks/03a_creating_an_mcp_client.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/notebooks/04_creating_an_mcp_client.ipynb` |
| `projects/lesson5_mcp_chatbot` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/projects/lesson5_mcp_chatbot` |
| `notebooks/04a_connecting_to_reference_servers.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/notebooks/05_connecting_to_reference_servers.ipynb` |
| `projects/lesson6_reference_servers_chatbot` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/projects/lesson6_reference_servers_chatbot` |
| `notebooks/05a_adding_prompt_and_resource_features.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/notebooks/06_adding_prompt_and_resource_features.ipynb` |
| `projects/lesson7_prompts_and_resources` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/projects/lesson7_prompts_and_resources` |
| `notebooks/06a_creating_and_deploying_remote_servers.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/notebooks/07_creating_and_deploying_remote_servers.ipynb` |
| `projects/lesson9_remote_research_server` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/projects/lesson9_remote_research_server` |
| `projects/wikipedia_assistant_1_tools` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/projects/wikipedia_assistant_1_tools` |
| `projects/wikipedia_assistant_2_resources` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/projects/wikipedia_assistant_2_resources` |
| `projects/wikipedia_assistant_3_prompts` | `ai-engineering-demystified-10-agent-protocols` | `modules/01_mcp_foundations/projects/wikipedia_assistant_3_prompts` |
