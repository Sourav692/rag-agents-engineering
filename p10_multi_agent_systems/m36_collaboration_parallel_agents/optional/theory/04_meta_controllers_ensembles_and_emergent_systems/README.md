# M36.4 Theory: Meta-controllers, ensembles and emergent systems

*[M36 theory](../../../mandatory/theory/README.md) · Lesson 36.4 · Notebooks: [`04a_meta_controller.ipynb`](../../notebook/04a_meta_controller.ipynb) (optional), [`04b_ensemble_parallel_exploration.ipynb`](../../notebook/04b_ensemble_parallel_exploration.ipynb) (optional), [`04c_cellular_automata.ipynb`](../../notebook/04c_cellular_automata.ipynb) (optional) · [All theory pages](../../../../../theory/README.md)*

## Three kinds of controller

Larkspur must decide whether a request needs a direct answer, live search, planning or debate. You will distinguish choosing an architecture from choosing a worker, compare independent votes with a final verdict and inspect the limit of controller-free local rules.

### Step 1: Choose what level the controller governs

A router, a meta-controller and a blackboard controller are all one structured-output call that picks from a fixed set. They differ in what they pick and how often:

| Controller | What it decides | When | Calls per request |
|---|---|---|---|
| Router | Which specialist answers, inside one fixed graph | Once, before any specialist runs | 1 |
| Meta-controller | Which whole architecture runs: one call, a search agent, a planner or a debate | Once, before any architecture runs | 1 |
| Blackboard controller (36.1) | Which specialist acts next, given the whole board | After every contribution, until done | Up to one per specialist turn, plus one |

A router differs from a handoff (M35) in who holds the decision: the router decides before any specialist runs, and the specialist cannot pass the request on. In a handoff the agent holding the conversation transfers it by calling a tool.

### Step 2: Dispatch through a typed strategy registry

The meta-controller wraps each architecture as a plain callable, `(query: str) -> str`, so it never sees inside one. Its decision is a `Strategy` Enum, and a registry maps each member to its callable instead of a chain of `if`s; a registry check catches a strategy with no callable. The example's four strategies, mapped onto Larkspur support traffic:

| Strategy | Shape of request | A Larkspur request of that shape |
|---|---|---|
| `direct_answer` | Self-contained fact the model already knows | "What is a vCPU?" (general knowledge, no handbook needed) |
| `search_agent` | Live or external information | "Is there an incident right now?" (only the live status page knows) |
| `multi_step_planning` | Several bundled sub-questions | The lab's refund, timing, export and credits question |
| `debate` | Trade-off with no single answer | "Should we move from a monthly to an annual plan?" |

### Step 3: Test a cascade from the wrong strategy

The main weakness is that classification errors cascade. A misrouted request still gets an answer, from the wrong specialist or architecture, and nothing downstream notices. The example's guard is a table of requests with the route each was written for, compared in code with the route each controller chose. That table is the regression test to run on every prompt or model change. One choice per request also cannot handle a mixture ("look up X, then debate whether it is a good idea"), and the classification call adds latency before any real work starts.

## Ensembles: vote against verdict

### Step 1: Compare independent votes with the aggregate decision

An ensemble runs several independent agents on the same question at the same time, each with a different persona, and an aggregator combines their conclusions. The example's committee has a bullish growth analyst, a cautious value analyst and a quantitative analyst, and a chief investment officer (CIO) who writes the recommendation.

```mermaid
flowchart LR
    S([Start]) --> G[Growth analyst]
    S --> V[Value analyst]
    S --> Q[Quant analyst]
    G & V & Q --> C["CIO<br/>list edge: waits for all three"]
```

The graph uses every piece of lesson 36.5. One edge from `START` to each analyst puts all three in one superstep. All three write the shared `analyses` key in that superstep, so it carries the `operator.or_` reducer, which merges their one-entry dicts. A list edge from the three analysts makes the CIO wait for every report.

### Step 2: Check overlap and vote-verdict consistency

The analysts never see each other's work, so none anchors on another. That independence is what an ensemble buys, and the example checks the parts that are easy to assume:

- **Overlap.** Each analyst records its start and end time. The check passes when all three windows were open at once.
- **Vote against verdict.** Each analyst ends its report with `Recommendation: Buy|Hold|Sell`, and the CIO's recommendation is a `Literal` of the same three values, so code can set the majority vote beside the verdict. A CIO that departs from the majority is fine if its summary says why. A CIO that departs with no reason given is the failure to look for.

For Larkspur, the same shape fits an answer review: three graders read one drafted reply, one for faithfulness to the retrieved chunks, one for tone, one for policy, and an aggregator decides whether it ships. Each grader costs its own model calls, so the committee is priced like three agents, while its latency is set by the slowest grader.

## Emergent systems

### Step 1: Trace synchronous updates without a controller

### Step 2: Follow a local rule to its global result

The cellular-automata example has no controller at all. Every cell of a warehouse grid is a small agent with one local rule: its distance to the packing station is 1 plus the smallest distance among its neighbours. Applied to every cell at once, tick after tick, the rule spreads a distance wave around the walls, and a carrier reaches the station by always stepping to the neighbour with the lowest value. The example checks the emergent paths against a global breadth-first search over the same grid, then walls off a cell next to the station and shows the path rerouting with no change to the code.

This is the far end of the control range in this module: no controller, only a local rule applied everywhere in synchronous ticks. It solves a global problem without a planner, at the cost of many cheap updates, and the example trusts the result only after the breadth-first check.

### Try it yourself

Give a live-status request to the meta-controller and check that it selects search rather than a direct answer. For the ensemble, compare the three Buy/Hold/Sell endings with the aggregator's verdict and inspect whether the analyst execution intervals overlap. Independence and a final consensus are separate observations.

### Practice notebook

Run the complete implementation from the practice material after checking the trace or calculation above. Use its stated environment for live model or server calls; recorded model choices and timings are observations, not guaranteed outputs.

- [Meta controller](../../notebook/04a_meta_controller.ipynb).
- [Ensemble parallel exploration](../../notebook/04b_ensemble_parallel_exploration.ipynb).
- [Cellular automata](../../notebook/04c_cellular_automata.ipynb).

### Continue learning

- [36.1](../../../mandatory/theory/01_blackboard_architectures/README.md#blackboard).

## Key Takeaways

- A router picks a specialist and a meta-controller picks a whole architecture, each once per request; a blackboard controller decides after every contribution. All three are one structured-output call over a fixed set.
- A misrouted request still gets an answer, and nothing downstream notices. Keep a table of requests with their intended routes and compare it in code on every prompt or model change.
- An ensemble runs independent agents in one superstep with a reducer on their shared key. Set the majority vote beside the aggregator's verdict, and flag a departure from the majority that gives no reason.

## Check yourself

<details>
<summary>1. A router and a meta-controller each make one structured-output call before any work starts. What does each one choose?</summary>

A router chooses which specialist answers inside one fixed graph. A meta-controller chooses which whole architecture runs (a direct answer, a search agent, a planner or a debate), each wrapped as a plain `(query: str) -> str` callable it never sees inside. A blackboard controller differs from both by deciding again after every contribution.

</details>

<details>
<summary>2. A Larkspur customer asks whether there is an incident right now. Which strategy should the meta-controller pick, and why not direct_answer?</summary>

`search_agent`, because only the live status page knows the answer. `direct_answer` suits a self-contained fact the model already knows, such as what a vCPU is. A misrouted request still gets an answer, which is why the implementation compares each chosen route with the route the request was written for.

</details>

<details>
<summary>3. All three ensemble analysts end with Buy, and the CIO recommends Hold. Is that a failure?</summary>

Only if the CIO's summary gives no reason. The CIO's recommendation is a `Literal` of the same three values, so code can set the majority vote beside the verdict. A CIO that departs from the majority and says why is fine; one that departs with no reason is the failure to look for.

</details>

---
*Previous: [36.3 STORM: multi-perspective research and writing](../../../mandatory/theory/03_storm_multi_perspective_research_and_writing/README.md). Next: [36.5 Parallel agents, async nodes and streaming](../../../mandatory/theory/05_parallel_agents_async_nodes_and_streaming/README.md).*
