# M29 — Knowledge Graphs with Neo4j

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VIII · Hierarchical, Memory & Graph RAG** · **Level:** Expert · **Time:** ~6 h · **Notebooks:** 6 mandatory, 1 optional

## Why it matters

Relationships such as 'which doctors treated patients with X at hospital Y' are joins, not similarity. Knowledge graphs answer them precisely.

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
| 29.1 | Graph fundamentals and Cypher | [`01a_kg_simple.ipynb`](notebooks/01a_kg_simple.ipynb) | — |
| 29.2 | From CSV to knowledge graph | [`02a_healthcare_kg.ipynb`](notebooks/02a_healthcare_kg.ipynb) | — |
| 29.3 | Natural-language graph QA (text-to-Cypher) | [`03a_query_kg_with_langchain.ipynb`](notebooks/03a_query_kg_with_langchain.ipynb) | — |
| 29.4 | Vector indexes on graph nodes | [`04a_vector_indexing_and_embedding.ipynb`](notebooks/04a_vector_indexing_and_embedding.ipynb) | — |
| 29.5 | LLM entity and relationship extraction | [`05a_entity_relationship_extraction.ipynb`](notebooks/05a_entity_relationship_extraction.ipynb) | [`05b_create_kg_from_text.ipynb`](exercises/05b_create_kg_from_text.ipynb) *(extension)* |
| 29.6 | End-to-end knowledge-graph RAG | [`06a_roman_empire_graph_rag.ipynb`](notebooks/06a_roman_empire_graph_rag.ipynb) | — |

## Hands-on lab

Domain KG: extract a graph from 20 documents in your domain, load it into Neo4j, and answer five multi-hop questions that vector RAG gets wrong. Details: [lab/README.md](lab/README.md).

## Key concepts

Nodes, edges, properties · Cypher · Text-to-Cypher · Graph + vector hybrid

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
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
