# Setup

## Install

```bash
uv sync                      # Python 3.12, core dependencies, dev tools, `aied-helpers` and the local `helpers` package
cp .env.example .env         # names only; fill in what you need
uv run pytest                # offline structural checks — no API keys, no network
uv run pre-commit install    # once per clone: runs the checks on commit
uv run nbstripout --install --attributes .gitattributes   # once per clone: strips notebook outputs on `git add`
uv run jupyter lab
```

The nbstripout *git filter* strips outputs from the copy git stores while your working copy keeps them, and the checks read that staged copy. Its command lives in `.git/config` and points at this clone's `.venv`, so run it once per clone; if you recreate `.venv`, run `uv sync` before `git add`ing notebooks.

Without `uv sync`, the same pinned environment installs from the exported `requirements.txt`:

```bash
uv venv --python 3.12 && uv pip install -r requirements.txt && uv pip install -e .
```

`requirements.txt` is generated — regenerate it after changing dependencies with
`uv export --format requirements-txt --no-hashes --no-dev --no-emit-project -o requirements.txt`.

Optional groups (kept out of the default install because they are large or rarely needed):

```bash
uv sync --group hf           # transformers (pulls PyTorch)
uv sync --group apps         # streamlit — chat_stream.py in module 01
uv sync --group finance      # openbb — the supervisor financial-research build in module 10
```

## Local services

| Service | Used by | Quick start |
|---|---|---|
| Postgres | `modules/03_long_term_and_persistent_memory/notebooks/01_cross_thread_memory_store.ipynb` (connects to `localhost:5433`) | `docker run -d -p 5433:5432 -e POSTGRES_PASSWORD=postgres postgres` |
| Neo4j (optional) | Part 5 of `modules/04_agentic_memory_architectures/notebooks/02_graph_memory_multi_hop.ipynb` (skipped when unset) | `docker run -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password123 -e NEO4J_PLUGINS='["apoc"]' neo4j` (APOC is required: `langchain-neo4j` reads the schema with it); set `NEO4J_URI=bolt://localhost:7687`, `NEO4J_USERNAME=neo4j`, `NEO4J_PASSWORD=password123` |

## Running notebooks

- Start Jupyter from the repository root and open notebooks in place; every relative path is written relative to the notebook's own folder, which is Jupyter's working directory. `load_dotenv()` finds the repository-root `.env` from there.
- Notebooks ship with outputs cleared. Every notebook makes paid model calls; several also call Tavily, OpenWeatherMap or OpenBB.
- Files a notebook creates (SQLite `.db` files, module 10's `logs.log` and `charts/`) land beside it and are git-ignored; they are listed in `scripts/path_allowlist.txt`.
- Notebooks never install packages: every dependency is declared in `pyproject.toml` and installed by `uv sync`. Keys come from the project-root `.env` (`load_dotenv(find_dotenv(usecwd=True))`), never from Colab or Kaggle secrets.
- Imports target LangChain 1.x. Legacy memory, chain and `AgentExecutor` classes are imported from `langchain_classic`; prompts, messages, runnables and documents from `langchain_core`.

## LLM factories

`aied-helpers` (the shared course package, pinned to a release tag in `pyproject.toml`) is the standard factory across the course repositories:

```python
from aied_helpers import get_openai_llm

llm = get_openai_llm(model="gpt-4o-mini")
```

Every notebook builds its model this way, with the model named explicitly (the factory's own default differs). Embeddings come from the same package: `get_embeddings(provider="openai", model="text-embedding-3-small")`.

The repository-local `helpers` package (`src/helpers/`) is still installed by `uv sync` for scripts and your own experiments (`from helpers import get_llm, get_embeddings`; with no arguments it builds the Databricks-served default model and needs `DATABRICKS_HOST` and `DATABRICKS_TOKEN`). No notebook imports it any more, and no notebook edits `sys.path`.

## The deep-agent scripts (module 11)

```bash
uv run python modules/11_deep_agents_and_harness_engineering/notebooks/simple_coding_agent.py
uv run python modules/11_deep_agents_and_harness_engineering/notebooks/long_term_memory_agent.py
```

They use `ChatDatabricks` (`databricks-claude-opus-4-6`), Tavily and four Databricks Genie spaces. The default backend is a virtual filesystem with no code execution; `USE_SANDBOX=true` switches to a backend that runs code on your machine — only use it with agents and prompts you trust.

## Checks

| Command | What it verifies |
|---|---|
| `uv run python scripts/check_notebooks.py` | valid notebooks, `# Title` first markdown cell, cleared outputs, relative file paths resolve (files a notebook creates are listed in `scripts/path_allowlist.txt`) |
| `uv run python scripts/check_links.py` | markdown links resolve inside the repo; no absolute workstation paths; no paths into the old monorepo layout |
| `uv run python scripts/smoke_test.py` | every `.py` file compiles, `helpers` imports, and both checks above pass |
| `uv run ruff check .` | lint (notebooks, `src/helpers` and the lesson scripts are excluded — they are lesson code kept as authored) |
