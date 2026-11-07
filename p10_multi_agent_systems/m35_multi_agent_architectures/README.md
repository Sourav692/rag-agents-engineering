# M35 — Multi-Agent Architectures

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part X · Multi-Agent Systems** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 6 mandatory, 3 optional

## Why it matters

When one agent has too many tools or knowledge bases, split it: a supervisor routes to specialist retrieval agents. This is routing (M30) at the agent level.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Who routes, and what it costs](mandatory/theory/05_handoffs_and_swarms/interactive/routing-cost-lab.html) (open the file in a browser)

## Learning objectives

- Decide when a task needs several agents instead of one
- Implement network, supervisor, tool-calling supervisor, hierarchical and custom architectures
- Design agent communication and add human review to a supervisor workflow
- Coordinate agents with handoffs and a swarm

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 35.1 | Monolithic vs multi-agent; a crew from scratch ([theory](mandatory/theory/01_monolithic_vs_multi_agent_a_crew_from_scratch/README.md)) | [`01a_multi_agent_vs_monolithic_agent.ipynb`](mandatory/notebook/01a_multi_agent_vs_monolithic_agent.ipynb) | [`01b_multiagent_pattern_from_scratch.ipynb`](optional/notebook/01b_multiagent_pattern_from_scratch.ipynb) *(extension)* |
| 35.2 | The five multi-agent architectures and agent communication ([theory](mandatory/theory/02_the_five_multi_agent_architectures_and_agent_communication/README.md)) | [`02a_five_multi_agent_architectures.ipynb`](mandatory/notebook/02a_five_multi_agent_architectures.ipynb) | [`02b_agent_communication.ipynb`](optional/notebook/02b_agent_communication.ipynb) *(extension)* |
| 35.3 | Supervisor workflow with human review *(optional lesson)* ([theory](optional/theory/03_supervisor_workflow_with_human_review/README.md)) | — | [`03a_supervisor_workflow_with_human_review.ipynb`](optional/notebook/03a_supervisor_workflow_with_human_review.ipynb) *(extension)* |
| 35.4 | Supervisors and hierarchical teams ([theory](mandatory/theory/04_supervisors_and_hierarchical_teams/README.md)) | [`04a_supervisor_pattern.ipynb`](mandatory/notebook/04a_supervisor_pattern.ipynb)<br>[`04b_hierarchical_agents.ipynb`](mandatory/notebook/04b_hierarchical_agents.ipynb) | — |
| 35.5 | Handoffs and swarms ([theory](mandatory/theory/05_handoffs_and_swarms/README.md)) | [`05a_agent_handoffs.ipynb`](mandatory/notebook/05a_agent_handoffs.ipynb)<br>[`05b_multi_agent_swarm.ipynb`](mandatory/notebook/05b_multi_agent_swarm.ipynb) | — |

## Hands-on lab

Specialist retrievers: replace the single router from M30 with a supervisor over three specialist RAG agents and compare routing accuracy and cost. Details: [lab/README.md](lab/README.md).

## Key concepts

[Supervisor](mandatory/theory/04_supervisors_and_hierarchical_teams/README.md#supervisor) · [Hierarchical teams](mandatory/theory/04_supervisors_and_hierarchical_teams/README.md#hierarchical-teams) · [Handoffs](mandatory/theory/05_handoffs_and_swarms/README.md#handoffs) · [Swarm](mandatory/theory/05_handoffs_and_swarms/README.md#swarm)

## Folder layout

- `mandatory/notebook/`: the mandatory track, plus the helper files those notebooks import
- `optional/notebook/`: alternate, platform-specific, extension and exercise notebooks
- `mandatory/theory/`: the module page, its `index.html` and the pages of lessons with a mandatory notebook
- `optional/theory/`: the pages of lessons whose notebooks are all optional
- `projects/`: runnable sub-projects (for example MCP servers and clients), where the module has them
- `assets/`: images and data used by this module's notebooks, where it has them
- `lab/`: the module lab brief, its solution notebook in `solution/` and its data in `data/`

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `mandatory/notebook/01a_multi_agent_vs_monolithic_agent.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/01_multi_agent_vs_monolithic_agent.ipynb` |
| `optional/notebook/01b_multiagent_pattern_from_scratch.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/02_multiagent_pattern_from_scratch.ipynb` |
| `mandatory/notebook/02a_five_multi_agent_architectures.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb` |
| `optional/notebook/02b_agent_communication.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb` |
| `optional/notebook/03a_supervisor_workflow_with_human_review.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb` |
| `mandatory/notebook/04a_supervisor_pattern.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb` |
| `mandatory/notebook/04b_hierarchical_agents.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/06_supervisor_and_hierarchical_agents/notebooks/02_hierarchical_agents.ipynb` |
| `mandatory/notebook/05a_agent_handoffs.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/07_swarm_and_handoffs/notebooks/01_agent_handoffs.ipynb` |
| `mandatory/notebook/05b_multi_agent_swarm.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/07_swarm_and_handoffs/notebooks/02_multi_agent_swarm.ipynb` |
