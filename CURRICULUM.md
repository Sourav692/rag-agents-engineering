# RAG & Agents Engineering Curriculum

*From your first retriever to agentic, memory-backed, multi-agent and graph-based RAG*

Built from 4 repositories. Every notebook in them is mapped to exactly one lesson below.

| Repo | Topic | Notebooks |
|---|---|---|
| [`ai-engineering-demystified-05-retrieval-rag`](https://github.com/Sourav692/ai-engineering-demystified-05-retrieval-rag) | Retrieval & RAG | 102 |
| [`ai-engineering-demystified-06-agent-fundamentals`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals) | Agent fundamentals | 64 |
| [`ai-engineering-demystified-08-advanced-agent-systems`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems) | Advanced agent systems | 53 |
| [`ai-engineering-demystified-09-advanced-rag`](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag) | Advanced RAG | 32 |

## Course at a glance

| Parts | Modules | Lessons | Notebooks mapped | Mandatory | Optional | Suggested effort | Pace |
|---|---|---|---|---|---|---|---|
| 9 | 31 + capstone | 150 | 251 | 145 | 106 | ~161 hours | 17 weeks at ~9 h/week |

## Who this course is for

- Software and ML engineers who build LLM applications and need retrieval that actually works
- Data engineers moving into AI engineering who already know Python and SQL
- Practitioners who have built a demo RAG app and want to understand why it fails and how to fix it

## Prerequisites

- Python 3.12, Jupyter notebooks, `.env` files and calling an LLM provider API
- Prompt writing and structured output
- LangChain basics: models, messages, prompt templates, output parsers and LCEL `|` composition
- LangGraph basics (state, nodes, conditional edges, checkpointers) before Part V; tool calling and the agent loop are taught in Part V

## Learning outcomes

By the end of the course you can:

1. Explain the RAG lifecycle and build a measured baseline before optimising anything
2. Engineer the ingestion pipeline: loaders, metadata, chunking, embeddings and vector stores
3. Change what gets indexed (parent-document, multi-representation, HyPE, contextual headers, hierarchical)
4. Improve retrieval quality with hybrid search, fusion, query transformation and reranking
5. Ship complete RAG apps with sources, citations, structured data and images
6. Write the agent loop by hand, build ReAct agents, and apply the five workflow patterns plus planning and reflection
7. Build self-correcting RAG (grading, CRAG, Self-RAG, adaptive routing) as LangGraph graphs
8. Expose retrieval as an agent tool and make it reliable with checks and feedback loops
9. Add conversation, long-term and agentic memory, and coordinate retrieval across supervisor, swarm and research multi-agent systems
10. Build knowledge graphs in Neo4j and apply RAPTOR, LightRAG and GraphRAG
11. Pick an architecture for a given problem and defend the trade-offs

## How to read this syllabus

- **Levels:** Foundation → Core → Advanced → Expert.
- **Notebooks:** every lesson lists its notebooks as `repo/module/notebook`, split into **Mandatory** and **Optional** columns (see below).
- **Baseline-first:** the Module 1 lab produces a baseline. Every later lab reports its change against it on the same golden question set.
- **Hours** are suggested study time for the mandatory notebooks plus the lab. Optional notebooks are extra.

## Mandatory vs optional notebooks

You do not need every notebook. **145 of 251 notebooks are mandatory**; the other 106 are optional.

**Rule:** each lesson keeps the one notebook (two, when they teach two distinct ideas) that you need for the lesson objective and the module lab. Everything else is optional for one of three reasons:

| Optional reason | Meaning | Notebooks |
|---|---|---|
| **Alternate** | Same idea taught again from another source course, or the same pattern in another API (e.g. LCEL instead of LangGraph) | 30 |
| **Platform-specific** | Needs a particular vendor or extra infrastructure: Databricks, Astra DB, Postgres, Milvus, Contextual AI, ColPali GPU stack | 8 |
| **Extension** | Extra applied example, reference material or a niche variant; useful practice, not needed for the lab | 68 |

If a lesson has no mandatory notebook, the whole lesson is optional.

## Course map

```mermaid
flowchart LR
  subgraph OFF[Offline: indexing]
    L[Load<br/>M2] --> C[Chunk<br/>M3] --> E[Embed<br/>M4 · M11] --> S[Store / Index<br/>M5–M6]
  end
  subgraph ON[Online: answering]
    Q[User query] --> T[Transform query<br/>M8] --> R[Retrieve<br/>M7 · M12] --> P[Rerank & compress<br/>M9] --> G[Generate & cite<br/>M10]
  end
  S --> R
  A{{Agents: plan · grade · route<br/>M13–M22 · M31}} -.retry / rewrite.-> T
  M[(Memory & multi-agent<br/>M23–M27)] -.history / shared state.-> A
  G -.check.-> A
  K[(Trees & graphs<br/>M28–M30)] --> R
```

## Roadmap

| Part | Title | When | Level | Modules |
|---|---|---|---|---|
| I | RAG Foundations | Week 1 | Foundation | M1 |
| II | The Ingestion & Indexing Pipeline | Weeks 2–3 | Core | M2, M3, M4, M5, M6 |
| III | Retrieval Quality Engineering | Weeks 4–5 | Core | M7, M8, M9 |
| IV | Building Complete RAG Applications | Week 6 | Core | M10, M11, M12 |
| V | Agent Foundations for RAG | Weeks 7–9 | Core | M13, M14, M15, M16, M17 |
| VI | Agentic & Self-Correcting RAG | Weeks 10–11 | Advanced | M18, M19, M20, M21, M22 |
| VII | Memory & Multi-Agent RAG | Weeks 12–13 | Advanced | M23, M24, M25, M26, M27 |
| VIII | Hierarchical, Memory & Graph RAG | Weeks 14–15 | Expert | M28, M29, M30 |
| IX | Architecture Synthesis & Capstone | Weeks 16–17 | Expert | M31, Capstone |

---

## Part I — RAG Foundations

**Week 1 · Foundation** — Why retrieval exists, the four stages of a pipeline, and a baseline you will measure every later change against.

### Module 1 — Why RAG & the RAG Lifecycle

**Level:** Foundation · **Time:** ~4 h · **Notebooks:** 4 mandatory, 0 optional · **Source:** `05/01_introduction_to_rag`

**Why it matters.** Before tuning anything you need a working pipeline and a number to beat. This module builds both, first by hand and then with LangChain.

**Learning objectives**

- Explain the knowledge problem RAG solves: stale training data, private data, hallucination, and context-window limits
- Compare RAG with fine-tuning and with simply using a long context window
- Build an index from scratch so 'indexing' and 'nearest neighbour' are concrete
- Run the full lifecycle (load → split → embed → store → retrieve → generate) and record baseline metrics

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 1.1 | The knowledge problem: hallucination, freshness, context-window growth, RAG vs fine-tuning vs long context | *Lecture / discussion* | — |
| 1.2 | Indexing from scratch with TF-IDF and nearest neighbours | [`02a_indexing_from_scratch`](course/p1_rag_foundations/m01_rag_lifecycle/notebooks/02a_indexing_from_scratch.ipynb) | — |
| 1.3 | Semantic retrieval with embedding similarity | [`03a_retrieval_strategies`](course/p1_rag_foundations/m01_rag_lifecycle/notebooks/03a_retrieval_strategies.ipynb) | — |
| 1.4 | Your first LangChain RAG with Chroma | [`04a_langchain_rag_quickstart`](course/p1_rag_foundations/m01_rag_lifecycle/notebooks/04a_langchain_rag_quickstart.ipynb) | — |
| 1.5 | The RAG lifecycle and a measured baseline | [`05a_rag_lifecycle_and_baseline`](course/p1_rag_foundations/m01_rag_lifecycle/notebooks/05a_rag_lifecycle_and_baseline.ipynb) | — |

**Hands-on lab.** Baseline pipeline: build the canonical lifecycle notebook end to end on the course corpus and save its retrieval and answer metrics. Every later module reports its improvement against this baseline.

**Key concepts:** Parametric vs non-parametric knowledge · Indexing vs retrieval vs generation · Top-k · Baseline-first optimisation

**Part I checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).

---

## Part II — The Ingestion & Indexing Pipeline

**Weeks 2–3 · Core** — Everything that happens before a query arrives: loading, metadata, chunking, embedding, storing, and deciding what to index.

### Module 2 — Document Ingestion & Metadata Design

**Level:** Core · **Time:** ~5 h · **Notebooks:** 4 mandatory, 9 optional · **Source:** `05/02_document_loading`

**Why it matters.** Retrieval can only be as good as the text and metadata you extract. Bad parsing and missing metadata are the most common root cause of weak RAG.

**Learning objectives**

- Load text, Markdown, CSV, JSON, PDF, Word, web pages, transcripts and papers into `Document` objects
- Choose a PDF parser by comparing PyPDF, PyMuPDF and Unstructured element-level output
- Design a metadata schema that filtering, citation and access control will rely on later
- Write a custom loader with `BaseLoader.lazy_load` for a source no library covers

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 2.1 | The Document abstraction and metadata design | [`01a_document_loading_and_metadata`](course/p2_ingestion_and_indexing/m02_document_ingestion/notebooks/01a_document_loading_and_metadata.ipynb) | [`01b_document_loaders_overview`](course/p2_ingestion_and_indexing/m02_document_ingestion/optional/01b_document_loaders_overview.ipynb) *(alternate)* |
| 2.2 | Plain text and Markdown (single vs element mode) *(optional lesson)* | — | [`02a_text_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/optional/02a_text_loader.ipynb) *(extension)*<br>[`02b_markdown_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/optional/02b_markdown_loader.ipynb) *(extension)* |
| 2.3 | Semi-structured sources: CSV rows and JSON / JSONL with jq schemas *(optional lesson)* | — | [`03a_csv_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/optional/03a_csv_loader.ipynb) *(extension)*<br>[`03b_json_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/optional/03b_json_loader.ipynb) *(extension)* |
| 2.4 | PDF and Word: parser comparison and element-level parsing | [`04a_pdf_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/notebooks/04a_pdf_loader.ipynb) | [`04b_ms_word_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/optional/04b_ms_word_loader.ipynb) *(extension)* |
| 2.5 | Web, YouTube and arXiv sources; bulk directory loading | [`05a_url_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/notebooks/05a_url_loader.ipynb) | [`05b_youtube_transcript_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/optional/05b_youtube_transcript_loader.ipynb) *(extension)*<br>[`05c_research_paper_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/optional/05c_research_paper_loader.ipynb) *(extension)*<br>[`05d_directory_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/optional/05d_directory_loader.ipynb) *(extension)* |
| 2.6 | Custom loaders with lazy loading | [`06a_custom_loader`](course/p2_ingestion_and_indexing/m02_document_ingestion/notebooks/06a_custom_loader.ipynb) | — |

**Hands-on lab.** Multi-source ingestor: load a mixed folder (PDF, DOCX, Markdown, CSV, one web page) into Documents that share one metadata schema (source, type, section, page, date).

**Key concepts:** Loader vs parser · Element-level parsing · Metadata schema · Lazy loading

### Module 3 — Chunking Strategies

**Level:** Core · **Time:** ~6 h · **Notebooks:** 4 mandatory, 6 optional · **Source:** `05/03_chunking`

**Why it matters.** The chunk is the unit of retrieval. Its size and boundaries decide what the retriever can find and how much noise reaches the model.

**Learning objectives**

