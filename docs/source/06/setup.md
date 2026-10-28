# Setup

## Install

```bash
uv sync                      # Python 3.12, core dependencies, dev tools, and `aied-helpers`
cp .env.example .env         # names only; fill in what you need
uv run pytest                # offline structural checks — no API keys, no network
uv run pre-commit install    # once per clone: runs the checks (and nbstripout --keep-output) on commit
uv run jupyter lab
```

Optional groups (kept out of the default install because they are large):

```bash
uv sync --group apps         # streamlit — the Hacker News chatbot UI in module 01
uv sync --group finance      # openbb — the OpenBB financial-analyst agent in module 14
```

## Running notebooks

- Start Jupyter from the repository root and open notebooks in place; every relative path is written relative to the notebook's own folder, which is Jupyter's working directory.
- Notebooks ship with the outputs of a clean top-to-bottom run, so you can read what each cell produces before spending anything. Re-running changes them (model answers vary). Every notebook makes paid model calls; several also call Tavily, OpenWeatherMap or OpenBB. Cost notes are at the top of the notebooks that are expensive (hosted tools, image generation, deep research).
- Some notebooks still carry `!pip install ...` cells from their original course. You do not need them after `uv sync`; skip them.

## Shared LLM helpers

[`aied-helpers`](https://github.com/Sourav692/ai-engineering-demystified-shared) is installed from its immutable `v0.1.0` Git tag by this repository. Its default `get_llm()` provider is OpenRouter's NVIDIA Nemotron 3 Ultra free model and requires `OPENROUTER_API_KEY`.

```python
from aied_helpers import get_llm

llm = get_llm()
```

It also exposes `get_openai_llm`, `get_groq_llm`, `get_databricks_llm`, `get_experientiallabs_llm`, and embedding factories. `get_databricks_llm` works with fully qualified `system.ai.*` model services. The shared package deliberately does not load `.env` files at import time; notebooks call `load_dotenv(find_dotenv(usecwd=True))` before provider use.

## Checks

| Command | What it verifies |
|---|---|
| `uv run python scripts/check_notebooks.py` | valid notebooks, `# Title` first markdown cell, saved outputs come from one clean run (execution counts 1..n, no errors) and are safe to publish (no API-key-like strings, no workstation paths, ≤ 2 MB), relative file paths resolve (files a notebook creates are listed in `scripts/path_allowlist.txt`) |
| `uv run python scripts/check_links.py` | markdown links resolve inside the repo; no absolute workstation paths; no paths into the old monorepo layout |
| `uv run python scripts/smoke_test.py` | every `.py` file compiles, `aied_helpers` imports, and both checks above pass |
| `uv run ruff check .` | lint (notebooks and the vendored `agentic_patterns` library are excluded) |
