# Advanced Agent Systems — Notebook Roadmap

**11 established modules · 53 notebooks across modules 01–10 · 2 Python teaching scripts in module 11.**

This roadmap maps the lessons actually present in this repository to their topics. Follow the existing module order and numeric notebook order; the final module is a script-based continuation. Coverage comes from notebook Markdown and implementing code cells, plus the two harness scripts. Notebook code was not executed for this roadmap.

## Before you start

Use the [setup guide](setup.md) for Python 3.12, `uv sync`, Jupyter and environment variables. The [prerequisites](prerequisites.md) cover Python, LangChain messages and LCEL, LangGraph state/reducers/checkpoints, basic retrieval and single-agent tool loops.

- **Model access:** Full runs of the notebooks use `OPENAI_API_KEY`; some mechanics can be studied without executing model sections.
- **Search and weather:** Search-enabled examples in modules 01, 02, 05, 08 and 10 use `TAVILY_API_KEY`; the module 01 research agent also uses `WEATHER_API_KEY`.
- **Local services:** Module 03 notebook 01 uses Postgres for its durable-backend section; module 04 notebook 02 has an optional Neo4j section.
- **Optional installs:** Module 10 notebook 08 uses the `hf` dependency group for optional local models; notebook 12 uses the `finance` group for optional OpenBB tools and can fall back to web search.
- **Harness access:** Module 11 scripts use Databricks model access, Tavily research and workspace-specific Genie space configuration; see the [module setup](../modules/11_deep_agents_and_harness_engineering/README.md).

**Offline portions:** Module 08 notebook 07 runs grid/pathfinding calculations offline; skip the optional Part 6 LLM cells. Module 09 notebooks 01 and 02 use models only in Part 4; their other execution-mechanics demos use stubs or timed waits, but skip the early LLM-initialization cell when studying those sections without credentials. Module 05 notebook 03 calls a model only in Part 3, although its setup constructs the model client. Other lessons contain selected stub-based checks; that does not make their full runs offline.

## Recommended sequence

| Stage | Modules | Focus |
|---|---|---|
| Conversation and persistence | 01 → 02 → 03 | Replay messages, persist threads, then share memory across threads |
| Memory architecture | 04 | Structure facts, graphs, context tiers, skills and workflows |
| Multi-agent coordination | 05 → 06 → 07 | Foundations, centralized supervision, then peer handoffs |
| Collaboration and concurrency | 08 → 09 | Richer control patterns, joins, reducers and async streams |
| Integration and harness | 10 → 11 | Applied builds followed by the script-based deep-agent harness |

Within module 10, read hotel notebooks 01–10 in order. They extend and revisit the core system through shared helpers; later notebooks are focused variants, so do not assume each incorporates every earlier extension. Notebooks 11–14 are separate applied builds. The existing [supervisor-to-swarm study route](supervisor-to-swarm/README.md) offers a focused route through modules 05–10.

## Module navigation