- Apply character, recursive, token and structure-aware (Markdown, HTML, code) splitters
- Chunk on meaning with embedding-distance breakpoints (semantic chunking)
- Turn text into atomic, self-contained propositions and index those
- Pick chunk size and overlap by measurement instead of by habit

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 3.1 | Splitter fundamentals: character, recursive, token and structure-aware | [`01a_document_splitting_and_chunking`](course/p2_ingestion_and_indexing/m03_chunking/notebooks/01a_document_splitting_and_chunking.ipynb) | [`01b_document_splitters_and_chunkers`](course/p2_ingestion_and_indexing/m03_chunking/optional/01b_document_splitters_and_chunkers.ipynb) *(alternate)*<br>[`01c_text_splitters_and_chunking_strategies`](course/p2_ingestion_and_indexing/m03_chunking/optional/01c_text_splitters_and_chunking_strategies.ipynb) *(alternate)* |
| 3.2 | Semantic chunking: breakpoints on embedding distance | [`02a_semantic_chunking`](course/p2_ingestion_and_indexing/m03_chunking/notebooks/02a_semantic_chunking.ipynb) | [`02b_semantic_chunking_walkthrough`](course/p2_ingestion_and_indexing/m03_chunking/optional/02b_semantic_chunking_walkthrough.ipynb) *(alternate)*<br>[`02c_semantic_chunking_rag_techniques`](course/p2_ingestion_and_indexing/m03_chunking/optional/02c_semantic_chunking_rag_techniques.ipynb) *(alternate)* |
| 3.3 | Proposition chunking with LLM quality checks | [`03a_proposition_chunking`](course/p2_ingestion_and_indexing/m03_chunking/notebooks/03a_proposition_chunking.ipynb) | [`03b_proposition_chunking_rag_techniques`](course/p2_ingestion_and_indexing/m03_chunking/optional/03b_proposition_chunking_rag_techniques.ipynb) *(alternate)* |
| 3.4 | Choosing chunk size empirically: retrieval quality, faithfulness, latency | [`04a_choosing_chunk_size`](course/p2_ingestion_and_indexing/m03_chunking/notebooks/04a_choosing_chunk_size.ipynb) | [`04b_choose_chunk_size_llamaindex`](course/p2_ingestion_and_indexing/m03_chunking/optional/04b_choose_chunk_size_llamaindex.ipynb) *(alternate)* |

**Hands-on lab.** Chunking bake-off: index the same corpus with recursive, semantic and proposition chunking at three sizes each, and compare hit rate and answer faithfulness against the Module 1 baseline.

**Key concepts:** Chunk size and overlap · Breakpoint threshold · Propositions · Structure-aware splitting

### Module 4 — Embeddings & Model Selection

**Level:** Core · **Time:** ~4 h · **Notebooks:** 4 mandatory, 4 optional · **Source:** `05/04_embeddings`

**Why it matters.** The embedding model defines what 'similar' means for your corpus. Choosing one is a measurable decision that trades quality, cost, latency and data residency.

**Learning objectives**

- Explain dense embeddings, dimensions and cosine / dot-product / Euclidean similarity
- Generate embeddings with OpenAI and open-source Hugging Face / sentence-transformers models
- Batch and cache embeddings with `CacheBackedEmbeddings` to cut cost and re-index time
- Benchmark candidate models on your own data and track runs with MLflow

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 4.1 | Embedding fundamentals, similarity metrics and model selection | [`01a_embeddings_and_model_selection`](course/p2_ingestion_and_indexing/m04_embeddings/notebooks/01a_embeddings_and_model_selection.ipynb) | — |
| 4.2 | Hosted embeddings: OpenAI models and dimensions | [`02a_openai_embeddings`](course/p2_ingestion_and_indexing/m04_embeddings/notebooks/02a_openai_embeddings.ipynb) | [`02b_openai_embeddings_tutorial`](course/p2_ingestion_and_indexing/m04_embeddings/optional/02b_openai_embeddings_tutorial.ipynb) *(alternate)* |
| 4.3 | Open-source embeddings with Hugging Face | [`03a_huggingface_embeddings`](course/p2_ingestion_and_indexing/m04_embeddings/notebooks/03a_huggingface_embeddings.ipynb) | [`03b_huggingface_embeddings_tutorial`](course/p2_ingestion_and_indexing/m04_embeddings/optional/03b_huggingface_embeddings_tutorial.ipynb) *(alternate)*<br>[`03c_embedding_models`](course/p2_ingestion_and_indexing/m04_embeddings/optional/03c_embedding_models.ipynb) *(alternate)* |
| 4.4 | Production concerns: batching, caching and similarity behaviour | [`04a_embeddings_deep_dive`](course/p2_ingestion_and_indexing/m04_embeddings/notebooks/04a_embeddings_deep_dive.ipynb) | — |
| 4.5 | Benchmarking embedding models with MLflow (Databricks) *(optional lesson)* | — | [`05a_compare_embedding_models_databricks`](course/p2_ingestion_and_indexing/m04_embeddings/optional/05a_compare_embedding_models_databricks.ipynb) *(platform-specific)* |

**Hands-on lab.** Embedding shoot-out: compare one hosted and two open-source models on a 30-question golden set and pick one, writing down the cost and latency per 1,000 chunks.

**Key concepts:** Vector dimensionality · Cosine similarity · Embedding cache · Domain fit

### Module 5 — Vector Stores & Index Operations

**Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 4 optional · **Source:** `05/05_vector_stores`, `05/12_langchain_rag_implementations`

**Why it matters.** A vector store is a database. You need to create, update, delete, persist and filter, and keep it in sync with sources that change.

**Learning objectives**

- Run CRUD and persistence operations through LangChain's common vector store interface
- Use embedded stores (Chroma, FAISS) and managed stores (Astra DB, Pinecone), and know when to pick each
- Combine semantic search with metadata filters on Postgres + pgvector
- Keep an index in sync with its sources using the Indexing API and a record manager

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 5.1 | Index operations: create, query, update, delete, persist | [`01a_vector_stores_and_index_operations`](course/p2_ingestion_and_indexing/m05_vector_stores/notebooks/01a_vector_stores_and_index_operations.ipynb) | [`01b_vector_database_operations`](course/p2_ingestion_and_indexing/m05_vector_stores/optional/01b_vector_database_operations.ipynb) *(alternate)*<br>[`01c_other_vector_stores`](course/p2_ingestion_and_indexing/m05_vector_stores/optional/01c_other_vector_stores.ipynb) *(extension)* |
| 5.2 | Embedded stores: Chroma and FAISS | [`02a_chromadb`](course/p2_ingestion_and_indexing/m05_vector_stores/notebooks/02a_chromadb.ipynb)<br>[`02b_faiss`](course/p2_ingestion_and_indexing/m05_vector_stores/notebooks/02b_faiss.ipynb) | [`02c_vector_stores_in_practice`](course/p2_ingestion_and_indexing/m05_vector_stores/optional/02c_vector_stores_in_practice.ipynb) *(alternate)* |
| 5.3 | Managed stores: Astra DB and Pinecone | [`03b_pinecone`](course/p2_ingestion_and_indexing/m05_vector_stores/notebooks/03b_pinecone.ipynb) | [`03a_astra_db`](course/p2_ingestion_and_indexing/m05_vector_stores/optional/03a_astra_db.ipynb) *(platform-specific)* |
| 5.4 | Postgres + pgvector with metadata-filtered search | [`04a_filtered_search_pgvector`](course/p2_ingestion_and_indexing/m05_vector_stores/notebooks/04a_filtered_search_pgvector.ipynb) | — |
| 5.5 | Incremental indexing: Indexing API and record manager | [`05a_indexing_api`](course/p2_ingestion_and_indexing/m05_vector_stores/notebooks/05a_indexing_api.ipynb) | — |

**Hands-on lab.** Living index: stand up pgvector with Docker, ingest the Module 2 corpus, then change, add and delete source files and show that the record manager re-indexes only what changed.

**Key concepts:** ANN search · Collections and namespaces · Metadata filters · Idempotent re-indexing

### Module 6 — Advanced Indexing Strategies

**Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 2 optional · **Source:** `05/06_indexing_strategies`, `05/10_building_rag_systems`

**Why it matters.** What you embed does not have to be what you return. Decoupling the search key from the payload fixes many precision and context problems.

**Learning objectives**

- Embed summaries but return full documents (multi-representation / multi-vector indexing)
- Embed small child chunks but return their parent (parent-document retrieval), with a persistent docstore
- Build two-tier hierarchical indices and search top-down
- Generate hypothetical questions at index time (HyPE, document augmentation)
- Prepend document context to chunks before embedding (contextual chunk headers, contextual retrieval)

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 6.1 | Multi-representation indexing: search summaries, return documents | [`01a_multi_representation_indexing`](course/p2_ingestion_and_indexing/m06_advanced_indexing/notebooks/01a_multi_representation_indexing.ipynb) | — |
| 6.2 | Parent-document retrieval, in memory and on Postgres | [`02a_parent_document_retrieval`](course/p2_ingestion_and_indexing/m06_advanced_indexing/notebooks/02a_parent_document_retrieval.ipynb) | [`02b_parent_document_retriever_postgres`](course/p2_ingestion_and_indexing/m06_advanced_indexing/optional/02b_parent_document_retriever_postgres.ipynb) *(platform-specific)* |
| 6.3 | Hierarchical indices: summary tier and detail tier | [`03a_hierarchical_indices`](course/p2_ingestion_and_indexing/m06_advanced_indexing/notebooks/03a_hierarchical_indices.ipynb) | — |
| 6.4 | Question-side indexing: HyPE and document augmentation | [`04a_hypothetical_prompt_embeddings`](course/p2_ingestion_and_indexing/m06_advanced_indexing/notebooks/04a_hypothetical_prompt_embeddings.ipynb) | [`04b_document_augmentation`](course/p2_ingestion_and_indexing/m06_advanced_indexing/optional/04b_document_augmentation.ipynb) *(alternate)* |
| 6.5 | Context-aware chunks: contextual headers and contextual retrieval | [`05a_contextual_chunk_headers`](course/p2_ingestion_and_indexing/m06_advanced_indexing/notebooks/05a_contextual_chunk_headers.ipynb)<br>[`05b_contextual_retrieval_rag_system`](course/p2_ingestion_and_indexing/m06_advanced_indexing/notebooks/05b_contextual_retrieval_rag_system.ipynb) | — |

**Hands-on lab.** Index redesign: apply parent-document retrieval and contextual chunk headers to the baseline and report the change in hit rate and answer quality.

**Key concepts:** Search key vs payload · Docstore · HyPE · Contextual retrieval

**Part II checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).

---

## Part III — Retrieval Quality Engineering

**Weeks 4–5 · Core** — Getting the right chunks into the top-k: hybrid search, fusion, query transformation, routing and reranking.

### Module 7 — Retrievers & Hybrid Search

**Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 2 optional · **Source:** `05/07_retrievers_and_hybrid_search`

**Why it matters.** Dense vectors miss exact terms such as IDs, names and codes; keyword search misses paraphrase. Production retrieval usually combines both.

**Learning objectives**

- Use the retriever interface: similarity, score threshold, MMR, multi-query, compression, ensemble
- Combine dense and sparse (BM25) retrieval and build a RAG chain on top
- Fuse rankings with normalised scores and with Reciprocal Rank Fusion
- Trade relevance against diversity with Maximal Marginal Relevance
- Filter by metadata, similarity threshold, keywords and diversity together

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 7.1 | The retriever interface and its search modes | [`01a_retrievers`](course/p3_retrieval_quality/m07_retrievers_hybrid_search/notebooks/01a_retrievers.ipynb) | — |
| 7.2 | Dense + sparse hybrid retrieval with BM25 and EnsembleRetriever | [`02a_dense_sparse_hybrid_retrieval`](course/p3_retrieval_quality/m07_retrievers_hybrid_search/notebooks/02a_dense_sparse_hybrid_retrieval.ipynb) | [`02b_hybrid_search_rag`](course/p3_retrieval_quality/m07_retrievers_hybrid_search/optional/02b_hybrid_search_rag.ipynb) *(extension)* |
| 7.3 | Fusion retrieval: score normalisation vs rank fusion | [`03a_fusion_retrieval`](course/p3_retrieval_quality/m07_retrievers_hybrid_search/notebooks/03a_fusion_retrieval.ipynb) | — |
| 7.4 | Maximal Marginal Relevance for diversity | [`04a_maximal_marginal_relevance`](course/p3_retrieval_quality/m07_retrievers_hybrid_search/notebooks/04a_maximal_marginal_relevance.ipynb) | — |
| 7.5 | Multi-faceted filtering | [`05a_multi_faceted_filtering`](course/p3_retrieval_quality/m07_retrievers_hybrid_search/notebooks/05a_multi_faceted_filtering.ipynb) | — |
| 7.6 | Retriever patterns compared; hybrid + rerank on Databricks Vector Search | [`06a_advanced_retriever_patterns`](course/p3_retrieval_quality/m07_retrievers_hybrid_search/notebooks/06a_advanced_retriever_patterns.ipynb) | [`06b_hybrid_search_and_reranking_databricks`](course/p3_retrieval_quality/m07_retrievers_hybrid_search/optional/06b_hybrid_search_and_reranking_databricks.ipynb) *(platform-specific)* |

