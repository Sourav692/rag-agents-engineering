# Curriculum map

Module → notebook → the one thing it teaches. *(RAG Techniques anthology)* marks notebooks under the anthology's non-commercial licence ([third_party/RAG_Techniques_LICENSE.txt](third_party/RAG_Techniques_LICENSE.txt)).

## [01 Retrieval Grading and Query Rewriting](../modules/01_retrieval_grading_and_query_rewriting/README.md)

| Notebook | Learning objective |
|---|---|
| [01_simple_agentic_rag.ipynb](../modules/01_retrieval_grading_and_query_rewriting/notebooks/01_simple_agentic_rag.ipynb) | Wrap a retriever as a LangGraph tool, grade retrieved documents and rewrite the query |
| [02_simple_agentic_rag_databricks.ipynb](../modules/01_retrieval_grading_and_query_rewriting/notebooks/02_simple_agentic_rag_databricks.ipynb) | The same grading/rewriting agent over Databricks Vector Search (runs in a Databricks workspace) |
| [03_advanced_rag_agent.ipynb](../modules/01_retrieval_grading_and_query_rewriting/notebooks/03_advanced_rag_agent.ipynb) | Add topic guardrails, query optimisation, relevance assessment and a query-enhancement retry loop |

## [02 Corrective RAG (CRAG)](../modules/02_corrective_rag/README.md)

| Notebook | Learning objective |
|---|---|
| [01_agentic_corrective_rag_langgraph.ipynb](../modules/02_corrective_rag/notebooks/01_agentic_corrective_rag_langgraph.ipynb) | Build corrective RAG in LangGraph: grade documents, rewrite the query, fall back to Tavily web search |
| [02_crag_rag_techniques.ipynb](../modules/02_corrective_rag/notebooks/02_crag_rag_techniques.ipynb) | Corrective RAG with dynamic evaluation and web-search correction (RAG Techniques anthology) |

## [03 Self-RAG](../modules/03_self_rag/README.md)

| Notebook | Learning objective |
|---|---|
| [01_self_rag_langgraph.ipynb](../modules/03_self_rag/notebooks/01_self_rag_langgraph.ipynb) | Build Self-RAG in LangGraph: decide retrieval, grade relevance, groundedness and utility, retry |
| [02_self_rag_rag_techniques.ipynb](../modules/03_self_rag/notebooks/02_self_rag_rag_techniques.ipynb) | Self-RAG with retrieval decision, relevance, support and utility evaluation (RAG Techniques anthology) |

## [04 Adaptive RAG and Routing](../modules/04_adaptive_rag_and_routing/README.md)

