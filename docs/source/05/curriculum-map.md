# Curriculum map

Module → notebook → one-line learning objective. Canonical lessons (consolidated, validated versions of a concept) are marked **canonical**; where two notebooks teach the same thing both are kept and the overlap is noted in the module README.

## 01 — [Introduction to RAG](../modules/01_introduction_to_rag/README.md)

Why retrieval-augmented generation exists and the four stages of a RAG pipeline, from a from-scratch index to a working LangChain baseline.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_indexing_from_scratch.ipynb](../modules/01_introduction_to_rag/notebooks/01_indexing_from_scratch.ipynb) | Build a tiny TF-IDF + nearest-neighbour index to see what 'indexing' means before any framework | RAG Demystified tracks |
| [02_retrieval_strategies.ipynb](../modules/01_introduction_to_rag/notebooks/02_retrieval_strategies.ipynb) | Retrieve by embedding similarity with a nearest-neighbour index over OpenAI embeddings | RAG Demystified tracks |
| [03_langchain_rag_quickstart.ipynb](../modules/01_introduction_to_rag/notebooks/03_langchain_rag_quickstart.ipynb) | Embed documents and store/search them with LangChain + Chroma instead of by hand | RAG Demystified tracks |
| [04_rag_lifecycle_and_baseline.ipynb](../modules/01_introduction_to_rag/notebooks/04_rag_lifecycle_and_baseline.ipynb) | Walk the full RAG lifecycle (load, split, embed, store, retrieve, generate) and build a measured baseline pipeline | RAG curriculum (canonical) |

## 02 — [Document Loading](../modules/02_document_loading/README.md)

Turning text, Markdown, CSV, JSON, PDF, Word, web, YouTube and custom sources into LangChain `Document` objects with useful metadata.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_document_loading_and_metadata.ipynb](../modules/02_document_loading/notebooks/01_document_loading_and_metadata.ipynb) | Load many source formats into Documents and design the metadata later stages rely on (canonical lesson) | RAG curriculum (canonical) |
| [02_text_loader.ipynb](../modules/02_document_loading/notebooks/02_text_loader.ipynb) | Load plain-text files with TextLoader | RAG Demystified tracks |
| [03_markdown_loader.ipynb](../modules/02_document_loading/notebooks/03_markdown_loader.ipynb) | Load Markdown in single and element mode with UnstructuredMarkdownLoader | RAG Demystified tracks |
| [04_csv_loader.ipynb](../modules/02_document_loading/notebooks/04_csv_loader.ipynb) | Load CSV rows as Documents with CSVLoader and UnstructuredCSVLoader | RAG Demystified tracks |
| [05_json_loader.ipynb](../modules/02_document_loading/notebooks/05_json_loader.ipynb) | Load JSON and JSON Lines with jq schemas and metadata functions | RAG Demystified tracks |
| [06_pdf_loader.ipynb](../modules/02_document_loading/notebooks/06_pdf_loader.ipynb) | Compare PyPDF, PyMuPDF and Unstructured PDF loaders, including element-level parsing | RAG Demystified tracks |
| [07_ms_word_loader.ipynb](../modules/02_document_loading/notebooks/07_ms_word_loader.ipynb) | Load .docx files with UnstructuredWordDocumentLoader, including section-based parsing | RAG Demystified tracks |
| [08_directory_loader.ipynb](../modules/02_document_loading/notebooks/08_directory_loader.ipynb) | Bulk-load a folder of mixed files with DirectoryLoader | RAG Demystified tracks |
| [09_youtube_transcript_loader.ipynb](../modules/02_document_loading/notebooks/09_youtube_transcript_loader.ipynb) | Load YouTube transcripts as Documents | RAG Demystified tracks |
| [10_url_loader.ipynb](../modules/02_document_loading/notebooks/10_url_loader.ipynb) | Scrape and clean web pages with RecursiveUrlLoader and BeautifulSoup | RAG Demystified tracks |
| [11_research_paper_loader.ipynb](../modules/02_document_loading/notebooks/11_research_paper_loader.ipynb) | Load research papers from arXiv with ArxivLoader | RAG Demystified tracks |
| [12_custom_loader.ipynb](../modules/02_document_loading/notebooks/12_custom_loader.ipynb) | Write a custom document loader by subclassing BaseLoader (lazy_load) | RAG Demystified tracks |
| [13_document_loaders_overview.ipynb](../modules/02_document_loading/notebooks/13_document_loaders_overview.ipynb) | Survey text, directory, web and PDF loaders and hand-built Documents in one notebook | RAG production course |

