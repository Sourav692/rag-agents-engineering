# M23 — ReAct Agents & LangChain create_agent

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part VI · Agent Foundations** · **Level:** Core · **Time:** ~4 h · **Notebooks:** 5 mandatory, 4 optional

## Why it matters

ReAct is the closed reason–act–observe loop most RAG agents run. LangChain 1.x packages it as `create_agent`, and middleware is where you add guardrails and human review.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [The ReAct loop and its call cap](mandatory/theory/01_the_react_loop_in_langgraph_tool_calling_vs_react/interactive/react-loop-lab.html) (open the file in a browser)

## Learning objectives

- Build a ReAct agent in LangGraph and explain how it differs from single-shot tool calling
- Build the same agent with LangChain 1.x `create_agent`, with typed messages and structured output
- Control agents with middleware, including human-in-the-loop
- Apply ReAct to web research, software engineering and computer use

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 23.1 | The ReAct loop in LangGraph; tool calling vs ReAct ([theory](mandatory/theory/01_the_react_loop_in_langgraph_tool_calling_vs_react/README.md)) | [`01a_react_agent_langgraph.ipynb`](mandatory/notebook/01a_react_agent_langgraph.ipynb)<br>[`01b_tool_calling_vs_react.ipynb`](mandatory/notebook/01b_tool_calling_vs_react.ipynb) | — |
| 23.2 | ReAct with LangChain `create_agent` ([theory](mandatory/theory/02_react_with_langchain_create_agent/README.md)) | [`02a_react_with_create_agent.ipynb`](mandatory/notebook/02a_react_with_create_agent.ipynb) | — |
| 23.3 | Models, messages and structured output in LangChain 1.x ([theory](mandatory/theory/03_models_messages_and_structured_output_in_langchain_1_x/README.md)) | [`03c_structured_output.ipynb`](mandatory/notebook/03c_structured_output.ipynb) | [`03a_model_integration.ipynb`](optional/notebook/03a_model_integration.ipynb) *(extension)*<br>[`03b_messages.ipynb`](optional/notebook/03b_messages.ipynb) *(extension)* |
| 23.4 | Middleware, including human-in-the-loop ([theory](mandatory/theory/04_middleware_including_human_in_the_loop/README.md)) | [`04a_middleware.ipynb`](mandatory/notebook/04a_middleware.ipynb) | — |
| 23.5 | Exercise: intelligent travel assistant agent (with solution) *(optional lesson)* ([theory](optional/theory/05_exercise_intelligent_travel_assistant_agent_with_solution/README.md)) | — | [`05a_intelligent_travel_assistant_agent.ipynb`](optional/notebook/05a_intelligent_travel_assistant_agent.ipynb) *(extension)*<br>[`05b_intelligent_travel_assistant_solution.ipynb`](optional/notebook/05b_intelligent_travel_assistant_solution.ipynb) *(extension)* |

## Hands-on lab

ReAct research agent: give a `create_agent` agent your RAG retriever and a web-search tool, add a middleware that blocks off-topic questions, and compare its answers with your Part V system. Details: [lab/README.md](lab/README.md).

## Key concepts

[Reason–act–observe](mandatory/theory/01_the_react_loop_in_langgraph_tool_calling_vs_react/README.md#reasonactobserve) · [create_agent](mandatory/theory/02_react_with_langchain_create_agent/README.md#create_agent) · [Middleware](mandatory/theory/04_middleware_including_human_in_the_loop/README.md#middleware) · [Structured output](mandatory/theory/03_models_messages_and_structured_output_in_langchain_1_x/README.md#structured-output)

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
| `mandatory/notebook/01a_react_agent_langgraph.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/01_react_agent_langgraph.ipynb` |
| `mandatory/notebook/01b_tool_calling_vs_react.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/02_tool_calling_vs_react.ipynb` |
| `mandatory/notebook/02a_react_with_create_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/notebooks/03_react_with_create_agent.ipynb` |
| `optional/notebook/03a_model_integration.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/04_langchain_agents_and_middleware/notebooks/01_model_integration.ipynb` |
| `optional/notebook/03b_messages.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/04_langchain_agents_and_middleware/notebooks/02_messages.ipynb` |
| `mandatory/notebook/03c_structured_output.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/04_langchain_agents_and_middleware/notebooks/03_structured_output.ipynb` |
| `mandatory/notebook/04a_middleware.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/04_langchain_agents_and_middleware/notebooks/04_middleware.ipynb` |
| `optional/notebook/05a_intelligent_travel_assistant_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/03_react_agents/exercises/01_intelligent_travel_assistant_agent.ipynb` |
| `optional/notebook/05b_intelligent_travel_assistant_solution.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `solutions/03_react_agents/01_intelligent_travel_assistant_solution.ipynb` |
