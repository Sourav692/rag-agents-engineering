# M29 lab data

Read by [`../solution/m29_solution.ipynb`](../solution/m29_solution.ipynb).

| File | What it is | Source and licence |
|---|---|---|
| [`larkspur/`](larkspur/README.md) | Copy of `data/larkspur/`, unchanged: the Larkspur Cloud handbook (13 files) and the 30-question golden set | Written for this course; fictional; the repository's licence |
| [`ooc_questions.jsonl`](ooc_questions.jsonl) | 10 more out-of-corpus questions, in the golden set's format (`evidence_spans` empty, `reference_answer` "The handbook does not say."). The notebook adds the golden set's 5 | Written for this course; the repository's licence |

`larkspur/` must stay byte-identical to `data/larkspur/`; `tests/test_labs.py` checks it. Lab-specific files sit beside it, never inside it.
