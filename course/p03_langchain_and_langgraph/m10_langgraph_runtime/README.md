# M10 — LangGraph Runtime: Persistence, HITL & Streaming

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part III · LangChain & LangGraph Fundamentals** · **Level:** Foundation · **Time:** ~4 h · **Notebooks:** 9 mandatory, 0 optional

## Why it matters

Grade-and-retry loops, human approval, conversation threads and multi-agent teams need checkpoints, interrupts, subgraphs, streaming and bounded cycles.

## Theory

Read the [theory page](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [What runs twice on resume](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/06_state_management_in_practice/interactive/resume-side-effects-lab.html) (open the file in a browser)

## Learning objectives

- Persist graph state with checkpointers, threads and branching
- Pause for human input with interrupt() and resume
- Compose subgraphs with state transformation
- Stream updates and messages, retry failed nodes, and bound loops

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 10.1 | Checkpointing and threads ([theory](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/01_checkpointing_and_threads/README.md)) | [`01a_Checkpointing.ipynb`](notebooks/01a_Checkpointing.ipynb) | — |
| 10.2 | Interrupts and human-in-the-loop ([theory](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/02_interrupts_and_human_in_the_loop/README.md)) | [`02a_HITL_Mechanics.ipynb`](notebooks/02a_HITL_Mechanics.ipynb)<br>[`02b_LangGraph_Interrupt_Primitive.ipynb`](notebooks/02b_LangGraph_Interrupt_Primitive.ipynb)<br>[`02c_HITL_Patterns.ipynb`](notebooks/02c_HITL_Patterns.ipynb) | — |
| 10.3 | Subgraphs ([theory](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/03_subgraphs/README.md)) | [`03a_Subgraphs.ipynb`](notebooks/03a_Subgraphs.ipynb) | — |
| 10.4 | Async and streaming ([theory](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/04_async_and_streaming/README.md)) | [`04a_Async_and_Streaming.ipynb`](notebooks/04a_Async_and_Streaming.ipynb) | — |
| 10.5 | Retry policies and bounded cycles ([theory](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/05_retry_policies_and_bounded_cycles/README.md)) | [`05a_Retries.ipynb`](notebooks/05a_Retries.ipynb)<br>[`05b_Cycles_and_Loops.ipynb`](notebooks/05b_Cycles_and_Loops.ipynb) | — |
| 10.6 | State management in practice ([theory](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/06_state_management_in_practice/README.md)) | [`06a_LangGraph_State_Management.ipynb`](notebooks/06a_LangGraph_State_Management.ipynb) | — |

## Hands-on lab

Approval loop: add a checkpointer and an interrupt before the answer node of your M09 graph, resume it after approval, and stream the steps. Details: [lab/README.md](lab/README.md).

## Key concepts

[Checkpointer](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/01_checkpointing_and_threads/README.md#checkpointer) · [interrupt()](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/02_interrupts_and_human_in_the_loop/README.md#interrupt) · [Subgraphs](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/03_subgraphs/README.md#subgraphs) · [Streaming modes](../../../theory/p03_langchain_and_langgraph/m10_langgraph_runtime/04_async_and_streaming/README.md#streaming-modes)

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
