# Supervisor to Swarm — study route

A five-session route through notebooks that already live in this repository's modules.
Open [`SUPERVISOR_TO_SWARM.html`](SUPERVISOR_TO_SWARM.html) alongside them: it carries
the goals, the classes and functions to read for, the exercises and the checkpoints for
each session.

**This folder holds no notebooks.** The route was first built as a folder of renamed copies;
the copies were dropped because they were byte-identical to the originals, and a second copy
would give multi-agent orchestration two homes in the repo. Work through the originals below
instead, so fixes to them reach you.

## Sessions

| # | Notebook | Session adds |
| --- | --- | --- |
| 1 | [`modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb`](../../modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb) | All five architectures side by side · `Command(goto=)` |
| 2 | [`modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb`](../../modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb) | State schema as the design decision · `RouteDecision` |
| 3 | [`modules/06_supervisor_and_hierarchical_agents/notebooks/02_hierarchical_agents.ipynb`](../../modules/06_supervisor_and_hierarchical_agents/notebooks/02_hierarchical_agents.ipynb) | Compiled subgraph as a node · `TeamState` |
| 4 | [`modules/07_swarm_and_handoffs/notebooks/02_multi_agent_swarm.ipynb`](../../modules/07_swarm_and_handoffs/notebooks/02_multi_agent_swarm.ipynb) | Handoff tools · `create_swarm` · checkpointer memory |
| 5 | [`modules/10_multi_agent_applied_builds/notebooks/14_multi_agent_research_system.ipynb`](../../modules/10_multi_agent_applied_builds/notebooks/14_multi_agent_research_system.ipynb) | `Send()` dynamic fan-out · cyclic quality gate |

Next step after session 5:
[`modules/09_async_and_parallel_multi_agent/notebooks/02_async_multi_agent_streaming.ipynb`](../../modules/09_async_and_parallel_multi_agent/notebooks/02_async_multi_agent_streaming.ipynb)
takes the same patterns async.

## Suggested pace

Each session is about 90 minutes (28–41 cells). Session 4 builds real RAG and NL2SQL
sub-agents before the swarm exists, so test the sub-agents first and the assembly second.

## Running them

Every notebook loads keys from the repository-root `.env` (`load_dotenv(find_dotenv(usecwd=True))`)
and builds its model with the shared `aied_helpers` package, so notebook depth doesn't matter. The
vector stores these sessions use are in memory. The only file written beside a notebook is session 4's
`chinook.db`, the sample database it downloads once from a pinned commit (git-ignored).
