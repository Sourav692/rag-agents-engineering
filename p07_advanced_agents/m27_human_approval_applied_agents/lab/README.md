# Lab: M27 Human Approval & Applied Single-Agent Builds

## Brief

SQL or vectors: answer the same 20 questions over a product catalogue with CSV RAG (M19) and with the text-to-SQL agent, and record which wins for each question type.

## Solution

[`solution/m27_solution.ipynb`](solution/m27_solution.ipynb) answers 20 catalogue questions with CSV RAG (one document per row, top 5) and with a text-to-SQL agent over a read-only SQLite copy of the CSV (`create_agent` with `SQLDatabaseToolkit`, as in `04b_text2sql_react_agent.ipynb`), grades both against the reference answers with a judge prompt, and names the winner per question type.

## Approach

- Text-to-SQL retrieves by computing over every row, which top-k vector retrieval cannot do for counts, sums and rankings (M27 theory). CSV RAG sees only the rows it retrieved.
- A text-to-SQL miss is often a schema detail or a business rule, which the system prompt has to state; here, the semicolon-separated `available_on` column.
- The workflow form of text-to-SQL costs 2 LLM calls per question and the ReAct agent several (M27 theory); the agent is used here because the brief names it.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter); no extra group and no Docker.
- Keys, read from the repository's `.env`: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), and `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the embeddings (`get_embeddings()` defaults to `databricks-gte-large-en`).
- Open [`solution/m27_solution.ipynb`](solution/m27_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m27_solution.ipynb --output /tmp/m27_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m27_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| Question type | Questions | CSV RAG correct | Text-to-SQL correct | Winner |
|---|---|---|---|---|
| lookup | 7 | *pending run* | *pending run* | *pending run* |
| filter | 6 | *pending run* | *pending run* | *pending run* |
| aggregate | 7 | *pending run* | *pending run* | *pending run* |
| all | 20 | *pending run* | *pending run* |  |

Back to the module: [README.md](../README.md)
