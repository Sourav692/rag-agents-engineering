# M33 lab data

Read by [`../solution/m33_solution.ipynb`](../solution/m33_solution.ipynb).

| File | What it is | Source and licence |
|---|---|---|
| [`larkspur/`](larkspur/README.md) | Copy of `data/larkspur/`, unchanged: the Larkspur Cloud handbook (13 files) and the 30-question golden set | Written for this course; fictional; the repository's licence |
| [`conversations.jsonl`](conversations.jsonl) | 15 three-turn conversations (`id`, `turns`); each turn has `question` and `evidence_spans`, exact substrings of the handbook, checked when the file was written | Written for this course; the repository's licence |

`larkspur/` must stay byte-identical to `data/larkspur/`; `tests/test_labs.py` checks it. Lab-specific files sit beside it, never inside it.
