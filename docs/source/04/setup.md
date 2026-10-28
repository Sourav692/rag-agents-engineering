# Setup

## Install

```bash
uv sync                    # Python 3.12 venv in .venv/, all notebook dependencies, dev tools, and aied-helpers
cp .env.example .env
uv run nbstripout --install --attributes .gitattributes   # once per clone: strip notebook outputs on `git add`
uv run pre-commit install  # once per clone: run the checks on commit
uv run pytest              # offline: notebook structure, links, compile + import smoke test
uv run jupyter lab
```

There is one supported Python version (3.12) and one dependency set; `uv.lock` pins every package. No optional dependency groups are needed.

The nbstripout git filter strips outputs from the copy git stores; your working copy keeps its outputs. The filter command lives in `.git/config` and points at this clone's `.venv`, so run `uv sync` before `git add`-ing notebooks if you recreate `.venv`.

### Without uv sync: requirements.txt

`requirements.txt` is generated from `uv.lock` for tools that need a flat list:

```bash
uv venv --python 3.12 && uv pip install -r requirements.txt
```

Regenerate it after any dependency change:

```bash
uv export --format requirements-txt --no-hashes --no-dev --no-emit-project -o requirements.txt
```

## The LLM factory: `aied-helpers`

Every notebook that calls a chat model creates it with the shared course package [`aied-helpers`](https://github.com/Sourav692/ai-engineering-demystified-shared) (pinned to tag `v0.1.0` in `pyproject.toml`):

```python
from aied_helpers import get_openai_llm
llm = get_openai_llm(model="gpt-4o-mini")
```

| Function | Provider | Reads |
|---|---|---|
| `get_openai_llm(model=..., temperature=...)` | OpenAI (the course default, `gpt-4o-mini`) | `OPENAI_API_KEY` |
| `get_groq_llm(...)` | Groq (first `uv add langchain-groq`) | `GROQ_API_KEY` |
| `get_databricks_llm(model=...)` | Databricks AI Gateway | `DATABRICKS_HOST`, `DATABRICKS_TOKEN` |
| `get_openrouter_llm(...)`, `get_llm(...)` | OpenRouter | `OPENROUTER_API_KEY` |
| `get_experientiallabs_llm(...)` | Experiential Labs OpenAI-compatible endpoint | `EXPERIENTIALLABS_API_KEY` |

To use a different provider, change the one LLM line in the notebook's setup cell and set that provider's key.

## Keys per notebook

Each module README has a "Keys needed" column. Summary:

- **No key:** module 01 (`02_MessagesState`), module 02 (`01_Conditional_Routing`), all of modules 03 and 04, module 06 (`01_HITL_Mechanics`), module 10, module 12. Module 01's `01_State_and_Graph_Basics` needs a key only for its final LLM section.
- **`OPENAI_API_KEY`:** modules 01 (LLM section), 02 (chatbot), 05, 06 (`02_LangGraph_Interrupt_Primitive`, `03_HITL_Patterns`), 07, 08, 09, 11.

## Files notebooks create

- Module 11 writes `graph_code.png` next to the notebook (the rendered graph).
- Module 05 writes its SQLite checkpoint database to a temporary directory; module 12 writes `/tmp/agent_ck.db`.

None of these are committed; `.gitignore` covers the usual runtime output.

## Graph diagrams need network access

`graph.get_graph().draw_mermaid_png()` sends the diagram to the public mermaid.ink service to render it. Offline, or if mermaid.ink is down, that cell raises an error; nothing else in the notebook depends on the image. To see the same graph without the network, print its Mermaid source instead:

```python
print(graph.get_graph().draw_mermaid())
```

Paste the output into any Mermaid viewer, or into a Markdown cell inside a ```` ```mermaid ```` block (JupyterLab 4.1+ renders it).
