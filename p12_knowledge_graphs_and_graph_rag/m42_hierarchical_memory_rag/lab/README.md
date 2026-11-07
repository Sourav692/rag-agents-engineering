# Lab: M42 Hierarchical & Memory-Augmented Retrieval

## Brief

Global-question test: ask ten 'summarise / compare across the whole corpus' questions and compare flat RAG, RAPTOR and LightRAG.

Solution: [solution/m42_solution.ipynb](solution/m42_solution.ipynb).

## Approach

A global question has no single passage that answers it: the reference answer for "compare the three plans" draws on four handbook files. The three systems differ in where that combining happens.

- **Flat RAG** embeds the chunks and passes the top 4 to the model, which has to combine whatever those four hold.
- **RAPTOR** (lesson 42.1, `01a_raptor.ipynb`) combines at indexing time. It embeds the chunks, clusters them with a Gaussian mixture, summarises each cluster, and repeats on the summaries up to three levels. Retrieval searches the collapsed tree, chunks and summaries together, so a broad question can match a summary.
- **LightRAG** (lesson 42.3, `03a_light_rag.ipynb`) combines through a graph. One extraction call per chunk yields entities and relationships, merged by lower-cased name. A question is split into low-level keywords (searched against entities, then their neighbours) and high-level keywords (searched against relationships), and the answer is written from the matched entities, relationships and their source chunks. The extraction schema and answer prompt follow the module's `light_rag.py`.

What to watch:

- Indexing cost differs by system: flat RAG makes no model calls to index, RAPTOR one per cluster, LightRAG one per chunk. The notebook records indexing seconds and model tokens for each.
- The judge is a model with its own errors. Its prompt is printed in the notebook, it never sees which system wrote an answer, and its one-sentence reason is printed for every score below 4.
- Entity merging is by lower-cased name only, as in the module's code, so "Business plan" and "Business" stay two nodes.

## How to run

- Environment: the default one (`uv sync`).
- Keys: `EXPERIENTIALLABS_API_KEY` (chat model, through `get_experientiallabs_llm()`), and `DATABRICKS_HOST` with `DATABRICKS_TOKEN` (embeddings, through `get_embeddings()`, whose default is `databricks-gte-large-en`).
- No Docker.
- Run `solution/m42_solution.ipynb` top to bottom from the `solution/` folder.

## Data

See [data/README.md](data/README.md): the shared `larkspur/` copy and `global_questions.jsonl` (ten global questions with reference answers).

## Results

Not run yet. The table is filled from a real run of the solution, with its date and models.

| System | Mean judge score (1 to 5) | Median query seconds | Index seconds | Index model tokens |
|---|---|---|---|---|
| Flat RAG | *pending run* | *pending run* | *pending run* | *pending run* |
| RAPTOR | *pending run* | *pending run* | *pending run* | *pending run* |
| LightRAG | *pending run* | *pending run* | *pending run* | *pending run* |

Run date: *pending run*. Chat model: *pending run*. Embeddings: *pending run*.

Back to the module: [README.md](../README.md)
