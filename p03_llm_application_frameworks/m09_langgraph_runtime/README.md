# M09 — LangGraph Runtime: Persistence, HITL & Streaming

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part III · LLM Application Frameworks: LangChain & LangGraph** · **Level:** Foundation · **Time:** ~4 h · **Notebooks:** 9 mandatory, 0 optional

## Why it matters

Grade-and-retry loops, human approval, conversation threads and multi-agent teams need checkpoints, interrupts, subgraphs, streaming and bounded cycles.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [What runs twice on resume](mandatory/theory/06_state_management_in_practice/interactive/resume-side-effects-lab.html) (open the file in a browser)

## Learning objectives

- Persist graph state with checkpointers, threads and branching
- Pause for human input with interrupt() and resume
- Compose subgraphs with state transformation
- Stream updates and messages, retry failed nodes, and bound loops

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 9.1 | Checkpointing and threads ([theory](mandatory/theory/01_checkpointing_and_threads/README.md)) | [`01a_Checkpointing.ipynb`](mandatory/notebook/01a_Checkpointing.ipynb) | — |
| 9.2 | Interrupts and human-in-the-loop ([theory](mandatory/theory/02_interrupts_and_human_in_the_loop/README.md)) | [`02a_HITL_Mechanics.ipynb`](mandatory/notebook/02a_HITL_Mechanics.ipynb)<br>[`02b_LangGraph_Interrupt_Primitive.ipynb`](mandatory/notebook/02b_LangGraph_Interrupt_Primitive.ipynb)<br>[`02c_HITL_Patterns.ipynb`](mandatory/notebook/02c_HITL_Patterns.ipynb) | — |
| 9.3 | Subgraphs ([theory](mandatory/theory/03_subgraphs/README.md)) | [`03a_Subgraphs.ipynb`](mandatory/notebook/03a_Subgraphs.ipynb) | — |
| 9.4 | Async and streaming ([theory](mandatory/theory/04_async_and_streaming/README.md)) | [`04a_Async_and_Streaming.ipynb`](mandatory/notebook/04a_Async_and_Streaming.ipynb) | — |
| 9.5 | Retry policies and bounded cycles ([theory](mandatory/theory/05_retry_policies_and_bounded_cycles/README.md)) | [`05a_Retries.ipynb`](mandatory/notebook/05a_Retries.ipynb)<br>[`05b_Cycles_and_Loops.ipynb`](mandatory/notebook/05b_Cycles_and_Loops.ipynb) | — |
| 9.6 | State management in practice ([theory](mandatory/theory/06_state_management_in_practice/README.md)) | [`06a_LangGraph_State_Management.ipynb`](mandatory/notebook/06a_LangGraph_State_Management.ipynb) | — |

## Hands-on lab

Approval loop: add a checkpointer and an interrupt before the answer node of your M08 graph, resume it after approval, and stream the steps. Details: [lab/README.md](lab/README.md).

## Key concepts

[Checkpointer](mandatory/theory/01_checkpointing_and_threads/README.md#checkpointer) · [interrupt()](mandatory/theory/02_interrupts_and_human_in_the_loop/README.md#interrupt) · [Subgraphs](mandatory/theory/03_subgraphs/README.md#subgraphs) · [Streaming modes](mandatory/theory/04_async_and_streaming/README.md#streaming-modes)

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
| `mandatory/notebook/01a_Checkpointing.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/05_checkpointing/notebooks/01_Checkpointing.ipynb` |
| `mandatory/notebook/02a_HITL_Mechanics.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/06_interrupts_and_human_in_the_loop/notebooks/01_HITL_Mechanics.ipynb` |
| `mandatory/notebook/02b_LangGraph_Interrupt_Primitive.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/06_interrupts_and_human_in_the_loop/notebooks/02_LangGraph_Interrupt_Primitive.ipynb` |
| `mandatory/notebook/02c_HITL_Patterns.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/06_interrupts_and_human_in_the_loop/notebooks/03_HITL_Patterns.ipynb` |
| `mandatory/notebook/03a_Subgraphs.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/08_subgraphs/notebooks/01_Subgraphs.ipynb` |
| `mandatory/notebook/04a_Async_and_Streaming.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/09_async_and_streaming/notebooks/01_Async_and_Streaming.ipynb` |
| `mandatory/notebook/05a_Retries.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/10_retry_policies/notebooks/01_Retries.ipynb` |
| `mandatory/notebook/05b_Cycles_and_Loops.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/11_cycles_and_loops/notebooks/01_Cycles_and_Loops.ipynb` |
| `mandatory/notebook/06a_LangGraph_State_Management.ipynb` | `ai-engineering-demystified-04-langgraph-fundamentals` | `modules/12_state_management_in_practice/notebooks/01_LangGraph_State_Management.ipynb` |