**Hands-on lab.** Hybrid upgrade: add BM25 to the vector retriever, tune the fusion weights on the golden set, and find three queries that only hybrid search answers.

**Key concepts:** Dense vs sparse · BM25 · Reciprocal Rank Fusion · MMR λ

### Module 8 — Query Transformation & Routing

**Level:** Core · **Time:** ~7 h · **Notebooks:** 9 mandatory, 6 optional · **Source:** `05/08_query_transformation`

**Why it matters.** Users write short, vague or compound questions. Rewriting the query before retrieval is often the cheapest large gain available.

**Learning objectives**

- Rewrite and expand queries with an LLM
- Generate multiple query variants and merge their results (multi-query, RAG-Fusion)
- Retrieve with a more general question (step-back) or a hypothetical answer (HyDE)
- Decompose multi-hop questions into sub-questions
- Route queries with an LLM classifier or by semantic similarity, and turn questions into metadata filters (self-query)

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 8.1 | Query rewriting and expansion | [`01a_query_expansion`](course/p3_retrieval_quality/m08_query_transformation/notebooks/01a_query_expansion.ipynb) | [`01b_query_transformations_rag_techniques`](course/p3_retrieval_quality/m08_query_transformation/optional/01b_query_transformations_rag_techniques.ipynb) *(alternate)* |
| 8.2 | Multi-query retrieval | [`02a_multi_query_retrieval`](course/p3_retrieval_quality/m08_query_transformation/notebooks/02a_multi_query_retrieval.ipynb) | [`02b_multiquery_retrieval_walkthrough`](course/p3_retrieval_quality/m08_query_transformation/optional/02b_multiquery_retrieval_walkthrough.ipynb) *(alternate)*<br>[`02c_better_queries`](course/p3_retrieval_quality/m08_query_transformation/optional/02c_better_queries.ipynb) *(alternate)* |
| 8.3 | RAG-Fusion with Reciprocal Rank Fusion | [`03a_rag_fusion`](course/p3_retrieval_quality/m08_query_transformation/notebooks/03a_rag_fusion.ipynb) | — |
| 8.4 | Step-back prompting | [`04a_step_back_prompting`](course/p3_retrieval_quality/m08_query_transformation/notebooks/04a_step_back_prompting.ipynb) | — |
| 8.5 | HyDE: embed a hypothetical answer | [`05a_hyde`](course/p3_retrieval_quality/m08_query_transformation/notebooks/05a_hyde.ipynb) | [`05b_hyde_walkthrough`](course/p3_retrieval_quality/m08_query_transformation/optional/05b_hyde_walkthrough.ipynb) *(alternate)*<br>[`05c_hyde_rag_techniques`](course/p3_retrieval_quality/m08_query_transformation/optional/05c_hyde_rag_techniques.ipynb) *(alternate)* |
| 8.6 | Query decomposition for multi-hop questions | [`06a_query_decomposition`](course/p3_retrieval_quality/m08_query_transformation/notebooks/06a_query_decomposition.ipynb) | [`06b_query_decomposition_walkthrough`](course/p3_retrieval_quality/m08_query_transformation/optional/06b_query_decomposition_walkthrough.ipynb) *(alternate)* |
| 8.7 | Routing: LLM classifier and semantic routing | [`07a_routing_with_llm_classifier`](course/p3_retrieval_quality/m08_query_transformation/notebooks/07a_routing_with_llm_classifier.ipynb)<br>[`07b_semantic_routing`](course/p3_retrieval_quality/m08_query_transformation/notebooks/07b_semantic_routing.ipynb) | — |
| 8.8 | Self-querying: natural language to metadata filter | [`08a_self_querying_retrieval`](course/p3_retrieval_quality/m08_query_transformation/notebooks/08a_self_querying_retrieval.ipynb) | — |

**Hands-on lab.** Query-transformation matrix: run multi-query, RAG-Fusion, HyDE and decomposition on the same 30 questions and record which question types each one helps, which it hurts, and the added latency and cost.

**Key concepts:** Query–document asymmetry · RRF · HyDE · Logical vs semantic routing

### Module 9 — Post-Retrieval Optimisation & Reranking

**Level:** Core · **Time:** ~4 h · **Notebooks:** 5 mandatory, 2 optional · **Source:** `05/09_post_retrieval_and_reranking`

**Why it matters.** Bi-encoders are fast but coarse. Retrieving wide and then reranking, compressing or expanding the context gives precision without losing recall.

**Learning objectives**

- Design two-stage retrieval: high-recall first stage, precise second stage
- Rerank with cross-encoders and with LLMs and compare cost and quality
- Compress chunks to only the query-relevant sentences
- Restore surrounding context with enrichment windows and relevant segment extraction

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 9.1 | Two-stage retrieval: retrieve wide, rerank narrow | [`01a_two_stage_reranking`](course/p3_retrieval_quality/m09_reranking_post_retrieval/notebooks/01a_two_stage_reranking.ipynb) | — |
| 9.2 | Cross-encoder reranking in a RAG chain | [`02a_cross_encoder_reranking`](course/p3_retrieval_quality/m09_reranking_post_retrieval/notebooks/02a_cross_encoder_reranking.ipynb) | [`02b_reranking_cross_encoder_walkthrough`](course/p3_retrieval_quality/m09_reranking_post_retrieval/optional/02b_reranking_cross_encoder_walkthrough.ipynb) *(alternate)* |
| 9.3 | LLM reranking vs cross-encoder reranking | [`03a_reranking_methods`](course/p3_retrieval_quality/m09_reranking_post_retrieval/notebooks/03a_reranking_methods.ipynb) | — |
| 9.4 | Contextual compression | [`04a_contextual_compression`](course/p3_retrieval_quality/m09_reranking_post_retrieval/notebooks/04a_contextual_compression.ipynb) | — |
| 9.5 | Context enrichment windows | [`05a_context_enrichment_window`](course/p3_retrieval_quality/m09_reranking_post_retrieval/notebooks/05a_context_enrichment_window.ipynb) | — |
| 9.6 | Relevant segment extraction *(optional lesson)* | — | [`06a_relevant_segment_extraction`](course/p3_retrieval_quality/m09_reranking_post_retrieval/optional/06a_relevant_segment_extraction.ipynb) *(extension)* |

**Hands-on lab.** Precision stack: add a cross-encoder reranker over a top-50 hybrid retrieval and measure the gain at top-5, plus the latency budget it consumes.

**Key concepts:** Bi-encoder vs cross-encoder · Recall@50 → precision@5 · Lost in the middle · Context budget

**Part III checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).

---

## Part IV — Building Complete RAG Applications

**Week 6 · Core** — Assembling full systems with sources, citations, structured data and images, in LangChain and LlamaIndex.

### Module 10 — End-to-End RAG Systems

**Level:** Core · **Time:** ~7 h · **Notebooks:** 8 mandatory, 3 optional · **Source:** `05/10_building_rag_systems`

**Why it matters.** Users trust answers they can check. This module turns pipelines into systems that cite sources, explain retrieval and handle tables and JSON.

**Learning objectives**

- Build an end-to-end RAG system over JSONL and PDF sources
- Return source documents with each answer and attach structured per-claim citations
- Explain why each retrieved chunk is relevant
- Choose a row / record representation for CSV and JSON data
- Run a fully local pipeline with Hugging Face models and FAISS

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 10.1 | Environment setup and a complete RAG system | [`01a_setup`](course/p4_rag_applications/m10_end_to_end_rag_systems/notebooks/01a_setup.ipynb)<br>[`01b_build_a_simple_rag_system`](course/p4_rag_applications/m10_end_to_end_rag_systems/notebooks/01b_build_a_simple_rag_system.ipynb) | [`01c_simple_rag_pdf`](course/p4_rag_applications/m10_end_to_end_rag_systems/optional/01c_simple_rag_pdf.ipynb) *(alternate)* |
| 10.2 | Answers with sources and per-claim citations | [`02a_rag_system_with_sources`](course/p4_rag_applications/m10_end_to_end_rag_systems/notebooks/02a_rag_system_with_sources.ipynb)<br>[`02b_rag_system_with_citations`](course/p4_rag_applications/m10_end_to_end_rag_systems/notebooks/02b_rag_system_with_citations.ipynb) | — |
| 10.3 | Explainable retrieval | [`03a_explainable_retrieval`](course/p4_rag_applications/m10_end_to_end_rag_systems/notebooks/03a_explainable_retrieval.ipynb) | — |
| 10.4 | RAG over structured data: CSV and JSON | [`04a_structured_data_rag`](course/p4_rag_applications/m10_end_to_end_rag_systems/notebooks/04a_structured_data_rag.ipynb) | [`04b_simple_csv_rag`](course/p4_rag_applications/m10_end_to_end_rag_systems/optional/04b_simple_csv_rag.ipynb) *(alternate)*<br>[`04c_json_rag`](course/p4_rag_applications/m10_end_to_end_rag_systems/optional/04c_json_rag.ipynb) *(extension)* |
| 10.5 | Fully local RAG with Hugging Face and FAISS | [`05a_local_rag_huggingface_faiss`](course/p4_rag_applications/m10_end_to_end_rag_systems/notebooks/05a_local_rag_huggingface_faiss.ipynb) | — |

**Hands-on lab.** Module lab, AI research assistant: package ingestion, retrieval, structured answers with citations and session history into one class (05/10/11). Notebook: [`lab_ai_research_assistant`](course/p4_rag_applications/m10_end_to_end_rag_systems/notebooks/lab_ai_research_assistant.ipynb).

**Key concepts:** Grounded generation · Citation schema · Record representation · Local inference

### Module 11 — Multimodal RAG

**Level:** Core · **Time:** ~3 h · **Notebooks:** 2 mandatory, 1 optional · **Source:** `05/11_multimodal_rag`

**Why it matters.** Real documents contain charts, diagrams and scanned pages. Text-only pipelines silently drop that information.

**Learning objectives**

- Embed text and images in one space with CLIP and answer with a multimodal LLM
- Caption images with a vision model and index captions alongside text
- Retrieve whole PDF pages as images with ColPali (late interaction)

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 11.1 | Shared text–image embedding space with CLIP | [`01a_multimodal_rag_with_clip`](course/p4_rag_applications/m11_multimodal_rag/notebooks/01a_multimodal_rag_with_clip.ipynb) | — |
| 11.2 | Caption-then-index with a vision LLM | [`02a_multimodal_rag_with_captioning`](course/p4_rag_applications/m11_multimodal_rag/notebooks/02a_multimodal_rag_with_captioning.ipynb) | — |
| 11.3 | Page-image retrieval with ColPali *(optional lesson)* | — | [`03a_multimodal_rag_with_colpali`](course/p4_rag_applications/m11_multimodal_rag/optional/03a_multimodal_rag_with_colpali.ipynb) *(platform-specific)* |

**Hands-on lab.** Chart-aware RAG: index a report that holds key numbers only in figures and show which of the three approaches answers questions about them.

**Key concepts:** Joint embedding space · Captioning · Late interaction · Page-level retrieval

### Module 12 — Framework Fluency: LlamaIndex

