# Curriculum map

Module → notebook or runnable sub-project → the one thing it teaches, in learning order.

## [01 MCP foundations](../modules/01_mcp_foundations/README.md)

| Item | Learning objective |
|---|---|
| [01_chatbot_example.ipynb](../modules/01_mcp_foundations/notebooks/01_chatbot_example.ipynb) | Build a tool-using arXiv research chatbot with plain function calling: the baseline MCP improves on |
| [02_chatbot_example_openai_walkthrough.ipynb](../modules/01_mcp_foundations/notebooks/02_chatbot_example_openai_walkthrough.ipynb) | Walk through the same chatbot step by step with OpenAI's tool-calling message format |
| [03_creating_an_mcp_server.ipynb](../modules/01_mcp_foundations/notebooks/03_creating_an_mcp_server.ipynb) → [lesson4_research_server/](../modules/01_mcp_foundations/projects/lesson4_research_server/) | Turn the research tools into an MCP server with FastMCP and test it in MCP Inspector |
| [04_creating_an_mcp_client.ipynb](../modules/01_mcp_foundations/notebooks/04_creating_an_mcp_client.ipynb) → [lesson5_mcp_chatbot/](../modules/01_mcp_foundations/projects/lesson5_mcp_chatbot/) | Write an MCP client so the chatbot discovers and calls the server's tools over stdio |
| [05_connecting_to_reference_servers.ipynb](../modules/01_mcp_foundations/notebooks/05_connecting_to_reference_servers.ipynb) → [lesson6_reference_servers_chatbot/](../modules/01_mcp_foundations/projects/lesson6_reference_servers_chatbot/) | Connect one chatbot to several servers (research, fetch, filesystem) from a server config |
| [06_adding_prompt_and_resource_features.ipynb](../modules/01_mcp_foundations/notebooks/06_adding_prompt_and_resource_features.ipynb) → [lesson7_prompts_and_resources/](../modules/01_mcp_foundations/projects/lesson7_prompts_and_resources/) | Expose resources and prompt templates next to tools and use them from the client |
| [07_creating_and_deploying_remote_servers.ipynb](../modules/01_mcp_foundations/notebooks/07_creating_and_deploying_remote_servers.ipynb) → [lesson9_remote_research_server/](../modules/01_mcp_foundations/projects/lesson9_remote_research_server/) | Serve the research server over a remote transport (SSE) and deploy it |
| [wikipedia_assistant_1_tools/](../modules/01_mcp_foundations/projects/wikipedia_assistant_1_tools/) | Build a Wikipedia MCP server with tools and a LangGraph client that loads them |
| [wikipedia_assistant_2_resources/](../modules/01_mcp_foundations/projects/wikipedia_assistant_2_resources/) | Add MCP resources to the Wikipedia server |
| [wikipedia_assistant_3_prompts/](../modules/01_mcp_foundations/projects/wikipedia_assistant_3_prompts/) | Add MCP prompt templates to the Wikipedia server |

## [02 Building MCP servers](../modules/02_building_mcp_servers/README.md)

| Item | Learning objective |
|---|---|
| [01_single_server_mcp/](../modules/02_building_mcp_servers/projects/01_single_server_mcp/) | Build one MCP server with tools and a client that uses it |
| [02_single_server_mcp_with_resources/](../modules/02_building_mcp_servers/projects/02_single_server_mcp_with_resources/) | Extend that server with resources |
| [03_multi_server_mcp/](../modules/02_building_mcp_servers/projects/03_multi_server_mcp/) | Combine two servers behind one client |
| [04_databricks_apps_mcp_server/](../modules/02_building_mcp_servers/projects/04_databricks_apps_mcp_server/) | Package a FastMCP server with tools over external data and a SQL warehouse as a Databricks App |

## [03 Building MCP clients](../modules/03_building_mcp_clients/README.md)

| Item | Learning objective |
|---|---|
| [01_build_your_own_server_client/](../modules/03_building_mcp_clients/projects/01_build_your_own_server_client/) | Write a stdio MCP client twice, with the raw SDK and with the LangChain adapter, against your own terminal server |
| [02_multi_server_client/](../modules/03_building_mcp_clients/projects/02_multi_server_client/) | Manage several Dockerised servers from one client and a config file |
| [03_sse_transport_server_client/](../modules/03_building_mcp_clients/projects/03_sse_transport_server_client/) | Serve and consume MCP over SSE |
| [04_streamable_http_client/](../modules/03_building_mcp_clients/projects/04_streamable_http_client/) | Mix streamable-HTTP and stdio servers in one CLI client with an ADK agent |

## [04 MCP applications](../modules/04_mcp_applications/README.md)

| Item | Learning objective |
|---|---|
| [assets/course_intro/](../modules/04_mcp_applications/assets/course_intro/) | Set up the toolchain and get a slide-level introduction to MCP |
| [01_build_your_first_mcp_server/](../modules/04_mcp_applications/projects/01_build_your_first_mcp_server/) | Build a first FastMCP server and call it from FastMCP and raw MCP clients |
| [02_mcp_servers_and_local_agent/](../modules/04_mcp_applications/projects/02_mcp_servers_and_local_agent/) | Drive MCP servers from a local Ollama agent over stdio and HTTP |
| [03_mcp_servers_with_claude_desktop/](../modules/04_mcp_applications/projects/03_mcp_servers_with_claude_desktop/) | Use Claude Desktop as the MCP host for local and third-party servers |
| [04_mcp_servers_for_data_analysis/](../modules/04_mcp_applications/projects/04_mcp_servers_for_data_analysis/) | Analyse a workbook and produce a report through Excel/PowerPoint MCP servers |
| [05_mcp_tools_resources_and_prompts/](../modules/04_mcp_applications/projects/05_mcp_tools_resources_and_prompts/) | Design one server that offers tools, resources and prompts together |
| [06_mcp_rag_with_langchain/](../modules/04_mcp_applications/projects/06_mcp_rag_with_langchain/) | Serve retrieval over MCP and consume it from a Streamlit + LangGraph app |
| [07_research_assistant_with_mcp_and_langgraph/](../modules/04_mcp_applications/projects/07_research_assistant_with_mcp_and_langgraph/) | Combine a custom server and a third-party server in a LangGraph assistant |
| [08_deploy_mcp_server_on_ec2/](../modules/04_mcp_applications/projects/08_deploy_mcp_server_on_ec2/) | Run an MCP server over streamable HTTP on a remote host |

## [05 A2A](../modules/05_a2a/README.md)

| Item | Learning objective |
|---|---|
| [01_a2a_protocol_basics.ipynb](../modules/05_a2a/notebooks/01_a2a_protocol_basics.ipynb) | Serve and call a minimal A2A agent: Agent Card, Task, Message with `a2a-sdk` |
| [02_langgraph_agent_over_a2a.ipynb](../modules/05_a2a/notebooks/02_langgraph_agent_over_a2a.ipynb) | Put an A2A server in front of a LangGraph tool-using agent and call it as a client |
| [03_cross_framework_agent_interop.ipynb](../modules/05_a2a/notebooks/03_cross_framework_agent_interop.ipynb) | Discover agents from a registry and chain agents built differently over A2A |
| [mcp_a2a_agentic_rag/](../modules/05_a2a/projects/mcp_a2a_agentic_rag/) | Compose both protocols: A2A agents that share MCP tool servers (agentic RAG is the payload) |

## [06 ACP](../modules/06_acp/README.md)

🚧 Planned: foundations, building agents with ACP, applications. No content yet.
