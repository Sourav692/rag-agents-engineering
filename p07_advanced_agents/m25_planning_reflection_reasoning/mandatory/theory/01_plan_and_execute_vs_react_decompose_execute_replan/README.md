# M25.1 Theory: Plan-and-execute vs ReAct; decompose, execute, replan

*[M25 theory](../README.md) · Lesson 25.1 · Notebooks: [`01a_planning_react_vs_plan.ipynb`](../../notebook/01a_planning_react_vs_plan.ipynb), [`01b_planning_decompose_execute_replan.ipynb`](../../notebook/01b_planning_decompose_execute_replan.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Writing the lookups down first saves calls, and a check on every result is what keeps a plan honest -->

## Plan-and-execute

> **What you'll learn**
>
> - **Compare** a ReAct agent and a plan-and-execute agent by LLM calls and tokens read on the same question.
> - **Explain** why a fixed plan writes a wrong search result straight into the answer.
> - **Trace** an evaluate-and-replan loop through a rejected step, and count what the rejection costs.
> - **Size** an executed-step cap from the plan and the retries you allow.

M22 and M23 built the ReAct loop, where the model reads each result and then decides the next step. This lesson asks what happens when the model decides every step before the first search runs.

A Larkspur Cloud customer wants to cancel an annual plan. The answer needs up to six handbook facts: the refund rule, how long a refund takes, what happens to the servers, how long data is kept, what an export includes and how fast support answers. A ReAct agent finds them one call at a time and sends the whole conversation back to the model on every call. Writing the lookups down first avoids that, but it also gives up the chance to react to a bad result. The page measures both sides and then adds the check that fixes the second.

A ReAct agent loops agent, tools, agent, and chooses each step after reading the last result. A **plan-and-execute agent** decides all its steps first and then runs them. The fixed-plan notebook builds it from three nodes:

| Node | What it does | LLM calls |
|---|---|---|
| Planner | One structured-output call returns the plan, a list of search queries with one fact each | 1 |
| Executor | Pops the next query and runs the search tool | 0 |
| Synthesizer | Reads every collected result and writes the answer, including any arithmetic | 1 |

*Table 1: The three nodes of a fixed plan and the LLM calls each one makes.*

One pure router drives the loop. After planning and after every execution it asks one question, whether the plan is empty:

```mermaid
flowchart LR
    P["Planner<br/>1 LLM call"] --> E["Executor<br/>search, no LLM"] --> D{"Plan<br/>empty?"}
    D -- no --> E
    D -- yes --> S["Synthesizer<br/>1 LLM call"]
```

*Figure 1: The fixed plan. Only the planner and the synthesizer call the model.*

Each step is a plain query. The executor needs no model, and the agent makes 2 LLM calls however long the plan is. ReAct makes one call per search plus one to answer, and each call re-reads the whole conversation, every earlier result included.

### A promise is not a tool call

A recorded comparison of four runs shows what ReAct's flexibility costs in reliability. On a three-capitals task, the ReAct agent stopped after the capitals in 4 of 4 runs. Each time it wrote *"Next, I will find the current population of the United States"* as text instead of a tool call. LangGraph's `tools_condition` ends the loop on any turn without a tool call. The promised search never ran.

We call this the **unkept promise**: ReAct keeps its to-do list in the model's head, and a turn of plain text ends the run. The planner wrote the missing lookup into its plan before the first search, where nothing could drop it.

### What each agent reads on a clean run

The [interactive lab](interactive/plan-or-react-lab.html) runs the comparison on the Larkspur cancellation question, with the reference prompts and the handbook chunks as search results. On clean runs, where every search returns the right chunk, the call and token counts are these:

| Lookups | ReAct calls | ReAct tokens | Fixed plan calls | Fixed plan tokens |
|---|---|---|---|---|
| 2 | 3 | ~362 | 2 | ~363 |
| 4 | 5 | ~918 | 2 | ~504 |
| 6 | 7 | ~1,676 | 2 | ~620 |

*Table 2: LLM calls and input tokens on clean runs, from the lab.*

The same numbers as a chart, with the replanning agent from the next section added:

![Line chart of tokens read against lookups for ReAct, the fixed plan and the replanning agent](diagrams/tokens-by-lookups.svg)

*Figure 2: Tokens read against lookups. ReAct's line bends upward because its prompt grows with every result.*

At two lookups the two agents read about the same. At six, ReAct reads 2.7 times as much, because its prompt grows with every result and it pays for that prompt on every call. Wall time is a different matter. In the fixed-plan comparison the searches dominate it and the executor runs them one after another. Either agent can be faster from run to run.

### When a plan fits

A plan suits steps you can list from the question, as in "find these four facts and compare them". ReAct suits work where the next step depends on what the last one found, as in troubleshooting a server that will not start. The decision fits in two questions:

```mermaid
flowchart TD
    Q{"Can you list the<br/>lookups from the<br/>question?"} -- no --> R["ReAct<br/>decide per step"]
    Q -- yes --> W{"Can a search<br/>return the wrong<br/>passage?"}
    W -- no --> F["Fixed plan<br/>2 LLM calls"]
    W -- yes --> RP["Plan, evaluate<br/>and replan"]
```

*Figure 3: Choosing between ReAct, a fixed plan and a plan that replans.*

The plan's weakness is the reverse of its strength. It was fixed before the first search, and nothing in the graph checks a result.

## Replanning

**Replanning** treats the plan as a living document: after every step an evaluator judges the result, and a failed step sends the run to a replanner that rewrites the steps still to come. The evaluator asks one structured question, *does this result state the fact the step asks for, about the right entity?* The notebook calls the verdict `StepEvaluation.satisfied`, and it goes into state with a one-sentence reason. Pure routers read it:

```mermaid
flowchart TD
    P[Plan] --> X["Execute next step<br/>then evaluate it"]
    X --> CAP{"iterations at<br/>max_iterations?"}
    CAP -- no --> OK{"Step<br/>satisfied?"}
    OK -- no --> RP["Replan from history<br/>and the reason"]
    RP --> X
    OK -- yes --> MORE{"Steps<br/>left?"}
    MORE -- yes --> X
    MORE -- no --> S[Synthesize]
    CAP -- yes --> S
```

*Figure 4: The replanning loop. The cap is checked before the verdict.*

Three rules make the loop safe:

- **A replan rewrites the remaining steps.** The replanner sees the goal, the history of OK and INSUFFICIENT steps and the reason the last one failed, then writes a new list of steps still to do. It is told never to resubmit a failed step unchanged.
- **Only accepted results reach the answer.** The synthesizer gets the satisfied results as data and is told to say a fact could not be found rather than fill it in from memory.
- **A cap ends the loop.** `max_iterations` counts executed steps. The router checks it before the verdict, which sends a run at the cap straight to the synthesizer.

### A wrong result becomes a revised search

In a controlled test, a stub search returns the U.S. state of Georgia for a question about the country. The evaluator marks the step INSUFFICIENT, the replanner rewrites the query and the next result is accepted. A fixed plan would have popped the step and written the state's 11 million people into the country's row. We call that the **silent wrong fact**: the search ran, the step counted as done and the answer is confidently wrong. A dead search tool, which never finds anything, runs until the cap and returns an honest "not found".

The lab plants the same failure in the Larkspur question: the search for the refund rule returns the `refund-timing` chunk. With four lookups the three agents end like this:

| Agent | LLM calls | Searches | Tokens read | Answer |
|---|---|---|---|---|
| ReAct, at its best | 6 | 5 | ~1,211 | Complete |
| Fixed plan | 2 | 4 | ~500 | One wrong fact |
| Plan and replan | 8 | 5 | ~1,582 | Complete |

*Table 3: Four lookups with one wrong first result, from the lab.*

### What a rejection costs

The replanner's bill follows from its graph: 1 planner call, 1 evaluator call per executed step, 1 replanner call per rejected step and 1 synthesizer call. Here is the arithmetic for N lookups and f wrong results under the cap:

| Part | Calls |
|---|---|
| Planner | 1 |
| Evaluator, one per executed step (N + f steps) | N + f |
| Replanner, one per rejected step | f |
| Synthesizer | 1 |
| **Total** | **N + 2 + 2f** |

*Table 4: LLM calls of the replanning agent.*

On a clean run that is N + 2, one more than ReAct, and the extra machinery changes nothing. The evaluator is the bottleneck. Too lenient, and wrong data slips through. Too strict, and the agent replans good results and pays 2 calls for each.

### Sizing the cap

The cap needs the same arithmetic. Six lookups with one wrong result need 7 executed steps. At the notebook's `max_iterations = 6`, the lab's run stops with one lookup unanswered after 9 LLM calls. At 7 it completes in 10, which is N + 2 + 2f with N = 6 and f = 1. We call this the **short cap**: a limit set from the plan's length that forgets a retry is an execution too.

ReAct has its own ceiling. The reference implementation runs it with `recursion_limit = 20` graph steps, and each search costs two (an agent turn and the tool). Six lookups with four wrong results need 10 searches and 21 steps, so LangGraph raises `GraphRecursionError` and the user gets no answer at all. Open the [plan or react lab](interactive/plan-or-react-lab.html), set six lookups with one wrong result and move the cap from 6 to 7:

<!-- lab: interactive/plan-or-react-lab.html -->

The lab's models are scripted. Its numbers are exact for these prompts and chunks and not for a live model. A real ReAct agent may stop early, as in the four-run comparison, and a real replanner may need more than one rewrite. The lab's numbers match the reference node and router code run under LangGraph with the same scripted models on all 1,764 settings.

## In practice: the cancellation assistant

For Larkspur's cancellation question, the choices above become four settings:

1. **Plan the lookups.** The six facts are known from the question, and a planner writes them as six queries.
2. **Evaluate every result.** Each search result must state the fact its step names, about the right subject (refund rule, not refund timing).
3. **Cap from the plan.** Six lookups plus one allowed retry gives `max_iterations = 7`, and the synthesizer reports any fact still missing.
4. **Count from state.** Log planned, executed and rejected steps per run. A rising replan rate then shows up before customers notice.

> **Key distinction:** the plan buys cheap, visible work, and the evaluator buys correctness. A plan without the evaluator saves calls and passes wrong results straight through.

Lesson 25.2 keeps the planner and replanner and hands each step to a whole research workflow instead of one search.

## Key Takeaways

- Use a plan when the steps are knowable from the question and ReAct when each step depends on the last result. ReAct can promise a search in text and stop, while a plan writes every lookup down.
- A fixed plan never checks a result, so a wrong search lands in the answer. Replanning evaluates each step and rewrites the remaining steps from the failure reason instead of retrying unchanged.
- Size caps from the call arithmetic: N + 2 + 2f calls for N lookups and f wrong results. The evaluator decides quality, since too lenient lets wrong data through and too strict replans good results.

## Check yourself

<details>
<summary>1. Why does the plan-and-execute agent make two LLM calls whatever the length of its plan?</summary>

The planner writes every step as a plain search query in one structured-output call, the executor runs each query with no LLM, and the synthesizer makes the one call that writes the answer. ReAct makes one call per search plus one to answer, and each call re-reads the whole conversation.

</details>

<details>
<summary>2. On clean runs with six lookups, how many tokens does ReAct read compared with the fixed plan, and why the gap?</summary>

About 1,676 against about 620, 2.7 times as much. ReAct's prompt grows with every result and it pays for that prompt on every call. At two lookups the two read about the same (about 362 and 363).

</details>

<details>
<summary>3. A replanning run with six lookups and one wrong result stops with one lookup unanswered. What caused it, and what fixes it?</summary>

The cap: `max_iterations = 6` counts executed steps, and six lookups with one wrong result need 7. The run stops after 9 LLM calls. At 7 it completes in 10. Size the cap from N + 2 + 2f calls for N lookups and f wrong results.

</details>

---
*Previous: [M25 overview](../README.md). Next: [25.2 Deep-research and reflective dynamic planners](../02_deep_research_and_reflective_dynamic_planners/README.md).*
