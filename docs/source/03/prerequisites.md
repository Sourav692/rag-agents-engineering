# Prerequisites

This repository assumes *knowledge*, not code, from earlier repositories. Nothing here imports files or packages from another course repository.

| You should know | Where it is taught |
|---|---|
| Python 3.12, virtual environments, `uv`, running Jupyter notebooks | [Repository 01 — foundations](https://github.com/Sourav692/ai-engineering-demystified-01-foundations) |
| Calling an LLM provider API directly (OpenAI, Gemini, Groq, Hugging Face) with keys loaded from `.env` | [Repository 01 — foundations](https://github.com/Sourav692/ai-engineering-demystified-01-foundations) |
| Prompt design: roles, instructions, few-shot examples, asking for a specific output format | [Repository 02 — prompt and context engineering](https://github.com/Sourav692/ai-engineering-demystified-02-prompt-context-engineering) |
| Basic Pydantic models and type hints | General Python background |

## Quick self-check

- Can you explain the difference between a system message and a user message?
- Can you write a Pydantic `BaseModel` with typed, described fields?
- Can you load `OPENAI_API_KEY` from a `.env` file with `python-dotenv`?

If yes, start with [module 01](../modules/01_getting_started/).
