# Lab: M19 End-to-End RAG Systems

## Brief

Module lab, AI research assistant: package ingestion, retrieval, structured answers with citations and session history into one class (05/10/11).

## Approach

- Grounded generation has three parts: evidence retrieved for this question, an instruction to use only that evidence, and permission to say "I don't know".
- Citations are structured output (a source and a quote per passage used). Check every quote against its chunk in code, because a paraphrased quote looks fine on the page and points at nothing.
- Session history needs a rewrite step: a follow-up such as "Does that apply to monthly plans too?" retrieves poorly on its own, so the class rewrites it into a standalone question first.
- The reference build is [`lab_ai_research_assistant.ipynb`](../mandatory/notebook/lab_ai_research_assistant.ipynb) in this module. The solution follows its shape (one class, ingestion, retrieval, structured answers, sessions) on the Larkspur handbook, with in-memory FAISS instead of a persisted Chroma store.

## How to run

The worked solution is [solution/m19_solution.ipynb](solution/m19_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`.

Keys, as environment variables in the `.env` file at the repo root: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`), `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings (`get_embeddings()`).

## Data

The solution reads the Larkspur Cloud handbook and its 30-question golden set from `data/larkspur/`, an unchanged copy of the repository's corpus. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date and models | *pending run* |
| Chunks ingested | *pending run* |
| Three turns: standalone question, answer, confidence | *pending run* |
| Citations per turn and how many were verified in the retrieved chunks | *pending run* |

Back to the module: [README.md](../README.md)
