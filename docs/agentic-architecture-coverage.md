# Agentic Architecture Coverage

Comparison of [FareedKhan-dev/all-agentic-architectures](https://github.com/FareedKhan-dev/all-agentic-architectures) (35 architectures) with repos 06, 08 and 09.

## Verdict

**All 35 architectures are covered.** 33 have a dedicated notebook, 1 is merged into another notebook (PEV), and 1 is taught as an adaptation (RLHF self-improvement).

| Family | Architectures | Covered |
|---|---|---|
| Reasoning & Reflection | 5 | 5/5 |
| Sampling & Search | 5 | 5/5 |
| Retrieval (RAG) | 5 | 5/5 |
| Memory | 5 | 5/5 |
| Tools & Actions | 6 | 6/6 |
| Multi-agent | 5 | 5/5 |
| Safety, Routing & Specialty | 4 | 4/4 |

## Architecture-by-architecture mapping

| # | Architecture | Family | Status | Your notebook(s) | Module |
|---|---|---|---|---|---|
| 1 | [Reflection](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/01_reflection.ipynb) | Reasoning & Reflection | Covered | [`06/11/01_reflection_agents`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/11_reflection/notebooks/01_reflection_agents.ipynb)<br>[`06/01/01_reflection_pattern`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/01_agents_from_scratch/notebooks/01_reflection_pattern.ipynb) | M16 |
| 2 | [Tool Use](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/02_tool_use.ipynb) | Tools & Actions | Covered | [`06/01/02_tool_use_pattern`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/01_agents_from_scratch/notebooks/02_tool_use_pattern.ipynb)<br>[`06/02/03_augmented_llm_with_tools_langgraph`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/02_tools_and_function_calling/notebooks/03_augmented_llm_with_tools_langgraph.ipynb) | M13 |
| 3 | [ReAct](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/03_react.ipynb) | Tools & Actions | Covered | [`06/03/01_react_agent_langgraph`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/03_react_agents/notebooks/01_react_agent_langgraph.ipynb) | M14 |
| 4 | [Tools & Actions](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/04_planning.ipynb) | Tools & Actions | Covered | [`06/10/01_planning_react_vs_plan`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/10_planning/notebooks/01_planning_react_vs_plan.ipynb) | M16 |
| 5 | [Multi-Agent (supervisor + specialists)](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/05_multi_agent.ipynb) | Multi-agent | Covered | [`08/06/01_supervisor_pattern`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/06_supervisor_and_hierarchical_agents/notebooks/01_supervisor_pattern.ipynb)<br>[`08/05/03_five_multi_agent_architectures`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/05_multi_agent_foundations/notebooks/03_five_multi_agent_architectures.ipynb) | M25 |
| 6 | [Plan–Execute–Verify (PEV)](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/06_pev.ipynb) | Tools & Actions | Covered (merged) | [`06/10/02_planning_decompose_execute_replan`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/10_planning/notebooks/02_planning_decompose_execute_replan.ipynb) | M16 |
| 7 | [Blackboard](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/07_blackboard.ipynb) | Multi-agent | Covered | [`08/08/01_blackboard_intro`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/08_collaboration_and_control_patterns/notebooks/01_blackboard_intro.ipynb)<br>[`08/08/02_blackboard_research_team`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/08_collaboration_and_control_patterns/notebooks/02_blackboard_research_team.ipynb) | M26 |
| 8 | [Episodic + Semantic Memory](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/08_episodic_semantic_memory.ipynb) | Memory | Covered | [`08/04/01_episodic_with_semantic_memory`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/04_agentic_memory_architectures/notebooks/01_episodic_with_semantic_memory.ipynb) | M24 |
| 9 | [Tree of Thoughts](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/09_tree_of_thoughts.ipynb) | Sampling & Search | Covered | [`06/12/02_tree_of_thoughts`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/12_advanced_cognitive_patterns/notebooks/02_tree_of_thoughts.ipynb) | M16 |
| 10 | [Mental Loop (simulator)](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/10_mental_loop.ipynb) | Sampling & Search | Covered | [`06/12/04_mental_loop_simulator`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/12_advanced_cognitive_patterns/notebooks/04_mental_loop_simulator.ipynb) | M16 |
| 11 | [Meta-Controller](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/11_meta_controller.ipynb) | Multi-agent | Covered | [`08/08/05_meta_controller`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/08_collaboration_and_control_patterns/notebooks/05_meta_controller.ipynb) | M26 |
| 12 | [Graph (world-model) Memory](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/12_graph_memory.ipynb) | Memory | Covered | [`08/04/02_graph_memory_multi_hop`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/04_agentic_memory_architectures/notebooks/02_graph_memory_multi_hop.ipynb) | M24 |
| 13 | [Ensemble](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/13_ensemble.ipynb) | Sampling & Search | Covered | [`08/08/06_ensemble_parallel_exploration`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/08_collaboration_and_control_patterns/notebooks/06_ensemble_parallel_exploration.ipynb) | M26 |
| 14 | [Dry-Run Harness](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/14_dry_run.ipynb) | Safety, Routing & Specialty | Covered | [`06/13/01_dry_run_harness`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/13_human_approval_basics/notebooks/01_dry_run_harness.ipynb) | M17 |
| 15 | [RLHF Self-Improvement](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/15_rlhf_self_improvement.ipynb) | Safety, Routing & Specialty | Covered (adapted) | [`06/12/06_self_improving_exemplar_memory`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/12_advanced_cognitive_patterns/notebooks/06_self_improving_exemplar_memory.ipynb) | M16 |
| 16 | [Cellular Automata](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/16_cellular_automata.ipynb) | Safety, Routing & Specialty | Covered | [`08/08/07_cellular_automata`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/08_collaboration_and_control_patterns/notebooks/07_cellular_automata.ipynb) | M26 |
| 17 | [Reflexive Metacognitive](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/17_reflexive_metacognitive.ipynb) | Safety, Routing & Specialty | Covered | [`06/12/05_reflexive_metacognitive`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/12_advanced_cognitive_patterns/notebooks/05_reflexive_metacognitive.ipynb) | M16 |
| 18 | [Reflexion](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/18_reflexion.ipynb) | Reasoning & Reflection | Covered | [`06/11/02_reflexion_agents`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/11_reflection/notebooks/02_reflexion_agents.ipynb) | M16 |
| 19 | [Self-Discover](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/19_self_discover.ipynb) | Reasoning & Reflection | Covered | [`06/11/05_self_discover`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/11_reflection/notebooks/05_self_discover.ipynb) | M16 |
| 20 | [Chain-of-Verification](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/20_chain_of_verification.ipynb) | Reasoning & Reflection | Covered | [`06/11/04_chain_of_verification`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/11_reflection/notebooks/04_chain_of_verification.ipynb) | M16 |
| 21 | [Self-Consistency](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/21_self_consistency.ipynb) | Sampling & Search | Covered | [`06/12/01_self_consistency`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/12_advanced_cognitive_patterns/notebooks/01_self_consistency.ipynb) | M16 |
| 22 | [LATS](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/22_lats.ipynb) | Sampling & Search | Covered | [`06/12/03_lats`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/12_advanced_cognitive_patterns/notebooks/03_lats.ipynb) | M16 |
| 23 | [Agentic RAG](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/23_agentic_rag.ipynb) | Retrieval (RAG) | Covered | [`09/01/01_simple_agentic_rag`](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag/blob/main/modules/01_retrieval_grading_and_query_rewriting/notebooks/01_simple_agentic_rag.ipynb)<br>[`09/05/01_rag_as_tool_in_agents`](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag/blob/main/modules/05_rag_as_an_agent_tool/notebooks/01_rag_as_tool_in_agents.ipynb) | M18, M21 |
| 24 | [Corrective RAG (CRAG)](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/24_corrective_rag.ipynb) | Retrieval (RAG) | Covered | [`09/02/01_agentic_corrective_rag_langgraph`](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag/blob/main/modules/02_corrective_rag/notebooks/01_agentic_corrective_rag_langgraph.ipynb) | M19 |
| 25 | [Self-RAG](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/25_self_rag.ipynb) | Retrieval (RAG) | Covered | [`09/03/01_self_rag_langgraph`](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag/blob/main/modules/03_self_rag/notebooks/01_self_rag_langgraph.ipynb) | M19 |
| 26 | [Adaptive RAG](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/26_adaptive_rag.ipynb) | Retrieval (RAG) | Covered | [`09/04/04_adaptive_rag_langgraph`](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag/blob/main/modules/04_adaptive_rag_and_routing/notebooks/04_adaptive_rag_langgraph.ipynb) | M20 |
| 27 | [GraphRAG](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/27_graph_rag.ipynb) | Retrieval (RAG) | Covered | [`09/10/03_microsoft_graphrag`](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag/blob/main/modules/10_graphrag_techniques/notebooks/03_microsoft_graphrag.ipynb)<br>[`09/09/05_roman_empire_graph_rag`](https://github.com/Sourav692/ai-engineering-demystified-09-advanced-rag/blob/main/modules/09_knowledge_graphs_with_neo4j/notebooks/05_roman_empire_graph_rag.ipynb) | M29, M30 |
| 28 | [Debate](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/28_debate.ipynb) | Multi-agent | Covered | [`08/08/03_debate`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/08_collaboration_and_control_patterns/notebooks/03_debate.ipynb) | M26 |
| 29 | [Voyager (skill library)](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/29_voyager.ipynb) | Memory | Covered | [`08/04/04_voyager_skill_library`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/04_agentic_memory_architectures/notebooks/04_voyager_skill_library.ipynb) | M24 |
| 30 | [STORM](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/30_storm.ipynb) | Multi-agent | Covered | [`08/08/04_storm`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/08_collaboration_and_control_patterns/notebooks/04_storm.ipynb) | M26 |
| 31 | [MemGPT](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/31_memgpt.ipynb) | Memory | Covered | [`08/04/03_memgpt_tiered_memory`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/04_agentic_memory_architectures/notebooks/03_memgpt_tiered_memory.ipynb) | M24 |
| 32 | [Constitutional AI](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/32_constitutional_ai.ipynb) | Reasoning & Reflection | Covered | [`06/11/06_constitutional_ai_critique_loop`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/11_reflection/notebooks/06_constitutional_ai_critique_loop.ipynb) | M16 |
| 33 | [SWE-Agent](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/33_swe_agent.ipynb) | Tools & Actions | Covered | [`06/03/05_swe_agent_applied`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/03_react_agents/notebooks/05_swe_agent_applied.ipynb) | M14 |
| 34 | [Computer Use / Browser Agent](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/34_computer_use.ipynb) | Tools & Actions | Covered | [`06/03/06_browser_agent_computer_use`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/03_react_agents/notebooks/06_browser_agent_computer_use.ipynb)<br>[`06/03/07_vision_driven_computer_use`](https://github.com/Sourav692/ai-engineering-demystified-06-agent-fundamentals/blob/main/modules/03_react_agents/notebooks/07_vision_driven_computer_use.ipynb) | M14 |
| 35 | [Agent Workflow Memory](https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/notebooks/35_agent_workflow_memory.ipynb) | Memory | Covered | [`08/04/05_agent_workflow_memory`](https://github.com/Sourav692/ai-engineering-demystified-08-advanced-agent-systems/blob/main/modules/04_agentic_memory_architectures/notebooks/05_agent_workflow_memory.ipynb) | M24 |

### Notes on partial matches

- **Plan–Execute–Verify (PEV) (#6):** No standalone notebook. Repo 06 removed it as a duplicate; the per-step verifier and replanning are taught inside the decompose–execute–replan notebook.
- **RLHF Self-Improvement (#15):** Taught as an exemplar memory of editor-approved outputs, described as an RLHF analogy. Upstream is also not real RLHF (deterministic scoring plus an archive), so the idea matches.
- **Cellular Automata (#16):** Marked optional in the curriculum.
- **Computer Use / Browser Agent (#34):** Both notebooks are optional in the curriculum.

## In your repos but not in the upstream catalogue

| Area | Patterns | Repo · module |
|---|---|---|
| Workflow patterns | Prompt chaining, routing, parallelization, orchestrator–worker, evaluator–optimizer | 06 · M15 |
| Multi-agent topologies | Network, agents-as-tools (tool-calling supervisor), hierarchical teams, handoffs, swarm | 08 · M25 |
| Async multi-agent | Send map-reduce, async nodes, streaming | 08 · M26 |
| Deep agents | Orchestrator with sub-agents, skills, long-term memory and an execution backend | 08 · M27 |
| Conversation & persistent memory | Buffer/window/summary memory, checkpointed threads, cross-thread store, procedural memory | 08 · M23–M24 |
| Human-in-the-loop middleware | Approval through LangChain 1.x middleware and interrupts | 06 · M14 |
| Planning variants | Deep-research planner, reflective dynamic planning | 06 · M16 |
| RAG-specific agent patterns | Multi-knowledge-base router RAG, RAG as an agent tool, Reliable RAG, retrieval feedback loop | 09 · M20–M22 |

## In the upstream repo but not in yours

These are engineering extras, not architectures:

- **Benchmark harness:** Per-task leaderboard comparing all architectures on the same tasks
- **Deterministic-picker pattern:** One documented technique reused across architectures to make outputs reproducible
- **Packaged library:** Architectures as an installable package with provider switching, evaluators, tracing and a UI

## Housekeeping

- `docs/patterns/all-agentic-architectures-overview.md` in repo 06 is a copy of an older upstream README. It lists only the first 17 architectures (#1–#17), although #18–#35 are already taught across repos 06, 08 and 09. Updating it to the 35-item list would make the coverage visible.