## 03 — [Chunking](../modules/03_chunking/README.md)

Splitting documents into retrievable units: character/recursive/token splitters, semantic chunking, proposition chunking and choosing a chunk size.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_document_splitting_and_chunking.ipynb](../modules/03_chunking/notebooks/01_document_splitting_and_chunking.ipynb) | Split documents with character, recursive, token and structure-aware splitters and measure the result (canonical lesson) | RAG curriculum (canonical) |
| [02_document_splitters_and_chunkers.ipynb](../modules/03_chunking/notebooks/02_document_splitters_and_chunkers.ipynb) | Tour LangChain's text splitters (character, recursive, token, NLTK, spaCy, Markdown/HTML/code) | RAG Demystified tracks |
| [03_text_splitters_and_chunking_strategies.ipynb](../modules/03_chunking/notebooks/03_text_splitters_and_chunking_strategies.ipynb) | Compare chunking strategies and chunk-size/overlap trade-offs on a PDF | RAG production course |
| [04_semantic_chunking.ipynb](../modules/03_chunking/notebooks/04_semantic_chunking.ipynb) | Chunk on meaning boundaries with embedding-distance breakpoints and compare against fixed-size chunks (canonical lesson) | RAG curriculum (canonical) |
| [05_semantic_chunking_walkthrough.ipynb](../modules/03_chunking/notebooks/05_semantic_chunking_walkthrough.ipynb) | Implement semantic chunking by hand with sentence embeddings and with LangChain's SemanticChunker | RAG Demystified tracks |
| [06_semantic_chunking_rag_techniques.ipynb](../modules/03_chunking/notebooks/06_semantic_chunking_rag_techniques.ipynb) | Build a semantic-chunked retriever over a PDF (RAG Techniques anthology version) | RAG Techniques anthology |
| [07_proposition_chunking.ipynb](../modules/03_chunking/notebooks/07_proposition_chunking.ipynb) | Turn text into atomic, self-contained propositions and index those instead of raw chunks (canonical lesson) | RAG curriculum (canonical) |
| [08_proposition_chunking_rag_techniques.ipynb](../modules/03_chunking/notebooks/08_proposition_chunking_rag_techniques.ipynb) | Generate and quality-check propositions with an LLM (RAG Techniques anthology version) | RAG Techniques anthology |
| [09_choosing_chunk_size.ipynb](../modules/03_chunking/notebooks/09_choosing_chunk_size.ipynb) | Choose a chunk size empirically by measuring retrieval quality across sizes (canonical lesson) | RAG curriculum (canonical) |
| [10_choose_chunk_size_llamaindex.ipynb](../modules/03_chunking/notebooks/10_choose_chunk_size_llamaindex.ipynb) | Evaluate response time, faithfulness and relevancy across chunk sizes with LlamaIndex evaluators | RAG Techniques anthology |

## 04 — [Embeddings](../modules/04_embeddings/README.md)

