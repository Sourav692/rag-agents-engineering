# M37 — Multi-Agent Applied Builds

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part X · Multi-Agent Systems** · **Level:** Expert · **Time:** ~4 h · **Notebooks:** 6 mandatory, 12 optional

## Why it matters

The applied builds show what production multi-agent systems need beyond the happy path: compliance checks, edge cases, testing, error handling and memory merging.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Router test bench](mandatory/theory/02_hardening_edge_cases_testing_and_system_wide_error_handling/interactive/router-test-bench-lab.html) (open the file in a browser)

## Learning objectives

- Build a multi-agent hotel reservation system step by step, including compliance, testing and error handling
- Pair developer and tester agents
- Build supervisor-led financial research and multi-agent research and summarisation systems
- Package sub-agents, skills, long-term memory and an execution backend as a deep agent

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 37.1 | Hotel system: environment, coordinator, reservation agent, compliance ([theory](mandatory/theory/01_hotel_system_environment_coordinator_reservation_agent_compliance/README.md)) | [`01a_hotel_environment_and_coordinator.ipynb`](mandatory/notebook/01a_hotel_environment_and_coordinator.ipynb)<br>[`01b_hotel_reservation_agent.ipynb`](mandatory/notebook/01b_hotel_reservation_agent.ipynb)<br>[`01c_hotel_compliance_checker.ipynb`](mandatory/notebook/01c_hotel_compliance_checker.ipynb) | — |
| 37.2 | Hardening: edge cases, testing and system-wide error handling ([theory](mandatory/theory/02_hardening_edge_cases_testing_and_system_wide_error_handling/README.md)) | [`02a_hotel_edge_cases_and_errors.ipynb`](mandatory/notebook/02a_hotel_edge_cases_and_errors.ipynb)<br>[`02b_hotel_testing_the_system.ipynb`](mandatory/notebook/02b_hotel_testing_the_system.ipynb) | [`02c_hotel_system_wide_error_handling.ipynb`](optional/notebook/02c_hotel_system_wide_error_handling.ipynb) *(extension)* |
| 37.3 | Scaling: parallel agents, memory merging, language and sentiment, web search *(optional lesson)* ([theory](optional/theory/03_scaling_parallel_agents_memory_merging_language_and_sentiment_web_search/README.md)) | — | [`03a_hotel_parallel_reservation_agents.ipynb`](optional/notebook/03a_hotel_parallel_reservation_agents.ipynb) *(extension)*<br>[`03b_hotel_merging_and_conversation_memory.ipynb`](optional/notebook/03b_hotel_merging_and_conversation_memory.ipynb) *(extension)*<br>[`03c_hotel_guest_language_and_sentiment.ipynb`](optional/notebook/03c_hotel_guest_language_and_sentiment.ipynb) *(extension)*<br>[`03d_hotel_web_search_integration.ipynb`](optional/notebook/03d_hotel_web_search_integration.ipynb) *(extension)* |
| 37.4 | Research systems: supervisor financial research, summarisation, full research system ([theory](mandatory/theory/04_research_systems_supervisor_financial_research_summarisation_full_research_system/README.md)) | [`04c_multi_agent_research_system.ipynb`](mandatory/notebook/04c_multi_agent_research_system.ipynb) | [`04a_supervisor_financial_research.ipynb`](optional/notebook/04a_supervisor_financial_research.ipynb) *(extension)*<br>[`04b_multi_agent_research_summarization.ipynb`](optional/notebook/04b_multi_agent_research_summarization.ipynb) *(extension)* |
| 37.5 | Five practical agent patterns, side by side *(optional lesson)* | — | [`05a_sequential_and_conditional_workflows.ipynb`](optional/notebook/05a_sequential_and_conditional_workflows.ipynb) *(extension)*<br>[`05b_supervisor_agents_as_tools.ipynb`](optional/notebook/05b_supervisor_agents_as_tools.ipynb) *(extension)*<br>[`05c_parallel_fan_out_fan_in.ipynb`](optional/notebook/05c_parallel_fan_out_fan_in.ipynb) *(extension)*<br>[`05d_generator_critic_loop.ipynb`](optional/notebook/05d_generator_critic_loop.ipynb) *(extension)*<br>[`05e_handoffs_with_swarm.ipynb`](optional/notebook/05e_handoffs_with_swarm.ipynb) *(extension)* |

## Hands-on lab

Research team: build a supervisor with a RAG researcher, a web researcher and a writer that cites sources, then test it on edge cases (no results, conflicting sources, tool failure). Details: [lab/README.md](lab/README.md).

## Key concepts

[Compliance agent](mandatory/theory/01_hotel_system_environment_coordinator_reservation_agent_compliance/README.md#compliance-agent) · [System testing](mandatory/theory/02_hardening_edge_cases_testing_and_system_wide_error_handling/README.md#system-testing) · [Memory merging](optional/theory/03_scaling_parallel_agents_memory_merging_language_and_sentiment_web_search/README.md#memory-merging)

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
| `mandatory/notebook/01a_hotel_environment_and_coordinator.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/01_hotel_environment_and_coordinator.ipynb` |
| `mandatory/notebook/01b_hotel_reservation_agent.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/02_hotel_reservation_agent.ipynb` |
| `mandatory/notebook/01c_hotel_compliance_checker.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/03_hotel_compliance_checker.ipynb` |
| `mandatory/notebook/02a_hotel_edge_cases_and_errors.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/04_hotel_edge_cases_and_errors.ipynb` |
| `mandatory/notebook/02b_hotel_testing_the_system.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/05_hotel_testing_the_system.ipynb` |
| `optional/notebook/02c_hotel_system_wide_error_handling.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/09_hotel_system_wide_error_handling.ipynb` |
| `optional/notebook/03a_hotel_parallel_reservation_agents.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/06_hotel_parallel_reservation_agents.ipynb` |
| `optional/notebook/03b_hotel_merging_and_conversation_memory.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/07_hotel_merging_and_conversation_memory.ipynb` |
| `optional/notebook/03c_hotel_guest_language_and_sentiment.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/08_hotel_guest_language_and_sentiment.ipynb` |
| `optional/notebook/03d_hotel_web_search_integration.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/10_hotel_web_search_integration.ipynb` |
| `optional/notebook/04a_supervisor_financial_research.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/12_supervisor_financial_research.ipynb` |
| `optional/notebook/04b_multi_agent_research_summarization.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/13_multi_agent_research_summarization.ipynb` |
| `mandatory/notebook/04c_multi_agent_research_system.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/10_multi_agent_applied_builds/notebooks/14_multi_agent_research_system.ipynb` |
| `optional/notebook/05a_sequential_and_conditional_workflows.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/12_five_practical_agent_patterns/notebooks/01_sequential_and_conditional_workflows.ipynb` |
| `optional/notebook/05b_supervisor_agents_as_tools.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/12_five_practical_agent_patterns/notebooks/02_supervisor_agents_as_tools.ipynb` |
| `optional/notebook/05c_parallel_fan_out_fan_in.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/12_five_practical_agent_patterns/notebooks/03_parallel_fan_out_fan_in.ipynb` |
| `optional/notebook/05d_generator_critic_loop.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/12_five_practical_agent_patterns/notebooks/04_generator_critic_loop.ipynb` |
| `optional/notebook/05e_handoffs_with_swarm.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/12_five_practical_agent_patterns/notebooks/05_handoffs_with_swarm.ipynb` |
