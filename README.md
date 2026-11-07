# RAG & Agents Engineering

From Python and your first LLM call to retrieval, advanced agents, a memory layer, multi-agent systems, agent protocols and GraphRAG: **14 parts, 46 modules, 227 lessons, 382 notebooks**, ordered as one course. About 216 hours over 26 weeks.

- **Syllabus:** [CURRICULUM.md](CURRICULUM.md), or open [docs/site/index.html](docs/site/index.html) in a browser for the interactive version (course map, filters, progress tracking).
- **Course folders:** one folder per part at the repo root, from [`p01_ai_engineering_foundations/`](p01_ai_engineering_foundations/README.md) to [`p14_architecture_decisions/`](p14_architecture_decisions/README.md), with one folder per module inside.
- **Theory:** [THEORY.md](THEORY.md) lists every module's theory page, its lesson pages and the interactive labs.
- **Capstones:** [capstones/](capstones/README.md).
- **Reference:** [agentic architecture coverage](docs/agentic-architecture-coverage.md) (all 35 architectures from all-agentic-architectures, mapped to course notebooks) and [how this repo is built](docs/combined-repo.md). Both have interactive pages in [docs/site/](docs/site/).

This repository was built from nine source repositories of the *AI Engineering Demystified* series (01 to 06 and 08 to 10), which are now archived. This repository is canonical: see [CLAUDE.md](CLAUDE.md) before changing anything.

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
uv sync                  # core stack: LangChain, LangGraph, RAG tooling, Jupyter
cp .env.example .env     # most notebooks need only OPENAI_API_KEY
uv run jupyter lab
```

New to the stack? Start at [M01](p01_ai_engineering_foundations/m01_python_data_refresher/README.md). Already comfortable with Python, prompting, LangChain and LangGraph? Start the RAG track at [M10](p04_rag_foundations/m10_rag_lifecycle/README.md). Each module README lists its lessons, the mandatory and optional notebooks, the theory pages and the lab.

## How the course is organised

```text
p01_ai_engineering_foundations/
├── README.md                  # the part's modules (generated)
└── m01_python_data_refresher/
    ├── README.md              # objectives, lessons, tiers, sources (generated)
    ├── mandatory/
    │   ├── notebook/          # mandatory track (+ helper files the notebooks import)
    │   └── theory/            # module page, index.html, pages of lessons with a mandatory notebook
    ├── optional/
    │   ├── notebook/          # alternate, platform-specific, extension and exercise notebooks
    │   └── theory/            # pages of lessons whose notebooks are all optional
    ├── lab/                   # the module lab: README.md, solution/m01_solution.ipynb, data/
    ├── projects/              # runnable sub-projects (MCP servers and clients) where the module has them
    └── assets/
p02_prompt_engineering/ … p14_architecture_decisions/
```

- **Mandatory vs optional:** 211 notebooks are mandatory and complete every lab. The other 171 are **alternate** (same idea, another source or API), **platform-specific** (Databricks, Astra DB, Postgres, Milvus, Contextual AI, AutoTrain, GPU video models, ColPali) or **extension** (extra practice and refreshers).
- **File names carry the lesson:** `03b_parallelization_sectioning_and_voting.ipynb` is lesson 3, second notebook.
- **Labs:** every module lab has a solution notebook in `lab/solution/` and the data it reads in `lab/data/`.
- **Baseline first:** the M10 lab builds a RAG baseline; every later RAG lab reports its change against it.

| Part | Title | Weeks | Modules |
|---|---|---|---|
| I | AI Engineering Foundations | 1 to 2 | M01 to M03 |
| II | Prompt & Context Engineering | 2 | M04 to M05 |
| III | LLM Application Frameworks: LangChain & LangGraph | 2 to 4 | M06 to M09 |
| IV | RAG Foundations: Ingestion & Indexing | 4 to 8 | M10 to M15 |
| V | Retrieval Quality & RAG Applications | 8 to 11 | M16 to M21 |
| VI | Agent Foundations | 12 to 13 | M22 to M24 |
| VII | Advanced Agents | 14 to 15 | M25 to M27 |
| VIII | Agentic RAG | 16 to 18 | M28 to M32 |
| IX | The Memory Layer | 18 to 19 | M33 to M34 |
| X | Multi-Agent Systems | 19 to 21 | M35 to M37 |
| XI | Agent Protocols: MCP & A2A | 21 to 23 | M38 to M41 |
| XII | Knowledge Graphs & GraphRAG | 23 to 25 | M42 to M44 |
| XIII | Fine-Tuning & Model Adaptation | 25 | M45 |
| XIV | Architecture Decisions | 26 | M46 + capstone |

## Optional dependency groups

| Group | Install | Needed by |
|---|---|---|
| `hf-foundations` | `uv sync --group hf-foundations` | Hugging Face media models, Gradio, fine-tuning (M03, M45; torch) |
| `document-parsing` | `uv sync --group document-parsing` | Unstructured loaders, NLTK/spaCy splitters (M11 to M12) |
| `hf` | `uv sync --group hf` | Hugging Face embeddings, cross-encoders, CLIP, MarianMT (torch) |
| `colpali` | `uv sync --no-default-groups --group dev --group colpali` | ColPali page retrieval (M20, optional); conflicts with `hf` and `hf-foundations` |
| `llamaindex` | `uv sync --group llamaindex` | LlamaIndex notebooks and the Chainlit exercise |
| `vendors` | `uv sync --group vendors` | Pinecone, Astra DB, Cohere, Gemini, Contextual AI |
| `databricks` | `uv sync --group databricks` | Databricks Vector Search / MLflow / SQL notebooks |
| `protocols` | `uv sync --group protocols` | MCP and A2A SDKs (M38 to M41) |
| `mcp-labs`, `mcp-apps` | `uv sync --group mcp-labs --group mcp-apps` | MCP labs and applications (M38 to M40) |
| `graph` | `uv sync --group graph` | Neo4j, Milvus, spaCy concept extraction (M43 to M44) |
| `msgraphrag` | `uv sync --group msgraphrag` | Microsoft GraphRAG (M44) |
| `local-models` | `uv sync --group local-models` | Ollama + sentence-transformers (M44) |
| `rag-ecosystem` | `uv sync --group rag-ecosystem` | ColBERT and RAGAS cells (M46) |
| `apps` | `uv sync --group apps` | Streamlit apps |
| `finance` | `uv sync --group finance` | OpenBB finance agents; conflicts with `protocols`, `mcp-labs` and `mcp-apps` |

## Maintaining this repo

This repo is canonical: notebooks, helpers and data are edited here. It was built from nine *AI Engineering Demystified* repos, now archived. The part and module READMEs, the `index.html` theory pages, `THEORY.md` and the syllabus are rendered from `curriculum.yaml` with `scripts/build_curriculum.py`; theory pages and labs are hand-written. The operating rules and the migration history are in [CLAUDE.md](CLAUDE.md). `uv run pytest -q` runs the offline checks.

## Licence

Original content is MIT ([LICENSE](LICENSE)). Some material keeps third-party terms, including the non-commercial RAG Techniques anthology, third-party MCP course material and GPL-3.0 MCP client labs: see [NOTICE.md](NOTICE.md). [docs/content-inventory.csv](docs/content-inventory.csv) maps every file to its source repository and path.
