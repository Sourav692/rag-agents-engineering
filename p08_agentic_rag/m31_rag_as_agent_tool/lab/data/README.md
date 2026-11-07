# M31 lab data

Read by [`../solution/m31_solution.ipynb`](../solution/m31_solution.ipynb).

| File | What it is | Source and licence |
|---|---|---|
| [`larkspur/`](larkspur/README.md) | Copy of `data/larkspur/`, unchanged: the Larkspur Cloud handbook (13 files) and the 30-question golden set | Written for this course; fictional; the repository's licence |
| [`mixed_questions.jsonl`](mixed_questions.jsonl) | 20 questions (`id`, `question`, `tool`): 10 need the handbook (`docs`), 10 need the web (`web`) | Written for this course; the repository's licence |

`larkspur/` must stay byte-identical to `data/larkspur/`; `tests/test_labs.py` checks it. Lab-specific files sit beside it, never inside it.