What embeddings are, how to generate them with OpenAI and Hugging Face models, and how to compare and choose an embedding model.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_embeddings_and_model_selection.ipynb](../modules/04_embeddings/notebooks/01_embeddings_and_model_selection.ipynb) | Understand embeddings, similarity metrics and how to select an embedding model (canonical lesson) | RAG curriculum (canonical) |
| [02_embedding_models.ipynb](../modules/04_embeddings/notebooks/02_embedding_models.ipynb) | Generate and compare embeddings from OpenAI and Hugging Face models | RAG Demystified tracks |
| [03_huggingface_embeddings.ipynb](../modules/04_embeddings/notebooks/03_huggingface_embeddings.ipynb) | Create sentence embeddings with Hugging Face models and visualise similarity | RAG Demystified tracks |
| [04_huggingface_embeddings_tutorial.ipynb](../modules/04_embeddings/notebooks/04_huggingface_embeddings_tutorial.ipynb) | Alternative walkthrough of Hugging Face text embeddings (overlaps 03) | RAG Demystified tracks |
| [05_openai_embeddings.ipynb](../modules/04_embeddings/notebooks/05_openai_embeddings.ipynb) | Use OpenAIEmbeddings: models, dimensions and cosine similarity | RAG Demystified tracks |
| [06_openai_embeddings_tutorial.ipynb](../modules/04_embeddings/notebooks/06_openai_embeddings_tutorial.ipynb) | Alternative OpenAI embeddings walkthrough (overlaps 05) | RAG Demystified tracks |
| [07_embeddings_deep_dive.ipynb](../modules/04_embeddings/notebooks/07_embeddings_deep_dive.ipynb) | Go deeper on embeddings: batching, caching with CacheBackedEmbeddings and similarity behaviour | RAG production course |
| [08_compare_embedding_models_databricks.ipynb](../modules/04_embeddings/notebooks/08_compare_embedding_models_databricks.ipynb) | Benchmark several embedding models side by side on Databricks with MLflow tracking | RAG Demystified tracks |

## 05 — [Vector Stores](../modules/05_vector_stores/README.md)

Storing and searching embeddings in Chroma, FAISS, Astra DB, Pinecone and others, and the index operations (add, update, delete, persist) a vector store supports.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_vector_stores_and_index_operations.ipynb](../modules/05_vector_stores/notebooks/01_vector_stores_and_index_operations.ipynb) | Create, query, update, delete and persist a vector store index (canonical lesson) | RAG curriculum (canonical) |
| [02_vector_database_operations.ipynb](../modules/05_vector_stores/notebooks/02_vector_database_operations.ipynb) | Perform core vector database operations with LangChain + Chroma | RAG Demystified tracks |
| [03_chromadb.ipynb](../modules/05_vector_stores/notebooks/03_chromadb.ipynb) | Build, persist and query a Chroma vector store end to end | RAG Demystified tracks |
| [04_faiss.ipynb](../modules/05_vector_stores/notebooks/04_faiss.ipynb) | Build, save and search a FAISS index | RAG Demystified tracks |
| [05_other_vector_stores.ipynb](../modules/05_vector_stores/notebooks/05_other_vector_stores.ipynb) | Use LangChain's InMemoryVectorStore and the common vector store interface | RAG Demystified tracks |
| [06_astra_db.ipynb](../modules/05_vector_stores/notebooks/06_astra_db.ipynb) | Use DataStax Astra DB as a managed vector store | RAG Demystified tracks |
| [07_pinecone.ipynb](../modules/05_vector_stores/notebooks/07_pinecone.ipynb) | Use Pinecone as a managed vector store | RAG Demystified tracks |
| [08_vector_stores_in_practice.ipynb](../modules/05_vector_stores/notebooks/08_vector_stores_in_practice.ipynb) | Ingest, persist, reload and search Chroma collections, including metadata filters | RAG production course |

## 06 — [Indexing Strategies](../modules/06_indexing_strategies/README.md)

