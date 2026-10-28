# Course Structure: Agent Fundamentals

This course explains how a single LLM agent works and how to build one, beginning with raw API loops and progressing through tools, ReAct, LangGraph, LangChain 1.x, workflow patterns, planning, reflection, human approval, and complete applied systems.

The repository contains **14 modules, 82 instructional notebooks, and 1 exercise notebook**. Complete the modules in numeric order and the notebooks within each module in filename order unless a module says otherwise.

## Course outcomes

By the end of the course, learners will be able to:

1. Explain and implement the generate–act–observe agent loop without a framework.
2. Define, bind, execute, and validate client-side and provider-hosted tools.
3. Build ReAct agents with raw APIs, LangGraph, and LangChain 1.x.
4. Select and implement prompt chaining, routing, parallelization, orchestrator–worker, and evaluator–optimizer workflows.
5. Add planning, replanning, reflection, verification, and search-based reasoning to an agent.
6. Place human approval gates in front of consequential actions.
7. Combine the patterns into research, finance, text-to-SQL, support, analysis, and content-generation applications.

## Prerequisites

- Python, notebooks, environment variables, and chat-completions APIs
- Prompt design and structured prompting
- LangChain fundamentals: models, prompts, messages, output parsers, and LCEL
- LangGraph fundamentals: state, nodes, edges, reducers, and conditional routing
- Retrieval and RAG are helpful but not required

See [docs/prerequisites.md](prerequisites.md) and [docs/setup.md](setup.md) before running the notebooks.

## Learning sequence

| Phase | Modules | Focus |
|---|---:|---|
| I. Agent foundations | 01–04 | Build the loop, add tools, learn ReAct, and use LangChain's packaged agent APIs |
| II. Workflow patterns | 05–09 | Build predictable workflows with chaining, routing, concurrency, orchestration, and evaluation |
| III. Advanced agentic patterns | 10–12 | Add planning, reflection, verification, search, and advanced cognitive strategies |
| IV. Human control | 13 | Preview actions and require approval before execution |
| V. Applied builds | 14 | Combine the course concepts in end-to-end single-agent applications |

---

## Phase I — Agent Foundations

### Module 01 — Agents from Scratch

**Purpose:** Understand an agent by implementing its core patterns directly, before relying on a framework.

**Topics covered:**

- Generation and reflection loops
- Tool schemas, decorators, system prompts, and tool execution
- ReAct reasoning: thought, action, observation, and iteration
- Packaging reusable agent components
- Building a Streamlit-based Hacker News chatbot
- Reusing the same classes from the small `agentic_patterns` library

| Notebook | Focus |
|---|---|
| [01 — Reflection pattern](../modules/01_agents_from_scratch/notebooks/01_reflection_pattern.ipynb) | Build a raw generate–reflect loop and a `ReflectionAgent` |
| [02 — Tool-use pattern](../modules/01_agents_from_scratch/notebooks/02_tool_use_pattern.ipynb) | Create a tool decorator and tool-using agent |
| [03 — Planning with ReAct](../modules/01_agents_from_scratch/notebooks/03_planning_pattern_react.ipynb) | Implement the ReAct loop step by step, then a `ReactAgent` |
| [04 — Hacker News chatbot](../modules/01_agents_from_scratch/notebooks/04_real_world_agent_hacker_news_chatbot.ipynb) | Reuse the agent classes as the `agentic_patterns` library; real tools and a Streamlit UI |

### Module 02 — Tools and Function Calling

**Purpose:** Master the mechanism that lets models interact with code and external systems.

**Topics covered:**

- Built-in and custom LangChain tools
- Tool schemas, binding, selection, arguments, and result messages
- Manual and LangGraph tool-execution loops
- Graceful failures, validation, tracing, and evaluation
- Client-side versus provider-hosted execution
- Hosted code interpreters and sandbox configuration
- Agent-directed image generation and vision-based artifact checks

