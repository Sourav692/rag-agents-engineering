# Theory rewrite tracker

Progress of rewriting every module's theory pages in the M22 style (theory only, no code, project pages for notebook-only builds). The `course-content` skill updates this file whenever it creates, rewrites or reviews a module.

- **Lessons, Pages, New style**: computed by `.claude/skills/course-content/scripts/tracker.py` from the repo.
- **Status**: `Not started` → `Review draft` (drafts shown, nothing applied) → `In progress` (pages being edited) → `In PR` → `Live` (merged and on forwarddeployedprep.com).
- **Updated, PRs, Notes**: set with `tracker.py --set <module> <status> [--pr '#N'] [--note '...']`.

**Modules:** Not started: 32 · Review draft: 0 · In progress: 0 · In PR: 13 · Live: 1

## Part I · AI Engineering Foundations

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | Python & Data Toolkit Refresher | 6 | 3 | 0 / 3 | Not started |  |  |  |
| 2 | LLM Provider APIs & Model Selection | 4 | 4 | 0 / 4 | Not started |  |  |  |
| 3 | Hugging Face Models & Gradio Demos | 5 | 3 | 0 / 3 | Not started |  |  |  |

## Part II · Prompt & Context Engineering

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 4 | Prompt Engineering Patterns | 4 | 4 | 0 / 4 | Not started |  |  |  |
| 5 | Multimodal Prompting | 3 | 3 | 0 / 3 | Not started |  |  |  |

## Part III · LLM Application Frameworks: LangChain & LangGraph

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 6 | LangChain Core: Models, Prompts & Parsers | 7 | 6 | 0 / 6 | Not started |  |  |  |
| 7 | LCEL, Runnables & Chains | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 8 | LangGraph Core: Graphs, State & Control Flow | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 9 | LangGraph Runtime: Persistence, HITL & Streaming | 6 | 6 | 0 / 6 | Not started |  |  |  |

## Part IV · RAG Foundations: Ingestion & Indexing

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 10 | Why RAG & the RAG Lifecycle | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 11 | Document Ingestion & Metadata Design | 6 | 5 | 0 / 5 | Not started |  |  |  |
| 12 | Chunking Strategies | 4 | 4 | 0 / 4 | Not started |  |  |  |
| 13 | Embeddings & Model Selection | 5 | 4 | 0 / 4 | Not started |  |  |  |
| 14 | Vector Stores & Index Operations | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 15 | Advanced Indexing Strategies | 5 | 5 | 0 / 5 | Not started |  |  |  |

## Part V · Retrieval Quality & RAG Applications

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 16 | Retrievers & Hybrid Search | 6 | 6 | 6 / 6 | In PR | 2026-11-09 | #45 | All lessons in new style |
| 17 | Query Transformation & Routing | 8 | 8 | 8 / 8 | In PR | 2026-11-09 | #45 | All 8 lessons in new style; 17.1 diagram labels read 18.x (protected) |
| 18 | Post-Retrieval Optimisation & Reranking | 6 | 6 | 6 / 6 | In PR | 2026-11-09 | #45 | All 6 lessons in new style; 06a KITE per-dataset table inconsistent, only averages quoted |
| 19 | End-to-End RAG Systems | 5 | 5 | 5 / 5 | In PR | 2026-11-09 | #45 | All lessons in new style |
| 20 | Multimodal RAG | 3 | 3 | 3 / 3 | In PR | 2026-11-09 | #45 | All lessons in new style |
| 21 | Framework Fluency: LlamaIndex | 4 | 4 | 4 / 4 | In PR | 2026-11-09 | #45 | All lessons in new style |

## Part VI · Agent Foundations

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 22 | The Agent Loop & Tool Calling | 6 | 6 | 6 / 6 | Live | 2026-11-09 | #39 #40 #41 | Rewritten; 22.1 trimmed; 22.2 is a project page |
| 23 | ReAct Agents & LangChain create_agent | 5 | 5 | 5 / 5 | In PR | 2026-11-09 | #43 | 23.1-23.4 rewritten; 23.5 project page added |
| 24 | Agentic Workflow Patterns | 5 | 5 | 5 / 5 | In PR | 2026-11-09 | #43 | All 5 pages rewritten |

## Part VII · Advanced Agents

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 25 | Planning, Reflection & Reasoning Patterns | 7 | 3 | 0 / 3 | Not started |  |  |  |
| 26 | Coding, Computer-Use & Deep Agents | 3 | 2 | 0 / 2 | Not started |  |  |  |
| 27 | Human Approval & Applied Single-Agent Builds | 5 | 3 | 0 / 3 | Not started |  |  |  |

## Part VIII · Agentic RAG

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 28 | Agentic RAG Foundations: Grading & Query Rewriting | 3 | 3 | 3 / 3 | In PR | 2026-11-09 | #47 | All 3 pages rewritten; 28.2 new platform page (site slug neutral) |
| 29 | Self-Correcting RAG: CRAG & Self-RAG | 3 | 3 | 3 / 3 | In PR | 2026-11-09 | #47 | All 3 pages rewritten; 29.3 k=3 means fixed (4.6, 13.4) |
| 30 | Adaptive RAG & Query Routing | 4 | 4 | 4 / 4 | In PR | 2026-11-09 | #47 | All 4 pages rewritten; 30.2 form fields fixed |
| 31 | RAG as an Agent Tool | 3 | 3 | 3 / 3 | In PR | 2026-11-09 | #47 | All 3 pages rewritten; lab results still pending |
| 32 | Reliability, Feedback Loops & Diversity | 3 | 3 | 3 / 3 | In PR | 2026-11-09 | #47 | All 3 pages rewritten; MMR ref fixed to 16.4 |

## Part IX · The Memory Layer

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 33 | Short-Term Memory & Conversation State | 6 | 5 | 0 / 5 | Not started |  |  |  |
| 34 | Long-Term & Agentic Memory | 5 | 5 | 0 / 5 | Not started |  |  |  |

## Part X · Multi-Agent Systems

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 35 | Multi-Agent Architectures | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 36 | Collaboration, Control & Parallel Agents | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 37 | Multi-Agent Applied Builds | 5 | 4 | 0 / 4 | Not started |  |  |  |

## Part XI · Agent Protocols: MCP & A2A

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 38 | MCP Foundations | 7 | 6 | 0 / 6 | Not started |  |  |  |
| 39 | Building MCP Servers & Clients | 6 | 4 | 0 / 4 | Not started |  |  |  |
| 40 | MCP Applications & RAG over MCP | 7 | 7 | 0 / 7 | Not started |  |  |  |
| 41 | A2A: Agent-to-Agent Protocol | 4 | 4 | 0 / 4 | Not started |  |  |  |

## Part XII · Knowledge Graphs & GraphRAG

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 42 | Hierarchical & Memory-Augmented Retrieval | 3 | 3 | 0 / 3 | Not started |  |  |  |
| 43 | Knowledge Graphs with Neo4j | 6 | 6 | 0 / 6 | Not started |  |  |  |
| 44 | GraphRAG Techniques | 4 | 4 | 0 / 4 | Not started |  |  |  |

## Part XIII · Fine-Tuning & Model Adaptation

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 45 | Fine-Tuning & Model Adaptation | 7 | 7 | 0 / 7 | Not started |  |  |  |

## Part XIV · Architecture Decisions

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 46 | Architecture Synthesis: Choosing a System Design | 3 | 3 | 0 / 3 | Not started |  |  |  |
