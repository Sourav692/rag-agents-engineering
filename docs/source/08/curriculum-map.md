# Curriculum Map

Module → notebook → the one thing it teaches. Run modules in order; inside a module, run notebooks in numeric order.

## 01 · LangChain Conversation Memory

| Notebook | Learning objective |
|---|---|
| [`01_why_llms_forget.ipynb`](../modules/01_langchain_conversation_memory/notebooks/01_why_llms_forget.ipynb) | A chat model is stateless; memory is the message list you resend |
| [`02_classic_memory_classes_and_chains.ipynb`](../modules/01_langchain_conversation_memory/notebooks/02_classic_memory_classes_and_chains.ipynb) | The classic (deprecated) memory classes — buffer, window, summary, summary-buffer, vector — inside LCEL chains, and the legacy conversation chains |
| [`03_runnable_with_message_history.ipynb`](../modules/01_langchain_conversation_memory/notebooks/03_runnable_with_message_history.ipynb) | Automatic history for any runnable with RunnableWithMessageHistory and MessagesPlaceholder |
| [`04_multi_user_sessions_and_persistence.ipynb`](../modules/01_langchain_conversation_memory/notebooks/04_multi_user_sessions_and_persistence.ipynb) | Per-user sessions and SQLite / file-backed histories that survive a restart |
| [`05_trimming_windowing_and_summary.ipynb`](../modules/01_langchain_conversation_memory/notebooks/05_trimming_windowing_and_summary.ipynb) | Bound long conversations with token trimming, windows and running summaries |
| [`06_conversational_rag_with_history.ipynb`](../modules/01_langchain_conversation_memory/notebooks/06_conversational_rag_with_history.ipynb) | Add history-aware retrieval to a question-answering chain |
| [`07_multi_user_product_recommender.ipynb`](../modules/01_langchain_conversation_memory/notebooks/07_multi_user_product_recommender.ipynb) | Combine filter, recommender and rephraser chains with per-user memory |
| [`08_multi_user_research_agent_sql_memory.ipynb`](../modules/01_langchain_conversation_memory/notebooks/08_multi_user_research_agent_sql_memory.ipynb) | Give a tool-calling research agent SQL-backed multi-user memory |

## 02 · LangGraph Threads and Checkpoint Memory

| Notebook | Learning objective |
|---|---|
| [`01_memory_and_conversational_agent.ipynb`](../modules/02_langgraph_threads_and_checkpoints/notebooks/01_memory_and_conversational_agent.ipynb) | Give a LangGraph agent memory with checkpointers and thread ids, in RAM and SQLite, and read the checkpoint rows on disk |
| [`02_memory_optimizations.ipynb`](../modules/02_langgraph_threads_and_checkpoints/notebooks/02_memory_optimizations.ipynb) | Compare sequential, sliding-window (delete), trim-on-read (view) and summarisation memory on prompt tokens per turn |

## 03 · Long-Term and Persistent Memory

| Notebook | Learning objective |
|---|---|
| [`01_cross_thread_memory_store.ipynb`](../modules/03_long_term_and_persistent_memory/notebooks/01_cross_thread_memory_store.ipynb) | Remember users across threads with a LangGraph Store — `InMemoryStore`, then `PostgresStore` |
| [`02_session_memory_sqlite.ipynb`](../modules/03_long_term_and_persistent_memory/notebooks/02_session_memory_sqlite.ipynb) | Keep session-scoped memory in a store with a TTL and see how expiry really behaves |
| [`03_long_term_semantic_memory_sqlite.ipynb`](../modules/03_long_term_and_persistent_memory/notebooks/03_long_term_semantic_memory_sqlite.ipynb) | Store per-user facts as long-term semantic memory reachable from any thread |
| [`04_long_term_episodic_memory_sqlite.ipynb`](../modules/03_long_term_and_persistent_memory/notebooks/04_long_term_episodic_memory_sqlite.ipynb) | Log past tasks as append-only episodes and recall them in later threads |
| [`05_long_term_procedural_memory_sqlite.ipynb`](../modules/03_long_term_and_persistent_memory/notebooks/05_long_term_procedural_memory_sqlite.ipynb) | Version an agent's own procedures behind a human-approval interrupt, with rollback |
| [`06_combined_memory_agent_sqlite.ipynb`](../modules/03_long_term_and_persistent_memory/notebooks/06_combined_memory_agent_sqlite.ipynb) | Capstone: one agent with all five layers — checkpointer plus session, semantic, episodic and procedural memory — in a single SQLite file |

## 04 · Agentic Memory Architectures

