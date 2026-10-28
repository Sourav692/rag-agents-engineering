# M23 — Conversation Memory & Conversational RAG

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VII · Memory & Multi-Agent RAG** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 7 mandatory, 3 optional

## Why it matters

Follow-up questions such as “and what about the second one?” fail without history. Conversational RAG rewrites each question with the chat history before retrieving.

## Learning objectives

- Explain why LLMs forget and add message histories, windows and summaries
- Manage multi-user sessions and persist them to SQLite
- Build history-aware conversational RAG
- Give LangGraph agents thread-scoped memory with checkpointers and keep long threads affordable

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 23.1 | Why LLMs forget; classic memory classes | [`01a_why_llms_forget.ipynb`](notebooks/01a_why_llms_forget.ipynb) | [`01b_classic_memory_classes_and_chains.ipynb`](optional/01b_classic_memory_classes_and_chains.ipynb) *(extension)* |
| 23.2 | RunnableWithMessageHistory, multi-user sessions and persistence | [`02a_runnable_with_message_history.ipynb`](notebooks/02a_runnable_with_message_history.ipynb)<br>[`02b_multi_user_sessions_and_persistence.ipynb`](notebooks/02b_multi_user_sessions_and_persistence.ipynb) | — |
| 23.3 | Trimming, windowing and summary memory | [`03a_trimming_windowing_and_summary.ipynb`](notebooks/03a_trimming_windowing_and_summary.ipynb) | — |
| 23.4 | Conversational RAG with history-aware retrieval | [`04a_conversational_rag_with_history.ipynb`](notebooks/04a_conversational_rag_with_history.ipynb) | — |
| 23.5 | Memory apps: product recommender and research agent with SQL memory *(optional lesson)* | — | [`05a_multi_user_product_recommender.ipynb`](optional/05a_multi_user_product_recommender.ipynb) *(extension)*<br>[`05b_multi_user_research_agent_sql_memory.ipynb`](optional/05b_multi_user_research_agent_sql_memory.ipynb) *(extension)* |
| 23.6 | LangGraph threads, checkpoints and memory optimisations | [`06a_memory_and_conversational_agent.ipynb`](notebooks/06a_memory_and_conversational_agent.ipynb)<br>[`06b_memory_optimizations.ipynb`](notebooks/06b_memory_optimizations.ipynb) | — |

## Hands-on lab

Follow-up test: write 15 three-turn conversations and compare retrieval hit rate on turns two and three with and without history-aware query rewriting. Details: [lab/README.md](lab/README.md).

## Key concepts

Message history · History-aware retriever · Checkpointer / thread_id · Summary memory

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `notebooks/01a_why_llms_forget.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/01_why_llms_forget.ipynb` |
| `optional/01b_classic_memory_classes_and_chains.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/02_classic_memory_classes_and_chains.ipynb` |
| `notebooks/02a_runnable_with_message_history.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/03_runnable_with_message_history.ipynb` |
| `notebooks/02b_multi_user_sessions_and_persistence.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/04_multi_user_sessions_and_persistence.ipynb` |
| `notebooks/03a_trimming_windowing_and_summary.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/05_trimming_windowing_and_summary.ipynb` |
| `notebooks/04a_conversational_rag_with_history.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/06_conversational_rag_with_history.ipynb` |
| `optional/05a_multi_user_product_recommender.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/07_multi_user_product_recommender.ipynb` |
| `optional/05b_multi_user_research_agent_sql_memory.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/08_multi_user_research_agent_sql_memory.ipynb` |
| `notebooks/06a_memory_and_conversational_agent.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/02_langgraph_threads_and_checkpoints/notebooks/01_memory_and_conversational_agent.ipynb` |
| `notebooks/06b_memory_optimizations.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/02_langgraph_threads_and_checkpoints/notebooks/02_memory_optimizations.ipynb` |
