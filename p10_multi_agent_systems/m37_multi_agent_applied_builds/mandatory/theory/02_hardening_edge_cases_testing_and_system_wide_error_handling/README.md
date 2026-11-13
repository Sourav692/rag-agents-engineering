# M37.2 Theory: Hardening: edge cases, testing and system-wide error handling

*[M37 theory](../README.md) · Lesson 37.2 · Notebooks: [`02a_hotel_edge_cases_and_errors.ipynb`](../../notebook/02a_hotel_edge_cases_and_errors.ipynb), [`02b_hotel_testing_the_system.ipynb`](../../notebook/02b_hotel_testing_the_system.ipynb), [`02c_hotel_system_wide_error_handling.ipynb`](../../../optional/notebook/02c_hotel_system_wide_error_handling.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Test the router without a model, read outcomes from state and the database, and give every failure a bounded way out -->
<!-- format: approved -->

## Start with a desk that fails politely

> **What you'll learn**
>
> - **Explain** why a multi-agent system needs tests at three levels, from a pure router to end-to-end runs.
> - **Trace** the router's three rules on hand-built states, and read which threshold makes which test pass.
> - **Diagnose** a test suite that turns green by hiding a bug.
> - **Choose** a bounded recovery for each kind of failure: retry, fallback model, degraded retrieval or a person.

Lesson 37.1 built a hotel desk with a coordinator, a compliance checker and a reservation agent, and left two gaps open: the checker runs only when the coordinator names it, and the router forwards on any mention of an agent's name.

Neither gap shows in a demo. The coordinator skips the compliance check, or forwards a booking before it has dates, and the guest still gets a polite reply. A vector store that goes down mid-turn ends the run with a stack trace.

## System testing

**System testing** for agents means checking the decisions and the side effects, never the tone of the final message. The build catches failures at three levels, from cheapest to most realistic:

| Level | What it checks | Model calls | How the result is read |
|---|---|---|---|
| Router unit tests | The routing rules, on 7 hand-built states | None | The route the pure router function returns |
| A confidence gate | That an unclear request stops the turn instead of forwarding | One per guest message | A `confidence` integer in state, from structured output |
| A regression table | 5 guest requests, end to end | Every agent's | The nodes that ran and the database |

*Table 1: Three levels of tests, cheapest first.*

### The router as a pure function

The router can be unit-tested because it is a pure function of the state: no model call, no I/O. It checks three rules in order:

```mermaid
flowchart TD
    R[Coordinator reply] --> Q1{"confidence<br/>below 50?"}
    Q1 -- yes --> E1["END<br/>ask the guest to repeat"]
    Q1 -- no --> Q2{"Verdict since the<br/>latest guest message?"}
    Q2 -- yes --> D["Drop compliance_checker<br/>from the candidates"]
    Q2 -- no --> Q3{"Reply names a<br/>candidate agent?"}
    D --> Q3
    Q3 -- yes --> F[Forward to it]
    Q3 -- no --> E2["END<br/>the reply stands"]
```

*Figure 1: The router's three rules. The confidence gate runs first, then the loop guard, then the name check.*

The seven tests pin each rule down. We ran the build's router on them at its threshold of 50:

| Test state | Confidence | Expected | Returned |
|---|---|---|---|
| Reply forwards to the checker | 90 | checker | checker |
| Verdict given, reply forwards to reservations | 90 | reservations | reservations |
| Loop guard: checker named again after a verdict | 90 | END | END |
| Old verdict, new guest message, checker named | 90 | checker | checker |
| Unsure reply that names the reservation agent | 20 | END | END |
| Plain answer about the gym | 95 | END | END |
| Known issue: "I can't involve the reservation assistant until you give me dates" | 70 | END | reservations |

*Table 2: The seven router tests at threshold 50, run with the shared hotel module and no model.*

The last row is a **known issue** kept on purpose: lesson 37.1's mention routing, where the refusal contains the words "reservation assistant" and the name check matches them. The suite keeps it as an expected failure, which documents the gap and flags the day a typed router fixes it.

### The confidence gate

The confidence score comes from the coordinator itself. On each new guest message it asks the model for a self-assessment, a score from 0 to 100 and a one-line reason. The assessor's prompt defines three bands:

- **80 to 100**: the intent is clear.
- **50 to 79**: the intent is clear but details are missing, such as a booking without dates.
- **0 to 49**: the model cannot tell what the guest wants.

Only the last band should stop the turn, which puts the threshold at 50. Below it the coordinator apologises and asks the guest to rephrase. The score is a heuristic, not a calibrated probability; its job is to trigger the "ask again" path.

### What a threshold can hide

The [interactive lab](interactive/router-test-bench-lab.html) runs the same router and its seven tests in the page, ported from the shared hotel module, and recomputes them at every threshold. We ran the Python router at all 101 thresholds and got the same four bands:

| Threshold | Tests passing | What changes |
|---|---|---|
| 0 to 20 | 5 of 7 | The confidence-20 reply clears the gate and forwards to the reservation agent |
| 21 to 70 | 6 of 7 | Only the known issue fails, as recorded |
| 71 to 90 | 7 of 7 | The known issue passes because the gate ends its turn before the name check runs |
| 91 to 100 | 4 of 7 | The gate blocks the three confident forwards, scored 90 |

*Table 3: Router tests passing at each threshold, from the Python router and the lab.*

All seven green at 75 is the wrong result. Mention routing is as fragile as at 50, and every guest whose booking lacks dates, which the assessor scores 50 to 79, now gets an apology instead of a question about the dates. Call this a **gate that hides the bug**: the suite passes because a different rule fires first.

<!-- lab: interactive/router-test-bench-lab.html -->

### Regression runs read from state

Unit tests cannot tell whether the model still behaves. The regression table can. Each row is a guest request with its expected outcome, run on a fresh thread after the database is rebuilt:

| Case | Confident | Verdict | Reservation agent runs | Booked |
|---|---|---|---|---|
| General question (jacuzzi) | yes | `COMPLIANT` | no | |
| Another guest's data (Bob Johnson's dates) | yes | `VIOLATION` | no | |
| Booking, dates missing | yes | `COMPLIANT` | no | |
| Complete booking (Dana Lee, Deluxe) | yes | `COMPLIANT` | yes | one row for Dana Lee |
| Ambiguous ("same as last time, but…") | no | not checked | no | |

