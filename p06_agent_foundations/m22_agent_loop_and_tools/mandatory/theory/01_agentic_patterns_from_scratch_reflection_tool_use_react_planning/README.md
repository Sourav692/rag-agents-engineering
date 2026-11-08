# M22.1 Theory: Agentic patterns from scratch: reflection, tool use, ReAct planning

*[M22 theory](../README.md) · Lesson 22.1 · Notebooks: [`01b_tool_use_pattern.ipynb`](../../notebook/01b_tool_use_pattern.ipynb), [`01c_planning_pattern_react.ipynb`](../../notebook/01c_planning_pattern_react.ipynb), [`01a_reflection_pattern.ipynb`](../../../optional/notebook/01a_reflection_pattern.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Three loops, three stopping rules, and who actually runs the tool -->

## Why the model cannot run the tool

> **What you'll learn**
>
> - **Explain** why a language model can request a tool but never run one.
> - **Trace** a text-protocol tool call from request to observation, and the four checks your code makes on the way.
> - **Compare** one-round tool use, ReAct and reflection by what repeats and what ends the loop.
> - **Diagnose** the planted failures: bad JSON, an unknown tool, a missing argument, a runaway loop, a lenient critic.

An **agent** is a model inside a loop that can act on the world. This lesson builds the loop's three classic shapes by hand, with no framework in between.

A Larkspur customer asks support *How long does a refund take?* The model does not know Larkspur's policy; the answer sits in the support handbook. So the model replies with a request, *search the handbook for "refund timeline"*, and then nothing happens. The model only writes text.

The model decides. Your application acts.

That split leaves two jobs every agent has to do:

- **Running the tool**: your code reads the request, executes the function and returns the result as an **observation**, a message telling the model what the tool returned.
- **Stopping**: every loop needs a **stopping rule**, a condition that ends it.

All three patterns share one shape:

```mermaid
flowchart LR
    U[User task] --> M[Model]
    M -->|text| C{Your code inspects}
    C -->|done| A[Answer]
    C -->|critique| M
    C -->|tool result| M
```

*Figure 1: The shared skeleton. The model only writes text; your code decides whether to stop or feed something back.*

## Agent loop

An **agentic pattern** is a fixed shape for repeating model calls until a task is done. The three patterns differ in what repeats and what ends the repetition:

| Pattern | What repeats | Stops when | Model calls in our runs |
|---|---|---|---|
| **Reflection** | Draft, critique, redraft | The critic approves, or after a set number of rounds | 2 to 7 with a three-round limit |
| **Tool use** | Nothing: one round of calls, then the answer | The model answers from the observation | 2 |
| **ReAct** | Thought, tool call, observation | The model writes its final response, or after a round cap (10 by default) | 4 for the arithmetic task |

*Table 1: The three patterns compared by loop body and stopping rule.*

The counts come from a re-implementation where a scripted policy stands in for the model. The parsing, checking and looping are real; the model's choices are not.

> **Key distinction:** every pattern has two kinds of exit. One belongs to the model (an approval, an answer, a final-response tag). The other belongs to you (a round limit). A loop with only the model's exit is not finished.

## Pattern 1: one round of tool use

Here tools are described in the system prompt and the model writes its calls as text, which shows what native tool calling (lesson 22.4) later automates.

### The contract the model reads

A **tool** is a function plus a description the model can read: its name, its docstring, and each argument with its type. That description goes into the system prompt with one instruction: when you need a tool, reply with a call in a fixed tagged format. A vague docstring makes a vague tool, because the model never sees the function body.

### The request is only a string

Asked *What's the current temperature in Madrid, in Celsius?*, the model does not answer. It writes a tagged call naming the weather tool, with Madrid as the location and celsius as the unit. Nothing has run yet. The whole round looks like this:

```mermaid
sequenceDiagram
    participant U as User
    participant A as Your code
    participant M as Model
    participant T as Weather tool
    U->>A: Weather in Madrid?
    A->>M: system prompt and question
    M-->>A: tagged call to the weather tool
    A->>A: parse, check, convert
    A->>T: Madrid, celsius
    T-->>A: 25 celsius
    A->>M: observation 25 celsius
    M-->>A: It is 25 °C in Madrid
    A-->>U: final answer
```

*Figure 2: One round of tool use. Two model calls; the tool runs between them, inside your code.*

### The gatekeeper

Between the reply and the tool sits a **gatekeeper**, the code that decides whether a call may run. It makes four checks in a fixed order, and turns every failure into an observation the model can read instead of an exception that ends the run:

```mermaid
flowchart TD
    R[Model reply] --> T{Call tags present?}
    T -->|no| E1[Error: no tags]
    T -->|yes| J{Valid JSON?}
    J -->|no| E2[Error: bad JSON]
    J -->|yes| N{Known tool name?}
    N -->|no| E3[Error: list valid tools]
    N -->|yes| V{Arguments complete?}
    V -->|no| E4[Error: name the missing one]
    V -->|yes| X[Convert types and run]
```

*Figure 3: Validate in this order. Each failure becomes a specific message the model can act on.*

The last step converts each argument to its declared type, so "5" becomes the number 5 when the tool wants a number. For Madrid the observation is 25 celsius, and a second model call turns it into a sentence.

### Planted failures

We planted five broken calls, each a mistake models really make, and one run with type conversion switched off:

| Planted call | What the gatekeeper returned |
|---|---|
| A reply with no call tags | Error: no call tags found |
| A sum call whose JSON is cut off | Error: the content is not valid JSON |
| A call to `calculator`, a tool that does not exist | Error naming the unknown tool and listing the four valid ones |
| A multiply call with only one of its two numbers | Error: missing argument `b` |
| A multiply call with "6912" and "5" as text | 34,560, after conversion to numbers |
| The same call with conversion switched off | "69126912691269126912…", and no error |

*Table 2: Five planted calls and one unguarded run.*

The first four never reach a tool; each comes back as an error the model can correct. The last row is the dangerous one: Python repeats the text five times and returns a wrong answer with no error. We call that a **stringly-typed answer**: the failure no exception reports.

### Where one round breaks

Now a harder task: *sum 1234 and 5678, multiply the result by 5, then take the natural log.*

Each call needs the result of the one before it, but in one round the model must write every argument before any tool has run. It can fill in the sum; the multiplication needs 6,912 and the log needs 34,560, and neither exists yet.

We call this **one-shot blindness**: a single round can run independent calls side by side, but it cannot chain dependent ones.

## Pattern 2: ReAct planning

**ReAct** (reason plus act) interleaves reasoning and acting: the model writes a thought, takes an action, reads the observation, and repeats. In the text protocol that is four kinds of message:

- **Thought**: what the model plans to do next and why.
- **Tool call**: one action, in the same format as before.
- **Observation**: the tool result, written by your code, never by the model.
- **Final response**: the answer, which ends the loop.

### The loop and its two exits

On each round the model gets the whole history. A final response ends the loop. Otherwise your code runs every call through the same gatekeeper and appends one observation per call, so by round two 6,912 is in the model's context.

```mermaid
stateDiagram-v2
    [*] --> Think
    Think --> Act: tool call
    Act --> Observe: run tool
    Observe --> Think: append observation
    Think --> [*]: final response
    Observe --> [*]: round cap hit
```

*Figure 4: The ReAct state machine with its two exits: the model's final response and your round cap.*

### Tracing the arithmetic task

The reference task uses three tools (sum, multiply, natural log) and needs them in order:

```mermaid
sequenceDiagram
    participant C as Your code
    participant M as Model
    C->>M: question and three tool signatures
    M-->>C: thought, sum_two_elements(1234, 5678)
    C->>M: observation 6912
    M-->>C: thought, multiply_two_elements(6912, 5)
    C->>M: observation 34560
    M-->>C: thought, compute_log(34560)
    C->>M: observation 10.450452222917992
    M-->>C: response, about 10.45
```

*Figure 5: ReAct on a three-step dependent task. Each tool argument comes from the previous observation.*

| Round | The model wrote | Observation sent back |
|---|---|---|
| 1 | Sum 1234 and 5678 | 6912 |
| 2 | Multiply 6912 by 5 | 34560 |
| 3 | Natural log of 34560 | 10.450452222917992 |
| 4 | Final response: about 10.45 | none, the loop returns |

*Table 3: The scripted ReAct run, four model calls.*

Every argument after round one came from an observation.

### Planted failure: the runaway loop

A model that never writes a final response never stops on its own. We planted a stubborn policy that calls the handbook search every round, capped at five rounds, and reran the arithmetic task with a cap of two, below the number of dependent steps:

| Run | Model calls | How it ended |
|---|---|---|
| Arithmetic task, cap of 2 | 2 | Stopped by the cap, no answer |
| Stubborn search, cap of 5 | 5 | Stopped by the cap, no answer |

*Table 4: Two capped runs.*

Without the cap, the stubborn run never ends. We call that a **runaway loop**, and it bills for every round. Reaching the cap means the run stopped, not that the task was done, so the loop needs a fallback reply that says so. The first row shows the opposite risk: a cap below the task's depth stops the agent before it can finish.

### What the loop costs

Each ReAct round resends the whole history, so round *k* pays again for everything in rounds 1 to *k* minus 1. Four rounds cost more than twice the input tokens of one round of tool use, and the gap widens every round. We call that **context creep**.

> **Interview tip:** asked why not always use ReAct, answer with latency and cost. Each round is a full model call that waits for the last one, and the prompt grows every time. Use the smallest loop that solves the task.

ReAct fixes reach and chaining. A weak answer from good tools needs a different loop.

## Pattern 3: reflection

**Reflection** improves an output by critiquing it and trying again. One persona writes a draft, a second persona reviews it against the task and returns either a list of fixes or an approval, and the writer revises.

```mermaid
stateDiagram-v2
    [*] --> Generate
    Generate --> Reflect: draft
    Reflect --> Generate: critique
    Reflect --> [*]: critic approves
    Generate --> [*]: round limit
```

*Figure 6: The reflection loop. The critique becomes the next message to the writer.*

It uses no tools but has the same two exits: the critic's approval and your round limit. We ran it with three planted critics and a three-round limit:

| Critic | Rounds | Model calls | How it ended |
|---|---|---|---|
| Approves everything | 1 | 2 | Critic approved |
| Finds two real bugs, then approves | 3 | 6 | Critic approved |
| Never approves | 3 | 7 | Round limit reached |

*Table 5: Reflection with three planted critics.*

The lenient critic ends the loop after one review, so reflection costs two calls and improves nothing. The never-satisfied critic is the reflection version of a runaway loop, and the limit stops it at 1 + 2 × 3 = 7 calls.

> **Pitfall: the lenient critic.** If the reviewer prompt is soft, reflection quietly becomes a single generation that costs double. Tell the critic exactly what good means.

One guard worth copying: each side keeps only its system prompt plus the latest exchange, so earlier drafts are not resent. M25 covers reflection in full.

## Choosing a pattern

Choosing is a short decision:

```mermaid
flowchart TD
    S[New task] --> D{Needs outside data?}
    D -->|no| Q{Worth a second pass?}
    Q -->|yes| R[Reflection]
    Q -->|no| P[Single call]
    D -->|yes| C{Steps depend on results?}
    C -->|no| TU[One-round tool use]
    C -->|yes| RA[ReAct loop]
```

*Figure 7: Pick the smallest loop that fits the task.*

| | Reflection | Tool use | ReAct |
|---|---|---|---|
| Reaches outside data | ✗ | ✓ | ✓ |
| Chains dependent calls | ✗ | ✗ | ✓ |
| Model calls | 1 + 2 × rounds | 2 | rounds + 1 |
| Main risk | Lenient critic | One-shot blindness | Runaway loop, context creep |

*Table 6: Trade-offs at a glance.*

The patterns combine. A production support agent often runs ReAct to gather evidence, then a reflection pass to check the draft answer against that evidence.

## In practice: the Larkspur refund question

Back to the customer. The loop is the one traced above; only the tool changes:

1. The model writes a thought ("I need the refund policy") and a call to the handbook search with the query "refund timeline".
2. The gatekeeper checks the call, runs the search and returns the top handbook chunks as an observation.
3. The model writes its final response, quoting the chunks it was given.

That is retrieval as a tool: your code touched the handbook, and the observation carried the evidence back. The round cap stops a search that never satisfies the model.

> **Key distinction:** native tool calling (lesson 22.4) moves the tool description into the API request and returns structured calls with ids, so most of the gatekeeper's parsing failures disappear. The loop in Figure 4 stays the same, and so does your responsibility for the round cap.

## Limits of this evidence

- **No live model.** Every model reply in Tables 2 to 5 is scripted. The planted failures cover the common shapes, not how often they happen.
- **Text protocol only.** Native tool calling changes the parsing, not the loop.

Left out on purpose, and when to add it:

- **Retries with backoff**: when you call a real API, which returns rate limits and timeouts.
- **History trimming or summaries**: once a task regularly needs more than a handful of rounds.
- **Parallel tool execution**: when one round requests several slow, independent calls.
- **Tracing every round**: before the first production user; a runaway loop is invisible without it.

## Key Takeaways

- The model never runs a tool. It writes a call as text; your code parses, checks, converts and runs it, and the result goes back as an observation.
- One round of tool use cannot chain dependent calls. ReAct can, because every observation stays in the history for the next decision.
- Give every loop two exits, the model's own and a round cap you own. Reaching the cap is a stop with a fallback reply, not a completed task.

## Check yourself

<details>
<summary>1. Why can the ReAct agent chain three dependent tool calls when the one-round tool-use agent cannot?</summary>

One round of tool use must write every argument before any tool has run, so it cannot use one result to choose the next call. ReAct loops, and every observation stays in the history, so the model sees 6912 before it asks to multiply it by 5.

</details>

<details>
<summary>2. The gatekeeper receives a multiply call with 6912 and 5 written as text. What comes back with type conversion, and what comes back without it?</summary>

With conversion the text becomes numbers and the tool returns 34,560. Without it, the language repeats the text "6912" five times and returns a long string with no error at all. That stringly-typed answer is more dangerous than a missing argument, which at least produces an error the model can read.

</details>

<details>
<summary>3. A hand-written ReAct agent keeps calling a search tool that returns nothing useful, and the bill keeps growing. Which exit was missing?</summary>

The round cap, the exit you own (10 rounds by default). The final-response exit only fires when the model decides it is done, and a model that keeps asking for tools never decides that. With the cap the run stops and says why, and the user should get a fallback reply rather than silence.

</details>

---
*Previous: [M22 overview](../README.md). Next: [22.3 Defining tools and binding them to a model](../03_defining_tools_and_binding_them_to_a_model/README.md).*