| Notebook | Learning objective |
|---|---|
| [`01_episodic_with_semantic_memory.ipynb`](../modules/04_agentic_memory_architectures/notebooks/01_episodic_with_semantic_memory.ipynb) | Combine episodic (turn summaries) and semantic (facts the user stated) memory in one vector-indexed store, in a retrieve → generate → update agent |
| [`02_graph_memory_multi_hop.ipynb`](../modules/04_agentic_memory_architectures/notebooks/02_graph_memory_multi_hop.ipynb) | Store facts as a knowledge graph and answer multi-hop questions by traversal; optionally in Neo4j with text-to-Cypher |
| [`03_memgpt_tiered_memory.ipynb`](../modules/04_agentic_memory_architectures/notebooks/03_memgpt_tiered_memory.ipynb) | Let an agent page facts between working context and archival memory, MemGPT-style |
| [`04_voyager_skill_library.ipynb`](../modules/04_agentic_memory_architectures/notebooks/04_voyager_skill_library.ipynb) | Accumulate verified code skills, run in a child process with a timeout, and reuse or compose them before generating new code |
| [`05_agent_workflow_memory.ipynb`](../modules/04_agentic_memory_architectures/notebooks/05_agent_workflow_memory.ipynb) | Abstract successful trajectories into reusable workflows, adapt them to new tasks, and measure the saving |

## 05 · Multi-Agent Foundations

| Notebook | Learning objective |
|---|---|
| [`01_multi_agent_vs_monolithic_agent.ipynb`](../modules/05_multi_agent_foundations/notebooks/01_multi_agent_vs_monolithic_agent.ipynb) | Why a team: a monolithic ReAct agent vs. parallel specialist agents on the same request, measured and blind-judged |
| [`02_multiagent_pattern_from_scratch.ipynb`](../modules/05_multi_agent_foundations/notebooks/02_multiagent_pattern_from_scratch.ipynb) | Build agents, dependencies, a crew and a fan-in from scratch on the OpenAI SDK, then map them to `StateGraph.add_edge` |
| [`03_five_multi_agent_architectures.ipynb`](../modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb) | Build network, supervisor, tool-calling supervisor, hierarchical and custom architectures side by side |
| [`04_agent_communication.ipynb`](../modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb) | Let agents communicate by message passing, typed shared state filled by structured output, and a generator–critic loop |
| [`05_supervisor_workflow_with_human_review.ipynb`](../modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb) | A supervisor routes an article to specialist agents until it passes its checks, then a human reviews it |

## 06 · Supervisor and Hierarchical Agents

| Notebook | Learning objective |
|---|---|
| [`01_supervisor_pattern.ipynb`](../modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb) | Build an LLM supervisor that routes to researcher, writer and critic with a typed RouteDecision, a route log kept out of the transcript, and a counter-reducer loop cap proved with a stub |
| [`02_hierarchical_agents.ipynb`](../modules/06_supervisor_and_hierarchical_agents/notebooks/02_hierarchical_agents.ipynb) | Nest compiled department subgraphs, one with its own supervisor, under a CEO supervisor that chains departments and then finishes, with a capped loop at each level |

## 07 · Swarm and Handoffs

| Notebook | Learning objective |
|---|---|
| [`01_agent_handoffs.ipynb`](../modules/07_swarm_and_handoffs/notebooks/01_agent_handoffs.ipynb) | Build handoffs by hand (a tool returning `Command(goto=…, graph=Command.PARENT)`): triage → specialist with a context note, sideways and hand-back handoffs, `active_agent` persisted by a checkpointer, and a `recursion_limit` loop guard |
| [`02_multi_agent_swarm.ipynb`](../modules/07_swarm_and_handoffs/notebooks/02_multi_agent_swarm.ipynb) | Build a RAG / NL2SQL / invoice swarm with `create_agent`, read-only SQLite tools, handoff tools and `create_swarm`; a checkpointer remembers the active agent across turns |

## 08 · Collaboration and Control Patterns

| Notebook | Learning objective |
|---|---|
| [`01_blackboard_intro.ipynb`](../modules/08_collaboration_and_control_patterns/notebooks/01_blackboard_intro.ipynb) | Contrast a fixed pipeline with a blackboard controller on a conditional request, and check in code which one respected it |
| [`02_blackboard_research_team.ipynb`](../modules/08_collaboration_and_control_patterns/notebooks/02_blackboard_research_team.ipynb) | Run a research-and-writing team whose controller loops back on failed fact-checks, with code-checked preconditions |
| [`03_debate.ipynb`](../modules/08_collaboration_and_control_patterns/notebooks/03_debate.ipynb) | Argue both sides of a trade-off over several rounds, judge the transcript, and compare with a single-call answer |
| [`04_storm.ipynb`](../modules/08_collaboration_and_control_patterns/notebooks/04_storm.ipynb) | Write long-form articles from simulated multi-perspective expert interviews (STORM) |
| [`05_meta_controller.ipynb`](../modules/08_collaboration_and_control_patterns/notebooks/05_meta_controller.ipynb) | Route each request to a specialist with a typed router graph, then pick a whole architecture per task with a meta-controller (Enum strategy + registry), and check both controllers' routes in one table |
| [`06_ensemble_parallel_exploration.ipynb`](../modules/08_collaboration_and_control_patterns/notebooks/06_ensemble_parallel_exploration.ipynb) | Run three search-enabled analysts in parallel, aggregate their reports into a structured CIO verdict, and set the verdict against the analysts' votes |
| [`07_cellular_automata.ipynb`](../modules/08_collaboration_and_control_patterns/notebooks/07_cellular_automata.ipynb) | Compute shortest paths from a local cell rule, verify them against BFS and reroute around a new wall |

