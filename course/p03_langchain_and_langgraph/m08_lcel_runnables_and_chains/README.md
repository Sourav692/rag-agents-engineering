# M08 — LCEL, Runnables & Chains

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part III · LangChain & LangGraph Fundamentals** · **Level:** Foundation · **Time:** ~3 h · **Notebooks:** 7 mandatory, 5 optional

## Why it matters

Every RAG chain in Parts IV–VII is an LCEL pipeline: retriever | prompt | model | parser. Summarization chains are also the first taste of map-reduce over documents.

## Learning objectives

- Compose Runnables with the pipe operator and run them with invoke, batch and stream
- Branch, route and merge chains
- Migrate pre-1.x chain classes to LCEL
- Summarise long documents with stuff, map-reduce and refine

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 8.1 | LCEL and the Runnable interface | [`01a_LCEL_Introduction.ipynb`](notebooks/01a_LCEL_Introduction.ipynb)<br>[`01b_Runnables.ipynb`](notebooks/01b_Runnables.ipynb) | — |
| 8.2 | LCEL deep dive | [`02a_LCEL_Deepdive.ipynb`](notebooks/02a_LCEL_Deepdive.ipynb) | [`02b_LCEL_and_Runnables.ipynb`](optional/02b_LCEL_and_Runnables.ipynb) *(alternate)* |
| 8.3 | Branching, routing and merging chains | [`03a_Branching_Routing_Merging_Chains.ipynb`](notebooks/03a_Branching_Routing_Merging_Chains.ipynb) | — |
| 8.4 | Legacy chains and migration to LCEL | [`04a_Chain_Migrations.ipynb`](notebooks/04a_Chain_Migrations.ipynb) | [`04b_Basics_of_Chains.ipynb`](optional/04b_Basics_of_Chains.ipynb) *(extension)*<br>[`04c_Chains_Basics_and_OutputParsers.ipynb`](optional/04c_Chains_Basics_and_OutputParsers.ipynb) *(extension)*<br>[`04d_Advanced_Chains.ipynb`](optional/04d_Advanced_Chains.ipynb) *(extension)*<br>[`04e_Chain_Migration_Advanced.ipynb`](optional/04e_Chain_Migration_Advanced.ipynb) *(extension)* |
| 8.5 | Summarization: stuff, map-reduce, refine | [`05a_Summarization_Essentials.ipynb`](notebooks/05a_Summarization_Essentials.ipynb)<br>[`05b_Doc_Chains_to_LCEL_LangChain_v1.ipynb`](notebooks/05b_Doc_Chains_to_LCEL_LangChain_v1.ipynb) | — |

## Hands-on lab

Chain rewrite: rebuild one legacy chain as LCEL, add a branch that routes short and long inputs differently, and compare outputs. Details: [lab/README.md](lab/README.md).

## Key concepts

Runnable interface · Pipe composition · RunnableParallel / Branch · Map-reduce summarisation

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
| `notebooks/01a_LCEL_Introduction.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/03_lcel_and_runnables/notebooks/01_LCEL_Introduction.ipynb` |
| `notebooks/01b_Runnables.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/03_lcel_and_runnables/notebooks/02_Runnables.ipynb` |
| `notebooks/02a_LCEL_Deepdive.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/03_lcel_and_runnables/notebooks/03_LCEL_Deepdive.ipynb` |
| `optional/02b_LCEL_and_Runnables.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/03_lcel_and_runnables/notebooks/04_LCEL_and_Runnables.ipynb` |
| `notebooks/03a_Branching_Routing_Merging_Chains.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/03_lcel_and_runnables/notebooks/05_Branching_Routing_Merging_Chains.ipynb` |
| `notebooks/04a_Chain_Migrations.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/04_legacy_chains_and_migration/notebooks/04_Chain_Migrations.ipynb` |
| `optional/04b_Basics_of_Chains.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/04_legacy_chains_and_migration/notebooks/01_Basics_of_Chains.ipynb` |
| `optional/04c_Chains_Basics_and_OutputParsers.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/04_legacy_chains_and_migration/notebooks/02_Chains_Basics_and_OutputParsers.ipynb` |
| `optional/04d_Advanced_Chains.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/04_legacy_chains_and_migration/notebooks/03_Advanced_Chains.ipynb` |
| `optional/04e_Chain_Migration_Advanced.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/04_legacy_chains_and_migration/notebooks/05_Chain_Migration_Advanced.ipynb` |
| `notebooks/05a_Summarization_Essentials.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/05_summarization/notebooks/01_Summarization_Essentials.ipynb` |
| `notebooks/05b_Doc_Chains_to_LCEL_LangChain_v1.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/05_summarization/notebooks/02_Doc_Chains_to_LCEL_LangChain_v1.ipynb` |
