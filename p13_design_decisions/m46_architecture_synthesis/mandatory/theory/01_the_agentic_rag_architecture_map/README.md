# M46.1 Theory: The agentic RAG architecture map

*[M46 theory](../README.md) · Lesson 46.1 · Notebooks: [`01a_AGENTIC_RAG_ARCHITECTURES.md`](../../notebook/01a_AGENTIC_RAG_ARCHITECTURES.md) · [All theory pages](../../../../../THEORY.md)*

## The architecture map

The course keeps two inventories of what it teaches. The wider one, [`docs/agentic-architectures.yaml`](../../../../../docs/agentic-architectures.yaml), rendered as [Agentic Architecture Coverage](../../../../../docs/agentic-architecture-coverage.md), compares the course with an upstream catalogue of 35 agentic architectures in seven families and finds all 35 covered. Five of them are retrieval architectures, and all five are on the mandatory track:

| # | Architecture | Taught in |
|---|---|---|
| 23 | Agentic RAG | [M28](../../../../../p08_agentic_rag/m28_retrieval_grading_rewriting/mandatory/theory/README.md), [M31](../../../../../p08_agentic_rag/m31_rag_as_agent_tool/mandatory/theory/README.md) |
| 24 | Corrective RAG (CRAG) | [M29](../../../../../p08_agentic_rag/m29_crag_and_self_rag/mandatory/theory/README.md) |
| 25 | Self-RAG | [M29](../../../../../p08_agentic_rag/m29_crag_and_self_rag/mandatory/theory/README.md) |
| 26 | Adaptive RAG | [M30](../../../../../p08_agentic_rag/m30_adaptive_rag_routing/mandatory/theory/README.md) |
| 27 | GraphRAG | [M43](../../../../../p12_knowledge_graphs_and_graph_rag/m43_knowledge_graphs_neo4j/mandatory/theory/README.md), [M44](../../../../../p12_knowledge_graphs_and_graph_rag/m44_graphrag/mandatory/theory/README.md) |

The lesson's reading, `01a_AGENTIC_RAG_ARCHITECTURES.md`, maps the retrieval side by graph shape rather than by folder. It names five architectures covered end to end (CRAG, Adaptive RAG, Self-RAG, domain-router RAG and retrieval as a tool) and writes each one as its `add_node` and `add_conditional_edges` structure, for example `retrieve → grade_documents → (rewrite_query ⟲ | web_search) → generate_answer` for CRAG. Its table has a sixth row, the M28 agent with query rewriting and guardrails, although the text above it says five notebooks. It lists RAPTOR and the GraphRAG notebooks as anthology variants, and one gap: CacheRAG exists in the source repository only as an empty placeholder.

Neither inventory says when to use what. For that, the architectures need a common unit. Every one of them is the M10 pipeline (retrieve, then generate) with components added, and each component is paid for in model calls per question. The course's labs have counted those calls on Larkspur questions:

![Model calls per question for each architecture, grouped by family, on a log scale from 1 to 20](diagrams/counted-calls.svg)

