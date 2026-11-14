# M27.1 Theory: Dry-run harness and human approval

*[M27 theory](../README.md) · Lesson 27.1 · Notebooks: [`01a_dry_run_harness.ipynb`](../../notebook/01a_dry_run_harness.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Preview the effect, pause for a person, and publish only the exact text they approved -->
<!-- format: approved -->

## The post nobody previewed

> **What you'll learn**
>
> - **Explain** what a dry run is and the three properties that make its preview trustworthy.
> - **Trace** a paused graph from `interrupt()` to `Command(resume=...)` on the same thread.
> - **Diagnose** an unclear answer and an edit made after review, and say why each one must stop the post.
> - **Choose** where the dry run sits in the graph, and what the approval has to cover.

M26 gave agents real reach: they write files, run commands and drive a browser. Every one of those agents ends a turn by doing something, and so far nothing stood between the model's decision and its effect.

Larkspur's operations agent drafts posts for the status feed. After the eu-west outage it writes *"The eu-west outage is resolved and all servers are back online. Engineers will publish a root-cause report within 72 hours of recovery."* With a plain tool call, the model proposes the post and the same call publishes it. A wrong number, a promise the engineers never made or a jab at a competitor reaches every customer before anyone reads it.

A plain tool call joins two moments that need to stay apart: the model *proposing* an action and the system *executing* it. This lesson separates them with two pieces. A **dry run** shows the reviewer the exact effect. An **approval gate** pauses the run until a person decides, and ties that decision to the preview they saw.

## Dry run

**A dry run executes an action's plan without its effect, and reports what the effect would be.** The idea is old: `rsync --dry-run`, `apt-get --simulate` and `terraform plan` all print the changes before anyone applies them.

The lesson's tool is a mock social-media API that stands in for the Larkspur status feed. It has one method that publishes a post, with a dry-run switch, and one rendering step shared by both modes:

```mermaid
flowchart LR
    P[/"Proposed post"/] --> R["Render the text<br/>shared by both modes"]
    R --> M{"Dry run?"}
    M -->|yes| V["Preview +<br/>fingerprint"]
    M -->|no| F["Append to<br/>the feed"]
```

*Figure 1: One code path, two outcomes. The preview and the published text come from the same rendering step.*

The two calls return different things, and only one of them touches the feed:

| Call | Returns | Changes the feed |
|---|---|---|
| Publish with dry run on | Status `DRY_RUN`, the rendered preview, fingerprint `c4e9e330698e` | No |
| Publish with dry run off | Status `PUBLISHED`, post id `post_1` | Appends one post |

*Table 1: The two modes for the eu-west post. The fingerprint is the lab's value.*

The **fingerprint** is the first 12 hex digits of a SHA-256 hash over the rendered text, post body plus hashtags. It names the exact text that was previewed, and the approval gate relies on it.

### Three properties that make a preview trustworthy

A preview is worth reading only if it predicts the live call. Three properties make that hold:

- **The preview comes from the live code path.** Both modes render the post the same way. The reviewer reads the text the platform will receive. A preview built by a separate "describe the action" function can drift away from what the live call does. Call that a **drifting preview**: the reviewer approves one thing and another thing runs.
- **"Nothing happened" is checked, not assumed.** The mock feed is a list the notebook can read back, and every claim that a dry run published nothing is an assertion that the feed is still empty. A real tool needs the same: a sandbox, a staging target or a way to read state back.
- **The dry run is its own graph node, before the pause.** On resume, LangGraph re-runs the paused node from the top. Anything placed before `interrupt()` inside the review node runs a second time. A preview generated there could differ from the one the reviewer approved.

The third property hides until the graph resumes:

```mermaid
flowchart TD
    S["Resume on<br/>the same thread"] --> T["Review node<br/>starts from the top"]
    T --> B["Code before interrupt()<br/>runs a second time"]
    B --> I["interrupt() returns<br/>the decision"]
    I --> N["Publish or cancel"]
```

*Figure 2: What a resume does. Only code that is safe to repeat may sit above the pause.*

### The cost: every consequential tool needs a preview

Each tool that changes the world needs its own preview, showing what the reviewer must judge:

| Action | What the dry run must show |
|---|---|
| Publish a status post | The rendered text, hashtags included |
| Send an email | The rendered message and every recipient |
| Issue a refund | The amount, the account and the invoice it reverses |
| Delete a server | The server name and what is stored on it |

*Table 2: Preview contents per action (illustrative examples beyond the notebook's post).*

With a trustworthy preview in hand, the next job is to stop the run until someone has read it.

## Approval gates

**An approval gate is a node that pauses the run, hands the preview to a reviewer and resumes only with their decision.** In the harness the gate is the review node. It calls `interrupt()` with three things: the question, the preview and the fingerprint.

```mermaid
flowchart LR
    P["propose<br/>model drafts the post"] --> D["dry_run<br/>preview + fingerprint"]
    D --> R["review<br/>interrupt()"]
    R -->|approve| U["publish<br/>fingerprint rechecked"]
    R -->|anything else| X["cancel<br/>nothing published"]
```

*Figure 3: The harness graph in notebook 01a. Only one branch can reach the feed, and it checks the fingerprint again first.*

### Parking and resuming the same thread

LangGraph stops the run at that call, saves its state in the checkpointer under the run's `thread_id`, and returns the payload to the caller under `__interrupt__`. Nothing more happens until someone invokes the graph again with `Command(resume=decision)` on the same thread:

```mermaid
sequenceDiagram
    participant C as Caller
    participant G as Graph
    participant S as Checkpointer
    participant H as Reviewer
    C->>G: invoke(request, thread_id)
    G->>G: propose, dry_run
    G->>S: save state at review
    G-->>C: __interrupt__ with preview
    C->>H: show preview
    H-->>C: "approve" or "reject"
    C->>G: Command(resume=decision)
    G->>G: review re-runs, interrupt() returns decision
    G->>G: publish or cancel
```

*Figure 4: One pause and one resume. The state waits in the checkpointer for as long as the reviewer takes.*

The notebook wraps that exchange in a small pause-and-resume loop: invoke, and while the result holds an interrupt, pass the payload to a reviewer function and resume with its answer. Only the reviewer function changes between uses:

- **A script**: approves the launch post and rejects the post that says the new model makes every competitor obsolete. An automated run then shows both outcomes.
- **A policy check**: an automated rule, configured explicitly.
- **A console prompt**: a person types the answer.
- **A review UI**: answers hours later, from another process.

An answer that arrives hours later from another process needs a persistent checkpointer, such as SQLite or Postgres, in place of the notebook's in-memory one.

### Binding the decision to the preview

Pausing is the mechanism. Three rules make the gate safe:

- **Fail closed.** The decision is normalised by stripping spaces and lowercasing, and only the exact word `approve` approves. Everything else counts as a rejection.
- **Approve what was previewed.** The approval stores the preview's fingerprint. The publish node recomputes the fingerprint of the post it is about to send and refuses if the two differ.
- **Log every decision** with the reviewer, the reason, the fingerprint and the time.

Here is the fail-closed rule against the answers reviewers actually type:

| Answer typed | Decision | Why |
|---|---|---|
| `approve` | approve | The exact word |
| `␣Approve␣` | approve | Spaces stripped, case ignored |
| `approved` | reject | Not the exact word, logged as an unclear answer |
| `yes` | reject | Logged as an unclear answer |
| `sure, why not` | reject | Logged as an unclear answer |
| `reject` | reject | The reviewer's own reason is kept |

*Table 3: Planted answers through the decision rule. An ambiguous answer never publishes.*

A console, a script and a web form all feed the same rule, and the audit entry keeps the original answer beside the decision. The opposite design, where "yes" counts, is a **lenient gate**. It approves whatever a person half-meant.

### Planted failure: an edit after approval

The second rule is the one that catches **post-approval drift**, any change between what the reviewer read and what is about to run. The notebook plants it by editing the paused post directly in the checkpointed state, appending " Buy now!!!", and then approving.

The [approval-gate lab](interactive/approval-gate-lab.html) runs the same harness in the page, with the decision rule and the SHA-256 fingerprint ported from the reference implementation. Checked against the reference graph on 315 runs (3 drafts, 3 kinds of edit, 35 typed answers), it agrees on every final status, fingerprint and audit entry. With the eu-west post approved at `c4e9e330698e`, three versions of the post reach the publish node:

<div class="learning-widget evidence-switcher" data-comparison id="drift-switcher">
<p class="widget-intro">Choose what happens to the eu-west post between the approval and the publish node.</p>
<div class="mode-controls" hidden role="group" aria-label="Change after the preview">
<button type="button" data-mode="none" aria-pressed="false" aria-controls="drift-none">No change</button>
<button type="button" data-mode="small" aria-pressed="false" aria-controls="drift-small">72 hours to 48 hours</button>
<button type="button" data-mode="append" aria-pressed="false" aria-controls="drift-append">Buy now appended</button>
</div>
<section id="drift-none" class="mode-panel" data-announcement="No change selected. The post publishes."><h4>No change</h4><dl><dt>Fingerprint at publish</dt><dd><code>c4e9e330698e</code>, the approved one</dd><dt>Final status</dt><dd><code>PUBLISHED as post_1</code></dd><dt>Feed</dt><dd>one post</dd></dl></section>
<section id="drift-small" class="mode-panel" data-announcement="Small edit selected. The publish node refuses."><h4>"72 hours" edited to "48 hours"</h4><dl><dt>Fingerprint at publish</dt><dd><code>11673ae3c1d4</code></dd><dt>Final status</dt><dd><code>REFUSED: the post differs from the approved preview</code></dd><dt>Feed</dt><dd>empty; the audit log still shows the <code>approve</code></dd></dl></section>
<section id="drift-append" class="mode-panel" data-announcement="Appended line selected. The publish node refuses."><h4>" Buy now!!!" appended (the notebook's test)</h4><dl><dt>Fingerprint at publish</dt><dd><code>78879f196e7d</code></dd><dt>Final status</dt><dd><code>REFUSED: the post differs from the approved preview</code></dd><dt>Feed</dt><dd>empty; the audit log still shows the <code>approve</code></dd></dl></section>
<p class="switch-status" aria-live="polite"></p>
</div>

We recomputed all three fingerprints from the lab's post text with Python's `hashlib`, and they match the lab.

<!-- lab: interactive/approval-gate-lab.html -->

A one-phrase edit changes the fingerprint as completely as a new sentence. Any edit after review needs a new preview and a new decision. In both refused runs the audit log still shows an `approve`. That entry is correct. The reviewer approved `c4e9e330698e`, and the text that tried to publish was something else.

> **Pitfall: the gate is only as good as its reviewer.** Approve the uptime post in the lab ("Larkspur Cloud now beats every other host on uptime") and it reaches the feed. The gate enforces the decision, and it cannot judge the content. The module page's interview questions cover how to measure whether reviewers read.

The same pause exists ready-made. `HumanInTheLoopMiddleware` from [M23's middleware lesson](../../../../../p06_agent_foundations/m23_react_agents/mandatory/theory/04_middleware_including_human_in_the_loop/README.md) gives a `create_agent` agent a pause before a tool call, built on the same `interrupt()` and checkpointer from M09. Building the gate by hand adds the two parts this lesson needs: a preview of the effect, and a fingerprint that ties the approval to it.

## In practice: the eu-west status post

Here is the whole harness on Larkspur's post, in the order the graph runs it.

<div class="walkthrough learning-widget" data-stepper id="harness-walkthrough">
<p class="widget-intro">Step through one run of the harness on the eu-west post.</p>
<div class="step-controls" hidden role="group" aria-label="Stages of the approval harness"><button type="button" data-step="0" aria-pressed="false" aria-controls="harness-step-0">1. Propose</button><button type="button" data-step="1" aria-pressed="false" aria-controls="harness-step-1">2. Dry run</button><button type="button" data-step="2" aria-pressed="false" aria-controls="harness-step-2">3. Review</button><button type="button" data-step="3" aria-pressed="false" aria-controls="harness-step-3">4. Decide</button><button type="button" data-step="4" aria-pressed="false" aria-controls="harness-step-4">5. Publish</button></div>
<div class="step-panels"><section id="harness-step-0" class="step-panel" aria-labelledby="harness-heading-0"><h4 id="harness-heading-0">1. Propose</h4><dl><dt>Input</dt><dd>the request to post that the eu-west outage is resolved</dd><dt>Output</dt><dd>the post body and its hashtags as structured output; nothing rendered yet</dd></dl></section><section id="harness-step-1" class="step-panel" aria-labelledby="harness-heading-1"><h4 id="harness-heading-1">2. Dry run</h4><dl><dt>Node</dt><dd>its own node, which runs once</dd><dt>State written</dt><dd>the rendered preview and fingerprint <code>c4e9e330698e</code></dd><dt>Feed</dt><dd>still empty, checked by reading it back</dd></dl></section><section id="harness-step-2" class="step-panel" aria-labelledby="harness-heading-2"><h4 id="harness-heading-2">3. Review</h4><dl><dt>Call</dt><dd><code>interrupt()</code> with the question, the preview and the fingerprint</dd><dt>State</dt><dd>saved in the checkpointer under the run's <code>thread_id</code>; the on-call lead reads the preview</dd></dl></section><section id="harness-step-3" class="step-panel" aria-labelledby="harness-heading-3"><h4 id="harness-heading-3">4. Decide</h4><dl><dt>Resume</dt><dd><code>Command(resume=...)</code> on the same thread; the review node re-runs and <code>interrupt()</code> returns the answer</dd><dt>Decision</dt><dd>the lead types <code>approve</code>; the audit log records reviewer, reason, fingerprint and time</dd></dl></section><section id="harness-step-4" class="step-panel" aria-labelledby="harness-heading-4"><h4 id="harness-heading-4">5. Publish</h4><dl><dt>Check</dt><dd>the fingerprint is recomputed from the post in state and compared with the approved one</dd><dt>Result</dt><dd>they match, and the post goes out as <code>post_1</code>; an edit in the meantime would have been refused</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

Lesson 27.2 builds agents that only read: they search the web and return a brief. Their risk is a wrong claim, and the guard moves from a person's approval to checks in code.

## Limits

The harness tested an unclear answer and an edit after the preview, on a mock feed. It leaves out:

- **Staleness.** The fingerprint covers the text, not the world it describes. A post approved four hours later still matches even if the incident reopened. Add an approval expiry or a precondition checked at publish time.
- **Persistence.** The in-memory checkpointer loses a paused run on restart. Add SQLite or Postgres before reviewers answer from another process.
- **Reviewer quality.** Nothing measures whether approvals are read. Add approval-rate and time-to-decision monitoring.
- **No model in our check.** The fingerprints and statuses on this page come from the lab and its fixed post text. The notebook's own posts are drafted by `gpt-4o-mini`: their text and fingerprints differ on every run.

## References

1. LangChain, [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts).
2. LangChain, [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence).
3. LangChain, [Human-in-the-loop middleware](https://docs.langchain.com/oss/python/langchain/human-in-the-loop).
4. HashiCorp, [terraform plan command](https://developer.hashicorp.com/terraform/cli/commands/plan).
5. Python Software Foundation, [hashlib: secure hashes and message digests](https://docs.python.org/3/library/hashlib.html).

## Key Takeaways

- A dry run renders the effect through the same code path as the live call and changes nothing. Check that by reading state back, and put the dry run in its own node before the pause.
- The gate pauses with `interrupt()`, saves state under the `thread_id` and waits for `Command(resume=...)`. Accept only the exact word `approve` and log every decision with reviewer, reason, fingerprint and time.
- Tie the approval to a fingerprint of the previewed text and recompute it before publishing. Any edit after review, even one phrase, needs a new preview and a new decision.

## Check yourself

<details>
<summary>1. Why must the dry run be its own graph node before the review node, rather than code inside the review node?</summary>

On resume LangGraph re-runs the paused node from the top, so anything placed before `interrupt()` in the review node runs twice. A preview generated there could differ from the one the reviewer approved.

</details>

<details>
<summary>2. The eu-west post is approved, then 72 hours is edited to 48 hours before it publishes. What happens, and what does the audit log show?</summary>

The fingerprint at publish is `11673ae3c1d4`, not the approved `c4e9e330698e`, so the publish node returns `REFUSED: the post differs from the approved preview`. The audit log still shows an `approve`, and that is correct: the reviewer approved `c4e9e330698e`. Any edit after review needs a new preview and a new decision.

</details>

<details>
<summary>3. A reviewer answers the approval prompt with yes. Does the post go out, and why is that the right behaviour?</summary>

No. The gate fails closed: the answer is stripped and lowercased, and only the exact word `approve` approves. `yes` and `approved` are rejections, logged as unclear answers. An ambiguous answer should never publish.

</details>

---
*Previous: [M27 overview](../README.md). Next: [27.2 Research and competitive-intelligence agents](../02_research_and_competitive_intelligence_agents/README.md).*
