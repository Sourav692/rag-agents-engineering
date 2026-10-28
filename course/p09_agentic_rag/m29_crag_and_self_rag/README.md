# M29 — Self-Correcting RAG: CRAG & Self-RAG

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part IX · Agentic & Self-Correcting RAG** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 2 mandatory, 2 optional

## Why it matters

Corrective RAG fixes bad retrieval; Self-RAG checks the answer. Together they are the classic patterns for reducing hallucination in production.

## Learning objectives

- Build CRAG: grade documents, rewrite the query, fall back to web search (Tavily)
- Build Self-RAG: decide whether to retrieve, then check relevance, groundedness and utility
- Compare CRAG and Self-RAG on accuracy, latency and LLM-call cost

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 29.1 | Corrective RAG in LangGraph with web-search fallback | [`01a_agentic_corrective_rag_langgraph.ipynb`](notebooks/01a_agentic_corrective_rag_langgraph.ipynb) | [`01b_crag_rag_techniques.ipynb`](optional/01b_crag_rag_techniques.ipynb) *(alternate)* |
| 29.2 | Self-RAG: retrieve-or-not, relevance, groundedness, utility | [`02a_self_rag_langgraph.ipynb`](notebooks/02a_self_rag_langgraph.ipynb) | [`02b_self_rag_rag_techniques.ipynb`](optional/02b_self_rag_rag_techniques.ipynb) *(alternate)* |
| 29.3 | Trade-offs: when correction is worth the extra calls | *Lecture / discussion* | — |

## Hands-on lab

Out-of-corpus stress test: send questions the corpus cannot answer and compare the baseline, CRAG and Self-RAG on refusals, web fallbacks and hallucinated answers. Details: [lab/README.md](lab/README.md).

## Key concepts

Retrieval evaluator · Knowledge refinement · Reflection tokens · Groundedness check

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
| `notebooks/01a_agentic_corrective_rag_langgraph.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/02_corrective_rag/notebooks/01_agentic_corrective_rag_langgraph.ipynb` |
| `optional/01b_crag_rag_techniques.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/02_corrective_rag/notebooks/02_crag_rag_techniques.ipynb` |
| `notebooks/02a_self_rag_langgraph.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/03_self_rag/notebooks/01_self_rag_langgraph.ipynb` |
| `optional/02b_self_rag_rag_techniques.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/03_self_rag/notebooks/02_self_rag_rag_techniques.ipynb` |
