# Prerequisites

This repository assumes knowledge, never code, from earlier repositories. Nothing here imports a file, package or dataset from another course repository.

| From | What you should already know | Where it is taught |
|---|---|---|
| 01 Foundations | Python (functions, classes, decorators, `asyncio` basics), `.env` files, calling a chat-completions API | [repository 01](https://github.com/Sourav692/ai-engineering-demystified-01-foundations) |
| 02 Prompt and context engineering | System prompts, structured prompting, context-window budgeting | [repository 02](https://github.com/Sourav692/ai-engineering-demystified-02-prompt-context-engineering) |
| 03 LangChain fundamentals | Chat models, messages, prompt templates, output parsers, `with_structured_output`, Runnables and LCEL | [repository 03](https://github.com/Sourav692/ai-engineering-demystified-03-langchain-fundamentals) |
| 04 LangGraph fundamentals | `StateGraph`, reducers, `MessagesState`, conditional edges, `Command`, subgraphs, `Send`, checkpointers, `interrupt()`, streaming | [repository 04](https://github.com/Sourav692/ai-engineering-demystified-04-langgraph-fundamentals) |
| 05 Retrieval and RAG | Embeddings, vector stores and a basic retriever (a few builds include a RAG agent) | [repository 05](https://github.com/Sourav692/ai-engineering-demystified-05-retrieval-rag) |
| 06 Agent fundamentals | The agent loop, tool calling, ReAct agents (`create_agent` / LangGraph), workflow patterns, planning and reflection | [repository 06](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals) |
| 07 First-party agent SDKs (optional) | How a provider SDK models an agent, tools and handoffs | [repository 07](https://github.com/Sourav692/ai-engineering-demystified-07-first-party-agent-sdks) |

## Quick self-check

- Can you build a ReAct agent that calls two tools and explain each message in its loop?
- Can you compile a LangGraph graph with a checkpointer and resume it with a `thread_id`?
- Can you write a node that returns `Command(goto=..., update=...)`, and a reducer that appends to a list?

If any answer is "no", revisit the linked repository first — the lessons here build on those mechanics without re-teaching them.
