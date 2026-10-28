# M27 — Multi-Agent Applied Builds & Deep Agents

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VII · Memory & Multi-Agent RAG** · **Level:** Expert · **Time:** ~6 h · **Notebooks:** 7 mandatory, 10 optional

## Why it matters

The applied builds show what production multi-agent systems need beyond the happy path: compliance checks, edge cases, testing, error handling and memory merging.

## Learning objectives

- Build a multi-agent hotel reservation system step by step, including compliance, testing and error handling
- Pair developer and tester agents
- Build supervisor-led financial research and multi-agent research and summarisation systems
- Package sub-agents, skills, long-term memory and an execution backend as a deep agent

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 27.1 | Hotel system: environment, coordinator, reservation agent, compliance | [`01a_hotel_environment_and_coordinator.ipynb`](notebooks/01a_hotel_environment_and_coordinator.ipynb)<br>[`01b_hotel_reservation_agent.ipynb`](notebooks/01b_hotel_reservation_agent.ipynb)<br>[`01c_hotel_compliance_checker.ipynb`](notebooks/01c_hotel_compliance_checker.ipynb) | — |
| 27.2 | Hardening: edge cases, testing and system-wide error handling | [`02a_hotel_edge_cases_and_errors.ipynb`](notebooks/02a_hotel_edge_cases_and_errors.ipynb)<br>[`02b_hotel_testing_the_system.ipynb`](notebooks/02b_hotel_testing_the_system.ipynb) | [`02c_hotel_system_wide_error_handling.ipynb`](optional/02c_hotel_system_wide_error_handling.ipynb) *(extension)* |
| 27.3 | Scaling: parallel agents, memory merging, language and sentiment, web search *(optional lesson)* | — | [`03a_hotel_parallel_reservation_agents.ipynb`](optional/03a_hotel_parallel_reservation_agents.ipynb) *(extension)*<br>[`03b_hotel_merging_and_conversation_memory.ipynb`](optional/03b_hotel_merging_and_conversation_memory.ipynb) *(extension)*<br>[`03c_hotel_guest_language_and_sentiment.ipynb`](optional/03c_hotel_guest_language_and_sentiment.ipynb) *(extension)*<br>[`03d_hotel_web_search_integration.ipynb`](optional/03d_hotel_web_search_integration.ipynb) *(extension)* |
| 27.4 | Developer vs tester agents *(optional lesson)* | — | [`04a_developer_vs_tester_agents.ipynb`](optional/04a_developer_vs_tester_agents.ipynb) *(extension)* |
| 27.5 | Research systems: supervisor financial research, summarisation, full research system | [`05c_multi_agent_research_system.ipynb`](notebooks/05c_multi_agent_research_system.ipynb) | [`05a_supervisor_financial_research.ipynb`](optional/05a_supervisor_financial_research.ipynb) *(extension)*<br>[`05b_multi_agent_research_summarization.ipynb`](optional/05b_multi_agent_research_summarization.ipynb) *(extension)* |
| 27.6 | Deep agents: orchestrator, sub-agents, skills and long-term memory | [`06a_simple_coding_agent.py`](notebooks/06a_simple_coding_agent.py) | [`06b_long_term_memory_agent.py`](optional/06b_long_term_memory_agent.py) *(extension)*<br>[`06c_skills`](optional/06c_skills) *(extension)* |

## Hands-on lab

Research team: build a supervisor with a RAG researcher, a web researcher and a writer that cites sources, then test it on edge cases (no results, conflicting sources, tool failure). Details: [lab/README.md](lab/README.md).

## Key concepts

Compliance agent · System testing · Memory merging · Deep-agent harness

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_hotel_environment_and_coordinator.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/01_hotel_environment_and_coordinator.ipynb` |
| `notebooks/01b_hotel_reservation_agent.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/02_hotel_reservation_agent.ipynb` |
| `notebooks/01c_hotel_compliance_checker.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/03_hotel_compliance_checker.ipynb` |
| `notebooks/02a_hotel_edge_cases_and_errors.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/04_hotel_edge_cases_and_errors.ipynb` |
| `notebooks/02b_hotel_testing_the_system.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/05_hotel_testing_the_system.ipynb` |
| `optional/02c_hotel_system_wide_error_handling.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/09_hotel_system_wide_error_handling.ipynb` |
| `optional/03a_hotel_parallel_reservation_agents.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/06_hotel_parallel_reservation_agents.ipynb` |
| `optional/03b_hotel_merging_and_conversation_memory.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/07_hotel_merging_and_conversation_memory.ipynb` |
| `optional/03c_hotel_guest_language_and_sentiment.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/08_hotel_guest_language_and_sentiment.ipynb` |
| `optional/03d_hotel_web_search_integration.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/10_hotel_web_search_integration.ipynb` |
| `optional/04a_developer_vs_tester_agents.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/11_developer_vs_tester_agents.ipynb` |
| `optional/05a_supervisor_financial_research.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/12_supervisor_financial_research.ipynb` |
| `optional/05b_multi_agent_research_summarization.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/13_multi_agent_research_summarization.ipynb` |
| `notebooks/05c_multi_agent_research_system.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/14_multi_agent_research_system.ipynb` |
| `notebooks/06a_simple_coding_agent.py` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/11_deep_agents_and_harness_engineering/notebooks/simple_coding_agent.py` |
| `optional/06b_long_term_memory_agent.py` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/11_deep_agents_and_harness_engineering/notebooks/long_term_memory_agent.py` |
| `optional/06c_skills` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/11_deep_agents_and_harness_engineering/notebooks/skills` |
