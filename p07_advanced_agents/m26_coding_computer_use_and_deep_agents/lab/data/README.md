# M26 lab data

Read by [`../solution/m26_solution.ipynb`](../solution/m26_solution.ipynb).

| File | What it is | Source and licence |
|---|---|---|
| [`larkspur/`](larkspur/README.md) | Copy of `data/larkspur/`, unchanged: the Larkspur Cloud handbook (13 files) and the 30-question golden set | Written for this course; fictional; the repository's licence |
| [`spec.md`](spec.md) | The function to build: a Larkspur refund-amount calculator. Its three rules quote `larkspur/handbook/02_refunds.md`; the decisions the handbook leaves open (month length, rounding, input checks) are written for this lab | Written for this course; the repository's licence |

`larkspur/` must stay byte-identical to `data/larkspur/`; `tests/test_labs.py` checks it. Lab-specific files sit beside it, never inside it.
