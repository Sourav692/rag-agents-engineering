# M45 lab data

| File | What it is | Source and licence |
|---|---|---|
| [larkspur/](larkspur/README.md) | The Larkspur Cloud handbook (13 sections) and the 30-question golden set | Copied unchanged from `data/larkspur/` in this repository; written for the course, repository licence |
| [train.jsonl](train.jsonl) | 101 question and answer pairs for fine-tuning, one JSON object per line: `question`, `answer`, `source` | Written for this lab from the handbook; repository licence |

## train.jsonl

The pairs cover the lab's narrow task, refund and billing questions. Each answer restates a sentence of the handbook section named in `source`:

| `source` | Rows |
|---|---|
| `01_billing.md` | 32 |
| `02_refunds.md` | 18 |
| `12_sla_credits.md` | 16 |
| `13_onboarding.md` (trial credit, payment method) | 8 |
| `03_plans.md` (annual billing, traffic allowances) | 7 |
| `07_account_deletion.md` (invoices, unpaid balance) | 5 |
| `10_support_tiers.md` (the Billing ticket category) | 3 |
| `none` | 12 |

The 12 `none` rows teach the model to decline: six billing questions the handbook does not answer and six off-topic requests, each answered with *The handbook does not say.*

No question is copied from `larkspur/golden.jsonl`; the solution asserts this and prints, for each test question, the closest training question by TF-IDF similarity. The facts overlap on purpose: the fine-tuned model and the RAG baseline both learn from the same handbook, one through its weights and one through its index. No training question asks for a plan price, so the out-of-corpus test question `g26` is not taught by example.
