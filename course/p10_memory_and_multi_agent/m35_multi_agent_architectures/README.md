# M35 — Multi-Agent Architectures

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part X · Memory & Multi-Agent RAG** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 6 mandatory, 3 optional

## Why it matters

When one agent has too many tools or knowledge bases, split it: a supervisor routes to specialist retrieval agents. This is routing (M30) at the agent level.

## Theory

Read the [theory page](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Who routes, and what it costs](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/05_handoffs_and_swarms/interactive/routing-cost-lab.html) (open the file in a browser)

## Learning objectives

- Decide when a task needs several agents instead of one
- Implement network, supervisor, tool-calling supervisor, hierarchical and custom architectures
- Design agent communication and add human review to a supervisor workflow
- Coordinate agents with handoffs and a swarm

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 35.1 | Monolithic vs multi-agent; a crew from scratch ([theory](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/01_monolithic_vs_multi_agent_a_crew_from_scratch/README.md)) | [`01a_multi_agent_vs_monolithic_agent.ipynb`](notebooks/01a_multi_agent_vs_monolithic_agent.ipynb) | [`01b_multiagent_pattern_from_scratch.ipynb`](optional/01b_multiagent_pattern_from_scratch.ipynb) *(extension)* |
| 35.2 | The five multi-agent architectures and agent communication ([theory](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/02_the_five_multi_agent_architectures_and_agent_communication/README.md)) | [`02a_five_multi_agent_architectures.ipynb`](notebooks/02a_five_multi_agent_architectures.ipynb) | [`02b_agent_communication.ipynb`](optional/02b_agent_communication.ipynb) *(extension)* |
| 35.3 | Supervisor workflow with human review *(optional lesson)* ([theory](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/03_supervisor_workflow_with_human_review/README.md)) | — | [`03a_supervisor_workflow_with_human_review.ipynb`](optional/03a_supervisor_workflow_with_human_review.ipynb) *(extension)* |
| 35.4 | Supervisors and hierarchical teams ([theory](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/04_supervisors_and_hierarchical_teams/README.md)) | [`04a_supervisor_pattern.ipynb`](notebooks/04a_supervisor_pattern.ipynb)<br>[`04b_hierarchical_agents.ipynb`](notebooks/04b_hierarchical_agents.ipynb) | — |
| 35.5 | Handoffs and swarms ([theory](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/05_handoffs_and_swarms/README.md)) | [`05a_agent_handoffs.ipynb`](notebooks/05a_agent_handoffs.ipynb)<br>[`05b_multi_agent_swarm.ipynb`](notebooks/05b_multi_agent_swarm.ipynb) | — |

## Hands-on lab

Specialist retrievers: replace the single router from M30 with a supervisor over three specialist RAG agents and compare routing accuracy and cost. Details: [lab/README.md](lab/README.md).

## Key concepts

[Supervisor](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/04_supervisors_and_hierarchical_teams/README.md#supervisor) · [Hierarchical teams](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/04_supervisors_and_hierarchical_teams/README.md#hierarchical-teams) · [Handoffs](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/05_handoffs_and_swarms/README.md#handoffs) · [Swarm](../../../theory/p10_memory_and_multi_agent/m35_multi_agent_architectures/05_handoffs_and_swarms/README.md#swarm)

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
| `notebooks/01a_multi_agent_vs_monolithic_agent.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/01_multi_agent_vs_monolithic_agent.ipynb` |
| `optional/01b_multiagent_pattern_from_scratch.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/02_multiagent_pattern_from_scratch.ipynb` |
| `notebooks/02a_five_multi_agent_architectures.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb` |
| `optional/02b_agent_communication.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb` |
| `optional/03a_supervisor_workflow_with_human_review.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb` |
| `notebooks/04a_supervisor_pattern.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb` |
| `notebooks/04b_hierarchical_agents.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/06_supervisor_and_hierarchical_agents/notebooks/02_hierarchical_agents.ipynb` |
| `notebooks/05a_agent_handoffs.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/07_swarm_and_handoffs/notebooks/01_agent_handoffs.ipynb` |
| `notebooks/05b_multi_agent_swarm.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/07_swarm_and_handoffs/notebooks/02_multi_agent_swarm.ipynb` |