| Notebook | Focus |
|---|---|
| [01 — Defining tools](../modules/02_tools_and_function_calling/notebooks/01_defining_tools.ipynb) | Built-in and custom tools, Pydantic schemas, and the JSON schema the model sees |
| [02 — Tool calling and the manual loop](../modules/02_tools_and_function_calling/notebooks/02_tool_calling_manual_loop.ipynb) | Bind tools, read single and parallel calls, run the loop by hand, prompt-based calling |
| [03 — Augmented LLM in LangGraph](../modules/02_tools_and_function_calling/notebooks/03_augmented_llm_with_tools_langgraph.ipynb) | `ToolNode` and `tools_condition`: one tool pass, then end |
| [04 — Tool loop: errors and evaluation](../modules/02_tools_and_function_calling/notebooks/04_tool_loop_errors_and_evaluation.ipynb) | Close the loop, handle tool failures, trace the run, and judge tool use |
| [05 — Hosted vs. client-side tools](../modules/02_tools_and_function_calling/notebooks/05_hosted_vs_client_side_tools.ipynb) | Compare runtimes, traces, and failure modes |
| [06 — Hosted code execution](../modules/02_tools_and_function_calling/notebooks/06_hosted_code_execution.ipynb) | Use and inspect a hosted code interpreter |
| [07 — Agentic image generation](../modules/02_tools_and_function_calling/notebooks/07_agentic_image_generation.ipynb) | Let the agent choose when to generate and verify an image |

### Module 03 — ReAct Agents

**Purpose:** Turn tool calling into a closed-loop agent that reasons, acts, observes, and adapts.

**Topics covered:**

- Augmented LLMs versus autonomous agent loops
- Single-shot tool calling versus iterative ReAct
- LangGraph and LangChain agent construction
- Structured and parallel tool calls
- Conversation state and web research
- Applied software-engineering and browser agents
- Screenshot-driven computer use and safety mitigations

| Notebook | Focus |
|---|---|
| [01 — ReAct with LangGraph](../modules/03_react_agents/notebooks/01_react_agent_langgraph.ipynb) | Build the loop, compare it with a single-shot tool caller, and score both |
| [02 — Tool calling vs. ReAct](../modules/03_react_agents/notebooks/02_tool_calling_vs_react.ipynb) | Native tool calls vs. text-parsed `Thought / Action / Observation` |
| [03 — ReAct with `create_agent`](../modules/03_react_agents/notebooks/03_react_with_create_agent.ipynb) | Multi-step and parallel calls, built-in and custom tools, call limits, memory |
| [04 — Web research agent](../modules/03_react_agents/notebooks/04_web_research_agent.ipynb) | A plan → search → report pipeline vs. a ReAct researcher |
| [05 — SWE agent](../modules/03_react_agents/notebooks/05_swe_agent_applied.ipynb) | Fix bugs with file and test tools in a sandbox |
| [06 — Browser agent](../modules/03_react_agents/notebooks/06_browser_agent_computer_use.ipynb) | Operate a deterministic mock browser through tools |
| [07 — Vision-driven computer use](../modules/03_react_agents/notebooks/07_vision_driven_computer_use.ipynb) | Run an act–observe loop over screenshots |

**Practice:** Complete the [Intelligent Travel Assistant exercise](../modules/03_react_agents/exercises/01_intelligent_travel_assistant_agent.ipynb), building attraction-search and weather tools and a `create_agent` travel assistant. The [assignment brief](../modules/03_react_agents/exercises/intelligent_travel_assistant_brief.pdf) was written for LangChain 0.x's `create_tool_calling_agent` and `AgentExecutor`; the exercise uses the 1.x equivalent. A worked answer is in [solutions/03_react_agents](../solutions/03_react_agents/01_intelligent_travel_assistant_solution.ipynb).

### Module 04 — LangChain 1.x Agents and Middleware

**Purpose:** Use LangChain's production-oriented abstractions around the same underlying agent loop.

**Topics covered:**

- Provider-agnostic model initialization (`create_agent` itself is introduced in Module 03, tools in Module 02)
- Streaming, batching, and provider switching
- System, human, AI, and tool messages, and the message trail an agent run returns
- Metadata and token usage
- Pydantic, TypedDict, and dataclass structured outputs
- Summarization, human-in-the-loop, PII, call-limit, and custom middleware

| Notebook | Focus |
|---|---|
| [01 — Model integration](../modules/04_langchain_agents_and_middleware/notebooks/01_model_integration.ipynb) | Swap providers, stream, and batch |
| [02 — Messages](../modules/04_langchain_agents_and_middleware/notebooks/02_messages.ipynb) | Use messages as the agent's context unit; read an agent's message trail |
| [03 — Structured output](../modules/04_langchain_agents_and_middleware/notebooks/03_structured_output.ipynb) | Return schema-validated results |
| [04 — Middleware](../modules/04_langchain_agents_and_middleware/notebooks/04_middleware.ipynb) | Intercept and control the agent loop |

---

## Phase II — Workflow Patterns

Modules 05–09 cover five complementary workflow patterns. These are controlled execution structures around model calls, not multi-agent systems.

### Module 05 — Prompt Chaining

**Purpose:** Break a task into a fixed sequence of smaller, testable stages.

