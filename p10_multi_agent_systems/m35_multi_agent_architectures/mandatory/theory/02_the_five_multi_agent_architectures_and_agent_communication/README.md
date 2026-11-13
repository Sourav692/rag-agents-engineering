# M35.2 Theory: The five multi-agent architectures and agent communication

*[M35 theory](../README.md) · Lesson 35.2 · Notebooks: [`02a_five_multi_agent_architectures.ipynb`](../../notebook/02a_five_multi_agent_architectures.ipynb), [`02b_agent_communication.ipynb`](../../../optional/notebook/02b_agent_communication.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Five ways to decide which agent runs next, all built from one return value, and three ways for agents to pass work to each other -->
<!-- format: approved -->

## Start with a request that needs two specialists

> **What you'll learn**
>
> - **Explain** the one primitive under every LangGraph architecture: a node that writes to state and names the next node.
> - **Compare** network, supervisor, tool-calling supervisor, hierarchical and custom workflow by who decides what runs next.
> - **Diagnose** a runaway loop, and stop it with `recursion_limit`.
> - **Choose** what agents exchange: messages, typed fields or a draft and its critique.

Lesson 35.1 ended on a fixed graph: a crew whose order is known before it runs. Larkspur's support requests do not come in a fixed order. *How long does a refund take?* needs billing alone. *My server went down last night. Do I get service credits?* needs operations, then billing. The M30 router picks one knowledge base once, and on the outage request it answers the outage and never reaches the credits. Something has to decide, at run time, which agent runs next.

## Five architectures, one primitive

Every architecture in the routing notebook is built from one return value. A **`Command`** is what a node returns to do two jobs at once: write an update to state and name the node that runs next.

| Part | Example | What it decides |
|---|---|---|
| `goto` | `"writer"` | the next node, chosen at run time |
| `update` | `{"messages": [reply]}` | what this node writes to state |
| Return annotation | `Command[Literal["writer", "__end__"]]` | the nodes this one may jump to; LangGraph draws them as the graph's edges |

*Table 1: The fields of a `Command` and the annotation that declares its targets.*

`add_edge` fixes a path when the graph is built, and `Command(goto=...)` picks one at run time. Most real systems use both. A target listed in the annotation that the code never returns still appears as an edge, which is why the notebook keeps each `Literal` to the branches the function can take.

### The five shapes

The five architectures put different rules on that one capability. Each figure shows who holds the routing decision.

```mermaid
flowchart TB
    S([START]) --> R[Researcher]
    R --> W[Writer]
    W --> V[Reviewer]
    V -. "needs work" .-> W
    V -. done .-> E([END])
```

*Figure 1: Network. Each agent names the next one. The reviewer's hop back to the writer is wired by no `add_edge`.*

```mermaid
flowchart TB
    S([START]) --> SV{Supervisor}
    SV --> C[Content creator]
    SV --> ED[Editor]
    C --> SV
    ED --> SV
    SV --> E([END])
```

*Figure 2: Supervisor. One central node chooses every worker, and every worker reports back to it.*

```mermaid
flowchart TB
    U[/Request/] --> M{"Model chooses tools"}
    M --> B["billing_agent tool"]
    M --> T["technical_agent tool"]
    M --> G["general_agent tool"]
    B --> M
    T --> M
    G --> M
    M --> A[/Answer/]
```

*Figure 3: Tool-calling supervisor. Each specialist is a tool, and its docstring is the routing rule the model reads.*

```mermaid
flowchart TB
    S([START]) --> TOP{Top supervisor}
    TOP --> DEV{Dev team supervisor}
    TOP --> QA{QA team supervisor}
    DEV <--> BE[Backend]
    DEV <--> FE[Frontend]
    QA <--> TE[Tester]
    QA <--> SE[Security]
    DEV --> TOP
    QA --> TOP
```

*Figure 4: Hierarchical. A coordinator routes to team supervisors, and each team is a compiled graph of its own.*

```mermaid
flowchart TB
    S([START]) --> P[Parser] --> AN{Analyzer}
    AN -- text --> TP[Text processor]
    AN -- image --> IP[Image processor]
    TP --> SU[Summarizer]
    IP --> SU
    SU --> E([END])
```

*Figure 5: Custom workflow. Fixed stages with one branch, the only node whose `Literal` lists two targets.*

We ran the notebook's four `StateGraph` builds with the model replaced by a stub that answers "ok". Routing keys off role tags the code adds to each reply, never off the model's wording, so these are the paths a live run takes:

<div class="learning-widget evidence-switcher" data-comparison id="architecture-switcher">
<p class="widget-intro">Pick an architecture to see who decides what runs next, the messages its stub run wrote, and when to reach for it.</p>
<div class="mode-controls" hidden role="group" aria-label="Architecture">
<button type="button" data-mode="network" aria-pressed="false" aria-controls="arch-network">Network</button>
<button type="button" data-mode="supervisor" aria-pressed="false" aria-controls="arch-supervisor">Supervisor</button>
<button type="button" data-mode="tools" aria-pressed="false" aria-controls="arch-tools">Tool-calling supervisor</button>
<button type="button" data-mode="hierarchy" aria-pressed="false" aria-controls="arch-hierarchy">Hierarchical</button>
<button type="button" data-mode="custom" aria-pressed="false" aria-controls="arch-custom">Custom workflow</button>
</div>
<section id="arch-network" class="mode-panel" data-announcement="Network selected. Each agent decides."><h4>Network</h4><dl><dt>Who decides</dt><dd>Each agent, for itself</dd><dt>Stub run wrote</dt><dd>researcher, writer, reviewer, writer, reviewer: the reviewer sends the draft back once, then ends</dd><dt>Fails when</dt><dd>Nothing guarantees the run ends</dd><dt>Reach for it when</dt><dd>Agents need to negotiate</dd></dl></section>
<section id="arch-supervisor" class="mode-panel" data-announcement="Supervisor selected. One central node decides."><h4>Supervisor</h4><dl><dt>Who decides</dt><dd>One central node</dd><dt>Stub run wrote</dt><dd>creator, editor. The supervisor routes without appending a message. The transcript holds only the work</dd><dt>Fails when</dt><dd>The supervisor becomes a bottleneck</dd><dt>Reach for it when</dt><dd>Routing must be auditable</dd></dl></section>
<section id="arch-tools" class="mode-panel" data-announcement="Tool-calling supervisor selected. The model decides by choosing tools."><h4>Tool-calling supervisor</h4><dl><dt>Who decides</dt><dd>The model, by choosing tools. <code>InjectedState</code> hands each tool the graph's state without the model passing it</dd><dt>Stub run wrote</dt><dd>Not reproducible with a stub: routing needs a real model. The notebook's mixed query, a bill problem plus an app crash, may call one specialist or two from one run to the next</dd><dt>Fails when</dt><dd>The same input routes differently</dd><dt>Reach for it when</dt><dd>Intent classification is the hard part</dd></dl></section>
<section id="arch-hierarchy" class="mode-panel" data-announcement="Hierarchical selected. A coordinator over team coordinators decides."><h4>Hierarchical</h4><dl><dt>Who decides</dt><dd>A coordinator over team coordinators</dd><dt>Stub run wrote</dt><dd>backend, frontend, tester, security</dd><dt>Fails when</dt><dd>Step budgets grow and team internals are hidden</dd><dt>Reach for it when</dt><dd>The problem is shaped like an org chart</dd></dl></section>
<section id="arch-custom" class="mode-panel" data-announcement="Custom workflow selected. The graph decides, with one dynamic branch."><h4>Custom workflow</h4><dl><dt>Who decides</dt><dd>Mostly the graph, with one dynamic branch</dd><dt>Stub run wrote</dt><dd>parser, analyzer, text processor, summarizer</dd><dt>Fails when</dt><dd>The work is too open-ended for fixed paths</dd><dt>Reach for it when</dt><dd>The sequence is known in advance</dd></dl></section>
<p class="switch-status" aria-live="polite"></p>
</div>

The tool-calling supervisor needs no routing code. Its routing quality becomes a prompt and description problem, and you can no longer read the rules in code.

### Planted failure: the runaway loop

A network has no node that can say "stop". The notebook plants a **runaway loop**: two nodes, ping and pong, that hand off to each other forever. LangGraph counts super-steps and stops a run at `recursion_limit`:

| Setting | What happens to ping and pong |
|---|---|
| Default limit | 10,007 super-steps before `GraphRecursionError` |
| `recursion_limit = 25`, as every notebook run passes | `GraphRecursionError` after 25 super-steps; 0.002 s in our stub run |
| Hierarchy run | the notebook doubles the cap to 50, because each team spends steps of its own |

*Table 2: The ping-pong loop under each limit. The default comes from LangGraph's installed source.*

The limit caps steps, not time. Twenty-five steps of a graph that calls a model at every node is still slow. Treat the limit as a guard against runaway loops, not a timeout. Pass it on every run.

For Larkspur, the choice comes down to a few questions in order:

```mermaid
flowchart TD
    A{"Order of steps<br/>known in advance?"} -- yes --> CW["Custom workflow<br/>fixed edges, one branch"]
    A -- no --> B{"Should an agent pass<br/>the conversation on?"}
    B -- yes --> SW["Handoffs and swarm<br/>(35.5)"]
    B -- no --> C{"Must peers negotiate<br/>with no one in charge?"}
    C -- yes --> N["Network<br/>peers name the next agent"]
    C -- no --> D{"Too many specialists<br/>for one supervisor?"}
    D -- yes --> H["Hierarchical<br/>supervisors over teams"]
    D -- no --> S["Supervisor<br/>(35.4)"]
```

*Figure 6: Choosing an architecture. Each "no" moves one question down.*

The support assistant's order is not known in advance (a question may need one specialist or two), so it starts at the second question. The answer depends on whether conversations stay with one specialist across turns. A swarm is a network in which the handoffs are tools and the graph remembers who holds the conversation. Lesson 35.4 builds the supervisor and the hierarchy, and lesson 35.5 builds the swarm. Who runs next is half the design, and the next section covers the other half.

## Agent communication

While agents run, they pass work to each other through state. The optional notebook builds three patterns for that:

```mermaid
flowchart TB
    subgraph MP["Message passing"]
        direction LR
        R1[Researcher] -- messages --> F1[Fact checker] -- messages --> S1[Summarizer]
    end
    subgraph TF["Typed fields"]
        direction LR
        C2[Collector] -- raw_data --> A2[Analyst] -- "analysis, confidence" --> AD[Advisor]
    end
    subgraph GC["Generator and critic"]
        direction LR
        D3[Drafter] -- drafts --> C3[Critic] -- critiques --> D3
    end
    MP ~~~ TF
    TF ~~~ GC
```

*Figure 7: Three ways to exchange work. One shared transcript, one field per stage, or a draft list and a critique list.*

| Pattern | State | Each agent reads | Trade-off |
|---|---|---|---|
| Message passing | one `messages` list with the `add_messages` reducer | the whole conversation so far | simple and transparent, but every agent re-reads and parses prose |
| Typed fields | one field per stage (`raw_data`, `analysis`, `confidence_score`, `recommendations`) | only the fields it needs | structured output fills each field with a validated Pydantic object, and the schema is rigid |
| Generator and critic | running lists of `drafts` and `critiques` (`operator.add`) | the last draft and the feedback on it | iterates to a better draft and needs a cap |

*Table 3: Three ways agents exchange work.*

With typed fields, a malformed reply fails validation instead of silently becoming a wrong value. The analyst's confidence must lie between 0.0 and 1.0, and the collector must return points with a source and a finding. Downstream agents read those fields directly and parse nothing.

### A critic that quotes its evidence

The generator and critic loop shows how to keep a model from ending its own loop. A critic that answers yes or no can approve a draft that misses a criterion, and nothing checks it. We call this the **lenient critic**. The notebook's critic never gives the verdict. For each of three criteria (a named LangGraph feature, a concrete use case, a trade-off) it copies the sentence from the draft that meets it, or writes `none`. Code computes the verdict:

```mermaid
flowchart LR
    D[Drafter] --> C["Critic<br/>quotes evidence<br/>per criterion"]
    C --> V{"Code: every quote<br/>found in the draft?"}
    V -- yes --> OK[/Approved/]
    V -- no --> K{"Under<br/>MAX_ITERATIONS?"}
    K -- yes --> D
    K -- no --> X[/Capped/]
```

*Figure 8: The generator and critic loop. The model supplies quotes, and code decides.*

We ran the notebook's check function on a three-sentence Larkspur draft ("LangGraph checkpointers let a support thread resume. A billing agent and an outage agent can share one graph. The cost is more model calls per request.") with planted critiques:

| Planted critique | Missing criteria returned | Why |
|---|---|---|
| All three sentences quoted exactly | none | every quote is in the draft, and the feature quote names "checkpoint" |
| Trade-off quote invented ("It is slower than plain code.") | trade-off | the quote is not in the draft |
| Use-case quote is `none` | use case | `none` counts as missing |
| Feature quote is the use-case sentence | feature | the quote names no feature from the notebook's list |
| A critic that always answers `none`, in the full loop | all three | the loop stops after 3 drafts with `capped` set |

*Table 4: The critic check on planted critiques (notebook functions run with a stub model).*

An invented quote cannot pass, because membership in the draft is tested in code. `MAX_ITERATIONS = 3` ends the loop whether or not the critic ever approves.

> **Key distinction:** this loop is not a blackboard. Its order is fixed (draft, critique, draft), and only the exit is decided at run time. A blackboard has a controller that picks which of several specialists acts next from what is on the shared board. M36 builds one.

## Limits of this evidence

- **Stub paths.** The message orders come from the notebook's graphs with a model that always answers "ok". They show routing, which keys off role tags, not answer quality.
- **Tool-calling routes are not reproduced.** That supervisor routes on the model's tool choice, which a stub cannot make. Its panel describes the notebook's claim instead of a run.
- **Timing.** The 0.002 s loop is one stub run on one laptop. With a model at every node, 25 steps take as long as 25 model calls.

## References

1. LangChain, [Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent) (supervisor, tool-calling and handoff patterns).
2. LangChain, [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api) (`Command`, super-steps and the recursion limit).
3. LangChain, [Use the graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api) (state reducers and conditional edges).

## Key Takeaways

- Build every architecture from one primitive, a node returning `Command(goto=..., update=...)`. `add_edge` fixes a path at build time, `Command` picks one at run time, and most systems use both.
- Pick the architecture by who should decide what runs next. Use a custom workflow when the order is known, handoffs when the conversation should move with an agent, and a supervisor when routing must be auditable.
- Always pass `recursion_limit`, since the default is 10,007 super-steps. In a generator and critic loop, have the critic quote evidence per criterion, compute the verdict in code and cap the iterations.

## Check yourself

<details>
<summary>1. What does a node return to choose the next agent at run time, and how does LangGraph know which edges to draw for it?</summary>

It returns `Command(goto="writer", update={...})`: the update goes into state and the named node runs next. The return annotation, such as `Command[Literal["writer", "__end__"]]`, lists the nodes it may jump to, and LangGraph draws those as edges. `add_edge` fixes a path at build time, while `Command(goto=...)` picks one at run time.

</details>

<details>
<summary>2. Larkspur's support assistant may need one specialist or two, so the order is not known in advance. Which question then decides between a swarm and a supervisor?</summary>

Whether an agent should pass the conversation on, which comes down to whether conversations stay with one specialist across turns. If yes, use handoffs and a swarm (35.5). If no, and peers need not negotiate and one supervisor can handle the specialists, use a supervisor (35.4).

</details>

<details>
<summary>3. A yes-or-no critic sometimes approves drafts that miss a criterion. How does the notebook's critic design prevent that, and what ends the loop?</summary>

The critic never gives the verdict. For each of three criteria it quotes the sentence from the draft that meets it, or writes `none`. Code checks that each quote is really in the draft and computes the verdict. An invented quote counts as missing. `MAX_ITERATIONS = 3` ends the loop whether or not the critic approves.

</details>

---
*Previous: [35.1 Monolithic vs multi-agent; a crew from scratch](../01_monolithic_vs_multi_agent_a_crew_from_scratch/README.md). Next: [35.3 Supervisor workflow with human review](../../../optional/theory/03_supervisor_workflow_with_human_review/README.md).*
