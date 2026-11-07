# M24.5 Theory: Evaluator–optimizer loops, always bounded: LangGraph vs LCEL

*[M24 theory](../README.md) · Lesson 24.5 · Notebooks: [`05a_evaluator_optimizer_langgraph.ipynb`](../../notebook/05a_evaluator_optimizer_langgraph.ipynb), [`05b_evaluator_optimizer_lcel.ipynb`](../../notebook/05b_evaluator_optimizer_lcel.ipynb) · [All theory pages](../../../../../theory/README.md)*

## Bounded loops

A Larkspur answer may cite the handbook but still promise a refund the policy does not allow. You want a reviewer to name that failure and let the generator revise it. You will trace this feedback, make the pass decision explicit, and prove that an always-rejecting reviewer cannot run forever.

### Step 1: Define what a passing draft means

Evaluator-optimizer generates a draft, grades it against explicit criteria and feeds the critique into the next draft, until the grade passes. An extraction gate checks whether an intermediate result may proceed. This loop instead sends a critique back to the content generator. It pays off when two things hold: the criteria are clear, and feedback measurably improves the next attempt.

```mermaid
flowchart LR
    T[/Topic/] --> G["Generate<br/>or revise"] --> E["Evaluate<br/>4 criteria + length"] --> R{Router}
    R -- approved --> F[/Final draft/]
    R -- "needs work,<br/>under 5 drafts" --> G
    R -- "5 drafts" --> C[/"Last draft,<br/>needs_improvement"/]
```

The evaluator is only as useful as its criteria. An initial version of the experiment asked for one holistic grade against loose criteria such as "is it genuinely funny?", and with `gpt-4o-mini` the loop almost never converged: the evaluator kept finding something that could be better. The bounded version changes three things:

- **One boolean per criterion.** `JokeReview` asks four yes-or-no questions: a clear punchline, a punchline that depends on agentic AI specifically, no stock template, appropriate. A met criterion passes even if the joke could be better.
- **Code checks what code can check.** Length is `len(joke.split()) <= MAX_WORDS` with `MAX_WORDS = 40`, not an LLM judgement.
- **The verdict is computed.** `approved` only when every criterion and the length check pass. The model never asserts the grade itself, and `improvement_feedback` names a fix for each failed criterion.

### Step 2: Pass the critique into the next draft

The generator runs at temperature 0.7 so a revision can differ from the draft before it, and the evaluator at 0 to reduce grading variation. It can still assign different grades to the same draft, so measure that variation rather than assuming determinism. Later passes receive the previous draft plus the feedback, so they revise instead of starting over.

### Step 3: Prove that rejection reaches the cap

A structured verdict does not guarantee the evaluator will ever approve. So the router checks a cap: approved ends the run, `iteration >= MAX_ITERATIONS` (5) ends it too, anything else loops back. The deterministic cap test uses with a stub reviewer that rejects every draft. Without the `iteration_cap_reached` branch that cell would never finish. The cap also bounds cost: each pass is one generator call and one evaluator call, so a run makes at most ten.

The router can be tested without a generator or judge. This is the reference stopping rule with a plain dictionary annotation for the small example.

```python
MAX_ITERATIONS = 5

def determine_next_action(state: dict) -> str:
    if state["quality_assessment"] == "approved":
        return "content_approved"
    if state["iteration"] >= MAX_ITERATIONS:
        return "iteration_cap_reached"
    return "content_needs_refinement"

for iteration in [1, 5]:
    print(determine_next_action({"quality_assessment": "needs_improvement",
                                 "iteration": iteration}))
print(determine_next_action({"quality_assessment": "approved", "iteration": 5}))
```

**Expected output**

```text
content_needs_refinement
iteration_cap_reached
content_approved
```

Approval is checked first. A rejected fifth draft ends at the cap. An approved fifth draft ends as approved. Neither case starts a sixth draft.

### Step 4: Compare the three loop bounds

The bound can live in three places, one per implementation:

| Implementation | The loop is | The bound is |
|---|---|---|
| LangGraph | a conditional edge back to `generate_content` | `MAX_ITERATIONS` checked in the router, with LangGraph's `recursion_limit` as a backstop |
| LCEL plus Python | a `for` loop around two chains | `range(1, MAX_ITERATIONS + 1)` |
| `create_agent` middleware | `after_model` returning `jump_to="model"` | `ModelCallLimitMiddleware(run_limit=5, exit_behavior="end")` |

