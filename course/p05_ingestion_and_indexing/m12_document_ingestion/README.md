# M12 — Document Ingestion & Metadata Design

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part V · The Ingestion & Indexing Pipeline** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 4 mandatory, 9 optional

## Why it matters

Retrieval can only be as good as the text and metadata you extract. Bad parsing and missing metadata are the most common root cause of weak RAG.

## Theory

Read the [theory page](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [One PDF page, three parsers](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/04_pdf_and_word_parser_comparison_and_element_level_parsing/interactive/pdf-parsers-lab.html) (open the file in a browser)

## Learning objectives

- Load text, Markdown, CSV, JSON, PDF, Word, web pages, transcripts and papers into `Document` objects
- Choose a PDF parser by comparing PyPDF, PyMuPDF and Unstructured element-level output
- Design a metadata schema that filtering, citation and access control will rely on later
- Write a custom loader with `BaseLoader.lazy_load` for a source no library covers

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 12.1 | The Document abstraction and metadata design ([theory](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/01_the_document_abstraction_and_metadata_design/README.md)) | [`01a_document_loading_and_metadata.ipynb`](notebooks/01a_document_loading_and_metadata.ipynb) | [`01b_document_loaders_overview.ipynb`](optional/01b_document_loaders_overview.ipynb) *(alternate)* |
| 12.2 | Plain text and Markdown (single vs element mode) *(optional lesson)* | — | [`02a_text_loader.ipynb`](optional/02a_text_loader.ipynb) *(extension)*<br>[`02b_markdown_loader.ipynb`](optional/02b_markdown_loader.ipynb) *(extension)* |
| 12.3 | Semi-structured sources: CSV rows and JSON / JSONL with jq schemas *(optional lesson)* ([theory](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/03_semi_structured_sources_csv_rows_and_json_jsonl_with_jq_schemas/README.md)) | — | [`03a_csv_loader.ipynb`](optional/03a_csv_loader.ipynb) *(extension)*<br>[`03b_json_loader.ipynb`](optional/03b_json_loader.ipynb) *(extension)* |
| 12.4 | PDF and Word: parser comparison and element-level parsing ([theory](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/04_pdf_and_word_parser_comparison_and_element_level_parsing/README.md)) | [`04a_pdf_loader.ipynb`](notebooks/04a_pdf_loader.ipynb) | [`04b_ms_word_loader.ipynb`](optional/04b_ms_word_loader.ipynb) *(extension)* |
| 12.5 | Web, YouTube and arXiv sources; bulk directory loading ([theory](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/05_web_youtube_and_arxiv_sources_bulk_directory_loading/README.md)) | [`05a_url_loader.ipynb`](notebooks/05a_url_loader.ipynb) | [`05b_youtube_transcript_loader.ipynb`](optional/05b_youtube_transcript_loader.ipynb) *(extension)*<br>[`05c_research_paper_loader.ipynb`](optional/05c_research_paper_loader.ipynb) *(extension)*<br>[`05d_directory_loader.ipynb`](optional/05d_directory_loader.ipynb) *(extension)* |
| 12.6 | Custom loaders with lazy loading ([theory](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/06_custom_loaders_with_lazy_loading/README.md)) | [`06a_custom_loader.ipynb`](notebooks/06a_custom_loader.ipynb) | — |

## Hands-on lab

Multi-source ingestor: load a mixed folder (PDF, DOCX, Markdown, CSV, one web page) into Documents that share one metadata schema (source, type, section, page, date). Details: [lab/README.md](lab/README.md).

## Key concepts

[Loader vs parser](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/01_the_document_abstraction_and_metadata_design/README.md#loader-vs-parser) · [Element-level parsing](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/04_pdf_and_word_parser_comparison_and_element_level_parsing/README.md#element-level-parsing) · [Metadata schema](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/01_the_document_abstraction_and_metadata_design/README.md#metadata-schema) · [Lazy loading](../../../theory/p05_ingestion_and_indexing/m12_document_ingestion/06_custom_loaders_with_lazy_loading/README.md#lazy-loading)

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
