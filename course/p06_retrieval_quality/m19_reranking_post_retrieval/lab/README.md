# Lab — M19 Post-Retrieval Optimisation & Reranking

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

## Brief

Precision stack: add a cross-encoder reranker over a top-50 hybrid retrieval and measure the gain at top-5, plus the latency budget it consumes.

## How to report it

- Use the golden question set and the baseline from the M11 lab.
- Report the change against that baseline: retrieval metrics, answer quality, latency and cost where relevant.
- Put your notebook or script in this folder and record results in a short table.

Back to the module: [README.md](../README.md)