Changing *what* is indexed: multi-representation and parent-document indexing, hierarchical indices, hypothetical prompt embeddings, document augmentation and contextual chunk headers.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_multi_representation_indexing.ipynb](../modules/06_indexing_strategies/notebooks/01_multi_representation_indexing.ipynb) | Embed a summary of each document but return the full document (multi-vector retriever) | RAG Demystified tracks |
| [02_parent_document_retrieval.ipynb](../modules/06_indexing_strategies/notebooks/02_parent_document_retrieval.ipynb) | Embed small child chunks but return their larger parent chunk | RAG Demystified tracks |
| [03_parent_document_retriever_postgres.ipynb](../modules/06_indexing_strategies/notebooks/03_parent_document_retriever_postgres.ipynb) | Run a parent-document retriever with a persistent Postgres docstore | RAG Demystified tracks |
| [04_hierarchical_indices.ipynb](../modules/06_indexing_strategies/notebooks/04_hierarchical_indices.ipynb) | Index summaries and detailed chunks in two tiers and search top-down | RAG Techniques anthology |
| [05_hypothetical_prompt_embeddings.ipynb](../modules/06_indexing_strategies/notebooks/05_hypothetical_prompt_embeddings.ipynb) | Pre-generate hypothetical questions per chunk at index time (HyPE) | RAG Techniques anthology |
| [06_document_augmentation.ipynb](../modules/06_indexing_strategies/notebooks/06_document_augmentation.ipynb) | Augment the index with generated questions per document/fragment | RAG Techniques anthology |
| [07_contextual_chunk_headers.ipynb](../modules/06_indexing_strategies/notebooks/07_contextual_chunk_headers.ipynb) | Prepend document-level context headers to chunks before embedding | RAG Techniques anthology |

## 07 — [Retrievers and Hybrid Search](../modules/07_retrievers_and_hybrid_search/README.md)

How candidates are selected: retriever interfaces, dense + sparse (BM25) hybrid search, fusion retrieval, MMR and metadata filtering.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_retrievers.ipynb](../modules/07_retrievers_and_hybrid_search/notebooks/01_retrievers.ipynb) | Use LangChain retrievers on Chroma: similarity, threshold, MMR, multi-query, compression and ensemble | RAG Demystified tracks |
| [02_dense_sparse_hybrid_retrieval.ipynb](../modules/07_retrievers_and_hybrid_search/notebooks/02_dense_sparse_hybrid_retrieval.ipynb) | Combine a dense (vector) and sparse (BM25) retriever with EnsembleRetriever | RAG Demystified tracks |
| [03_hybrid_search_rag.ipynb](../modules/07_retrievers_and_hybrid_search/notebooks/03_hybrid_search_rag.ipynb) | Build a RAG chain on top of BM25 + vector hybrid search | RAG Demystified tracks |
| [04_fusion_retrieval.ipynb](../modules/07_retrievers_and_hybrid_search/notebooks/04_fusion_retrieval.ipynb) | Fuse normalised vector and BM25 scores into one ranking | RAG Techniques anthology |
| [05_maximal_marginal_relevance.ipynb](../modules/07_retrievers_and_hybrid_search/notebooks/05_maximal_marginal_relevance.ipynb) | Trade relevance against diversity with Maximal Marginal Relevance | RAG Demystified tracks |
| [06_multi_faceted_filtering.ipynb](../modules/07_retrievers_and_hybrid_search/notebooks/06_multi_faceted_filtering.ipynb) | Filter retrieval by metadata, similarity threshold, keywords and diversity | RAG Techniques anthology |
| [07_advanced_retriever_patterns.ipynb](../modules/07_retrievers_and_hybrid_search/notebooks/07_advanced_retriever_patterns.ipynb) | Compare multi-query, contextual-compression, ensemble and parent-document retrievers in one chain | RAG production course |
| [08_hybrid_search_and_reranking_databricks.ipynb](../modules/07_retrievers_and_hybrid_search/notebooks/08_hybrid_search_and_reranking_databricks.ipynb) | Compare semantic, hybrid and hybrid + reranked search on Databricks Vector Search | RAG Demystified tracks |

## 08 — [Query Transformation](../modules/08_query_transformation/README.md)

