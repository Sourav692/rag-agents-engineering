# M36 — Collaboration, Control & Parallel Agents

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part X · Multi-Agent Systems** · **Level:** Expert · **Time:** ~4 h · **Notebooks:** 4 mandatory, 5 optional

## Why it matters

Research-style RAG benefits from several perspectives: STORM interviews multiple personas, debate surfaces conflicting evidence, and parallel agents cut latency.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Parallel sub-question agents](mandatory/theory/05_parallel_agents_async_nodes_and_streaming/interactive/parallel-subquestions-lab.html) (open the file in a browser)

## Learning objectives

- Share intermediate results through a blackboard
- Use debate, meta-controllers and ensembles to improve answers
- Generate multi-perspective research with STORM
- Run agents concurrently with supersteps, reducers, `Send` map-reduce, async nodes and `astream`

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 36.1 | Blackboard architectures ([theory](mandatory/theory/01_blackboard_architectures/README.md)) | [`01a_blackboard_intro.ipynb`](mandatory/notebook/01a_blackboard_intro.ipynb) | [`01b_blackboard_research_team.ipynb`](optional/notebook/01b_blackboard_research_team.ipynb) *(extension)* |
| 36.2 | Debate *(optional lesson)* ([theory](optional/theory/02_debate/README.md)) | — | [`02a_debate.ipynb`](optional/notebook/02a_debate.ipynb) *(extension)* |
| 36.3 | STORM: multi-perspective research and writing ([theory](mandatory/theory/03_storm_multi_perspective_research_and_writing/README.md)) | [`03a_storm.ipynb`](mandatory/notebook/03a_storm.ipynb) | — |
| 36.4 | Meta-controllers, ensembles and emergent systems *(optional lesson)* ([theory](optional/theory/04_meta_controllers_ensembles_and_emergent_systems/README.md)) | — | [`04a_meta_controller.ipynb`](optional/notebook/04a_meta_controller.ipynb) *(extension)*<br>[`04b_ensemble_parallel_exploration.ipynb`](optional/notebook/04b_ensemble_parallel_exploration.ipynb) *(extension)*<br>[`04c_cellular_automata.ipynb`](optional/notebook/04c_cellular_automata.ipynb) *(extension)* |
| 36.5 | Parallel agents, async nodes and streaming ([theory](mandatory/theory/05_parallel_agents_async_nodes_and_streaming/README.md)) | [`05a_parallel_agents.ipynb`](mandatory/notebook/05a_parallel_agents.ipynb)<br>[`05b_async_multi_agent_streaming.ipynb`](mandatory/notebook/05b_async_multi_agent_streaming.ipynb) | — |

## Hands-on lab

Parallel retrieval: run the sub-questions of a decomposed query as parallel agents and stream partial answers, then report the latency saved. Details: [lab/README.md](lab/README.md).

## Key concepts

[Blackboard](mandatory/theory/01_blackboard_architectures/README.md#blackboard) · [Debate](optional/theory/02_debate/README.md#debate) · [STORM](mandatory/theory/03_storm_multi_perspective_research_and_writing/README.md#storm) · [Map-reduce / async](mandatory/theory/05_parallel_agents_async_nodes_and_streaming/README.md#map-reduce--async)

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
| `mandatory/notebook/01a_blackboard_intro.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/01_blackboard_intro.ipynb` |
| `optional/notebook/01b_blackboard_research_team.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/02_blackboard_research_team.ipynb` |
| `optional/notebook/02a_debate.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/03_debate.ipynb` |
| `mandatory/notebook/03a_storm.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/04_storm.ipynb` |
| `optional/notebook/04a_meta_controller.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/05_meta_controller.ipynb` |
| `optional/notebook/04b_ensemble_parallel_exploration.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/06_ensemble_parallel_exploration.ipynb` |
| `optional/notebook/04c_cellular_automata.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/08_collaboration_and_control_patterns/notebooks/07_cellular_automata.ipynb` |
| `mandatory/notebook/05a_parallel_agents.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/09_async_and_parallel_multi_agent/notebooks/01_parallel_agents.ipynb` |
| `mandatory/notebook/05b_async_multi_agent_streaming.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/09_async_and_parallel_multi_agent/notebooks/02_async_multi_agent_streaming.ipynb` |
