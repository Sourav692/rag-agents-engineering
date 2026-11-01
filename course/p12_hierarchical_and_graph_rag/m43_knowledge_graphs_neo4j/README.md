# M43 — Knowledge Graphs with Neo4j

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part XII · Hierarchical, Memory & Graph RAG** · **Level:** Expert · **Time:** ~6 h · **Notebooks:** 6 mandatory, 1 optional

## Why it matters

Relationships such as 'which doctors treated patients with X at hospital Y' are joins, not similarity. Knowledge graphs answer them precisely.

## Theory

Read the [theory page](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Candidates and graph constraints](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/04_vector_indexes_on_graph_nodes/interactive/graph-filter-lab.html) (open the file in a browser)

## Learning objectives

- Model a domain as nodes and relationships and query it with Cypher
- Load CSV data into a Neo4j knowledge graph
- Answer natural-language questions with LangChain's text-to-Cypher graph QA
- Add embeddings and a vector index to graph nodes for hybrid graph + vector retrieval
- Extract entities and relationships from text with an LLM and build KG-RAG end to end

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 43.1 | Graph fundamentals and Cypher ([theory](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/01_graph_fundamentals_and_cypher/README.md)) | [`01a_kg_simple.ipynb`](notebooks/01a_kg_simple.ipynb) | — |
| 43.2 | From CSV to knowledge graph ([theory](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/02_from_csv_to_knowledge_graph/README.md)) | [`02a_healthcare_kg.ipynb`](notebooks/02a_healthcare_kg.ipynb) | — |
| 43.3 | Natural-language graph QA (text-to-Cypher) ([theory](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/03_natural_language_graph_qa_text_to_cypher/README.md)) | [`03a_query_kg_with_langchain.ipynb`](notebooks/03a_query_kg_with_langchain.ipynb) | — |
| 43.4 | Vector indexes on graph nodes ([theory](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/04_vector_indexes_on_graph_nodes/README.md)) | [`04a_vector_indexing_and_embedding.ipynb`](notebooks/04a_vector_indexing_and_embedding.ipynb) | — |
| 43.5 | LLM entity and relationship extraction ([theory](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/05_llm_entity_and_relationship_extraction/README.md)) | [`05a_entity_relationship_extraction.ipynb`](notebooks/05a_entity_relationship_extraction.ipynb) | [`05b_create_kg_from_text.ipynb`](exercises/05b_create_kg_from_text.ipynb) *(extension)* |
| 43.6 | End-to-end knowledge-graph RAG ([theory](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/06_end_to_end_knowledge_graph_rag/README.md)) | [`06a_roman_empire_graph_rag.ipynb`](notebooks/06a_roman_empire_graph_rag.ipynb) | — |

## Hands-on lab

Domain KG: extract a graph from 20 documents in your domain, load it into Neo4j, and answer five multi-hop questions that vector RAG gets wrong. Details: [lab/README.md](lab/README.md).

## Key concepts

[Nodes, edges, properties](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/01_graph_fundamentals_and_cypher/README.md#nodes-edges-properties) · [Cypher](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/01_graph_fundamentals_and_cypher/README.md#cypher) · [Text-to-Cypher](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/03_natural_language_graph_qa_text_to_cypher/README.md#text-to-cypher) · [Graph + vector hybrid](../../../theory/p12_hierarchical_and_graph_rag/m43_knowledge_graphs_neo4j/04_vector_indexes_on_graph_nodes/README.md#graph--vector-hybrid)

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
| `notebooks/01a_kg_simple.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/09_knowledge_graphs_with_neo4j/notebooks/01_kg_simple.ipynb` |
| `notebooks/02a_healthcare_kg.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/09_knowledge_graphs_with_neo4j/notebooks/02_healthcare_kg.ipynb` |
| `notebooks/03a_query_kg_with_langchain.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/09_knowledge_graphs_with_neo4j/notebooks/03_query_kg_with_langchain.ipynb` |
| `notebooks/04a_vector_indexing_and_embedding.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/09_knowledge_graphs_with_neo4j/notebooks/04_vector_indexing_and_embedding.ipynb` |
| `notebooks/05a_entity_relationship_extraction.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/09_knowledge_graphs_with_neo4j/notebooks/06_entity_relationship_extraction.ipynb` |
| `exercises/05b_create_kg_from_text.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/09_knowledge_graphs_with_neo4j/exercises/01_create_kg_from_text.ipynb` |
| `notebooks/06a_roman_empire_graph_rag.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/09_knowledge_graphs_with_neo4j/notebooks/05_roman_empire_graph_rag.ipynb` |
