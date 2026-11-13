# M35.5 Theory: Handoffs and swarms

*[M35 theory](../README.md) · Lesson 35.5 · Notebooks: [`05a_agent_handoffs.ipynb`](../../notebook/05a_agent_handoffs.ipynb), [`05b_multi_agent_swarm.ipynb`](../../notebook/05b_multi_agent_swarm.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: An agent passes the conversation on with a tool call, the graph remembers who holds it, and follow-ups skip routing altogether -->
<!-- format: approved -->

## Start with a follow-up the supervisor routes again

> **What you'll learn**
>
> - **Distinguish** a handoff from a router by who holds control after an agent finishes.
> - **Explain** the handoff tool: a tool call that returns a command for the parent graph.
> - **Trace** one Larkspur thread across turns with the active agent saved by a checkpointer.
> - **Compare** the calls a swarm and a supervisor spend as follow-ups pile up.

Lesson 35.4's supervisor decides every step and takes control back each time. On a thread where the customer keeps talking to billing, it still pays a routing call before and after every answer.

A Larkspur customer asks about an outage and credits, then follows up with *Which invoice will the credit be on?* That second message belongs to billing, and billing already has the context. A supervisor routes it again from scratch: 3 calls for one answer. A **handoff** lets the agent holding the conversation pass it on itself, and lets the next message go straight to whoever holds it now.

## Handoffs

A router and a handoff both move a request between agents. They differ in who holds control afterwards:

| | Router or supervisor | Handoff |
|---|---|---|
| Who picks the next agent | the router, after every step | the agent holding the conversation, by calling a tool |
| Where control goes after an agent | back to the router, on a static edge | nowhere: the agent finishes the turn or hands off |
| The next user message starts at | the router | the active agent, read from `active_agent` in state |
| What stops a loop | the router's own cap | nothing built in; only `recursion_limit` |

*Table 1: Router against handoff.*

The difference shows on the follow-up turn:

```mermaid
flowchart TB
    subgraph SV["Supervisor, turn 2"]
        direction LR
        U1[/follow-up/] --> S1[supervisor] --> B1[billing] --> S2[supervisor] --> E1([end])
    end
    subgraph HO["Handoff, turn 2"]
        direction LR
        U2[/follow-up/] --> A2{"START reads<br/>active_agent"} --> B2[billing] --> E2([end])
    end
    SV ~~~ HO
```

*Figure 1: The same follow-up under each design. The supervisor spends two routing calls around billing's answer; the handoff graph's `START` router is code and calls no model.*

A structured-output classifier that sends each request to one specialist is still a router. A handoff needs three things: the agent itself chooses (a tool call), the parent graph moves control, and the choice is remembered.

### The handoff tool

A **handoff tool** is an ordinary tool that returns a `Command` instead of a string. It runs inside the calling agent's own graph, but the decision belongs to the parent graph that holds all the agents. The `Command` is addressed there. The handoff notebook calls one directly, with no model, for a customer charged twice. We ran that cell, unchanged, in langgraph 1.2.18:

| Field | Value returned | What it does |
|---|---|---|
| `goto` | `billing` | names the parent node to run next |
| `graph` | `__parent__` (`Command.PARENT`) | applies the command in the closest parent graph, which ends the calling agent's run |
| `update.messages` | the conversation plus a `ToolMessage` | the `ToolMessage` answers call `call_demo` and carries the note "Customer was charged twice for this month's subscription." |
| `update.active_agent` | `billing` | who answers the next message on this thread |

*Table 2: The `Command` a hand-built handoff tool returns (the notebook's direct-call cell).*

`InjectedState` gives the tool the agent's messages and `InjectedToolCallId` gives it the id of the call it answers. The model fills in one argument only: `context`, a note for the next agent, which spares the customer from being asked again. The parent's state is `MessagesState` plus `active_agent`. Its only routing of its own is at `START`: read `active_agent` and send the new message there, or to triage on a new thread.

### Following the active agent across turns

With a checkpointer, `active_agent` outlives the turn. Here is one Larkspur thread through triage and the specialists:

```mermaid
sequenceDiagram
    participant C as Customer
    participant T as Triage
    participant O as Operations
    participant B as Billing
    C->>T: Turn 1: server down, credits?
    T->>O: transfer_to_operations
    O->>B: transfer_to_billing
    B-->>C: answer (active: billing)
    C->>B: Turn 2: which invoice?
    B-->>C: answer
    C->>B: Turn 3: root-cause report?
    B->>O: transfer_to_operations
    O-->>C: answer (active: operations)
```
<!-- animated: diagrams/handoff-thread.anim.html -->

*Figure 2: One thread, three turns. Each handoff is one tool call that rewrites `active_agent`.*

Turn 2 is the point of the checkpointer: triage does not run, because `START` read `active_agent = billing` from the saved thread. Turn 3 moves sideways, billing to operations, with no coordinator involved. Billing has no incident section and has to recognise that and hand off.

The notebook proves the mechanism with a **scripted model**, LangChain's `GenericFakeChatModel` replaying fixed replies, tool calls included. We ran it:

| Turn | Customer | Agents that acted | `active_agent` after |
|---|---|---|---|
| 1 | "I was charged twice." | triage, then billing (via `transfer_to_billing`) | billing |
| 2 | "Will I get a confirmation?" | billing only | billing |

*Table 3: Two turns on one thread with a scripted model and no API call.*

### Planted failure: the handoff ping-pong

Nothing in this graph forces a stop. If agents keep deciding someone else should answer, they pass the request around until `recursion_limit` raises `GraphRecursionError`. Each agent run is one super-step of the parent graph. The notebook scripts that **handoff ping-pong** (triage to support to billing to triage, forever) and caps it:

<div class="learning-widget evidence-switcher" data-comparison id="limit-switcher">
<p class="widget-intro">Compare how the scripted handoff loop ends under each recursion limit.</p>
<div class="mode-controls" hidden role="group" aria-label="Recursion limit">
<button type="button" data-mode="ten" aria-pressed="false" aria-controls="limit-ten">10 (the demo cap)</button>
<button type="button" data-mode="twentyfive" aria-pressed="false" aria-controls="limit-twentyfive">25 (the notebook's runs)</button>
<button type="button" data-mode="none" aria-pressed="false" aria-controls="limit-none">No limit passed</button>
</div>
<section id="limit-ten" class="mode-panel" data-announcement="Limit 10 selected. 10 handoffs, then an error."><h4>recursion_limit = 10</h4><ul><li>10 handoffs: support, billing, triage, support, and so on.</li><li>Then <code>GraphRecursionError</code>, caught in code. We reran the cell: the count is exact.</li></ul></section>
<section id="limit-twentyfive" class="mode-panel" data-announcement="Limit 25 selected. The same error after 25 super-steps."><h4>recursion_limit = 25</h4><ul><li>Every real run in the notebook passes this limit.</li><li>The same loop would end the same way, after 25 super-steps.</li></ul></section>
<section id="limit-none" class="mode-panel" data-announcement="No limit selected. LangGraph's default of 10,007 super-steps."><h4>No limit passed</h4><ul><li>LangGraph's default of 10,007 super-steps applies.</li><li>In a live run each super-step is a model call, all spent before the error.</li></ul></section>
<p class="switch-status" aria-live="polite"></p>
</div>

The fix for a real ping-pong is ownership: one agent's prompt and tool descriptions must claim the topic. The limit only makes the failure fast and visible.

## Swarm

A **swarm** is the same mechanism packaged by the `langgraph-swarm` library. `create_handoff_tool` builds the tool, and `create_swarm` builds the parent graph with one node per agent and the `START` router. `SwarmState` is `MessagesState` plus `active_agent`, and `default_active_agent` names the agent a new thread starts at. Compile with a checkpointer and the swarm remembers, per `thread_id`, which agent holds each conversation.

```mermaid
flowchart LR
    S([START]) --> R{"active_agent<br/>saved?"}
    R -- no --> D["default agent<br/>(general QA)"]
    R -- yes --> A["that agent"]
    D -- "handoff tool" --> P["peer agent"]
    A -- "handoff tool" --> P
```

*Figure 3: The swarm's only routing of its own. Every other move is a handoff tool call.*

The swarm notebook builds three agents for a music store: a general QA agent that does RAG over company documents, an NL2SQL agent over the Chinook catalogue, and an invoice agent. Each gets its own tools plus handoff tools to the other two. Two details carry over to any swarm.

**The library tool carries no note.** It takes no arguments. Called directly in langgraph-swarm 0.1.0, it returns the same `goto`, `graph` and update keys as the hand-built tool, and its `ToolMessage` says only "Successfully transferred to billing". Whatever the next agent needs must already be in the conversation. The hand-built tool's `context` argument exists to fix that.

**Tools that run model-written queries must be safe whatever the model writes.** The NL2SQL connection reads only, three times over:

| Planted query | Result | Guard that refuses it |
|---|---|---|
| `DELETE FROM Invoice` | not authorized | `PRAGMA query_only = ON` and the authorizer |
| `ATTACH DATABASE ...` | not authorized | the authorizer (read-only flags alone allow `ATTACH`) |
| `PRAGMA query_only = OFF` | not authorized | the authorizer |

*Table 4: Writes and escapes sent through the query tool. The notebook checks all three on Chinook, and we reproduced the same authorizer on an in-memory database.*

The file itself is opened read-only too. The invoice tools go further: they run fixed queries with the customer ID bound as a parameter, never pasted into the SQL.

### Trace the outage thread through a swarm

A swarm spends routing once per thread. The [routing cost lab](interactive/routing-cost-lab.html) counts the outage thread with one follow-up:

<div class="walkthrough learning-widget" data-stepper id="swarm-walkthrough">
<p class="widget-intro">Step through the outage thread under a swarm. Each stage is one model call, as the lab counts it.</p>
<div class="step-controls" hidden role="group" aria-label="Swarm calls on the outage thread"><button type="button" data-step="0" aria-pressed="false" aria-controls="swarm-step-0">1. Triage</button><button type="button" data-step="1" aria-pressed="false" aria-controls="swarm-step-1">2. Operations</button><button type="button" data-step="2" aria-pressed="false" aria-controls="swarm-step-2">3. Billing</button><button type="button" data-step="3" aria-pressed="false" aria-controls="swarm-step-3">4. Follow-up</button></div>
<div class="step-panels"><section id="swarm-step-0" class="step-panel" aria-labelledby="swarm-heading-0"><h4 id="swarm-heading-0">1. Triage hands off</h4><dl><dt>Call</dt><dd>1, the thread's only routing call</dd><dt>State</dt><dd><code>active_agent</code> becomes operations</dd></dl></section><section id="swarm-step-1" class="step-panel" aria-labelledby="swarm-heading-1"><h4 id="swarm-heading-1">2. Operations answers, then hands off</h4><dl><dt>Call</dt><dd>2, answer plus <code>transfer_to_billing</code></dd><dt>State</dt><dd><code>active_agent</code> becomes billing; nobody takes control back</dd></dl></section><section id="swarm-step-2" class="step-panel" aria-labelledby="swarm-heading-2"><h4 id="swarm-heading-2">3. Billing answers the credit claim</h4><dl><dt>Call</dt><dd>3, answer</dd><dt>Turn 1 total</dt><dd>3 calls, 1 of them routing, against 5 for the supervisor</dd></dl></section><section id="swarm-step-3" class="step-panel" aria-labelledby="swarm-heading-3"><h4 id="swarm-heading-3">4. The follow-up goes straight to billing</h4><dl><dt>Call</dt><dd>4, answer; <code>START</code> read <code>active_agent = billing</code></dd><dt>Thread total</dt><dd>4 calls, against 8 for the supervisor</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

The lab runs the same three Larkspur requests through all four architectures, with the follow-up turns on a slider.

<!-- lab: interactive/routing-cost-lab.html -->

The lab's totals for the outage request as follow-ups pile up:

| Architecture | Request only | Plus 1 follow-up | Plus 3 follow-ups | Reaches billing |
|---|---|---|---|---|
| Router (M30) | 2 | 4 | 8 | No |
| Supervisor | 5 | 8 | 14 | Yes |
| Hierarchy | 7 | 12 | 22 | Yes |
| Swarm | 3 | 4 | 6 | Yes |

*Table 5: Model calls on the outage thread, from the routing cost lab. Each follow-up stays with billing.*

### Choosing a swarm or a supervisor

The swarm's saving rests on the conversation staying with one specialist. When a follow-up changes topic, the active agent has to recognise that and hand off, and routing quality now lives in every agent's prompt instead of one supervisor's. Choose the swarm when threads stay on one specialist's topic, and the supervisor when you need one decision log and one cap.

## Limits of this evidence

- **The lab counts a script, not a model.** Every handoff in its traces goes to the right agent the first time; a real agent can miss a topic change or hand off wrongly, which adds calls the lab does not show.
- **Live routes depend on the model.** The notebooks' four-customer and four-turn runs use `gpt-4o-mini`; only the direct tool calls, the scripted two turns and the ping-pong run without a model.
- **The SQL guard was rechecked off Chinook.** We reproduced the authorizer on an in-memory table, not the downloaded catalogue.

## References

1. LangChain, [Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs), LangChain documentation.
2. LangChain, [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence), LangGraph documentation.
3. LangChain, [langgraph-swarm](https://github.com/langchain-ai/langgraph-swarm-py), the library behind `create_swarm`.
4. OpenAI, [Swarm](https://github.com/openai/swarm), an educational framework for agent handoffs, 2024.
5. SQLite, [Compile-time authorization callbacks](https://www.sqlite.org/c3ref/set_authorizer.html).

## Key Takeaways

- A handoff tool returns `Command(goto=..., graph=Command.PARENT)` and sets `active_agent`. With a checkpointer, the next user message goes straight to the agent holding the conversation, with no router in between.
- Nothing in a swarm forces a stop, so agents can bounce a request until `recursion_limit` raises. Pass a note with each handoff, because the library tool carries none.
- A swarm spends routing once per thread: 6 calls for the outage request and 3 follow-ups, against 14 for a supervisor. The saving holds only while follow-ups stay on one specialist's topic.

## Check yourself

<details>
<summary>1. A structured-output classifier sends each Larkspur request to one specialist. Is that a handoff, and what would make it one?</summary>

No, it is still a router. A handoff needs the agent holding the conversation to choose the next agent by calling a tool, and the graph to remember the choice in `active_agent`. The handoff tool returns a `Command` with `graph=Command.PARENT`, so the parent graph runs the named agent next.

</details>

<details>
<summary>2. In the routing cost lab, how many model calls do the swarm, the supervisor and the hierarchy spend on the outage request plus 3 follow-ups?</summary>

6 for the swarm, 14 for the supervisor and 22 for the hierarchy. The swarm spends 3 calls on the first request and 1 per follow-up, because each follow-up goes straight to the active agent. The supervisor pays 3 per follow-up and the hierarchy 5.

</details>

<details>
<summary>3. In a langgraph-swarm build, the billing agent asks the customer again for details they already gave triage. Why?</summary>

The library's handoff tool takes no arguments and its `ToolMessage` says only "Successfully transferred", so it carries no note. Whatever the next agent needs must already be in the conversation. The hand-built tool's `context` argument exists to fix that.

</details>

---
*Previous: [35.4 Supervisors and hierarchical teams](../04_supervisors_and_hierarchical_teams/README.md). Next: [M35 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
