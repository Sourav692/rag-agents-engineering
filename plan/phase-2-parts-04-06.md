# Phase 2: v2 Parts IV to VI (M10 to M24)

Parts: `p04_rag_foundations`, `p05_retrieval_quality_and_rag_apps`, `p06_agent_foundations`. Depends only on [Phase 0](phase-0-foundations.md). Branch: `restructure/phase-2` (or `phase-2a` for Part IV and `phase-2b` for Parts V and VI).

Several briefs say "your Part V system" or "your Part V retriever". Each solution builds it inline: `lab_kit` chunks and a vector retriever over `larkspur/`, plus an answer prompt with citations, in one cell the solution says it reuses.

### Task 2.1: Restructure the three parts

Same steps as [Task 1.1](phase-1-parts-01-03.md#task-11-restructure-the-three-parts), for these three parts. Part VI loses lesson 24.5 to M26 and renumbers 24.6 to 23.5: check that `p06_agent_foundations/m23_react_agents/` has five lesson pages and that the travel-assistant files are `05a_*` and `05b_*`. Commit message: `content: copy v2 Parts IV to VI into the part-folder layout`.

### Tasks 2.2 to 2.16: one lab per module

Each row is one task. Follow the [lab recipe](README.md#lab-recipe-every-module-lab-task-follows-it). Every row uses `larkspur/` in `data/`; extra files are listed.

| Task | Module | Extra `data/` contents | Run with | The solution must show |
|---|---|---|---|---|
| 2.2 | M10 Why RAG & the RAG Lifecycle | none | default | the lifecycle of `05a_rag_lifecycle_and_baseline.ipynb` (load, split, embed, store, retrieve, generate) on the Larkspur handbook; retrieval metrics from `lab_kit` and answer correctness and faithfulness (LLM judge, prompt shown) on all 30 questions, refusals counted on the 5 `out_of_corpus` ones; results written to `solution/baseline.json` and committed as the course's reference baseline |
| 2.3 | M11 Document Ingestion & Metadata Design | `mixed/`: one small PDF and `Intel Strategy.docx` from `data/sample` (licence checked; else fictional Larkspur files), a Markdown file, a CSV, and one saved HTML page (a fictional Larkspur status page written for the lab) | default | each file loaded with the module's loaders into `Document`s that share `source, type, section, page, date`; documents per type and one printed metadata record per type; a schema check that fails if a key is missing |
| 2.4 | M12 Chunking Strategies | none | default | recursive, semantic and proposition chunking at three sizes each (nine indexes); hit rate (`lab_kit`) and answer faithfulness for each, against `lab_kit.baseline` |
| 2.5 | M13 Embeddings & Model Selection | none | `hf` group | one hosted model (`text-embedding-3-small`) and two open models (`all-MiniLM-L6-v2`, `BAAI/bge-small-en-v1.5`) on the 30 questions; hit rate, recall and MRR; measured seconds and computed cost per 1,000 chunks; a pick with the reason |
| 2.6 | M14 Vector Stores & Index Operations | `mixed/` (the M11 set, copied into this lab) | Docker | `solution/docker-compose.yml` for pgvector; ingestion with LangChain's `SQLRecordManager` and `index(..., cleanup="incremental")`; one file changed, one added, one deleted, with `num_added`, `num_updated`, `num_skipped`, `num_deleted` printed after each run |
| 2.7 | M15 Advanced Indexing Strategies | none | default | parent-document retrieval and contextual chunk headers each applied to the baseline; hit rate and answer quality before and after |
| 2.8 | M16 Retrievers & Hybrid Search | none | default | BM25 plus the vector retriever (`EnsembleRetriever`); fusion weights swept on the golden set with the best named; three queries only hybrid answers (if the golden set has fewer, add lab-local questions to `data/extra_questions.jsonl` and say so) |
| 2.9 | M17 Query Transformation & Routing | none | default | multi-query, RAG-Fusion, HyDE and decomposition on the 30 questions; per question type, which method helps and which hurts; added latency and cost per question |
| 2.10 | M18 Post-Retrieval Optimisation & Reranking | none | `hf` group | a cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) over a top-50 hybrid retrieval; hit rate and MRR at top 5 with and without it; reranking latency per query |
| 2.11 | M19 End-to-End RAG Systems | none | default | a `ResearchAssistant` class with ingestion, retrieval, a structured answer with citations, and session history; a three-turn session printed. The README links `mandatory/notebook/lab_ai_research_assistant.ipynb` as the reference build the solution follows |
| 2.12 | M20 Multimodal RAG | `report.pdf`: a short fictional Larkspur quarterly report drawn with matplotlib whose key numbers appear only in its charts; `questions.jsonl` (five questions, answers from the plotted data) | default | the three approaches the module teaches, each answering the five questions; which approach answers which |
| 2.13 | M21 Framework Fluency: LlamaIndex | none | `llamaindex` group | the hybrid plus rerank pipeline built inline in LangChain, then ported to LlamaIndex; hit rate and MRR from both on the 30 questions, with any gap explained |
| 2.14 | M22 The Agent Loop & Tool Calling | none | default | the retriever wrapped as a tool and run through a hand-written tool loop on raw API calls (no framework); every tool call and error logged and printed; one forced error (a bad argument) shown being handled |
| 2.15 | M23 ReAct Agents & LangChain create_agent | `off_topic.jsonl` (five questions outside the handbook's domain) | default; `TAVILY_API_KEY` | `create_agent` with the retriever and a web-search tool; a middleware that blocks off-topic questions; answers on 10 golden and the 5 off-topic questions compared with the inline Part V system |
| 2.16 | M24 Agentic Workflow Patterns | none | default | query decomposition (M17) rebuilt as orchestrator and workers, an answer-quality check rebuilt as evaluator and optimizer; latency and cost against the chain versions on 10 multi-hop and lookup questions |

### Task 2.17: Close the phase

Same steps as [Task 1.11](phase-1-parts-01-03.md#task-111-close-the-phase), adding `"p04_rag_foundations", "p05_retrieval_quality_and_rag_apps", "p06_agent_foundations"` to `DONE_PARTS`.