**Topics covered:** sequential pipelines, quality gates, bounded regeneration, Pydantic hand-offs, retries, fallbacks, LangGraph, and LCEL.

| Notebook | Focus |
|---|---|
| [01 — Prompt chaining in LangGraph](../modules/05_prompt_chaining/notebooks/01_prompt_chaining_langgraph.ipynb) | Build a gated email-generation pipeline |
| [02 — Structured-output chaining](../modules/05_prompt_chaining/notebooks/02_prompt_chaining_structured_output.ipynb) | Pass validated objects between stages |
| [03 — Prompt chaining with LCEL](../modules/05_prompt_chaining/notebooks/03_prompt_chaining_lcel.ipynb) | Rebuild the pipeline with retries and fallbacks |

### Module 06 — Routing

**Purpose:** Classify an input and dispatch it to the most suitable specialist path or model.

**Topics covered:** structured classification, conditional edges, specialist handlers, cost/capability model tiers, baseline comparison, `RunnableBranch`, and dictionary dispatch.

| Notebook | Focus |
|---|---|
| [01 — Routing in LangGraph](../modules/06_routing/notebooks/01_routing_langgraph.ipynb) | Classify and dispatch to specialist nodes |
| [02 — Routing by model tier](../modules/06_routing/notebooks/02_routing_by_model_tier.ipynb) | Choose cheap or reasoning models and measure results |
| [03 — LCEL `RunnableBranch`](../modules/06_routing/notebooks/03_routing_lcel_runnable_branch.ipynb) | Route among specialist chains |

### Module 07 — Parallelization

**Purpose:** Run independent work concurrently and merge the results.

**Topics covered:** sequential baselines, fan-out/fan-in, asymmetric branches, sectioning, reducers, multi-source retrieval, `RunnableParallel`, and concurrency controls.

| Notebook | Focus |
|---|---|
| [01 — Parallelization in LangGraph](../modules/07_parallelization/notebooks/01_parallelization_langgraph.ipynb) | Build static and asymmetric parallel paths |
| [02 — Sectioning and voting](../modules/07_parallelization/notebooks/02_parallelization_sectioning_and_voting.ipynb) | Generate independent sections concurrently; vote with parallel reviewers |
| [03 — Parallelization with LCEL](../modules/07_parallelization/notebooks/03_parallelization_lcel.ipynb) | Use `RunnableParallel` and limit concurrency |

### Module 08 — Orchestrator–Worker

**Purpose:** Decompose work dynamically when the number and nature of subtasks are not known in advance.

**Topics covered:** runtime planning, per-worker state, dynamic fan-out, LangGraph `Send`, map-reduce, synthesis, the fixed-worker anti-pattern, LCEL `Runnable.map()`, and framework trade-offs.

| Notebook | Focus |
|---|---|
| [01 — Orchestrator–worker with `Send`](../modules/08_orchestrator_worker/notebooks/01_orchestrator_worker_send_api.ipynb) | Plan and dispatch runtime-sized work (map-reduce), prove the worker count follows the input, diagnose a plan that does not drive execution |
| [02 — Orchestrator–worker with LCEL](../modules/08_orchestrator_worker/notebooks/02_orchestrator_worker_lcel_map.ipynb) | Use `Runnable.map()` and assess its limits |

### Module 09 — Evaluator–Optimizer

**Purpose:** Improve an output through a bounded generate–critique–refine cycle.

**Topics covered:** explicit evaluation criteria, structured grades, conditional refinement, stopping conditions, iteration limits, Python/LCEL loops, and `after_model` middleware.

| Notebook | Focus |
|---|---|
| [01 — Evaluator–optimizer in LangGraph](../modules/09_evaluator_optimizer/notebooks/01_evaluator_optimizer_langgraph.ipynb) | Refine until a per-criterion evaluator approves, with an iteration cap and an optional Qwen-on-Databricks judge |
| [02 — Evaluator–optimizer with LangChain](../modules/09_evaluator_optimizer/notebooks/02_evaluator_optimizer_lcel.ipynb) | Compare a bounded Python loop with middleware |

---

## Phase III — Advanced Agentic Patterns (Planning, Reflection, and Reasoning)

### Module 10 — Planning

**Purpose:** Give an agent foresight, explicit task decomposition, and the ability to recover when a plan stops working.

**Topics covered:** ReAct versus plan-first behavior, plan-and-execute, structured plans, step evaluation, replanning, research orchestration, report synthesis, and reflective plan revision.

