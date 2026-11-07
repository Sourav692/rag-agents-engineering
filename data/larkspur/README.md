# Larkspur Cloud handbook and golden set

Larkspur Cloud is a fictional hosting company. Its customer handbook is the running example of the theory pages and the shared corpus of the module labs. Everything in this folder was written for this course; no real company, product or customer data is involved, and it carries the repository's licence.

The twelve chunks of the M11 top-k lab appear here word for word, so a lab run on this corpus and the theory pages quote the same text.

## Files

| File | Section |
|---|---|
| [handbook/01_billing.md](handbook/01_billing.md) | Billing and payments |
| [handbook/02_refunds.md](handbook/02_refunds.md) | Refunds |
| [handbook/03_plans.md](handbook/03_plans.md) | Plans and server sizes |
| [handbook/04_outages_and_status.md](handbook/04_outages_and_status.md) | Outages and status |
| [handbook/05_backups.md](handbook/05_backups.md) | Backups and snapshots |
| [handbook/06_data_export.md](handbook/06_data_export.md) | Data export and retention |
| [handbook/07_account_deletion.md](handbook/07_account_deletion.md) | Account deletion |
| [handbook/08_security.md](handbook/08_security.md) | Security |
| [handbook/09_api_limits.md](handbook/09_api_limits.md) | API limits |
| [handbook/10_support_tiers.md](handbook/10_support_tiers.md) | Support tiers |
| [handbook/11_regions.md](handbook/11_regions.md) | Regions |
| [handbook/12_sla_credits.md](handbook/12_sla_credits.md) | SLA and service credits |
| [handbook/13_onboarding.md](handbook/13_onboarding.md) | Onboarding |
| [golden.jsonl](golden.jsonl) | 30 golden questions |

Each handbook file starts with `# <Section title>`.

## Golden set

`golden.jsonl` holds one question per line with these fields:

- `id`: `g01` to `g30`.
- `question`: what a customer asks.
- `type`: `lookup` (15), `multi_hop` (6, evidence from two or more files), `numeric` (4) or `out_of_corpus` (5, the handbook has no answer).
- `evidence_spans`: exact substrings of the handbook that answer the question; empty for `out_of_corpus`.
- `reference_answer`: written from the handbook text only.

`g01` to `g03` are the three questions of the M11 top-k lab.

Evidence is a text span, not a chunk id, so any chunker can be scored: a retrieved chunk is a hit when it contains a span after lower-casing and collapsing whitespace. `src/lab_kit.py` implements the metrics.

## Using it in a lab

Copy the folder unchanged into the lab, `cp -R data/larkspur <part>/<module>/lab/data/larkspur`, and never edit the copy. Lab-specific files go beside it in `lab/data/`. `tests/test_labs.py` checks that every copy matches this folder byte for byte.
