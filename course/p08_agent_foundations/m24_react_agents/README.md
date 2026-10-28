# M24 — ReAct Agents & LangChain create_agent

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part VIII · Agent Foundations for RAG** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 6 mandatory, 7 optional

## Why it matters

ReAct is the closed reason–act–observe loop most RAG agents run. LangChain 1.x packages it as `create_agent`, and middleware is where you add guardrails and human review.

## Learning objectives

- Build a ReAct agent in LangGraph and explain how it differs from single-shot tool calling
- Build the same agent with LangChain 1.x `create_agent`, with typed messages and structured output
- Control agents with middleware, including human-in-the-loop
- Apply ReAct to web research, software engineering and computer use

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 24.1 | The ReAct loop in LangGraph; tool calling vs ReAct | [`01a_react_agent_langgraph.ipynb`](notebooks/01a_react_agent_langgraph.ipynb)<br>[`01b_tool_calling_vs_react.ipynb`](notebooks/01b_tool_calling_vs_react.ipynb) | — |
| 24.2 | ReAct with LangChain `create_agent` | [`02a_react_with_create_agent.ipynb`](notebooks/02a_react_with_create_agent.ipynb) | — |
| 24.3 | Models, messages and structured output in LangChain 1.x | [`03c_structured_output.ipynb`](notebooks/03c_structured_output.ipynb) | [`03a_model_integration.ipynb`](optional/03a_model_integration.ipynb) *(extension)*<br>[`03b_messages.ipynb`](optional/03b_messages.ipynb) *(extension)* |
| 24.4 | Middleware, including human-in-the-loop | [`04a_middleware.ipynb`](notebooks/04a_middleware.ipynb) | — |
| 24.5 | Applied ReAct: web research, SWE and computer-use agents | [`05a_web_research_agent.ipynb`](notebooks/05a_web_research_agent.ipynb) | [`05b_swe_agent_applied.ipynb`](optional/05b_swe_agent_applied.ipynb) *(extension)*<br>[`05c_browser_agent_computer_use.ipynb`](optional/05c_browser_agent_computer_use.ipynb) *(extension)*<br>[`05d_vision_driven_computer_use.ipynb`](optional/05d_vision_driven_computer_use.ipynb) *(extension)* |
| 24.6 | Exercise: intelligent travel assistant agent (with solution) *(optional lesson)* | — | [`06a_intelligent_travel_assistant_agent.ipynb`](exercises/06a_intelligent_travel_assistant_agent.ipynb) *(extension)*<br>[`06b_intelligent_travel_assistant_solution.ipynb`](exercises/06b_intelligent_travel_assistant_solution.ipynb) *(extension)* |

## Hands-on lab

ReAct research agent: give a `create_agent` agent your RAG retriever and a web-search tool, add a middleware that blocks off-topic questions, and compare its answers with your Part VII system. Details: [lab/README.md](lab/README.md).

## Key concepts

Reason–act–observe · create_agent · Middleware · Structured output

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
| `notebooks/01a_react_agent_langgraph.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/01_react_agent_langgraph.ipynb` |
| `notebooks/01b_tool_calling_vs_react.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/02_tool_calling_vs_react.ipynb` |
| `notebooks/02a_react_with_create_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/03_react_with_create_agent.ipynb` |
| `optional/03a_model_integration.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/04_langchain_agents_and_middleware/notebooks/01_model_integration.ipynb` |
| `optional/03b_messages.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/04_langchain_agents_and_middleware/notebooks/02_messages.ipynb` |
| `notebooks/03c_structured_output.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/04_langchain_agents_and_middleware/notebooks/03_structured_output.ipynb` |
| `notebooks/04a_middleware.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/04_langchain_agents_and_middleware/notebooks/04_middleware.ipynb` |
| `notebooks/05a_web_research_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/04_web_research_agent.ipynb` |
| `optional/05b_swe_agent_applied.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/05_swe_agent_applied.ipynb` |
| `optional/05c_browser_agent_computer_use.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/06_browser_agent_computer_use.ipynb` |
| `optional/05d_vision_driven_computer_use.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/07_vision_driven_computer_use.ipynb` |
| `exercises/06a_intelligent_travel_assistant_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/exercises/01_intelligent_travel_assistant_agent.ipynb` |
| `exercises/06b_intelligent_travel_assistant_solution.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `solutions/03_react_agents/01_intelligent_travel_assistant_solution.ipynb` |
