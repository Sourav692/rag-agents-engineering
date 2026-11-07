# Lab: M09 LangGraph Runtime: Persistence, HITL & Streaming

## Brief

Approval loop: add a checkpointer and an interrupt before the answer node of your M08 graph, resume it after approval, and stream the steps.

## Approach

The solution, [solution/m09_solution.ipynb](solution/m09_solution.ipynb), rebuilds the M08 lab graph inline (classify, then `billing_answer` or `support_answer`), compiles it with `MemorySaver` and `interrupt_before` both answer nodes, and streams every step with `stream_mode="updates"`. One thread stops before answering, is approved and resumes from its checkpoint; a second thread is rejected and never resumes.

- **No checkpointer, no resume.** The checkpointer saves the whole state after every step under the `thread_id`; same id shares one history, different ids never see each other (lesson 9.1).
- **Resume with `None`.** After the pause, `graph.stream(None, config)` continues the saved thread. Passing the question again would start a new run on that thread.
- **Approve on an exact value.** The approval is whatever the caller passes, so treat anything but an explicit yes as no (lesson 9.2). In this lab the reviewer is a variable in the notebook.
- **Stream for the screen.** `updates` prints one line per node with only the keys it changed, which is the progress view an approval screen needs (lesson 9.4).
- **What to watch.** `interrupt_before` pauses between steps, so nothing in the answer node has run yet. With `interrupt()` inside a node instead, the node runs again from its first line on resume, so side effects above the call would repeat (lessons 9.2 and 9.6).

## How to run

- Environment: the default `uv sync`; no extra group.
- Keys: `EXPERIENTIALLABS_API_KEY`, read from the repository's `.env` (template: `.env.example`). Docker: none.
- Execute in place: `uv run jupyter nbconvert --to notebook --execute p03_llm_application_frameworks/m09_langgraph_runtime/lab/solution/m09_solution.ipynb --output /tmp/m09_run.ipynb`

## Data

`data/larkspur/`, a byte-for-byte copy of the course corpus. See [data/README.md](data/README.md).

## Results

Not run yet; the owner runs the solution and fills this table with the run date and the model. The notebook prints the streamed updates of both threads.

| Thread | Question | Category | Stopped before | After resume | Answered | Checkpoints |
|---|---|---|---|---|---|---|
| approved | g01 How long does a refund take? | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| rejected | g05 Does a reboot change my server's IP address? | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
