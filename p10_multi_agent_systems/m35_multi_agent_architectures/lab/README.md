# Lab: M35 Multi-Agent Architectures

## Brief

Specialist retrievers: replace the single router from M30 with a supervisor over three specialist RAG agents and compare routing accuracy and cost.

Solution: [solution/m35_solution.ipynb](solution/m35_solution.ipynb).

## Approach

The handbook is split into three knowledge bases (billing, technical, general), each behind its own retriever. Two systems answer the same 40 tickets:

- **Single router.** One structured-output call returns a `Literal` route, then one call answers from that base. Two model calls per ticket, every time.
- **Supervisor.** A LangGraph `StateGraph` in the shape of notebook `04a_supervisor_pattern.ipynb`: the supervisor picks a specialist, the specialist answers, control returns to the supervisor, which finishes or tries another base. The module page counts the cost of this shape: a supervisor decides every step and takes control back, so it spends calls on routing and buys one place to log, test and cap every decision.

What to watch:

- Score routing on the first base each system picks, so the two numbers measure the same decision.
- The supervisor's turn cap lives in the router function (`MAX_TURNS = 3`) and a `recursion_limit` backs it up; a prompt alone does not stop a loop.
- Retrieval is offline TF-IDF (`lab_kit.tfidf_retriever`), so any cost difference comes from model calls. Token counts come from `UsageMetadataCallbackHandler`; set `PRICE_PER_MILLION_TOKENS_USD` from your provider's price page to turn them into money.

## How to run

- Environment: the default one (`uv sync`).
- Keys: `EXPERIENTIALLABS_API_KEY` (chat model, through `get_experientiallabs_llm()`).
- No Docker.
- Run `solution/m35_solution.ipynb` top to bottom from the `solution/` folder.

## Data

See [data/README.md](data/README.md): `kb/billing/`, `kb/technical/`, `kb/general/` (handbook files, unchanged) and `tickets.jsonl` (40 tickets labelled with route and sentiment), plus the shared `larkspur/` copy.

## Results

Not run yet. The table is filled from a real run of the solution, with its date and model.

| System | Routing accuracy | Model calls per ticket | Tokens per ticket | Seconds per ticket |
|---|---|---|---|---|
| Single router | *pending run* | *pending run* | *pending run* | *pending run* |
| Supervisor | *pending run* | *pending run* | *pending run* | *pending run* |

Run date: *pending run*. Model: *pending run*.

Back to the module: [README.md](../README.md)
