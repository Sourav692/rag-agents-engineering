# M27 lab data

Read by [`../solution/m27_solution.ipynb`](../solution/m27_solution.ipynb).

| File | What it is | Source and licence |
|---|---|---|
| [`larkspur/`](larkspur/README.md) | Copy of `data/larkspur/`, unchanged: the Larkspur Cloud handbook (13 files) and the 30-question golden set | Written for this course; fictional; the repository's licence |
| [`catalogue.csv`](catalogue.csv) | 25 products: Small, Medium and Large servers in the five regions (vCPUs, memory and traffic from `larkspur/handbook/03_plans.md`) and 10 add-ons. Prices and add-ons are invented for this lab and are not handbook facts | Written for this course; fictional; the repository's licence |
| [`questions.jsonl`](questions.jsonl) | 20 questions (`id`, `type`, `question`, `answer`): 7 `lookup`, 6 `filter`, 7 `aggregate`. Each answer was computed from the CSV with pandas | Written for this course; the repository's licence |

`larkspur/` must stay byte-identical to `data/larkspur/`; `tests/test_labs.py` checks it. Lab-specific files sit beside it, never inside it.
