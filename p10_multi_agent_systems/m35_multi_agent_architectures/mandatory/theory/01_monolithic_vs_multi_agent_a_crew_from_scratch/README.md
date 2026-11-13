# M35.1 Theory: Monolithic vs multi-agent; a crew from scratch

*[M35 theory](../README.md) · Lesson 35.1 · Notebooks: [`01a_multi_agent_vs_monolithic_agent.ipynb`](../../notebook/01a_multi_agent_vs_monolithic_agent.ipynb), [`01b_multiagent_pattern_from_scratch.ipynb`](../../../optional/notebook/01b_multiagent_pattern_from_scratch.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: When one agent with every tool should become a team of specialists, and how a fixed team runs its members in dependency order -->
<!-- format: approved -->

## Start with one agent that holds every tool

> **What you'll learn**
>
> - **Compare** a monolithic agent with a team of specialists on prompts, tool choice, model calls and latency.
> - **Explain** fan-out and fan-in, and why the team's latency is set by its slowest specialist.
> - **Diagnose** a comparison that rests on one judge score for one request.
> - **Trace** a crew of agents through a topological sort, and see why a cycle fails before any model runs.

M34 gave one agent a memory that lasts across sessions. This module asks a different question: when should the work be split across several agents at all?

Larkspur's support assistant is one agent with the whole handbook and every tool. A customer writes *My server went down last night. Do I get service credits?* On every step the agent chooses among billing, outage, export and sizing material in one long prompt. The question needs two parts of the handbook: the outage rules, then the credit rule (10% of the month's server charges when availability falls below 99.95%, claimed by ticket within 30 days). One prompt that covers everything has to get both parts right in one loop.

## When one agent becomes a team

A **monolithic agent** is one ReAct loop with one system prompt and every tool. A **specialist team** splits the request among agents that each have one domain, a narrow persona and a few tools, plus a step that merges their work. The comparison notebook builds both for a market report with three sections: news and sentiment, a technical read of the price trend, and financial performance.

```mermaid
flowchart TB
    S([START]) --> M["One ReAct agent<br/>one prompt, every domain<br/>web search, 3 results"]
    M --> M
    M --> E([END])
```

*Figure 1: The monolithic agent. One loop writes all three sections, and each step chooses among every tool and topic.*

The team gives each section its own ReAct agent with the same search tool, and a report writer merges their sections:

```mermaid
flowchart LR
    S([START]) --> N[News analyst]
    S --> T[Technical analyst]
    S --> F[Financial analyst]
    N --> W[Report writer]
    T --> W
    F --> W
    W --> E([END])
```

*Figure 2: The specialist team. The three analysts share one super-step, and the writer waits for all of them.*

The team runs as **fan-out and fan-in**: `START` has an edge to all three analysts, and each analyst has an edge to the writer. LangGraph runs nodes in **super-steps**. Every node whose inputs are ready runs in the same step, and the next step starts only when they have all finished. The three analysts share the first step and the writer runs in the second.

<div class="learning-widget evidence-switcher" data-comparison id="design-switcher">
<p class="widget-intro">Compare the two designs on the same market-report request. Each panel lists what that design costs and where you look when it fails.</p>
<div class="mode-controls" hidden role="group" aria-label="Agent design">
<button type="button" data-mode="monolith" aria-pressed="false" aria-controls="design-monolith">Monolithic agent (Figure 1)</button>
<button type="button" data-mode="team" aria-pressed="false" aria-controls="design-team">Specialist team (Figure 2)</button>
</div>
<section id="design-monolith" class="mode-panel" data-announcement="Monolithic agent selected. One prompt and one loop."><h4>Monolithic agent</h4><dl><dt>Prompts</dt><dd>One, covering every domain</dd><dt>Tool choice</dt><dd>Every tool, on every step</dd><dt>Model calls</dt><dd>One ReAct loop</dd><dt>Latency</dt><dd>Sequential: each section waits for the one before</dd><dt>Failure you debug</dt><dd>One long transcript</dd></dl></section>
<section id="design-team" class="mode-panel" data-announcement="Specialist team selected. Three loops in parallel and a synthesis call."><h4>Specialist team</h4><dl><dt>Prompts</dt><dd>One per specialist, each about one domain</dd><dt>Tool choice</dt><dd>A few tools per agent</dd><dt>Model calls</dt><dd>Three ReAct loops and a synthesis call, which the notebook puts at roughly four times the calls</dd><dt>Latency</dt><dd>The slowest analyst plus the synthesis call</dd><dt>Failure you debug</dt><dd>Which specialist went wrong, and whether the writer used its section</dd></dl></section>
<p class="switch-status" aria-live="polite"></p>
</div>