Changing the query before retrieval: multi-query, RAG-Fusion, step-back prompting, HyDE, decomposition, routing and self-querying.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_multi_query_retrieval.ipynb](../modules/08_query_transformation/notebooks/01_multi_query_retrieval.ipynb) | Generate several rephrasings of a question and union their retrieved documents | RAG Demystified tracks |
| [02_rag_fusion.ipynb](../modules/08_query_transformation/notebooks/02_rag_fusion.ipynb) | Merge the rankings of multiple generated queries with Reciprocal Rank Fusion | RAG Demystified tracks |
| [03_step_back_prompting.ipynb](../modules/08_query_transformation/notebooks/03_step_back_prompting.ipynb) | Retrieve with a more general 'step-back' question alongside the original | RAG Demystified tracks |
| [04_hyde.ipynb](../modules/08_query_transformation/notebooks/04_hyde.ipynb) | Embed a hypothetical answer (HyDE) instead of the question | RAG Demystified tracks |
| [05_query_decomposition.ipynb](../modules/08_query_transformation/notebooks/05_query_decomposition.ipynb) | Break a complex question into sub-questions answered recursively or individually | RAG Demystified tracks |
| [06_routing_with_llm_classifier.ipynb](../modules/08_query_transformation/notebooks/06_routing_with_llm_classifier.ipynb) | Route a query to a specialist prompt with a structured-output LLM classifier | RAG Demystified tracks |
| [07_semantic_routing.ipynb](../modules/08_query_transformation/notebooks/07_semantic_routing.ipynb) | Route a query by embedding similarity to candidate prompts | RAG Demystified tracks |
| [08_self_querying_retrieval.ipynb](../modules/08_query_transformation/notebooks/08_self_querying_retrieval.ipynb) | Let an LLM turn a question into a semantic query plus a metadata filter | RAG Demystified tracks |
| [09_query_expansion.ipynb](../modules/08_query_transformation/notebooks/09_query_expansion.ipynb) | Expand a query with an LLM before retrieval | RAG Demystified tracks |
| [10_query_decomposition_walkthrough.ipynb](../modules/08_query_transformation/notebooks/10_query_decomposition_walkthrough.ipynb) | Decompose a query into sub-questions and answer each (overlaps 05) | RAG Demystified tracks |
| [11_hyde_walkthrough.ipynb](../modules/08_query_transformation/notebooks/11_hyde_walkthrough.ipynb) | Implement HyDE with Hugging Face embeddings and Chroma (overlaps 04) | RAG Demystified tracks |
| [12_multiquery_retrieval_walkthrough.ipynb](../modules/08_query_transformation/notebooks/12_multiquery_retrieval_walkthrough.ipynb) | Hand-build a multi-query chain and de-duplicate results (overlaps 01) | RAG Demystified tracks |
| [13_better_queries.ipynb](../modules/08_query_transformation/notebooks/13_better_queries.ipynb) | Multi-query plus multi-answer HyDE on the same corpus (near-duplicate of 12 with extra HyDE cells) | Udemy course notebook (anthology folder) |
| [14_query_transformations_rag_techniques.ipynb](../modules/08_query_transformation/notebooks/14_query_transformations_rag_techniques.ipynb) | Query rewriting, step-back prompting and sub-query decomposition (RAG Techniques anthology version) | RAG Techniques anthology |
| [15_hyde_rag_techniques.ipynb](../modules/08_query_transformation/notebooks/15_hyde_rag_techniques.ipynb) | HyDE retriever over a PDF (RAG Techniques anthology version) | RAG Techniques anthology |

## 09 — [Post-Retrieval and Reranking](../modules/09_post_retrieval_and_reranking/README.md)

