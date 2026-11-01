# M34 — Long-Term & Agentic Memory

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part X · Memory & Multi-Agent RAG** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 6 mandatory, 5 optional

## Why it matters

Long-term memory is retrieval over the agent's own past: facts, episodes and procedures. The same indexing and retrieval choices from Parts V–VI apply.

## Theory

Read the [theory page](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [The window and the archive](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/05_memgpt_tiers_voyager_skill_library_agent_workflow_memory/interactive/tiered-memory-lab.html) (open the file in a browser)

## Learning objectives

- Share memory across threads with a LangGraph `Store` (in-memory and Postgres)
- Build session, semantic, episodic and procedural memory layers
- Compare agentic memory architectures: graph memory, MemGPT tiers, Voyager skill library, Agent Workflow Memory

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 34.1 | Cross-thread memory with a Store ([theory](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/01_cross_thread_memory_with_a_store/README.md)) | [`01a_cross_thread_memory_store.ipynb`](notebooks/01a_cross_thread_memory_store.ipynb) | — |
| 34.2 | Session, semantic, episodic and procedural memory on SQLite ([theory](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/02_session_semantic_episodic_and_procedural_memory_on_sqlite/README.md)) | [`02b_long_term_semantic_memory_sqlite.ipynb`](notebooks/02b_long_term_semantic_memory_sqlite.ipynb)<br>[`02c_long_term_episodic_memory_sqlite.ipynb`](notebooks/02c_long_term_episodic_memory_sqlite.ipynb) | [`02a_session_memory_sqlite.ipynb`](optional/02a_session_memory_sqlite.ipynb) *(extension)*<br>[`02d_long_term_procedural_memory_sqlite.ipynb`](optional/02d_long_term_procedural_memory_sqlite.ipynb) *(extension)* |
| 34.3 | A combined-memory agent ([theory](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/03_a_combined_memory_agent/README.md)) | [`03a_combined_memory_agent_sqlite.ipynb`](notebooks/03a_combined_memory_agent_sqlite.ipynb) | — |
| 34.4 | Episodic + semantic stack and multi-hop graph memory ([theory](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/04_episodic_semantic_stack_and_multi_hop_graph_memory/README.md)) | [`04a_episodic_with_semantic_memory.ipynb`](notebooks/04a_episodic_with_semantic_memory.ipynb) | [`04b_graph_memory_multi_hop.ipynb`](optional/04b_graph_memory_multi_hop.ipynb) *(extension)* |
| 34.5 | MemGPT tiers, Voyager skill library, Agent Workflow Memory ([theory](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/05_memgpt_tiers_voyager_skill_library_agent_workflow_memory/README.md)) | [`05a_memgpt_tiered_memory.ipynb`](notebooks/05a_memgpt_tiered_memory.ipynb) | [`05b_voyager_skill_library.ipynb`](optional/05b_voyager_skill_library.ipynb) *(extension)*<br>[`05c_agent_workflow_memory.ipynb`](optional/05c_agent_workflow_memory.ipynb) *(extension)* |

## Hands-on lab

Personal RAG: give your assistant semantic memory of user preferences and show that answers in a new thread use them. Details: [lab/README.md](lab/README.md).

## Key concepts

[Semantic / episodic / procedural memory](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/02_session_semantic_episodic_and_procedural_memory_on_sqlite/README.md#semantic--episodic--procedural-memory) · [Store namespaces](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/01_cross_thread_memory_with_a_store/README.md#store-namespaces) · [Tiered memory](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/05_memgpt_tiers_voyager_skill_library_agent_workflow_memory/README.md#tiered-memory) · [Skill library](../../../theory/p10_memory_and_multi_agent/m34_long_term_agentic_memory/05_memgpt_tiers_voyager_skill_library_agent_workflow_memory/README.md#skill-library)

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
| `notebooks/01a_cross_thread_memory_store.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/03_long_term_and_persistent_memory/notebooks/01_cross_thread_memory_store.ipynb` |
| `optional/02a_session_memory_sqlite.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/03_long_term_and_persistent_memory/notebooks/02_session_memory_sqlite.ipynb` |
| `notebooks/02b_long_term_semantic_memory_sqlite.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/03_long_term_and_persistent_memory/notebooks/03_long_term_semantic_memory_sqlite.ipynb` |
| `notebooks/02c_long_term_episodic_memory_sqlite.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/03_long_term_and_persistent_memory/notebooks/04_long_term_episodic_memory_sqlite.ipynb` |
| `optional/02d_long_term_procedural_memory_sqlite.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/03_long_term_and_persistent_memory/notebooks/05_long_term_procedural_memory_sqlite.ipynb` |
| `notebooks/03a_combined_memory_agent_sqlite.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/03_long_term_and_persistent_memory/notebooks/06_combined_memory_agent_sqlite.ipynb` |
| `notebooks/04a_episodic_with_semantic_memory.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/04_agentic_memory_architectures/notebooks/01_episodic_with_semantic_memory.ipynb` |
| `optional/04b_graph_memory_multi_hop.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/04_agentic_memory_architectures/notebooks/02_graph_memory_multi_hop.ipynb` |
| `notebooks/05a_memgpt_tiered_memory.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/04_agentic_memory_architectures/notebooks/03_memgpt_tiered_memory.ipynb` |
| `optional/05b_voyager_skill_library.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/04_agentic_memory_architectures/notebooks/04_voyager_skill_library.ipynb` |
| `optional/05c_agent_workflow_memory.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/04_agentic_memory_architectures/notebooks/05_agent_workflow_memory.ipynb` |
