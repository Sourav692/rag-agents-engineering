# RAG & Agents Engineering

From Python and your first LLM call to agentic, memory-backed, multi-agent, protocol-connected and graph-based RAG: **13 parts, 45 modules, 377 notebooks**, ordered as one course. About 214 hours over 26 weeks.

- **Syllabus:** [CURRICULUM.md](CURRICULUM.md), or open [docs/site/index.html](docs/site/index.html) in a browser for the interactive version (course map, filters, progress tracking).
- **Course folders:** [course/](course/README.md), one folder per Part and module.
- **Capstones:** [capstones/](capstones/README.md).
- **Reference:** [agentic architecture coverage](docs/agentic-architecture-coverage.md) (all 35 architectures from all-agentic-architectures, mapped to course notebooks) and [how this repo is built](docs/combined-repo.md). Both have interactive pages in [docs/site/](docs/site/).

This repository is generated from nine source repositories of the *AI Engineering Demystified* series (01–06 and 08–10). They stay canonical: see [CLAUDE.md](CLAUDE.md) before changing anything.

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
uv sync                  # core stack: LangChain, LangGraph, RAG tooling, Jupyter
cp .env.example .env     # most notebooks need only OPENAI_API_KEY
uv run jupyter lab
```

New to the stack? Start at [M01](course/p01_ai_engineering_foundations/m01_python_data_refresher/README.md). Already comfortable with Python, prompting, LangChain and LangGraph? Start the RAG track at [M11](course/p04_rag_foundations/m11_rag_lifecycle/README.md). Each module README lists its lessons, the mandatory and optional notebooks, and the lab.

## How the course is organised

```text
course/
├── p01_ai_engineering_foundations/
│   └── m01_python_data_refresher/
│       ├── README.md      # objectives, lessons, tiers, sources
│       ├── lab/README.md  # the module lab
│       ├── notebooks/     # mandatory track (+ helper files the notebooks import)
│       ├── optional/      # alternate, platform-specific and extension notebooks
│       ├── exercises/     # where the module has exercises
│       ├── projects/      # runnable sub-projects (MCP servers and clients) where the module has them
│       └── assets/
├── p02_prompt_engineering/ … p13_architecture_and_capstone/
```

- **Mandatory vs optional:** 211 notebooks are mandatory and complete every lab. The other 166 are **alternate** (same idea, another source or API), **platform-specific** (Databricks, Astra DB, Postgres, Milvus, Contextual AI, AutoTrain, GPU video models, ColPali) or **extension** (extra practice and refreshers).
- **File names carry the lesson:** `03b_parallelization_sectioning_and_voting.ipynb` is lesson 3, second notebook.
- **Baseline first:** the M11 lab builds a RAG baseline; every later RAG lab reports its change against it.

| Part | Title | Weeks | Modules |
|---|---|---|---|
| I | AI Engineering Foundations | 1–2 | M01–M04 |
| II | Prompt & Context Engineering | 3 | M05–M06 |
| III | LangChain & LangGraph Fundamentals | 4–5 | M07–M10 |
| IV | RAG Foundations | 6 | M11 |
| V | The Ingestion & Indexing Pipeline | 7–9 | M12–M16 |
| VI | Retrieval Quality Engineering | 10–11 | M17–M19 |
| VII | Building Complete RAG Applications | 12 | M20–M22 |
| VIII | Agent Foundations for RAG | 13–15 | M23–M27 |
| IX | Agentic & Self-Correcting RAG | 16–17 | M28–M32 |
| X | Memory & Multi-Agent RAG | 18–20 | M33–M37 |
| XI | Agent Protocols: MCP & A2A | 21–22 | M38–M41 |
| XII | Hierarchical, Memory & Graph RAG | 23–24 | M42–M44 |
| XIII | Architecture Synthesis & Capstone | 25–26 | M45 + capstone |

## Optional dependency groups

| Group | Install | Needed by |
|---|---|---|
| `hf-foundations` | `uv sync --group hf-foundations` | Hugging Face media models, Gradio, fine-tuning (M03–M04; torch) |
| `document-parsing` | `uv sync --group document-parsing` | Unstructured loaders, NLTK/spaCy splitters (M12–M13) |
| `hf` | `uv sync --group hf` | Hugging Face embeddings, cross-encoders, CLIP, MarianMT (torch) |
| `colpali` | `uv sync --no-default-groups --group dev --group colpali` | ColPali page retrieval (M21, optional); conflicts with `hf` and `hf-foundations` |
| `llamaindex` | `uv sync --group llamaindex` | LlamaIndex notebooks and the Chainlit exercise |
| `vendors` | `uv sync --group vendors` | Pinecone, Astra DB, Cohere, Gemini, Contextual AI |
| `databricks` | `uv sync --group databricks` | Databricks Vector Search / MLflow / SQL notebooks |
| `protocols` | `uv sync --group protocols` | MCP and A2A SDKs (M38–M41) |
| `mcp-labs`, `mcp-apps` | `uv sync --group mcp-labs --group mcp-apps` | MCP labs and applications (M38–M40) |
| `graph` | `uv sync --group graph` | Neo4j, Milvus, spaCy concept extraction (M43–M44) |
| `msgraphrag` | `uv sync --group msgraphrag` | Microsoft GraphRAG (M44) |
| `local-models` | `uv sync --group local-models` | Ollama + sentence-transformers (M44) |
| `rag-ecosystem` | `uv sync --group rag-ecosystem` | ColBERT and RAGAS cells (M45) |
| `apps` | `uv sync --group apps` | Streamlit apps |
| `finance` | `uv sync --group finance` | OpenBB finance agents; conflicts with `protocols`, `mcp-labs` and `mcp-apps` |

## Maintaining this repo

This repo is canonical: notebooks, helpers and data are edited here. It was built from nine *AI Engineering Demystified* repos, now archived. The READMEs and syllabus are rendered from `curriculum.yaml` with `scripts/build_curriculum.py`. The operating rules and the migration history are in [CLAUDE.md](CLAUDE.md). `uv run pytest -q` runs the offline checks.

## Licence

Original content is MIT ([LICENSE](LICENSE)). Some material keeps third-party terms, including the non-commercial RAG Techniques anthology, third-party MCP course material and GPL-3.0 MCP client labs: see [NOTICE.md](NOTICE.md). [docs/content-inventory.csv](docs/content-inventory.csv) maps every file to its source repository and path.
