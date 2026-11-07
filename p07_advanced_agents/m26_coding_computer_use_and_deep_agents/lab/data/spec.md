# Spec: Larkspur refund-amount calculator

Write a Python module `refund.py` with one public function:

```python
def refund_amount(billing: str, amount_paid: float, days_since_purchase: int, outbound_gb: float) -> float:
    ...
```

It returns the refund, in USD, that a Larkspur Cloud customer gets when they cancel a plan.

## Rules from the handbook

These come from `larkspur/handbook/02_refunds.md`:

1. Monthly plans are not refundable.
2. An annual plan can get a full refund within 30 days of purchase if the account used less than 100 GB of outbound traffic.
3. After day 30, annual refunds are prorated: you get back the unused whole months, minus a 15% early-termination fee.

## Decisions the handbook leaves open

The handbook does not define these, so this spec fixes them:

- `billing` is `"monthly"` or `"annual"`; any other value raises `ValueError`.
- `amount_paid` is what the customer paid for the current cycle (one month or one year) and must be greater than 0; `days_since_purchase` and `outbound_gb` must be 0 or more. A value outside those ranges raises `ValueError`.
- A month is 30 days, and a year has 12 months. A month counts as used as soon as it has started, so day 0 to day 30 use one month, day 31 to day 60 use two, and so on.
- Each month of an annual plan is worth `amount_paid / 12`.
- Day 30 is still "within 30 days of purchase". The full refund needs both conditions: `days_since_purchase <= 30` and `outbound_gb < 100`.
- An annual plan that does not qualify for the full refund gets the prorated refund, including within the first 30 days (one month used).
- When all 12 months are used, the refund is 0.
- The result is rounded to cents with `round(value, 2)`.

## Worked examples

| billing | amount_paid | days_since_purchase | outbound_gb | refund | Why |
|---|---|---|---|---|---|
| monthly | 40.00 | 3 | 5 | 0.00 | Monthly plans are not refundable |
| annual | 1200.00 | 10 | 20 | 1200.00 | Full refund: within 30 days, under 100 GB |
| annual | 1200.00 | 30 | 99.9 | 1200.00 | Day 30 still counts |
| annual | 1200.00 | 10 | 100 | 935.00 | 100 GB is not under 100 GB: 11 unused months x 100 x 0.85 |
| annual | 1200.00 | 31 | 0 | 850.00 | Two months used: 10 x 100 x 0.85 |
| annual | 1200.00 | 200 | 0 | 425.00 | Seven months used: 5 x 100 x 0.85 |
| annual | 1200.00 | 360 | 0 | 0.00 | All 12 months used |

## Tests

Write `test_refund.py` for pytest. It covers every worked example, each `ValueError` case, and the boundary days 30, 31, 330, 331 and 360.
