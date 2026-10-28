# Agentic RAG Architectures Covered in This Repo

A map of every agentic-RAG architecture built in this repository, grouped by **architecture** rather than by folder. Five architectures are covered end-to-end — **CRAG, Adaptive RAG, Self-RAG, domain-router RAG, and retrieval-as-tool** — each with a LangGraph implementation plus an independent anthology implementation alongside it.

All links are repo-relative — click through from this file. Last surveyed: 2026-09-10 (links repointed at this repository's modules on 2026-09-29).

---

## 1. Core architectures — the LangGraph implementations

The canonical home. Five notebooks, each a distinct control-flow architecture. Graph shapes below are the actual `add_node` / `add_conditional_edges` structures in the notebooks.

| Architecture | Notebook | Graph shape |
|---|---|---|
| **Agentic RAG with query rewriting + guardrails** | [`03_advanced_rag_agent.ipynb`](../../../p09_agentic_rag/m28_retrieval_grading_rewriting/notebooks/03a_advanced_rag_agent.ipynb) | `validate_topic → optimize_query → fetch_content → assess_relevance → enhance_query ⟲ → generate_response`, with `handle_off_topic` / `handle_no_results` terminal branches |
| **Retrieval-as-a-tool (ReAct-style)** | [`01_rag_as_tool_in_agents.ipynb`](../../../p09_agentic_rag/m31_rag_as_agent_tool/notebooks/01a_rag_as_tool_in_agents.ipynb) | `topic_decision → agent ⇄ tools/retrieve → generate_answer`; the retriever is a tool the LLM *chooses* to call, not a fixed pipeline step |
| **Domain-router agentic RAG** | [`03_healthcare_router_agentic_rag.ipynb`](../../../p09_agentic_rag/m30_adaptive_rag_routing/optional/02a_healthcare_router_agentic_rag.ipynb) | `categorize_inquiry` + `analyze_inquiry_sentiment` → `generate_department_response`, with `escalate_to_human_agent` / `escalate_to_oncall_team` human-in-the-loop branches (data: [`healthcare_db.json`](../../../p09_agentic_rag/m30_adaptive_rag_routing/assets/healthcare_db.json)) |
| **Corrective RAG (CRAG)** | [`01_agentic_corrective_rag_langgraph.ipynb`](../../../p09_agentic_rag/m29_crag_and_self_rag/notebooks/01a_agentic_corrective_rag_langgraph.ipynb) | `retrieve → grade_documents → (rewrite_query ⟲ \| web_search) → generate_answer` — web search as the fallback corpus when retrieval grades poorly |
| **Adaptive RAG** | [`04_adaptive_rag_langgraph.ipynb`](../../../p09_agentic_rag/m30_adaptive_rag_routing/notebooks/03a_adaptive_rag_langgraph.ipynb) | Routes the query to `retrieve_vectordb` **or** `web_search` up front, then `grade_documents → generate_answer → grade_hallucinations`, with separate `rewrite_query_vectordb` / `rewrite_query_web_search` retry loops per source |
| **Self-RAG** | [`01_self_rag_langgraph.ipynb`](../../../p09_agentic_rag/m29_crag_and_self_rag/notebooks/02a_self_rag_langgraph.ipynb) | `decide_retrieval → retrieve → grade_relevance → generate → grade_groundedness → grade_utility`, plus a `rephrase_and_retry` loop — the full reflection-token triad (retrieve? / grounded? / useful?) |

Supporting material: [`data/sample/research_papers/`](../../../../data/sample/research_papers) (attention, chain-of-thought, diffusion, DINO, PEFT PDFs) used as the corpus.

---

## 2. Entry-level agentic RAG — [module 01](../../../p09_agentic_rag/m28_retrieval_grading_rewriting/README.md)

| Notebook | Content |
|---|---|
| [`01_simple_agentic_rag.ipynb`](../../../p09_agentic_rag/m28_retrieval_grading_rewriting/notebooks/01a_simple_agentic_rag.ipynb) | Minimal version — PDF → Chroma → agent loop |
| [`02_simple_agentic_rag_databricks.ipynb`](../../../p09_agentic_rag/m28_retrieval_grading_rewriting/optional/02a_simple_agentic_rag_databricks.ipynb) | Same agent on Databricks Vector Search |

---

## 3. Router mechanics — [module 04](../../../p09_agentic_rag/m30_adaptive_rag_routing/README.md)

| Notebook | Content |
|---|---|
| [`01_router_agentic_rag.ipynb`](../../../p09_agentic_rag/m30_adaptive_rag_routing/notebooks/01a_router_agentic_rag.ipynb) | Customer-support router agentic RAG |
| [`02_router_agentic_rag_modular.ipynb`](../../../p09_agentic_rag/m30_adaptive_rag_routing/optional/01b_router_agentic_rag_modular.ipynb) | Same system, refactored into modules |

These two notebooks used to sit with the LangGraph fundamentals as its routing demo; their main example is agentic RAG, so they live here. Graph routing mechanics themselves are taught in [repository 04 (LangGraph fundamentals)](https://github.com/Sourav692/ai-engineering-demystified-04-langgraph-fundamentals).

---

## 4. Anthology variants — RAG Techniques anthology notebooks

Independent implementations of the same architectures, useful as second opinions:

| Notebook | Note |
|---|---|
| [`02_agentic_rag_contextual_ai.ipynb`](../../../p09_agentic_rag/m31_rag_as_agent_tool/optional/02a_agentic_rag_contextual_ai.ipynb) | Managed-SDK flavour — parsing, reranking, grounded generation |
| [`02_crag_rag_techniques.ipynb`](../../../p09_agentic_rag/m29_crag_and_self_rag/optional/01b_crag_rag_techniques.ipynb) | Corrective RAG |
| [`02_self_rag_rag_techniques.ipynb`](../../../p09_agentic_rag/m29_crag_and_self_rag/optional/02b_self_rag_rag_techniques.ipynb) | Self-RAG |
| [`05_adaptive_retrieval_rag_techniques.ipynb`](../../../p09_agentic_rag/m30_adaptive_rag_routing/notebooks/04a_adaptive_retrieval_rag_techniques.ipynb) | Query-**type** strategy routing (factual / analytical / opinion) — distinct from CRAG's document-grading loop |
| [`02_retrieval_with_feedback_loop.ipynb`](../../../p09_agentic_rag/m32_reliability_feedback/notebooks/02a_retrieval_with_feedback_loop.ipynb) | Feedback-driven retrieval |
| [`01_raptor.ipynb`](../../../p12_hierarchical_and_graph_rag/m42_hierarchical_memory_rag/notebooks/01a_raptor.ipynb) | Recursive hierarchical summarization index |
| [`01_graph_rag.ipynb`](../../../p12_hierarchical_and_graph_rag/m44_graphrag/notebooks/01a_graph_rag.ipynb) · [`02_graph_rag_local_attribution.ipynb`](../../../p12_hierarchical_and_graph_rag/m44_graphrag/optional/02a_graph_rag_local_attribution.ipynb) · [`03_microsoft_graphrag.ipynb`](../../../p12_hierarchical_and_graph_rag/m44_graphrag/notebooks/03a_microsoft_graphrag.ipynb) · [`04_graphrag_with_milvus.ipynb`](../../../p12_hierarchical_and_graph_rag/m44_graphrag/optional/04a_graphrag_with_milvus.ipynb) | GraphRAG family |

---

## 5. Deployed / application forms

These live in later repositories and are named here for orientation only.

| Location | Content |
|---|---|
| `Building_Adaptive_RAG` — [repository 14 (projects)](https://github.com/Sourav692/ai-engineering-demystified-14-projects) | Adaptive RAG as a real Python app, not a notebook: `src/workflow/graph.py` + `nodes/` (`retrieve`, `grade_documents`, `generate`, `web_search`) + `chains/` (`router`, `retrieval_grader`, `hallucination_grader`, `answer_grader`). The cleanest reference for how the grader chains factor out of the graph. |
| `mcp_a2a_agentic_rag` — [repository 10 (agent protocols)](https://github.com/Sourav692/ai-engineering-demystified-10-agent-protocols) | Agentic RAG where retrieval tools are served over **MCP** and agents coordinate over **A2A** — `agents/`, `mcp/`, `mcp_config.json` |
| `ShopUNow_Agentic_RAG_Capstone` — [repository 14 (projects)](https://github.com/Sourav692/ai-engineering-demystified-14-projects) | Two-stage capstone: `01_create_vector_databases.ipynb` → `02_agentic_rag_system.ipynb` over 7 department JSON datasets |

---

## Gaps

- **CacheRAG** — [module 12](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag/tree/main/modules/12_cacherag/README.md) exists as a scaffolded placeholder with no content.
