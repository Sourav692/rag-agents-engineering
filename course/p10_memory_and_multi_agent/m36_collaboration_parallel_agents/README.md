# M36 — Collaboration, Control & Parallel Agents

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part X · Memory & Multi-Agent RAG** · **Level:** Expert · **Time:** ~4 h · **Notebooks:** 4 mandatory, 5 optional

## Why it matters

Research-style RAG benefits from several perspectives: STORM interviews multiple personas, debate surfaces conflicting evidence, and parallel agents cut latency.

## Learning objectives

- Share intermediate results through a blackboard
- Use debate, meta-controllers and ensembles to improve answers
- Generate multi-perspective research with STORM
- Run agents concurrently with supersteps, reducers, `Send` map-reduce, async nodes and `astream`

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 36.1 | Blackboard architectures | [`01a_blackboard_intro.ipynb`](notebooks/01a_blackboard_intro.ipynb) | [`01b_blackboard_research_team.ipynb`](optional/01b_blackboard_research_team.ipynb) *(extension)* |
| 36.2 | Debate *(optional lesson)* | — | [`02a_debate.ipynb`](optional/02a_debate.ipynb) *(extension)* |
| 36.3 | STORM: multi-perspective research and writing | [`03a_storm.ipynb`](notebooks/03a_storm.ipynb) | — |
| 36.4 | Meta-controllers, ensembles and emergent systems *(optional lesson)* | — | [`04a_meta_controller.ipynb`](optional/04a_meta_controller.ipynb) *(extension)*<br>[`04b_ensemble_parallel_exploration.ipynb`](optional/04b_ensemble_parallel_exploration.ipynb) *(extension)*<br>[`04c_cellular_automata.ipynb`](optional/04c_cellular_automata.ipynb) *(extension)* |
| 36.5 | Parallel agents, async nodes and streaming | [`05a_parallel_agents.ipynb`](notebooks/05a_parallel_agents.ipynb)<br>[`05b_async_multi_agent_streaming.ipynb`](notebooks/05b_async_multi_agent_streaming.ipynb) | — |

## Hands-on lab

Parallel retrieval: run the sub-questions of a decomposed query as parallel agents and stream partial answers, then report the latency saved. Details: [lab/README.md](lab/README.md).

## Key concepts

Blackboard · Debate · STORM · Map-reduce / async

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
| `notebooks/01a_blackboard_intro.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/01_blackboard_intro.ipynb` |
| `optional/01b_blackboard_research_team.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/02_blackboard_research_team.ipynb` |
| `optional/02a_debate.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/03_debate.ipynb` |
| `notebooks/03a_storm.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/04_storm.ipynb` |
| `optional/04a_meta_controller.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/05_meta_controller.ipynb` |
| `optional/04b_ensemble_parallel_exploration.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/06_ensemble_parallel_exploration.ipynb` |
| `optional/04c_cellular_automata.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/07_cellular_automata.ipynb` |
| `notebooks/05a_parallel_agents.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/09_async_and_parallel_multi_agent/notebooks/01_parallel_agents.ipynb` |
| `notebooks/05b_async_multi_agent_streaming.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/09_async_and_parallel_multi_agent/notebooks/02_async_multi_agent_streaming.ipynb` |
