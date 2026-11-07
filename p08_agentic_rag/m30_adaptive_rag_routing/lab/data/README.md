# M30 lab data

Read by [`../solution/m30_solution.ipynb`](../solution/m30_solution.ipynb).

| File | What it is | Source and licence |
|---|---|---|
| [`larkspur/`](larkspur/README.md) | Copy of `data/larkspur/`, unchanged: the Larkspur Cloud handbook (13 files) and the 30-question golden set | Written for this course; fictional; the repository's licence |
| [`kb/billing/`](kb/billing), [`kb/technical/`](kb/technical), [`kb/general/`](kb/general) | The 13 handbook files split by section: billing holds billing, refunds and SLA credits; technical holds outages, backups, data export, security, API limits and regions; general holds plans, account deletion, support tiers and onboarding. Each file is an unchanged copy from `larkspur/handbook/` | Written for this course; fictional; the repository's licence |
| [`tickets.jsonl`](tickets.jsonl) | 40 tickets (`id`, `text`, `route`, `sentiment`): 14 billing, 14 technical, 12 general; 12 negative, 22 neutral, 6 positive. Labels were written by the author | Written for this course; the repository's licence |

`larkspur/` must stay byte-identical to `data/larkspur/`; `tests/test_labs.py` checks it. Lab-specific files sit beside it, never inside it.
