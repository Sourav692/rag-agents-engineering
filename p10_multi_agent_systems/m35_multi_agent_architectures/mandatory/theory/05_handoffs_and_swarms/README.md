# M35.5 Theory: Handoffs and swarms

*[M35 theory](../README.md) · Lesson 35.5 · Notebooks: [`05a_agent_handoffs.ipynb`](../../notebook/05a_agent_handoffs.ipynb), [`05b_multi_agent_swarm.ipynb`](../../notebook/05b_multi_agent_swarm.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: An agent passes the conversation on with a tool call, the graph remembers who holds it, and follow-ups skip routing altogether -->

## Handoffs

> **What you'll learn**
>
> - **Distinguish** a handoff from a router by who holds control after an agent finishes.
> - **Explain** the handoff tool: a tool call that returns a command for the parent graph.
> - **Trace** one Larkspur thread across turns with the active agent saved by a checkpointer.
> - **Compare** the calls a swarm and a supervisor spend as follow-ups pile up.

Lesson 35.4's supervisor decides every step and takes control back each time. On a thread where the customer keeps talking to billing, it still pays a routing call before and after every answer.

A Larkspur customer asks about an outage and credits, then follows up with *Which invoice will the credit be on?* That second message belongs to billing, and billing already has the context. A supervisor routes it again from scratch. A **handoff** lets the agent holding the conversation pass it on itself, and lets the next message go straight to whoever holds it now.

A router and a handoff both move a request between agents. They differ in who holds control afterwards:

| | Router or supervisor | Handoff |
|---|---|---|
| Who picks the next agent | the router, after every step | the agent holding the conversation, by calling a tool |
| Where control goes after an agent | back to the router, on a static edge | nowhere: the agent finishes the turn or hands off |
| The next user message starts at | the router | the active agent, read from `active_agent` in state |
| What stops a loop | the router's own cap | nothing built in; only `recursion_limit` |

*Table 1: Router against handoff.*

A structured-output classifier that sends each request to one specialist is still a router. A handoff needs three things: the agent itself chooses (a tool call), the parent graph moves control, and the choice is remembered.

### The handoff tool

A **handoff tool** is an ordinary tool that returns a `Command` instead of a string. It runs inside the calling agent's own graph, but the decision belongs to the parent graph that holds all the agents. The `Command` is addressed there. The handoff notebook calls one directly, with no model, for a customer charged twice. We ran that cell:

| Field | Value returned | What it does |
|---|---|---|
| `goto` | `billing` | names the parent node to run next |
| `graph` | `__parent__` (`Command.PARENT`) | applies the command in the closest parent graph, which ends the calling agent's run |
| `update.messages` | the conversation plus a `ToolMessage` | the `ToolMessage` answers call `call_demo` and carries the note "Customer was charged twice for this month's subscription." |
| `update.active_agent` | `billing` | who answers the next message on this thread |

*Table 2: The `Command` a hand-built handoff tool returns (the notebook's direct-call cell).*

`InjectedState` gives the tool the agent's messages and `InjectedToolCallId` gives it the id of the call it answers. The model fills in one argument only: `context`, a note for the next agent so the customer is not asked again. The parent's state is `MessagesState` plus `active_agent`. Its only routing of its own is at `START`: read `active_agent` and send the new message there, or to triage on a new thread.

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

*Figure 1: One thread, three turns. Each handoff is one tool call that rewrites `active_agent`.*

Turn 2 is the point of the checkpointer: triage does not run, because `START` read `active_agent = billing` from the saved thread. Turn 3 moves sideways, billing to operations, with no coordinator involved. Billing has no incident section and has to recognise that and hand off.

The notebook proves the mechanism with a **scripted model**, LangChain's `GenericFakeChatModel` replaying fixed replies, tool calls included. We ran it:

| Turn | Customer | Agents that acted | `active_agent` after |
|---|---|---|---|
| 1 | "I was charged twice." | triage, then billing (via `transfer_to_billing`) | billing |
| 2 | "Will I get a confirmation?" | billing only | billing |

*Table 3: Two turns on one thread with a scripted model and no API call.*

### Planted failure: the handoff ping-pong

Nothing in this graph forces a stop. If agents keep deciding someone else should answer, they pass the request around until `recursion_limit` raises `GraphRecursionError`. Each agent run is one super-step of the parent graph. The notebook scripts that **handoff ping-pong** (triage to support to billing to triage, forever) and caps it:

| Setting | Result |
|---|---|
| `recursion_limit = 10` (the demo cap) | 10 handoffs, then `GraphRecursionError` |
| `recursion_limit = 25` (every real run in the notebook) | would end the same way, after 25 super-steps |
| No limit passed | LangGraph's default of 10,007 super-steps, each one a model call in a live run |

*Table 4: The scripted handoff loop under each limit.*

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

*Figure 2: The swarm's only routing of its own. Every other move is a handoff tool call.*

The swarm notebook builds three agents for a music store: a general QA agent that does RAG over company documents, an NL2SQL agent over the Chinook catalogue, and an invoice agent. Each gets its own tools plus handoff tools to the other two. Two details carry over to any swarm.

**The library tool carries no note.** It takes no arguments. Called directly, it returns the same `goto`, `graph` and update keys as the hand-built tool, and its `ToolMessage` says only "Successfully transferred to billing". Whatever the next agent needs must already be in the conversation. The hand-built tool's `context` argument exists to fix that.

**Tools that run model-written queries must be safe whatever the model writes.** The NL2SQL connection reads only, three times over:

| Planted query | Result | Guard that refuses it |
|---|---|---|
| `DELETE FROM Invoice` | not authorized | `PRAGMA query_only = ON` and the authorizer |
| `ATTACH DATABASE ...` | not authorized | the authorizer (read-only flags alone allow `ATTACH`) |
| `PRAGMA query_only = OFF` | not authorized | the authorizer |

*Table 5: Writes and escapes sent through the query tool. The notebook checks all three on Chinook, and we reproduced the same authorizer on an in-memory database.*

The file itself is opened read-only too. The invoice tools go further: they run fixed queries with the customer ID bound as a parameter, never pasted into the SQL.

### What a swarm saves

A swarm spends routing once per thread. On the outage request, triage hands off to operations, operations answers its part and hands off to billing: 3 model calls, one of them routing, against 5 for a supervisor. After that, each follow-up goes straight to the active agent for 1 call. The [routing cost lab](interactive/routing-cost-lab.html) runs the same three Larkspur requests through all four architectures, with the follow-up turns on a slider.

<!-- lab: interactive/routing-cost-lab.html -->

The lab's totals for the outage request as follow-ups pile up:

| Architecture | Request only | Plus 1 follow-up | Plus 3 follow-ups | Reaches billing |
|---|---|---|---|---|
| Router (M30) | 2 | 4 | 8 | ✗ |
| Supervisor | 5 | 8 | 14 | ✓ |
| Hierarchy | 7 | 12 | 22 | ✓ |
| Swarm | 3 | 4 | 6 | ✓ |

*Table 6: Model calls on the outage thread, from the routing cost lab. Each follow-up stays with billing.*

The swarm's saving rests on the conversation staying with one specialist. When a follow-up changes topic, the active agent has to recognise that and hand off, and routing quality now lives in every agent's prompt instead of one supervisor's. Choose the swarm when threads stay on one specialist's topic, and the supervisor when you need one decision log.

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
