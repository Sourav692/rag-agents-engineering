# M10.6 Theory: State management in practice

*[M10 theory](../README.md) · Lesson 10.6 · Notebooks: [`06a_LangGraph_State_Management.ipynb`](../../../../course/p03_langchain_and_langgraph/m10_langgraph_runtime/notebooks/06a_LangGraph_State_Management.ipynb) · [All theory pages](../../../README.md)*

## Reducers and parallel writes

The 06a notebook runs without an API key: its LLM and tools are deterministic stubs, so every result in this section comes from running its code. The state schema is the contract between steps, and each field's reducer decides how a node's partial update lands. In the notebook, nodes `a` then `b` each return `1` for two fields:

| Reducer | Two nodes in a row each write | Two parallel nodes write in one step |
|---|---|---|
| None (`plain: int`) | the last write wins: `1` | `InvalidUpdateError` |
| `operator.add` (`summed`) | the writes add up: `2` | the writes add up |
| `add_messages` | appended, matched by id | appended; `RemoveMessage(id=...)` deletes |

A missing reducer fails in the parallel case. When two reviewers fan out from `START` and both return `risk`, LangGraph cannot choose, and stops with *At key 'risk': Can receive only one value per step. Use an Annotated key to handle multiple values.* Give the field a reducer and the merge is deterministic; that is how parallel reviewers' scores are summed.

The refund graph keeps one field as an audit trail, `events: Annotated[list[str], operator.add]`. Every node appends a line, nothing overwrites it, and the checkpoint history records when each line arrived. The model-facing `messages` list is the opposite case: section 10 of the notebook prunes it with `RemoveMessage` to fit the context window, while `events` is never pruned.

## Resume and side effects

A durable workflow re-executes code. The run resumes after an approval, a worker restarts after a crash, a `RetryPolicy` tries again. The checkpointer makes the state safe across all three; it cannot take back what a node already did to the outside world. The notebook's refund agent shows three ways a node runs again, and the Larkspur refund graph in the lab records each one with LangGraph 1.2.18:

- **Resume after `interrupt()`** re-runs the interrupted node from its first line ([lesson 10.2](../02_interrupts_and_human_in_the_loop/README.md#interrupt)). Nodes before it do not run again.
- **Resume after a crash** is `invoke(None, cfg)` on the same thread once the cause is fixed. The failed node runs again; `triage` and `assess` keep their checkpointed results. The low-risk refund takes 2 client calls: the first raises `ConnectionError` and leaves the thread parked at `execute`, the second finishes.
- **A `RetryPolicy`** re-runs the node inside the same call ([lesson 10.5](../05_retry_policies_and_bounded_cycles/README.md#retry-policies)). The caller sees no error; the provider sees two requests.

The [interactive lab](interactive/resume-side-effects-lab.html) counts what reaches the outside world for each combination. Its headline numbers, for the high-risk refund `refund-99`:

| Fault in `execute` | Guards off: notices, refunds | Guards on: notices, refunds |
|---|---|---|
| None | 2, 1 | 1, 1 |
| 503, crash then `invoke(None)` | 2, 1 | 1, 1 |
| 503, `RetryPolicy` | 2, 1 | 1, 1 |
| Response lost, `RetryPolicy` | 2, 2 | 1, 1 |

<!-- lab: interactive/resume-side-effects-lab.html -->

Two guards account for every difference:

- **Keep side effects off the resumed path.** With guards off, the approval notice is sent inside `human_gate` above `interrupt()`, so the billing team gets it again when the gate resumes. Moved into its own `notify` node before the gate, it runs once. The graph gains a node and one checkpoint (8 instead of 7), and the client still makes 2 calls.
- **Make external writes idempotent.** A 503 before the provider refunds is harmless to retry. A lost response after it refunds is not: with guards off the customer is refunded twice. With guards on, the call carries the key `refund:refund-99`, the provider recognises the second request and returns the stored result. The notebook's `EXECUTION_LEDGER` does the same check in process.

Put together, these are the notebook's closing rules: workers stay stateless, state lives in the checkpointer, the `events` field is the audit log, the workflow is an explicit graph with the human gate as a waiting state, and every side effect can run twice without harm.

## Check yourself

<details>
<summary>1. Two reviewers fan out from the start node and both return risk, and the run stops. Why, and what fixes it?</summary>

The `risk` field has no reducer, so LangGraph cannot choose between two writes in one step and raises "Can receive only one value per step". Give the field a reducer, such as `operator.add`, and the merge is deterministic; that is how parallel reviewers' scores are summed.

</details>

<details>
<summary>2. In the lab, refund-99's provider applies the refund and the response is lost, then a RetryPolicy retries. How many refunds does the customer get with guards off, and with guards on?</summary>

Two with guards off, one with guards on. With guards on the call carries the key `refund:refund-99`, so the provider recognises the second request and returns the stored result. A 503 before the refund is harmless to retry either way.

</details>

<details>
<summary>3. The billing team gets every high-risk approval notice twice, even with no faults. What causes it, and what is the fix?</summary>

The notice is sent inside `human_gate` above `interrupt()`, and a resume re-runs that node from its first line. Move the notice into its own `notify` node before the gate, so it runs once. The graph gains a node and one checkpoint (8 instead of 7), and the client still makes 2 calls.

</details>

---
*Previous: [10.5 Retry policies and bounded cycles](../05_retry_policies_and_bounded_cycles/README.md). Next: [M10 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
