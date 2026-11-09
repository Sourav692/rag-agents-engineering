# M36.1 Theory: Blackboard architectures

*[M36 theory](../README.md) · Lesson 36.1 · Notebooks: [`01a_blackboard_intro.ipynb`](../../notebook/01a_blackboard_intro.ipynb), [`01b_blackboard_research_team.ipynb`](../../../optional/notebook/01b_blackboard_research_team.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: A controller that re-reads a shared board after every post can skip the branch a fixed pipeline always pays for -->

## Blackboard

> **What you'll learn**
>
> - **Explain** how a blackboard coordinates specialists through one shared store, with a controller as the only part that decides order.
> - **Compare** a blackboard controller with a fixed pipeline on a request whose next step depends on an earlier finding.
> - **Diagnose** the ways an LLM controller goes wrong: an invalid name, an impossible step, a loop that never finishes.
> - **Choose** between a blackboard, a pipeline and a fan-out by asking when the order of work is known.

M35 built supervisors and handoffs, where one agent passes control to the next. This module adds shared state: several specialists contribute to one record, and something decides who goes next.

Larkspur's support team gets an escalation: *a customer says their server went down twice this week. If the outages pushed availability below the 99.95% SLA, draft a service-credit reply, otherwise draft a reply that points to the status page and the root-cause report.* A fixed pipeline of analysts would run the credits analyst and the status analyst on every escalation, because its edges cannot skip a node. Half that work is wasted on each request, and the writer has to ignore one of the two reports.

A **blackboard system** coordinates specialists through one shared store, the **blackboard**. Specialists never call each other. Each one reads the board, does its own job and appends its result. A **controller** reads the whole board after every contribution and picks the next specialist, or `FINISH`:

```mermaid
flowchart LR
    R[/Request/] --> C{"Controller<br/>reads the board"}
    C -- next --> S["One specialist<br/>reads, works, posts"]
    S -- posts --> B[(Blackboard)]
    B --> C
    C -- FINISH --> A[/Reply/]
```
<!-- animated: diagrams/blackboard-loop.anim.html -->

*Figure 1: The blackboard loop. Every specialist turn sits between two controller turns.*

The design comes from the HEARSAY-II speech-recognition system (Erman et al., 1980). In HEARSAY-II the specialists watched the board for their own trigger conditions and a scheduler chose among them. In the reference implementations the controller does all the watching.

The controller is the only part that decides order. The specialists stay narrow, and adding one means adding a node and a name the controller may choose. Nothing else is rewired.

## Branching on what the board says

The intro notebook gives both designs one request with an either/or condition: find the latest news about a company, then run a technical analysis if the news is neutral or positive, or a financial analysis if it is negative. Here are both graphs, one row per design:

| Design | Order of work | Branches that run |
|---|---|---|
| Fixed pipeline | news, technical, financial, writer | Both, on every request |
| Blackboard | controller, news, controller, one analyst, controller, writer, controller | One, chosen after the news post lands |

*Table 1: The same conditional request through both designs. The pipeline's edges fix its order before the run starts.*

The notebook does not ask another model whether the instruction was followed. It computes two checks from `steps`, the list of specialists that ran:

| Check, computed from `steps` | Sequential pipeline | Blackboard |
|---|---|---|
| Followed the either/or | Never: both branches run by construction | Whatever this run's controller chose |
| Correct branch for the sentiment | Never: both branches run | Checked against a sentiment label from the news post |

*Table 2: The code-computed comparison. The pipeline fails by structure, the blackboard can fail by judgment.*

The blackboard row can fail too, because the controller is an LLM. A run where it calls both analysts, or the wrong one, shows up as a failed check instead of a plausible report. That is why the check runs on every run rather than once.

On the Larkspur escalation the same shape plays out with three specialists. An incident analyst posts what the incident log shows. The controller reads that post and calls either the credits analyst or the status analyst. A writer drafts the reply from the board.

## Guarding an LLM controller

A controller that re-decides at every step can also loop, stall or name a step that cannot run yet. We name the three failures and reuse the names:

- **Phantom route**: the controller names a specialist that does not exist.
- **Premature step**: it names a real specialist whose input is not on the board yet, such as a writer with no findings.
- **Runaway controller**: it keeps choosing specialists and never returns `FINISH`.

The reference implementations guard each one in code. The planted cases below come from the research-team notebook, which feeds hand-written boards to its pure guard functions with no model call. All six checks pass:

| Planted case | What the guard returned | Guard |
|---|---|---|
| Fact-Checker chosen on an empty board | Refused: there is no finding to check | Precondition |
| Outline-Writer chosen with 1 verified finding | Refused: fewer than 2 verified findings | Precondition |
| `FINISH` chosen with no draft | Refused: there is no draft yet | Precondition |
| A flagged finding followed by its revision | Only the revision counts as verified | Structured posts |
| Fallback after an unchecked finding | Fact-Checker | Rule-based next step |
| Fallback after a `needs_revision` verdict | Researcher | Rule-based next step |

*Table 3: Guard checks on hand-written blackboards, from a scratch run of the research-team notebook's pure functions.*

Four guards cover the three failures:

- **A typed decision** stops the phantom route. The decision field is a `Literal` of the specialist names plus `FINISH`, so the model can only name a real node. The node writes the decision to state, and a separate, pure routing function reads it.
- **Preconditions checked in code** stop the premature step. In the research-team implementation, `precondition_problem()` rejects impossible choices and `rule_based_next()` substitutes the rule-based choice. Every override is printed and counted.
- **A cap in code** stops the runaway controller. The intro notebook's controller returns `FINISH` without calling the model once `MAX_SPECIALIST_CALLS = 6` specialists have run (the research team allows 12 contributions). LangGraph's `recursion_limit` (20 in the intro, 40 in the research team) is only the backstop: it ends the run with an error rather than a clean stop.
- **Structured contributions** let code read the board. Posts in the research team are records with `agent`, `type` and `content`. Code can then tell a finding from a fact-check from a draft, and pair each finding with its own verdict.

Specialists that search must execute their tool. The intro notebook runs each analyst as a small `create_agent` loop. Binding a tool to the model alone only lets the model request a search, and nothing runs it.

> **Pitfall: an ungrounded fact-check.** The research team's Researcher and Fact-Checker have no search tool. The Fact-Checker judges clarity and internal consistency, and a fluent but wrong finding can still come out `verified`. Give the Researcher sources and have the Fact-Checker compare claims against them before trusting the label.

## What the controller costs

Every specialist turn sits between two controller turns. A run with `k` specialists makes up to `k + 1` controller calls on top of the specialists' own. For the Larkspur escalation that looks like this:

| Run | Specialist calls | Controller model calls |
|---|---|---|
| Incident analyst, credits analyst, writer | 3 | 4 |
| Pipeline running both analysts | 4 | 0 |
| Intro notebook at its cap | 6 | 6 (the seventh decision is made in code) |

*Table 4: Calls per run, counting each specialist as one call even when its own tool loop makes more. The first two rows are illustrative.*

The blackboard saves a specialist and pays for it in controller calls. That trade pays when the skipped specialist is expensive, such as a search loop, or when its output would mislead the writer.

Traces are harder to read than a pipeline's, because the path changes from run to run. In the research-team implementation a fact-check that flags a finding sends the controller back to the Researcher, a loop-back no edge in the graph spells out. The notebook counts loop-backs and overrides from the final board. A run with zero loop-backs is valid: every finding passed its first check.

## Choosing a coordination shape

The deciding question is when the next step becomes known:

```mermaid
flowchart TD
    Q{"Is the order known<br/>before the run?"} -- no --> B["Blackboard<br/>controller re-decides"]
    Q -- yes --> I{"Are the steps<br/>independent?"}
    I -- yes --> F["Fan-out<br/>lesson 36.5"]
    I -- no --> P["Fixed pipeline"]
```

*Figure 2: A blackboard earns its controller calls only when the order depends on what earlier steps find.*

| | Fixed pipeline | Fan-out | Blackboard |
|---|---|---|---|
| Who decides order | The graph's edges | The graph's edges | An LLM controller, every turn |
| Can skip a branch | ✗ | ✗ | ✓ |
| Extra model calls | None | None | Up to `k + 1` |
| Same path every run | ✓ | ✓ | ✗ |
| Main risk | Wasted branches | Joins and shared keys | Runaway or wrong choices |

*Table 5: Three coordination shapes for several specialists.*

Use a blackboard for diagnosis, triage and research with verification. When the order is known before the run starts, a pipeline or a fan-out ([lesson 36.5](../05_parallel_agents_async_nodes_and_streaming/README.md)) is cheaper and easier to test.

## In practice: Larkspur's outage escalation

1. **Board**: the request and the customer's account go on the board as the first post.
2. **Incident analyst** posts what the status page probes recorded for the customer's region this month, with the month's availability.
3. **Controller** reads that post. Below 99.95% it calls the credits analyst, which posts the credit owed (10% of the month's server charges in that region, 25% below 99.0%) and the rule that credits are claimed with a Billing ticket within 30 days. At or above 99.95% it calls the status analyst, which posts the status-page link and the 72-hour root-cause report.
4. **Writer** drafts from the board, and the controller returns `FINISH` once a draft exists.
5. **Checks in code**: exactly one of the two analysts ran, it matches the availability figure, and the run stayed under the call cap.

Lesson 36.2 swaps cooperation for disagreement: two agents argue opposite sides and a judge weighs them.

## Key Takeaways

- A blackboard coordinates specialists through one shared store, and only the controller decides order. It can pick one branch from what earlier posts found, where a fixed pipeline runs every branch by construction.
- Guard the controller in code: a typed `Literal` choice against phantom routes, precondition checks against premature steps, and a specialist-call cap against a runaway controller. `recursion_limit` is only the backstop, because it ends the run with an error.
- A run with `k` specialists makes up to `k + 1` controller calls, and its path changes from run to run. When the order is known before the run, a pipeline or fan-out is cheaper and easier to test.

## Check yourself

<details>
<summary>1. A request asks for a technical or a financial analysis depending on the news sentiment. Why does the fixed pipeline never follow it, while the blackboard can?</summary>

The pipeline's edges cannot skip a node, so news, technical, financial and writer run on every request and both analyses always happen. The blackboard controller reads the news analyst's post and then picks one branch. It can still choose wrong, because it is an LLM, and the implementation computes the check from `steps` on every run.

</details>

<details>
<summary>2. In the Larkspur outage escalation, the incident analyst posts that availability stayed above the 99.95% SLA. Which specialists should run next?</summary>

The controller should call the status analyst, not the credits analyst, and then the writer drafts a reply that points to the status page and the root-cause report. That run makes three specialist calls and four controller calls. A fixed pipeline would pay for both analysts on every escalation.

</details>

<details>
<summary>3. A blackboard controller keeps picking specialists and never returns FINISH. What in the implementations stops the run, and why is that better than relying on recursion_limit?</summary>

A cap in code: once `MAX_SPECIALIST_CALLS = 6` specialists have run, the controller returns `FINISH` without calling the model, and the run ends with a reply. `recursion_limit = 20` is only the backstop, and it ends the run with an error rather than a clean stop.

</details>

---
*Previous: [M36 overview](../README.md). Next: [36.2 Debate](../../../optional/theory/02_debate/README.md).*
