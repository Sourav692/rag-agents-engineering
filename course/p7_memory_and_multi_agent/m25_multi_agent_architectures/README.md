# M25 — Multi-Agent Architectures

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VII · Memory & Multi-Agent RAG** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 6 mandatory, 3 optional

## Why it matters

When one agent has too many tools or knowledge bases, split it: a supervisor routes to specialist retrieval agents. This is routing (M20) at the agent level.

## Learning objectives

- Decide when a task needs several agents instead of one
- Implement network, supervisor, tool-calling supervisor, hierarchical and custom architectures
- Design agent communication and add human review to a supervisor workflow
- Coordinate agents with handoffs and a swarm

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 25.1 | Monolithic vs multi-agent; a crew from scratch | [`01a_multi_agent_vs_monolithic_agent.ipynb`](notebooks/01a_multi_agent_vs_monolithic_agent.ipynb) | [`01b_multiagent_pattern_from_scratch.ipynb`](optional/01b_multiagent_pattern_from_scratch.ipynb) *(extension)* |
| 25.2 | The five multi-agent architectures and agent communication | [`02a_five_multi_agent_architectures.ipynb`](notebooks/02a_five_multi_agent_architectures.ipynb) | [`02b_agent_communication.ipynb`](optional/02b_agent_communication.ipynb) *(extension)* |
| 25.3 | Supervisor workflow with human review *(optional lesson)* | — | [`03a_supervisor_workflow_with_human_review.ipynb`](optional/03a_supervisor_workflow_with_human_review.ipynb) *(extension)* |
| 25.4 | Supervisors and hierarchical teams | [`04a_supervisor_pattern.ipynb`](notebooks/04a_supervisor_pattern.ipynb)<br>[`04b_hierarchical_agents.ipynb`](notebooks/04b_hierarchical_agents.ipynb) | — |
| 25.5 | Handoffs and swarms | [`05a_agent_handoffs.ipynb`](notebooks/05a_agent_handoffs.ipynb)<br>[`05b_multi_agent_swarm.ipynb`](notebooks/05b_multi_agent_swarm.ipynb) | — |

## Hands-on lab

Specialist retrievers: replace the single router from M20 with a supervisor over three specialist RAG agents and compare routing accuracy and cost. Details: [lab/README.md](lab/README.md).

## Key concepts

Supervisor · Hierarchical teams · Handoffs · Swarm

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
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