**Level:** Core · **Time:** ~3 h · **Notebooks:** 4 mandatory, 1 optional · **Source:** `05/13_llamaindex_rag`

**Why it matters.** The techniques are framework-independent. Rebuilding them in LlamaIndex proves you understand the idea and not only one API.

**Learning objectives**

- Map LangChain concepts to LlamaIndex (Document/Node, Retriever, QueryEngine, NodePostprocessor)
- Build simple PDF and CSV RAG in LlamaIndex
- Use QueryFusionRetriever, LLM and cross-encoder postprocessors, and sentence-window retrieval

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 12.1 | Simple PDF and CSV RAG in LlamaIndex | [`01a_simple_rag_with_llamaindex`](course/p4_rag_applications/m12_llamaindex/notebooks/01a_simple_rag_with_llamaindex.ipynb) | [`01b_simple_csv_rag_with_llamaindex`](course/p4_rag_applications/m12_llamaindex/optional/01b_simple_csv_rag_with_llamaindex.ipynb) *(extension)* |
| 12.2 | Fusion retrieval with QueryFusionRetriever | [`02a_fusion_retrieval_with_llamaindex`](course/p4_rag_applications/m12_llamaindex/notebooks/02a_fusion_retrieval_with_llamaindex.ipynb) | — |
| 12.3 | Reranking with node postprocessors | [`03a_reranking_with_llamaindex`](course/p4_rag_applications/m12_llamaindex/notebooks/03a_reranking_with_llamaindex.ipynb) | — |
| 12.4 | Sentence-window retrieval | [`04a_context_enrichment_window_with_llamaindex`](course/p4_rag_applications/m12_llamaindex/notebooks/04a_context_enrichment_window_with_llamaindex.ipynb) | — |

**Hands-on lab.** Port one of your Part III pipelines (hybrid + rerank) to LlamaIndex and confirm the metrics match.

**Key concepts:** Nodes · QueryEngine · Postprocessors · Sentence window

**Part IV checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).

---

## Part V — Agent Foundations for RAG

**Weeks 7–9 · Core** — The agent loop, tools, ReAct, the five workflow patterns, planning and reflection. Agentic RAG in Part VI is built from exactly these parts.

### Module 13 — The Agent Loop & Tool Calling

**Level:** Core · **Time:** ~5 h · **Notebooks:** 7 mandatory, 4 optional · **Source:** `06/01_agents_from_scratch`, `06/02_tools_and_function_calling`

**Why it matters.** Agentic RAG is an agent loop with a retriever as one of its tools. Writing that loop by hand first makes every framework later in the course transparent.

**Learning objectives**

- Implement reflection, tool use and ReAct-style planning with raw API calls and no framework
- Define tools, bind them to a model and run the tool-calling loop by hand and in LangGraph
- Handle tool errors and evaluate whether the model called the right tool with the right arguments
- Choose between client-side tools and provider-hosted tools such as code execution

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 13.1 | Agentic patterns from scratch: reflection, tool use, ReAct planning | [`01b_tool_use_pattern`](course/p5_agent_foundations/m13_agent_loop_and_tools/notebooks/01b_tool_use_pattern.ipynb)<br>[`01c_planning_pattern_react`](course/p5_agent_foundations/m13_agent_loop_and_tools/notebooks/01c_planning_pattern_react.ipynb) | [`01a_reflection_pattern`](course/p5_agent_foundations/m13_agent_loop_and_tools/optional/01a_reflection_pattern.ipynb) *(extension)* |
| 13.2 | A real-world agent on raw API calls (Hacker News chatbot) *(optional lesson)* | — | [`02a_real_world_agent_hacker_news_chatbot`](course/p5_agent_foundations/m13_agent_loop_and_tools/optional/02a_real_world_agent_hacker_news_chatbot.ipynb) *(extension)* |
| 13.3 | Defining tools and binding them to a model | [`03a_defining_tools`](course/p5_agent_foundations/m13_agent_loop_and_tools/notebooks/03a_defining_tools.ipynb) | — |
| 13.4 | The manual tool loop and the augmented LLM in LangGraph | [`04a_tool_calling_manual_loop`](course/p5_agent_foundations/m13_agent_loop_and_tools/notebooks/04a_tool_calling_manual_loop.ipynb)<br>[`04b_augmented_llm_with_tools_langgraph`](course/p5_agent_foundations/m13_agent_loop_and_tools/notebooks/04b_augmented_llm_with_tools_langgraph.ipynb) | — |
| 13.5 | Tool errors and evaluating tool calls | [`05a_tool_loop_errors_and_evaluation`](course/p5_agent_foundations/m13_agent_loop_and_tools/notebooks/05a_tool_loop_errors_and_evaluation.ipynb) | — |
| 13.6 | Hosted vs client-side tools: code execution and image generation | [`06a_hosted_vs_client_side_tools`](course/p5_agent_foundations/m13_agent_loop_and_tools/notebooks/06a_hosted_vs_client_side_tools.ipynb) | [`06b_hosted_code_execution`](course/p5_agent_foundations/m13_agent_loop_and_tools/optional/06b_hosted_code_execution.ipynb) *(extension)*<br>[`06c_agentic_image_generation`](course/p5_agent_foundations/m13_agent_loop_and_tools/optional/06c_agentic_image_generation.ipynb) *(extension)* |

**Hands-on lab.** Retriever as a tool, by hand: wrap your Part IV retriever as a tool, run it through your own tool loop with no framework, and log every tool call and error.

**Key concepts:** Agent loop · Tool schema · Tool-call evaluation · Hosted vs client-side tools

### Module 14 — ReAct Agents & LangChain create_agent

**Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 7 optional · **Source:** `06/03_react_agents`, `06/04_langchain_agents_and_middleware`

**Why it matters.** ReAct is the closed reason–act–observe loop most RAG agents run. LangChain 1.x packages it as `create_agent`, and middleware is where you add guardrails and human review.

**Learning objectives**

- Build a ReAct agent in LangGraph and explain how it differs from single-shot tool calling
- Build the same agent with LangChain 1.x `create_agent`, with typed messages and structured output
- Control agents with middleware, including human-in-the-loop
- Apply ReAct to web research, software engineering and computer use

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 14.1 | The ReAct loop in LangGraph; tool calling vs ReAct | [`01a_react_agent_langgraph`](course/p5_agent_foundations/m14_react_agents/notebooks/01a_react_agent_langgraph.ipynb)<br>[`01b_tool_calling_vs_react`](course/p5_agent_foundations/m14_react_agents/notebooks/01b_tool_calling_vs_react.ipynb) | — |
| 14.2 | ReAct with LangChain `create_agent` | [`02a_react_with_create_agent`](course/p5_agent_foundations/m14_react_agents/notebooks/02a_react_with_create_agent.ipynb) | — |
| 14.3 | Models, messages and structured output in LangChain 1.x | [`03c_structured_output`](course/p5_agent_foundations/m14_react_agents/notebooks/03c_structured_output.ipynb) | [`03a_model_integration`](course/p5_agent_foundations/m14_react_agents/optional/03a_model_integration.ipynb) *(extension)*<br>[`03b_messages`](course/p5_agent_foundations/m14_react_agents/optional/03b_messages.ipynb) *(extension)* |
| 14.4 | Middleware, including human-in-the-loop | [`04a_middleware`](course/p5_agent_foundations/m14_react_agents/notebooks/04a_middleware.ipynb) | — |
| 14.5 | Applied ReAct: web research, SWE and computer-use agents | [`05a_web_research_agent`](course/p5_agent_foundations/m14_react_agents/notebooks/05a_web_research_agent.ipynb) | [`05b_swe_agent_applied`](course/p5_agent_foundations/m14_react_agents/optional/05b_swe_agent_applied.ipynb) *(extension)*<br>[`05c_browser_agent_computer_use`](course/p5_agent_foundations/m14_react_agents/optional/05c_browser_agent_computer_use.ipynb) *(extension)*<br>[`05d_vision_driven_computer_use`](course/p5_agent_foundations/m14_react_agents/optional/05d_vision_driven_computer_use.ipynb) *(extension)* |
| 14.6 | Exercise: intelligent travel assistant agent (with solution) *(optional lesson)* | — | [`06a_intelligent_travel_assistant_agent`](course/p5_agent_foundations/m14_react_agents/exercises/06a_intelligent_travel_assistant_agent.ipynb) *(extension)*<br>[`06b_intelligent_travel_assistant_solution`](course/p5_agent_foundations/m14_react_agents/exercises/06b_intelligent_travel_assistant_solution.ipynb) *(extension)* |

**Hands-on lab.** ReAct research agent: give a `create_agent` agent your RAG retriever and a web-search tool, add a middleware that blocks off-topic questions, and compare its answers with your Part IV system.

**Key concepts:** Reason–act–observe · create_agent · Middleware · Structured output

### Module 15 — Agentic Workflow Patterns

**Level:** Core · **Time:** ~7 h · **Notebooks:** 8 mandatory, 5 optional · **Source:** `06/05_prompt_chaining`, `06/06_routing`, `06/07_parallelization`, `06/08_orchestrator_worker`, `06/09_evaluator_optimizer`

**Why it matters.** Every agentic RAG architecture is a combination of five patterns: CRAG is evaluator–optimizer, adaptive RAG is routing, query decomposition is orchestrator–worker. Learn the patterns once and the architectures become easy to read.

**Learning objectives**

- Chain prompts with quality gates between steps
- Route by handler or by model tier to control cost
- Fan out independent branches (sectioning and voting) and merge the results
- Decompose tasks at runtime with orchestrator–worker and the `Send` API
- Build bounded generate–critique–refine loops (evaluator–optimizer)
- Explain where LCEL stops (it cannot loop) and when a workflow needs LangGraph

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 15.1 | Prompt chaining with quality gates | [`01a_prompt_chaining_langgraph`](course/p5_agent_foundations/m15_agentic_workflow_patterns/notebooks/01a_prompt_chaining_langgraph.ipynb) | [`01b_prompt_chaining_structured_output`](course/p5_agent_foundations/m15_agentic_workflow_patterns/optional/01b_prompt_chaining_structured_output.ipynb) *(extension)*<br>[`01c_prompt_chaining_lcel`](course/p5_agent_foundations/m15_agentic_workflow_patterns/optional/01c_prompt_chaining_lcel.ipynb) *(alternate)* |
| 15.2 | Routing by handler and by model tier | [`02a_routing_langgraph`](course/p5_agent_foundations/m15_agentic_workflow_patterns/notebooks/02a_routing_langgraph.ipynb)<br>[`02b_routing_by_model_tier`](course/p5_agent_foundations/m15_agentic_workflow_patterns/notebooks/02b_routing_by_model_tier.ipynb) | [`02c_routing_lcel_runnable_branch`](course/p5_agent_foundations/m15_agentic_workflow_patterns/optional/02c_routing_lcel_runnable_branch.ipynb) *(alternate)* |
| 15.3 | Parallelization: sectioning and voting | [`03a_parallelization_langgraph`](course/p5_agent_foundations/m15_agentic_workflow_patterns/notebooks/03a_parallelization_langgraph.ipynb)<br>[`03b_parallelization_sectioning_and_voting`](course/p5_agent_foundations/m15_agentic_workflow_patterns/notebooks/03b_parallelization_sectioning_and_voting.ipynb) | [`03c_parallelization_lcel`](course/p5_agent_foundations/m15_agentic_workflow_patterns/optional/03c_parallelization_lcel.ipynb) *(alternate)* |
| 15.4 | Orchestrator–worker with the Send API | [`04a_orchestrator_worker_send_api`](course/p5_agent_foundations/m15_agentic_workflow_patterns/notebooks/04a_orchestrator_worker_send_api.ipynb) | [`04b_orchestrator_worker_lcel_map`](course/p5_agent_foundations/m15_agentic_workflow_patterns/optional/04b_orchestrator_worker_lcel_map.ipynb) *(alternate)* |
| 15.5 | Evaluator–optimizer loops, always bounded: LangGraph vs LCEL | [`05a_evaluator_optimizer_langgraph`](course/p5_agent_foundations/m15_agentic_workflow_patterns/notebooks/05a_evaluator_optimizer_langgraph.ipynb)<br>[`05b_evaluator_optimizer_lcel`](course/p5_agent_foundations/m15_agentic_workflow_patterns/notebooks/05b_evaluator_optimizer_lcel.ipynb) | — |

