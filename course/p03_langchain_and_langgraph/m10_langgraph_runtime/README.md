# M10 — LangGraph Runtime: Persistence, HITL & Streaming

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part III · LangChain & LangGraph Fundamentals** · **Level:** Foundation · **Time:** ~4 h · **Notebooks:** 9 mandatory, 0 optional

## Why it matters

Grade-and-retry loops, human approval, conversation threads and multi-agent teams need checkpoints, interrupts, subgraphs, streaming and bounded cycles.

## Learning objectives

- Persist graph state with checkpointers, threads and branching
- Pause for human input with interrupt() and resume
- Compose subgraphs with state transformation
- Stream updates and messages, retry failed nodes, and bound loops

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 10.1 | Checkpointing and threads | [`01a_Checkpointing.ipynb`](notebooks/01a_Checkpointing.ipynb) | — |
| 10.2 | Interrupts and human-in-the-loop | [`02a_HITL_Mechanics.ipynb`](notebooks/02a_HITL_Mechanics.ipynb)<br>[`02b_LangGraph_Interrupt_Primitive.ipynb`](notebooks/02b_LangGraph_Interrupt_Primitive.ipynb)<br>[`02c_HITL_Patterns.ipynb`](notebooks/02c_HITL_Patterns.ipynb) | — |
| 10.3 | Subgraphs | [`03a_Subgraphs.ipynb`](notebooks/03a_Subgraphs.ipynb) | — |
| 10.4 | Async and streaming | [`04a_Async_and_Streaming.ipynb`](notebooks/04a_Async_and_Streaming.ipynb) | — |
| 10.5 | Retry policies and bounded cycles | [`05a_Retries.ipynb`](notebooks/05a_Retries.ipynb)<br>[`05b_Cycles_and_Loops.ipynb`](notebooks/05b_Cycles_and_Loops.ipynb) | — |
| 10.6 | State management in practice | [`06a_LangGraph_State_Management.ipynb`](notebooks/06a_LangGraph_State_Management.ipynb) | — |

## Hands-on lab

Approval loop: add a checkpointer and an interrupt before the answer node of your M09 graph, resume it after approval, and stream the steps. Details: [lab/README.md](lab/README.md).

## Key concepts

Checkpointer · interrupt() · Subgraphs · Streaming modes

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
| `notebooks/01a_Checkpointing.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/05_checkpointing/notebooks/01_Checkpointing.ipynb` |
| `notebooks/02a_HITL_Mechanics.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/06_interrupts_and_human_in_the_loop/notebooks/01_HITL_Mechanics.ipynb` |
| `notebooks/02b_LangGraph_Interrupt_Primitive.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/06_interrupts_and_human_in_the_loop/notebooks/02_LangGraph_Interrupt_Primitive.ipynb` |
| `notebooks/02c_HITL_Patterns.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/06_interrupts_and_human_in_the_loop/notebooks/03_HITL_Patterns.ipynb` |
| `notebooks/03a_Subgraphs.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/08_subgraphs/notebooks/01_Subgraphs.ipynb` |
| `notebooks/04a_Async_and_Streaming.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/09_async_and_streaming/notebooks/01_Async_and_Streaming.ipynb` |
| `notebooks/05a_Retries.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/10_retry_policies/notebooks/01_Retries.ipynb` |
| `notebooks/05b_Cycles_and_Loops.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/11_cycles_and_loops/notebooks/01_Cycles_and_Loops.ipynb` |
| `notebooks/06a_LangGraph_State_Management.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/12_state_management_in_practice/notebooks/01_LangGraph_State_Management.ipynb` |
