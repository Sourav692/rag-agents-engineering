# Theory rewrite tracker

Progress of rewriting every module's theory pages in the M22 style (theory only, no code, project pages for notebook-only builds). The `course-content` skill updates this file whenever it creates, rewrites or reviews a module.

- **Lessons, Pages, New style**: computed by `.claude/skills/course-content/scripts/tracker.py` from the repo.
- **Status**: `Not started` → `Review draft` (drafts shown, nothing applied) → `In progress` (pages being edited) → `In PR` → `Live` (merged and on forwarddeployedprep.com).
- **Updated, PRs, Notes**: set with `tracker.py --set <module> <status> [--pr '#N'] [--note '...']`.

**Modules:** Not started: 30 · Review draft: 3 · In progress: 0 · In PR: 3 · Live: 10

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
| 6 | LangChain Core: Models, Prompts & Parsers | 7 | 7 | 0 / 7 | Not started |  |  |  |
| 7 | LCEL, Runnables & Chains | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 8 | LangGraph Core: Graphs, State & Control Flow | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 9 | LangGraph Runtime: Persistence, HITL & Streaming | 6 | 6 | 0 / 6 | Not started |  |  |  |

## Part IV · RAG Foundations: Ingestion & Indexing

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 10 | Why RAG & the RAG Lifecycle | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 11 | Document Ingestion & Metadata Design | 6 | 6 | 0 / 6 | Not started |  |  |  |
| 12 | Chunking Strategies | 4 | 4 | 0 / 4 | Not started |  |  |  |
| 13 | Embeddings & Model Selection | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 14 | Vector Stores & Index Operations | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 15 | Advanced Indexing Strategies | 5 | 5 | 0 / 5 | Not started |  |  |  |

## Part V · Retrieval Quality & RAG Applications

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 16 | Retrievers & Hybrid Search | 6 | 6 | 0 / 6 | Not started |  |  |  |
| 17 | Query Transformation & Routing | 8 | 8 | 0 / 8 | Not started |  |  |  |
| 18 | Post-Retrieval Optimisation & Reranking | 6 | 6 | 0 / 6 | Not started |  |  |  |
| 19 | End-to-End RAG Systems | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 20 | Multimodal RAG | 3 | 3 | 0 / 3 | Not started |  |  |  |
| 21 | Framework Fluency: LlamaIndex | 4 | 4 | 0 / 4 | Not started |  |  |  |

## Part VI · Agent Foundations

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 22 | The Agent Loop & Tool Calling | 6 | 6 | 0 / 6 | Not started |  |  |  |
| 23 | ReAct Agents & LangChain create_agent | 5 | 5 | 0 / 5 | Not started |  |  |  |
| 24 | Agentic Workflow Patterns | 5 | 5 | 0 / 5 | Not started |  |  |  |

## Part VII · Advanced Agents

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 25 | Planning, Reflection & Reasoning Patterns | 7 | 7 | 0 / 7 | Review draft | 2026-11-13 |  | 25.1 to 25.7 and overview rewritten; HTML: site-export/part-vii-advanced-agents/index.html; structural/browser checks passed; source application pending. |
| 26 | Coding, Computer-Use & Deep Agents | 3 | 3 | 0 / 3 | Review draft | 2026-11-13 |  | 26.1 to 26.3 and overview rewritten; HTML: site-export/part-vii-advanced-agents/index.html; structural/browser checks passed; source application pending. |
| 27 | Human Approval & Applied Single-Agent Builds | 5 | 5 | 0 / 5 | Review draft | 2026-11-13 |  | 27.1 to 27.5 and overview rewritten; HTML: site-export/part-vii-advanced-agents/index.html; structural/browser checks and SQL fixture checks passed; source application pending. |

