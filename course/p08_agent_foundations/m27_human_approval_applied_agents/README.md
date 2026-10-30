# M27 — Human Approval & Applied Single-Agent Builds

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VIII · Agent Foundations for RAG** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 4 mandatory, 6 optional

## Why it matters

Real agents take actions, so they need approval gates. The applied builds also show text-to-SQL, which is often a better retriever than vectors for structured data.

## Theory

Read the [theory page](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [The approval gate](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/01_dry_run_harness_and_human_approval/interactive/approval-gate-lab.html) (open the file in a browser)

## Learning objectives

- Put a dry-run and approval gate in front of consequential actions
- Build research, competitive-intelligence and financial-analyst agents
- Retrieve from SQL databases with a text-to-SQL workflow and a text-to-SQL ReAct agent
- Build LLM workflow apps over business text (reviews, IT support, writing, quizzes)

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 27.1 | Dry-run harness and human approval ([theory](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/01_dry_run_harness_and_human_approval/README.md)) | [`01a_dry_run_harness.ipynb`](notebooks/01a_dry_run_harness.ipynb) | — |
| 27.2 | Research and competitive-intelligence agents | [`02a_research_assistant_agent.ipynb`](notebooks/02a_research_assistant_agent.ipynb) | [`02b_competitive_intelligence_agent.ipynb`](optional/02b_competitive_intelligence_agent.ipynb) *(extension)* |
| 27.3 | Financial analyst agent *(optional lesson)* | — | [`03a_financial_analyst_agent.ipynb`](optional/03a_financial_analyst_agent.ipynb) *(extension)* |
| 27.4 | Text-to-SQL: workflow vs ReAct agent ([theory](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/04_text_to_sql_workflow_vs_react_agent/README.md)) | [`04a_text2sql_workflow.ipynb`](notebooks/04a_text2sql_workflow.ipynb)<br>[`04b_text2sql_react_agent.ipynb`](notebooks/04b_text2sql_react_agent.ipynb) | — |
| 27.5 | LLM workflow apps: review analyst, IT support desk, tailored writer, quiz generator *(optional lesson)* ([theory](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/05_llm_workflow_apps_review_analyst_it_support_desk_tailored_writer_quiz_generator/README.md)) | — | [`05a_review_analyst.ipynb`](optional/05a_review_analyst.ipynb) *(extension)*<br>[`05b_multilingual_it_support_desk.ipynb`](optional/05b_multilingual_it_support_desk.ipynb) *(extension)*<br>[`05c_audience_tailored_writer.ipynb`](optional/05c_audience_tailored_writer.ipynb) *(extension)*<br>[`05d_quiz_generator.ipynb`](optional/05d_quiz_generator.ipynb) *(extension)* |

## Hands-on lab

SQL or vectors: answer the same 20 questions over a product catalogue with CSV RAG (M20) and with the text-to-SQL agent, and record which wins for each question type. Details: [lab/README.md](lab/README.md).

## Key concepts

[Approval gates](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/01_dry_run_harness_and_human_approval/README.md#approval-gates) · [Dry run](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/01_dry_run_harness_and_human_approval/README.md#dry-run) · [Text-to-SQL](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/04_text_to_sql_workflow_vs_react_agent/README.md#text-to-sql) · [Workflow apps](../../../theory/p08_agent_foundations/m27_human_approval_applied_agents/05_llm_workflow_apps_review_analyst_it_support_desk_tailored_writer_quiz_generator/README.md#workflow-apps)

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
| `notebooks/01a_dry_run_harness.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/13_human_approval_basics/notebooks/01_dry_run_harness.ipynb` |
| `notebooks/02a_research_assistant_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/14_applied_single_agent_builds/notebooks/01_research_assistant_agent.ipynb` |
| `optional/02b_competitive_intelligence_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/14_applied_single_agent_builds/notebooks/02_competitive_intelligence_agent.ipynb` |
| `optional/03a_financial_analyst_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/14_applied_single_agent_builds/notebooks/03_financial_analyst_agent.ipynb` |
| `notebooks/04a_text2sql_workflow.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/14_applied_single_agent_builds/notebooks/04_text2sql_workflow.ipynb` |
| `notebooks/04b_text2sql_react_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/14_applied_single_agent_builds/notebooks/05_text2sql_react_agent.ipynb` |
| `optional/05a_review_analyst.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/14_applied_single_agent_builds/notebooks/06_review_analyst.ipynb` |
| `optional/05b_multilingual_it_support_desk.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/14_applied_single_agent_builds/notebooks/07_multilingual_it_support_desk.ipynb` |
| `optional/05c_audience_tailored_writer.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/14_applied_single_agent_builds/notebooks/08_audience_tailored_writer.ipynb` |
| `optional/05d_quiz_generator.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/14_applied_single_agent_builds/notebooks/09_quiz_generator.ipynb` |
