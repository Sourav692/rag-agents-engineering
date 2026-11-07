# Lesson coverage: optional and notebook-only lessons

A snapshot of which lessons in `curriculum.yaml` are optional, and which have no theory page. Taken on 8 November 2026, after the Phase 6 switch to the part folders, in v2 lesson numbers.

## Definitions

- **Optional lesson:** none of its notebooks has tier `mandatory`. Its notebooks are `extension` (extra practice and refreshers), `alternate` (the same idea from another source or API) or `platform` (tied to one platform, such as Databricks). Its theory page, when it has one, sits in the module's `optional/theory/` folder.
- **Notebook-only lesson:** the lesson has no theory page (`<part>/<module>/<tier>/theory/<NN>_<lesson>/README.md`). Its module page lists it as *planned*, and the site shows its notebooks only.
- The `theory-module` skill leaves a lesson *planned* when it has nothing to teach beyond its notebook, because each module concept goes on exactly one lesson page (`.claude/skills/theory-module/SKILL.md`).

## Summary

| Group | Lessons |
|---|---|
| Mandatory but notebook-only | 7 |
| Optional and notebook-only | 19 |
| Optional with a theory page | 23 |
| Theory-only, with no notebooks | 3 |

Notebook-only lessons: 26. Optional lessons: 42.

## 1. Mandatory but notebook-only

These lessons are on the required path but have no theory page. They are the main coverage gap.

| Lesson | Title | Module | Optional tiers | Notebooks |
|---|---|---|---|---|
| 6.3 | Open-source LLMs: Transformers, Inference Client, Groq, LangChain | M06 LangChain Core: Models, Prompts & Parsers | alternate | 4 |
| 17.2 | Multi-query retrieval | M17 Query Transformation & Routing | alternate | 3 |
| 17.4 | Step-back prompting | M17 Query Transformation & Routing | none | 1 |
| 17.8 | Self-querying: natural language to metadata filter | M17 Query Transformation & Routing | none | 1 |
| 25.2 | Deep-research and reflective dynamic planners | M25 Planning, Reflection & Reasoning Patterns | extension | 2 |
| 25.3 | Reflection and Reflexion agents | M25 Planning, Reflection & Reasoning Patterns | alternate | 3 |
| 27.2 | Research and competitive-intelligence agents | M27 Human Approval & Applied Single-Agent Builds | extension | 2 |

The tiers column lists the lesson's optional notebooks beside its mandatory ones.

## 2. Optional and notebook-only

| Lesson | Title | Module | Optional tiers | Notebooks |
|---|---|---|---|---|
| 1.1 | Python essentials: variables, operators, control flow, functions | M01 Python & Data Toolkit Refresher | extension | 5 |
| 1.2 | Python best practices | M01 Python & Data Toolkit Refresher | extension | 1 |
| 1.5 | Serving data with Flask APIs | M01 Python & Data Toolkit Refresher | extension | 2 |
| 3.3 | Images, diffusion and video generation | M03 Hugging Face Models & Gradio Demos | extension, platform | 5 |
| 3.4 | Audio: data, classification, transcription, generation | M03 Hugging Face Models & Gradio Demos | extension | 4 |
| 11.2 | Plain text and Markdown (single vs element mode) | M11 Document Ingestion & Metadata Design | extension | 2 |
| 13.5 | Benchmarking embedding models with MLflow (Databricks) | M13 Embeddings & Model Selection | platform | 1 |
| 22.2 | A real-world agent on raw API calls (Hacker News chatbot) | M22 The Agent Loop & Tool Calling | extension | 1 |
| 23.5 | Exercise: intelligent travel assistant agent (with solution) | M23 ReAct Agents & LangChain create_agent | extension | 2 |
| 25.5 | Self-Discover and reflective code generation | M25 Planning, Reflection & Reasoning Patterns | extension | 2 |
| 25.7 | Simulator-in-the-loop, metacognition and exemplar memory | M25 Planning, Reflection & Reasoning Patterns | extension | 3 |
| 26.2 | Developer vs tester agents | M26 Coding, Computer-Use & Deep Agents | extension | 1 |
| 27.3 | Financial analyst agent | M27 Human Approval & Applied Single-Agent Builds | extension | 1 |
| 28.2 | The same agent on Databricks Vector Search | M28 Agentic RAG Foundations: Grading & Query Rewriting | platform | 1 |
| 33.5 | Memory apps: product recommender and research agent with SQL memory | M33 Short-Term Memory & Conversation State | extension | 2 |
| 37.5 | Five practical agent patterns, side by side (theory page on hold) | M37 Multi-Agent Applied Builds | extension | 5 |
| 38.7 | Labs: Wikipedia assistant with tools, resources and prompts | M38 MCP Foundations | extension | 3 |
| 39.3 | An MCP server as a Databricks App | M39 Building MCP Servers & Clients | platform | 1 |
| 39.6 | Licence and references for the client projects | M39 Building MCP Servers & Clients | extension | 2 |

