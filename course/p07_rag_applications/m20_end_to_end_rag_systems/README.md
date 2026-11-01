# M20 — End-to-End RAG Systems

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part VII · Building Complete RAG Applications** · **Level:** Core · **Time:** ~7 h · **Notebooks:** 8 mandatory, 3 optional

## Why it matters

Users trust answers they can check. This module turns pipelines into systems that cite sources, explain retrieval and handle tables and JSON.

## Theory

Read the [theory page](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Sample or population](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/04_rag_over_structured_data_csv_and_json/interactive/sample-or-population-lab.html) (open the file in a browser)

## Learning objectives

- Build an end-to-end RAG system over JSONL and PDF sources
- Return source documents with each answer and attach structured per-claim citations
- Explain why each retrieved chunk is relevant
- Choose a row / record representation for CSV and JSON data
- Run a fully local pipeline with Hugging Face models and FAISS

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 20.1 | Environment setup and a complete RAG system ([theory](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/01_environment_setup_and_a_complete_rag_system/README.md)) | [`01a_setup.ipynb`](notebooks/01a_setup.ipynb)<br>[`01b_build_a_simple_rag_system.ipynb`](notebooks/01b_build_a_simple_rag_system.ipynb) | [`01c_simple_rag_pdf.ipynb`](optional/01c_simple_rag_pdf.ipynb) *(alternate)* |
| 20.2 | Answers with sources and per-claim citations ([theory](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/02_answers_with_sources_and_per_claim_citations/README.md)) | [`02a_rag_system_with_sources.ipynb`](notebooks/02a_rag_system_with_sources.ipynb)<br>[`02b_rag_system_with_citations.ipynb`](notebooks/02b_rag_system_with_citations.ipynb) | — |
| 20.3 | Explainable retrieval ([theory](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/03_explainable_retrieval/README.md)) | [`03a_explainable_retrieval.ipynb`](notebooks/03a_explainable_retrieval.ipynb) | — |
| 20.4 | RAG over structured data: CSV and JSON ([theory](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/04_rag_over_structured_data_csv_and_json/README.md)) | [`04a_structured_data_rag.ipynb`](notebooks/04a_structured_data_rag.ipynb) | [`04b_simple_csv_rag.ipynb`](optional/04b_simple_csv_rag.ipynb) *(alternate)*<br>[`04c_json_rag.ipynb`](optional/04c_json_rag.ipynb) *(extension)* |
| 20.5 | Fully local RAG with Hugging Face and FAISS ([theory](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/05_fully_local_rag_with_hugging_face_and_faiss/README.md)) | [`05a_local_rag_huggingface_faiss.ipynb`](notebooks/05a_local_rag_huggingface_faiss.ipynb) | — |

## Hands-on lab

Module lab, AI research assistant: package ingestion, retrieval, structured answers with citations and session history into one class (05/10/11). Details: [lab/README.md](lab/README.md).

## Key concepts

[Grounded generation](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/01_environment_setup_and_a_complete_rag_system/README.md#grounded-generation) · [Citation schema](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/02_answers_with_sources_and_per_claim_citations/README.md#citation-schema) · [Record representation](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/04_rag_over_structured_data_csv_and_json/README.md#record-representation) · [Local inference](../../../theory/p07_rag_applications/m20_end_to_end_rag_systems/05_fully_local_rag_with_hugging_face_and_faiss/README.md#local-inference)

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
| `notebooks/01a_setup.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/00_setup.ipynb` |
| `notebooks/01b_build_a_simple_rag_system.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/01_build_a_simple_rag_system.ipynb` |
| `optional/01c_simple_rag_pdf.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/05_simple_rag_pdf.ipynb` |
| `notebooks/02a_rag_system_with_sources.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/03_rag_system_with_sources.ipynb` |
| `notebooks/02b_rag_system_with_citations.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/04_rag_system_with_citations.ipynb` |
| `notebooks/03a_explainable_retrieval.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/07_explainable_retrieval.ipynb` |
| `notebooks/04a_structured_data_rag.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/08_structured_data_rag.ipynb` |
| `optional/04b_simple_csv_rag.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/09_simple_csv_rag.ipynb` |
| `optional/04c_json_rag.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/10_json_rag.ipynb` |
| `notebooks/05a_local_rag_huggingface_faiss.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/06_local_rag_huggingface_faiss.ipynb` |
| `notebooks/lab_ai_research_assistant.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/10_building_rag_systems/notebooks/11_ai_research_assistant.ipynb` |
