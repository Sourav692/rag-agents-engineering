# M28 — Agentic RAG Foundations: Grading & Query Rewriting

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part VIII · Agentic RAG** · **Level:** Advanced · **Time:** ~4 h · **Notebooks:** 2 mandatory, 1 optional

## Why it matters

The smallest agentic step is to check what came back and try again when it is wrong. Every self-correcting architecture builds on this loop.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Grade, rewrite, retry](mandatory/theory/03_guardrails_query_optimisation_and_a_retry_loop/interactive/grade-rewrite-retry-lab.html) (open the file in a browser)

## Learning objectives

- Wrap a retriever as a LangGraph tool
- Grade retrieved documents for relevance with a structured-output LLM
- Rewrite the query and retry when documents fail the grade
- Add topic guardrails and a bounded query-enhancement retry loop

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 28.1 | Retriever as a tool; grade then rewrite in LangGraph ([theory](mandatory/theory/01_retriever_as_a_tool_grade_then_rewrite_in_langgraph/README.md)) | [`01a_simple_agentic_rag.ipynb`](mandatory/notebook/01a_simple_agentic_rag.ipynb) | — |
| 28.2 | The same agent on Databricks Vector Search *(optional lesson)* | — | [`02a_simple_agentic_rag_databricks.ipynb`](optional/notebook/02a_simple_agentic_rag_databricks.ipynb) *(platform-specific)* |
| 28.3 | Guardrails, query optimisation and a retry loop ([theory](mandatory/theory/03_guardrails_query_optimisation_and_a_retry_loop/README.md)) | [`03a_advanced_rag_agent.ipynb`](mandatory/notebook/03a_advanced_rag_agent.ipynb) | — |

## Hands-on lab

Grader loop: add a relevance grader and a two-retry rewrite loop to your Part V system and log how often each path fires on the golden set. Details: [lab/README.md](lab/README.md).

## Key concepts

[Document grader](mandatory/theory/01_retriever_as_a_tool_grade_then_rewrite_in_langgraph/README.md#document-grader) · [Conditional edges](mandatory/theory/01_retriever_as_a_tool_grade_then_rewrite_in_langgraph/README.md#conditional-edges) · [Bounded retries](mandatory/theory/03_guardrails_query_optimisation_and_a_retry_loop/README.md#bounded-retries) · [Topic guardrails](mandatory/theory/03_guardrails_query_optimisation_and_a_retry_loop/README.md#topic-guardrails)

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
| `mandatory/notebook/01a_simple_agentic_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/01_retrieval_grading_and_query_rewriting/notebooks/01_simple_agentic_rag.ipynb` |
| `optional/notebook/02a_simple_agentic_rag_databricks.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/01_retrieval_grading_and_query_rewriting/notebooks/02_simple_agentic_rag_databricks.ipynb` |
| `mandatory/notebook/03a_advanced_rag_agent.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/01_retrieval_grading_and_query_rewriting/notebooks/03_advanced_rag_agent.ipynb` |