The call count follows from the shape. If every ReAct loop takes about the same number of calls, three loops plus one synthesis call come to roughly four times one loop. The notebook caps each loop with a `recursion_limit` of 12, which bounds how far any one analyst can run.

### Comparing the two reports fairly

The notebook does not declare a winner from one run. It measures both reports in two ways:

| Evidence | What it records | What it can claim |
|---|---|---|
| Code measures | word count, markdown headings, and whether the text covers news, technicals and financials (keyword checks such as "revenue" or "moving average") | facts about the text |
| Judge scores | 1 to 10 for clarity and structure, analytical depth and completeness, plus a justification | one model's opinion of one sample |

*Table 1: The two kinds of evidence. The judge scores each report as "the report" and never learns which design wrote it.*

We call the trap here the **single-sample verdict**. One request on one company is one sample, and a gap of a point or two on the judge alone is noise. When the code measures and the judge point the same way, the difference is worth testing on more requests. When only the judge prefers one report, it is not.

> **Key distinction:** a team buys focus and parallelism with more model calls. Whether it also buys better answers is an empirical question, settled by measuring many of your own requests.

For Larkspur the same test decides whether to split the support assistant into billing, operations and data agents that each search one part of the handbook. The price is a decision about which of them should answer, and the rest of this module is about that decision. First comes the simplest kind of team, one whose order is fixed before it runs.

## A crew is a dependency graph

The optional notebook rebuilds the core of CrewAI without a framework, on the raw OpenAI SDK. Two ideas carry it: an **Agent** and a **Crew**.

An agent has a backstory (its system prompt), a task description, an expected output and a context slot. Dependencies are declared with operators borrowed from Airflow:

| Declaration | Meaning | What happens at run time |
|---|---|---|
| `a >> b` | b depends on a | a's output lands in b's context, labelled "Output of a" |
| `b << a` | the same dependency, written the other way | the same |
| `a >> b >> c` | a chain | each agent feeds the next |
| `[a, b] >> c` | fan-in: c depends on both | c waits for both and reads both outputs |

*Table 2: The crew's dependency operators.*

A **crew** collects every agent created inside its block and runs them in **topological order**: an agent runs only after everything it depends on. The notebook sorts with Kahn's algorithm, which also detects cycles:

```mermaid
flowchart TD
    A["Queue agents<br/>with no dependencies"] --> B["Take one, add it<br/>to the run order"]
    B --> C["Release dependents<br/>whose inputs are met"]
    C --> D{"Queue empty?"}
    D -- no --> B
    D -- yes --> E{"Every agent<br/>sorted?"}
    E -- yes --> R[/Run in that order/]
    E -- no --> X[/ValueError: cycle/]
```

*Figure 3: Kahn's algorithm as the crew uses it. Agents caught in a cycle never reach the queue.*

### Sort the fan-in crew

Creating and sorting agents makes no model call, so we ran the notebook's `Agent` and `Crew` cells with a stub in place of the ReAct agent. Follow the fan-in crew `[pros, cons] >> editor`:

<div class="walkthrough learning-widget" data-stepper id="kahn-walkthrough">
<p class="widget-intro">Follow Kahn's algorithm on the fan-in crew. Each stage shows the queue, the run order so far and the editor's count of unmet inputs.</p>
<div class="step-controls" hidden role="group" aria-label="Sort stages"><button type="button" data-step="0" aria-pressed="false" aria-controls="kahn-step-0">1. Count</button><button type="button" data-step="1" aria-pressed="false" aria-controls="kahn-step-1">2. Take Pros</button><button type="button" data-step="2" aria-pressed="false" aria-controls="kahn-step-2">3. Take Cons</button><button type="button" data-step="3" aria-pressed="false" aria-controls="kahn-step-3">4. Take Editor</button></div>
<div class="step-panels"><section id="kahn-step-0" class="step-panel" aria-labelledby="kahn-heading-0"><h4 id="kahn-heading-0">1. Count each agent's dependencies</h4><dl><dt>Unmet inputs</dt><dd>Pros Analyst 0, Cons Analyst 0, Editor 2</dd><dt>Queue</dt><dd>Pros Analyst, Cons Analyst</dd><dt>Run order</dt><dd>empty</dd></dl></section><section id="kahn-step-1" class="step-panel" aria-labelledby="kahn-heading-1"><h4 id="kahn-heading-1">2. Take Pros Analyst</h4><dl><dt>Unmet inputs</dt><dd>Editor drops to 1</dd><dt>Queue</dt><dd>Cons Analyst</dd><dt>Run order</dt><dd>Pros Analyst</dd></dl></section><section id="kahn-step-2" class="step-panel" aria-labelledby="kahn-heading-2"><h4 id="kahn-heading-2">3. Take Cons Analyst</h4><dl><dt>Unmet inputs</dt><dd>Editor drops to 0 and joins the queue</dd><dt>Queue</dt><dd>Editor</dd><dt>Run order</dt><dd>Pros Analyst, Cons Analyst</dd></dl></section><section id="kahn-step-3" class="step-panel" aria-labelledby="kahn-heading-3"><h4 id="kahn-heading-3">4. Take Editor</h4><dl><dt>Queue</dt><dd>empty</dd><dt>Run order</dt><dd>Pros Analyst, Cons Analyst, Editor: all three sorted. The crew runs them in this order</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

