# Data

Small sample datasets shared by more than one module live in `sample/`. Data used by a single module sits in that module's `assets/`. Every file is listed in `docs/data-sources.md` with its source, license and SHA-256.

## Layout

| Path | Contents | Used by |
|---|---|---|
| `sample/*.pdf`, `sample/Intel Strategy.docx` | Research papers and a Word document | loaders (02), splitters (03), the end-to-end systems in 10 (which embed every PDF in this folder) |
| `sample/*.txt`, `*.csv`, `*.json`, `*.jsonl` | Small text, tabular and chat samples, two LangChain blog posts, a Wikipedia-derived JSONL | loaders (02), indexing (06), query transformation (08), reranking (09), 10, 12 |
| `sample/langchain_README.markdown` | A copy of LangChain's README used as a sample Markdown document (its links point into LangChain's own repository) | 02 |
| `sample/restaurant/` | Three short files about a fictional restaurant | 06, 08, 09 |
| `sample/rag_techniques/` | The RAG Techniques anthology's sample data (climate-change report, customers CSV, Nike annual report, Q&A pairs) | 03, 06, 07, 08, 09, 10, 13 |
| `sample/rag_production_course/` | A small LangChain demo PDF | 02, 03 |
