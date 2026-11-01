# M30 — Adaptive RAG & Query Routing

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part IX · Agentic & Self-Correcting RAG** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 3 mandatory, 2 optional

## Why it matters

Different questions need different paths: some need no retrieval, some need the web, some need a specific knowledge base. Routing up front saves cost and improves answers.

## Theory

Read the [theory page](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Routing confidence and the fallback](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/01_router_agentic_rag_over_multiple_knowledge_bases/interactive/kb-router-lab.html) (open the file in a browser)

## Learning objectives

- Route queries to department knowledge bases with a LangGraph router agent
- Refactor an agentic RAG system into reusable modules
- Add sentiment detection and escalation to a human
- Route between vector store and web search, then grade documents and hallucinations
- Pick a retrieval strategy per query type (factual, analytical, opinion, contextual)

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 30.1 | Router agentic RAG over multiple knowledge bases ([theory](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/01_router_agentic_rag_over_multiple_knowledge_bases/README.md)) | [`01a_router_agentic_rag.ipynb`](notebooks/01a_router_agentic_rag.ipynb) | [`01b_router_agentic_rag_modular.ipynb`](optional/01b_router_agentic_rag_modular.ipynb) *(extension)* |
| 30.2 | Customer-facing routing with sentiment and human escalation *(optional lesson)* ([theory](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/02_customer_facing_routing_with_sentiment_and_human_escalation/README.md)) | — | [`02a_healthcare_router_agentic_rag.ipynb`](optional/02a_healthcare_router_agentic_rag.ipynb) *(alternate)* |
| 30.3 | Adaptive RAG: vector store vs web, with hallucination grading ([theory](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/03_adaptive_rag_vector_store_vs_web_with_hallucination_grading/README.md)) | [`03a_adaptive_rag_langgraph.ipynb`](notebooks/03a_adaptive_rag_langgraph.ipynb) | — |
| 30.4 | Strategy per query type ([theory](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/04_strategy_per_query_type/README.md)) | [`04a_adaptive_retrieval_rag_techniques.ipynb`](notebooks/04a_adaptive_retrieval_rag_techniques.ipynb) | — |

## Hands-on lab

Support desk router: route billing, technical and general questions to separate knowledge bases, escalate negative-sentiment tickets, and report routing accuracy. Details: [lab/README.md](lab/README.md).

## Key concepts

[Query classification](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/01_router_agentic_rag_over_multiple_knowledge_bases/README.md#query-classification) · [Multi-KB routing](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/01_router_agentic_rag_over_multiple_knowledge_bases/README.md#multi-kb-routing) · [Human-in-the-loop escalation](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/02_customer_facing_routing_with_sentiment_and_human_escalation/README.md#human-in-the-loop-escalation) · [Per-query strategy](../../../theory/p09_agentic_rag/m30_adaptive_rag_routing/04_strategy_per_query_type/README.md#per-query-strategy)

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
| `notebooks/01a_router_agentic_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/04_adaptive_rag_and_routing/notebooks/01_router_agentic_rag.ipynb` |
| `optional/01b_router_agentic_rag_modular.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/04_adaptive_rag_and_routing/notebooks/02_router_agentic_rag_modular.ipynb` |
| `optional/02a_healthcare_router_agentic_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/04_adaptive_rag_and_routing/notebooks/03_healthcare_router_agentic_rag.ipynb` |
| `notebooks/03a_adaptive_rag_langgraph.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/04_adaptive_rag_and_routing/notebooks/04_adaptive_rag_langgraph.ipynb` |
| `notebooks/04a_adaptive_retrieval_rag_techniques.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/04_adaptive_rag_and_routing/notebooks/05_adaptive_retrieval_rag_techniques.ipynb` |
