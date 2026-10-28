# M24 — Long-Term & Agentic Memory

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VII · Memory & Multi-Agent RAG** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 6 mandatory, 5 optional

## Why it matters

Long-term memory is retrieval over the agent's own past: facts, episodes and procedures. The same indexing and retrieval choices from Parts II–III apply.

## Learning objectives

- Share memory across threads with a LangGraph `Store` (in-memory and Postgres)
- Build session, semantic, episodic and procedural memory layers
- Compare agentic memory architectures: graph memory, MemGPT tiers, Voyager skill library, Agent Workflow Memory

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 24.1 | Cross-thread memory with a Store | [`01a_cross_thread_memory_store.ipynb`](notebooks/01a_cross_thread_memory_store.ipynb) | — |
| 24.2 | Session, semantic, episodic and procedural memory on SQLite | [`02b_long_term_semantic_memory_sqlite.ipynb`](notebooks/02b_long_term_semantic_memory_sqlite.ipynb)<br>[`02c_long_term_episodic_memory_sqlite.ipynb`](notebooks/02c_long_term_episodic_memory_sqlite.ipynb) | [`02a_session_memory_sqlite.ipynb`](optional/02a_session_memory_sqlite.ipynb) *(extension)*<br>[`02d_long_term_procedural_memory_sqlite.ipynb`](optional/02d_long_term_procedural_memory_sqlite.ipynb) *(extension)* |
| 24.3 | A combined-memory agent | [`03a_combined_memory_agent_sqlite.ipynb`](notebooks/03a_combined_memory_agent_sqlite.ipynb) | — |
| 24.4 | Episodic + semantic stack and multi-hop graph memory | [`04a_episodic_with_semantic_memory.ipynb`](notebooks/04a_episodic_with_semantic_memory.ipynb) | [`04b_graph_memory_multi_hop.ipynb`](optional/04b_graph_memory_multi_hop.ipynb) *(extension)* |
| 24.5 | MemGPT tiers, Voyager skill library, Agent Workflow Memory | [`05a_memgpt_tiered_memory.ipynb`](notebooks/05a_memgpt_tiered_memory.ipynb) | [`05b_voyager_skill_library.ipynb`](optional/05b_voyager_skill_library.ipynb) *(extension)*<br>[`05c_agent_workflow_memory.ipynb`](optional/05c_agent_workflow_memory.ipynb) *(extension)* |

## Hands-on lab

Personal RAG: give your assistant semantic memory of user preferences and show that answers in a new thread use them. Details: [lab/README.md](lab/README.md).

## Key concepts

Semantic / episodic / procedural memory · Store namespaces · Tiered memory · Skill library

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
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
