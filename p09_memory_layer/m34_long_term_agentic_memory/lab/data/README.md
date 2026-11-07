# M34 lab data

Read by [`../solution/m34_solution.ipynb`](../solution/m34_solution.ipynb).

| File | What it is | Source and licence |
|---|---|---|
| [`larkspur/`](larkspur/README.md) | Copy of `data/larkspur/`, unchanged: the Larkspur Cloud handbook (13 files) and the 30-question golden set | Written for this course; fictional; the repository's licence |
| [`preferences.jsonl`](preferences.jsonl) | Six first-thread messages from one user (`turn`, `user_id`, `thread`, `text`, `states`), each stating one preference or fact | Written for this course; fictional; the repository's licence |

`larkspur/` must stay byte-identical to `data/larkspur/`; `tests/test_labs.py` checks it. Lab-specific files sit beside it, never inside it.
