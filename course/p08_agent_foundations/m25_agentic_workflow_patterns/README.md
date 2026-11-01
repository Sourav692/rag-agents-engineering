# M25 — Agentic Workflow Patterns

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part VIII · Agent Foundations for RAG** · **Level:** Core · **Time:** ~7 h · **Notebooks:** 8 mandatory, 5 optional

## Why it matters

Every agentic RAG architecture is a combination of five patterns: CRAG is evaluator–optimizer, adaptive RAG is routing, query decomposition is orchestrator–worker. Learn the patterns once and the architectures become easy to read.

## Theory

Read the [theory page](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Fan-out and the concurrency cap](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/03_parallelization_sectioning_and_voting/interactive/fan-out-lab.html) (open the file in a browser)

## Learning objectives

- Chain prompts with quality gates between steps
- Route by handler or by model tier to control cost
- Fan out independent branches (sectioning and voting) and merge the results
- Decompose tasks at runtime with orchestrator–worker and the `Send` API
- Build bounded generate–critique–refine loops (evaluator–optimizer)
- Explain where LCEL stops (it cannot loop) and when a workflow needs LangGraph

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 25.1 | Prompt chaining with quality gates ([theory](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/01_prompt_chaining_with_quality_gates/README.md)) | [`01a_prompt_chaining_langgraph.ipynb`](notebooks/01a_prompt_chaining_langgraph.ipynb) | [`01b_prompt_chaining_structured_output.ipynb`](optional/01b_prompt_chaining_structured_output.ipynb) *(extension)*<br>[`01c_prompt_chaining_lcel.ipynb`](optional/01c_prompt_chaining_lcel.ipynb) *(alternate)* |
| 25.2 | Routing by handler and by model tier ([theory](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/02_routing_by_handler_and_by_model_tier/README.md)) | [`02a_routing_langgraph.ipynb`](notebooks/02a_routing_langgraph.ipynb)<br>[`02b_routing_by_model_tier.ipynb`](notebooks/02b_routing_by_model_tier.ipynb) | [`02c_routing_lcel_runnable_branch.ipynb`](optional/02c_routing_lcel_runnable_branch.ipynb) *(alternate)* |
| 25.3 | Parallelization: sectioning and voting ([theory](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/03_parallelization_sectioning_and_voting/README.md)) | [`03a_parallelization_langgraph.ipynb`](notebooks/03a_parallelization_langgraph.ipynb)<br>[`03b_parallelization_sectioning_and_voting.ipynb`](notebooks/03b_parallelization_sectioning_and_voting.ipynb) | [`03c_parallelization_lcel.ipynb`](optional/03c_parallelization_lcel.ipynb) *(alternate)* |
| 25.4 | Orchestrator–worker with the Send API ([theory](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/04_orchestrator_worker_with_the_send_api/README.md)) | [`04a_orchestrator_worker_send_api.ipynb`](notebooks/04a_orchestrator_worker_send_api.ipynb) | [`04b_orchestrator_worker_lcel_map.ipynb`](optional/04b_orchestrator_worker_lcel_map.ipynb) *(alternate)* |
| 25.5 | Evaluator–optimizer loops, always bounded: LangGraph vs LCEL ([theory](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/05_evaluator_optimizer_loops_always_bounded_langgraph_vs_lcel/README.md)) | [`05a_evaluator_optimizer_langgraph.ipynb`](notebooks/05a_evaluator_optimizer_langgraph.ipynb)<br>[`05b_evaluator_optimizer_lcel.ipynb`](notebooks/05b_evaluator_optimizer_lcel.ipynb) | — |

## Hands-on lab

Pattern mapping: rebuild query decomposition (M18) as orchestrator–worker and an answer-quality check as evaluator–optimizer, then compare latency and cost with the chain versions. Details: [lab/README.md](lab/README.md).

## Key concepts

[Workflow vs agent](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/01_prompt_chaining_with_quality_gates/README.md#workflow-vs-agent) · [Quality gates](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/01_prompt_chaining_with_quality_gates/README.md#quality-gates) · [Fan-out / fan-in](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/03_parallelization_sectioning_and_voting/README.md#fan-out--fan-in) · [Bounded loops](../../../theory/p08_agent_foundations/m25_agentic_workflow_patterns/05_evaluator_optimizer_loops_always_bounded_langgraph_vs_lcel/README.md#bounded-loops)

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `projects/` — runnable sub-projects (e.g. MCP servers and clients), where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_prompt_chaining_langgraph.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/05_prompt_chaining/notebooks/01_prompt_chaining_langgraph.ipynb` |
| `optional/01b_prompt_chaining_structured_output.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/05_prompt_chaining/notebooks/02_prompt_chaining_structured_output.ipynb` |
| `optional/01c_prompt_chaining_lcel.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/05_prompt_chaining/notebooks/03_prompt_chaining_lcel.ipynb` |
| `notebooks/02a_routing_langgraph.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/06_routing/notebooks/01_routing_langgraph.ipynb` |
| `notebooks/02b_routing_by_model_tier.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/06_routing/notebooks/02_routing_by_model_tier.ipynb` |
| `optional/02c_routing_lcel_runnable_branch.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/06_routing/notebooks/03_routing_lcel_runnable_branch.ipynb` |
| `notebooks/03a_parallelization_langgraph.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/07_parallelization/notebooks/01_parallelization_langgraph.ipynb` |
| `notebooks/03b_parallelization_sectioning_and_voting.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/07_parallelization/notebooks/02_parallelization_sectioning_and_voting.ipynb` |
| `optional/03c_parallelization_lcel.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/07_parallelization/notebooks/03_parallelization_lcel.ipynb` |
| `notebooks/04a_orchestrator_worker_send_api.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/08_orchestrator_worker/notebooks/01_orchestrator_worker_send_api.ipynb` |
| `optional/04b_orchestrator_worker_lcel_map.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/08_orchestrator_worker/notebooks/02_orchestrator_worker_lcel_map.ipynb` |
| `notebooks/05a_evaluator_optimizer_langgraph.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/09_evaluator_optimizer/notebooks/01_evaluator_optimizer_langgraph.ipynb` |
| `notebooks/05b_evaluator_optimizer_lcel.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/09_evaluator_optimizer/notebooks/02_evaluator_optimizer_lcel.ipynb` |
