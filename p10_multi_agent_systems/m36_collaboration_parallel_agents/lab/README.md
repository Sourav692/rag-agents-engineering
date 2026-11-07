# Lab: M36 Collaboration, Control & Parallel Agents

## Brief

Parallel retrieval: run the sub-questions of a decomposed query as parallel agents and stream partial answers, then report the latency saved.

Solution: [solution/m36_solution.ipynb](solution/m36_solution.ipynb).

## Approach

A decomposer splits each multi-hop question into two to four sub-questions. Each sub-question goes to a retrieval agent (TF-IDF top 3 over the handbook, then one answer call), and a synthesizer joins the partial answers.

- **Parallel graph.** A conditional edge from `START` returns one `Send("agent", ...)` per sub-question, as in notebook `05a_parallel_agents.ipynb`. LangGraph runs every branch of a superstep at once, and the next step starts when the slowest branch ends.
- **Sequential graph.** One node answers the same sub-questions in turn.

What to watch:

- The branches share one key, `partials`, so it needs a reducer (`operator.add`); without one the run raises `InvalidUpdateError`, as the module page warns.
- Both graphs get the same sub-questions from one decomposition, so the timing difference is the fan-out alone. The order of the two runs alternates per question.
- `stream_mode="updates"` yields one update per finished node, so each agent's partial answer prints when that agent ends, before the synthesizer runs.

## How to run

- Environment: the default one (`uv sync`).
- Keys: `EXPERIENTIALLABS_API_KEY` (chat model, through `get_experientiallabs_llm()`).
- No Docker.
- Run `solution/m36_solution.ipynb` top to bottom from the `solution/` folder.

## Data

See [data/README.md](data/README.md): the shared `larkspur/` copy; the lab uses its six `multi_hop` golden questions.

## Results

Not run yet. The table is filled from a real run of the solution, with its date and model.

| Question | Sub-questions | Sequential (s) | Parallel (s) | Saved (s) |
|---|---|---|---|---|
| g02 | *pending run* | *pending run* | *pending run* | *pending run* |
| g17 | *pending run* | *pending run* | *pending run* | *pending run* |
| g18 | *pending run* | *pending run* | *pending run* | *pending run* |
| g19 | *pending run* | *pending run* | *pending run* | *pending run* |
| g20 | *pending run* | *pending run* | *pending run* | *pending run* |
| g21 | *pending run* | *pending run* | *pending run* | *pending run* |

Run date: *pending run*. Model: *pending run*.

Back to the module: [README.md](../README.md)