## 3. Optional with a theory page

| Lesson | Title | Module | Optional tiers | Notebooks |
|---|---|---|---|---|
| 1.6 | Concurrency: threads, processes, the GIL and asyncio (22 runnable scripts) | M01 Python & Data Toolkit Refresher | extension | 1 |
| 5.2 | Multimodal prompting with GPT-4o | M05 Multimodal Prompting | alternate | 1 |
| 5.3 | Exercise: financial report analysis | M05 Multimodal Prompting | extension | 1 |
| 11.3 | Semi-structured sources: CSV rows and JSON / JSONL with jq schemas | M11 Document Ingestion & Metadata Design | extension | 2 |
| 18.6 | Relevant segment extraction | M18 Post-Retrieval Optimisation & Reranking | extension | 1 |
| 20.3 | Page-image retrieval with ColPali | M20 Multimodal RAG | platform | 1 |
| 27.5 | LLM workflow apps: review analyst, IT support desk, tailored writer, quiz generator | M27 Human Approval & Applied Single-Agent Builds | extension | 4 |
| 30.2 | Customer-facing routing with sentiment and human escalation | M30 Adaptive RAG & Query Routing | alternate | 1 |
| 31.2 | Managed RAG platforms: Contextual AI | M31 RAG as an Agent Tool | platform | 1 |
| 31.3 | Exercise: LlamaIndex Wikipedia agent with Chainlit | M31 RAG as an Agent Tool | extension | 1 |
| 32.3 | Dartboard RAG: relevance and diversity together | M32 Reliability, Feedback Loops & Diversity | extension | 1 |
| 35.3 | Supervisor workflow with human review | M35 Multi-Agent Architectures | extension | 1 |
| 36.2 | Debate | M36 Collaboration, Control & Parallel Agents | extension | 1 |
| 36.4 | Meta-controllers, ensembles and emergent systems | M36 Collaboration, Control & Parallel Agents | extension | 3 |
| 37.3 | Scaling: parallel agents, memory merging, language and sentiment, web search | M37 Multi-Agent Applied Builds | extension | 4 |
| 40.2 | MCP servers with Claude Desktop | M40 MCP Applications & RAG over MCP | platform | 1 |
| 40.3 | MCP servers for data analysis | M40 MCP Applications & RAG over MCP | extension | 1 |
| 40.7 | Deploying an MCP server on EC2 | M40 MCP Applications & RAG over MCP | platform | 1 |
| 42.2 | MemoRAG: global memory and clue-guided retrieval | M42 Hierarchical & Memory-Augmented Retrieval | extension | 1 |
| 44.2 | Local GraphRAG with source attribution | M44 GraphRAG Techniques | extension | 1 |
| 44.4 | Graph expansion inside a vector database (Milvus) | M44 GraphRAG Techniques | platform | 1 |
| 45.2 | Where fine-tuning fits | M45 Fine-Tuning & Model Adaptation | alternate, extension | 2 |
| 45.7 | Fine-tuning Llama 2 with AutoTrain | M45 Fine-Tuning & Model Adaptation | platform | 1 |

## 4. Theory-only, with no notebooks

These lessons are taught on the theory page alone, so they are neither optional nor notebook-only.

| Lesson | Title | Module |
|---|---|---|
| 10.1 | The knowledge problem: hallucination, freshness, context-window growth, RAG vs fine-tuning vs long context | M10 Why RAG & the RAG Lifecycle |
| 29.3 | Trade-offs: when correction is worth the extra calls | M29 Self-Correcting RAG: CRAG & Self-RAG |
| 46.3 | Decision framework: picking the simplest architecture that works | M46 Architecture Synthesis: Choosing a System Design |

## Regenerating

This file is written by hand and is not updated by `scripts/build_curriculum.py`. To refresh it, recount from `curriculum.yaml` with `lesson_pages()` and `lesson_tier()` in `scripts/curriculum_lib.py`.
