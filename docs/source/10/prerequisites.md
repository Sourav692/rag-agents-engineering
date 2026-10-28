# Prerequisites

This repository assumes the following as *knowledge*. Nothing here imports code, data or environments from another repository. Each earlier repository is listed so you know where the concept is taught.

| You should be comfortable with | Taught in |
|---|---|
| Python, notebooks, `.env` files and calling an LLM provider API | [repository 01 (foundations)](https://github.com/Sourav692/ai-engineering-demystified-01-foundations) |
| Writing system prompts and prompt templates (MCP prompts are server-side templates) | [repository 02 (prompt and context engineering)](https://github.com/Sourav692/ai-engineering-demystified-02-prompt-context-engineering) |
| LangChain chat models, messages and tools | [repository 03 (LangChain fundamentals)](https://github.com/Sourav692/ai-engineering-demystified-03-langchain-fundamentals) |
| LangGraph graphs and prebuilt agents (several MCP clients and the A2A notebooks use them) | [repository 04 (LangGraph fundamentals)](https://github.com/Sourav692/ai-engineering-demystified-04-langgraph-fundamentals) |
| Tool calling, the agent loop and ReAct. MCP standardises exactly this tool layer | [repository 06 (agent fundamentals)](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals) |
| Google ADK basics (used by one MCP client and the capstone; helpful, not required) | [repository 07 (first-party agent SDKs)](https://github.com/Sourav692/ai-engineering-demystified-07-first-party-agent-sdks) |
| Agentic RAG: grading, multi-candidate retrieval, answer ranking (for the module 05 capstone only) | [repository 09 (advanced RAG)](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag) |

Tooling: a terminal, `uv`, and for some sub-projects Node.js (`npx` for MCP Inspector and third-party servers), Docker (module 03 lab 2) and Ollama (module 04).

## Quick self-check

Before module 01 you should be able to:

1. Explain what happens when an LLM decides to call a tool, and who actually executes it (repository 06).
2. Run a Python script with environment variables loaded from `.env`, and run a notebook with `uv run jupyter lab`.
3. Start a local HTTP server and call it with `curl` or `httpx`.
