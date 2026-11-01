# M10.4 Theory: Async and streaming

*[M10 theory](../README.md) · Lesson 10.4 · Notebooks: [`04a_Async_and_Streaming.ipynb`](../../../../course/p03_langchain_and_langgraph/m10_langgraph_runtime/notebooks/04a_Async_and_Streaming.ipynb) · [All theory pages](../../../README.md)*

## Streaming modes

`invoke` returns once, at the end. `stream` (and `astream`) yields chunks while the graph runs, and `stream_mode` decides what a chunk is. The installed LangGraph 1.2.18 has seven modes. Here is what each yields for one run of the four-node low-risk refund (triage, assess, execute, done), counted in the scratchpad:

| Mode | One chunk is | Chunks |
|---|---|---|
| `values` | the whole state, once at the start and after each step | 5 |
| `updates` | `{node: what it returned}`, after each node | 4 |
| `checkpoints` | a snapshot in the shape `get_state()` returns | 6 |
| `tasks` | a node starting, then finishing with its result or error | 8 |
| `debug` | checkpoints and tasks together, with step and timestamp | 14 |
| `messages` | `(token chunk, metadata)` from a chat model inside a node | per token |
| `custom` | whatever a node writes with `StreamWriter` | per write |

Match the mode to the screen:

- **Progress labels** ("checking eligibility", "waiting for approval"): `updates`. Each chunk names the node that just finished. When the run pauses, the last chunk is `{"__interrupt__": ...}`, so the client knows to show an approval card.
- **A typing effect:** `messages`. The 04a notebook prints each token as it arrives and adds the `AIMessageChunk` objects with `+` to rebuild the full reply.
- **A client that renders the whole state:** `values`.
- **Audits and debugging:** `checkpoints` or `debug`.

`messages` mode streams tokens from every chat-model call inside every node, not only the one that writes the answer. A RAG graph with a grader node streams the grader's "yes relevant" before the answer. Each chunk's metadata names its node, so filter on `metadata["langgraph_node"]` before you render.

Pass a list to get several modes from one run: `stream_mode=["updates", "messages"]` yields `(mode, chunk)` pairs. On the refund run, `["updates", "values"]` yields 9 pairs, the 4 and the 5 from the table.

## Async nodes

A node can be `async def` and `await model.ainvoke(...)`; the graph then runs with `await graph.ainvoke(...)` or `async for chunk in graph.astream(...)`. The notebook's async graph has the same shape as its synchronous one; only the node and the call change.

Async matters when one server process handles many conversations. A synchronous `invoke` holds its worker for the whole run, model calls included. An async node gives the event loop back while it waits on the model or a tool, so a FastAPI handler can serve other Larkspur customers in the meantime. Streaming and async are separate choices: `stream` works synchronously, and `ainvoke` returns once at the end like `invoke`. A chat endpoint usually wants both, `astream` with `messages` and `updates`.

Two details from the notebook:

- **`streaming=True` on the model** makes the provider send tokens as they are generated, which `messages` mode then passes through.
- **Checkpoints work the same.** The async graph is compiled with `MemorySaver`, and a second `ainvoke` on the same thread sees the first turn.

## Key Takeaways

- Choose the stream mode for the screen: `updates` for progress labels and pauses, `messages` for a typing effect, `values` for whole-state clients, `checkpoints` or `debug` for audits.
- `messages` mode streams tokens from every model call in every node. Filter on `metadata["langgraph_node"]` before you render.
- Async nodes free the event loop while waiting on models and tools, so one process serves many conversations. Streaming is a separate choice; a chat endpoint usually wants both.

## Check yourself

<details>
<summary>1. A RAG graph streamed in messages mode shows the grader's "yes relevant" before the answer. Why, and how do you stop it reaching the screen?</summary>

`messages` mode streams tokens from every chat-model call inside every node, not only the one that writes the answer. Each chunk's metadata names its node, so filter on `metadata["langgraph_node"]` before you render.

</details>

<details>
<summary>2. The Larkspur client shows progress labels and must show an approval card when the refund run pauses. Which stream mode fits, and how does it know to show the card?</summary>

`updates`. Each chunk is `{node: what it returned}`, so it names the node that just finished; the low-risk refund yields 4 of them. When the run pauses, the last chunk is `{"__interrupt__": ...}`, which tells the client to show the approval card.

</details>

<details>
<summary>3. A FastAPI chat endpoint calls invoke synchronously and slows down as conversations grow. What does making the nodes async change?</summary>

A synchronous `invoke` holds its worker for the whole run, model calls included. An `async def` node gives the event loop back while it waits on the model or a tool, so the handler can serve other customers meanwhile. Async does not stream by itself; a chat endpoint usually wants `astream` with `messages` and `updates`.

</details>

---
*Previous: [10.3 Subgraphs](../03_subgraphs/README.md). Next: [10.5 Retry policies and bounded cycles](../05_retry_policies_and_bounded_cycles/README.md).*