Refining retrieved candidates before generation: cross-encoder and LLM reranking, contextual compression, context-enrichment windows and relevant segment extraction.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_cross_encoder_reranking.ipynb](../modules/09_post_retrieval_and_reranking/notebooks/01_cross_encoder_reranking.ipynb) | Re-score retrieved documents with a cross-encoder before generation | RAG Demystified tracks |
| [02_two_stage_reranking.ipynb](../modules/09_post_retrieval_and_reranking/notebooks/02_two_stage_reranking.ipynb) | Retrieve broadly, then rerank with an LLM for a precise top-k | RAG Demystified tracks |
| [03_reranking_cross_encoder_walkthrough.ipynb](../modules/09_post_retrieval_and_reranking/notebooks/03_reranking_cross_encoder_walkthrough.ipynb) | Cross-encoder reranking inside a LangChain RAG chain (overlaps 01) | RAG Demystified tracks |
| [04_reranking_methods.ipynb](../modules/09_post_retrieval_and_reranking/notebooks/04_reranking_methods.ipynb) | Compare LLM-based and cross-encoder reranking (RAG Techniques anthology version) | RAG Techniques anthology |
| [05_contextual_compression.ipynb](../modules/09_post_retrieval_and_reranking/notebooks/05_contextual_compression.ipynb) | Compress retrieved chunks to only the query-relevant parts with an LLM extractor | RAG Techniques anthology |
| [06_context_enrichment_window.ipynb](../modules/09_post_retrieval_and_reranking/notebooks/06_context_enrichment_window.ipynb) | Return neighbouring chunks around each hit to restore surrounding context | RAG Techniques anthology |
| [07_relevant_segment_extraction.ipynb](../modules/09_post_retrieval_and_reranking/notebooks/07_relevant_segment_extraction.ipynb) | Reconstruct contiguous relevant segments from chunk-level relevance scores | RAG Techniques anthology |

## 10 — [Building RAG Systems](../modules/10_building_rag_systems/README.md)

Assembling complete, non-agentic RAG pipelines over PDFs, CSV and JSON, with sources, citations and explainable retrieval, ending in a research-assistant lab.

| Notebook | Learning objective | Source |
|---|---|---|
| [00_setup.ipynb](../modules/10_building_rag_systems/notebooks/00_setup.ipynb) | Install the packages and load the environment used by the notebooks in this module | RAG Demystified tracks |
| [01_build_a_simple_rag_system.ipynb](../modules/10_building_rag_systems/notebooks/01_build_a_simple_rag_system.ipynb) | Build an end-to-end RAG system over JSONL and PDF sources with Chroma | RAG Demystified tracks |
| [02_contextual_retrieval_rag_system.ipynb](../modules/10_building_rag_systems/notebooks/02_contextual_retrieval_rag_system.ipynb) | Add LLM-generated chunk context before embedding (contextual retrieval) | RAG Demystified tracks |
| [03_rag_system_with_sources.ipynb](../modules/10_building_rag_systems/notebooks/03_rag_system_with_sources.ipynb) | Return the source documents alongside each answer | RAG Demystified tracks |
| [04_rag_system_with_citations.ipynb](../modules/10_building_rag_systems/notebooks/04_rag_system_with_citations.ipynb) | Attach structured, per-claim citations to answers | RAG Demystified tracks |
| [05_simple_rag_pdf.ipynb](../modules/10_building_rag_systems/notebooks/05_simple_rag_pdf.ipynb) | Build a simple FAISS-based RAG retriever over a PDF (RAG Techniques anthology version) | RAG Techniques anthology |
| [06_local_rag_huggingface_faiss.ipynb](../modules/10_building_rag_systems/notebooks/06_local_rag_huggingface_faiss.ipynb) | Run a fully local RAG pipeline with Hugging Face models and FAISS | RAG Techniques anthology |
| [07_explainable_retrieval.ipynb](../modules/10_building_rag_systems/notebooks/07_explainable_retrieval.ipynb) | Explain why each retrieved chunk is relevant to the query | RAG Techniques anthology |
| [08_structured_data_rag.ipynb](../modules/10_building_rag_systems/notebooks/08_structured_data_rag.ipynb) | Apply RAG to tabular and JSON data by choosing a row/record representation (canonical lesson) | RAG curriculum (canonical) |
| [09_simple_csv_rag.ipynb](../modules/10_building_rag_systems/notebooks/09_simple_csv_rag.ipynb) | Build a RAG pipeline over a CSV file (RAG Techniques anthology version) | RAG Techniques anthology |
| [10_json_rag.ipynb](../modules/10_building_rag_systems/notebooks/10_json_rag.ipynb) | Turn JSON records into embeddable text and search them semantically | RAG Techniques anthology |
| [11_ai_research_assistant.ipynb](../modules/10_building_rag_systems/notebooks/11_ai_research_assistant.ipynb) | Module lab: package ingestion, retrieval, structured answers and session history into one research-assistant class | RAG production course |