**Architecture boundary:** Notebooks 01–02 are single-agent workflows. Notebooks 03–04 use nested agentic components and are classified as compound-agent designs. A compound agent is one overall system containing nested workflows or agentic components; it is not a multi-agent team of independent agents communicating or handing off work.

| Notebook | Architecture | Focus |
|---|---|---|
| [01 — ReAct vs. planning](../modules/10_planning/notebooks/01_planning_react_vs_plan.ipynb) | Single-agent workflow | Compare and score reactive and plan-first agents |
| [02 — Decompose, execute, replan](../modules/10_planning/notebooks/02_planning_decompose_execute_replan.ipynb) | Single-agent workflow | Evaluate steps and revise a failing plan |
| [03 — Deep-research planning agent](../modules/10_planning/notebooks/03_planning_agent_deep_research.ipynb) | Nested workflow / compound agent | Dispatch nested section-writing workflows and synthesize a structured report |
| [04 — Reflective dynamic planner](../modules/10_planning/notebooks/04_reflective_dynamic_planning_agent.ipynb) | Hierarchical compound agent | Combine planning and replanning with a nested ReAct research component |

### Module 11 — Reflection

**Purpose:** Let an agent critique, verify, and improve its own work.

**Topics covered:** Reflection versus Reflexion, external feedback, measuring reflection with hidden tests and ground truth, chain-of-verification, Self-Discover, constitutional critique, bounded revisions, and execution-driven code correction.

| Notebook | Focus |
|---|---|
| [01 — Reflection agents](../modules/11_reflection/notebooks/01_reflection_agents.ipynb) | Build a bounded generator–critic loop in LangGraph |
| [02 — Reflexion agents](../modules/11_reflection/notebooks/02_reflexion_agents.ipynb) | Revise using self-critique, external search and citations |
| [03 — Reflection architecture](../modules/11_reflection/notebooks/03_reflection_architecture.ipynb) | Run one structured generate–critique–refine pass and measure it with hidden tests |
| [04 — Chain-of-verification](../modules/11_reflection/notebooks/04_chain_of_verification.ipynb) | Verify claims through independent questions |
| [05 — Self-Discover](../modules/11_reflection/notebooks/05_self_discover.ipynb) | Compose a task-specific reasoning structure |
| [06 — Constitutional AI critique loop](../modules/11_reflection/notebooks/06_constitutional_ai_critique_loop.ipynb) | Critique and revise against written rules |
| [07 — Reflective code generation](../modules/11_reflection/notebooks/07_reflective_code_generation_agent.ipynb) | Generate, execute, diagnose, and repair code |

### Module 12 — Advanced Single-Agent Cognitive Patterns

**Purpose:** Explore more deliberate reasoning and search strategies that remain inside one agent.

**Topics covered:** self-consistency voting, tree search over intermediate steps, Monte Carlo tree search with reflection, simulation before action, metacognition and escalation, and a memory of approved outputs. (Plan–execute–verify is covered by Module 10.)

| Notebook | Focus |
|---|---|
| [01 — Self-consistency](../modules/12_advanced_cognitive_patterns/notebooks/01_self_consistency.ipynb) | Sample multiple reasoning paths, vote, and measure when voting helps |
| [02 — Tree of Thoughts](../modules/12_advanced_cognitive_patterns/notebooks/02_tree_of_thoughts.ipynb) | Propose, evaluate and beam-search intermediate steps |
| [03 — LATS](../modules/12_advanced_cognitive_patterns/notebooks/03_lats.ipynb) | Combine tree search, value estimates, and reflection |
| [04 — Mental-model simulator](../modules/12_advanced_cognitive_patterns/notebooks/04_mental_loop_simulator.ipynb) | Simulate an action and refine it before taking it |
| [05 — Reflexive metacognition](../modules/12_advanced_cognitive_patterns/notebooks/05_reflexive_metacognitive.ipynb) | Decide whether to answer, use a tool, or escalate |
| [06 — Self-improving exemplar memory](../modules/12_advanced_cognitive_patterns/notebooks/06_self_improving_exemplar_memory.ipynb) | Reuse editor-approved outputs to improve the next task's first draft |

---

## Phase IV — Human Control

### Module 13 — Human Approval Basics

**Purpose:** Keep a person in control before an agent performs a consequential action.

**Topics covered:** dry-run execution, action previews, approval gates with LangGraph `interrupt()` and `Command(resume=...)`, scripted and interactive reviewers, separation of planning and execution, fail-closed decisions, and an audit log.

| Notebook | Focus |
|---|---|
| [01 — Dry-run harness](../modules/13_human_approval_basics/notebooks/01_dry_run_harness.ipynb) | Preview an action, pause for review with `interrupt()`, and execute only the approved preview |

