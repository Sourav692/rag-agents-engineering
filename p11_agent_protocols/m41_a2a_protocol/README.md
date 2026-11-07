# M41 — A2A: Agent-to-Agent Protocol

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part XI · Agent Protocols: MCP & A2A** · **Level:** Advanced · **Time:** ~4 h · **Notebooks:** 4 mandatory, 0 optional

## Why it matters

MCP connects agents to tools; A2A connects agents to each other across frameworks. Together they let a RAG agent be one service in a larger multi-agent system.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [What comes back over A2A](mandatory/theory/02_a_langgraph_agent_over_a2a/interactive/a2a-exchange-lab.html) (open the file in a browser)

## Learning objectives

- Describe agents with Agent Cards and exchange tasks and messages
- Serve a LangGraph agent over A2A
- Make agents from different frameworks interoperate
- Combine MCP and A2A in an agentic RAG system

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 41.1 | A2A basics: Agent Cards, tasks, messages ([theory](mandatory/theory/01_a2a_basics_agent_cards_tasks_messages/README.md)) | [`01a_a2a_protocol_basics.ipynb`](mandatory/notebook/01a_a2a_protocol_basics.ipynb) | — |
| 41.2 | A LangGraph agent over A2A ([theory](mandatory/theory/02_a_langgraph_agent_over_a2a/README.md)) | [`02a_langgraph_agent_over_a2a.ipynb`](mandatory/notebook/02a_langgraph_agent_over_a2a.ipynb) | — |
| 41.3 | Cross-framework agent interop ([theory](mandatory/theory/03_cross_framework_agent_interop/README.md)) | [`03a_cross_framework_agent_interop.ipynb`](mandatory/notebook/03a_cross_framework_agent_interop.ipynb) | — |
| 41.4 | Capstone: agentic RAG with MCP and A2A ([theory](mandatory/theory/04_capstone_agentic_rag_with_mcp_and_a2a/README.md)) | [`mcp_a2a_agentic_rag`](projects/mcp_a2a_agentic_rag) | — |

## Hands-on lab

Agent as a service: put your agentic RAG graph behind A2A and call it from an agent built in a different framework. Details: [lab/README.md](lab/README.md).

## Key concepts

[Agent Card](mandatory/theory/01_a2a_basics_agent_cards_tasks_messages/README.md#agent-card) · [Tasks & messages](mandatory/theory/02_a_langgraph_agent_over_a2a/README.md#tasks--messages) · [Cross-framework interop](mandatory/theory/03_cross_framework_agent_interop/README.md#cross-framework-interop) · [MCP + A2A](mandatory/theory/04_capstone_agentic_rag_with_mcp_and_a2a/README.md#mcp--a2a)

## Folder layout

- `mandatory/notebook/`: the mandatory track, plus the helper files those notebooks import
- `optional/notebook/`: alternate, platform-specific, extension and exercise notebooks
- `mandatory/theory/`: the module page, its `index.html` and the pages of lessons with a mandatory notebook
- `optional/theory/`: the pages of lessons whose notebooks are all optional
- `projects/`: runnable sub-projects (for example MCP servers and clients), where the module has them
- `assets/`: images and data used by this module's notebooks, where it has them
- `lab/`: the module lab brief, its solution notebook in `solution/` and its data in `data/`

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `mandatory/notebook/01a_a2a_protocol_basics.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/05_a2a/notebooks/01_a2a_protocol_basics.ipynb` |
| `mandatory/notebook/02a_langgraph_agent_over_a2a.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/05_a2a/notebooks/02_langgraph_agent_over_a2a.ipynb` |
| `mandatory/notebook/03a_cross_framework_agent_interop.ipynb` | `ai-engineering-demystified-10-agent-protocols` | `modules/05_a2a/notebooks/03_cross_framework_agent_interop.ipynb` |
| `projects/mcp_a2a_agentic_rag` | `ai-engineering-demystified-10-agent-protocols` | `modules/05_a2a/projects/mcp_a2a_agentic_rag` |
