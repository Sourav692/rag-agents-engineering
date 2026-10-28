# Setup

## 1. Install

```bash
uv sync                  # Python 3.12, the LangChain/LangGraph/RAG stack, the local helpers package and dev tools
cp .env.example .env     # names only; fill in the keys for the notebooks you plan to run
uv run pytest            # offline: notebook structure, links, and a smoke test; no API keys, no network
uv run jupyter lab
```

`uv sync` installs `src/helpers` in editable mode, so notebooks can `from helpers import get_llm,
get_embeddings, get_experientiallabs_llm` and `from helpers.utils import get_groq_llm, get_openai_llm,
get_databricks_llm`. Some notebooks still append a parent folder to `sys.path` before that import (a leftover of
the monorepo layout); it is harmless, the installed package is found either way. The knowledge-graph
lessons (module 09) used an older private copy of the same factory in the source; its three functions exist
with the same names in `src/helpers`, but `get_databricks_llm()` now goes through the Databricks AI Gateway
with a different default model.

## 2. Optional dependency groups

The default install stays light. Add a group only when a notebook needs it:

| Group | Command | What it adds | Used by |
|---|---|---|---|
| `graph` | `uv sync --group graph` | `neo4j`, `langchain-neo4j`, `pymilvus`, `spacy` + the `en_core_web_sm` model, `nltk`, `streamlit` | module 09, 10/01, 10/04 |
| `local-models` | `uv sync --group local-models` | `ollama` client, `sentence-transformers` (torch — large download) | 10/02 (also needs a running Ollama server) |
| `msgraphrag` | `uv sync --group msgraphrag` | Microsoft `graphrag` | 10/03 |
| `llamaindex` | `uv sync --group llamaindex` | `llama-index`, the Wikipedia reader, `chainlit` | the module 05 LlamaIndex exercise |
| `rag-ecosystem` | `uv sync --group rag-ecosystem` | `ragatouille` (ColBERT, torch), `ragas`, `datasets` | 11/01 |
| `vendors` | `uv sync --group vendors` | `contextual-client`, `langchain-cohere` | 05/02, 06/01, the anthology helpers' Cohere option |
| `databricks` | `uv sync --group databricks` | `databricks-sdk`, `databricks-ai-search` (formerly `databricks-vectorsearch`) | 01/02 (written to run on a Databricks workspace) |

Groups combine: `uv sync --group graph --group vendors`.

**Not installable here:** the `grouse` evaluation cells in 11/01. `grouse` pins `numpy<1.26.4` and
`openai<1.57`, which cannot coexist with this stack; if you want to run those cells, install `grouse` in a
separate virtual environment. They are evaluation pointers — RAG evaluation is taught in the separate
`Agent_Evaluation_Demystified` repository.

**Installable but not importable on LangChain 1.x:** the `rag-ecosystem` group installs, but the newest
releases still import LangChain 0.x paths at import time — `ragas` 0.4.3 imports
`langchain_community.chat_models.vertexai` and `ragatouille` 0.0.9.post2 imports `langchain.retrievers`.
The RAGAS and ColBERT cells in 11/01 therefore fail with `ModuleNotFoundError` until those projects release
LangChain 1.x support. The rest of 11/01 does not depend on them.

Some notebooks also need extra downloads at run time: NLTK data (10/01), Hugging Face / Ollama model
weights, the sample files the Contextual AI (05/02) and Microsoft GraphRAG (10/03) notebooks fetch, and the
example feedback file 06/02 starts from. The spaCy model 10/01 uses is installed by the `graph` group, and
no notebook installs packages: every dependency is declared in `pyproject.toml`.

## 3. External services

| Service | Needed by | How |
|---|---|---|
| Neo4j | 09/01–05 | free AuraDB instance (https://console.neo4j.io); `NEO4J_*`, `AURA_INSTANCENAME` in `.env` |
| Milvus / Zilliz Cloud | 10/04 | the notebook connects to a Zilliz Cloud (managed Milvus) endpoint and token you paste into its `MilvusClient(...)` cell |
| Ollama | 10/02 | local server with the model the notebook pulls |
| Databricks workspace | 01/02, and `helpers.get_llm()`'s default provider | `DATABRICKS_HOST`, `DATABRICKS_TOKEN` |
| Tavily | 02/01, 04/04 | `TAVILY_API_KEY` |
| Azure OpenAI | 08/02 (optional), 10/03 | `AZURE_OPENAI_*` deployment variables |
| Contextual AI | 05/02 | `CONTEXTUAL_API_KEY` |

## 4. Where things are

- `modules/NN_topic/notebooks/` — lessons, run with that folder as the working directory. Python files
  beside a notebook (`helper_functions.py`, `evaluation/`, runnable `*.py` scripts, the knowledge-graph
  extraction modules and Streamlit `app.py`) are imported or run from there.
- `modules/NN_topic/assets/` — data and diagrams used by one module.
- `modules/NN_topic/exercises/` — practice material without worked solutions.
- `data/sample/` — corpora shared by several modules (see `data/README.md` and `docs/data-sources.md`).
- `scripts/path_allowlist.txt` — literal file names in notebooks that are metadata labels or files the
  notebook downloads/creates at run time, so the notebook check does not expect them on disk.

## 5. Checks

```bash
uv run ruff check .
uv run pytest -q
uv run pre-commit install    # once per clone: strips notebook outputs and runs the checks on commit
```

## 6. Import check

Every notebook and companion `.py` file is import-checked against LangChain 1.x: each distinct import
statement is executed in the repository environment with all groups installed (`uv sync --all-groups`),
from the file's own folder. Nothing is run beyond the imports. Expected results:

| Import | Result | Why |
|---|---|---|
| `from evaluation.evalute_rag import *` | needs `OPENAI_API_KEY` | the scoring helper builds its DeepEval metrics at import time; the notebooks load `.env` before this import |
| `from entity_relationship_extraction import ...` (09 `app.py`) | needs `DATABRICKS_HOST` | the module creates its LLM at import time |
| `ragas`, `ragatouille` (11/01) | `ModuleNotFoundError` | upstream still imports LangChain 0.x paths — see section 2 |
| `grouse` (11/01) | not installed | cannot coexist with this stack — see section 2 |

Everything else imports cleanly.
