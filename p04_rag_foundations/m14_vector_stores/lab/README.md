# Lab: M14 Vector Stores & Index Operations

## Brief

Living index: stand up pgvector with Docker, ingest the M11 corpus, then change, add and delete source files and show that the record manager re-indexes only what changed.

## Approach

- A vector store cannot update text in place: new text means a new vector, so an update is a delete followed by an insert, and both need an ID that stays the same from one run to the next.
- The Indexing API hashes every chunk and records the hash with `SQLRecordManager`. Unchanged chunks are skipped, so re-running ingestion costs embeddings only for what changed, and `cleanup="incremental"` deletes a source's superseded chunks in the same run.
- What to watch: incremental cleanup works per source that appears in the batch. A file deleted from disk never appears, so its chunks stay until a `cleanup="full"` run or an explicit delete. The solution shows both runs.
- `source_id_key="source"` must be the same field on every chunk of a file; the loader cell sets it to the file name.

## How to run

The worked solution is [solution/m14_solution.ipynb](solution/m14_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Needs Docker. From `lab/solution/`: `docker compose -f docker-compose.yml up -d` starts `pgvector/pgvector:pg16` on port 5434 (user, password and database `admin`/`admin`/`vectordb`). Then run with the default environment, `uv run jupyter lab`. Afterwards: `docker compose -f docker-compose.yml down -v`.

Keys, as environment variables in the `.env` file at the repo root: `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`). No chat model is called.

## Data

The solution reads `data/mixed/`, the M11 lab's five files copied into this lab, and changes a copy of it in a temporary folder. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date and embedding model | *pending run* |
| Initial ingest: added, updated, skipped, deleted | *pending run* |
| Same folder again | *pending run* |
| One file changed | *pending run* |
| One file added | *pending run* |
| One file deleted (incremental, then full) | *pending run* |

Back to the module: [README.md](../README.md)
