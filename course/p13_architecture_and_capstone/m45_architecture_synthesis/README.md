# M45 — Agentic RAG Architectures: Choosing a Design

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part XIII · Architecture Synthesis & Capstone** · **Level:** Expert · **Time:** ~3 h · **Notebooks:** 2 mandatory, 0 optional

## Why it matters

You now know more than a dozen architectures. The final skill is choosing the simplest one that meets the requirement.

## Learning objectives

- Place every architecture from the course on one map: entry-level, self-correcting, routing, tool-based, structural
- Walk the whole RAG stack from basic RAG through RAPTOR / ColBERT to agentic self-correction
- Choose an architecture from query complexity, data shape, latency budget and cost

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 45.1 | The agentic RAG architecture map | [`01a_AGENTIC_RAG_ARCHITECTURES.md`](notebooks/01a_AGENTIC_RAG_ARCHITECTURES.md) | — |
| 45.2 | End-to-end RAG ecosystem walkthrough (incl. ColBERT and RAGAS) | [`02a_rag_ecosystem.ipynb`](notebooks/02a_rag_ecosystem.ipynb) | — |
| 45.3 | Decision framework: picking the simplest architecture that works | *Lecture / discussion* | — |

## Hands-on lab

Architecture review: write a two-page design document for your capstone that justifies each component against a simpler alternative. Details: [lab/README.md](lab/README.md).

## Key concepts

Architecture selection · Complexity budget · Late interaction (ColBERT) · End-to-end evaluation

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `projects/` — runnable sub-projects (e.g. MCP servers and clients), where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_AGENTIC_RAG_ARCHITECTURES.md` | `ai-engineering-demystified-09-advanced-rag` | `modules/11_agentic_rag_architectures/AGENTIC_RAG_ARCHITECTURES.md` |
| `notebooks/02a_rag_ecosystem.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/11_agentic_rag_architectures/notebooks/01_rag_ecosystem.ipynb` |
