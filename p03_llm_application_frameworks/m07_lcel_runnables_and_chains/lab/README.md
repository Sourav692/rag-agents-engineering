# Lab: M07 LCEL, Runnables & Chains

## Brief

Chain rewrite: rebuild one legacy chain as LCEL, add a branch that routes short and long inputs differently, and compare outputs.

## Approach

The solution, [solution/m07_solution.ipynb](solution/m07_solution.ipynb), answers 10 golden questions from three TF-IDF passages each, three ways: the legacy `LLMChain` from `langchain_classic` (the chain notebook 04a migrates), the same prompt and model as `prompt | llm | StrOutputParser()`, and a `RunnableBranch` that answers short contexts directly and condenses long ones first.

- **Migrate behind the same shape.** `LLMChain` returns a dict with the reply under `text`; the LCEL pipe returns a string. Map the output shape, switch to `.invoke()`, and compare old and new answers on a fixed question set before deleting the old class (lesson 7.4).
- **Branch on something code can measure.** The threshold is the median context length of the 10 inputs, so both routes run. `RunnableBranch` runs the first true condition, so the order of conditions decides ties (lesson 7.3).
- **Keep the question moving.** The condense step uses `RunnablePassthrough.assign(context=...)`, which replaces the context and keeps the question for the answer step (lesson 7.2).
- **What to watch.** Exact string equality at temperature 0 is the strictest check of the migration; a difference is worth reading rather than assuming. The condense route costs one extra call per long input.

## How to run

- Environment: the default `uv sync`; no extra group (`langchain-classic` is a default dependency).
- Keys: `EXPERIENTIALLABS_API_KEY`, read from the repository's `.env` (template: `.env.example`). Docker: none.
- Execute in place: `uv run jupyter nbconvert --to notebook --execute p03_llm_application_frameworks/m07_lcel_runnables_and_chains/lab/solution/m07_solution.ipynb --output /tmp/m07_run.ipynb`

## Data

`data/larkspur/`, a byte-for-byte copy of the course corpus. See [data/README.md](data/README.md).

## Results

Not run yet; the owner runs the solution and fills this table with the run date and the model. The notebook's side-by-side table holds all three answers per question.

| Route | Questions | Legacy and LCEL answers identical |
|---|---|---|
| short: answer | *pending run* | *pending run* |
| long: condense, then answer | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
