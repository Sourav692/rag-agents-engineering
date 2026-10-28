# Prerequisites

This repository assumes knowledge, never code, from earlier repositories. Nothing here imports a file, package or dataset from another course repository.

| From | What you should already know | Where it is taught |
|---|---|---|
| 01 Foundations | Python (functions, classes, decorators, `asyncio` basics), `.env` files, calling a chat-completions API, choosing a model | [repository 01](https://github.com/Sourav692/ai-engineering-demystified-01-foundations) |
| 02 Prompt and context engineering | System prompts, few-shot and structured prompting, asking for JSON | [repository 02](https://github.com/Sourav692/ai-engineering-demystified-02-prompt-context-engineering) |
| 03 LangChain fundamentals | Chat models, messages, prompt templates, output parsers, `with_structured_output`, Runnables and LCEL (`|`, `RunnablePassthrough`, `RunnableParallel`) | [repository 03](https://github.com/Sourav692/ai-engineering-demystified-03-langchain-fundamentals) |
| 04 LangGraph fundamentals | `StateGraph`, nodes, edges, reducers, `MessagesState`, conditional edges, checkpointers, `interrupt()` | [repository 04](https://github.com/Sourav692/ai-engineering-demystified-04-langgraph-fundamentals) |
| 05 Retrieval and RAG (recommended) | What a retriever and a vector store are | [repository 05](https://github.com/Sourav692/ai-engineering-demystified-05-retrieval-rag) |

## Quick self-check

- Can you write a LangGraph graph with a conditional edge that loops back to an earlier node?
- Can you explain what `bind_tools` returns and what a `ToolMessage` is?
- Can you turn a Pydantic model into a structured-output schema for a chat model?

If any answer is "no", revisit the linked repository first — the lessons here build on those mechanics without re-teaching them.