## 11 — [Multimodal RAG](../modules/11_multimodal_rag/README.md)

Retrieval over documents that contain images: CLIP-style multimodal embeddings, image captioning and ColPali page retrieval.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_multimodal_rag_with_clip.ipynb](../modules/11_multimodal_rag/notebooks/01_multimodal_rag_with_clip.ipynb) | Embed PDF text and images in one space with CLIP and answer with a multimodal LLM | RAG Demystified tracks |
| [02_multimodal_rag_with_captioning.ipynb](../modules/11_multimodal_rag/notebooks/02_multimodal_rag_with_captioning.ipynb) | Caption PDF images with a Gemini vision model and index captions alongside text (Cohere embeddings) | RAG Techniques anthology |
| [03_multimodal_rag_with_colpali.ipynb](../modules/11_multimodal_rag/notebooks/03_multimodal_rag_with_colpali.ipynb) | Retrieve whole PDF pages as images with ColPali | RAG Techniques anthology |

## 12 — [LangChain RAG Implementations](../modules/12_langchain_rag_implementations/README.md)

LangChain-specific retrieval features on PGVector: metadata-filtered search and the Indexing API with a record manager.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_filtered_search_pgvector.ipynb](../modules/12_langchain_rag_implementations/notebooks/01_filtered_search_pgvector.ipynb) | Combine semantic search with metadata filters on PGVector | RAG Demystified tracks |
| [02_indexing_api.ipynb](../modules/12_langchain_rag_implementations/notebooks/02_indexing_api.ipynb) | Keep a vector store in sync with its sources using the LangChain Indexing API and a record manager | RAG Demystified tracks |

## 13 — [LlamaIndex RAG Implementations](../modules/13_llamaindex_rag/README.md)

The same foundational techniques (simple RAG, CSV RAG, fusion retrieval, reranking, context windows) implemented with LlamaIndex.

| Notebook | Learning objective | Source |
|---|---|---|
| [01_simple_rag_with_llamaindex.ipynb](../modules/13_llamaindex_rag/notebooks/01_simple_rag_with_llamaindex.ipynb) | Build a simple PDF RAG pipeline with LlamaIndex and FAISS | RAG Techniques anthology |
| [02_simple_csv_rag_with_llamaindex.ipynb](../modules/13_llamaindex_rag/notebooks/02_simple_csv_rag_with_llamaindex.ipynb) | Build a CSV RAG pipeline with LlamaIndex | RAG Techniques anthology |
| [03_fusion_retrieval_with_llamaindex.ipynb](../modules/13_llamaindex_rag/notebooks/03_fusion_retrieval_with_llamaindex.ipynb) | Fuse vector and BM25 retrieval with LlamaIndex's QueryFusionRetriever | RAG Techniques anthology |
| [04_reranking_with_llamaindex.ipynb](../modules/13_llamaindex_rag/notebooks/04_reranking_with_llamaindex.ipynb) | Rerank with LLM and cross-encoder postprocessors in LlamaIndex | RAG Techniques anthology |
| [05_context_enrichment_window_with_llamaindex.ipynb](../modules/13_llamaindex_rag/notebooks/05_context_enrichment_window_with_llamaindex.ipynb) | Sentence-window retrieval with LlamaIndex | RAG Techniques anthology |