This module complements the human-in-the-loop middleware covered in Module 04.

---

## Phase V — Applied Single-Agent Builds

### Module 14 — Applied Projects

**Purpose:** Combine tools, ReAct, workflow patterns, structured output, and domain integrations in complete applications — each one checking its own output in code (tool data, ground-truth SQL, hand labels, the source document).

#### A. Agent applications

| Notebook | Applied topics |
|---|---|
| [01 — Research assistant agent](../modules/14_applied_single_agent_builds/notebooks/01_research_assistant_agent.ipynb) | Web search + page extraction + OpenWeatherMap tools, `create_agent`, checkpointer memory checked against tool data |
| [02 — Competitive-intelligence agent](../modules/14_applied_single_agent_builds/notebooks/02_competitive_intelligence_agent.ipynb) | Domain persona, structured brief via `response_format`, data gaps, source-grounding check |
| [03 — Financial analyst agent](../modules/14_applied_single_agent_builds/notebooks/03_financial_analyst_agent.ipynb) | OpenBB (key-free SEC/Yahoo Finance providers), scope flows and refusal, follow-ups, numbers checked against the provider |
| [04 — Text-to-SQL workflow](../modules/14_applied_single_agent_builds/notebooks/04_text2sql_workflow.ipynb) | Schema inspection, SQL generation, execution, ground-truth scoring, business rules for ambiguous terms |
| [05 — Text-to-SQL ReAct agent](../modules/14_applied_single_agent_builds/notebooks/05_text2sql_react_agent.ipynb) | SQL toolkit, read-only connection, same scoring as the workflow, cost per answer |

#### B. LLM-workflow applications

| Notebook | Applied topics |
|---|---|
| [06 — Review analyst](../modules/14_applied_single_agent_builds/notebooks/06_review_analyst.ipynb) | Structured analysis, sentiment-routed replies, instruction router with an out-of-scope intent |
| [07 — Multilingual IT support desk](../modules/14_applied_single_agent_builds/notebooks/07_multilingual_it_support_desk.ipynb) | One structured call vs a four-step translation chain, measured on the same tickets |
| [08 — Audience-tailored writer](../modules/14_applied_single_agent_builds/notebooks/08_audience_tailored_writer.ipynb) | Iterative prompts, format and number-faithfulness checks, parallel audience reports |
| [09 — Quiz generator](../modules/14_applied_single_agent_builds/notebooks/09_quiz_generator.ipynb) | PDF text cleanup, summarize → quiz chain, evidence-checked multiple-choice questions |

## Supporting theory and reference material

Use these readings alongside the corresponding modules:

- **Pattern notes:** ReAct, prompt chaining, routing, parallelization, orchestrator–worker, evaluator–optimizer, planning, and reflection under each module's `assets/theory/` directory
- **Workflow selection:** [Choosing a workflow pattern](workflow-patterns/choosing-a-workflow-pattern.md)
- **Workflows versus agents:** [Workflow vs. agentic patterns](workflow-patterns/workflow-vs-agentic-patterns.md)
- **Framework comparison:** [LangGraph vs. LangChain](workflow-patterns/langgraph-vs-langchain.md)
- **Implementation guide:** [LangChain implementations](workflow-patterns/langchain-implementations.md)
- **Complete workflow reference:** [Agentic workflows](workflow-patterns/workflows.md)
- **Architecture overview:** [All agentic architectures](patterns/all-agentic-architectures-overview.md)
- **Design-pattern reference:** [Agentic design patterns](patterns/design-patterns-reference.md)

## Recommended completion checkpoints

1. **Foundation checkpoint (Modules 01–04):** Build a ReAct agent with at least two tools, error handling, structured output, and an inspectable message trail.
2. **Workflow checkpoint (Modules 05–09):** Implement the same use case with two different workflow patterns and explain why one is a better fit.
3. **Reasoning checkpoint (Modules 10–12):** Add a bounded planner, evaluator, or verifier and measure whether it improves the baseline.
4. **Safety checkpoint (Module 13):** Put a dry-run and explicit approval step before a state-changing tool.
5. **Capstone checkpoint (Module 14):** Complete or extend one applied build with traceable decisions, bounded loops, and graceful tool failures.

## Scope boundary

This course focuses on **single-agent systems**. Provider-native agent SDKs, multi-agent systems, durable memory, agent protocols, advanced agentic RAG, production observability, security, and deployment are intentionally reserved for later repositories in the learning path. See [docs/learning-path.md](learning-path.md).