**Hands-on lab.** Pattern mapping: rebuild query decomposition (M8) as orchestrator–worker and an answer-quality check as evaluator–optimizer, then compare latency and cost with the chain versions.

**Key concepts:** Workflow vs agent · Quality gates · Fan-out / fan-in · Bounded loops

### Module 16 — Planning, Reflection & Reasoning Patterns

**Level:** Advanced · **Time:** ~6 h · **Notebooks:** 8 mandatory, 9 optional · **Source:** `06/10_planning`, `06/11_reflection`, `06/12_advanced_cognitive_patterns`

**Why it matters.** Deep research and multi-hop RAG need a plan, and grounded answers need self-checks. Reflection and chain-of-verification are the general forms of Self-RAG's groundedness checks.

**Learning objectives**

- Compare ReAct with plan-and-execute and add replanning
- Build a deep-research planner and a reflective dynamic planning agent
- Apply Reflection, Reflexion, chain-of-verification and constitutional critique
- Use self-consistency, tree of thoughts and LATS when one reasoning path is not reliable enough

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 16.1 | Plan-and-execute vs ReAct; decompose, execute, replan | [`01a_planning_react_vs_plan`](course/p5_agent_foundations/m16_planning_reflection_reasoning/notebooks/01a_planning_react_vs_plan.ipynb)<br>[`01b_planning_decompose_execute_replan`](course/p5_agent_foundations/m16_planning_reflection_reasoning/notebooks/01b_planning_decompose_execute_replan.ipynb) | — |
| 16.2 | Deep-research and reflective dynamic planners | [`02a_planning_agent_deep_research`](course/p5_agent_foundations/m16_planning_reflection_reasoning/notebooks/02a_planning_agent_deep_research.ipynb) | [`02b_reflective_dynamic_planning_agent`](course/p5_agent_foundations/m16_planning_reflection_reasoning/optional/02b_reflective_dynamic_planning_agent.ipynb) *(extension)* |
| 16.3 | Reflection and Reflexion agents | [`03a_reflection_agents`](course/p5_agent_foundations/m16_planning_reflection_reasoning/notebooks/03a_reflection_agents.ipynb)<br>[`03b_reflexion_agents`](course/p5_agent_foundations/m16_planning_reflection_reasoning/notebooks/03b_reflexion_agents.ipynb) | [`03c_reflection_architecture`](course/p5_agent_foundations/m16_planning_reflection_reasoning/optional/03c_reflection_architecture.ipynb) *(alternate)* |
| 16.4 | Chain-of-verification and constitutional critique | [`04a_chain_of_verification`](course/p5_agent_foundations/m16_planning_reflection_reasoning/notebooks/04a_chain_of_verification.ipynb) | [`04b_constitutional_ai_critique_loop`](course/p5_agent_foundations/m16_planning_reflection_reasoning/optional/04b_constitutional_ai_critique_loop.ipynb) *(extension)* |
| 16.5 | Self-Discover and reflective code generation *(optional lesson)* | — | [`05a_self_discover`](course/p5_agent_foundations/m16_planning_reflection_reasoning/optional/05a_self_discover.ipynb) *(extension)*<br>[`05b_reflective_code_generation_agent`](course/p5_agent_foundations/m16_planning_reflection_reasoning/optional/05b_reflective_code_generation_agent.ipynb) *(extension)* |
| 16.6 | Self-consistency, tree of thoughts and LATS | [`06a_self_consistency`](course/p5_agent_foundations/m16_planning_reflection_reasoning/notebooks/06a_self_consistency.ipynb)<br>[`06b_tree_of_thoughts`](course/p5_agent_foundations/m16_planning_reflection_reasoning/notebooks/06b_tree_of_thoughts.ipynb) | [`06c_lats`](course/p5_agent_foundations/m16_planning_reflection_reasoning/optional/06c_lats.ipynb) *(extension)* |
| 16.7 | Simulator-in-the-loop, metacognition and exemplar memory *(optional lesson)* | — | [`07a_mental_loop_simulator`](course/p5_agent_foundations/m16_planning_reflection_reasoning/optional/07a_mental_loop_simulator.ipynb) *(extension)*<br>[`07b_reflexive_metacognitive`](course/p5_agent_foundations/m16_planning_reflection_reasoning/optional/07b_reflexive_metacognitive.ipynb) *(extension)*<br>[`07c_self_improving_exemplar_memory`](course/p5_agent_foundations/m16_planning_reflection_reasoning/optional/07c_self_improving_exemplar_memory.ipynb) *(extension)* |

**Hands-on lab.** Verified answers: add chain-of-verification to your RAG answer step and measure how many unsupported claims it removes on the golden set.

**Key concepts:** Plan-and-execute · Replanning · Chain-of-verification · Tree of thoughts / LATS

### Module 17 — Human Approval & Applied Single-Agent Builds

**Level:** Advanced · **Time:** ~5 h · **Notebooks:** 4 mandatory, 6 optional · **Source:** `06/13_human_approval_basics`, `06/14_applied_single_agent_builds`

**Why it matters.** Real agents take actions, so they need approval gates. The applied builds also show text-to-SQL, which is often a better retriever than vectors for structured data.

**Learning objectives**

- Put a dry-run and approval gate in front of consequential actions
- Build research, competitive-intelligence and financial-analyst agents
- Retrieve from SQL databases with a text-to-SQL workflow and a text-to-SQL ReAct agent
- Build LLM workflow apps over business text (reviews, IT support, writing, quizzes)

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 17.1 | Dry-run harness and human approval | [`01a_dry_run_harness`](course/p5_agent_foundations/m17_human_approval_applied_agents/notebooks/01a_dry_run_harness.ipynb) | — |
| 17.2 | Research and competitive-intelligence agents | [`02a_research_assistant_agent`](course/p5_agent_foundations/m17_human_approval_applied_agents/notebooks/02a_research_assistant_agent.ipynb) | [`02b_competitive_intelligence_agent`](course/p5_agent_foundations/m17_human_approval_applied_agents/optional/02b_competitive_intelligence_agent.ipynb) *(extension)* |
| 17.3 | Financial analyst agent *(optional lesson)* | — | [`03a_financial_analyst_agent`](course/p5_agent_foundations/m17_human_approval_applied_agents/optional/03a_financial_analyst_agent.ipynb) *(extension)* |
| 17.4 | Text-to-SQL: workflow vs ReAct agent | [`04a_text2sql_workflow`](course/p5_agent_foundations/m17_human_approval_applied_agents/notebooks/04a_text2sql_workflow.ipynb)<br>[`04b_text2sql_react_agent`](course/p5_agent_foundations/m17_human_approval_applied_agents/notebooks/04b_text2sql_react_agent.ipynb) | — |
| 17.5 | LLM workflow apps: review analyst, IT support desk, tailored writer, quiz generator *(optional lesson)* | — | [`05a_review_analyst`](course/p5_agent_foundations/m17_human_approval_applied_agents/optional/05a_review_analyst.ipynb) *(extension)*<br>[`05b_multilingual_it_support_desk`](course/p5_agent_foundations/m17_human_approval_applied_agents/optional/05b_multilingual_it_support_desk.ipynb) *(extension)*<br>[`05c_audience_tailored_writer`](course/p5_agent_foundations/m17_human_approval_applied_agents/optional/05c_audience_tailored_writer.ipynb) *(extension)*<br>[`05d_quiz_generator`](course/p5_agent_foundations/m17_human_approval_applied_agents/optional/05d_quiz_generator.ipynb) *(extension)* |

**Hands-on lab.** SQL or vectors: answer the same 20 questions over a product catalogue with CSV RAG (M10) and with the text-to-SQL agent, and record which wins for each question type.

**Key concepts:** Approval gates · Dry run · Text-to-SQL · Workflow apps

**Part V checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).

---

## Part VI — Agentic & Self-Correcting RAG

**Weeks 10–11 · Advanced** — Retrieval that makes decisions: grade, rewrite, fall back to the web, reflect, route, and act as an agent tool.

### Module 18 — Agentic RAG Foundations: Grading & Query Rewriting

**Level:** Advanced · **Time:** ~4 h · **Notebooks:** 2 mandatory, 1 optional · **Source:** `09/01_retrieval_grading_and_query_rewriting`

**Why it matters.** The smallest agentic step is to check what came back and try again when it is wrong. Every self-correcting architecture builds on this loop.

**Learning objectives**

- Wrap a retriever as a LangGraph tool
- Grade retrieved documents for relevance with a structured-output LLM
- Rewrite the query and retry when documents fail the grade
- Add topic guardrails and a bounded query-enhancement retry loop

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 18.1 | Retriever as a tool; grade then rewrite in LangGraph | [`01a_simple_agentic_rag`](course/p6_agentic_rag/m18_retrieval_grading_rewriting/notebooks/01a_simple_agentic_rag.ipynb) | — |
| 18.2 | The same agent on Databricks Vector Search *(optional lesson)* | — | [`02a_simple_agentic_rag_databricks`](course/p6_agentic_rag/m18_retrieval_grading_rewriting/optional/02a_simple_agentic_rag_databricks.ipynb) *(platform-specific)* |
| 18.3 | Guardrails, query optimisation and a retry loop | [`03a_advanced_rag_agent`](course/p6_agentic_rag/m18_retrieval_grading_rewriting/notebooks/03a_advanced_rag_agent.ipynb) | — |

**Hands-on lab.** Grader loop: add a relevance grader and a two-retry rewrite loop to your Part IV system and log how often each path fires on the golden set.

**Key concepts:** Document grader · Conditional edges · Bounded retries · Topic guardrails

### Module 19 — Self-Correcting RAG: CRAG & Self-RAG

**Level:** Advanced · **Time:** ~5 h · **Notebooks:** 2 mandatory, 2 optional · **Source:** `09/02_corrective_rag`, `09/03_self_rag`

**Why it matters.** Corrective RAG fixes bad retrieval; Self-RAG checks the answer. Together they are the classic patterns for reducing hallucination in production.

**Learning objectives**

- Build CRAG: grade documents, rewrite the query, fall back to web search (Tavily)
- Build Self-RAG: decide whether to retrieve, then check relevance, groundedness and utility
- Compare CRAG and Self-RAG on accuracy, latency and LLM-call cost

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 19.1 | Corrective RAG in LangGraph with web-search fallback | [`01a_agentic_corrective_rag_langgraph`](course/p6_agentic_rag/m19_crag_and_self_rag/notebooks/01a_agentic_corrective_rag_langgraph.ipynb) | [`01b_crag_rag_techniques`](course/p6_agentic_rag/m19_crag_and_self_rag/optional/01b_crag_rag_techniques.ipynb) *(alternate)* |
| 19.2 | Self-RAG: retrieve-or-not, relevance, groundedness, utility | [`02a_self_rag_langgraph`](course/p6_agentic_rag/m19_crag_and_self_rag/notebooks/02a_self_rag_langgraph.ipynb) | [`02b_self_rag_rag_techniques`](course/p6_agentic_rag/m19_crag_and_self_rag/optional/02b_self_rag_rag_techniques.ipynb) *(alternate)* |
| 19.3 | Trade-offs: when correction is worth the extra calls | *Lecture / discussion* | — |

**Hands-on lab.** Out-of-corpus stress test: send questions the corpus cannot answer and compare the baseline, CRAG and Self-RAG on refusals, web fallbacks and hallucinated answers.

**Key concepts:** Retrieval evaluator · Knowledge refinement · Reflection tokens · Groundedness check

### Module 20 — Adaptive RAG & Query Routing