## 09 · Async and Parallel Multi-Agent Systems

| Notebook | Learning objective |
|---|---|
| [`01_parallel_agents.ipynb`](../modules/09_async_and_parallel_multi_agent/notebooks/01_parallel_agents.ipynb) | See how LangGraph runs nodes in parallel with zero-LLM stub graphs: supersteps, joins (separate edges vs list edge vs `defer=True`), reducers and `InvalidUpdateError`; then map-reduce over any number of documents with `Send` |
| [`02_async_multi_agent_streaming.ipynb`](../modules/09_async_and_parallel_multi_agent/notebooks/02_async_multi_agent_streaming.ipynb) | Run agents concurrently with async nodes and watch them with astream |

## 10 · Multi-Agent Applied Builds

| Notebook | Learning objective |
|---|---|
| [`01_hotel_environment_and_coordinator.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/01_hotel_environment_and_coordinator.ipynb) | Hotel system 1: the room database (dates relative to today), the compliance rules as a vector store, the agents' prompts, a coordinator with checkpointer memory per guest, and routing by agent name |
| [`02_hotel_reservation_agent.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/02_hotel_reservation_agent.ipynb) | Hotel system 2: a reservation agent with read-only SQL tools and a parameterised booking tool, forwarded to by name, with the booking checked in the database |
| [`03_hotel_compliance_checker.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/03_hotel_compliance_checker.ipynb) | Hotel system 3: a RAG compliance checker in front of the agents, with a routing loop guard and code-checked verdicts |
| [`04_hotel_edge_cases_and_errors.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/04_hotel_edge_cases_and_errors.ipynb) | Hotel system 4: injection attempts, `interrupt()` human review, state history and a past-date guard |
| [`05_hotel_testing_the_system.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/05_hotel_testing_the_system.ipynb) | Hotel system 5: self-assessed confidence, router unit tests and a scripted regression table |
| [`06_hotel_parallel_reservation_agents.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/06_hotel_parallel_reservation_agents.ipynb) | Hotel system 6: two hotels' reservation agents in parallel, with per-agent message keys and a join |
| [`07_hotel_merging_and_conversation_memory.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/07_hotel_merging_and_conversation_memory.ipynb) | Hotel system 7: an LLM merges the parallel agents' answers by priority, and a summarizer node shrinks long conversations |
| [`08_hotel_guest_language_and_sentiment.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/08_hotel_guest_language_and_sentiment.ipynb) | Hotel system 8: `translate_in → sentiment_analysis → coordinator … → translate_out`: work in English, answer in the guest's language, de-escalate angry guests, and where a lexicon analyser fails (optional local MarianMT part) |
| [`09_hotel_system_wide_error_handling.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/09_hotel_system_wide_error_handling.ipynb) | Hotel system 9: `RetryPolicy` for transient failures, errors in state, recovery paths (fallback model, degraded retrieval, a human-handoff stub) and one log file |
| [`10_hotel_web_search_integration.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/10_hotel_web_search_integration.ipynb) | Hotel system 10: a web-search agent for questions about the neighbourhood |
| [`11_developer_vs_tester_agents.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/11_developer_vs_tester_agents.ipynb) | Developer and tester agents in a capped critique-and-revise loop, building small games with a timed Python tool (a child process, not a sandbox) |
| [`12_supervisor_financial_research.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/12_supervisor_financial_research.ipynb) | A supervisor over financial-research and coding agents, with optional OpenBB data, a turn cap, and a typed numbers-only hand-off so no web text reaches the agent that runs code |
| [`13_multi_agent_research_summarization.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/13_multi_agent_research_summarization.ipynb) | A typed router over RAG, web-search and LLM agents, with a summarizer and follow-up history |
| [`14_multi_agent_research_system.ipynb`](../modules/10_multi_agent_applied_builds/notebooks/14_multi_agent_research_system.ipynb) | A one-shot planner, `Send` fan-out to real search agents, a findings reducer and a capped quality loop in one research system |

## 11 · Deep Agents and Harness Engineering

This module is taught through runnable scripts rather than notebooks.

| Script | Learning objective |
|---|---|
| [`simple_coding_agent.py`](../modules/11_deep_agents_and_harness_engineering/notebooks/simple_coding_agent.py) | Run a deepagents orchestrator with sub-agents, skills and a pluggable execution backend |
| [`long_term_memory_agent.py`](../modules/11_deep_agents_and_harness_engineering/notebooks/long_term_memory_agent.py) | Add save/recall/forget long-term memory tools and a memory-manager sub-agent to a deep agent |

Cross-module study guide: [Supervisor to Swarm](supervisor-to-swarm/README.md) — five sessions across modules 05, 06, 07 and 10.
