# M46 — Architecture Synthesis: Choosing a System Design

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part XIII · Design Decisions: Model Adaptation & Architecture** · **Level:** Expert · **Time:** ~3 h · **Notebooks:** 2 mandatory, 0 optional

## Why it matters

You now know more than a dozen architectures. The final skill is choosing the simplest one that meets the requirement.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [The simplest architecture that works](mandatory/theory/03_decision_framework_picking_the_simplest_architecture_that_works/interactive/architecture-picker-lab.html) (open the file in a browser)

## Learning objectives

- Place every architecture from the course on one map: entry-level, self-correcting, routing, tool-based, structural
- Walk the whole RAG stack from basic RAG through RAPTOR / ColBERT to agentic self-correction
- Choose an architecture from query complexity, data shape, latency budget and cost

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 46.1 | The agentic RAG architecture map ([theory](mandatory/theory/01_the_agentic_rag_architecture_map/README.md)) | [`01a_AGENTIC_RAG_ARCHITECTURES.md`](mandatory/notebook/01a_AGENTIC_RAG_ARCHITECTURES.md) | — |
| 46.2 | End-to-end RAG ecosystem walkthrough (incl. ColBERT and RAGAS) ([theory](mandatory/theory/02_end_to_end_rag_ecosystem_walkthrough_incl_colbert_and_ragas/README.md)) | [`02a_rag_ecosystem.ipynb`](mandatory/notebook/02a_rag_ecosystem.ipynb) | — |
| 46.3 | Decision framework: picking the simplest architecture that works ([theory](mandatory/theory/03_decision_framework_picking_the_simplest_architecture_that_works/README.md)) | *Lecture / discussion* | — |

## Hands-on lab

Architecture review: write a two-page design document for your capstone that justifies each component against a simpler alternative. Details: [lab/README.md](lab/README.md).

## Key concepts

[Architecture selection](mandatory/theory/03_decision_framework_picking_the_simplest_architecture_that_works/README.md#architecture-selection) · [Complexity budget](mandatory/theory/03_decision_framework_picking_the_simplest_architecture_that_works/README.md#complexity-budget) · [Late interaction (ColBERT)](mandatory/theory/02_end_to_end_rag_ecosystem_walkthrough_incl_colbert_and_ragas/README.md#late-interaction-colbert) · [End-to-end evaluation](mandatory/theory/02_end_to_end_rag_ecosystem_walkthrough_incl_colbert_and_ragas/README.md#end-to-end-evaluation)

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
| `mandatory/notebook/01a_AGENTIC_RAG_ARCHITECTURES.md` | `ai-engineering-demystified-09-advanced-rag` | `modules/11_agentic_rag_architectures/AGENTIC_RAG_ARCHITECTURES.md` |
| `mandatory/notebook/02a_rag_ecosystem.ipynb` | `ai-engineering-demystified-09-advanced-rag` | `modules/11_agentic_rag_architectures/notebooks/01_rag_ecosystem.ipynb` |