**Level:** Advanced · **Time:** ~5 h · **Notebooks:** 3 mandatory, 2 optional · **Source:** `09/04_adaptive_rag_and_routing`, `05/08_query_transformation`

**Why it matters.** Different questions need different paths: some need no retrieval, some need the web, some need a specific knowledge base. Routing up front saves cost and improves answers.

**Learning objectives**

- Route queries to department knowledge bases with a LangGraph router agent
- Refactor an agentic RAG system into reusable modules
- Add sentiment detection and escalation to a human
- Route between vector store and web search, then grade documents and hallucinations
- Pick a retrieval strategy per query type (factual, analytical, opinion, contextual)

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 20.1 | Router agentic RAG over multiple knowledge bases | [`01a_router_agentic_rag`](course/p6_agentic_rag/m20_adaptive_rag_routing/notebooks/01a_router_agentic_rag.ipynb) | [`01b_router_agentic_rag_modular`](course/p6_agentic_rag/m20_adaptive_rag_routing/optional/01b_router_agentic_rag_modular.ipynb) *(extension)* |
| 20.2 | Customer-facing routing with sentiment and human escalation *(optional lesson)* | — | [`02a_healthcare_router_agentic_rag`](course/p6_agentic_rag/m20_adaptive_rag_routing/optional/02a_healthcare_router_agentic_rag.ipynb) *(alternate)* |
| 20.3 | Adaptive RAG: vector store vs web, with hallucination grading | [`03a_adaptive_rag_langgraph`](course/p6_agentic_rag/m20_adaptive_rag_routing/notebooks/03a_adaptive_rag_langgraph.ipynb) | — |
| 20.4 | Strategy per query type | [`04a_adaptive_retrieval_rag_techniques`](course/p6_agentic_rag/m20_adaptive_rag_routing/notebooks/04a_adaptive_retrieval_rag_techniques.ipynb) | — |

**Hands-on lab.** Support desk router: route billing, technical and general questions to separate knowledge bases, escalate negative-sentiment tickets, and report routing accuracy.

**Key concepts:** Query classification · Multi-KB routing · Human-in-the-loop escalation · Per-query strategy

### Module 21 — RAG as an Agent Tool

**Level:** Advanced · **Time:** ~3 h · **Notebooks:** 1 mandatory, 2 optional · **Source:** `09/05_rag_as_an_agent_tool`

**Why it matters.** In agent systems retrieval is one tool among many, and the agent decides when to call it. Tool design (name, description, inputs) now matters as much as retrieval quality.

**Learning objectives**

- Expose a RAG pipeline as a tool the agent chooses to call in LangGraph
- Build a managed RAG agent (datastore, parser, reranker, grounded LM) with the Contextual AI SDK
- Ship a LlamaIndex Wikipedia agent with a Chainlit chat UI

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 21.1 | RAG as a tool inside a LangGraph agent | [`01a_rag_as_tool_in_agents`](course/p6_agentic_rag/m21_rag_as_agent_tool/notebooks/01a_rag_as_tool_in_agents.ipynb) | — |
| 21.2 | Managed RAG platforms: Contextual AI *(optional lesson)* | — | [`02a_agentic_rag_contextual_ai`](course/p6_agentic_rag/m21_rag_as_agent_tool/optional/02a_agentic_rag_contextual_ai.ipynb) *(platform-specific)* |
| 21.3 | Exercise: LlamaIndex Wikipedia agent with Chainlit *(optional lesson)* | — | [`03a_llamaindex_wikipedia_agent`](course/p6_agentic_rag/m21_rag_as_agent_tool/optional/03a_llamaindex_wikipedia_agent) *(extension)* |

**Hands-on lab.** Two-tool agent: give an agent a private-docs RAG tool and a web-search tool, and tune the tool descriptions until it picks the right one on 20 mixed questions.

**Key concepts:** Tool descriptions · Agent-decided retrieval · Managed RAG · Chat UI

### Module 22 — Reliability, Feedback Loops & Diversity

**Level:** Advanced · **Time:** ~3 h · **Notebooks:** 2 mandatory, 1 optional · **Source:** `09/06_retrieval_feedback_and_reliability`

**Why it matters.** A RAG system in production must show where an answer came from, detect when it is unsupported, and improve from user feedback.

**Learning objectives**

- Add relevance checks, hallucination checks and source highlighting
- Re-score documents from user feedback and refresh the index periodically
- Balance relevance and diversity with Dartboard RAG

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 22.1 | Reliable RAG: relevance checks, hallucination checks, source highlighting | [`01a_reliable_rag`](course/p6_agentic_rag/m22_reliability_feedback/notebooks/01a_reliable_rag.ipynb) | — |
| 22.2 | Retrieval with a user-feedback loop | [`02a_retrieval_with_feedback_loop`](course/p6_agentic_rag/m22_reliability_feedback/notebooks/02a_retrieval_with_feedback_loop.ipynb) | — |
| 22.3 | Dartboard RAG: relevance and diversity together *(optional lesson)* | — | [`03a_dartboard_rag`](course/p6_agentic_rag/m22_reliability_feedback/optional/03a_dartboard_rag.ipynb) *(extension)* |

**Hands-on lab.** Feedback flywheel: simulate 100 thumbs-up / thumbs-down events and show the effect on ranking for the affected queries.

**Key concepts:** Hallucination detection · Source highlighting · Implicit vs explicit feedback · Diversity-aware selection

**Part VI checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).

---

## Part VII — Memory & Multi-Agent RAG

**Weeks 12–13 · Advanced** — Conversation and long-term memory as retrieval over the agent's own history, then supervisors, swarms and research teams that retrieve together.

### Module 23 — Conversation Memory & Conversational RAG

**Level:** Advanced · **Time:** ~5 h · **Notebooks:** 7 mandatory, 3 optional · **Source:** `08/01_langchain_conversation_memory`, `08/02_langgraph_threads_and_checkpoints`

**Why it matters.** Follow-up questions such as “and what about the second one?” fail without history. Conversational RAG rewrites each question with the chat history before retrieving.

**Learning objectives**

- Explain why LLMs forget and add message histories, windows and summaries
- Manage multi-user sessions and persist them to SQLite
- Build history-aware conversational RAG
- Give LangGraph agents thread-scoped memory with checkpointers and keep long threads affordable

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 23.1 | Why LLMs forget; classic memory classes | [`01a_why_llms_forget`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/notebooks/01a_why_llms_forget.ipynb) | [`01b_classic_memory_classes_and_chains`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/optional/01b_classic_memory_classes_and_chains.ipynb) *(extension)* |
| 23.2 | RunnableWithMessageHistory, multi-user sessions and persistence | [`02a_runnable_with_message_history`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/notebooks/02a_runnable_with_message_history.ipynb)<br>[`02b_multi_user_sessions_and_persistence`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/notebooks/02b_multi_user_sessions_and_persistence.ipynb) | — |
| 23.3 | Trimming, windowing and summary memory | [`03a_trimming_windowing_and_summary`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/notebooks/03a_trimming_windowing_and_summary.ipynb) | — |
| 23.4 | Conversational RAG with history-aware retrieval | [`04a_conversational_rag_with_history`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/notebooks/04a_conversational_rag_with_history.ipynb) | — |
| 23.5 | Memory apps: product recommender and research agent with SQL memory *(optional lesson)* | — | [`05a_multi_user_product_recommender`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/optional/05a_multi_user_product_recommender.ipynb) *(extension)*<br>[`05b_multi_user_research_agent_sql_memory`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/optional/05b_multi_user_research_agent_sql_memory.ipynb) *(extension)* |
| 23.6 | LangGraph threads, checkpoints and memory optimisations | [`06a_memory_and_conversational_agent`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/notebooks/06a_memory_and_conversational_agent.ipynb)<br>[`06b_memory_optimizations`](course/p7_memory_and_multi_agent/m23_conversational_memory_rag/notebooks/06b_memory_optimizations.ipynb) | — |

**Hands-on lab.** Follow-up test: write 15 three-turn conversations and compare retrieval hit rate on turns two and three with and without history-aware query rewriting.

**Key concepts:** Message history · History-aware retriever · Checkpointer / thread_id · Summary memory

### Module 24 — Long-Term & Agentic Memory

**Level:** Advanced · **Time:** ~5 h · **Notebooks:** 6 mandatory, 5 optional · **Source:** `08/03_long_term_and_persistent_memory`, `08/04_agentic_memory_architectures`

**Why it matters.** Long-term memory is retrieval over the agent's own past: facts, episodes and procedures. The same indexing and retrieval choices from Parts II–III apply.

**Learning objectives**

- Share memory across threads with a LangGraph `Store` (in-memory and Postgres)
- Build session, semantic, episodic and procedural memory layers
- Compare agentic memory architectures: graph memory, MemGPT tiers, Voyager skill library, Agent Workflow Memory

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 24.1 | Cross-thread memory with a Store | [`01a_cross_thread_memory_store`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/notebooks/01a_cross_thread_memory_store.ipynb) | — |
| 24.2 | Session, semantic, episodic and procedural memory on SQLite | [`02b_long_term_semantic_memory_sqlite`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/notebooks/02b_long_term_semantic_memory_sqlite.ipynb)<br>[`02c_long_term_episodic_memory_sqlite`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/notebooks/02c_long_term_episodic_memory_sqlite.ipynb) | [`02a_session_memory_sqlite`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/optional/02a_session_memory_sqlite.ipynb) *(extension)*<br>[`02d_long_term_procedural_memory_sqlite`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/optional/02d_long_term_procedural_memory_sqlite.ipynb) *(extension)* |
| 24.3 | A combined-memory agent | [`03a_combined_memory_agent_sqlite`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/notebooks/03a_combined_memory_agent_sqlite.ipynb) | — |
| 24.4 | Episodic + semantic stack and multi-hop graph memory | [`04a_episodic_with_semantic_memory`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/notebooks/04a_episodic_with_semantic_memory.ipynb) | [`04b_graph_memory_multi_hop`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/optional/04b_graph_memory_multi_hop.ipynb) *(extension)* |
| 24.5 | MemGPT tiers, Voyager skill library, Agent Workflow Memory | [`05a_memgpt_tiered_memory`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/notebooks/05a_memgpt_tiered_memory.ipynb) | [`05b_voyager_skill_library`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/optional/05b_voyager_skill_library.ipynb) *(extension)*<br>[`05c_agent_workflow_memory`](course/p7_memory_and_multi_agent/m24_long_term_agentic_memory/optional/05c_agent_workflow_memory.ipynb) *(extension)* |

**Hands-on lab.** Personal RAG: give your assistant semantic memory of user preferences and show that answers in a new thread use them.

**Key concepts:** Semantic / episodic / procedural memory · Store namespaces · Tiered memory · Skill library

### Module 25 — Multi-Agent Architectures

**Level:** Advanced · **Time:** ~5 h · **Notebooks:** 6 mandatory, 3 optional · **Source:** `08/05_multi_agent_foundations`, `08/06_supervisor_and_hierarchical_agents`, `08/07_swarm_and_handoffs`

**Why it matters.** When one agent has too many tools or knowledge bases, split it: a supervisor routes to specialist retrieval agents. This is routing (M20) at the agent level.

**Learning objectives**