- [01 · LangChain conversation memory](#module-01)
- [02 · LangGraph threads and checkpoints](#module-02)
- [03 · Long-term and persistent memory](#module-03)
- [04 · Agentic memory architectures](#module-04)
- [05 · Multi-agent foundations](#module-05)
- [06 · Supervisor and hierarchical agents](#module-06)
- [07 · Swarm and handoffs](#module-07)
- [08 · Collaboration and control patterns](#module-08)
- [09 · Async and parallel multi-agent](#module-09)
- [10 · Multi-agent applied builds](#module-10)
- [11 · Deep agents and harness engineering](#module-11)

<a id="module-01"></a>

## Module 01 — LangChain conversation memory

Build message-based memory, bound its size and isolate persistent user conversations.

### [01_why_llms_forget.ipynb](../modules/01_langchain_conversation_memory/notebooks/01_why_llms_forget.ipynb)

**Topics covered:**

- **Stateless calls:** Show why separate model calls forget earlier messages.
- **Manual replay:** Resend `HumanMessage` and `AIMessage` objects to preserve context.
- **History objects:** Store turns with `InMemoryChatMessageHistory`.
- **Message roles:** Distinguish system, human and assistant messages and filter by type.

### [02_classic_memory_classes_and_chains.ipynb](../modules/01_langchain_conversation_memory/notebooks/02_classic_memory_classes_and_chains.ipynb)

**Topics covered:**

- **Classic memory API:** Inspect the deprecated `ConversationBufferMemory` API and its stored history.
- **Load–invoke–save:** Connect classic memory to LCEL with `RunnablePassthrough.assign`.
- **Bounding strategies:** Compare window, summary and summary-buffer memory in Part 3.
- **Vector recall:** Retrieve relevant past turns with Chroma and `VectorStoreRetrieverMemory`.
- **Legacy chains:** Compare automatic memory in `ConversationChain` and `LLMChain` with their replacements.

### [03_runnable_with_message_history.ipynb](../modules/01_langchain_conversation_memory/notebooks/03_runnable_with_message_history.ipynb)

**Topics covered:**

- **Automatic history:** Wrap a model or chain with `RunnableWithMessageHistory`.
- **Prompt placement:** Inject history through `MessagesPlaceholder` and configure message keys.
- **Prompt inspection:** Render the actual messages the model receives.
- **Extra inputs:** Combine session history with other prompt variables, including response language.

### [04_multi_user_sessions_and_persistence.ipynb](../modules/01_langchain_conversation_memory/notebooks/04_multi_user_sessions_and_persistence.ipynb)

**Topics covered:**

- **User isolation:** Select an independent history with each `session_id`.
- **Streaming turns:** Stream responses while saving each user's history.
- **SQLite histories:** Persist conversations with `SQLChatMessageHistory`.
- **Restart proof:** Rebuild a chain and inspect database-backed recall.
- **File histories:** Resume JSON-backed sessions with `FileChatMessageHistory`.

### [05_trimming_windowing_and_summary.ipynb](../modules/01_langchain_conversation_memory/notebooks/05_trimming_windowing_and_summary.ipynb)

**Topics covered:**

- **Token trimming:** Use `trim_messages` to fit history within a token budget.
- **Chain integration:** Trim messages before rendering the prompt on every call.
- **Exchange windows:** Implement `WindowedChatHistory` to retain the last k exchanges.
- **Running summaries:** Compress older turns while preserving recent messages verbatim.

### [06_conversational_rag_with_history.ipynb](../modules/01_langchain_conversation_memory/notebooks/06_conversational_rag_with_history.ipynb)

**Topics covered:**

- **Retrieval baseline:** Load a blog post, split it and index it in Chroma.
- **Follow-up failure:** Observe why an unresolved pronoun produces a poor retrieval query.
- **Query rewriting:** Use `create_history_aware_retriever` to turn follow-ups into standalone questions.
- **Conversation wrapper:** Add `RunnableWithMessageHistory` to the retrieval chain.

### [07_multi_user_product_recommender.ipynb](../modules/01_langchain_conversation_memory/notebooks/07_multi_user_product_recommender.ipynb)

**Topics covered:**

- **Catalogue filtering:** Generate pandas filters from natural-language requests and run them through a guarded executor.
- **Recommendation chain:** Recommend products from the filtered catalogue.
- **Query rephrasing:** Resolve a user's follow-up using earlier requests.
- **Persistent users:** Compose filtering and recommendation with SQLite-backed per-user history.

### [08_multi_user_research_agent_sql_memory.ipynb](../modules/01_langchain_conversation_memory/notebooks/08_multi_user_research_agent_sql_memory.ipynb)

**Topics covered:**

- **Research tools:** Implement web search with extraction and a weather tool.
- **Tool-calling agent:** Run tools through `AgentExecutor` with history and scratchpad placeholders.
- **SQL memory:** Wrap the agent with `RunnableWithMessageHistory` and `SQLChatMessageHistory`.
- **Contextual follow-ups:** Keep financial and weather conversations separate for two users.

**Ready to move on when:** you can explain which messages reach the model and resume two separate users from persistent history.

<a id="module-02"></a>

## Module 02 — LangGraph threads and checkpoints

Persist graph state within a thread and compare the cost of different replay strategies.

### [01_memory_and_conversational_agent.ipynb](../modules/02_langgraph_threads_and_checkpoints/notebooks/01_memory_and_conversational_agent.ipynb)

**Topics covered:**

- **Graph state:** Accumulate messages and wire a search-enabled tool loop.
- **Transient checkpoints:** Compile with `InMemorySaver` for thread-scoped state.
- **Thread identity:** Use `thread_id` to isolate conversations and revisit earlier users.
- **State history:** Inspect current state and earlier checkpoint snapshots.
- **SQLite checkpoints:** Reopen `SqliteSaver` state and inspect checkpoint rows on disk.

### [02_memory_optimizations.ipynb](../modules/02_langgraph_threads_and_checkpoints/notebooks/02_memory_optimizations.ipynb)

**Topics covered:**

- **Full-history baseline:** Measure prompt tokens as a conversation grows.
- **Sliding-window deletion:** Remove stored messages with `RemoveMessage`.
- **Trim on read:** Limit model input with `trim_messages` while retaining complete thread history.
- **Summarization state:** Keep a running summary alongside recent turns.
- **Measured trade-offs:** Compare all four strategies on the same conversation in Part 5.

**Ready to move on when:** you can inspect a saved thread and distinguish deleting messages from trimming only the model input.

<a id="module-03"></a>

## Module 03 — Long-term and persistent memory

Separate memory scopes and write rules for facts, experiences, sessions and approved procedures.

### [01_cross_thread_memory_store.ipynb](../modules/03_long_term_and_persistent_memory/notebooks/01_cross_thread_memory_store.ipynb)

**Topics covered:**

- **Store primitives:** Put, get and search items inside `InMemoryStore` namespaces.
- **Runtime context:** Pass a trusted user identity and the store to graph nodes through `Runtime`.
- **Cross-thread recall:** Recall the same user's facts on new threads while isolating other users.
- **Durable backend:** Run the store-backed graph with `PostgresStore` in Part 4.

### [02_session_memory_sqlite.ipynb](../modules/03_long_term_and_persistent_memory/notebooks/02_session_memory_sqlite.ipynb)

**Topics covered:**

- **TTL configuration:** Configure session-scoped `SqliteStore` data with `TTLConfig`.
- **Session identity:** Scope preferences to `session_id` rather than one thread.
- **Visit boundaries:** Share preferences across conversations within a visit and separate new visits.
- **Expiry behavior:** Demonstrate that expired items remain readable until the SQLite TTL sweep removes them.

### [03_long_term_semantic_memory_sqlite.ipynb](../modules/03_long_term_and_persistent_memory/notebooks/03_long_term_semantic_memory_sqlite.ipynb)

**Topics covered:**

- **Memory tools:** Read trusted user context and the store through `ToolRuntime`.
- **Preload and recall:** Insert known facts in the system prompt and expose tools for additional access.
- **User scope:** Recall facts across conversations while isolating user namespaces.
- **Stable-key updates:** Upsert a fact under its existing key instead of accumulating duplicates.

### [04_long_term_episodic_memory_sqlite.ipynb](../modules/03_long_term_and_persistent_memory/notebooks/04_long_term_episodic_memory_sqlite.ipynb)

**Topics covered:**

- **Append-only episodes:** Store a fresh timestamped experience for each logged task.
- **Recent context:** Preload the newest episodes into the system prompt.
- **Later recall:** Reference prior work from a new conversation and compare episodes with semantic facts.
- **Pruning:** Delete older experiences while retaining the most recent N episodes per user.

### [05_long_term_procedural_memory_sqlite.ipynb](../modules/03_long_term_and_persistent_memory/notebooks/05_long_term_procedural_memory_sqlite.ipynb)

**Topics covered:**

- **Active procedures:** Load approved instructions scoped to an agent identity.
- **Human approval:** Pause a proposal tool with `interrupt()` before writing the decision.
- **Resume decisions:** Use `Command(resume=...)` to approve or reject a proposed procedure.
- **Behavior changes:** Run the agent under the approved instruction set.
- **Version lifecycle:** Retire superseded procedures and roll back to an earlier approved version in Part 5.

### [06_combined_memory_agent_sqlite.ipynb](../modules/03_long_term_and_persistent_memory/notebooks/06_combined_memory_agent_sqlite.ipynb)

**Topics covered:**

- **Five memory layers:** Combine `SqliteSaver` and `SqliteStore` in one SQLite file.
- **Scope keys:** Distinguish `thread_id`, `session_id`, `user_id` and `agent_id` in Part 2.
- **Write ownership:** Upsert facts, append and prune episodes, and keep session/procedure writes outside the agent.
- **Cross-visit behavior:** Retain user facts and experiences while resetting thread and session context.
- **Storage inspection:** Read the combined database and review the Postgres migration discussion in Part 5.

**Ready to move on when:** you can choose the correct scope key and explain expiry, update, pruning and approval behavior for each layer.

<a id="module-04"></a>

## Module 04 — Agentic memory architectures

Organize remembered information and capabilities into vector, graph, tiered, skill and workflow structures.

### [01_episodic_with_semantic_memory.ipynb](../modules/04_agentic_memory_architectures/notebooks/01_episodic_with_semantic_memory.ipynb)

**Topics covered:**

- **Vector-indexed namespaces:** Keep episodic summaries and semantic triples separate within one `InMemoryStore`.
- **Memory extraction:** Summarize turns and extract facts from the user's own words with structured output.
- **Agent pipeline:** Implement retrieve → generate → update as a LangGraph flow.
- **Recall checks:** Query the memory stack and inspect what was stored for the user.

### [02_graph_memory_multi_hop.ipynb](../modules/04_agentic_memory_architectures/notebooks/02_graph_memory_multi_hop.ipynb)

**Topics covered:**

- **Graph store:** Index `(subject, relation, object)` facts in forward and backward directions.
- **Fact writer:** Extract typed triples with a restricted relation vocabulary.
- **Multi-hop reader:** Select a start entity, traverse N hops and answer from the resulting facts.
- **Hop comparison:** Compare one-hop and multi-hop answers to the same question in Part 4.
- **Optional Neo4j:** Load triples into Neo4j and execute model-written Cypher through a read-only path in Part 5.

### [03_memgpt_tiered_memory.ipynb](../modules/04_agentic_memory_architectures/notebooks/03_memgpt_tiered_memory.ipynb)

**Topics covered:**

- **Memory tiers:** Separate bounded core context and recent messages from archival memory.
- **Self-editing tools:** Append or replace core facts and insert or search archival items.
- **Context reconstruction:** Rebuild the prompt from the active memory tiers before each model call.
- **Eviction and recall:** Page old messages into the archive and bring relevant information back.

### [04_voyager_skill_library.ipynb](../modules/04_agentic_memory_architectures/notebooks/04_voyager_skill_library.ipynb)

**Topics covered:**

- **Generated-code execution:** Screen code with a denylist and run it in a child process with a timeout.
- **Skill registry:** Register named functions, descriptions, source code and usage counts.
- **Retrieval first:** Reuse or compose existing skills before generating another function.
- **Verification gate:** Check new and reused skills against test cases before accepting results.
- **Accumulation lifecycle:** Follow four tasks through generation, composition and a deliberately failing candidate.

### [05_agent_workflow_memory.ipynb](../modules/04_agentic_memory_architectures/notebooks/05_agent_workflow_memory.ipynb)

**Topics covered:**

- **Trajectory logging:** Record tool calls, outputs and errors from a small ReAct-style loop.
- **Workflow abstraction:** Convert a successful trajectory into reusable steps with placeholders.
- **Structural retrieval:** Match a new task to the shape of a saved workflow.
- **Adaptation and execution:** Fill placeholders and resolve prior step outputs at run time.
- **Planning comparison:** Count LLM calls for adaptation versus fresh planning, with fallback for novel tasks.

**Ready to move on when:** you can choose an architecture for a task and explain what the example actually stores, retrieves and reuses.

<a id="module-05"></a>

## Module 05 — Multi-agent foundations

Compare a specialist team with a single agent, then build dependencies, routing and communication from first principles.

### [01_multi_agent_vs_monolithic_agent.ipynb](../modules/05_multi_agent_foundations/notebooks/01_multi_agent_vs_monolithic_agent.ipynb)

**Topics covered:**

- **Monolithic baseline:** Run one search-enabled generalist on a market-analysis task.
- **Specialist roles:** Split the same task between news, technical and financial analysts.
- **Fan-out and synthesis:** Run specialists in parallel and combine their reports with a writer.
- **Measured comparison:** Compare reports using code-computed measures and an approach-blind structured judge.

### [02_multiagent_pattern_from_scratch.ipynb](../modules/05_multi_agent_foundations/notebooks/02_multiagent_pattern_from_scratch.ipynb)

**Topics covered:**

- **Raw agent loop:** Recap prompt helpers, a `@tool` decorator and a ReAct loop using the OpenAI SDK.
- **Dependency operators:** Give `Agent` objects roles, tasks and dependencies with `>>` and `<<`.
- **Crew execution:** Execute a sequential dependency graph with the custom `Crew` class.
- **Fan-in semantics:** Wait for both upstream agents before running `[a, b] >> c`.
- **LangGraph bridge:** Translate that dependency into `StateGraph.add_edge([a, b], c)` in Part 5.

### [03_five_multi_agent_architectures.ipynb](../modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb)

**Topics covered:**

- **Peer network:** Route directly among agents with `Command(goto=...)` in Part 1.
- **Central supervisor:** Return each worker's output to a coordinating node in Part 2.
- **Agents as tools:** Let `create_agent` delegate through agent tools with injected state in Part 3.
- **Hierarchy:** Nest compiled development and QA team subgraphs in Part 4.
- **Custom workflow:** Combine mostly fixed paths with an explicit branch in Part 5.
- **Termination bounds:** Demonstrate `recursion_limit` and catch `GraphRecursionError` on a routing loop.

### [04_agent_communication.ipynb](../modules/05_multi_agent_foundations/notebooks/04_agent_communication.ipynb)

**Topics covered:**

- **Message passing:** Append agent contributions to a shared conversation with message reducers.
- **Typed shared fields:** Pass data, analysis and recommendations through structured state.
- **Generator–critic loop:** Alternate drafting and critique on one artifact.
- **Stopping criteria:** Route conditionally until the critique passes or the refinement bound is reached.

### [05_supervisor_workflow_with_human_review.ipynb](../modules/05_multi_agent_foundations/notebooks/05_supervisor_workflow_with_human_review.ipynb)

**Topics covered:**

- **Specialist subgraphs:** Build focused club-research, market-value and writing agents.
- **Hybrid grading:** Combine structured model judgments with code-based word-count checks.
- **Supervisor repairs:** Route to the first failing check's specialist and cap repair passes.
- **Human review:** Pause after the workflow, inspect or edit the article, then resume.

**Ready to move on when:** you can explain who runs next, what agents exchange and how the workflow reaches a bounded stopping point.

<a id="module-06"></a>

## Module 06 — Supervisor and hierarchical agents

Coordinate specialist workers through typed supervisors and nested department graphs.

### [01_supervisor_pattern.ipynb](../modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb)

**Topics covered:**

- **Shared state:** Track messages, specialist outputs and a specialist-call counter.
- **Typed routing:** Validate supervisor choices with Pydantic `RouteDecision`.
- **Worker return paths:** Send researcher, writer and critic results back to the supervisor.
- **Finalization:** Produce the final answer from accumulated state.
- **Trace and bounds:** Read routing traces in Part 8 and prove the loop cap with stubs in Part 9.

### [02_hierarchical_agents.ipynb](../modules/06_supervisor_and_hierarchical_agents/notebooks/02_hierarchical_agents.ipynb)

**Topics covered:**

- **Department subgraphs:** Compile research, content and analysis teams as parent-graph nodes.
- **State contracts:** Share `TeamState` fields and add level-specific CEO and content keys.
- **Internal coordination:** Use parallel specialists in research and a writer–editor supervisor in content.
- **CEO routing:** Chain departments while returning control to the top-level supervisor.
- **Execution traces:** Follow multi-level routing and enforce counters at both supervisor levels.

**Ready to move on when:** you can trace a request through both supervisor levels and identify the state contract and loop counters.

<a id="module-07"></a>

## Module 07 — Swarm and handoffs

Transfer conversation ownership between specialists and remember the active agent on a thread.

### [01_agent_handoffs.ipynb](../modules/07_swarm_and_handoffs/notebooks/01_agent_handoffs.ipynb)

**Topics covered:**

- **Conversation ownership:** Compare supervisor routing with an agent transferring control to a peer.
- **Handoff commands:** Return `Command` with `graph=Command.PARENT`, state updates and a destination.
- **Triage graph:** Compose `create_agent` specialists in a parent `StateGraph`.
- **Active agent:** Persist `active_agent` with a checkpointer to select the next turn's entry point.
- **Loop guard:** Prove ownership with scripted messages and bound repeated transfers with `recursion_limit`.

### [02_multi_agent_swarm.ipynb](../modules/07_swarm_and_handoffs/notebooks/02_multi_agent_swarm.ipynb)

**Topics covered:**

- **Three specialists:** Build and inspect independent RAG, NL2SQL and invoice agents.
- **Database boundaries:** Restrict model-written SQL to reads and use parameters for invoice queries.
- **RAG knowledge:** Retrieve music-store knowledge from local documents indexed in Chroma.
- **Swarm assembly:** Attach `create_handoff_tool` tools and compose agents with `create_swarm` in Part 6.
- **Thread ownership:** Verify cross-agent routing and remembered active-agent identity over multiple turns.

**Ready to move on when:** you can explain a parent-graph handoff command and show how the next user turn finds its active specialist.

<a id="module-08"></a>

## Module 08 — Collaboration and control patterns

Compare shared-artifact collaboration, adversarial reasoning, architecture selection and local-rule coordination.

### [01_blackboard_intro.ipynb](../modules/08_collaboration_and_control_patterns/notebooks/01_blackboard_intro.ipynb)

**Topics covered:**

- **Search specialists:** Execute real search tools inside each analyst's `create_agent` loop.
- **Sequential baseline:** Run news, technical, financial and writing nodes in a fixed order.
- **Blackboard routing:** Let a typed controller choose specialists from the shared contributions.
- **Conditional execution:** Skip analysis that the request's sentiment condition does not require.
- **Code-based comparison:** Check which specialists actually ran instead of relying on report wording.

### [02_blackboard_research_team.ipynb](../modules/08_collaboration_and_control_patterns/notebooks/02_blackboard_research_team.ipynb)

**Topics covered:**

- **Typed contributions:** Post research, checks, outlines and drafts as structured blackboard entries.
- **Controller loop:** Return to the controller after each specialist and revisit research when checks fail.
- **Routing guards:** Enforce preconditions, bounded steps and a rule-based fallback.
- **Draft dependency:** Require checked findings before an outline and an outline before a final draft.
- **Evidence limits:** The researcher and checker use model knowledge and internal consistency, without live source verification.

### [03_debate.ipynb](../modules/08_collaboration_and_control_patterns/notebooks/03_debate.ipynb)

**Topics covered:**

- **Opposing personas:** Assign fixed stances and honest-argument instructions to two debaters.
- **Round-robin loop:** Alternate rebuttals and stop with an explicit round counter.
- **Structured verdict:** Ask a neutral judge for each side's strongest point and a synthesized decision.
- **Cost comparison:** Compare the `2N + 1`-call debate with a one-call answer in Part 5.

### [04_storm.ipynb](../modules/08_collaboration_and_control_patterns/notebooks/04_storm.ipynb)

**Topics covered:**

- **Perspective generation:** Create distinct editor personas with structured output.
- **Simulated interviews:** Alternate persona-editor and expert roles across multiple Q&A turns.
- **Outline synthesis:** Merge interview notes into ordered article sections.
- **Section drafting:** Write long-form content from the collected model-generated notes.
- **Call accounting:** Measure every LLM call and compare totals with the workflow arithmetic.

### [05_meta_controller.ipynb](../modules/08_collaboration_and_control_patterns/notebooks/05_meta_controller.ipynb)

**Topics covered:**

- **Specialist router:** Dispatch typed choices with `add_conditional_edges`.
- **Search execution:** Reuse a tool-calling search agent as both a specialist and a strategy.
- **Architecture registry:** Put direct answering, search, multi-step planning and debate behind callable interfaces.
- **Meta-classification:** Choose the whole strategy through a structured enum decision.
- **Route checks:** Compare both controllers' selected paths against expected task shapes.

### [06_ensemble_parallel_exploration.ipynb](../modules/08_collaboration_and_control_patterns/notebooks/06_ensemble_parallel_exploration.ipynb)

**Topics covered:**

- **Independent perspectives:** Keep bullish, value and quantitative analysts unaware of each other's reports.
- **Tool-using analysis:** Give each analyst a search-enabled `create_agent` loop.
- **Explicit join:** Wait for all analysts with `add_edge(ANALYSTS, cio_synthesizer)`.
- **Structured synthesis:** Merge evidence into a typed CIO recommendation.
- **Vote comparison:** Compare the analysts' majority vote with the aggregator's verdict.

### [07_cellular_automata.ipynb](../modules/08_collaboration_and_control_patterns/notebooks/07_cellular_automata.ipynb)

**Topics covered:**

- **Local cell rules:** Apply synchronous neighbor-based updates across a warehouse grid.
- **Wave propagation:** Spread distances from a target until the grid stabilizes.
- **Path readout:** Move items down the distance gradient toward the packing station.
- **BFS reference:** Compare emergent path lengths with breadth-first shortest paths.
- **Obstacle adaptation:** Recompute the wave after adding a blockage.
- **Optional narration:** Summarize measured results with an LLM in Part 6; the grid computation needs no model.

**Ready to move on when:** you can choose a coordination pattern and explain its stopping rule, evidence source and measured cost or behavior.

<a id="module-09"></a>

## Module 09 — Async and parallel multi-agent

Understand joins, concurrent state updates and streamed asynchronous execution.

### [01_parallel_agents.ipynb](../modules/09_async_and_parallel_multi_agent/notebooks/01_parallel_agents.ipynb)

**Topics covered:**

- **Supersteps:** Record which parallel branches execute together in Part 1.
- **Join behavior:** Compare separate incoming edges, a list edge and `defer=True` for unequal branch lengths.
- **Concurrent writes:** Trigger `InvalidUpdateError` and fix it with list or dictionary reducers.
- **Dynamic fan-out:** Emit one `Send` per input document in Part 4.
- **Map-reduce:** Summarize documents in parallel and combine their results with model calls.

### [02_async_multi_agent_streaming.ipynb](../modules/09_async_and_parallel_multi_agent/notebooks/02_async_multi_agent_streaming.ipynb)

**Topics covered:**

- **Overlapping waits:** Measure sequential awaits against `asyncio.gather`.
- **Async graph nodes:** Run independent asynchronous research nodes together with `ainvoke`.
- **Progress streams:** Compare `astream` updates with complete state values.
- **Text streaming:** Consume message chunks and node metadata from two concurrent LLM writers in Part 4.
- **Whole-system concurrency:** Run independent graph invocations side by side.
- **Async limits:** Explain why dependent chains and CPU-bound work do not gain the same overlap.

**Ready to move on when:** you can predict join behavior, resolve conflicting writes and distinguish state updates from streamed message chunks.

<a id="module-10"></a>

## Module 10 — Multi-agent applied builds

Compose memory, routing, tools, parallelism, review and recovery in progressively richer applications.

### [01_hotel_environment_and_coordinator.ipynb](../modules/10_multi_agent_applied_builds/notebooks/01_hotel_environment_and_coordinator.ipynb)

**Topics covered:**

- **Hotel environment:** Seed SQLite room and reservation tables with dates relative to the run.
- **Rule retrieval:** Index compliance rules and expose them through a retrieval tool.
- **Agent prompts:** Define coordinator and specialist responsibilities in `hotel_common.py`.
- **Coordinator memory:** Compare two-turn behavior with and without `InMemorySaver`.
- **Forwarding convention:** Inspect how a coordinator names the specialist that should handle the request.

### [02_hotel_reservation_agent.ipynb](../modules/10_multi_agent_applied_builds/notebooks/02_hotel_reservation_agent.ipynb)

**Topics covered:**

- **SQL boundaries:** Run generated SQL on a read-only connection and book through a parameterized `book_room` tool.
- **Reservation loop:** Connect the reservation model to tools using `tools_condition`.
- **Coordinator routing:** Read the specialist name from the coordinator's reply.
- **Outcome inspection:** Query the reservation table to confirm the scripted booking actually changed data.

### [03_hotel_compliance_checker.ipynb](../modules/10_multi_agent_applied_builds/notebooks/03_hotel_compliance_checker.ipynb)

**Topics covered:**

- **Compliance retrieval:** Retrieve relevant hotel rules before generating a verdict.
- **Three-agent flow:** Route coordinator → compliance → coordinator → reservation.
- **Repeat-check guard:** Avoid sending the same guest turn through compliance twice.
- **Verdict checks:** Inspect compliant, violating and booking outcomes in code.

### [04_hotel_edge_cases_and_errors.ipynb](../modules/10_multi_agent_applied_builds/notebooks/04_hotel_edge_cases_and_errors.ipynb)

**Topics covered:**

- **Injection-style requests:** Inspect what happens when guest text influences generated SQL.
- **Human review:** Pause policy violations with `interrupt()` and resume approval or rejection with `Command`.
- **Checkpoint inspection:** Read `get_state()` and `get_state_history()` around a paused run.
- **Date validation:** Extract typed booking dates and refuse dates in the past.

### [05_hotel_testing_the_system.ipynb](../modules/10_multi_agent_applied_builds/notebooks/05_hotel_testing_the_system.ipynb)

**Topics covered:**

- **Confidence state:** Add a typed score beside conversation messages.
- **Structured assessment:** Return confidence through `with_structured_output`.
- **Routing threshold:** Ask for clarification when confidence falls below the forwarding threshold.
- **Router unit checks:** Exercise routing decisions without an LLM.
- **Regression cases:** Record routes, verdicts and outcomes in a scripted end-to-end table.

### [06_hotel_parallel_reservation_agents.ipynb](../modules/10_multi_agent_applied_builds/notebooks/06_hotel_parallel_reservation_agents.ipynb)

**Topics covered:**

- **Two hotel stores:** Give each reservation agent its own SQLite database.
- **Reducer failure:** Demonstrate parallel writes to an un-reduced state key.
- **Branch isolation:** Separate tool-loop histories with `ToolNode(messages_key=...)` and matching `tools_condition` keys.
- **Join failure:** Compare unsynchronized tool-loop completion with branch-specific synchronization nodes.
- **Working parallel graph:** Join both hotel results before producing the guest reply.

### [07_hotel_merging_and_conversation_memory.ipynb](../modules/10_multi_agent_applied_builds/notebooks/07_hotel_merging_and_conversation_memory.ipynb)

**Topics covered:**

- **Priority merging:** Let an LLM combine both hotel answers in hotel-priority order.
- **Conversation inspection:** Read guest and agent messages from checkpointed state.
- **Summary node:** Save a running summary and remove older messages with `RemoveMessage`.
- **Thread continuity:** Use the changed graph on the existing thread and preserve relevant context.

### [08_hotel_guest_language_and_sentiment.ipynb](../modules/10_multi_agent_applied_builds/notebooks/08_hotel_guest_language_and_sentiment.ipynb)

**Topics covered:**

- **Typed translation:** Detect a language and produce English input with one structured model call.
- **Guest state:** Store language, original text, sentiment and reply separately for each thread.
- **Lexicon sentiment:** Apply TextBlob polarity to translated English and prompt de-escalation for negative tone.
- **Composed pipeline:** Translate in, analyze sentiment, run hotel agents and translate the final reply out.
- **Behavior checks:** Check language, booking and apology behavior across scripted guest conversations.
- **Optional local models:** Inspect lexicon limits in Part 6 and Hugging Face alternatives in Part 7.

### [09_hotel_system_wide_error_handling.ipynb](../modules/10_multi_agent_applied_builds/notebooks/09_hotel_system_wide_error_handling.ipynb)

**Topics covered:**

- **Error state:** Catch typed failures in nodes and record a structured `error` field.
- **Central logging:** Log node, error details and thread identity through one handler.
- **Recovery routing:** Select an alternative model, degraded retrieval or human intervention.
- **Transient retries:** Apply a node `RetryPolicy` and compare runs with and without it.
- **Injected failures:** Trigger repeatable failures and verify which recovery path executed.

### [10_hotel_web_search_integration.ipynb](../modules/10_multi_agent_applied_builds/notebooks/10_hotel_web_search_integration.ipynb)

**Topics covered:**

- **Search tool:** Fetch titles, URLs and snippets with `TavilySearch`.
- **Web specialist:** Run a dedicated search tool loop with a source-grounded prompt.
- **Additional route:** Forward outside-world questions to `web_search_assistant`.
- **Routing checks:** Inspect streamed node updates for a neighborhood question and a booking.

### [11_developer_vs_tester_agents.ipynb](../modules/10_multi_agent_applied_builds/notebooks/11_developer_vs_tester_agents.ipynb)

**Topics covered:**

- **Critique and revision:** Alternate developer and tester contributions on one shared conversation.
- **Python tool:** Execute developer-generated code in a timed child process without keyboard input.
- **Tester reports:** Produce review scores, proposed unit tests and fixes rather than an independent execution guarantee.
- **Termination proof:** Check the reflection-round bound with stub nodes in Part 6.
- **Applied games:** Inspect FLAMES and Tic-Tac-Toe builds with reference implementations in Parts 8–9.

### [12_supervisor_financial_research.ipynb](../modules/10_multi_agent_applied_builds/notebooks/12_supervisor_financial_research.ipynb)

**Topics covered:**

- **Financial tools:** Combine Tavily search with optional OpenBB prices, fundamentals, news and market data.
- **Coding specialist:** Run timed Python calculations and save chart files.
- **Typed market data:** Transfer structured research results through the `MarketData` schema.
- **Supervisor loop:** Route between researcher and coder using a pure decision function and turn cap.
- **Run inspection:** Prove the bound with stubs and trace research/coding outputs.

### [13_multi_agent_research_summarization.ipynb](../modules/10_multi_agent_applied_builds/notebooks/13_multi_agent_research_summarization.ipynb)

**Topics covered:**

- **Local RAG specialist:** Index the fictional restaurant knowledge base in Chroma.
- **Web specialist:** Search DuckDuckGo and extract relevant facts with their sources.
- **Pure typed routing:** Dispatch a structured `Literal` choice to RAG, web research or direct LLM answering.
- **Structured summary:** Turn each specialist's output into the final answer.
- **Conversation memory:** Preserve follow-up context and isolate threads with a checkpointer.

### [14_multi_agent_research_system.ipynb](../modules/10_multi_agent_applied_builds/notebooks/14_multi_agent_research_system.ipynb)

**Topics covered:**

- **One-shot planning:** Decompose a topic into targeted search queries before seeing results.
- **Parallel search:** Fan out with `Send` and append typed findings through a reducer.
- **Synthesis stages:** Analyze findings and draft a report with separate nodes.
- **Quality loop:** Revise report writing until the typed score passes or the revision cap is reached.
- **Async progress:** Run with `astream` and inspect completion updates in Part 7.
- **Wiring checks:** Use stub nodes in Part 6 to verify joins and bounded revision paths.

**Ready to move on when:** you can trace a hotel or research request and verify routing, state changes, join behavior and termination.

<a id="module-11"></a>

## Module 11 — Deep agents and harness engineering

Read the script-based harness that packages orchestration, skills, specialist sub-agents and cross-thread memory.

This module contains no `.ipynb` files. Read the following scripts in order with the [module guide](../modules/11_deep_agents_and_harness_engineering/README.md).

### [simple_coding_agent.py](../modules/11_deep_agents_and_harness_engineering/notebooks/simple_coding_agent.py)

**Topics covered:**

- **Harness construction:** Configure `create_deep_agent` with tools, skills, a backend and a checkpointer.
- **Specialist delegation:** Compose developer, reviewer, researcher and four insurance analytics sub-agents.
- **Domain tools:** Wrap configured Genie spaces in tools that return answers, SQL and result metadata.
- **Backend choice:** Select virtual `FilesystemBackend` or host-executing `LocalShellBackend` through `USE_SANDBOX`.
- **Task streams:** Use a new task thread for each prompt and display agent state updates.

### [long_term_memory_agent.py](../modules/11_deep_agents_and_harness_engineering/notebooks/long_term_memory_agent.py)

**Topics covered:**

- **JSON persistence:** Save categorized preferences, facts and decisions in `long_term_memories.json`.
- **Memory operations:** Expose `save_memory`, `recall_memories` and `forget_memory` as tools.
- **Memory specialist:** Add a memory-manager sub-agent and explicit instructions to recall relevant context.
- **Thread lifecycle:** Start a fresh conversation with `new` while retaining JSON-backed memories across restarts.
- **Storage boundary:** Keep thread checkpoints in RAM; the commented Postgres upgrade is guidance, not an implemented backend.

**Backend detail:** With the default filesystem backend, `/skills/` resolves beside the scripts. With `USE_SANDBOX=true`, the backend root changes to `notebooks/projects/`; the module guide documents copying or linking skills into that root. `LocalShellBackend` executes on the host without isolation.

**Ready to move on when:** you can explain which state survives a restart, how skills resolve under the backend and when code executes on the host.

## Coverage boundaries

- **Research-inspired examples:** MemGPT, Voyager and Agent Workflow Memory lessons implement teaching versions of the patterns; names do not imply a complete upstream implementation.
- **Source grounding:** The blackboard research team checks model-generated findings for internal consistency; STORM uses simulated interviews and model-generated notes rather than live source retrieval.
- **Code execution:** Child-process timeouts and denylists in coding examples are guards, not isolation guarantees.
- **Persistence scope:** An in-memory store or checkpointer lasts only within its process; SQLite, Postgres and the harness JSON file have different durability and concurrency properties.
- **Curriculum scope:** SDK-native multi-agent sections are planned in module 07; protocols, advanced RAG, production deployment and evaluation curricula live elsewhere, as described in the [repository scope](../README.md#out-of-scope).

For the concise objective index, see the [curriculum map](curriculum-map.md). For the broader course sequence, see the [learning path](learning-path.md).