| Notebook | Learning objective |
|---|---|
| [01_router_agentic_rag.ipynb](../modules/04_adaptive_rag_and_routing/notebooks/01_router_agentic_rag.ipynb) | Route customer-support queries to department knowledge bases with a LangGraph router agent |
| [02_router_agentic_rag_modular.ipynb](../modules/04_adaptive_rag_and_routing/notebooks/02_router_agentic_rag_modular.ipynb) | The same router agentic RAG system refactored into reusable modules |
| [03_healthcare_router_agentic_rag.ipynb](../modules/04_adaptive_rag_and_routing/notebooks/03_healthcare_router_agentic_rag.ipynb) | Categorise inquiries and sentiment, route to department RAG, escalate to a human (a separate source's take on 01) |
| [04_adaptive_rag_langgraph.ipynb](../modules/04_adaptive_rag_and_routing/notebooks/04_adaptive_rag_langgraph.ipynb) | Route each query to the vector store or web search up front, then grade documents and hallucinations |
| [05_adaptive_retrieval_rag_techniques.ipynb](../modules/04_adaptive_rag_and_routing/notebooks/05_adaptive_retrieval_rag_techniques.ipynb) | Pick a retrieval strategy per query type — factual, analytical, opinion, contextual (RAG Techniques anthology) |

## [05 RAG as an Agent Tool](../modules/05_rag_as_an_agent_tool/README.md)

| Notebook | Learning objective |
|---|---|
| [01_rag_as_tool_in_agents.ipynb](../modules/05_rag_as_an_agent_tool/notebooks/01_rag_as_tool_in_agents.ipynb) | Expose a RAG pipeline as a tool the agent chooses to call inside a LangGraph workflow |
| [02_agentic_rag_contextual_ai.ipynb](../modules/05_rag_as_an_agent_tool/notebooks/02_agentic_rag_contextual_ai.ipynb) | Build a managed RAG agent (datastore, parser, reranker, grounded LM) with the Contextual AI SDK (RAG Techniques anthology) |

## [06 Retrieval Feedback Loops and Reliability](../modules/06_retrieval_feedback_and_reliability/README.md)

| Notebook | Learning objective |
|---|---|
| [01_reliable_rag.ipynb](../modules/06_retrieval_feedback_and_reliability/notebooks/01_reliable_rag.ipynb) | Add document relevance checks, hallucination checks and source highlighting to RAG (RAG Techniques anthology) |
| [02_retrieval_with_feedback_loop.ipynb](../modules/06_retrieval_feedback_and_reliability/notebooks/02_retrieval_with_feedback_loop.ipynb) | Use user feedback to re-score documents and periodically refresh the index (RAG Techniques anthology) |
| [03_dartboard_rag.ipynb](../modules/06_retrieval_feedback_and_reliability/notebooks/03_dartboard_rag.ipynb) | Balance relevance and diversity when selecting retrieved passages — Dartboard RAG (RAG Techniques anthology) |

## [07 Hierarchical Retrieval with RAPTOR](../modules/07_hierarchical_retrieval_raptor/README.md)

| Notebook | Learning objective |
|---|---|
| [01_raptor.ipynb](../modules/07_hierarchical_retrieval_raptor/notebooks/01_raptor.ipynb) | Build a recursive tree of abstractive summaries and retrieve across its levels (RAG Techniques anthology) |

## [08 Memory-Augmented and Light RAG](../modules/08_memory_augmented_and_light_rag/README.md)

| Notebook | Learning objective |
|---|---|
| [01_memorag.ipynb](../modules/08_memory_augmented_and_light_rag/notebooks/01_memorag.ipynb) | Add a global memory model that drafts clues to guide retrieval over long documents (MemoRAG, RAG Techniques anthology) |
| [02_light_rag.ipynb](../modules/08_memory_augmented_and_light_rag/notebooks/02_light_rag.ipynb) | Index entities and relations in a lightweight graph with dual-level retrieval (LightRAG, RAG Techniques anthology) |

## [09 Knowledge Graphs with Neo4j](../modules/09_knowledge_graphs_with_neo4j/README.md)

| Notebook | Learning objective |
|---|---|
| [01_kg_simple.ipynb](../modules/09_knowledge_graphs_with_neo4j/notebooks/01_kg_simple.ipynb) | Create and query a first knowledge graph in Neo4j with Cypher |
| [02_healthcare_kg.ipynb](../modules/09_knowledge_graphs_with_neo4j/notebooks/02_healthcare_kg.ipynb) | Load a healthcare CSV into a Neo4j knowledge graph |
| [03_query_kg_with_langchain.ipynb](../modules/09_knowledge_graphs_with_neo4j/notebooks/03_query_kg_with_langchain.ipynb) | Query the healthcare graph in natural language through LangChain's Neo4j graph QA |
| [04_vector_indexing_and_embedding.ipynb](../modules/09_knowledge_graphs_with_neo4j/notebooks/04_vector_indexing_and_embedding.ipynb) | Add embeddings and a vector index to graph nodes for hybrid graph + vector retrieval |
| [05_roman_empire_graph_rag.ipynb](../modules/09_knowledge_graphs_with_neo4j/notebooks/05_roman_empire_graph_rag.ipynb) | Build end-to-end knowledge-graph RAG: LLM graph extraction, Neo4j storage, hybrid retrieval |
| [06_entity_relationship_extraction.ipynb](../modules/09_knowledge_graphs_with_neo4j/notebooks/06_entity_relationship_extraction.ipynb) | Extract entities and relationships from text with an LLM and visualise the graph |

## [10 GraphRAG Techniques](../modules/10_graphrag_techniques/README.md)

| Notebook | Learning objective |
|---|---|
| [01_graph_rag.ipynb](../modules/10_graphrag_techniques/notebooks/01_graph_rag.ipynb) | Build a concept graph over chunks and traverse it to answer questions (RAG Techniques anthology) |
| [02_graph_rag_local_attribution.ipynb](../modules/10_graphrag_techniques/notebooks/02_graph_rag_local_attribution.ipynb) | Local graph RAG with verifiable per-claim source attribution (RAG Techniques anthology) |
| [03_microsoft_graphrag.ipynb](../modules/10_graphrag_techniques/notebooks/03_microsoft_graphrag.ipynb) | Index a document with Microsoft GraphRAG and run global and local queries (RAG Techniques anthology) |
| [04_graphrag_with_milvus.ipynb](../modules/10_graphrag_techniques/notebooks/04_graphrag_with_milvus.ipynb) | Store entities, relations and passages in Milvus and expand retrieval through graph adjacency (RAG Techniques anthology) |

## [11 Agentic RAG Architectures](../modules/11_agentic_rag_architectures/README.md)

| Notebook | Learning objective |
|---|---|
| [01_rag_ecosystem.ipynb](../modules/11_agentic_rag_architectures/notebooks/01_rag_ecosystem.ipynb) | Walk the whole RAG stack end to end, from basic RAG through RAPTOR/ColBERT and agentic self-correction |

## [12 CacheRAG](../modules/12_cacherag/README.md)

🚧 Planned — no notebooks yet.
