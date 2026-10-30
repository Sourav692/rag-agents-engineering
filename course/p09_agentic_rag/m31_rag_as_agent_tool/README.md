# M31 — RAG as an Agent Tool

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part IX · Agentic & Self-Correcting RAG** · **Level:** Advanced · **Time:** ~3 h · **Notebooks:** 1 mandatory, 2 optional

## Why it matters

In agent systems retrieval is one tool among many, and the agent decides when to call it. Tool design (name, description, inputs) now matters as much as retrieval quality.

## Theory

Read the [theory page](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Tool descriptions and routing](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/01_rag_as_a_tool_inside_a_langgraph_agent/interactive/tool-routing-lab.html) (open the file in a browser)

## Learning objectives

- Expose a RAG pipeline as a tool the agent chooses to call in LangGraph
- Build a managed RAG agent (datastore, parser, reranker, grounded LM) with the Contextual AI SDK
- Ship a LlamaIndex Wikipedia agent with a Chainlit chat UI

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 31.1 | RAG as a tool inside a LangGraph agent ([theory](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/01_rag_as_a_tool_inside_a_langgraph_agent/README.md)) | [`01a_rag_as_tool_in_agents.ipynb`](notebooks/01a_rag_as_tool_in_agents.ipynb) | — |
| 31.2 | Managed RAG platforms: Contextual AI *(optional lesson)* ([theory](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/02_managed_rag_platforms_contextual_ai/README.md)) | — | [`02a_agentic_rag_contextual_ai.ipynb`](optional/02a_agentic_rag_contextual_ai.ipynb) *(platform-specific)* |
| 31.3 | Exercise: LlamaIndex Wikipedia agent with Chainlit *(optional lesson)* ([theory](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/03_exercise_llamaindex_wikipedia_agent_with_chainlit/README.md)) | — | [`03a_llamaindex_wikipedia_agent`](optional/03a_llamaindex_wikipedia_agent) *(extension)* |

## Hands-on lab

Two-tool agent: give an agent a private-docs RAG tool and a web-search tool, and tune the tool descriptions until it picks the right one on 20 mixed questions. Details: [lab/README.md](lab/README.md).

## Key concepts

[Tool descriptions](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/01_rag_as_a_tool_inside_a_langgraph_agent/README.md#tool-descriptions) · [Agent-decided retrieval](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/01_rag_as_a_tool_inside_a_langgraph_agent/README.md#agent-decided-retrieval) · [Managed RAG](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/02_managed_rag_platforms_contextual_ai/README.md#managed-rag) · [Chat UI](../../../theory/p09_agentic_rag/m31_rag_as_agent_tool/03_exercise_llamaindex_wikipedia_agent_with_chainlit/README.md#chat-ui)

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
| `notebooks/01a_rag_as_tool_in_agents.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/05_rag_as_an_agent_tool/notebooks/01_rag_as_tool_in_agents.ipynb` |
| `optional/02a_agentic_rag_contextual_ai.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/05_rag_as_an_agent_tool/notebooks/02_agentic_rag_contextual_ai.ipynb` |
| `optional/03a_llamaindex_wikipedia_agent` | `ai-engineering-demystified-09-advanced-rag` | `modules/05_rag_as_an_agent_tool/exercises/llamaindex_wikipedia_agent` |
