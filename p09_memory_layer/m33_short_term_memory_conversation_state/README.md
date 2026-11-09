# M33 — Short-Term Memory & Conversation State

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part IX · The Memory Layer** · **Level:** Advanced · **Time:** ~5 h · **Notebooks:** 7 mandatory, 3 optional

## Why it matters

Follow-up questions such as “and what about the second one?” fail without history. Conversational RAG rewrites each question with the chat history before retrieving.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Follow-ups and the retriever](mandatory/theory/04_conversational_rag_with_history_aware_retrieval/interactive/follow-up-retrieval-lab.html) (open the file in a browser)

## Learning objectives

- Explain why LLMs forget and add message histories, windows and summaries
- Manage multi-user sessions and persist them to SQLite
- Build history-aware conversational RAG
- Give LangGraph agents thread-scoped memory with checkpointers and keep long threads affordable

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 33.1 | Why LLMs forget; classic memory classes ([theory](mandatory/theory/01_why_llms_forget_classic_memory_classes/README.md)) | [`01a_why_llms_forget.ipynb`](mandatory/notebook/01a_why_llms_forget.ipynb) | [`01b_classic_memory_classes_and_chains.ipynb`](optional/notebook/01b_classic_memory_classes_and_chains.ipynb) *(extension)* |
| 33.2 | RunnableWithMessageHistory, multi-user sessions and persistence ([theory](mandatory/theory/02_runnablewithmessagehistory_multi_user_sessions_and_persistence/README.md)) | [`02a_runnable_with_message_history.ipynb`](mandatory/notebook/02a_runnable_with_message_history.ipynb)<br>[`02b_multi_user_sessions_and_persistence.ipynb`](mandatory/notebook/02b_multi_user_sessions_and_persistence.ipynb) | — |
| 33.3 | Trimming, windowing and summary memory ([theory](mandatory/theory/03_trimming_windowing_and_summary_memory/README.md)) | [`03a_trimming_windowing_and_summary.ipynb`](mandatory/notebook/03a_trimming_windowing_and_summary.ipynb) | — |
| 33.4 | Conversational RAG with history-aware retrieval ([theory](mandatory/theory/04_conversational_rag_with_history_aware_retrieval/README.md)) | [`04a_conversational_rag_with_history.ipynb`](mandatory/notebook/04a_conversational_rag_with_history.ipynb) | — |
| 33.5 | Memory apps: product recommender and research agent with SQL memory *(optional lesson)* ([theory](optional/theory/05_memory_apps_product_recommender_and_research_agent_with_sql_memory/README.md)) | — | [`05a_multi_user_product_recommender.ipynb`](optional/notebook/05a_multi_user_product_recommender.ipynb) *(extension)*<br>[`05b_multi_user_research_agent_sql_memory.ipynb`](optional/notebook/05b_multi_user_research_agent_sql_memory.ipynb) *(extension)* |
| 33.6 | LangGraph threads, checkpoints and memory optimisations ([theory](mandatory/theory/06_langgraph_threads_checkpoints_and_memory_optimisations/README.md)) | [`06a_memory_and_conversational_agent.ipynb`](mandatory/notebook/06a_memory_and_conversational_agent.ipynb)<br>[`06b_memory_optimizations.ipynb`](mandatory/notebook/06b_memory_optimizations.ipynb) | — |

## Hands-on lab

Follow-up test: write 15 three-turn conversations and compare retrieval hit rate on turns two and three with and without history-aware query rewriting. Details: [lab/README.md](lab/README.md).

## Key concepts

[Message history](mandatory/theory/01_why_llms_forget_classic_memory_classes/README.md#message-history) · [History-aware retriever](mandatory/theory/04_conversational_rag_with_history_aware_retrieval/README.md#history-aware-retriever) · [Checkpointer / thread_id](mandatory/theory/06_langgraph_threads_checkpoints_and_memory_optimisations/README.md#checkpointer--thread_id) · [Summary memory](mandatory/theory/03_trimming_windowing_and_summary_memory/README.md#summary-memory)

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
| `mandatory/notebook/01a_why_llms_forget.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/01_why_llms_forget.ipynb` |
| `optional/notebook/01b_classic_memory_classes_and_chains.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/02_classic_memory_classes_and_chains.ipynb` |
| `mandatory/notebook/02a_runnable_with_message_history.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/03_runnable_with_message_history.ipynb` |
| `mandatory/notebook/02b_multi_user_sessions_and_persistence.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/04_multi_user_sessions_and_persistence.ipynb` |
| `mandatory/notebook/03a_trimming_windowing_and_summary.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/05_trimming_windowing_and_summary.ipynb` |
| `mandatory/notebook/04a_conversational_rag_with_history.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/06_conversational_rag_with_history.ipynb` |
| `optional/notebook/05a_multi_user_product_recommender.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/07_multi_user_product_recommender.ipynb` |
| `optional/notebook/05b_multi_user_research_agent_sql_memory.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/01_langchain_conversation_memory/notebooks/08_multi_user_research_agent_sql_memory.ipynb` |
| `mandatory/notebook/06a_memory_and_conversational_agent.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/02_langgraph_threads_and_checkpoints/notebooks/01_memory_and_conversational_agent.ipynb` |
| `mandatory/notebook/06b_memory_optimizations.ipynb` | `ai-engineering-demystified-08-advanced-agent-systems` | `modules/02_langgraph_threads_and_checkpoints/notebooks/02_memory_optimizations.ipynb` |
