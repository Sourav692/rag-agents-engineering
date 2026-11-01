# M28 — Agentic RAG Foundations: Grading & Query Rewriting

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part IX · Agentic & Self-Correcting RAG** · **Level:** Advanced · **Time:** ~4 h · **Notebooks:** 2 mandatory, 1 optional

## Why it matters

The smallest agentic step is to check what came back and try again when it is wrong. Every self-correcting architecture builds on this loop.

## Theory

Read the [theory page](../../../theory/p09_agentic_rag/m28_retrieval_grading_rewriting/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p09_agentic_rag/m28_retrieval_grading_rewriting/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Grade, rewrite, retry](../../../theory/p09_agentic_rag/m28_retrieval_grading_rewriting/03_guardrails_query_optimisation_and_a_retry_loop/interactive/grade-rewrite-retry-lab.html) (open the file in a browser)

## Learning objectives

- Wrap a retriever as a LangGraph tool
- Grade retrieved documents for relevance with a structured-output LLM
- Rewrite the query and retry when documents fail the grade
- Add topic guardrails and a bounded query-enhancement retry loop

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 28.1 | Retriever as a tool; grade then rewrite in LangGraph ([theory](../../../theory/p09_agentic_rag/m28_retrieval_grading_rewriting/01_retriever_as_a_tool_grade_then_rewrite_in_langgraph/README.md)) | [`01a_simple_agentic_rag.ipynb`](notebooks/01a_simple_agentic_rag.ipynb) | — |
| 28.2 | The same agent on Databricks Vector Search *(optional lesson)* | — | [`02a_simple_agentic_rag_databricks.ipynb`](optional/02a_simple_agentic_rag_databricks.ipynb) *(platform-specific)* |
| 28.3 | Guardrails, query optimisation and a retry loop ([theory](../../../theory/p09_agentic_rag/m28_retrieval_grading_rewriting/03_guardrails_query_optimisation_and_a_retry_loop/README.md)) | [`03a_advanced_rag_agent.ipynb`](notebooks/03a_advanced_rag_agent.ipynb) | — |

## Hands-on lab

Grader loop: add a relevance grader and a two-retry rewrite loop to your Part VII system and log how often each path fires on the golden set. Details: [lab/README.md](lab/README.md).

## Key concepts

[Document grader](../../../theory/p09_agentic_rag/m28_retrieval_grading_rewriting/01_retriever_as_a_tool_grade_then_rewrite_in_langgraph/README.md#document-grader) · [Conditional edges](../../../theory/p09_agentic_rag/m28_retrieval_grading_rewriting/01_retriever_as_a_tool_grade_then_rewrite_in_langgraph/README.md#conditional-edges) · [Bounded retries](../../../theory/p09_agentic_rag/m28_retrieval_grading_rewriting/03_guardrails_query_optimisation_and_a_retry_loop/README.md#bounded-retries) · [Topic guardrails](../../../theory/p09_agentic_rag/m28_retrieval_grading_rewriting/03_guardrails_query_optimisation_and_a_retry_loop/README.md#topic-guardrails)

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
| `notebooks/01a_simple_agentic_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/01_retrieval_grading_and_query_rewriting/notebooks/01_simple_agentic_rag.ipynb` |
| `optional/02a_simple_agentic_rag_databricks.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/01_retrieval_grading_and_query_rewriting/notebooks/02_simple_agentic_rag_databricks.ipynb` |
| `notebooks/03a_advanced_rag_agent.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/01_retrieval_grading_and_query_rewriting/notebooks/03_advanced_rag_agent.ipynb` |
