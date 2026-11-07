# Lab: M01 Python & Data Toolkit Refresher

## Brief

Data warm-up: load a CSV into pandas and into SQLite, answer five questions both ways, and expose one of them through a small Flask endpoint.

## Approach

The solution, [solution/m01_solution.ipynb](solution/m01_solution.ipynb), loads the churn CSV into a pandas DataFrame and into an in-memory SQLite table, then answers five questions twice and asserts that both answers agree.

- **Check the frame first.** `df.info()` shows the dtypes and the missing values. `groupby` drops `NaN` keys and `mean()` skips `NaN` without a warning, so the SQL side needs `WHERE ... IS NOT NULL` to match (lesson 1.3).
- **Parameters, not f-strings.** The age threshold reaches SQL as the second argument to `execute`, so the driver sends it as data (lesson 1.4).
- **Order is part of the answer.** Both sides sort on every column that can tie before the comparison.
- **The route.** A Flask `GET /churn-rate?min_age=` reuses the parameterised query, returns 400 on a bad value, and is called through `app.test_client()`, so no server is left running (lesson 1.5 notebooks).

## How to run

- Environment: the default `uv sync`; no extra group.
- Keys: none. Docker: none.
- Open the notebook in Jupyter from the repository's environment and run all cells, or execute it in place:
  `uv run jupyter nbconvert --to notebook --execute p01_ai_engineering_foundations/m01_python_data_refresher/lab/solution/m01_solution.ipynb --output /tmp/m01_run.ipynb`

## Data

`data/churn_prediction.csv`, copied from the module's `assets/`. Source and licence: [data/README.md](data/README.md).

## Results

Not run yet; the owner runs the solution and fills this table with the run date.

| Question | pandas == SQL | Answer |
|---|---|---|
| Q1 customers and churned | *pending run* | *pending run* |
| Q2 churn rate by gender | *pending run* | *pending run* |
| Q3 average balance by occupation | *pending run* | *pending run* |
| Q4 churn rate at age 60 or over | *pending run* | *pending run* |
| Q5 five cities with the most customers | *pending run* | *pending run* |
| Flask `GET /churn-rate?min_age=60` | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
