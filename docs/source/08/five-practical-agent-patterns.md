# Five Practical Agent Patterns

A focused study guide for the patterns covered in this repository, with exact notebook paths and the sections to study.

These five are a practical learning shortlist based on current framework guidance and the repository's examples. They are not a measured ranking of industry adoption. The numbering identifies the patterns; the suggested learning order appears below.

**Mandatory** means the minimum notebooks or lesson sections recommended for this focused study route. **Optional** means extra background, applications, or extensions you can study afterwards. You do not need to complete every notebook in each referenced module.

This route assumes familiarity with Python, tool-calling agents, and basic LangGraph state, nodes, edges, and checkpointers. When reading, focus on the sections listed. When running a selected section, execute its setup and earlier dependency cells in the notebook's original order.

## At a glance

| Pattern | Mandatory study | Optional extensions |
|---|---|---|
| Supervisor / agents as tools | Module 05, notebook 03: Parts 2–3; module 06, notebook 01: full notebook | Foundations, human review, hierarchical teams |
| Sequential / conditional workflow | Module 05, notebook 02: Parts 2–3 and 5; notebook 03: Part 5 | Agent communication, supervisor workflows with human review |
| Parallel fan-out / fan-in | Module 09, notebook 01: full notebook | Async streaming, ensembles, applied research |
| Generator–critic / evaluator–optimizer | Module 05, notebook 04: Part 3 | Developer/tester loop, article quality review |
| Handoffs | Module 07, notebook 01: full notebook | Swarm application, comparison with supervisors |

The mandatory route spans **six unique notebooks**. Module 05's notebook 03 serves both the supervisor and conditional-workflow patterns.

## 1. Supervisor / agents as tools

**How it works:** A central agent decides which specialist should work next and combines the results. In the agents-as-tools variant, specialists return their results through tool calls to the supervisor.

**Typical uses:** Research assistants, enterprise assistants spanning several domains, and coding systems with developer and reviewer roles.

**Flow:** `User → supervisor → specialist → supervisor → answer`

### Mandatory notebooks

**First — compare both variants:** [modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb](../modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb) — Read the setup, Part 2: Supervisor Architecture, and Part 3: Supervisor with Tool-Calling. The other architecture sections are optional for this pattern.

**Then — build a supervisor:** [modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb](../modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb) — Work through the full notebook.

- Study Parts 2–6 for typed routing, the supervisor, specialists, and graph assembly.
- Study Parts 8–9 for the routing trace and loop cap.

### Optional notebooks

- [modules/05_multi_agent_foundations/notebooks/02_multiagent_pattern_from_scratch.ipynb](../modules/05_multi_agent_foundations/notebooks/02_multiagent_pattern_from_scratch.ipynb) — Background on agent tools, dependencies, and crews; useful if these building blocks are unfamiliar.
- [modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb](../modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb) — Parts 1–2 deepen message passing and typed shared-state communication.
- [modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb](../modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb) — Adds article quality checks and human review to a supervisor workflow.
- [modules/06_supervisor_and_hierarchical_agents/notebooks/02_hierarchical_agents.ipynb](../modules/06_supervisor_and_hierarchical_agents/notebooks/02_hierarchical_agents.ipynb) — Extends the supervisor into nested teams and department subgraphs.

**Completion check:** Build a supervisor that delegates to two specialists, collects their results, and stops reliably. Explain how calling a specialist as a tool differs from graph-based supervisor routing.

**Choose it when:** The task requires several specialists and a central agent needs to coordinate their work dynamically.

## 2. Sequential / conditional workflow

**How it works:** Define the execution stages in advance. Outputs feed the next stage; explicit conditions select branches. The workflow controls the sequence.

**Typical uses:** Research → draft → review, document processing, and business processes with well-defined steps.

**Flow:** `Input → stage A → stage B → condition → stage C or D → result`

### Mandatory notebooks

**Sequential workflow:** [modules/05_multi_agent_foundations/notebooks/02_multiagent_pattern_from_scratch.ipynb](../modules/05_multi_agent_foundations/notebooks/02_multiagent_pattern_from_scratch.ipynb)

- Study Part 2 for agents and their dependencies.
- Study Part 3 for a sequential crew.
- Study Part 5 for the bridge to LangGraph using `StateGraph.add_edge`.

**Conditional workflow:** [modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb](../modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb) — Part 5: Custom Workflow Architecture.

### Optional notebooks

- [modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb](../modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb) — Parts 1–2 compare passing messages with sharing typed fields between workflow stages.
- [modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb](../modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb) — Applies branching, quality checks, and human review in an article workflow.

**Completion check:** Build a sequence of stages and add a conditional branch. Identify which steps are fixed by the workflow and which decisions are made by an agent.

**Choose it when:** The required stages and decision points are known before execution. This is a useful first pattern to learn.

## 3. Parallel fan-out / fan-in

**How it works:** Dispatch independent tasks to multiple workers, wait for the required results, and aggregate them. Map-reduce extends this to a variable number of items.

**Typical uses:** Summarizing many documents, searching multiple sources, and comparing independent analyses.

**Flow:** `Input → workers A, B, C concurrently → join / reducer → result`

### Mandatory notebook

**Core parallel execution:** [modules/09_async_and_parallel_multi_agent/notebooks/01_parallel_agents.ipynb](../modules/09_async_and_parallel_multi_agent/notebooks/01_parallel_agents.ipynb) — Work through the full notebook.

- Study Part 1 for supersteps and fan-out.
- Study Part 2 for joins, list edges, and `defer=True`.
- Study Part 3 for reducers and concurrent state updates.
- Study Part 4 for document map-reduce using `Send`.

### Optional notebooks