- Decide when a task needs several agents instead of one
- Implement network, supervisor, tool-calling supervisor, hierarchical and custom architectures
- Design agent communication and add human review to a supervisor workflow
- Coordinate agents with handoffs and a swarm

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 25.1 | Monolithic vs multi-agent; a crew from scratch | [`01a_multi_agent_vs_monolithic_agent`](course/p7_memory_and_multi_agent/m25_multi_agent_architectures/notebooks/01a_multi_agent_vs_monolithic_agent.ipynb) | [`01b_multiagent_pattern_from_scratch`](course/p7_memory_and_multi_agent/m25_multi_agent_architectures/optional/01b_multiagent_pattern_from_scratch.ipynb) *(extension)* |
| 25.2 | The five multi-agent architectures and agent communication | [`02a_five_multi_agent_architectures`](course/p7_memory_and_multi_agent/m25_multi_agent_architectures/notebooks/02a_five_multi_agent_architectures.ipynb) | [`02b_agent_communication`](course/p7_memory_and_multi_agent/m25_multi_agent_architectures/optional/02b_agent_communication.ipynb) *(extension)* |
| 25.3 | Supervisor workflow with human review *(optional lesson)* | — | [`03a_supervisor_workflow_with_human_review`](course/p7_memory_and_multi_agent/m25_multi_agent_architectures/optional/03a_supervisor_workflow_with_human_review.ipynb) *(extension)* |
| 25.4 | Supervisors and hierarchical teams | [`04a_supervisor_pattern`](course/p7_memory_and_multi_agent/m25_multi_agent_architectures/notebooks/04a_supervisor_pattern.ipynb)<br>[`04b_hierarchical_agents`](course/p7_memory_and_multi_agent/m25_multi_agent_architectures/notebooks/04b_hierarchical_agents.ipynb) | — |
| 25.5 | Handoffs and swarms | [`05a_agent_handoffs`](course/p7_memory_and_multi_agent/m25_multi_agent_architectures/notebooks/05a_agent_handoffs.ipynb)<br>[`05b_multi_agent_swarm`](course/p7_memory_and_multi_agent/m25_multi_agent_architectures/notebooks/05b_multi_agent_swarm.ipynb) | — |

**Hands-on lab.** Specialist retrievers: replace the single router from M20 with a supervisor over three specialist RAG agents and compare routing accuracy and cost.

**Key concepts:** Supervisor · Hierarchical teams · Handoffs · Swarm

### Module 26 — Collaboration, Control & Parallel Agents

**Level:** Expert · **Time:** ~4 h · **Notebooks:** 4 mandatory, 5 optional · **Source:** `08/08_collaboration_and_control_patterns`, `08/09_async_and_parallel_multi_agent`

**Why it matters.** Research-style RAG benefits from several perspectives: STORM interviews multiple personas, debate surfaces conflicting evidence, and parallel agents cut latency.

**Learning objectives**

- Share intermediate results through a blackboard
- Use debate, meta-controllers and ensembles to improve answers
- Generate multi-perspective research with STORM
- Run agents concurrently with supersteps, reducers, `Send` map-reduce, async nodes and `astream`

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 26.1 | Blackboard architectures | [`01a_blackboard_intro`](course/p7_memory_and_multi_agent/m26_collaboration_parallel_agents/notebooks/01a_blackboard_intro.ipynb) | [`01b_blackboard_research_team`](course/p7_memory_and_multi_agent/m26_collaboration_parallel_agents/optional/01b_blackboard_research_team.ipynb) *(extension)* |
| 26.2 | Debate *(optional lesson)* | — | [`02a_debate`](course/p7_memory_and_multi_agent/m26_collaboration_parallel_agents/optional/02a_debate.ipynb) *(extension)* |
| 26.3 | STORM: multi-perspective research and writing | [`03a_storm`](course/p7_memory_and_multi_agent/m26_collaboration_parallel_agents/notebooks/03a_storm.ipynb) | — |
| 26.4 | Meta-controllers, ensembles and emergent systems *(optional lesson)* | — | [`04a_meta_controller`](course/p7_memory_and_multi_agent/m26_collaboration_parallel_agents/optional/04a_meta_controller.ipynb) *(extension)*<br>[`04b_ensemble_parallel_exploration`](course/p7_memory_and_multi_agent/m26_collaboration_parallel_agents/optional/04b_ensemble_parallel_exploration.ipynb) *(extension)*<br>[`04c_cellular_automata`](course/p7_memory_and_multi_agent/m26_collaboration_parallel_agents/optional/04c_cellular_automata.ipynb) *(extension)* |
| 26.5 | Parallel agents, async nodes and streaming | [`05a_parallel_agents`](course/p7_memory_and_multi_agent/m26_collaboration_parallel_agents/notebooks/05a_parallel_agents.ipynb)<br>[`05b_async_multi_agent_streaming`](course/p7_memory_and_multi_agent/m26_collaboration_parallel_agents/notebooks/05b_async_multi_agent_streaming.ipynb) | — |

**Hands-on lab.** Parallel retrieval: run the sub-questions of a decomposed query as parallel agents and stream partial answers, then report the latency saved.

**Key concepts:** Blackboard · Debate · STORM · Map-reduce / async

### Module 27 — Multi-Agent Applied Builds & Deep Agents

**Level:** Expert · **Time:** ~6 h · **Notebooks:** 7 mandatory, 10 optional · **Source:** `08/10_multi_agent_applied_builds`, `08/11_deep_agents_and_harness_engineering`

**Why it matters.** The applied builds show what production multi-agent systems need beyond the happy path: compliance checks, edge cases, testing, error handling and memory merging.

**Learning objectives**

- Build a multi-agent hotel reservation system step by step, including compliance, testing and error handling
- Pair developer and tester agents
- Build supervisor-led financial research and multi-agent research and summarisation systems
- Package sub-agents, skills, long-term memory and an execution backend as a deep agent

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 27.1 | Hotel system: environment, coordinator, reservation agent, compliance | [`01a_hotel_environment_and_coordinator`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/notebooks/01a_hotel_environment_and_coordinator.ipynb)<br>[`01b_hotel_reservation_agent`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/notebooks/01b_hotel_reservation_agent.ipynb)<br>[`01c_hotel_compliance_checker`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/notebooks/01c_hotel_compliance_checker.ipynb) | — |
| 27.2 | Hardening: edge cases, testing and system-wide error handling | [`02a_hotel_edge_cases_and_errors`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/notebooks/02a_hotel_edge_cases_and_errors.ipynb)<br>[`02b_hotel_testing_the_system`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/notebooks/02b_hotel_testing_the_system.ipynb) | [`02c_hotel_system_wide_error_handling`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/02c_hotel_system_wide_error_handling.ipynb) *(extension)* |
| 27.3 | Scaling: parallel agents, memory merging, language and sentiment, web search *(optional lesson)* | — | [`03a_hotel_parallel_reservation_agents`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/03a_hotel_parallel_reservation_agents.ipynb) *(extension)*<br>[`03b_hotel_merging_and_conversation_memory`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/03b_hotel_merging_and_conversation_memory.ipynb) *(extension)*<br>[`03c_hotel_guest_language_and_sentiment`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/03c_hotel_guest_language_and_sentiment.ipynb) *(extension)*<br>[`03d_hotel_web_search_integration`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/03d_hotel_web_search_integration.ipynb) *(extension)* |
| 27.4 | Developer vs tester agents *(optional lesson)* | — | [`04a_developer_vs_tester_agents`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/04a_developer_vs_tester_agents.ipynb) *(extension)* |
| 27.5 | Research systems: supervisor financial research, summarisation, full research system | [`05c_multi_agent_research_system`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/notebooks/05c_multi_agent_research_system.ipynb) | [`05a_supervisor_financial_research`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/05a_supervisor_financial_research.ipynb) *(extension)*<br>[`05b_multi_agent_research_summarization`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/05b_multi_agent_research_summarization.ipynb) *(extension)* |
| 27.6 | Deep agents: orchestrator, sub-agents, skills and long-term memory | [`06a_simple_coding_agent`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/notebooks/06a_simple_coding_agent.py) | [`06b_long_term_memory_agent`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/06b_long_term_memory_agent.py) *(extension)*<br>[`06c_skills`](course/p7_memory_and_multi_agent/m27_multi_agent_builds_deep_agents/optional/06c_skills) *(extension)* |

**Hands-on lab.** Research team: build a supervisor with a RAG researcher, a web researcher and a writer that cites sources, then test it on edge cases (no results, conflicting sources, tool failure).

**Key concepts:** Compliance agent · System testing · Memory merging · Deep-agent harness

**Part VII checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).

---

## Part VIII — Hierarchical, Memory & Graph RAG

**Weeks 14–15 · Expert** — Structural indexes for questions flat chunks cannot answer: summary trees, memory, knowledge graphs and GraphRAG.

### Module 28 — Hierarchical & Memory-Augmented Retrieval

**Level:** Expert · **Time:** ~4 h · **Notebooks:** 2 mandatory, 1 optional · **Source:** `09/07_hierarchical_retrieval_raptor`, `09/08_memory_augmented_and_light_rag`

**Why it matters.** Questions like 'what are the main themes of this book?' have no single matching chunk. Trees and memory let retrieval work at several levels of abstraction.

**Learning objectives**

- Build a recursive tree of abstractive summaries (RAPTOR) and retrieve across its levels
- Use a global memory model that drafts clues to guide retrieval over long documents (MemoRAG)
- Index entities and relations in a lightweight graph with dual-level retrieval (LightRAG)

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 28.1 | RAPTOR: clustering and recursive summarisation | [`01a_raptor`](course/p8_hierarchical_and_graph_rag/m28_hierarchical_memory_rag/notebooks/01a_raptor.ipynb) | — |
| 28.2 | MemoRAG: global memory and clue-guided retrieval *(optional lesson)* | — | [`02a_memorag`](course/p8_hierarchical_and_graph_rag/m28_hierarchical_memory_rag/optional/02a_memorag.ipynb) *(extension)* |
| 28.3 | LightRAG: low-level and high-level graph retrieval | [`03a_light_rag`](course/p8_hierarchical_and_graph_rag/m28_hierarchical_memory_rag/notebooks/03a_light_rag.ipynb) | — |

**Hands-on lab.** Global-question test: ask ten 'summarise / compare across the whole corpus' questions and compare flat RAG, RAPTOR and LightRAG.

**Key concepts:** Abstraction levels · Collapsed-tree retrieval · Global memory · Dual-level retrieval

### Module 29 — Knowledge Graphs with Neo4j

**Level:** Expert · **Time:** ~6 h · **Notebooks:** 6 mandatory, 1 optional · **Source:** `09/09_knowledge_graphs_with_neo4j`

**Why it matters.** Relationships such as 'which doctors treated patients with X at hospital Y' are joins, not similarity. Knowledge graphs answer them precisely.

**Learning objectives**

- Model a domain as nodes and relationships and query it with Cypher
- Load CSV data into a Neo4j knowledge graph
- Answer natural-language questions with LangChain's text-to-Cypher graph QA
- Add embeddings and a vector index to graph nodes for hybrid graph + vector retrieval
- Extract entities and relationships from text with an LLM and build KG-RAG end to end

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 29.1 | Graph fundamentals and Cypher | [`01a_kg_simple`](course/p8_hierarchical_and_graph_rag/m29_knowledge_graphs_neo4j/notebooks/01a_kg_simple.ipynb) | — |
| 29.2 | From CSV to knowledge graph | [`02a_healthcare_kg`](course/p8_hierarchical_and_graph_rag/m29_knowledge_graphs_neo4j/notebooks/02a_healthcare_kg.ipynb) | — |
| 29.3 | Natural-language graph QA (text-to-Cypher) | [`03a_query_kg_with_langchain`](course/p8_hierarchical_and_graph_rag/m29_knowledge_graphs_neo4j/notebooks/03a_query_kg_with_langchain.ipynb) | — |
| 29.4 | Vector indexes on graph nodes | [`04a_vector_indexing_and_embedding`](course/p8_hierarchical_and_graph_rag/m29_knowledge_graphs_neo4j/notebooks/04a_vector_indexing_and_embedding.ipynb) | — |
| 29.5 | LLM entity and relationship extraction | [`05a_entity_relationship_extraction`](course/p8_hierarchical_and_graph_rag/m29_knowledge_graphs_neo4j/notebooks/05a_entity_relationship_extraction.ipynb) | [`05b_create_kg_from_text`](course/p8_hierarchical_and_graph_rag/m29_knowledge_graphs_neo4j/exercises/05b_create_kg_from_text.ipynb) *(extension)* |
| 29.6 | End-to-end knowledge-graph RAG | [`06a_roman_empire_graph_rag`](course/p8_hierarchical_and_graph_rag/m29_knowledge_graphs_neo4j/notebooks/06a_roman_empire_graph_rag.ipynb) | — |

