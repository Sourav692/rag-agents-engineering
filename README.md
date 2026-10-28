# RAG & Agents Engineering

From your first retriever to agentic, memory-backed, multi-agent and graph-based RAG: **9 parts, 31 modules, 251 notebooks**, ordered as one course. About 161 hours over 17 weeks.

- **Syllabus:** [CURRICULUM.md](CURRICULUM.md), or open [docs/site/index.html](docs/site/index.html) in a browser for the interactive version (course map, filters, progress tracking).
- **Course folders:** [course/](course/README.md), one folder per Part and module.
- **Capstones:** [capstones/](capstones/README.md).

This repository is generated from four source repositories (05 Retrieval & RAG, 06 Agent fundamentals, 08 Advanced agent systems, 09 Advanced RAG). They stay canonical: see [CLAUDE.md](CLAUDE.md) before changing anything.

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
uv sync                  # core LangChain / LangGraph stack + Jupyter
cp .env.example .env     # most notebooks need only OPENAI_API_KEY
uv run jupyter lab
```

Start with [M01](course/p1_rag_foundations/m01_rag_lifecycle/README.md). Each module README lists its lessons, the mandatory and optional notebooks, and the lab.

## How the course is organised

```text
course/
├── p1_rag_foundations/
│   └── m01_rag_lifecycle/
│       ├── README.md      # objectives, lessons, tiers, sources
│       ├── lab/README.md  # the module lab
│       ├── notebooks/     # mandatory track (+ helper files the notebooks import)
│       ├── optional/      # alternate, platform-specific and extension notebooks
│       ├── exercises/     # where the module has exercises
│       └── assets/
├── p2_ingestion_and_indexing/ … p9_architecture_and_capstone/
```

- **Mandatory vs optional:** 145 notebooks are mandatory and complete every lab. The other 106 are **alternate** (same idea, another source or API), **platform-specific** (Databricks, Astra DB, Postgres, Milvus, Contextual AI, ColPali) or **extension** (extra practice).
- **File names carry the lesson:** `03b_parallelization_sectioning_and_voting.ipynb` is lesson 3, second notebook.
- **Baseline first:** the M01 lab builds a baseline; every later lab reports its change against it.

| Part | Title | Weeks | Modules |
|---|---|---|---|
| I | RAG Foundations | 1 | M01 |
| II | The Ingestion & Indexing Pipeline | 2–3 | M02–M06 |
| III | Retrieval Quality Engineering | 4–5 | M07–M09 |
| IV | Building Complete RAG Applications | 6 | M10–M12 |
| V | Agent Foundations for RAG | 7–9 | M13–M17 |
| VI | Agentic & Self-Correcting RAG | 10–11 | M18–M22 |
| VII | Memory & Multi-Agent RAG | 12–13 | M23–M27 |
| VIII | Hierarchical, Memory & Graph RAG | 14–15 | M28–M30 |
| IX | Architecture Synthesis & Capstone | 16–17 | M31 + capstone |

## Optional dependency groups

| Group | Install | Needed by |
|---|---|---|
| `document-parsing` | `uv sync --group document-parsing` | Unstructured loaders, NLTK/spaCy splitters (M02–M03) |
| `hf` | `uv sync --group hf` | Hugging Face embeddings, cross-encoders, CLIP, MarianMT (torch) |
| `colpali` | `uv sync --no-default-groups --group dev --group colpali` | ColPali page retrieval (M11, optional); conflicts with `hf` |
| `llamaindex` | `uv sync --group llamaindex` | LlamaIndex notebooks and the Chainlit exercise |
| `vendors` | `uv sync --group vendors` | Pinecone, Astra DB, Cohere, Gemini, Contextual AI |
| `databricks` | `uv sync --group databricks` | Databricks Vector Search / MLflow notebooks |
| `graph` | `uv sync --group graph` | Neo4j, Milvus, spaCy concept extraction (M29–M30) |
| `msgraphrag` | `uv sync --group msgraphrag` | Microsoft GraphRAG (M30) |
| `local-models` | `uv sync --group local-models` | Ollama + sentence-transformers (M30) |
| `rag-ecosystem` | `uv sync --group rag-ecosystem` | ColBERT and RAGAS cells (M31) |
| `apps`, `finance` | `uv sync --group apps --group finance` | Streamlit apps, OpenBB finance agents |

## Maintaining this repo

Notebooks are fixed in their source repos and synced here with `scripts/migrate.py`; the READMEs and syllabus are rendered from `curriculum.yaml` with `scripts/build_curriculum.py`. The full workflow, the migration plan and the options for the source repos' future are in [CLAUDE.md](CLAUDE.md). `uv run pytest -q` runs the offline checks.

## Licence

Original content is MIT ([LICENSE](LICENSE)). Some notebooks keep third-party licences, including the non-commercial RAG Techniques anthology: see [NOTICE.md](NOTICE.md). [docs/content-inventory.csv](docs/content-inventory.csv) maps every file to its source repository and path.
