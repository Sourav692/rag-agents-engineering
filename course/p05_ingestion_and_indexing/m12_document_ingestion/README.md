# M12 — Document Ingestion & Metadata Design

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part V · The Ingestion & Indexing Pipeline** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 4 mandatory, 9 optional

## Why it matters

Retrieval can only be as good as the text and metadata you extract. Bad parsing and missing metadata are the most common root cause of weak RAG.

## Learning objectives

- Load text, Markdown, CSV, JSON, PDF, Word, web pages, transcripts and papers into `Document` objects
- Choose a PDF parser by comparing PyPDF, PyMuPDF and Unstructured element-level output
- Design a metadata schema that filtering, citation and access control will rely on later
- Write a custom loader with `BaseLoader.lazy_load` for a source no library covers

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 12.1 | The Document abstraction and metadata design | [`01a_document_loading_and_metadata.ipynb`](notebooks/01a_document_loading_and_metadata.ipynb) | [`01b_document_loaders_overview.ipynb`](optional/01b_document_loaders_overview.ipynb) *(alternate)* |
| 12.2 | Plain text and Markdown (single vs element mode) *(optional lesson)* | — | [`02a_text_loader.ipynb`](optional/02a_text_loader.ipynb) *(extension)*<br>[`02b_markdown_loader.ipynb`](optional/02b_markdown_loader.ipynb) *(extension)* |
| 12.3 | Semi-structured sources: CSV rows and JSON / JSONL with jq schemas *(optional lesson)* | — | [`03a_csv_loader.ipynb`](optional/03a_csv_loader.ipynb) *(extension)*<br>[`03b_json_loader.ipynb`](optional/03b_json_loader.ipynb) *(extension)* |
| 12.4 | PDF and Word: parser comparison and element-level parsing | [`04a_pdf_loader.ipynb`](notebooks/04a_pdf_loader.ipynb) | [`04b_ms_word_loader.ipynb`](optional/04b_ms_word_loader.ipynb) *(extension)* |
| 12.5 | Web, YouTube and arXiv sources; bulk directory loading | [`05a_url_loader.ipynb`](notebooks/05a_url_loader.ipynb) | [`05b_youtube_transcript_loader.ipynb`](optional/05b_youtube_transcript_loader.ipynb) *(extension)*<br>[`05c_research_paper_loader.ipynb`](optional/05c_research_paper_loader.ipynb) *(extension)*<br>[`05d_directory_loader.ipynb`](optional/05d_directory_loader.ipynb) *(extension)* |
| 12.6 | Custom loaders with lazy loading | [`06a_custom_loader.ipynb`](notebooks/06a_custom_loader.ipynb) | — |

## Hands-on lab

Multi-source ingestor: load a mixed folder (PDF, DOCX, Markdown, CSV, one web page) into Documents that share one metadata schema (source, type, section, page, date). Details: [lab/README.md](lab/README.md).

## Key concepts

Loader vs parser · Element-level parsing · Metadata schema · Lazy loading

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
| `notebooks/01a_document_loading_and_metadata.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/01_document_loading_and_metadata.ipynb` |
| `optional/01b_document_loaders_overview.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/13_document_loaders_overview.ipynb` |
| `optional/02a_text_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/02_text_loader.ipynb` |
| `optional/02b_markdown_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/03_markdown_loader.ipynb` |
| `optional/03a_csv_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/04_csv_loader.ipynb` |
| `optional/03b_json_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/05_json_loader.ipynb` |
| `notebooks/04a_pdf_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/06_pdf_loader.ipynb` |
| `optional/04b_ms_word_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/07_ms_word_loader.ipynb` |
| `notebooks/05a_url_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/10_url_loader.ipynb` |
| `optional/05b_youtube_transcript_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/09_youtube_transcript_loader.ipynb` |
| `optional/05c_research_paper_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/11_research_paper_loader.ipynb` |
| `optional/05d_directory_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/08_directory_loader.ipynb` |
| `notebooks/06a_custom_loader.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/02_document_loading/notebooks/12_custom_loader.ipynb` |
