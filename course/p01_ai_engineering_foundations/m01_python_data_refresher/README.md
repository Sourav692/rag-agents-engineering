# M01 — Python & Data Toolkit Refresher

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part I · AI Engineering Foundations** · **Level:** Foundation · **Time:** ~3 h · **Notebooks:** 3 mandatory, 12 optional

## Why it matters

RAG and agent code leans on a small set of Python tools: NumPy arrays for embeddings, pandas for tabular data, SQL for structured retrieval and asyncio for concurrent calls. Skim what you know and practise the rest.

## Theory

Read the [theory page](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Concurrent calls with asyncio](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/06_concurrency_threads_processes_the_gil_and_asyncio_22_runnable_scripts/interactive/asyncio-concurrency-lab.html) (open the file in a browser)

## Learning objectives

- Write idiomatic Python: data types, control flow, functions and PEP 8
- Work with arrays and tables in NumPy and pandas, and plot results with Matplotlib
- Query SQLite, MySQL and PostgreSQL from Python
- Serve data through a Flask API
- Explain threads, processes, the GIL and asyncio, and avoid race conditions and deadlocks

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 1.1 | Python essentials: variables, operators, control flow, functions *(optional lesson)* | — | [`01a_implementing_variables_in_python.ipynb`](optional/01a_implementing_variables_in_python.ipynb) *(extension)*<br>[`01b_implementation_of_operators_in_python.ipynb`](optional/01b_implementation_of_operators_in_python.ipynb) *(extension)*<br>[`01c_implementing_conditional_statements.ipynb`](optional/01c_implementing_conditional_statements.ipynb) *(extension)*<br>[`01d_looping_constructs.ipynb`](optional/01d_looping_constructs.ipynb) *(extension)*<br>[`01e_implementing_functions_in_python.ipynb`](optional/01e_implementing_functions_in_python.ipynb) *(extension)* |
| 1.2 | Python best practices *(optional lesson)* | — | [`02a_python_best_practices.ipynb`](optional/02a_python_best_practices.ipynb) *(extension)* |
| 1.3 | NumPy, pandas and Matplotlib ([theory](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/03_numpy_pandas_and_matplotlib/README.md)) | [`03a_numpy_basics.ipynb`](notebooks/03a_numpy_basics.ipynb)<br>[`03b_pandas_basics_for_data_analysis.ipynb`](notebooks/03b_pandas_basics_for_data_analysis.ipynb) | [`03c_matplotlib_basics.ipynb`](optional/03c_matplotlib_basics.ipynb) *(extension)* |
| 1.4 | Databases from Python: SQLite, MySQL, PostgreSQL ([theory](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/04_databases_from_python_sqlite_mysql_postgresql/README.md)) | [`04a_sqlite_operations.ipynb`](notebooks/04a_sqlite_operations.ipynb) | [`04b_mysql_connection.ipynb`](optional/04b_mysql_connection.ipynb) *(platform-specific)*<br>[`04c_postgresdb_connection.ipynb`](optional/04c_postgresdb_connection.ipynb) *(platform-specific)* |
| 1.5 | Serving data with Flask APIs *(optional lesson)* | — | [`05a_creating_and_accessing_apis_with_flask.ipynb`](optional/05a_creating_and_accessing_apis_with_flask.ipynb) *(extension)*<br>[`05b_stock_market_api_endpoints.ipynb`](optional/05b_stock_market_api_endpoints.ipynb) *(extension)* |
| 1.6 | Concurrency: threads, processes, the GIL and asyncio (22 runnable scripts) *(optional lesson)* ([theory](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/06_concurrency_threads_processes_the_gil_and_asyncio_22_runnable_scripts/README.md)) | — | [`06a_concurrency_scripts`](optional/06a_concurrency_scripts) *(extension)* |

## Hands-on lab

Data warm-up: load a CSV into pandas and into SQLite, answer five questions both ways, and expose one of them through a small Flask endpoint. Details: [lab/README.md](lab/README.md).

## Key concepts

[NumPy arrays](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/03_numpy_pandas_and_matplotlib/README.md#numpy-arrays) · [pandas DataFrames](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/03_numpy_pandas_and_matplotlib/README.md#pandas-dataframes) · [SQL from Python](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/04_databases_from_python_sqlite_mysql_postgresql/README.md#sql-from-python) · [asyncio](../../../theory/p01_ai_engineering_foundations/m01_python_data_refresher/06_concurrency_threads_processes_the_gil_and_asyncio_22_runnable_scripts/README.md#asyncio)

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
| `optional/01a_implementing_variables_in_python.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/01_python_for_ai_engineering/notebooks/01_implementing_variables_in_python.ipynb` |
| `optional/01b_implementation_of_operators_in_python.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/01_python_for_ai_engineering/notebooks/02_implementation_of_operators_in_python.ipynb` |
| `optional/01c_implementing_conditional_statements.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/01_python_for_ai_engineering/notebooks/03_implementing_conditional_statements.ipynb` |
| `optional/01d_looping_constructs.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/01_python_for_ai_engineering/notebooks/04_looping_constructs.ipynb` |
| `optional/01e_implementing_functions_in_python.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/01_python_for_ai_engineering/notebooks/05_implementing_functions_in_python.ipynb` |
| `optional/02a_python_best_practices.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/01_python_for_ai_engineering/notebooks/06_python_best_practices.ipynb` |
| `notebooks/03a_numpy_basics.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/02_files_data_and_apis/notebooks/01_numpy_basics.ipynb` |
| `notebooks/03b_pandas_basics_for_data_analysis.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/02_files_data_and_apis/notebooks/02_pandas_basics_for_data_analysis.ipynb` |
| `optional/03c_matplotlib_basics.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/02_files_data_and_apis/notebooks/03_matplotlib_basics.ipynb` |
| `notebooks/04a_sqlite_operations.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/02_files_data_and_apis/notebooks/04_sqlite_operations.ipynb` |
| `optional/04b_mysql_connection.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/02_files_data_and_apis/notebooks/05_mysql_connection.ipynb` |
| `optional/04c_postgresdb_connection.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/02_files_data_and_apis/notebooks/06_postgresdb_connection.ipynb` |
| `optional/05a_creating_and_accessing_apis_with_flask.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/02_files_data_and_apis/notebooks/07_creating_and_accessing_apis_with_flask.ipynb` |
| `optional/05b_stock_market_api_endpoints.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/02_files_data_and_apis/notebooks/08_stock_market_api_endpoints.ipynb` |
| `optional/06a_concurrency_scripts` | `ai-engineering-demystified-01-foundations` | `modules/03_concurrency_and_asyncio/notebooks` |
