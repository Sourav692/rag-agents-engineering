# Lab: M11 Document Ingestion & Metadata Design

## Brief

Multi-source ingestor: load a mixed folder (PDF, DOCX, Markdown, CSV, one web page) into Documents that share one metadata schema (source, type, section, page, date).

## Approach

- Every loader returns `Document(page_content, metadata)`. `page_content` is embedded and shown to the model; `metadata` is never embedded, and it is the only thing you can filter on exactly.
- A loader gets bytes from a source; a parser turns those bytes into text and structure. Which parser you choose decides what the index can contain. The solution uses the module's loaders: `PyPDFLoader`, `Docx2txtLoader`, `TextLoader` plus `MarkdownHeaderTextSplitter`, `CSVLoader` and `BSHTMLLoader`.
- Design the metadata schema for the filters, citations and access rules you will need later. Every loader names its fields differently (`page` counts from 0 in PyPDF), so map them onto the schema at load time; adding a field after indexing means re-ingesting the corpus.
- What to watch: a schema check that only tests for keys will pass a document whose values are wrong. Read one printed record per type.

## How to run

The worked solution is [solution/m11_solution.ipynb](solution/m11_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the default environment: `uv run jupyter lab`. No API keys are needed: the lab makes no model calls.

## Data

The solution reads the five files in `data/mixed/`: a public-domain CRS report (PDF) and four fictional Larkspur Cloud files (DOCX, Markdown, CSV, HTML). The Larkspur corpus is in `data/larkspur/` as in every lab, but this solution does not read it. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date | *pending run* |
| Documents per type | *pending run* |
| One metadata record per type | *pending run* |
| Schema check on the folder | *pending run* |
| Schema check on a document without `date` | *pending run* |

Back to the module: [README.md](../README.md)
