# Setup

## Install

```bash
uv sync                  # Python 3.12 env with the LangChain stack, aied-helpers and dev tools
cp .env.example .env     # fill in only the providers you will use

# One-time per clone: notebook hygiene
uv run nbstripout --install --attributes .gitattributes   # git filter: strips outputs on `git add`, keeps them on disk
uv run pre-commit install                                  # runs ruff and the notebook/link checks on every commit
```

The shared course helpers (`aied-helpers`, e.g. `from aied_helpers import get_openai_llm`) are a normal dependency pinned to a release tag in `pyproject.toml`; `uv sync` installs them.

Without uv's project workflow, install from the exported `requirements.txt`:

```bash
uv venv --python 3.12 && uv pip install -r requirements.txt
```

Regenerate it after changing dependencies: `uv export --format requirements-txt --no-hashes --no-dev --no-emit-project -o requirements.txt`.

Optional groups (the default `uv sync` stays light):

| Group | Command | Needed for |
|---|---|---|
| `hf` | `uv sync --group hf` | `modules/01_getting_started` notebooks 04 and 07, which run open-source models locally with PyTorch/Transformers |
| `app` | `uv sync --group app` | The Streamlit summarizer, `uv run streamlit run modules/05_summarization/notebooks/app.py` |

Combine groups with `uv sync --group hf --group app`.

## Run

```bash
uv run jupyter lab
```

Notebooks use paths relative to their own folder (Jupyter's working directory), so open them from the Jupyter file browser rather than moving them.

## Verify (offline, no API keys)

```bash
uv run pytest            # notebook structure, links/self-containment, smoke test
uv run ruff check .
```

`scripts/check_notebooks.py` fails on outputs in the staged copy of a notebook, a missing `# Title`, or a file path a notebook reads that does not exist. Paths a notebook *creates* (or that are only labels) are listed in `scripts/path_allowlist.txt`.

## Costs

Most notebooks make small calls to paid APIs (usually `gpt-4o-mini`). Nothing in `uv run pytest` calls a model.
