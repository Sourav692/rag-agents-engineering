# M25 Theory: Planning, reflection and reasoning patterns

*Part VII · Advanced Agents · [Module README](../../README.md) · [All theory pages](../../../../THEORY.md)*

An agent that answers a multi-part question has to decide its steps, and an agent whose answer must be right has to check its own work. This module covers both: planning the steps before running them, replanning when a result is wrong, critiquing and verifying a draft, and searching over several reasoning paths when one is not reliable enough. The M25 notebooks build on four ideas: plan-and-execute, replanning, chain-of-verification and tree search with tree of thoughts and LATS. Each idea has a page in the folder of the lesson that teaches it, listed under [Lessons](#lessons). This page has the overview, the interview questions and the takeaways.

The running example is a Larkspur Cloud customer who wants to cancel an annual plan. The answer needs up to six handbook lookups: the refund rule, how long a refund takes, what happens to servers, how long data is kept, what an export includes, and how fast support answers. The lab plans and runs those lookups against the handbook chunks M10 to M12 use, lesson 25.3 critiques an incident post against the SLA, and lesson 25.4 verifies a drafted cancellation answer against the same chunks.

## TL;DR

- A fixed plan makes 2 LLM calls (planner and synthesizer) however many lookups it holds. ReAct makes one per search plus one to answer, and each call re-reads the conversation so far. On the lab's four-lookup question that is 2 calls and about 504 tokens against 5 calls and about 918.
- A fixed plan writes a wrong search result straight into the answer. Evaluating every step and replanning costs N + 2 + 2f calls for N lookups and f wrong results, and the cap must count retries: six lookups with one retry need 7 executed steps, and the notebook's cap of 6 leaves one lookup unanswered.
- A critic with only its own opinion improves style and invents facts it was asked for. Reflexion turns the critique into searches the revision must cite, and chain-of-verification answers one question per claim in a fresh call that never sees the draft, at 1 + 1 + N + 1 calls. It removes unsupported claims and adds no missing ones.
- Self-consistency, tree of thoughts and LATS spend extra calls on several reasoning paths. They pay off only when something can score a partial answer: the evaluator decides what survives.
- The optional patterns put a rule in code behind every model judgment: Self-Discover's verification step, an execution critic, a simulator's 5th-percentile limit, a metacognitive router and an editor that approves what a memory keeps.

## Mental model

```mermaid
flowchart LR
    Q[/Question/] --> P["Plan<br/>list the lookups"]
    P --> X["Execute<br/>next lookup"]
    X --> C{"Result answers<br/>the step?"}
    C -- no --> R["Replan<br/>the rest"]
    R --> X
    C -- "yes, more" --> X
    C -- "yes, done" --> D["Draft<br/>the answer"]
    D --> V["Verify<br/>each claim"]
    V --> A[/Answer/]
```
<!-- animated: diagrams/plan-check-verify.anim.html -->

*Figure 1: Plan, check, verify. Each box is a place to spend an LLM call, and each buys a different guarantee.*

The plan makes the work visible before it runs, the check stops a wrong result from reaching the answer, and verification catches claims the draft invented. ReAct folds plan, execute and check into one call per step. Reflection (lesson 25.3) puts a critic after Draft, and tree search (lesson 25.6) replaces the single Execute box with several candidate steps and an evaluator that keeps the best.

## Lessons

| Lesson | Topic | Theory |
|---|---|---|
| 25.1 | Plan-and-execute vs ReAct; decompose, execute, replan | [Plan-and-execute](01_plan_and_execute_vs_react_decompose_execute_replan/README.md#plan-and-execute)<br>[Replanning](01_plan_and_execute_vs_react_decompose_execute_replan/README.md#replanning) |
| 25.2 | Deep-research and reflective dynamic planners | [The project: two research planners](02_deep_research_and_reflective_dynamic_planners/README.md#the-project-two-research-planners) |
| 25.3 | Reflection and Reflexion agents | [Reflection: a writer and a critic](03_reflection_and_reflexion_agents/README.md#reflection-a-writer-and-a-critic)<br>[Reflexion: critique backed by search](03_reflection_and_reflexion_agents/README.md#reflexion-critique-backed-by-search) |
| 25.4 | Chain-of-verification and constitutional critique | [Chain-of-verification](04_chain_of_verification_and_constitutional_critique/README.md#chain-of-verification)<br>[Constitutional critique](04_chain_of_verification_and_constitutional_critique/README.md#constitutional-critique) |
| 25.5 | Self-Discover and reflective code generation | [Self-Discover: plan the reasoning first](../../optional/theory/05_self_discover_and_reflective_code_generation/README.md#self-discover-plan-the-reasoning-first)<br>[Execution as the critic](../../optional/theory/05_self_discover_and_reflective_code_generation/README.md#execution-as-the-critic) |
| 25.6 | Self-consistency, tree of thoughts and LATS | [Tree of thoughts / LATS](06_self_consistency_tree_of_thoughts_and_lats/README.md#tree-of-thoughts--lats) |
| 25.7 | Simulator-in-the-loop, metacognition and exemplar memory | [Simulate before you act](../../optional/theory/07_simulator_in_the_loop_metacognition_and_exemplar_memory/README.md#simulate-before-you-act)<br>[Metacognition: decide whether to answer](../../optional/theory/07_simulator_in_the_loop_metacognition_and_exemplar_memory/README.md#metacognition-decide-whether-to-answer)<br>[Exemplar memory: better first drafts](../../optional/theory/07_simulator_in_the_loop_metacognition_and_exemplar_memory/README.md#exemplar-memory-better-first-drafts) |

## Interactive lab

[**Plan or react: the call budget**](01_plan_and_execute_vs_react_decompose_execute_replan/interactive/plan-or-react-lab.html): open the file in a browser. Clear the wrong-result toggle and slide the lookups from 1 to 6: the fixed plan stays at 2 LLM calls while ReAct's tokens climb past the replanner's at six. Then press lookup 1 again and compare the three answers. Finally set six lookups, keep one wrong, and drop the cap from 7 to 6 to see a lookup go unanswered.

## How it connects

- **Before:** [M22](../../../../p06_agent_foundations/m22_agent_loop_and_tools/mandatory/theory/README.md) and [M23](../../../../p06_agent_foundations/m23_react_agents/mandatory/theory/README.md) build the agent loop and ReAct that this module measures against. In [M24](../../../../p06_agent_foundations/m24_agentic_workflow_patterns/mandatory/theory/README.md)'s workflow patterns (prompt chaining, routing, parallelization, orchestrator and worker, evaluator and optimizer) you draw every step. From this module on, the model writes part of the control flow, and lesson 25.2 reuses M24's Send fan-out.
- **Next:** [M26](../../../m26_coding_computer_use_and_deep_agents/mandatory/theory/README.md) applies planning to coding and deep agents, and [M27](../../../m27_human_approval_applied_agents/mandatory/theory/README.md) adds human approval before an agent acts. [M17](../../../../p05_retrieval_quality_and_rag_apps/m17_query_transformation/mandatory/theory/README.md)'s query decomposition is a plan for retrieval, and [M29](../../../../p08_agentic_rag/m29_crag_and_self_rag/mandatory/theory/README.md)'s Self-RAG checks a generated answer for groundedness in the retrieved evidence, the RAG form of the verify step.

## Interview Spotlight: 5 Questions You Might Get Asked

*Production questions of the kind asked in applied AI engineering interviews.*

### 1. Larkspur's cancellation assistant, a plan-and-execute agent, told a customer their data is kept for 12 months after cancelling. The handbook says 30 days. The trace shows the retention lookup ran. What went wrong, and what do you change?

**What a strong answer covers:**
- Reads the trace: the retention search returned the promotional-credits chunk ("expire 12 months"), and a fixed plan pops every step as done whatever it returned
- Adds a per-step evaluator that asks whether the result states the requested fact about the right subject, writes the verdict to state, and routes a failure to a replanner
- Passes only accepted results to the synthesizer and tells it to say a fact was not found rather than fill it in
- Reproduces the failure with a stub search that returns the wrong chunk on the first call, and adds the question to the golden set

### 2. The team is choosing between ReAct and plan-and-execute for two Larkspur assistants: one answers multi-part billing questions, the other troubleshoots a server that will not start. Which pattern goes where?

**What a strong answer covers:**
- Billing questions have lookups you can list up front, so a plan is cheaper (2 LLM calls) and inspectable before any search runs
- Troubleshooting is exploratory: the next check depends on the last result, which is what ReAct's per-step reasoning is for
- Names ReAct's failure from lesson 25.1: it can announce its next step as text and end, because nothing tracks what is left
- Suggests a middle ground for either: plan, execute, evaluate each step and replan, at N + 2 calls on a clean run

### 3. After adding replanning, the cost per question went up and the team wants to know whether it is paying for itself. What do you measure?

**What a strong answer covers:**
- Logs per run: planned steps, executed steps, rejected steps, replans, cap hits and LLM calls, from state rather than from prompts
- Tracks the replan rate and the share of rejected results that were really wrong, by sampling and labelling evaluator verdicts
- Compares answer completeness on the golden set with and without replanning, and the calls each extra complete answer cost
- Watches cap hits as their own alert, since a run that hits the cap returns a partial answer

### 4. A customer question needs six lookups, and the replanning agent runs with `max_iterations = 6`. On a day when one search returns the wrong chunk, one part of the answer goes missing. Why, and how should the cap be set?

**What a strong answer covers:**
- The cap counts executed steps, and a rejected step plus its retry is two executions: six lookups with one retry need seven
- The router checks the cap before it checks the verdict, so the run goes to the synthesizer with one lookup unanswered
- Sets the cap from the plan: planned lookups plus the retries you will pay for, or a per-step retry limit
- Keeps the honest fallback: the synthesizer reports the missing fact, and the response says the answer is partial

### 5. You add chain-of-verification to the RAG answer step, as the M25 lab brief asks. Unsupported claims fall on the golden set, but a reviewer finds one correct claim was removed. How do you evaluate and guard this?

**What a strong answer covers:**
- Scores before and after in code against labelled claims, counting removed correct claims as well as removed unsupported ones
- Expects precision to rise and recall not to: CoVe checks the claims that were made and adds none
- Answers verification questions from retrieved handbook chunks rather than the model's memory, and checks the reviser's output instead of trusting its list of corrections
- Reports the cost of 1 + 1 + N + 1 calls per answer and batches the N independent calls to hold latency

## Key Takeaways

- Plan when the steps are knowable up front and react when the next step depends on the last result. Count LLM calls and tokens for both on your own questions before choosing.
- A plan is only as safe as its check. Evaluate every step's result, replan from the reason it failed, cap the loop from planned steps plus allowed retries, and send only accepted results to the answer.
- Give the critic evidence: a check in code, a search, a verification question answered without the draft, or the result of running the output. A critic with only its opinion fixes style.
- Spend extra reasoning paths only where an evaluator can tell a good partial answer from a bad one, and keep every numeric rule in code.

---
*Previous: [M24 Agentic workflow patterns](../../../../p06_agent_foundations/m24_agentic_workflow_patterns/mandatory/theory/README.md). Next: [M26 Coding, computer-use and deep agents](../../../m26_coding_computer_use_and_deep_agents/mandatory/theory/README.md).*
