# M24.2 Theory: Routing by handler and by model tier

*[M24 theory](../README.md) · Lesson 24.2 · Notebooks: [`02a_routing_langgraph.ipynb`](../../notebook/02a_routing_langgraph.ipynb), [`02b_routing_by_model_tier.ipynb`](../../notebook/02b_routing_by_model_tier.ipynb), [`02c_routing_lcel_runnable_branch.ipynb`](../../../optional/notebook/02c_routing_lcel_runnable_branch.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*

## Routing by handler

A Larkspur refund request belongs in billing, but a refund calculation may also need a stronger model. Those are two routing decisions. You will first choose one handler from a closed set, then use the measured model-tier example to diagnose the cost of sending hard work to the cheap tier.

### Step 1: Classify into a closed set

A router classifies the input once and sends it down exactly one specialist path. The model makes one small decision, a label from a fixed set, and everything after it is ordinary Python dispatch.

The content router has the same two-part shape as the 24.1 gate:

- **A constrained classifier.** `with_structured_output(ContentRoute)`, where `content_type` is `Literal["story", "poem", "joke"]`. The model cannot return a label the graph has no edge for, which a free-text answer like "I think they want a poem" could.
- **A pure condition function.** `determine_next_step` maps the stored label to a node name with `.get(..., "generate_story")`, so even an unexpected label lands somewhere.

### Step 2: Inspect the chosen handler

The recorded test uses with phrasing that implies the category without naming it: *Tell me something funny about artificial intelligence*, *I want to hear a tale about a brave knight*, *Create something poetic about the ocean*. All three reached the expected handler. Each request cost two LLM calls, one to classify and one in the handler, however many handlers exist. A fourth category is one more `Literal` value, one node and one edge. The LCEL version builds the same router with `RunnableBranch` and confirms that exactly one specialist chain runs per request.

For Larkspur, the closed set is the ticket queue: billing, technical, sales. The test that matters is the one the routing experiment models: check the routing decision itself, not only whether the final answer reads well.

## Routing by model tier

### Step 1: Separate triage from answering

The model-tier variant routes on a different axis. The conditional edge picks a **model**, not a handler: a cheap model triages each request as `easy` or `hard`, easy work stays on the cheap model and hard work goes to a reasoning model. You pay reasoning prices only on the traffic that needs them.

```mermaid
flowchart LR
    Q[/Request/] --> T{"Triage<br/>gpt-4o-mini"}
    T -- easy --> C["Cheap tier<br/>gpt-4o-mini"]
    T -- hard --> R["Reasoning tier<br/>o4-mini, effort high"]
```

Both answering nodes send the same prompt. Only the model differs, so a measured difference belongs to the model. Two details bite on the first real call: o-series models reject a custom temperature, so the reasoning tier passes `temperature=1`, and `reasoning_effort="high"` only means something to a reasoning model.

### Step 2: Compare the three answering strategies

The workload is mixed the way real traffic is, mostly easy: seven requests, four easy (extract an order id, a capital, a time conversion, reply "ok") and three hard (a deploy-schedule puzzle, an LRU eviction, a backoff sum). A router means nothing without "cheaper than what", so the recorded comparison runs all three strategies:

| Strategy | Accuracy | Answering time, total | Reasoning calls |
|---|---|---|---|
| All cheap | 71% | 5.2 s | 0 of 7 |
| **Routed** | **86%** | **13.4 s** | **1 of 7** |
| All reasoning | 100% | 20.1 s | 7 of 7 |

Treat these as saved results on a seven-question workload, not a general ranking of models. The time column counts the answering calls only. The routed row also pays one triage call per request on top. With seven requests one question moves accuracy by 14 points, so read the table for its shape: routed accuracy should track all-reasoning while its reasoning-call count tracks all-cheap. A router that sends everything to `hard` is worse than no router, because it adds triage to the full reasoning bill.

### Step 3: Inspect the costly misclassifications

The router predicts difficulty. It does not observe it. So it has a confusion matrix:

| | Sent to reasoning | Sent to cheap |
|---|---|---|
| Truly hard | 1 | **2**, one answered wrong (the LRU question) |
| Truly easy | 0 | 4 |

The two errors are not symmetric. Easy sent to reasoning wastes money: bounded, and visible on a bill. Hard sent to cheap returns a confident wrong answer: invisible until someone acts on it. So bias the triage prompt toward `hard` on borderline cases and accept the overspend as insurance. The same asymmetry fixes the fallback direction. "Try cheap, detect a bad answer, retry on reasoning" needs a reliable wrong-answer detector, and the detector can itself miss the error. A measured detector may support a fallback, but the fallback is not automatic evidence of correctness. Escalate on uncertainty before answering.

On Larkspur, *Can I get a refund after 45 days?* is the case to watch: it looks like a lookup and needs proration arithmetic. Put questions like it in the labelled set the router is measured on.

### Try it yourself

Read the confusion matrix before the accuracy table. Count the truly hard requests sent to cheap: two, with one wrong answer. Now send all seven requests to reasoning. Check that you remove those triage misses while paying seven reasoning calls rather than one, and explain why retaining triage on that path would add cost without saving a reasoning call.

### Practice notebook

Use the implementation below to test the exercise and inspect each state update. Follow its provider setup for live model calls. Recorded model responses and timings can change on a new run.

- [Specialist routing](../../notebook/02a_routing_langgraph.ipynb).
- [Model-tier routing](../../notebook/02b_routing_by_model_tier.ipynb).
- [LCEL routing](../../../optional/notebook/02c_routing_lcel_runnable_branch.ipynb) (optional).

## Key Takeaways

- A router makes one small decision, a label from a fixed set, and dispatches in plain code. Each request costs two calls however many handlers exist, so test the routing decision itself.
- Routing by model tier pays reasoning prices only on hard traffic. In the recorded run the routed strategy reached 86% accuracy with 1 of 7 reasoning calls, against 71% all cheap and 100% all reasoning.
- Hard work sent to the cheap tier returns confident wrong answers, while easy work sent up only costs money. Lean the triage prompt toward `hard` on borderline cases and accept the overspend.

## Check yourself

<details>
<summary>1. Why does the content router classify with a structured output limited to a fixed set of labels instead of free text?</summary>

With `content_type` typed as `Literal["story", "poem", "joke"]`, the model cannot return a label the graph has no edge for, which a free-text answer like "I think they want a poem" could. The pure function `determine_next_step` then maps the label to a node, with a `.get` default so even an unexpected label lands somewhere.

</details>

<details>
<summary>2. A Larkspur customer asks whether they can get a refund after 45 days. Why is this a risky question for the model-tier router?</summary>

It looks like a lookup but needs proration arithmetic, so triage may label it `easy` and send it to the cheap tier, which can return a confident wrong answer. Put questions like it in the labelled set the router is measured on.

</details>

<details>
<summary>3. A teammate proposes trying the cheap model first and retrying on the reasoning model when the answer is bad. Why does this fail?</summary>

It needs a reliable wrong-answer detector, and the detector can itself miss the error. A measured detector may support a fallback, but the fallback is not automatic evidence of correctness. A hard question answered on the cheap tier returns a confident wrong answer that stays invisible until someone acts on it. Escalate on uncertainty before answering, and bias triage toward `hard` on borderline cases.

</details>

---
*Previous: [24.1 Prompt chaining with quality gates](../01_prompt_chaining_with_quality_gates/README.md). Next: [24.3 Parallelization: sectioning and voting](../03_parallelization_sectioning_and_voting/README.md).*
