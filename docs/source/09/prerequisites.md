# Prerequisites

This repository assumes the following as *knowledge*. Nothing here imports code, data or environments from another repository — each earlier repository is listed so you know where the concept is taught.

| You should be comfortable with | Taught in |
|---|---|
| Python, notebooks, `.env` files and calling an LLM provider API | [repository 01 (foundations)](https://github.com/Sourav692/ai-engineering-demystified-01-foundations) |
| Writing prompts and structured-output prompts (graders in this repo are prompts that return a score) | [repository 02 (prompt and context engineering)](https://github.com/Sourav692/ai-engineering-demystified-02-prompt-context-engineering) |
| LangChain models, messages, prompt templates, output parsers and LCEL composition | [repository 03 (LangChain fundamentals)](https://github.com/Sourav692/ai-engineering-demystified-03-langchain-fundamentals) |
| LangGraph state, nodes, conditional edges, checkpointers and interrupts | [repository 04 (LangGraph fundamentals)](https://github.com/Sourav692/ai-engineering-demystified-04-langgraph-fundamentals) |
| The standard RAG pipeline: loading, chunking, embeddings, vector stores, retrievers, query transformation and reranking | [repository 05 (retrieval and RAG)](https://github.com/Sourav692/ai-engineering-demystified-05-retrieval-rag) |
| Tool calling, the agent loop and ReAct | [repository 06 (agent fundamentals)](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals) |
| Agent memory and multi-agent systems (helpful for the later modules, not required) | [repository 08 (advanced agent systems)](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems) |

## Quick self-check

Before module 01 you should be able to:

1. Build a basic retrieve-then-generate chain over a PDF with a vector store (repository 05).
2. Write a LangGraph graph with a conditional edge that loops back to an earlier node (repository 04).
3. Explain what happens when an LLM decides to call a tool (repository 06).

Module 09 (knowledge graphs) additionally uses a little Cypher; the first notebook introduces it.
