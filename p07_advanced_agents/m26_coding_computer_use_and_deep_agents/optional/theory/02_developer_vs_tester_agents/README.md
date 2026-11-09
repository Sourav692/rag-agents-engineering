# M26.2 Theory: Developer vs tester agents

*[M26 theory](../../../mandatory/theory/README.md) · Lesson 26.2 · Notebooks: [`02a_developer_vs_tester_agents.ipynb`](../../notebook/02a_developer_vs_tester_agents.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: A small project: a developer agent and a tester agent in a critique-and-revise loop that ends by a counter in code -->

## The project: a developer and tester pair

> **What you'll build**
>
> - **A developer agent** that writes Python and can run it with a timed Python tool.
> - **A tester agent** that reviews the code, writes unit tests in its report, scores it and lists fixes.
> - **A two-node graph** that loops developer, tester, developer until a reflection counter reaches its cap.
> - **Two small games**, FLAMES and Tic-Tac-Toe, built by the pair and checked against hand-written references.

Lesson 26.1 graded a coding agent on a test suite someone had already written. This project asks a second agent to supply the critique. It is the critique-and-revise (reflection) pattern from [M25](../../../../m25_planning_reflection_reasoning/mandatory/theory/README.md), with a **generator** (the developer) and a **reflector** (the tester) taking turns on one shared conversation.

The project adds no new pattern. It shows what two agents in one loop need: a stop rule no model can talk its way past, a safe-enough way to run model-written code, and a line between a test that ran and a test the tester only imagined.

## Architecture

The graph has two nodes and one decision:

```mermaid
flowchart LR
    T[/Task/] --> D["Developer<br/>writes or revises code"]
    D --> R{"Reflections<br/>reached cap?"}
    R -->|no| TE["Tester<br/>critique, score"]
    TE -->|"count + 1"| D
    R -->|yes| E[/Final code/]
```

*Figure 1: The critique-and-revise loop. The router reads a counter in state. Code decides the stop.*

| Piece | What it does | Built on |
|---|---|---|
| **Developer** | A `create_agent` agent with one Python tool, its own tool loop capped at 12 steps, which sees the whole conversation on every turn | M23's `create_agent` |
| **Tester** | A prompt piped into the model, no tools. Its report enters the conversation as a user message, because to the developer it is feedback | M25's reflector |
| **Python tool** | Runs each snippet as a script in a new isolated Python process, in an empty folder, with no environment variables, closed standard input and a 10-second timeout | |
| **State** | The conversation, the cap and a `reflection_count` that each tester turn adds 1 to | M08 reducers |
| **Router** | A pure function that ends the run once the count reaches the cap | [M37's capped quality loop](../../../../../p10_multi_agent_systems/m37_multi_agent_applied_builds/mandatory/theory/04_research_systems_supervisor_financial_research_summarisation_full_research_system/README.md#a-quality-loop-with-a-cap-in-code) |

*Table 1: The project's five pieces.*

The notebook checks the Python tool's guards without a model. Keyboard input fails at once with `EOFError`, and an endless loop is killed at its timeout (2.0 s with a 2-second limit in our run).

## Following one FLAMES request

The task is *Write a Python program for the FLAMES game, plus a short example that calls it with two fixed names*, with a cap of one reflection:

```mermaid
sequenceDiagram
    participant D as Developer
    participant T as Tester
    participant R as Router
    D->>R: draft 1, maybe after running it
    R->>T: count 0, cap 1, go on
    T->>D: tests, pass rate, score, fixes
    Note over T: count becomes 1
    D->>R: draft 2 with the fixes
    R-->>R: count 1, cap 1, stop
```

*Figure 2: One reflection round. The developer speaks twice, the tester once.*

The loop's arithmetic holds for any cap. Stub nodes that only append a message, with zero model calls, give these counts:

| Cap `r` | Developer turns | Tester turns | Graph steps used | `recursion_limit` (2r + 4) |
|---|---|---|---|---|
| 0 | 1 | 0 | 1 | 4 |
| 1 | 2 | 1 | 3 | 6 |
| 3 | 4 | 3 | 7 | 10 |

*Table 2: Stub runs from the notebook's own graph builder. The developer runs r + 1 times, the tester r times, and the recursion limit leaves 3 spare steps as a second guard.*

After the run, code checks how many times each agent spoke and whether the last answer holds a Python block that parses. Parsing does not prove the game is right.

A hand-written reference does. For John and Jane it finds 4 letters left, crosses out M, L, F, A and S in turn, and lands on Enemy. The notebook records two mistakes one model run made: it restarted counting from the start of FLAMES after each removal, and read S as "Sister" rather than "Sibling". The Tic-Tac-Toe reference plays three scripted games (a win, a draw, a move onto an occupied square) and all three end as expected.

## Design choices worth copying

| Choice | Why |
|---|---|
| **Counter in state, pure router** | The loop ends by a rule in code, not when a model decides it is happy |
| **`recursion_limit` as a second guard** | If the router were ever broken, the run still stops after 2r + 4 steps |
| **Prove the cap with stubs** | Zero model calls make the termination test free and repeatable |
| **Ask for code driven by fixed inputs** | The tool closes standard input. An interactive game would only raise `EOFError` |
| **Check against a reference** | The tester's verdict is a model's opinion. A hand-written implementation is a fact |

*Table 3: Six choices and what each protects against.*

## Limits

- **The tester estimates.** It has no tools. Its pass percentage and score are the model's estimates, not executed results. We call this an **estimated pass rate**. Giving it the Python tool makes the results real, at roughly twice the cost.
- **Fixed rounds, not "until the tests pass".** The loop stops at the cap even if the tester still lists failures. The module's lab brief asks for iteration until tests pass, which needs a router that also reads an executed test result.
- **A guard, not a sandbox.** The Python tool runs model-written code with your user's permissions. It can still read your files and reach the network, and anything beyond a demo needs a container or a hosted sandbox (lesson 26.3).
- **No recorded model run.** The notebook ships without outputs and the drafts change each run. This page quotes only the deterministic checks.

The notebook needs an OpenAI key for the two agents. The stub runs, the tool guards and both references run without one.

## Key Takeaways

- Stop a two-agent loop with a counter in state and a pure router, back it with a `recursion_limit`, and prove the counts with stub nodes before spending a model call.
- A tester without a way to run code only estimates its pass rate. Run the tests, or check against a reference, before trusting the verdict.
- Running model-written code in a fresh process with a timeout, no environment and closed input keeps a demo from hanging or leaking keys, but it is not a sandbox.

## Check yourself

<details>
<summary>1. With a cap of three reflections, how many times does each agent run, and what stops the loop?</summary>

The developer runs four times (a first draft plus one revision per critique) and the tester three times. The router stops the loop once the reflection counter in state reaches the cap, and a recursion limit of 2r + 4, here 10 steps, stops it even if the router were broken.

</details>

<details>
<summary>2. After one round the tester reports 100% of its tests passing and a score of 9 out of 10. How much does that tell you?</summary>

Little. The tester has no tools. It wrote the tests in its report and reasoned about them. The pass rate and score are the model's estimates. Run the tests, give the tester the Python tool at roughly twice the cost, or compare against a hand-written reference.

</details>

<details>
<summary>3. Why does the Tic-Tac-Toe task ask for a function that plays a fixed list of moves?</summary>

The developer's Python tool closes standard input and kills a snippet after a timeout. A game that waits for a player would raise an error at once or be stopped. The task asks for a version the tool can run and check without a keyboard.

</details>

---
*Previous: [26.1 Applied ReAct: web research, SWE and computer-use agents](../../../mandatory/theory/01_applied_react_web_research_swe_and_computer_use_agents/README.md). Next: [26.3 Deep agents: orchestrator, sub-agents, skills and long-term memory](../../../mandatory/theory/03_deep_agents_orchestrator_sub_agents_skills_and_long_term_memory/README.md).*
