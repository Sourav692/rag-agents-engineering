# RAG with LlamaIndex

Exercise for module 05: a LlamaIndex ReAct agent that uses a `QueryEngineTool` over a Wikipedia index — RAG as an agent tool, outside LangGraph. Merged from [`LlamaIndex_Demystified`](https://github.com/Sourav692/LlamaIndex_Demystified); files that used to live under `RAG With LlamaIndex/` are in this folder.

> **In this repository** the two scaffolds ship as `chat_agent.py.txt` and `index_wikipages.py.txt`, because they are intentionally incomplete and do not compile until you fill them in. Copy each to its `.py` name before you start (for example `cp chat_agent.py.txt chat_agent.py`). The dependencies are in the `llamaindex` group: `uv sync --group llamaindex`.

# LlamaIndex Demystified

A hands-on learning project for building a **Retrieval-Augmented Generation (RAG)** chatbot using [LlamaIndex](https://www.llamaindex.ai/) and [Chainlit](https://chainlit.io/). The chatbot indexes Wikipedia pages on demand and answers questions about them using a ReAct agent powered by OpenAI.

## Architecture

```
User ──▶ Chainlit UI ──▶ ReAct Agent (OpenAI LLM)
                              │
                              ▼
                      QueryEngineTool
                              │
                              ▼
                    LlamaIndex Vector Index
                              │
                              ▼
                     Wikipedia Documents
```

1. The user selects a model and provides Wikipedia page topics through the Chainlit settings panel.
2. The app fetches and indexes those Wikipedia pages into a LlamaIndex vector store.
3. A ReAct agent is created with a `QueryEngineTool` backed by the index.
4. The user asks natural-language questions and the agent retrieves relevant context to generate answers.

## Project Structure

```
LlamaIndex_Demystified/
├── README.md
└── RAG With LlamaIndex/
    ├── chat_agent.py        # Chainlit chat app with ReAct agent (exercise)
    ├── index_wikipages.py   # Wikipedia page indexing pipeline (exercise)
    ├── utils.py             # API key loader from apikeys.yml
    ├── welcome.py           # Terminal welcome message
    ├── config.toml          # Chainlit configuration
    └── chainlit.md          # In-app user instructions
```

## Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/LlamaIndex_Demystified.git
   cd LlamaIndex_Demystified
   ```

2. **Install dependencies** (from the repository root)

   ```bash
   uv sync --group llamaindex
   ```

3. **Pick an LLM program for `index_wikipages.py`**

   The legacy `llama-index-program-openai` package does not support `llama-index-core` 0.14. Use
   `FunctionCallingProgram` (or `LLMTextCompletionProgram`) from `llama_index.core.program` instead.

4. **Configure your API key**

   Create a file at `apikeys.yml` in this folder (it is git-ignored):

   ```yaml
   openai:
     api_key: "sk-..."
   ```

   > **Warning:** Never commit this file. Add `apikeys.yml` to your `.gitignore`.

## Usage

1. Navigate to the project folder:

   ```bash
   cd modules/05_rag_as_an_agent_tool/exercises/llamaindex_wikipedia_agent
   ```

2. Launch the Chainlit app:

   ```bash
   chainlit run chat_agent.py -w
   ```

3. In the chat UI:
   - Open **Settings** (bottom-left icon).
   - Choose an OpenAI model.
   - Enter Wikipedia pages to index (e.g. `London, Barcelona, Paris`).
   - Save settings and wait for the indexing confirmation.
   - Ask questions about the indexed pages.

## How It Works

| Module | Responsibility |
|---|---|
| `utils.py` | Loads the OpenAI API key from `apikeys.yml` |
| `index_wikipages.py` | Converts a user query into a list of Wikipedia pages (via an LLM program + Pydantic model), fetches them, and builds a LlamaIndex vector index |
| `chat_agent.py` | Runs the Chainlit UI, manages settings, creates a ReAct agent with a `QueryEngineTool`, and streams answers back to the user |

## Exercise Format

The core files (`chat_agent.py` and `index_wikipages.py`) contain `# REPLACE THIS WITH YOUR CODE` placeholders. The goal is to implement the missing pieces to get a working RAG chatbot. Key concepts covered:

- Structured LLM output with Pydantic models
- Document loading from Wikipedia
- Vector index creation with LlamaIndex
- Building a ReAct agent with tool use
- Wiring everything into a Chainlit chat interface

## License

This project is provided for educational purposes.
