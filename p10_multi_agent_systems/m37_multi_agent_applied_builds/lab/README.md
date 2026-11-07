# Lab: M37 Multi-Agent Applied Builds

## Brief

Research team: build a supervisor with a RAG researcher, a web researcher and a writer that cites sources, then test it on edge cases (no results, conflicting sources, tool failure).

Solution: [solution/m37_solution.ipynb](solution/m37_solution.ipynb).

## Approach

The team is a LangGraph supervisor in the shape of notebook `04a_supervisor_financial_research.ipynb`: the supervisor writes `next` into state with a typed decision, and a pure function follows it. Lesson 37.4's theory page names a mechanism for each edge case, and the solution uses them:

| Edge case | Mechanism in the solution | From |
|---|---|---|
| No results | The RAG researcher keeps only chunks above a relevance floor; when none clears it, it returns no findings and makes no model call | 04b |
| Conflicting sources | Every finding keeps its source id (`handbook/<file>`, `forum/conflicting.md` or a URL), so the writer can cite both and name the handbook as policy | 04c |
| Tool failure | The web researcher catches the exception and writes it to `errors`; the router caps the run at `MAX_SUPERVISOR_TURNS` and always ends at the writer | 02c, 04a |

What to watch:

- The caps are in `route()`, not in the supervisor prompt: no worker runs twice, and the writer runs when the turn budget is spent.
- The writer's citations are checked in code against the sources the researchers returned (`unverified_citations`), the early sign of an invented source that the module's interview questions describe.
- Larkspur Cloud is fictional, so real web results will not mention it. The no-results case swaps in an empty search and the tool-failure case a search that raises, so neither depends on the live web.
- The relevance floor is a TF-IDF cosine of 0.1, chosen by reading the top scores of the lab's questions; lexical scores do not separate every out-of-corpus question from an answerable one, which is why the no-results case uses `g29`.

## How to run

- Environment: the default one (`uv sync`).
- Keys: `EXPERIENTIALLABS_API_KEY` (chat model, through `get_experientiallabs_llm()`) and `TAVILY_API_KEY` (web researcher).
- No Docker.
- Run `solution/m37_solution.ipynb` top to bottom from the `solution/` folder.

## Data

See [data/README.md](data/README.md): the shared `larkspur/` copy and `conflicting.md`, a fictional forum post that contradicts the handbook's refund time.

## Results

Not run yet. The table is filled from a real run of the solution, with its date and model.

| Case | Expected | Path | Findings | Errors | Citations | Unverified | Conflicts | Policy source |
|---|---|---|---|---|---|---|---|---|
| Baseline (g06) | Cited handbook answer | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| No results (g29) | Says no answer, no citations | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| Conflicting sources | Both sources cited, handbook named as policy | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| Tool failure (g12) | Error recorded, answer from handbook | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |

Run date: *pending run*. Model: *pending run*.

Back to the module: [README.md](../README.md)