*Table 4: The five end-to-end cases and their expected outcomes.*

The outcome comes from the final state, the nodes that ran and a row count on `reservations`, never from the reply text. Each failure names the field that broke. `verdict: expected COMPLIANT, got None` means the coordinator skipped the check; `reservation: expected False, got True` means it forwarded a booking without dates.

Model output varies between runs. A single failure is a lead, and the number to track is the pass rate over several runs after every prompt or model change. Tests show that something broke; the next section covers how the system recovers.

## Edge cases and error paths

The build pushes on three edges of the core system and puts each safeguard in code:

- **Injection-style input.** A guest hides `' OR '1'='1` in the room type. Pasted into a `WHERE`, the condition is true for every row: on a scratch copy of the hotel database, a Deluxe search widened that way returned all 8 rooms instead of 2. It can only widen a read, because the query tool refuses every write and the booking tool binds its values as parameters. The durable fixes are structural: a read-only connection and a narrow write tool.
- **A violation that should reach a person.** A human review node pauses the graph with `interrupt()`: the graph saves a checkpoint and stops. The thread's state shows which node waits, and resuming with the reviewer's decision continues from that point. A resumed node runs again from its first line, so side effects such as writing to the review log go after the pause, where they run once. The checkpoint history replays the thread step by step for investigating a complaint.
- **Dates in the past.** The model extracts the dates with structured output, given today's date to resolve "next Friday", and a plain function compares them with today. That check is testable without an API call.

### Recovery by error type

Some failures do not fix themselves. A failing node catches its exception and writes a small record to an `error` field in state, with no message added. Routers read that field, so a guest who types the word "error" cannot trigger the error path. One error handler logs every failure with the thread id, and a pure decision router picks the recovery:

```mermaid
flowchart LR
    N[Failing node] --> E["error field<br/>in state"]
    E --> H[Error handler]
    H --> DR{Error type}
    DR -->|LLM call| AM[Alternative model]
    DR -->|retrieval| DG[Degraded retrieval]
    DR -->|other| HI[Human intervention]
```

*Figure 2: The error path. Failures travel through state, and a pure router picks one recovery per error type.*

The three recoveries:

| Failure | Recovery | What it does |
|---|---|---|
| The coordinator's model call fails | Alternative model | Answers as the coordinator with a second model, `gpt-4o` |
| The vector store fails | Degraded retrieval | Skips the store and sends the hard-coded rules straight to the verdict node |
| Anything else, including a failing fallback | Human intervention | A stub that writes a handoff message |

*Table 5: Recovery per error type.*

Follow one failure through that path:

<div class="walkthrough learning-widget" data-stepper id="error-walkthrough">
<p class="widget-intro">The vector store is down when a guest asks about rooms with a jacuzzi. Each stage names the node that runs and what it writes to state.</p>
<div class="step-controls" hidden role="group" aria-label="Error path stages"><button type="button" data-step="0" aria-pressed="false" aria-controls="error-step-0">1. Fail</button><button type="button" data-step="1" aria-pressed="false" aria-controls="error-step-1">2. Route</button><button type="button" data-step="2" aria-pressed="false" aria-controls="error-step-2">3. Log</button><button type="button" data-step="3" aria-pressed="false" aria-controls="error-step-3">4. Degrade</button><button type="button" data-step="4" aria-pressed="false" aria-controls="error-step-4">5. Verdict</button></div>
<div class="step-panels"><section id="error-step-0" class="step-panel" aria-labelledby="error-heading-0"><h4 id="error-heading-0">1. The checker records its failure</h4><dl><dt>Node</dt><dd>compliance_checker</dd><dt>State</dt><dd>error holds the type RetrievalException, the node name and the detail; no message is added</dd></dl></section><section id="error-step-1" class="step-panel" aria-labelledby="error-heading-1"><h4 id="error-heading-1">2. The checker's router sees the field</h4><dl><dt>Router</dt><dd>after_compliance_checker reads error before anything else</dd><dt>Route</dt><dd>error_handler, not the retrieval tool</dd></dl></section><section id="error-step-2" class="step-panel" aria-labelledby="error-heading-2"><h4 id="error-heading-2">3. The handler logs and the decision router picks</h4><dl><dt>Node</dt><dd>error_handler, with the thread id read from the run's config</dd><dt>Route</dt><dd>decision_router maps RetrievalException to degraded_retrieval</dd></dl></section><section id="error-step-3" class="step-panel" aria-labelledby="error-heading-3"><h4 id="error-heading-3">4. Degraded retrieval lists every rule</h4><dl><dt>Node</dt><dd>degraded_retrieval</dd><dt>State</dt><dd>A fallback_rules message with all four rules; error cleared to None</dd><dt>Route</dt><dd>Straight to generate, skipping the vector store</dd></dl></section><section id="error-step-4" class="step-panel" aria-labelledby="error-heading-4"><h4 id="error-heading-4">5. The verdict uses the fallback rules</h4><dl><dt>Node</dt><dd>generate, then the coordinator</dd><dt>Result</dt><dd>A verdict judged against all four rules instead of the top 2, and the turn carries on</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

A fallback that fails raises a different error type, and the router sends it to a person instead of looping. Call the trap this avoids a **fallback loop**. Every failure is injected with a simulation flag, which lets each recovery path run on every run, and a table computed from the node paths proves which one ran.

### Retries for brief outages

Transient failures get a cheaper fix first: a retry policy re-runs a node that raises, without writing anything to the `error` field. It sits on the node itself:

```mermaid
flowchart LR
    N[Node raises] --> W["Wait 0.2 s,<br/>then 0.4 s"]
    W --> A{"Attempts<br/>left?"}
    A -- yes --> N2[Run the node again]
    A -- no --> X[Exception reaches the caller]
```

*Figure 3: A retry policy. It handles a failure that clears on its own, and gives up after a fixed number of attempts.*

The build uses three attempts, a 0.2 s first wait and no jitter. We ran that policy on a tiny graph whose node fails a set number of times:

<div class="learning-widget evidence-switcher" data-comparison id="retry-switcher">
<p class="widget-intro">Compare the same flaky node with and without the build's retry policy.</p>
<div class="mode-controls" hidden role="group" aria-label="Retry setting">
<button type="button" data-mode="none" aria-pressed="false" aria-controls="retry-none">No policy</button>
<button type="button" data-mode="two" aria-pressed="false" aria-controls="retry-two">Policy, 2 failures</button>
<button type="button" data-mode="three" aria-pressed="false" aria-controls="retry-three">Policy, 3 failures</button>
</div>
<section id="retry-none" class="mode-panel" data-announcement="No policy selected. The first failure ends the run."><h4>No policy</h4><ul><li>The node raises once.</li><li>The exception ends the whole run.</li></ul><p>1 attempt, the run crashes.</p></section>
<section id="retry-two" class="mode-panel" data-announcement="Policy with 2 failures selected. Succeeds on the third attempt."><h4>Policy, node fails twice</h4><ul><li>Waits 0.2 s, then 0.4 s, between attempts.</li><li>The third attempt succeeds and the guest never sees the outage.</li></ul><p>3 attempts, the run completes.</p></section>
<section id="retry-three" class="mode-panel" data-announcement="Policy with 3 failures selected. The exception reaches the caller."><h4>Policy, node fails three times</h4><ul><li>The same two waits.</li><li>No attempts left after the third failure.</li></ul><p>3 attempts, the exception reaches the caller.</p></section>
<p class="switch-status" aria-live="polite"></p>
</div>

A retry suits an outage that clears in under a second; the error path suits one that does not, or a failure that is not an outage at all, such as low confidence. Use both: retries on the node, and the `error` field for whatever the retries cannot fix.

### A test plan for Larkspur

Larkspur's desk from lesson 37.1 gets the same three levels: router unit tests, with the billing refusal that names the billing agent kept as a known issue; a regression table of handbook requests (a refund inside the window, one outside it, another account's data, an ambiguous "same as last month") read from node paths and the refunds table; and a pass rate per case over several runs. Errors recover by type, as above.

## Limits of this evidence

- **No model in the replays.** Tables 2 and 3, the injection count and the retry timings come from the shared hotel module and LangGraph's retry policy on scratch graphs. Tables 4 and 5 describe what the notebooks check, not a measured pass rate.
- **Simulated failures.** The error path is exercised with flags that raise at the node. A real outage can fail inside a tool call the node does not wrap. The error walkthrough follows the graph's edges, not a recorded run.
- **A stub for people.** Human intervention only writes a handoff message here; the `interrupt()` review node shows what a real pause needs.

Lesson 37.3 adds agents in parallel and a memory that outlives the context window.

## References

1. LangChain, [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts).
2. LangChain, [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence).
3. LangChain, [Fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance).
4. OWASP, [SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection).

## Key Takeaways

- Test at three levels: unit tests on the pure router with no model calls, a confidence gate that stops unclear turns, and an end-to-end regression table read from the nodes that ran and the database.
- A threshold that turns every test green can still be wrong. At 75 all seven router tests pass, yet every booking that lacks dates gets an apology instead of a question about the dates.
- Record failures in an `error` field in state and let a pure router pick the recovery, with a failed fallback raising a different error so it reaches a person. Keep retries for brief outages.

## Check yourself

<details>
<summary>1. Why can the router be unit-tested without a model call, and what does the regression table catch that those tests cannot?</summary>

The router is a pure function of the state, with no model call and no I/O, and seven hand-built states pin down its rules. The unit tests cannot tell whether the model still behaves. The regression table runs 5 guest requests end to end and reads the nodes that ran and the `reservations` table, never the reply text.

</details>

<details>
<summary>2. In the router test bench lab, a threshold of 75 makes all seven tests pass. Should you set the confidence threshold to 75?</summary>

No. The known issue passes only because the gate ends its turn before the name check runs, and mention routing is as fragile as at 50. Every guest whose booking lacks dates, which the assessor scores 50 to 79, would also get an apology instead of a question about the dates.

</details>

<details>
<summary>3. A regression run fails with verdict expected COMPLIANT but got None. What happened, and is one such failure enough to act on?</summary>

The coordinator skipped the compliance check, and no verdict was recorded. Model output varies between runs, which makes a single failure a lead to investigate, not a conclusion. The number to track is the pass rate over several runs, re-run after every prompt or model change.

</details>

---
*Previous: [37.1 Hotel system: environment, coordinator, reservation agent, compliance](../01_hotel_system_environment_coordinator_reservation_agent_compliance/README.md). Next: [37.3 Scaling: parallel agents, memory merging, language and sentiment, web search](../../../optional/theory/03_scaling_parallel_agents_memory_merging_language_and_sentiment_web_search/README.md).*
