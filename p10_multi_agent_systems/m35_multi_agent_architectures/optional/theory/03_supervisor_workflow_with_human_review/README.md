# M35.3 Theory: Supervisor workflow with human review

*[M35 theory](../../../mandatory/theory/README.md) · Lesson 35.3 · Notebooks: [`03a_supervisor_workflow_with_human_review.ipynb`](../../notebook/03a_supervisor_workflow_with_human_review.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: A supervisor that routes each draft to the specialist that fixes its first failing check, and a pause where a person can edit the result before it ships -->

## Human review in a supervisor loop

> **What you'll learn**
>
> - **Explain** a supervisor loop that grades a draft and routes it to the first failing check.
> - **Separate** checks code can do exactly from checks that need a model's judgement.
> - **Trace** a draft through the loop, the pass cap and the single place the approved output is written.
> - **Choose** between a static pause on every run and a dynamic pause that only some runs take.

Lesson 35.2 sketched a supervisor with hard-coded routing. This lesson gives it real specialists, a grader and a person at the end.

Larkspur's billing agent drafts refund replies. An annual plan gets a full refund within 30 days of purchase if the account used less than 100 GB of outbound traffic. After day 30 the refund is prorated, minus a 15% early-termination fee. A reply that promises a full refund on day 45 commits Larkspur to money the handbook does not allow. Someone has to read those replies before the customer does. The pattern needs three parts: a loop that keeps fixing a draft until it meets its rules, a cap on that loop, and a pause for review.

The notebook builds the same pattern on news articles. A short transfer rumour ("Lionel Messi will join Real Madrid in 2025") has to become a publishable article. A supervisor, the "news chef", grades the article and routes it to the specialist that can fix what is missing. A person reads the result before it is published.

### Grading in code and in a model

An article passes when four checks pass. The notebook splits them by who can check each one reliably:

| Check | Checked by | Specialist that fixes it |
|---|---|---|
| About football transfers | model, structured output | none: an off-topic article ends the run |
| Mentions the market value | model, structured output | `market_value_researcher` (a one-tool agent over a small lookup table) |
| Mentions the current club | model, structured output | `current_club_researcher` (the same shape) |
| At least 100 words | code, by counting words | `word_count_rewriter` (asked for at least 120 words) |

*Table 1: The four publication checks. Only the word count never reaches a model.*

**Grade in code what code can check.** Topic, club and value need judgement. The word count is exact, and a model asked to count words is a second source of error. Each researcher's first model call is also forced to call its tool and cannot skip the lookup to answer from a guess.

After every specialist, control returns to the news chef, which grades the updated article again:

```mermaid
flowchart TD
    R[/Rumour/] --> G{"News chef grades:<br/>first failing check?"}
    G -- market value --> MV["market_value_<br/>researcher"]
    G -- club --> CL["current_club_<br/>researcher"]
    G -- length --> TW["word_count_<br/>rewriter"]
    MV --> G
    CL --> G
    TW --> G
    G -- "all pass" --> FA["final_article set<br/>run pauses"]
    FA --> H{"Human reviews,<br/>may edit"}
    H --> P[/Publish/]
```

*Figure 1: The supervisor loop and the review step. Every specialist reports back to the news chef.*

The chef routes to the **first failing check**, in a fixed order: market value, then club, then length. An off-topic article ends the run at once.

### Tracing a rumour through the loop

We ran the notebook's workflow graph with the model-backed pieces replaced by stubs: a grader that checks for "join", "€" and "Inter Miami", researchers that return the lookup-table values, and a rewriter that pads the text past 100 words. The routing, the word count and the cap are the notebook's own code:

| Pass | Checks failing | Routed to |
|---|---|---|
| 1 | value, club, length | `market_value_researcher` (adds €50 million) |
| 2 | club, length | `current_club_researcher` (adds Inter Miami) |
| 3 | length | `word_count_rewriter` |
| 4 | none | end; `final_article` set (120 words) |

*Table 2: The rumour through the loop (stubbed grader and specialists, notebook routing).*

Two more inputs complete the picture. "Today in Munich will be 9°C" fails the topic check on pass 1 and ends with no article. A 109-word article that already names the club and the value passes on pass 1, and no specialist runs.

Two guards keep the loop safe to run unattended up to the human step:

- **A pass cap.** `MAX_PASSES = 5`. A live grader sometimes marks a check "no" twice, and the same specialist runs again. A grader that never says "yes" cannot keep the loop going past five passes.
- **One place for the output.** Only a full pass copies the article into `final_article`. The published text is always the version that passed, whether or not any specialist ran. The 109-word article reaches publication unchanged for that reason.

The planted failure here is the **stale output**: a variable set before the last specialist ran, published after it. Writing the output in exactly one place, on a full pass, rules it out.

## Pausing before publication

The workflow becomes one node of an outer graph, followed by a node that publishes. Compiling the outer graph with a checkpointer and `interrupt_after=["newsagent_node"]` pauses every run after the article is written:

```mermaid
sequenceDiagram
    participant W as Workflow node
    participant C as Checkpointer
    participant R as Reviewer
    participant P as Publish node
    W->>C: answer saved, run pauses
    R->>C: read state, edit with update_state
    R->>P: resume with invoke(None)
    P-->>R: publishes the saved answer
```

*Figure 2: A static pause. The reviewer works on the saved state, and the run resumes from the pause.*

The notebook runs three threads to the pause and resumes each one, which we reproduced with the stubbed workflow:

| Thread | Answer at the pause | Reviewer action | Published |
|---|---|---|---|
| weather | "Article not relevant for news agency" | resume as is | the same text |
| messi | the four-pass article | `update_state` sets "Fake news!!!" | "Fake news!!!" |
| clean | the 109-word article | resume as is | the article, word for word |

*Table 3: Three paused threads (notebook review graph, stubbed workflow).*

The edited answer reaches the publishing call, not the model's. The checkpointer holds each thread's state by `thread_id`, and the reviewer can take the threads in any order.

### Static or dynamic review

`interrupt_after` is **static**: fixed at compile time, it pauses every run at the named node. A **dynamic** pause calls `interrupt(payload)` inside a node, which pauses only when the node decides to and shows the reviewer the payload. The run resumes with `Command(resume=...)`.

| | Static `interrupt_after` | Dynamic `interrupt(payload)` |
|---|---|---|
| Decided | at compile time | at run time, inside the node |
| Pauses | every run at that node | only the runs the node chooses |
| Reviewer sees | the saved state | the payload the node sends |
| Resume | `invoke(None)` after any `update_state` | `Command(resume=...)` |

*Table 4: Two ways to put a person in the loop.*

Larkspur needs the dynamic kind. A refund inside the 30-day window can go straight to the customer, and one outside it pauses for a person. The check that decides to pause compares the purchase date with today in code, for the same reason the word count does. A static pause would stop every refund reply, including the ones the handbook already allows.

## Key Takeaways

- Grade in code whatever code can check exactly, such as word count, and use a model with structured output only for checks that need judgement. Route to the first failing check and cap the passes.
- Write the published output in one place, set only on a full pass, so the text that ships is always the version that passed.
- A static `interrupt_after` pauses every run at a node, while a dynamic `interrupt(payload)` pauses only when the node decides. Use the dynamic kind for a refund outside the 30-day window, and compare the dates in code.

## Check yourself

<details>
<summary>1. Why does the news chef use a model to judge topic, club and market value, but leave the 100-word check to code?</summary>

Topic, club and market value need judgement, so a model answers them with structured output. The word count is exact. Code computes it and the model is never asked. A check that code can do exactly should never depend on a model's answer.

</details>

<details>
<summary>2. An article names the player's current club but has no market value and only 80 words. Which specialists run, and in what order?</summary>

The news chef routes to the first failing check, in the order market value, club, length. `market_value_researcher` runs first. Control returns to the chef, which grades again. The club passes, and `word_count_rewriter` runs next. `MAX_PASSES = 5` caps the loop if a check keeps failing.

</details>

<details>
<summary>3. Larkspur wants a person to review only refunds proposed outside the 30-day window. Should it use a static interrupt_after or a dynamic interrupt?</summary>

A dynamic `interrupt(payload)` inside the node. A static `interrupt_after` is fixed at compile time and pauses every run, while the dynamic one pauses only when the node decides to, and the run resumes with `Command(resume=...)`. The check that decides to pause compares the dates in code.

</details>

---
*Previous: [35.2 The five multi-agent architectures and agent communication](../../../mandatory/theory/02_the_five_multi_agent_architectures_and_agent_communication/README.md). Next: [35.4 Supervisors and hierarchical teams](../../../mandatory/theory/04_supervisors_and_hierarchical_teams/README.md).*
