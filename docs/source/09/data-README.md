# Data

Small sample datasets shared by more than one module live in `sample/`. Data used by a single module sits in that module's `assets/`. Every file is listed in `docs/data-sources.md` with its source, license and SHA-256.

## Layout

| Path | Contents | Used by |
|---|---|---|
| `sample/research_papers/` | Five arXiv papers (Attention, chain-of-thought, diffusion, DINO, PEFT) | the LangGraph corrective (02/01) and adaptive (04/04) RAG notebooks |
| `sample/rag_techniques/` | The RAG Techniques anthology's climate-change report and its Q&A pairs (non-commercial licence, see `docs/third_party/`) | anthology notebooks in modules 02, 03, 04, 06, 07, 08, 10 |

Some notebooks download or generate more files here at run time (listed in `scripts/path_allowlist.txt`); those paths are git-ignored.