A planted cycle shows the other exit. With `ping >> pong` and `pong >> ping`, both agents start with one unmet input, the queue starts empty, and the sort raises `ValueError: Circular dependencies detected among agents`. It fails at the sort, before any agent runs and before any model call. A crew is a fixed dependency graph, and a cycle has no topological order.

### The same crew as a StateGraph

The sort fixes an order and nothing more. In the crew, the pros and cons analysts still run one after the other, even though neither needs the other. The notebook's last part rebuilds the same fan-in as a LangGraph `StateGraph`, with stub nodes that log what they had seen:

| Super-step | Node | Had seen |
|---|---|---|
| 1 | cons | nothing |
| 1 | pros | nothing |
| 2 | editor | cons, pros |

*Table 3: The fan-in crew as a StateGraph (the notebook's bridge cell, run as written).*

The two analysts share a super-step and the editor runs once, with both entries in state. Each crew piece has a LangGraph counterpart: an agent is a node, `a >> b` is `add_edge("a", "b")`, `[a, b] >> c` is one edge from a list of nodes, the growing context string becomes typed state with a reducer, and the sort plus run becomes `compile()` and `invoke()`.

> **Pitfall: parallel in name only.** A dependency graph says what may run together. Whether it does is up to the runtime: Kahn's sort feeding a plain loop is sequential, and LangGraph's super-steps run ready nodes together.

LangGraph also adds what a fixed graph lacks: conditional edges, loops and checkpoints. Every architecture from lesson 35.2 on uses them to add a node that chooses the next agent at run time.

## Limits of this evidence

- **No live comparison.** The notebook ships without outputs, and this page quotes no judge scores or report lengths. The "roughly four times the calls" figure is the notebook's own estimate from the team's shape, not a measured count.
- **Stub runs.** The sort, the planted cycle and the StateGraph trace come from the notebook's cells run with stub agents and no model. They show order and wiring, not output quality.
- **Different domain.** The notebook compares market reports. The Larkspur split into billing, operations and data agents is an illustration of the same decision.

## References

1. A. B. Kahn, [Topological sorting of large networks](https://doi.org/10.1145/368996.369025), *Communications of the ACM*, 1962.
2. LangChain, [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api) (super-steps, edges and state reducers).
3. CrewAI, [documentation](https://docs.crewai.com/) (the framework the optional notebook rebuilds).

## Key Takeaways

- A specialist team gives each agent one domain and a few tools, at roughly four times the model calls of one ReAct loop. Running the specialists in one super-step keeps latency near the slowest one.
- Compare a team with a single agent using code measures and a judge that does not know which design wrote each report. A gap of a point or two on the judge from one request is noise.
- A crew is a fixed dependency graph run in topological order, and a cycle fails at the sort before any model is called. Choosing the next agent at run time is what the later architectures add.

## Check yourself

<details>
<summary>1. The specialist team makes roughly four times the monolithic agent's model calls. Why is its latency set by the slowest analyst, not the sum of all three?</summary>

`START` has an edge to all three analysts, so LangGraph runs them in the same super-step, in parallel. The report writer has an edge from each analyst and starts only when all three have finished. The time is the slowest analyst plus the synthesis call.

</details>

<details>
<summary>2. On one company, the team's report scores a point higher than the monolithic report from the judge. Is that enough to switch to the team?</summary>

No. One request on one company is one sample, and a gap of a point or two on the judge alone is noise. Check whether the code measures (word count, headings, topic coverage) point the same way, and repeat on more requests before deciding.

</details>

<details>
<summary>3. A crew declares writer >> reviewer and reviewer >> writer. What happens when you run it, and at which point?</summary>

The crew raises a `ValueError` at the topological sort, before any agent runs or any model is called. Kahn's algorithm never queues an agent caught in a cycle, and the sorted list comes up short. Choosing the next agent at run time, loops included, needs the graph-based patterns from lesson 35.2 on.

</details>

---
*Previous: [M35 overview](../README.md). Next: [35.2 The five multi-agent architectures and agent communication](../02_the_five_multi_agent_architectures_and_agent_communication/README.md).*
