# M21 — Multimodal RAG

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part VII · Building Complete RAG Applications** · **Level:** Core · **Time:** ~3 h · **Notebooks:** 2 mandatory, 1 optional

## Why it matters

Real documents contain charts, diagrams and scanned pages. Text-only pipelines silently drop that information.

## Theory

Read the [theory page](../../../theory/p07_rag_applications/m21_multimodal_rag/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p07_rag_applications/m21_multimodal_rag/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Four ways to index a chart](../../../theory/p07_rag_applications/m21_multimodal_rag/01_shared_text_image_embedding_space_with_clip/interactive/chart-retrieval-lab.html) (open the file in a browser)

## Learning objectives

- Embed text and images in one space with CLIP and answer with a multimodal LLM
- Caption images with a vision model and index captions alongside text
- Retrieve whole PDF pages as images with ColPali (late interaction)

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 21.1 | Shared text–image embedding space with CLIP ([theory](../../../theory/p07_rag_applications/m21_multimodal_rag/01_shared_text_image_embedding_space_with_clip/README.md)) | [`01a_multimodal_rag_with_clip.ipynb`](notebooks/01a_multimodal_rag_with_clip.ipynb) | — |
| 21.2 | Caption-then-index with a vision LLM ([theory](../../../theory/p07_rag_applications/m21_multimodal_rag/02_caption_then_index_with_a_vision_llm/README.md)) | [`02a_multimodal_rag_with_captioning.ipynb`](notebooks/02a_multimodal_rag_with_captioning.ipynb) | — |
| 21.3 | Page-image retrieval with ColPali *(optional lesson)* ([theory](../../../theory/p07_rag_applications/m21_multimodal_rag/03_page_image_retrieval_with_colpali/README.md)) | — | [`03a_multimodal_rag_with_colpali.ipynb`](optional/03a_multimodal_rag_with_colpali.ipynb) *(platform-specific)* |

## Hands-on lab

Chart-aware RAG: index a report that holds key numbers only in figures and show which of the three approaches answers questions about them. Details: [lab/README.md](lab/README.md).

## Key concepts

[Joint embedding space](../../../theory/p07_rag_applications/m21_multimodal_rag/01_shared_text_image_embedding_space_with_clip/README.md#joint-embedding-space) · [Captioning](../../../theory/p07_rag_applications/m21_multimodal_rag/02_caption_then_index_with_a_vision_llm/README.md#captioning) · [Late interaction](../../../theory/p07_rag_applications/m21_multimodal_rag/03_page_image_retrieval_with_colpali/README.md#late-interaction) · [Page-level retrieval](../../../theory/p07_rag_applications/m21_multimodal_rag/03_page_image_retrieval_with_colpali/README.md#page-level-retrieval)

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
| `notebooks/01a_multimodal_rag_with_clip.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/11_multimodal_rag/notebooks/01_multimodal_rag_with_clip.ipynb` |
| `notebooks/02a_multimodal_rag_with_captioning.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/11_multimodal_rag/notebooks/02_multimodal_rag_with_captioning.ipynb` |
| `optional/03a_multimodal_rag_with_colpali.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/11_multimodal_rag/notebooks/03_multimodal_rag_with_colpali.ipynb` |
