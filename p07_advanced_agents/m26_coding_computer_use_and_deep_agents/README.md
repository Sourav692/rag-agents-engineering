# M26 — Coding, Computer-Use & Deep Agents

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part VII · Advanced Agents** · **Level:** Expert · **Time:** ~5 h · **Notebooks:** 2 mandatory, 6 optional

## Why it matters

Agents that write code, drive a browser or run for hours need a harness: sub-agents, a file system, skills and a tester that checks the work.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).


## Learning objectives

- Run ReAct agents in web, code and computer-use environments and see where the loop changes
- Pair a developer agent with a tester agent and iterate until the tests pass
- Build a deep agent with an orchestrator, sub-agents, skills and long-term memory

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 26.1 | Applied ReAct: web research, SWE and computer-use agents ([theory](mandatory/theory/01_applied_react_web_research_swe_and_computer_use_agents/README.md)) | [`01a_web_research_agent.ipynb`](mandatory/notebook/01a_web_research_agent.ipynb) | [`01b_swe_agent_applied.ipynb`](optional/notebook/01b_swe_agent_applied.ipynb) *(extension)*<br>[`01c_browser_agent_computer_use.ipynb`](optional/notebook/01c_browser_agent_computer_use.ipynb) *(extension)*<br>[`01d_vision_driven_computer_use.ipynb`](optional/notebook/01d_vision_driven_computer_use.ipynb) *(extension)* |
| 26.2 | Developer vs tester agents *(optional lesson)* ([theory](optional/theory/02_developer_vs_tester_agents/README.md)) | — | [`02a_developer_vs_tester_agents.ipynb`](optional/notebook/02a_developer_vs_tester_agents.ipynb) *(extension)* |
| 26.3 | Deep agents: orchestrator, sub-agents, skills and long-term memory ([theory](mandatory/theory/03_deep_agents_orchestrator_sub_agents_skills_and_long_term_memory/README.md)) | [`03a_simple_coding_agent.py`](mandatory/notebook/03a_simple_coding_agent.py) | [`03b_long_term_memory_agent.py`](optional/notebook/03b_long_term_memory_agent.py) *(extension)*<br>[`03c_skills`](optional/notebook/03c_skills) *(extension)* |

## Hands-on lab

Coding agent: give a deep agent a developer sub-agent and a tester sub-agent, ask it for a small Python function with tests, and log each iteration until the tests pass. Details: [lab/README.md](lab/README.md).

## Key concepts

[Deep-agent harness](mandatory/theory/03_deep_agents_orchestrator_sub_agents_skills_and_long_term_memory/README.md#deep-agent-harness)

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
| `mandatory/notebook/01a_web_research_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/04_web_research_agent.ipynb` |
| `optional/notebook/01b_swe_agent_applied.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/05_swe_agent_applied.ipynb` |
| `optional/notebook/01c_browser_agent_computer_use.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/06_browser_agent_computer_use.ipynb` |
| `optional/notebook/01d_vision_driven_computer_use.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/07_vision_driven_computer_use.ipynb` |
| `optional/notebook/02a_developer_vs_tester_agents.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/11_developer_vs_tester_agents.ipynb` |
| `mandatory/notebook/03a_simple_coding_agent.py` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/11_deep_agents_and_harness_engineering/notebooks/simple_coding_agent.py` |
| `optional/notebook/03b_long_term_memory_agent.py` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/11_deep_agents_and_harness_engineering/notebooks/long_term_memory_agent.py` |
| `optional/notebook/03c_skills` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/11_deep_agents_and_harness_engineering/notebooks/skills` |