**Async execution and streaming:** [modules/09_async_and_parallel_multi_agent/notebooks/02_async_multi_agent_streaming.ipynb](../modules/09_async_and_parallel_multi_agent/notebooks/02_async_multi_agent_streaming.ipynb) — Parts 2–4; read Part 1 first if `async`/`await` is unfamiliar.

**Ensemble application:** [modules/08_collaboration_and_control_patterns/notebooks/06_ensemble_parallel_exploration.ipynb](../modules/08_collaboration_and_control_patterns/notebooks/06_ensemble_parallel_exploration.ipynb) — Parallel specialist analysts and an aggregator; study Parts 1–3 for the core design.

**Applied research system:** [modules/10_multi_agent_applied_builds/notebooks/14_multi_agent_research_system.ipynb](../modules/10_multi_agent_applied_builds/notebooks/14_multi_agent_research_system.ipynb) — Parts 4–6 combine planning, worker fan-out, findings aggregation, and quality review.

**Completion check:** Run two independent workers, join their results once, and use a reducer when workers write to the same state field. Explain how `Send` supports a variable number of tasks.

**Choose it when:** Workers can proceed independently and the merge rule is clear. Concurrent execution can reduce latency, while still incurring each worker's model cost.

## 4. Generator–critic / evaluator–optimizer

**How it works:** One agent produces a candidate; another evaluates it and returns actionable feedback. Revise until the acceptance criteria are met or the iteration cap is reached.

**Typical uses:** Code generation and testing, document review, and iterative answer refinement.

**Flow:** `Generator → critic → accepted result OR feedback → generator`

### Mandatory notebook

**Core refinement loop:** [modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb](../modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb) — Part 3: Generator–Critic Refinement. Parts 1–2 are optional communication background for this pattern.

### Optional notebooks

**Applied developer/tester loop:** [modules/10_multi_agent_applied_builds/notebooks/11_developer_vs_tester_agents.ipynb](../modules/10_multi_agent_applied_builds/notebooks/11_developer_vs_tester_agents.ipynb)

- Study Parts 1 and 3–5 for the pattern, developer, tester, state, and revision loop.
- Study Part 6 for the deterministic check that the loop terminates.
- Parts 8–9 apply the loop to small games.

**Article quality review:** [modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb](../modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb) — Parts 2–3 show a grader and supervisor review loop; Part 4 adds human review.

**Completion check:** Build a generator–critic loop with explicit acceptance criteria and a revision cap. Show both the accepted-result path and the stop-at-limit path.

**Choose it when:** You can state clear quality criteria and feedback can improve the candidate. Independent tests or source checks strengthen the evaluation.

## 5. Handoffs

**How it works:** An agent transfers control and relevant context to another agent. The specialist becomes active and may continue the conversation, hand it onward, or return it.

**Typical uses:** Customer support triage, booking assistants, and conversations that cross specialist domains.

**Flow:** `User → triage agent → handoff → active specialist → conversation continues`

### Mandatory notebook

**Core handoff mechanism:** [modules/07_swarm_and_handoffs/notebooks/01_agent_handoffs.ipynb](../modules/07_swarm_and_handoffs/notebooks/01_agent_handoffs.ipynb) — Work through the full notebook.

- Study Part 1 for router versus handoff.
- Study Parts 2–3 for the handoff tool and triage/specialist graph, including `Command.PARENT`.
- Study Part 4 for persisting the active agent with a checkpointer.
- Study Part 5 for handoff-loop protection.

### Optional notebooks

**Swarm application:** [modules/07_swarm_and_handoffs/notebooks/02_multi_agent_swarm.ipynb](../modules/07_swarm_and_handoffs/notebooks/02_multi_agent_swarm.ipynb) — Parts 3–7 combine RAG, NL2SQL, and invoice agents with handoff tools and active-agent memory. This is an application extension; notebook 01 covers the core handoff pattern.

**Supervisor comparison:** [modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb](../modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb) — Parts 3–6 clarify central routing versus transferring control. Reuse your earlier supervisor study if already completed.

**Completion check:** Transfer a conversation to a specialist with a context note, preserve the active agent across turns, and stop accidental handoff loops.

**Choose it when:** A specialist should take ownership of the ongoing interaction. A supervisor's tool call normally returns control to the supervisor; a handoff changes the active agent.

## Suggested learning order

Complete the mandatory route first. Add the optional notebooks when their application or extension is relevant to your work.

1. **Sequential workflows:** Module 05, notebook 02, Parts 2–3 and 5; then notebook 03, Part 5.
2. **Supervisors / agents as tools:** Module 05, notebook 03, Parts 2–3; then module 06, notebook 01 in full.
3. **Parallel execution:** Module 09, notebook 01 in full.
4. **Generator–critic:** Module 05, notebook 04, Part 3.
5. **Handoffs:** Module 07, notebook 01 in full.

Optional status is specific to each pattern. For example, module 05's notebook 04 is optional communication background for supervisors, but Part 3 is mandatory for the generator–critic pattern.

For the complete repository sequence and prerequisites, see the [curriculum map](curriculum-map.md) and [repository README](../README.md).

## Sources and scope

Notebook paths and section references were checked against the local repository on October 13, 2026. This guide maps existing lessons; it does not claim that the notebooks were executed for this review.

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — sequential workflows, parallelization, orchestration, and evaluator–optimizer workflows.
- [LangChain: Subagents](https://github.com/langchain-ai/docs/blob/main/src/oss/langchain/multi-agent/subagents.mdx) — central supervisors and specialists called as tools.
- [LangChain: Learn](https://docs.langchain.com/oss/python/learn) — multi-agent tutorials, including subagents and customer-support handoffs.

Memory, human review, and loop limits can be combined with these patterns. This guide focuses on five coordination and workflow patterns, rather than every architecture in the repository.