The ranges come from different questions and settings, so read them as orders of magnitude. Plain RAG is 1 call. Routing and tool loops cost 2 to 7. The self-correcting loops climb to 10 (M28's retry loop with two rewrites) and 20 (Self-RAG at `k = 5` on a question the handbook cannot answer, M29). Collapsed-tree RAPTOR and GraphRAG have no counted query cost; their main cost is LLM work at index time, which this axis does not show.

## What each family adds

The module objectives sort the architectures into five families. Each family adds a different kind of component to plain RAG, and each has a module whose theory page measures what that component buys.

- **Entry-level** changes nothing in the control flow and improves what reaches the model. Plain RAG and its baseline ([M10](../../../../../p04_rag_foundations/m10_rag_lifecycle/mandatory/theory/README.md)), indexing that searches small and returns large ([M15](../../../../../p04_rag_foundations/m15_advanced_indexing/mandatory/theory/README.md)), hybrid search ([M16](../../../../../p05_retrieval_quality_and_rag_apps/m16_retrievers_hybrid_search/mandatory/theory/README.md)), query transformation ([M17](../../../../../p05_retrieval_quality_and_rag_apps/m17_query_transformation/mandatory/theory/README.md)) and reranking ([M18](../../../../../p05_retrieval_quality_and_rag_apps/m18_reranking_post_retrieval/mandatory/theory/README.md)). Late interaction (lesson 46.2) belongs here too. Most add no model call; query rewriting adds one, decomposition four.
- **Self-correcting** puts a judgment between retrieval and the answer: grade, rewrite and retry ([M28](../../../../../p08_agentic_rag/m28_retrieval_grading_rewriting/mandatory/theory/README.md)), CRAG and Self-RAG ([M29](../../../../../p08_agentic_rag/m29_crag_and_self_rag/mandatory/theory/README.md)), graders and user feedback ([M32](../../../../../p08_agentic_rag/m32_reliability_feedback/mandatory/theory/README.md)). Each check is a model call, and each failed check sends the question round again.
- **Routing** decides where a question goes before anything is retrieved: a classifier over knowledge bases and adaptive RAG ([M30](../../../../../p08_agentic_rag/m30_adaptive_rag_routing/mandatory/theory/README.md)), then supervisors, hierarchies and swarms of specialist agents ([M35](../../../../../p10_multi_agent_systems/m35_multi_agent_architectures/mandatory/theory/README.md)). A misroute hides the answer, because the filter restricts retrieval to a knowledge base that does not hold it.
- **Tool-based** hands retrieval to a model that decides when to call it: ReAct ([M23](../../../../../p06_agent_foundations/m23_react_agents/mandatory/theory/README.md)), plan and execute ([M25](../../../../../p07_advanced_agents/m25_planning_reflection_reasoning/mandatory/theory/README.md)) and retrieval as a tool ([M31](../../../../../p08_agentic_rag/m31_rag_as_agent_tool/mandatory/theory/README.md)). The same tool can be served over MCP and called across agents over A2A ([M38](../../../../../p11_agent_protocols/m38_mcp_foundations/mandatory/theory/README.md) to [M41](../../../../../p11_agent_protocols/m41_a2a_protocol/mandatory/theory/README.md)) without changing the loop.
- **Structural** changes the shape of the index: summary trees ([M42](../../../../../p12_knowledge_graphs_and_graph_rag/m42_hierarchical_memory_rag/mandatory/theory/README.md)), knowledge graphs ([M43](../../../../../p12_knowledge_graphs_and_graph_rag/m43_knowledge_graphs_neo4j/mandatory/theory/README.md)) and community-based GraphRAG ([M44](../../../../../p12_knowledge_graphs_and_graph_rag/m44_graphrag/mandatory/theory/README.md)). The work moves to index time, and the index has to be rebuilt or patched when the handbook changes.

Memory ([M33](../../../../../p09_memory_layer/m33_short_term_memory_conversation_state/mandatory/theory/README.md), [M34](../../../../../p09_memory_layer/m34_long_term_agentic_memory/mandatory/theory/README.md)) cuts across all five. A follow-up such as *How long do I have?* needs rewriting into a standalone question before any of these architectures can retrieve for it.

The families also stack. The M28 agent is a tool-based loop with a self-correcting grader; adaptive RAG in M30 is a router in front of two graders. When a design names several families, count each component's calls separately, so a later review can remove one without guessing what it cost.

## Key Takeaways

- Every architecture is retrieve-then-generate with components added. Compare them in model calls per question: plain RAG is 1, routing and tool loops 2 to 7, self-correcting loops up to 20.
- Each family adds one kind of component: better context, a judgement step, routing, a model that calls retrieval, or a new index shape whose cost moves to index time.
- Families stack. Count each component's calls separately so a review can remove one and know what it saves.

## Check yourself

<details>
<summary>1. What common unit does the lesson use to compare the architectures, and what does that unit leave out?</summary>

Model calls per question, because every architecture is the M10 pipeline with components added: plain RAG is 1 call, routing and tool loops 2 to 7, and self-correcting loops climb to 10 and 20. It leaves out index-time LLM work, which is the main cost of collapsed-tree RAPTOR and GraphRAG, so those have no counted query cost on the axis.

</details>

<details>
<summary>2. The agentic RAG agent with query rewriting is a tool-based loop with a self-correcting grader. How should a design document count its cost?</summary>

Count each component's calls separately: the loop's calls and the grader's calls. A later review can then remove one component and know what it saves, instead of guessing from a single total.

</details>

<details>
<summary>3. A customer asks a follow-up, How long do I have?, and every architecture retrieves the wrong chunks. What is missing?</summary>

Memory (M33, M34), which cuts across all five families. The follow-up has to be rewritten into a standalone question using the conversation before any architecture can retrieve for it.

</details>

---
*Previous: [M46 overview](../README.md). Next: [46.2 End-to-end RAG ecosystem walkthrough (incl. ColBERT and RAGAS)](../02_end_to_end_rag_ecosystem_walkthrough_incl_colbert_and_ragas/README.md).*
