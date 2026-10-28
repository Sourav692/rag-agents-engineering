# M30 — GraphRAG Techniques

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VIII · Hierarchical, Memory & Graph RAG** · **Level:** Expert · **Time:** ~5 h · **Notebooks:** 2 mandatory, 2 optional

## Why it matters

GraphRAG uses graph structure for retrieval itself: traversing concepts, summarising communities, and expanding through adjacency.

## Learning objectives

- Build a concept graph over chunks and traverse it to answer questions
- Attach verifiable per-claim source attribution in local graph RAG
- Index with Microsoft GraphRAG and run global (community) and local queries
- Store entities, relations and passages in Milvus and expand retrieval through graph adjacency

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 30.1 | Concept-graph traversal | [`01a_graph_rag.ipynb`](notebooks/01a_graph_rag.ipynb) | — |
| 30.2 | Local GraphRAG with source attribution *(optional lesson)* | — | [`02a_graph_rag_local_attribution.ipynb`](optional/02a_graph_rag_local_attribution.ipynb) *(extension)* |
| 30.3 | Microsoft GraphRAG: communities, global vs local search | [`03a_microsoft_graphrag.ipynb`](notebooks/03a_microsoft_graphrag.ipynb) | — |
| 30.4 | Graph expansion inside a vector database (Milvus) *(optional lesson)* | — | [`04a_graphrag_with_milvus.ipynb`](optional/04a_graphrag_with_milvus.ipynb) *(platform-specific)* |

## Hands-on lab

GraphRAG vs RAPTOR vs hybrid: run the same global and multi-hop question set through each and write a one-page recommendation including indexing cost. Details: [lab/README.md](lab/README.md).

## Key concepts

Community detection · Global vs local search · Graph expansion · Indexing cost

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_graph_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/10_graphrag_techniques/notebooks/01_graph_rag.ipynb` |
| `optional/02a_graph_rag_local_attribution.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/10_graphrag_techniques/notebooks/02_graph_rag_local_attribution.ipynb` |
| `notebooks/03a_microsoft_graphrag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/10_graphrag_techniques/notebooks/03_microsoft_graphrag.ipynb` |
| `optional/04a_graphrag_with_milvus.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/10_graphrag_techniques/notebooks/04_graphrag_with_milvus.ipynb` |
