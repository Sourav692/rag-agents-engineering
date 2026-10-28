# M41 — A2A: Agent-to-Agent Protocol

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part XI · Agent Protocols: MCP & A2A** · **Level:** Advanced · **Time:** ~4 h · **Notebooks:** 4 mandatory, 0 optional

## Why it matters

MCP connects agents to tools; A2A connects agents to each other across frameworks. Together they let a RAG agent be one service in a larger multi-agent system.

## Learning objectives

- Describe agents with Agent Cards and exchange tasks and messages
- Serve a LangGraph agent over A2A
- Make agents from different frameworks interoperate
- Combine MCP and A2A in an agentic RAG system

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 41.1 | A2A basics: Agent Cards, tasks, messages | [`01a_a2a_protocol_basics.ipynb`](notebooks/01a_a2a_protocol_basics.ipynb) | — |
| 41.2 | A LangGraph agent over A2A | [`02a_langgraph_agent_over_a2a.ipynb`](notebooks/02a_langgraph_agent_over_a2a.ipynb) | — |
| 41.3 | Cross-framework agent interop | [`03a_cross_framework_agent_interop.ipynb`](notebooks/03a_cross_framework_agent_interop.ipynb) | — |
| 41.4 | Capstone: agentic RAG with MCP and A2A | [`mcp_a2a_agentic_rag`](projects/mcp_a2a_agentic_rag) | — |

## Hands-on lab

Agent as a service: put your agentic RAG graph behind A2A and call it from an agent built in a different framework. Details: [lab/README.md](lab/README.md).

## Key concepts

Agent Card · Tasks & messages · Cross-framework interop · MCP + A2A

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
| `notebooks/01a_a2a_protocol_basics.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/05_a2a/notebooks/01_a2a_protocol_basics.ipynb` |
| `notebooks/02a_langgraph_agent_over_a2a.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/05_a2a/notebooks/02_langgraph_agent_over_a2a.ipynb` |
| `notebooks/03a_cross_framework_agent_interop.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/05_a2a/notebooks/03_cross_framework_agent_interop.ipynb` |
| `projects/mcp_a2a_agentic_rag` | `ai-engineering-demystified-10-agent-protocols` | `modules/05_a2a/projects/mcp_a2a_agentic_rag` |
