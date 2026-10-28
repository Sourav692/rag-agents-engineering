# Setup

## 1. Install

```bash
uv sync                  # Python 3.12, the core LangChain/RAG stack, the local helpers package and dev tools
cp .env.example .env     # names only; fill in the keys for the notebooks you plan to run
uv run pytest            # offline: notebook structure, links, and a smoke test; no API keys, no network
uv run jupyter lab
```

`uv sync` installs `src/helpers` in editable mode, so notebooks can `from helpers import get_llm,
get_embeddings, get_experientiallabs_llm`. The canonical lessons also put `src/` on `sys.path` to import
`rag_paths`, which finds sample files by name under `data/sample/` (and `modules/03_chunking/assets/`).

## 2. Optional dependency groups

The default install stays light. Add a group only when a notebook needs it:

| Group | Command | What it adds | Used by |
|---|---|---|---|
| `hf` | `uv sync --group hf` | `langchain-huggingface`, `sentence-transformers`, `transformers`, `torch`, `pillow` | Hugging Face embeddings and cross-encoders (modules 04, 07, 08, 09, 10), CLIP (11/01) |
| `document-parsing` | `uv sync --group document-parsing` | `unstructured[md,pdf,docx]`, `nltk`, `spacy`, spaCy model `en_core_web_sm` | Unstructured loaders (module 02), NLTK/spaCy splitters (03/02) |
| `llamaindex` | `uv sync --group llamaindex` | `llama-index` and its FAISS / file-reader / BM25 integrations | module 13, `03_chunking/10` |
| `vendors` | `uv sync --group vendors` | `langchain-pinecone`, `langchain-astradb`, `langchain-cohere`, `google-generativeai`, `jrag` | 05/06, 05/07, 11/02, 10/10 |
| `databricks` | `uv sync --group databricks` | `databricks-vectorsearch`, `mlflow` | 04/08, 07/08 (run on a Databricks workspace) |
| `colpali` | `uv sync --no-default-groups --group dev --group colpali` | `byaldi`, `google-generativeai` | 11/03 only |

Groups combine: `uv sync --group hf --group document-parsing`. The `colpali` group pins
`transformers<5` and is declared as conflicting with `hf`, so use a separate sync for it.

Some notebooks also need extra downloads at run time: NLTK data (`nltk.download`, 02/03 and 03/02),
Hugging Face model weights, and the `!wget` data-download cells kept from the original notebooks
(`wget` is not preinstalled on macOS: `brew install wget`, or skip the cell — the files are already in
`data/sample/`). The spaCy model comes from the `document-parsing` group; no notebook installs packages.

One notebook path is optional and not installed: `YoutubeLoader(add_video_info=True)` (02/09) needs
`pytube`, which is unmaintained; the notebook falls back to transcript-only loading without it.

## 3. External services

| Service | Needed by | How |
|---|---|---|
| PostgreSQL + pgvector | module 12, 06/03 | `docker compose up -d` in `modules/12_langchain_rag_implementations/notebooks/` |
| Databricks workspace | 04/08, 07/08, `helpers.get_llm()` default provider | `DATABRICKS_HOST`, `DATABRICKS_TOKEN` |
| Astra DB, Pinecone | 05/06, 05/07 | keys in `.env` |

## 4. Where things are

- `modules/NN_topic/notebooks/` — lessons, run with that folder as the working directory. Python files
  beside a notebook (`helper_functions.py`, `evaluation/`, `utils.py`, runnable `*.py` scripts) are
  imported or run from there.
- `modules/NN_topic/assets/` — data and diagrams used by one module.
- `data/sample/` — corpora shared by several modules (see `data/README.md` and `docs/data-sources.md`).
- `scripts/path_allowlist.txt` — literal file names in notebooks that are metadata labels, runtime
  outputs, or resolved through `rag_paths`, so the notebook check does not expect them on disk.

## 5. Checks

```bash
uv run ruff check .
uv run pytest -q
uv run pre-commit install    # once per clone: strips notebook outputs and runs the checks on commit
```

## 6. LangChain 1.x import paths

The lessons carried over from older sources used LangChain 0.x module paths (`langchain.text_splitter`,
`langchain.chains`, `langchain.retrievers`, `langchain.schema`, `langchain_core.pydantic_v1`, ...) that no
longer exist in LangChain 1.x. Their imports now point at the 1.x homes — `langchain_text_splitters`,
`langchain_core`, `langchain_community`, `langchain_openai`, `langchain_chroma` and, for legacy chains and
retrievers, `langchain_classic` — with the lesson code otherwise unchanged. Every notebook and `.py` file
import is checked by executing it against the locked environment (all optional groups included).
