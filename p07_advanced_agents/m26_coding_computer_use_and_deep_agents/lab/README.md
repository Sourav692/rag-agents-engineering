# Lab: M26 Coding, Computer-Use & Deep Agents

## Brief

Coding agent: give a deep agent a developer sub-agent and a tester sub-agent, ask it for a small Python function with tests, and log each iteration until the tests pass.

## Solution

[`solution/m26_solution.ipynb`](solution/m26_solution.ipynb) builds a deep agent with a developer sub-agent and a tester sub-agent (`create_deep_agent`, as in `03a_simple_coding_agent.py`), asks it for the refund calculator in `data/spec.md`, runs pytest in a temporary folder after each iteration, and stops when the tests pass or after 5 iterations.

## Approach

- A deep agent is one orchestrator inside a harness: file tools, a `task` tool that runs each sub-agent in its own context, a backend and a checkpointer. Only a sub-agent's final message returns to the orchestrator (lesson 26.3).
- `FilesystemBackend(virtual_mode=True)` anchors paths in the workspace and blocks `..`, but it provides no process isolation and cannot run commands. The tests therefore run in the notebook, outside the agent, and their report is the observation the agent gets back: tests are the reward signal (lesson 26.1).
- The iteration cap is a loop bound in code. The tester's own tests can be wrong, so the notebook also checks the spec's worked examples, typed in by hand.
- The test runner is a fresh process with a timeout, no keyboard and no keys in its environment. Like `python_runner.py`, that is a guard, not a sandbox: run the lab in a throwaway environment.

## How to run

- Environment: the default uv environment (`uv sync`, whose default `dev` group brings Jupyter and the pytest the test runner calls); no extra group and no Docker.
- Keys, read from the repository's `.env`: `EXPERIENTIALLABS_API_KEY` for the chat model (`get_experientiallabs_llm()`); the solution makes no embedding calls.
- Open [`solution/m26_solution.ipynb`](solution/m26_solution.ipynb) in Jupyter (`uv run jupyter lab`) and run it from the `solution/` folder, or from there: `uv run jupyter nbconvert --to notebook --execute m26_solution.ipynb --output /tmp/m26_run.ipynb`.
- Clear outputs before committing: `uv run nbstripout m26_solution.ipynb`.

## Data

The notebook reads only [`data/`](data/README.md); [`data/README.md`](data/README.md) names each file's source and licence.

## Results

Not run yet: the owner runs the solutions. Each cell is filled from a real run, with its date and models.

- Run date: *pending run*
- Models: *pending run*

| Iteration | Sub-agents called | Pytest summary |
|---|---|---|
| *pending run* | *pending run* | *pending run* |

Independent check of the spec's seven worked examples: *pending run*.

Back to the part: [README.md](../../README.md)
