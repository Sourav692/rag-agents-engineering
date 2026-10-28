# Prerequisites

This repository assumes knowledge, not code, from earlier repositories. Nothing here imports from another repository.

## You should know

- **Python and notebooks** — functions, f-strings, lists and dicts; running cells in Jupyter; installing packages into a virtual environment.
- **Calling an LLM API** — creating a client with an API key, sending a chat message, and reading the text of the reply. Covered in [repository 01 (foundations)](https://github.com/Sourav692/ai-engineering-demystified-01-foundations).
- **Basic model vocabulary** — tokens, context window, temperature, and the difference between a hosted model and an open-weight one.

## You do not need

- LangChain. Modules 01 and 02 send prompts through LangChain's `ChatOpenAI`, but only as a thin client; the framework itself is taught in [repository 03](https://github.com/Sourav692/ai-engineering-demystified-03-langchain-fundamentals).
- Any agent or retrieval background.

## Accounts and keys

API keys for the providers you want to try: OpenAI, Google AI Studio (Gemini), Groq, and a Hugging Face access token with access to `meta-llama/Llama-3.2-1B-Instruct`. Every notebook runs against one or two providers, so you can work through the modules whose keys you have. Running the notebooks makes paid API calls; `uv run pytest` does not.