**Hands-on lab.** Domain KG: extract a graph from 20 documents in your domain, load it into Neo4j, and answer five multi-hop questions that vector RAG gets wrong.

**Key concepts:** Nodes, edges, properties · Cypher · Text-to-Cypher · Graph + vector hybrid

### Module 30 — GraphRAG Techniques

**Level:** Expert · **Time:** ~5 h · **Notebooks:** 2 mandatory, 2 optional · **Source:** `09/10_graphrag_techniques`

**Why it matters.** GraphRAG uses graph structure for retrieval itself: traversing concepts, summarising communities, and expanding through adjacency.

**Learning objectives**

- Build a concept graph over chunks and traverse it to answer questions
- Attach verifiable per-claim source attribution in local graph RAG
- Index with Microsoft GraphRAG and run global (community) and local queries
- Store entities, relations and passages in Milvus and expand retrieval through graph adjacency

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 30.1 | Concept-graph traversal | [`01a_graph_rag`](course/p8_hierarchical_and_graph_rag/m30_graphrag/notebooks/01a_graph_rag.ipynb) | — |
| 30.2 | Local GraphRAG with source attribution *(optional lesson)* | — | [`02a_graph_rag_local_attribution`](course/p8_hierarchical_and_graph_rag/m30_graphrag/optional/02a_graph_rag_local_attribution.ipynb) *(extension)* |
| 30.3 | Microsoft GraphRAG: communities, global vs local search | [`03a_microsoft_graphrag`](course/p8_hierarchical_and_graph_rag/m30_graphrag/notebooks/03a_microsoft_graphrag.ipynb) | — |
| 30.4 | Graph expansion inside a vector database (Milvus) *(optional lesson)* | — | [`04a_graphrag_with_milvus`](course/p8_hierarchical_and_graph_rag/m30_graphrag/optional/04a_graphrag_with_milvus.ipynb) *(platform-specific)* |

**Hands-on lab.** GraphRAG vs RAPTOR vs hybrid: run the same global and multi-hop question set through each and write a one-page recommendation including indexing cost.

**Key concepts:** Community detection · Global vs local search · Graph expansion · Indexing cost

**Part VIII checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).

---

## Part IX — Architecture Synthesis & Capstone

**Weeks 16–17 · Expert** — Compare every architecture side by side, choose one for a real problem, and ship it as a capstone.

### Module 31 — Agentic RAG Architectures: Choosing a Design

**Level:** Expert · **Time:** ~3 h · **Notebooks:** 2 mandatory, 0 optional · **Source:** `09/11_agentic_rag_architectures`

**Why it matters.** You now know more than a dozen architectures. The final skill is choosing the simplest one that meets the requirement.

**Learning objectives**

- Place every architecture from the course on one map: entry-level, self-correcting, routing, tool-based, structural
- Walk the whole RAG stack from basic RAG through RAPTOR / ColBERT to agentic self-correction
- Choose an architecture from query complexity, data shape, latency budget and cost

**Lessons**

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 31.1 | The agentic RAG architecture map | [`01a_AGENTIC_RAG_ARCHITECTURES`](course/p9_architecture_and_capstone/m31_architecture_synthesis/notebooks/01a_AGENTIC_RAG_ARCHITECTURES.md) | — |
| 31.2 | End-to-end RAG ecosystem walkthrough (incl. ColBERT and RAGAS) | [`02a_rag_ecosystem`](course/p9_architecture_and_capstone/m31_architecture_synthesis/notebooks/02a_rag_ecosystem.ipynb) | — |
| 31.3 | Decision framework: picking the simplest architecture that works | *Lecture / discussion* | — |

**Hands-on lab.** Architecture review: write a two-page design document for your capstone that justifies each component against a simpler alternative.

**Key concepts:** Architecture selection · Complexity budget · Late interaction (ColBERT) · End-to-end evaluation

**Part IX checkpoint:** concept quiz plus one design question (for example, “Your hit rate is fine but answers are wrong — which stage do you inspect first and why?”).

---

## Capstone projects (Weeks 16–17, ~12 h)

Pick one. Each capstone must ship a working system, an evaluation report against a golden question set, and a 10-minute demo.

### Capstone A — Enterprise Knowledge Assistant (Core)

A cited Q&A assistant over a company's PDFs, wiki pages and tables.

**Must include:**

- Multi-source ingestion with a metadata schema (M2)
- Measured chunking and embedding choice (M3, M4)
- pgvector with incremental indexing (M5)
- Hybrid retrieval and reranking (M7, M9)
- Per-claim citations (M10)
- CRAG fallback for out-of-corpus questions (M19)

### Capstone B — Customer-Support Routing Copilot (Advanced)

An agent that routes tickets across department knowledge bases, remembers each customer, and escalates to humans.

**Must include:**

- Query routing and self-query filters (M8, M20)
- Graded retrieval with a rewrite loop (M18)
- Conversation and long-term customer memory (M23, M24)
- RAG exposed as agent tools with approval gates (M21, M17)
- Hallucination checks and a feedback loop (M22)

### Capstone C — Multi-Agent Research Analyst (Advanced)

A supervisor-led research team that plans, retrieves from private and web sources in parallel, and writes a cited report.

**Must include:**

- Plan-and-execute with replanning (M16)
- Orchestrator–worker decomposition (M15)
- Supervisor with specialist RAG agents (M25)
- Parallel retrieval and STORM-style perspectives (M26)
- Edge-case testing and error handling (M27)

### Capstone D — Research GraphRAG Explorer (Expert)

An assistant that answers multi-hop and whole-corpus questions over a research collection.

**Must include:**

- arXiv and PDF ingestion including figures (M2, M11)
- Neo4j knowledge graph built by LLM extraction (M29)
- RAPTOR or Microsoft GraphRAG for global questions (M28, M30)
- Adaptive routing between vector, graph and global search (M20)
- Architecture decision record (M31)

## Assessment

| Component | Weight | What is assessed |
|---|---|---|
| Module labs | 40% | One lab per module, each reported as a change against the Module 1 baseline |
| Part checkpoints | 20% | Short concept quiz plus a design question at the end of each Part |
| Architecture review | 10% | The final module's design document, peer reviewed |
| Capstone | 30% | Working system, evaluation report on a golden set, and a 10-minute demo |

## Recommended additions (not covered by the source repos)

A top course would also cover the topics below. They are outside the scope of these repositories and are listed so the gaps are explicit.

| Topic | Status in repos | What to add |
|---|---|---|
| **RAG evaluation** | Partial | The repos include `evaluation/evalute_rag.py` helpers, LlamaIndex faithfulness and relevancy evaluators (05/03/10) and RAGAS cells (09/11/01), but no dedicated module. Add retrieval metrics (hit rate, recall@k, MRR, nDCG), generation metrics (faithfulness, answer relevancy, context precision), golden-set building and LLM-as-judge. The repos point to the separate `Agent_Evaluation_Demystified` repository for this. |
| **Caching (CacheRAG)** | Planned | Module 09/12 exists as a placeholder: semantic caching and result reuse. Embedding caching is already covered in 05/04/07. |
| **Production RAG** | Missing here | Serving behind an API, streaming, tracing, latency budgets and cost control. The repos defer this to repository 13 (production and observability). |
| **Security & governance** | Missing | Prompt injection carried in retrieved documents, document-level access control enforced through metadata filters, PII redaction at ingestion, and audit logging of sources. |
| **Vector index internals** | Missing | HNSW, IVF and product quantisation, the recall / latency / memory trade-off, and tuning parameters such as ef and nprobe. Fits as a lesson inside Module 5. |
| **Fine-tuning retrieval models** | Missing | Fine-tuning embedding models and rerankers on domain pairs, and synthetic query generation for training data. Fits after Module 9. |

## Appendix — source coverage

Every notebook in the source repositories, by source module, and the course modules that use it.

| Repo | Source module | Notebooks | Mandatory | Course modules |
|---|---|---|---|---|
| 05 | `01_introduction_to_rag` | 4 | 4 | M1 |
| 05 | `02_document_loading` | 13 | 4 | M2 |
| 05 | `03_chunking` | 10 | 4 | M3 |
| 05 | `04_embeddings` | 8 | 4 | M4 |
| 05 | `05_vector_stores` | 8 | 4 | M5 |
| 05 | `06_indexing_strategies` | 7 | 5 | M6 |
| 05 | `07_retrievers_and_hybrid_search` | 8 | 6 | M7 |
| 05 | `08_query_transformation` | 15 | 9 | M8 |
| 05 | `09_post_retrieval_and_reranking` | 7 | 5 | M9 |
| 05 | `10_building_rag_systems` | 12 | 9 | M6, M10 |
| 05 | `11_multimodal_rag` | 3 | 2 | M11 |
| 05 | `12_langchain_rag_implementations` | 2 | 2 | M5 |
| 05 | `13_llamaindex_rag` | 5 | 4 | M12 |
| 06 | `01_agents_from_scratch` | 4 | 2 | M13 |
| 06 | `02_tools_and_function_calling` | 7 | 5 | M13 |
| 06 | `03_react_agents` | 8 | 4 | M14 |
| 06 | `04_langchain_agents_and_middleware` | 4 | 2 | M14 |
| 06 | `05_prompt_chaining` | 3 | 1 | M15 |
| 06 | `06_routing` | 3 | 2 | M15 |
| 06 | `07_parallelization` | 3 | 2 | M15 |
| 06 | `08_orchestrator_worker` | 2 | 1 | M15 |
| 06 | `09_evaluator_optimizer` | 2 | 2 | M15 |
| 06 | `10_planning` | 4 | 3 | M16 |
| 06 | `11_reflection` | 7 | 3 | M16 |
| 06 | `12_advanced_cognitive_patterns` | 6 | 2 | M16 |
| 06 | `13_human_approval_basics` | 1 | 1 | M17 |
| 06 | `14_applied_single_agent_builds` | 9 | 3 | M17 |
| 06 | `solutions` | 1 | 0 | M14 |
| 08 | `01_langchain_conversation_memory` | 8 | 5 | M23 |
| 08 | `02_langgraph_threads_and_checkpoints` | 2 | 2 | M23 |
| 08 | `03_long_term_and_persistent_memory` | 6 | 4 | M24 |
| 08 | `04_agentic_memory_architectures` | 5 | 2 | M24 |
| 08 | `05_multi_agent_foundations` | 5 | 2 | M25 |
| 08 | `06_supervisor_and_hierarchical_agents` | 2 | 2 | M25 |
| 08 | `07_swarm_and_handoffs` | 2 | 2 | M25 |
| 08 | `08_collaboration_and_control_patterns` | 7 | 2 | M26 |
| 08 | `09_async_and_parallel_multi_agent` | 2 | 2 | M26 |
| 08 | `10_multi_agent_applied_builds` | 14 | 6 | M27 |
| 08 | `11_deep_agents_and_harness_engineering` | 0 | 0 | M27 |
| 09 | `01_retrieval_grading_and_query_rewriting` | 3 | 2 | M18 |
| 09 | `02_corrective_rag` | 2 | 1 | M19 |
| 09 | `03_self_rag` | 2 | 1 | M19 |
| 09 | `04_adaptive_rag_and_routing` | 5 | 3 | M20 |
| 09 | `05_rag_as_an_agent_tool` | 2 | 1 | M21 |
| 09 | `06_retrieval_feedback_and_reliability` | 3 | 2 | M22 |
| 09 | `07_hierarchical_retrieval_raptor` | 1 | 1 | M28 |
| 09 | `08_memory_augmented_and_light_rag` | 2 | 1 | M28 |
| 09 | `09_knowledge_graphs_with_neo4j` | 7 | 6 | M29 |
| 09 | `10_graphrag_techniques` | 4 | 2 | M30 |
| 09 | `11_agentic_rag_architectures` | 1 | 1 | M31 |
| 09 | `12_cacherag` | 0 | 0 | — (planned in repo) |
