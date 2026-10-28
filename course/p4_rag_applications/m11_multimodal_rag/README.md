# M11 — Multimodal RAG

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part IV · Building Complete RAG Applications** · **Level:** Core · **Time:** ~3 h · **Notebooks:** 2 mandatory, 1 optional

## Why it matters

Real documents contain charts, diagrams and scanned pages. Text-only pipelines silently drop that information.

## Learning objectives

- Embed text and images in one space with CLIP and answer with a multimodal LLM
- Caption images with a vision model and index captions alongside text
- Retrieve whole PDF pages as images with ColPali (late interaction)

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 11.1 | Shared text–image embedding space with CLIP | [`01a_multimodal_rag_with_clip.ipynb`](notebooks/01a_multimodal_rag_with_clip.ipynb) | — |
| 11.2 | Caption-then-index with a vision LLM | [`02a_multimodal_rag_with_captioning.ipynb`](notebooks/02a_multimodal_rag_with_captioning.ipynb) | — |
| 11.3 | Page-image retrieval with ColPali *(optional lesson)* | — | [`03a_multimodal_rag_with_colpali.ipynb`](optional/03a_multimodal_rag_with_colpali.ipynb) *(platform-specific)* |

## Hands-on lab

Chart-aware RAG: index a report that holds key numbers only in figures and show which of the three approaches answers questions about them. Details: [lab/README.md](lab/README.md).

## Key concepts

Joint embedding space · Captioning · Late interaction · Page-level retrieval

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_multimodal_rag_with_clip.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/11_multimodal_rag/notebooks/01_multimodal_rag_with_clip.ipynb` |
| `notebooks/02a_multimodal_rag_with_captioning.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/11_multimodal_rag/notebooks/02_multimodal_rag_with_captioning.ipynb` |
| `optional/03a_multimodal_rag_with_colpali.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/11_multimodal_rag/notebooks/03_multimodal_rag_with_colpali.ipynb` |
