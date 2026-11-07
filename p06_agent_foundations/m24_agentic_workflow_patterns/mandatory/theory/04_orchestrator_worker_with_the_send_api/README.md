# M24.4 Theory: Orchestrator–worker with the Send API

*[M24 theory](../README.md) · Lesson 24.4 · Notebooks: [`04a_orchestrator_worker_send_api.ipynb`](../../notebook/04a_orchestrator_worker_send_api.ipynb), [`04b_orchestrator_worker_lcel_map.ipynb`](../../../optional/notebook/04b_orchestrator_worker_lcel_map.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*

## Dynamic fan-out with Send

The Larkspur export question has two distinct information needs: how to export and how long data remains after cancellation. A refund-timing question needs only one. You will turn that difference into a variable-length plan, dispatch one worker per item, and inspect how the results return to shared state.

### Step 1: Distinguish a plan from fixed branches

Orchestrator-worker looks like parallelization: several LLM calls run at once and a final step merges them. The difference is who decides the branches. In parallelization you wrote them into the graph. Here an orchestrator LLM decides, per input, how many subtasks there are and what each one covers.

| | Parallelization (24.3) | Orchestrator-worker (24.4) |
|---|---|---|
| Who decides the subtasks | you, when you build the graph | the orchestrator, at run time |
| Number of branches | fixed | follows the input |
| Branch identity | known in advance (characters, setting, premise) | generated (whatever sections this topic needs) |
| Graph shape | static `add_edge` fan-out | one conditional edge returning a list of `Send` |

A reducer combines a previous state value with a returned update. Here `operator.add` concatenates the workers' result lists.

The same graph is often called **map-reduce**: the plan is the list, the `Send` fan-out is the map, and the synthesizer is the reduce.

```mermaid
flowchart LR
    Q[/Question/] --> O["Orchestrator<br/>returns a plan"]
    O -. "one Send per item" .-> W["llm_call<br/>one plan item each"]
    W --> R["Reducer<br/>operator.add"] --> S[Synthesizer] --> A[/Answer/]
```
<!-- animated: diagrams/send-fanout.anim.html -->

### Step 2: Follow a plan item into a worker

Trace the four parts of the implementation:

- **A plan with a variable length.** The orchestrator calls `with_structured_output(ReportPlan)`, where `sections` is a `list[Section]`, each with a `name` and a `description`.
- **Dispatch from the plan.** A normal conditional edge returns one node name. `assign_workers` returns a list, one `Send("llm_call", {"topic": ..., "section": section})` per planned section, and LangGraph starts that many runs of `llm_call`. The graph drawing shows the `orchestrator` to `llm_call` edge once, because the graph does not know the count until the orchestrator has run.
- **A narrow worker state.** Each worker gets a `WorkerState` with the topic and its one section, and its prompt uses `section.description`. That is what makes the plan load-bearing.
- **A reducer for the results.** `completed_sections` is `Annotated[list, operator.add]`, because an unknown number of workers write to it at once. The reference trace shows that the merged list follows the order the `Send`s were created, while `stream_mode="updates"` reports workers in the order they finish.

Inspect dispatch with a hand-written plan before using a model to generate one. These `Send` objects describe worker tasks. This snippet does not execute them.

```python
from langgraph.types import Send

sections = ["export instructions", "retention after cancellation"]
workers = [Send("llm_call", {"topic": "cancel and export", "section": section})
           for section in sections]
print(len(workers))
print([worker.arg["section"] for worker in workers])
```

**Expected output**

```text
2
['export instructions', 'retention after cancellation']
```

Replace the plan with `["refund timing"]` and inspect the list again. The dispatch count follows the plan rather than a fixed set of edges.

### Step 3: Check that the plan drives execution

The reference implementation demonstrates two failure modes. The first is in the prompt: a planner told "simple topics might need 2 sections, broad topics 5+" answered with five sections, Introduction and Conclusion included, for every topic. Asking for one section per distinct question and banning padding sections let the plan size follow the input. The second is the anti-pattern of a plan nobody reads: the orchestrator runs, but five fixed workers wired with `add_edge` ignore its output. If the set of workers that ran is the same for every input while the plan changes, the plan does not drive execution. That graph is parallelization with a decorative LLM call in front.

### Step 4: Choose the result and persistence model

LCEL can express the fan-out with `.map()` , with four gaps against `Send`:

| | LangGraph `Send` | LCEL `.map()` |
|---|---|---|
| Worker identity | each `Send` names its own target node | every item goes to the same runnable |
| Results land in | shared state, merged by a reducer | an ordered list matching the input |
| One worker fails | the graph can route around it | the whole batch raises, unless you use `batch(..., return_exceptions=True)` |
| Durability | per-worker checkpoints, interrupts, resume | none: the chain is stateless |

### Step 5: Bound the number of dispatched tasks

This is the shape of query decomposition (M17) and of the module lab: the orchestrator splits a Larkspur question into sub-questions, each worker retrieves and answers one, and the synthesizer writes the reply. *Can I export my data after I cancel my plan?* splits into "how do I export?" and "what happens to my data after I cancel?", whose evidence is the `export` and `retention` chunks of the M10 golden set. *How long does a refund take?* should get a plan of one item. Bound the plan in code as well as in the prompt: a maximum number of `Send`s, a direct path for one-item plans, and a decision about what an empty plan returns.

### Try it yourself

Write a two-item plan for exporting after cancellation and a one-item plan for refund timing. Check that `assign_workers` returns two `Send`s for the first and one for the second, and that each payload includes its own `section`. If both inputs always run five fixed workers, inspect the edges: the plan is not controlling dispatch. Also specify a maximum plan size and what an empty plan returns.

### Practice notebook

Use the implementation below to test the exercise and inspect each state update. Follow its provider setup for live model calls. Recorded model responses and timings can change on a new run.

- [Dynamic Send workers](../../notebook/04a_orchestrator_worker_send_api.ipynb).
- [LCEL mapped workers](../../../optional/notebook/04b_orchestrator_worker_lcel_map.ipynb) (optional).

## Key Takeaways

- In orchestrator-worker an LLM decides at run time how many subtasks there are, and a conditional edge returns one `Send` per plan item. Merge the workers' results with a reducer such as `operator.add`.
- Make the plan drive execution by giving each worker only its own section and using that section's description in its prompt. Fixed workers that ignore the plan waste the orchestrator call.
- Planner prompts tend to pad. One that suggested 2 to 5+ sections returned five for every topic. Ask for one section per distinct question, and cap the number of `Send`s in code.

## Check yourself

<details>
<summary>1. Both orchestrator-worker and parallelization run several LLM calls at once and merge them. What separates them?</summary>

Who decides the branches. In parallelization you wrote them into the graph with a static `add_edge` fan-out. In orchestrator-worker an LLM decides at run time how many subtasks there are and what each covers, and one conditional edge returns a list of `Send`, one per plan item.

</details>

<details>
<summary>2. How should the orchestrator plan the export-after-cancelling question and the refund-duration question?</summary>

The export question splits into "how do I export?" and "what happens to my data after I cancel?", whose evidence is the `export` and `retention` chunks. The refund question should get a plan of one item. Bound the plan in code too: a maximum number of `Send`s, a direct path for one-item plans and a decision about what an empty plan returns.

</details>

<details>
<summary>3. The orchestrator's plan changes with every topic, yet the same five workers run every time. What is wrong?</summary>

The plan drives nothing: five fixed workers wired with `add_edge` ignore the orchestrator's output, so the graph is parallelization with a decorative LLM call in front. Dispatch from the plan with one `Send` per section, and let each worker's prompt use its `section.description`.

</details>

---
*Previous: [24.3 Parallelization: sectioning and voting](../03_parallelization_sectioning_and_voting/README.md). Next: [24.5 Evaluator-optimizer loops, always bounded: LangGraph vs LCEL](../05_evaluator_optimizer_loops_always_bounded_langgraph_vs_lcel/README.md).*
