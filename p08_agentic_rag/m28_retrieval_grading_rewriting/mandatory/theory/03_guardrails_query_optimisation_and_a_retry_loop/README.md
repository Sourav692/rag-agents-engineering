# M28.3 Theory: Guardrails, query optimisation and a retry loop

*[M28 theory](../README.md) · Lesson 28.3 · Notebooks: [`03a_advanced_rag_agent.ipynb`](../../notebook/03a_advanced_rag_agent.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Keep off-topic questions out of retrieval, stop the rewrite loop on purpose, and price every extra attempt. -->
<!-- format: approved -->

## Start with two questions the loop cannot finish

> **What you'll learn**
>
> - **Distinguish** an off-topic question from one the handbook cannot answer, and the check that catches each.
> - **Trace** an unanswerable question through a bounded loop and count its LLM calls.
> - **Compare** two router check orders on the same question.
> - **Choose** a rewrite bound from the golden set.

Lesson 28.1's graph rewrites when the grade fails, but it cannot stop. Two Larkspur questions show the cost. *Do you offer a student discount?* is about pricing, but the handbook has no discount policy. *What's the weather like today?* has nothing to do with Larkspur. In lesson 28.1's graph both rewrite again and again and never get a reply. Even with a counter, both would end in the same "I couldn't find that" message, which is wrong for the weather question.

## Topic guardrails

### The eight-node support agent

The notebook builds this agent for a fictional company's support documents. These pages run it on the Larkspur handbook. Before retrieving, it asks whether the question belongs to the assistant at all:

```mermaid
flowchart TD
    E[enhance_query] --> V{validate_topic}
    V -- IRRELEVANT --> OT[handle_off_topic]
    V -- RELEVANT --> F[fetch_content]
    F --> AR{assess_relevance}
    AR -- a chunk passed --> GR[generate_response]
    AR -- rewrites left --> OQ[optimize_query]
    AR -- 2 rewrites used --> NR[handle_no_results]
    OQ --> F
```

*Figure 1: The support agent. Three nodes end the turn, and the two handlers reply with fixed text and make no LLM call.*

A **topic guardrail** is a classification step before retrieval that decides whether a question is in scope. Here it is one structured-output call whose schema has a classification (`RELEVANT` or `IRRELEVANT`) and a confidence (`HIGH`, `MEDIUM` or `LOW`), both typed as fixed sets of values. Its prompt lists what is on topic (services, pricing, support procedures, company information) and what is not (general technology, other companies, weather and news). `RELEVANT` goes to retrieval. Anything else goes to the off-topic handler, which lists what the assistant can help with.

### Off topic or unanswered

The check comes before retrieval because the grader cannot tell "off topic" from "not in the handbook": both look like a retrieval where nothing passes. The [lab](interactive/grade-rewrite-retry-lab.html) shows the difference with two rewrites allowed:

| Question | Topic check | Grader | Ends in | LLM calls |
|---|---|---|---|---|
| *Can I export my data after I cancel my plan?* | on topic | 2 of 2 pass on the first retrieval | answer | 4 |
| *Do you offer a student discount?* | on topic | 0 of 2 on each of 3 retrievals | no-results reply | 9 |
| *What's the weather like today?* | off topic | not reached | off-topic reply | 1 |
| *What's the weather like today?*, check off | none | 0 of 2 on each of 3 retrievals | no-results reply | 8 |

*Table 1: Three golden questions, two rewrites allowed. The guardrail and the grader catch different failures.*

The weather question stops for 1 call instead of 8, and the customer reads "I can help with pricing, refunds and servers" instead of "I couldn't find that in the handbook".

The check costs one call on every question. Over the lab's five golden questions it costs 3 calls at zero rewrites (14 with the check, 11 without), breaks even at one (24 and 24) and saves 3 at two (31 and 34). It pays in calls when the off-topic share of traffic times the cost of a full retry loop exceeds one call per question. It pays in reply quality at any bound.

### The classification boundary

- **It classifies the enhanced query.** The enhancement node first folds the conversation history into a standalone question, and a follow-up such as *What about annual plans?* carries the refund question it follows.
- **Confidence is computed and ignored.** The router reads only the classification. Asking a clarifying question on `LOW` confidence needs a third branch.
- **A false rejection is silent.** An on-topic question classified `IRRELEVANT` never reaches retrieval or its logs. We call this the **silent rejection**. Track the off-topic rate and sample those replies.

## Bounded retries

**Bounded retries** means the graph counts its rewrites in the state and takes a different exit when the count reaches a limit. Lesson 28.1's graph has no counter. When the handbook has no answer, LangGraph's recursion limit (a cap on graph steps per run) is the only stop.

### The runaway rewrite loop

In the pinned `langgraph` 1.2.18 the default recursion limit is 10,007 steps. Lesson 28.1's graph, run with stub nodes and a grader that always says no:

| Recursion limit | Retrievals | LLM calls | How it ended |
|---|---|---|---|
| Default, 10,007 | 3,336 | 10,007 | `GraphRecursionError` |
| 25, set in the run's config | 8 | 25 | `GraphRecursionError` |

*Table 2: Lesson 28.1's graph on a question nothing can answer, with stub nodes.*

We call this the **runaway rewrite loop**. Each round costs three LLM calls (agent, grader, rewrite) and three graph steps. Calls track the step limit, and the run still ends in an error, not a reply.

### A counter in the state

This lesson's graph bounds the loop in the state:

- **The count**: a rewrite counter that the enhancement node resets to 0 at the start of every turn. The bound is per question, not per conversation.
- **The router**: after grading, it picks one of three exits in a fixed order, shown in Figure 2.
- **The guard**: the rewrite node repeats the limit check and does nothing if it is reached, in case a later edge reaches it directly.

```mermaid
flowchart TD
    G[Chunks graded] --> P{"Any chunk<br/>passed?"}
    P -- yes --> A[generate_response]
    P -- no --> C{"2 rewrites<br/>used?"}
    C -- yes --> N[handle_no_results]
    C -- no --> O[optimize_query]
```

*Figure 2: The router's check order. Evidence is checked before the budget, and a hit on the last retrieval is still answered.*

### Trace the student-discount question

With a bound of 2, a turn makes at most 3 retrievals. Follow the question that never finds evidence:

<div class="walkthrough learning-widget" data-stepper id="discount-walkthrough">
<p class="widget-intro">Follow the student-discount question through the bounded loop. Each stage shows the counter and the running call total.</p>
<div class="step-controls" hidden role="group" aria-label="Loop stages"><button type="button" data-step="0" aria-pressed="false" aria-controls="discount-step-0">1. Check</button><button type="button" data-step="1" aria-pressed="false" aria-controls="discount-step-1">2. Retrieve</button><button type="button" data-step="2" aria-pressed="false" aria-controls="discount-step-2">3. Rewrite</button><button type="button" data-step="3" aria-pressed="false" aria-controls="discount-step-3">4. Rewrite</button><button type="button" data-step="4" aria-pressed="false" aria-controls="discount-step-4">5. Stop</button></div>
<div class="step-panels"><section id="discount-step-0" class="step-panel" aria-labelledby="discount-heading-0"><h4 id="discount-heading-0">1. Enhance and check the topic</h4><dl><dt>Node</dt><dd>enhance_query, then validate_topic</dd><dt>Decision</dt><dd>RELEVANT: pricing is in scope</dd><dt>Counter</dt><dd>Reset to 0</dd><dt>LLM calls so far</dt><dd>1 (a first turn needs no enhancement call)</dd></dl></section><section id="discount-step-1" class="step-panel" aria-labelledby="discount-heading-1"><h4 id="discount-heading-1">2. First retrieval fails</h4><dl><dt>Node</dt><dd>fetch_content, then assess_relevance</dd><dt>Decision</dt><dd>Both chunks score 0.000 and fail. Rewrites are left.</dd><dt>Counter</dt><dd>0</dd><dt>LLM calls so far</dt><dd>3 (two grader calls)</dd></dl></section><section id="discount-step-2" class="step-panel" aria-labelledby="discount-heading-2"><h4 id="discount-heading-2">3. First rewrite, second retrieval</h4><dl><dt>Node</dt><dd>optimize_query, then fetch and grade</dd><dt>Decision</dt><dd>New wording, still no discount policy. One rewrite left.</dd><dt>Counter</dt><dd>1</dd><dt>LLM calls so far</dt><dd>6</dd></dl></section><section id="discount-step-3" class="step-panel" aria-labelledby="discount-heading-3"><h4 id="discount-heading-3">4. Second rewrite, third retrieval</h4><dl><dt>Node</dt><dd>optimize_query, then fetch and grade</dd><dt>Decision</dt><dd>No chunk passes, and the budget is used up.</dd><dt>Counter</dt><dd>2</dd><dt>LLM calls so far</dt><dd>9</dd></dl></section><section id="discount-step-4" class="step-panel" aria-labelledby="discount-heading-4"><h4 id="discount-heading-4">5. Reply that the handbook has no answer</h4><dl><dt>Node</dt><dd>handle_no_results</dd><dt>Decision</dt><dd>Fixed text, no LLM call</dd><dt>Counter</dt><dd>2</dd><dt>LLM calls so far</dt><dd>9 in all. The question needs new handbook content, which no rewrite can supply.</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

### Check evidence before the budget

The order of the router's two checks changes the outcome on the last retrieval. The outage question, *What happens if my server goes down?*, finds `sla` only on its third retrieval, after both rewrites are used.

**Evidence first (Figure 2).** The router sees a passing chunk and answers. The question costs 10 calls: 1 check, 6 grader calls, 2 rewrites and 1 answer.

**Budget first (Figure 3, an added counter-example).** The router sees two rewrites used and replies "not found" before it looks at the grades. It spends 9 calls and discards the evidence it has just retrieved.

```mermaid
flowchart TD
    G[Chunks graded] --> C{"2 rewrites<br/>used?"}
    C -- yes --> N[handle_no_results]
    C -- no --> P{"Any chunk<br/>passed?"}
    P -- yes --> A[generate_response]
    P -- no --> O[optimize_query]
```

*Figure 3: Added counter-example with the checks swapped. A hit on the last retrieval goes to the no-results reply.*

<div class="learning-widget evidence-switcher" data-comparison id="router-order-switcher">
<p class="widget-intro">Compare what the outage question's third retrieval produces under each check order.</p>
<div class="mode-controls" hidden role="group" aria-label="Router check order">
<button type="button" data-mode="evidence" aria-pressed="false" aria-controls="evidence-first">Evidence first</button>
<button type="button" data-mode="budget" aria-pressed="false" aria-controls="budget-first">Budget first</button>
</div>
<section id="evidence-first" class="mode-panel" data-announcement="Evidence first selected. The outage question is answered."><h4>Evidence first</h4><ul><li>Third retrieval: sla 0.470, incidents 0.253. The sla chunk passes.</li><li>First check: a chunk passed, so go to generate_response.</li></ul><p>Reply: an answer from the availability guarantee. 10 LLM calls.</p></section>
<section id="budget-first" class="mode-panel" data-announcement="Budget first selected. The outage question gets the no-results reply."><h4>Budget first</h4><ul><li>Third retrieval: sla 0.470, incidents 0.253. The sla chunk passes.</li><li>First check: two rewrites used, so go to handle_no_results.</li></ul><p>Reply: "I couldn't find that in the handbook". 9 LLM calls, and the passing chunk is discarded.</p></section>
<p class="switch-status" aria-live="polite"></p>
</div>

### The cost of each attempt

With `k = 2` chunks per retrieval, a question costs one call for the topic check, two grader calls per retrieval, one per rewrite and one for the answer if there is one. The handlers and a first-turn enhancement make none. Answered on the first retrieval, a question costs 1 + 2 + 1 = 4. Never answered with a bound of `m`, it costs `1 + 2(m + 1) + m`: 9 at a bound of 2. The [interactive lab](interactive/grade-rewrite-retry-lab.html) runs the loop on the five golden questions with real TF-IDF retrieval over the M10 handbook chunks and the bound as its slider:

| Rewrites allowed | Answered | No-results reply | Off-topic reply | Retrievals | LLM calls |
|---|---|---|---|---|---|
| 0 | 1 | 3 | 1 | 4 | 14 |
| 1 | 2 | 2 | 1 | 7 | 24 |
| **2** | **3** | **1** | **1** | **9** | **31** |
| 3 | 3 | 1 | 1 | 10 | 34 |

*Table 3: The golden set at each bound. The bold row is the notebook's bound.*

<!-- lab: interactive/grade-rewrite-retry-lab.html -->

### Choosing the bound

Each step up the bound reaches one more question until 2, where the outage question is answered on its second rewrite. Going to 3 answers nothing new: the extra retrieval and three calls all go to the student-discount question, which no bound can answer. Unanswerable questions always pay the full bound. Set it where the answered count stops rising.

> **Pitfall: the counter as the only stop.** Keep the recursion limit as a backstop under the counter. The counter bounds the loop you designed. The recursion limit bounds the one a later edit creates by accident.

## Two rewrites, two jobs

The graph rewrites the query in two places, for different reasons:

| | `enhance_query` | `optimize_query` |
|---|---|---|
| Runs | Once per turn, before the topic check | After a retrieval where no chunk passed |
| Reads | The conversation history and the new question | The current query |
| Job | Make a follow-up standalone | Find words that retrieve better |
| On the first turn | Passes the question through, no LLM call | Same as any turn |

*Table 4: Enhancement repairs the conversation. Optimisation repairs the retrieval.*

### When a rewrite helps

A rewrite helps only if it moves toward the documents' words. The outage question shows both cases:

| Attempt | Query | Top two chunks | Passes? |
|---|---|---|---|
| Original | *What happens if my server goes down?* | `reboot` 0.416, `sizing` 0.389 | No |
| Rewrite 1 | *What happens when my server is unavailable?* | `reboot` 0.416, `sizing` 0.389 | No |
| Rewrite 2 | *Larkspur outage availability guarantee and incident updates* | `sla` 0.470, `incidents` 0.253 | Yes |

*Table 5: The outage question's three retrievals. The rewrites are the lab's hand-written ones.*

TF-IDF matches exact words, and "unavailable" is not in the handbook (only "availability" is). The first rewrite retrieves the same chunks at the same scores. We call this the **synonym swap**: new wording that never reaches the documents' vocabulary. The second rewrite uses the handbook's words, "outage" and "availability".

### Drift across rewrites

Each optimisation reads the current query and writes back to the same field. The second rewrite rewrites the first, and two rounds can drift from what the customer asked. Lesson 28.1's rewrite node rewords the original question every time instead, at the cost of never building on a near miss. M17 covers rewriting before retrieval as a stage of its own, including HyDE and multi-query.

## Diagnose a loop that misbehaves

*Added diagnosis guide.* Each failure has a different signal in the logs:

| Failure | Signal | Fix |
|---|---|---|
| Silent rejection | Off-topic rate rises, with no retrieval logged for those questions | Sample off-topic replies, and branch on `LOW` confidence |
| Runaway rewrite loop | `GraphRecursionError` instead of a reply | A per-question counter in the state, recursion limit as backstop |
| Budget checked first | "Not found" right after a passing grade | Check evidence before the budget |
| Synonym swap | A rewrite retrieves the same chunks at the same scores | Steer the rewriter toward the documents' vocabulary |
| Drift | Later rewrites no longer ask the customer's question | Rewrite from the original question, or keep it beside the search wording |

*Table 6: Five loop failures, the signal each leaves and its fix.*

The no-results rate lists the handbook's gaps, and a jump after a change points at the index or the grader.

> **Key distinction:** this graph knows when to stop, but it never checks its own answer. M29 adds a web-search fallback when grading fails and a check on the generated answer.

## Limits of this evidence

- **Stand-ins in the lab.** Retrieval is real TF-IDF, but the grader passes only the golden set's answer chunks, the topic check reads the golden label and the rewrites are hand-written. Real LLMs make mistakes these do not.
- **Five questions.** A larger golden set may keep gaining answers past a bound of 2.
- **Stub nodes.** Table 2 measures graph steps, not a model's behaviour.
- **Illustrations.** The walkthrough and the check-order comparison are scripted from the lab's numbers. Figure 3 is a counter-example, not the notebook's graph.

## References

1. [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), accessed 13 November 2026.

## Key Takeaways

- A topic check before retrieval costs one call per question and keeps off-topic questions out of the retry loop. Track the off-topic rate, because a silent rejection leaves no retrieval log.
- Bound rewrites with a per-question counter in the state, check evidence before the budget, and keep the recursion limit as a backstop. Unanswerable questions always pay the full bound: set it where the golden set's answered count stops rising.
- Enhancement makes a follow-up standalone, and optimisation looks for words that retrieve better. A rewrite helps only when it reaches the documents' vocabulary, and rewriting a rewrite can drift from the question.

## Check yourself

<details>
<summary>1. Why does the topic check run before retrieval instead of leaving off-topic questions to the document grader?</summary>

The grader cannot tell "off topic" from "not in the handbook": both look like a retrieval where nothing passes, spend the retry budget and end in the same no-results reply. In the lab the weather question costs 1 call with the check and 8 without.

</details>

<details>
<summary>2. With two rewrites allowed and two chunks per retrieval, how many LLM calls does a question the handbook cannot answer cost?</summary>

Nine: 1 for the topic check, 6 grader calls (2 per retrieval over 3 retrievals) and 2 rewrites, with no answer call. In general it is `1 + 2(m + 1) + m` for a bound of `m`, because unanswerable questions always pay the full bound.

</details>

<details>
<summary>3. The outage question's first rewrite retrieves exactly the same two chunks as the original. What went wrong, and should you raise the bound to compensate?</summary>

It is a synonym swap: "unavailable" is no more a handbook word than "goes down", so TF-IDF returns the same chunks at the same scores. A higher bound only buys more attempts. The fix is a rewriter that reaches the documents' vocabulary, as the second rewrite does with "outage" and "availability".

</details>

---
*Previous: [28.2 The same agent on Databricks Vector Search](../../../optional/theory/02_the_same_agent_on_databricks_vector_search/README.md). Next: [M28 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
