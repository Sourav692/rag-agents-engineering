# M09 — LangGraph Core: Graphs, State & Control Flow

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part III · LangChain & LangGraph Fundamentals** · **Level:** Foundation · **Time:** ~4 h · **Notebooks:** 10 mandatory, 0 optional

## Why it matters

Agentic RAG, memory and multi-agent systems are all LangGraph graphs. This module covers the core: state, nodes, edges, reducers and routing.

## Theory

Read the [theory page](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Reducers and the message list](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/01_state_graphs_and_reducers/interactive/reducer-lab.html) (open the file in a browser)

## Learning objectives

- Build a StateGraph with nodes, edges and reducers, including MessagesState
- Route with conditional edges and put a chat model inside a node
- Choose a state schema (TypedDict, dataclass, Pydantic) and validate it
- Use node signatures, runtime context, Command, input/output schemas and configuration

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 9.1 | State, graphs and reducers ([theory](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/01_state_graphs_and_reducers/README.md)) | [`01a_State_and_Graph_Basics.ipynb`](notebooks/01a_State_and_Graph_Basics.ipynb)<br>[`01b_MessagesState.ipynb`](notebooks/01b_MessagesState.ipynb) | — |
| 9.2 | Conditional edges and LLM nodes ([theory](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/02_conditional_edges_and_llm_nodes/README.md)) | [`02a_Conditional_Routing.ipynb`](notebooks/02a_Conditional_Routing.ipynb)<br>[`02b_LLM_Powered_Chatbot.ipynb`](notebooks/02b_LLM_Powered_Chatbot.ipynb) | — |
| 9.3 | State schemas and validation ([theory](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/03_state_schemas_and_validation/README.md)) | [`03a_Different_Graph_States.ipynb`](notebooks/03a_Different_Graph_States.ipynb)<br>[`03b_Pydantic_State_Validation.ipynb`](notebooks/03b_Pydantic_State_Validation.ipynb) | — |
| 9.4 | Nodes, runtime context and Command ([theory](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/04_nodes_runtime_context_and_command/README.md)) | [`04a_Node_Patterns.ipynb`](notebooks/04a_Node_Patterns.ipynb)<br>[`04b_Runtime_Context.ipynb`](notebooks/04b_Runtime_Context.ipynb)<br>[`04c_Command_Objects.ipynb`](notebooks/04c_Command_Objects.ipynb) | — |
| 9.5 | Input/output schemas and configuration ([theory](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/05_input_output_schemas_and_configuration/README.md)) | [`05a_Advanced_State.ipynb`](notebooks/05a_Advanced_State.ipynb) | — |

## Hands-on lab

First graph: build a graph that classifies a question, routes it to one of two nodes, and returns a structured answer. Details: [lab/README.md](lab/README.md).

## Key concepts

[StateGraph](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/01_state_graphs_and_reducers/README.md#stategraph) · [Reducers](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/01_state_graphs_and_reducers/README.md#reducers) · [Conditional edges](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/02_conditional_edges_and_llm_nodes/README.md#conditional-edges) · [Command](../../../theory/p03_langchain_and_langgraph/m09_langgraph_core/04_nodes_runtime_context_and_command/README.md#command)

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
| `notebooks/01a_State_and_Graph_Basics.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/01_graphs_state_and_reducers/notebooks/01_State_and_Graph_Basics.ipynb` |
| `notebooks/01b_MessagesState.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/01_graphs_state_and_reducers/notebooks/02_MessagesState.ipynb` |
| `notebooks/02a_Conditional_Routing.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/02_conditional_edges_and_llm_nodes/notebooks/01_Conditional_Routing.ipynb` |
| `notebooks/02b_LLM_Powered_Chatbot.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/02_conditional_edges_and_llm_nodes/notebooks/02_LLM_Powered_Chatbot.ipynb` |
| `notebooks/03a_Different_Graph_States.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/03_state_schemas/notebooks/01_Different_Graph_States.ipynb` |
| `notebooks/03b_Pydantic_State_Validation.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/03_state_schemas/notebooks/02_Pydantic_State_Validation.ipynb` |
| `notebooks/04a_Node_Patterns.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/04_nodes_runtime_context_and_commands/notebooks/01_Node_Patterns.ipynb` |
| `notebooks/04b_Runtime_Context.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/04_nodes_runtime_context_and_commands/notebooks/02_Runtime_Context.ipynb` |
| `notebooks/04c_Command_Objects.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/04_nodes_runtime_context_and_commands/notebooks/03_Command_Objects.ipynb` |
| `notebooks/05a_Advanced_State.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/07_input_output_schemas_and_configuration/notebooks/01_Advanced_State.ipynb` |
