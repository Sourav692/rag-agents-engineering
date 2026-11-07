# Lab: M44 GraphRAG Techniques

## Brief

GraphRAG vs RAPTOR vs hybrid: run the same global and multi-hop question set through each and write a one-page recommendation including indexing cost.

Solution: [solution/m44_solution.ipynb](solution/m44_solution.ipynb). Its last cell prints the recommendation, written from that run's measurements.

## Approach

All three systems index the same 20 documents (the M43 corpus) and answer the same 15 questions: the M42 global set and the M43 multi-hop set.

- **GraphRAG**, in the shape of lesson 44.3's Microsoft GraphRAG: one extraction call per chunk builds an entity graph, `networkx` Louvain groups it into communities, and the model writes a report per community. The module page's rule decides the search mode: local search starts near entities, global search uses community reports to cover the corpus. So global questions use global search (map over the closest community reports, each returning scored points, then reduce), and multi-hop questions use local search (nearest entities, their one-hop relationships and source chunks).
- **RAPTOR**, the M42 build: Gaussian-mixture clusters, one summary per cluster, up to three levels, collapsed-tree retrieval.
- **Hybrid**: RAPTOR's top nodes and GraphRAG's local context in one prompt for every question, so it needs no routing and pays both indexing costs.

What to watch:

- Indexing cost is measured, not estimated: model tokens through `UsageMetadataCallbackHandler` and wall-clock seconds for each build. Embedding calls are timed but not counted in tokens.
- `MAP_REPORTS = 8` bounds global search: it maps over the eight reports closest to the question, not every community. Raise it to move toward full Microsoft-style global search, at one model call per extra report per question.
- Carry source passages through: local search returns the chunks its entities came from, so an answer can be checked against text, not only against graph descriptions.
- The judge prompt is printed, and every score below 4 prints the judge's reason.

## How to run

- Environment: the default one (`uv sync`).
- Keys: `EXPERIENTIALLABS_API_KEY` (chat model, through `get_experientiallabs_llm()`), and `DATABRICKS_HOST` with `DATABRICKS_TOKEN` (embeddings, through `get_embeddings()`).
- No Docker: the graph is in memory (`networkx`), unlike the M43 lab's Neo4j.
- Run `solution/m44_solution.ipynb` top to bottom from the `solution/` folder.

## Data

See [data/README.md](data/README.md): the shared `larkspur/` copy, `extra_docs/` (the M43 records), `global_questions.jsonl` (copy of M42's) and `multihop.jsonl` (copy of M43's).

## Results

Not run yet. The table is filled from a real run of the solution, with its date and models, and the recommendation from its last cell is pasted below it.

| System | Global (mean score, 1 to 5) | Multi-hop (mean score, 1 to 5) | Index model tokens | Index seconds | Median query seconds |
|---|---|---|---|---|---|
| GraphRAG | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| RAPTOR | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| Hybrid | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |

Run date: *pending run*. Chat model: *pending run*. Embeddings: *pending run*.

Recommendation: *pending run*.

Back to the module: [README.md](../README.md)