A run that ends at the cap returns the last draft marked `needs_improvement`, so count it as a failure. Watch the share of runs that end there. It rises when the criteria drift, or when a new evaluator model is stricter than the old one.

For Larkspur, an answer-quality check is the natural evaluator, written as booleans: does the reply cite a handbook chunk, does it state the refund window the chunk states, does it avoid promising anything the handbook does not say, and is it under a length limit counted in code. CRAG (M29) applies the same loop to retrieval: grade the documents, rewrite the query, try again, within a bound.

## Where LCEL stops

### Step 1: Distinguish a cycle from a longer chain

LCEL, the LangChain Expression Language, composes runnable steps into a flow. Every earlier pattern is a directed acyclic flow, so each maps onto an LCEL operator. This one has a cycle, and LCEL has no operator for "go back and try again until a predicate passes". `a | b | a` does not loop: it builds a three-step chain that runs `a` twice. `.with_retry()` comes close but retries blind, with no memory of why the last attempt failed, and feeding the critique forward is the point of the pattern.

| Pattern | LangChain 1.x primitive | Full coverage |
|---|---|---|
| Prompt chaining | `\|` plus `.with_retry()` plus `.with_fallbacks()` | yes |
| Routing | `RunnableBranch` | yes |
| Parallelization | `RunnableParallel` | yes |
| Orchestrator-worker | `.map()` | the fan-out; shared state and per-worker durability need `Send` |
| Evaluator-optimizer | a Python loop, or `after_model` plus `jump_to` | yes |

### Step 2: Choose the runtime around the loop

Choosing between the two LangChain loops comes down to what you need around the loop. The Python `for` loop is easy to read and returns a dict you shaped, but traces each pass as separate chain runs and has no streaming, checkpointing or interrupts. The middleware loop is one agent run with every pass nested, keeps the full message history as its state, and inherits tools, streaming and persistence from the agent runtime. Two details matter there: `can_jump_to=["model"]` on the decorator is what creates the conditional edge, and the critique reaches the next draft as an appended `HumanMessage`. When the loop needs checkpoints, interrupts or a human in it, that is the point to move to LangGraph.

### Try it yourself

Replace the evaluator with a stub that rejects every draft. Check that the fifth draft terminates with `needs_improvement` and that at most ten generator-and-evaluator calls occur. Then make the evaluator approve an earlier draft. Check that approval stops the loop before the cap. Reaching the cap is a bounded failure, not a quality pass.

### Practice notebook

Use the implementation below to test the exercise and inspect each state update. Follow its provider setup for live model calls. Recorded model responses and timings can change on a new run.

- [A bounded review graph](../../notebook/05a_evaluator_optimizer_langgraph.ipynb).
- [Review loops in LCEL](../../notebook/05b_evaluator_optimizer_lcel.ipynb).

## Key Takeaways

- Evaluator-optimizer feeds a critique into the next draft until the grade passes. Use it only when the criteria are clear and feedback measurably improves the next attempt.
- Grade with one boolean per criterion, check length in code and compute `approved` from the checks. A single holistic grade with `gpt-4o-mini` almost never converged.
- Cap every loop and count a run that hits the cap as a failure. LCEL cannot express the cycle, so use a Python loop or middleware, and move to LangGraph when you need checkpoints or interrupts.

## Check yourself

<details>
<summary>1. Why did replacing one holistic grade with one boolean per criterion make the joke loop converge?</summary>

Against a loose holistic grade the evaluator kept finding something that could be better. With four yes-or-no criteria, a met criterion passes even if the joke could improve, length is checked in code (`MAX_WORDS = 40`), and `approved` is computed only when every check passes, so the model never asserts the grade itself.

</details>

<details>
<summary>2. With a cap of 5 iterations, how many LLM calls can one run make at most, and how should you count a run that hits the cap?</summary>

Ten, because each pass makes one generator call and one evaluator call. A run that ends at the cap returns its last draft marked `needs_improvement`, so count it as a failure and watch the share of runs that end there.

</details>

<details>
<summary>3. A teammate builds the loop in LCEL by piping generator, evaluator and generator again, or by adding a retry. Why does neither work?</summary>

`a | b | a` builds a three-step chain that runs `a` twice. It never loops. `.with_retry()` retries blind, with no memory of why the last attempt failed, and feeding the critique forward is the point of the pattern. Use a Python `for` loop or `after_model` with `jump_to`, and move to LangGraph when the loop needs checkpoints or interrupts.

</details>

---
*Previous: [24.4 Orchestrator-worker with the Send API](../04_orchestrator_worker_with_the_send_api/README.md). Next: [M24 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
