# Prerequisites

This repository assumes knowledge, not code, from earlier repositories. Nothing here imports from another course repository.

## Knowledge you need

| Topic | Needed for | Where it is taught |
|---|---|---|
| Python type hints: `TypedDict`, `Annotated`, `Literal`, `dataclass` | Every state schema, from module 01 on | [Repository 01 — foundations](https://github.com/Sourav692/ai-engineering-demystified-01-foundations) |
| `async`/`await` and `asyncio` basics | Modules 09 and 12 | [Repository 01 — foundations](https://github.com/Sourav692/ai-engineering-demystified-01-foundations) |
| Pydantic `BaseModel` | Module 03 | [Repository 01 — foundations](https://github.com/Sourav692/ai-engineering-demystified-01-foundations) |
| Writing a clear prompt | Any notebook that calls a model | [Repository 02 — prompt and context engineering](https://github.com/Sourav692/ai-engineering-demystified-02-prompt-context-engineering) |
| LangChain chat models, message types, `RunnableConfig` | Modules 01–02 onward | [Repository 03 — LangChain fundamentals](https://github.com/Sourav692/ai-engineering-demystified-03-langchain-fundamentals) |

## Things some notebooks touch before they are formally taught

A few notebooks use a tool-calling model or `ToolNode` as the *example workload* while teaching a graph mechanic — `bind_tools` in modules 06 (HITL patterns), 08 and 09, and `create_react_agent` in module 06. You only need to follow what the call does; tools, function calling and the agent loop are taught properly in [repository 06 — agent fundamentals](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals).

## Accounts

A key for one chat-model provider is enough for every notebook that needs a model; see [setup.md](setup.md). Ten notebooks need no key at all.
