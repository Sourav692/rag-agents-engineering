# M44 — GraphRAG Techniques

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part XII · Hierarchical, Memory & Graph RAG** · **Level:** Expert · **Time:** ~5 h · **Notebooks:** 2 mandatory, 2 optional

## Why it matters

GraphRAG uses graph structure for retrieval itself: traversing concepts, summarising communities, and expanding through adjacency.

## Theory

Read the [theory page](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Expansion and the evidence set](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/04_graph_expansion_inside_a_vector_database_milvus/interactive/expansion-lab.html) (open the file in a browser)

## Learning objectives

- Build a concept graph over chunks and traverse it to answer questions
- Attach verifiable per-claim source attribution in local graph RAG
- Index with Microsoft GraphRAG and run global (community) and local queries
- Store entities, relations and passages in Milvus and expand retrieval through graph adjacency

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 44.1 | Concept-graph traversal ([theory](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/01_concept_graph_traversal/README.md)) | [`01a_graph_rag.ipynb`](notebooks/01a_graph_rag.ipynb) | — |
| 44.2 | Local GraphRAG with source attribution *(optional lesson)* ([theory](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/02_local_graphrag_with_source_attribution/README.md)) | — | [`02a_graph_rag_local_attribution.ipynb`](optional/02a_graph_rag_local_attribution.ipynb) *(extension)* |
| 44.3 | Microsoft GraphRAG: communities, global vs local search ([theory](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/03_microsoft_graphrag_communities_global_vs_local_search/README.md)) | [`03a_microsoft_graphrag.ipynb`](notebooks/03a_microsoft_graphrag.ipynb) | — |
| 44.4 | Graph expansion inside a vector database (Milvus) *(optional lesson)* ([theory](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/04_graph_expansion_inside_a_vector_database_milvus/README.md)) | — | [`04a_graphrag_with_milvus.ipynb`](optional/04a_graphrag_with_milvus.ipynb) *(platform-specific)* |

## Hands-on lab

GraphRAG vs RAPTOR vs hybrid: run the same global and multi-hop question set through each and write a one-page recommendation including indexing cost. Details: [lab/README.md](lab/README.md).

## Key concepts

[Community detection](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/03_microsoft_graphrag_communities_global_vs_local_search/README.md#community-detection) · [Global vs local search](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/03_microsoft_graphrag_communities_global_vs_local_search/README.md#global-vs-local-search) · [Graph expansion](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/04_graph_expansion_inside_a_vector_database_milvus/README.md#graph-expansion) · [Indexing cost](../../../theory/p12_hierarchical_and_graph_rag/m44_graphrag/03_microsoft_graphrag_communities_global_vs_local_search/README.md#indexing-cost)

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `projects/` — runnable sub-projects (e.g. MCP servers and clients), where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_graph_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/10_graphrag_techniques/notebooks/01_graph_rag.ipynb` |
| `optional/02a_graph_rag_local_attribution.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/10_graphrag_techniques/notebooks/02_graph_rag_local_attribution.ipynb` |
| `notebooks/03a_microsoft_graphrag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/10_graphrag_techniques/notebooks/03_microsoft_graphrag.ipynb` |
| `optional/04a_graphrag_with_milvus.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/10_graphrag_techniques/notebooks/04_graphrag_with_milvus.ipynb` |
