# Lab: M43 Knowledge Graphs with Neo4j

## Brief

Domain KG: extract a graph from 20 documents in your domain, load it into Neo4j, and answer five multi-hop questions that vector RAG gets wrong.

Solution: [solution/m43_solution.ipynb](solution/m43_solution.ipynb), with [solution/docker-compose.yml](solution/docker-compose.yml) for Neo4j.

## Approach

The corpus is the 13 Larkspur handbook files plus seven internal records (three teams, four incidents). The records are written so that every question needs a join: an incident names a service and a region, a team record names the services it owns and the regions it is on call for, and only the two together say who was responsible.

- **Extraction.** `LLMGraphTransformer` with `allowed_nodes` (`Team`, `Person`, `Service`, `Region`, `Incident`), `allowed_relationships` as typed triples (`LEADS`, `OWNS`, `ON_CALL_FOR`, `AFFECTED`, `IN_REGION`) and `strict_mode=True`, so anything outside the schema is dropped. Incidents keep `date` and `availability` as properties. `Neo4jGraph.add_graph_documents` loads the result, as notebook `05b_create_kg_from_text.ipynb` does.
- **Graph route.** Hand-written Cypher first checks that each question's path exists in the extracted graph. Then `GraphCypherQAChain` (lesson 43.3, text-to-Cypher) writes and runs a query per question; its rows, plus the two closest handbook passages for policy text the schema does not model, go to one answer call.
- **Vector route.** The same 20 documents, chunked and embedded, top 4 chunks, one answer call.

What to watch:

- A graph answers only as far as extraction built it. If a hand-written path query returns no rows, fix the extraction (schema, prompt, model) before blaming Cypher generation.
- `GraphCypherQAChain` runs model-written Cypher against the database, which is why it needs `allow_dangerous_requests=True`; use a read-only user for anything but a local container.
- For every vector failure the notebook lists the documents on the answer's path that top-k retrieval never returned, which is the usual cause.

## How to run

- Environment: the default one (`uv sync`; `langchain-neo4j`, `neo4j` and `langchain-experimental` are default dependencies).
- Docker: from `solution/`, run `docker compose up -d` to start Neo4j 5 with APOC (browser at `http://localhost:7474`, Bolt at `bolt://localhost:7687`, user `neo4j`, password `larkspur-lab`). `docker compose down -v` removes it and its volume.
- Keys: `EXPERIENTIALLABS_API_KEY` (chat model), and `DATABRICKS_HOST` with `DATABRICKS_TOKEN` (embeddings, through `get_embeddings()`). Optional: `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD` to use another Neo4j; the defaults match the compose file.
- Run `solution/m43_solution.ipynb` top to bottom from the `solution/` folder. It deletes every node in the database before loading, so do not point it at a database you want to keep.

## Data

See [data/README.md](data/README.md): the shared `larkspur/` copy, `extra_docs/` (seven fictional team and incident records) and `multihop.jsonl` (five multi-hop questions with reference answers and the documents on each answer's path).

## Results

Not run yet. The table is filled from a real run of the solution, with its date and models.

| Question | Graph route score (1 to 5) | Vector route score (1 to 5) | Path documents vector RAG missed |
|---|---|---|---|
| m1 | *pending run* | *pending run* | *pending run* |
| m2 | *pending run* | *pending run* | *pending run* |
| m3 | *pending run* | *pending run* | *pending run* |
| m4 | *pending run* | *pending run* | *pending run* |
| m5 | *pending run* | *pending run* | *pending run* |

Run date: *pending run*. Chat model: *pending run*. Embeddings: *pending run*. Graph extraction time: *pending run*.

Back to the module: [README.md](../README.md)
