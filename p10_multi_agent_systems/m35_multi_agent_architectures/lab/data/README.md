# M35 lab data

All files were written for this course and carry the repository's licence. Larkspur Cloud is fictional.

| Path | Source | Licence |
|---|---|---|
| [larkspur/](larkspur/README.md) | Unchanged copy of `data/larkspur/` (handbook and golden set) | Repository licence |
| [kb/billing/](kb/billing/) | Handbook files `01_billing.md`, `02_refunds.md`, `12_sla_credits.md`, copied unchanged | Repository licence |
| [kb/technical/](kb/technical/) | Handbook files `04_outages_and_status.md`, `05_backups.md`, `06_data_export.md`, `08_security.md`, `09_api_limits.md`, `11_regions.md`, copied unchanged | Repository licence |
| [kb/general/](kb/general/) | Handbook files `03_plans.md`, `07_account_deletion.md`, `10_support_tiers.md`, `13_onboarding.md`, copied unchanged | Repository licence |
| [tickets.jsonl](tickets.jsonl) | 40 customer tickets written by the author, one per line: `id`, `text`, `route` (`billing` 14, `technical` 14, `general` 12: the knowledge base that holds the answer) and `sentiment` (`negative` 12, `neutral` 22, `positive` 6) | Repository licence |

`kb/` and `tickets.jsonl` are byte-identical copies of the M30 lab's files (`p08_agentic_rag/m30_adaptive_rag_routing/lab/data/`), so the two labs' routing results compare.
