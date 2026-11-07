# Lab: M08 LangGraph Core: Graphs, State & Control Flow

## Brief

First graph: build a graph that classifies a question, routes it to one of two nodes, and returns a structured answer.

## Approach

The solution, [solution/m08_solution.ipynb](solution/m08_solution.ipynb), builds a `StateGraph` with three nodes. `classify` labels a Larkspur question billing, technical or general with structured output; a conditional edge sends billing questions to `billing_answer`, which searches only the billing, refunds and SLA files, and the rest to `support_answer`, which searches the whole handbook. Each answer node returns a Pydantic `Answer` with its source files. The graph is drawn with `get_graph().draw_mermaid()` and run on 10 golden questions.

- **Nodes return only what they change.** `classify` writes `category`; the answer nodes write `node` and `answer` (lesson 8.1).
- **List the destinations.** `add_conditional_edges("classify", route, [...])` makes an unknown route fail loudly and puts both branches in the drawing (lesson 8.2).
- **Type the labels.** The classifier's `Literal` field means it can only return one of the three categories, so the router never sees a fourth.
- **Validate node output inside the node.** The state schema checks nothing a node writes, so the structured answer comes from `with_structured_output` in the node (lesson 8.3).

## How to run

- Environment: the default `uv sync`; no extra group.
- Keys: `EXPERIENTIALLABS_API_KEY`, read from the repository's `.env` (template: `.env.example`). Docker: none.
- Execute in place: `uv run jupyter nbconvert --to notebook --execute p03_llm_application_frameworks/m08_langgraph_core/lab/solution/m08_solution.ipynb --output /tmp/m08_run.ipynb`

## Data

`data/larkspur/`, a byte-for-byte copy of the course corpus. See [data/README.md](data/README.md).

## Results

Not run yet; the owner runs the solution and fills this table with the run date and the model. The notebook prints the Mermaid drawing and every question's route and answer.

| Category | Node | Questions (of 10) |
|---|---|---|
| billing | `billing_answer` | *pending run* |
| technical | `support_answer` | *pending run* |
| general | `support_answer` | *pending run* |

Back to the module: [README.md](../README.md)