## Part VIII · Agentic RAG

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 28 | Agentic RAG Foundations: Grading & Query Rewriting | 3 | 3 | 3 / 3 | Live | 2026-11-13 | #67 | 28.1-28.3 approved format live 2026-11-13 (course #67, site #279 sync + architect estHours 377, site #278 interactive widgets); all 5 widgets verified live at 1280/390 |
| 29 | Self-Correcting RAG: CRAG & Self-RAG | 3 | 3 | 3 / 3 | Live | 2026-11-13 | #68 | 29.1-29.3 approved format; merged 5131dcf, site sync 26efccc (CI incl. bundle, routes, E2E pass), Vercel success, live pages checked 2026-11-13. |
| 30 | Adaptive RAG & Query Routing | 4 | 4 | 4 / 4 | Live | 2026-11-13 | #69 | Approved format; merged f165271; site PR #280 (sync + estHours ml-engineer 208, architect 376) merged 17eac2b, CI incl. bundle/routes/E2E pass, Vercel success, live pages checked 2026-11-13. |
| 31 | RAG as an Agent Tool | 3 | 3 | 3 / 3 | Live | 2026-11-13 | #69 | Approved format; merged f165271; site PR #280 (sync + estHours ml-engineer 208, architect 376) merged 17eac2b, CI incl. bundle/routes/E2E pass, Vercel success, live pages checked 2026-11-13. |
| 32 | Reliability, Feedback Loops & Diversity | 3 | 3 | 3 / 3 | Live | 2026-11-13 | #69 | Approved format; merged f165271; site PR #280 (sync + estHours ml-engineer 208, architect 376) merged 17eac2b, CI incl. bundle/routes/E2E pass, Vercel success, live pages checked 2026-11-13. |

## Part IX · The Memory Layer

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 33 | Short-Term Memory & Conversation State | 6 | 6 | 6 / 6 | Live | 2026-11-13 | #70 | Approved format; merged 2462879; site PR #281 (sync + estHours ml-engineer 209, architect 377) merged 6183d0b, CI incl. bundle/routes/E2E pass, Vercel success, live pages checked 2026-11-13. |
| 34 | Long-Term & Agentic Memory | 5 | 5 | 5 / 5 | Live | 2026-11-13 | #70 | Approved format; merged 2462879; site PR #281 (sync + estHours ml-engineer 209, architect 377) merged 6183d0b, CI incl. bundle/routes/E2E pass, Vercel success, live pages checked 2026-11-13. |

## Part X · Multi-Agent Systems

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 35 | Multi-Agent Architectures | 5 | 5 | 5 / 5 | Live | 2026-11-13 | #71 | Approved format; merged cff546a; site PR #282 (sync + estHours data-engineer 254, fde 298, fde-frontier-lab 328, 'ACM' in NOT_ACRONYMS) merged 406bad5, CI incl. bundle/routes/E2E pass, Vercel success, live pages checked 2026-11-13. |
| 36 | Collaboration, Control & Parallel Agents | 5 | 5 | 5 / 5 | Live | 2026-11-13 | #71 | Approved format; merged cff546a; site PR #282 (sync + estHours data-engineer 254, fde 298, fde-frontier-lab 328, 'ACM' in NOT_ACRONYMS) merged 406bad5, CI incl. bundle/routes/E2E pass, Vercel success, live pages checked 2026-11-13. |
| 37 | Multi-Agent Applied Builds | 5 | 5 | 5 / 5 | Live | 2026-11-13 | #71 | Approved format; merged cff546a; site PR #282 (sync + estHours data-engineer 254, fde 298, fde-frontier-lab 328, 'ACM' in NOT_ACRONYMS) merged 406bad5, CI incl. bundle/routes/E2E pass, Vercel success, live pages checked 2026-11-13. |

## Part XI · Agent Protocols: MCP & A2A

| # | Module | Lessons | Pages | New style | Status | Updated | PRs | Notes |
|---|---|---|---|---|---|---|---|---|
| 38 | MCP Foundations | 7 | 6 | 6 / 6 | In PR | 2026-11-14 | #73 | 38.1-38.6 approved format in PR #73; validator, browser, protect, pytest, links pass. 38.7 (extension labs) has no page. |
| 39 | Building MCP Servers & Clients | 6 | 4 | 4 / 4 | In PR | 2026-11-14 | #73 | 39.1, 39.2, 39.4, 39.5 approved format in PR #73; validator, browser, protect, pytest, links pass. 39.3 (site-hidden) and 39.6 (licence) have no page; 39.5 keeps the sentence the site text rule matches. |
| 40 | MCP Applications & RAG over MCP | 7 | 7 | 7 / 7 | In PR | 2026-11-14 | #73 | 40.1-40.7 approved format in PR #73; validator, browser, protect, pytest, links pass. |
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
