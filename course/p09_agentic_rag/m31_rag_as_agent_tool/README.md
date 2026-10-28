# M31 — RAG as an Agent Tool

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part IX · Agentic & Self-Correcting RAG** · **Level:** Advanced · **Time:** ~3 h · **Notebooks:** 1 mandatory, 2 optional

## Why it matters

In agent systems retrieval is one tool among many, and the agent decides when to call it. Tool design (name, description, inputs) now matters as much as retrieval quality.

## Learning objectives

- Expose a RAG pipeline as a tool the agent chooses to call in LangGraph
- Build a managed RAG agent (datastore, parser, reranker, grounded LM) with the Contextual AI SDK
- Ship a LlamaIndex Wikipedia agent with a Chainlit chat UI

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 31.1 | RAG as a tool inside a LangGraph agent | [`01a_rag_as_tool_in_agents.ipynb`](notebooks/01a_rag_as_tool_in_agents.ipynb) | — |
| 31.2 | Managed RAG platforms: Contextual AI *(optional lesson)* | — | [`02a_agentic_rag_contextual_ai.ipynb`](optional/02a_agentic_rag_contextual_ai.ipynb) *(platform-specific)* |
| 31.3 | Exercise: LlamaIndex Wikipedia agent with Chainlit *(optional lesson)* | — | [`03a_llamaindex_wikipedia_agent`](optional/03a_llamaindex_wikipedia_agent) *(extension)* |

## Hands-on lab

Two-tool agent: give an agent a private-docs RAG tool and a web-search tool, and tune the tool descriptions until it picks the right one on 20 mixed questions. Details: [lab/README.md](lab/README.md).

## Key concepts

Tool descriptions · Agent-decided retrieval · Managed RAG · Chat UI

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
