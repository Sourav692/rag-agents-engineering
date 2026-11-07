# M12 — Chunking Strategies

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part IV · RAG Foundations: Ingestion & Indexing** · **Level:** Core · **Time:** ~6 h · **Notebooks:** 4 mandatory, 6 optional

## Why it matters

The chunk is the unit of retrieval. Its size and boundaries decide what the retriever can find and how much noise reaches the model.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Chunk size and overlap](mandatory/theory/01_splitter_fundamentals_character_recursive_token_and_structure_aware/interactive/chunk-size-overlap-lab.html) (open the file in a browser)

## Learning objectives

- Apply character, recursive, token and structure-aware (Markdown, HTML, code) splitters
- Chunk on meaning with embedding-distance breakpoints (semantic chunking)
- Turn text into atomic, self-contained propositions and index those
- Pick chunk size and overlap by measurement instead of by habit

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 12.1 | Splitter fundamentals: character, recursive, token and structure-aware ([theory](mandatory/theory/01_splitter_fundamentals_character_recursive_token_and_structure_aware/README.md)) | [`01a_document_splitting_and_chunking.ipynb`](mandatory/notebook/01a_document_splitting_and_chunking.ipynb) | [`01b_document_splitters_and_chunkers.ipynb`](optional/notebook/01b_document_splitters_and_chunkers.ipynb) *(alternate)*<br>[`01c_text_splitters_and_chunking_strategies.ipynb`](optional/notebook/01c_text_splitters_and_chunking_strategies.ipynb) *(alternate)* |
| 12.2 | Semantic chunking: breakpoints on embedding distance ([theory](mandatory/theory/02_semantic_chunking_breakpoints_on_embedding_distance/README.md)) | [`02a_semantic_chunking.ipynb`](mandatory/notebook/02a_semantic_chunking.ipynb) | [`02b_semantic_chunking_walkthrough.ipynb`](optional/notebook/02b_semantic_chunking_walkthrough.ipynb) *(alternate)*<br>[`02c_semantic_chunking_rag_techniques.ipynb`](optional/notebook/02c_semantic_chunking_rag_techniques.ipynb) *(alternate)* |
| 12.3 | Proposition chunking with LLM quality checks ([theory](mandatory/theory/03_proposition_chunking_with_llm_quality_checks/README.md)) | [`03a_proposition_chunking.ipynb`](mandatory/notebook/03a_proposition_chunking.ipynb) | [`03b_proposition_chunking_rag_techniques.ipynb`](optional/notebook/03b_proposition_chunking_rag_techniques.ipynb) *(alternate)* |
| 12.4 | Choosing chunk size empirically: retrieval quality, faithfulness, latency ([theory](mandatory/theory/04_choosing_chunk_size_empirically_retrieval_quality_faithfulness_latency/README.md)) | [`04a_choosing_chunk_size.ipynb`](mandatory/notebook/04a_choosing_chunk_size.ipynb) | [`04b_choose_chunk_size_llamaindex.ipynb`](optional/notebook/04b_choose_chunk_size_llamaindex.ipynb) *(alternate)* |

## Hands-on lab

Chunking bake-off: index the same corpus with recursive, semantic and proposition chunking at three sizes each, and compare hit rate and answer faithfulness against the M10 baseline. Details: [lab/README.md](lab/README.md).

## Key concepts

[Chunk size and overlap](mandatory/theory/01_splitter_fundamentals_character_recursive_token_and_structure_aware/README.md#chunk-size-and-overlap) · [Breakpoint threshold](mandatory/theory/02_semantic_chunking_breakpoints_on_embedding_distance/README.md#breakpoint-threshold) · [Propositions](mandatory/theory/03_proposition_chunking_with_llm_quality_checks/README.md#propositions) · [Structure-aware splitting](mandatory/theory/01_splitter_fundamentals_character_recursive_token_and_structure_aware/README.md#structure-aware-splitting)

## Folder layout

- `mandatory/notebook/`: the mandatory track, plus the helper files those notebooks import
- `optional/notebook/`: alternate, platform-specific, extension and exercise notebooks
- `mandatory/theory/`: the module page, its `index.html` and the pages of lessons with a mandatory notebook
- `optional/theory/`: the pages of lessons whose notebooks are all optional
- `projects/`: runnable sub-projects (for example MCP servers and clients), where the module has them
- `assets/`: images and data used by this module's notebooks, where it has them
- `lab/`: the module lab brief, its solution notebook in `solution/` and its data in `data/`

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `mandatory/notebook/01a_document_splitting_and_chunking.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/01_document_splitting_and_chunking.ipynb` |
| `optional/notebook/01b_document_splitters_and_chunkers.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/02_document_splitters_and_chunkers.ipynb` |
| `optional/notebook/01c_text_splitters_and_chunking_strategies.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/03_text_splitters_and_chunking_strategies.ipynb` |
| `mandatory/notebook/02a_semantic_chunking.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/04_semantic_chunking.ipynb` |
| `optional/notebook/02b_semantic_chunking_walkthrough.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/05_semantic_chunking_walkthrough.ipynb` |
| `optional/notebook/02c_semantic_chunking_rag_techniques.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/06_semantic_chunking_rag_techniques.ipynb` |
| `mandatory/notebook/03a_proposition_chunking.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/07_proposition_chunking.ipynb` |
| `optional/notebook/03b_proposition_chunking_rag_techniques.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/08_proposition_chunking_rag_techniques.ipynb` |
| `mandatory/notebook/04a_choosing_chunk_size.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/09_choosing_chunk_size.ipynb` |
| `optional/notebook/04b_choose_chunk_size_llamaindex.ipynb` | `ai-engineering-demystified-05-retrieval-rag` | `modules/03_chunking/notebooks/10_choose_chunk_size_llamaindex.ipynb` |
