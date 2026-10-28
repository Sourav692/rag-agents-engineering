# M13 — The Agent Loop & Tool Calling

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part V · Agent Foundations for RAG** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 7 mandatory, 4 optional

## Why it matters

Agentic RAG is an agent loop with a retriever as one of its tools. Writing that loop by hand first makes every framework later in the course transparent.

## Learning objectives

- Implement reflection, tool use and ReAct-style planning with raw API calls and no framework
- Define tools, bind them to a model and run the tool-calling loop by hand and in LangGraph
- Handle tool errors and evaluate whether the model called the right tool with the right arguments
- Choose between client-side tools and provider-hosted tools such as code execution

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 13.1 | Agentic patterns from scratch: reflection, tool use, ReAct planning | [`01b_tool_use_pattern.ipynb`](notebooks/01b_tool_use_pattern.ipynb)<br>[`01c_planning_pattern_react.ipynb`](notebooks/01c_planning_pattern_react.ipynb) | [`01a_reflection_pattern.ipynb`](optional/01a_reflection_pattern.ipynb) *(extension)* |
| 13.2 | A real-world agent on raw API calls (Hacker News chatbot) *(optional lesson)* | — | [`02a_real_world_agent_hacker_news_chatbot.ipynb`](optional/02a_real_world_agent_hacker_news_chatbot.ipynb) *(extension)* |
| 13.3 | Defining tools and binding them to a model | [`03a_defining_tools.ipynb`](notebooks/03a_defining_tools.ipynb) | — |
| 13.4 | The manual tool loop and the augmented LLM in LangGraph | [`04a_tool_calling_manual_loop.ipynb`](notebooks/04a_tool_calling_manual_loop.ipynb)<br>[`04b_augmented_llm_with_tools_langgraph.ipynb`](notebooks/04b_augmented_llm_with_tools_langgraph.ipynb) | — |
| 13.5 | Tool errors and evaluating tool calls | [`05a_tool_loop_errors_and_evaluation.ipynb`](notebooks/05a_tool_loop_errors_and_evaluation.ipynb) | — |
| 13.6 | Hosted vs client-side tools: code execution and image generation | [`06a_hosted_vs_client_side_tools.ipynb`](notebooks/06a_hosted_vs_client_side_tools.ipynb) | [`06b_hosted_code_execution.ipynb`](optional/06b_hosted_code_execution.ipynb) *(extension)*<br>[`06c_agentic_image_generation.ipynb`](optional/06c_agentic_image_generation.ipynb) *(extension)* |

## Hands-on lab

Retriever as a tool, by hand: wrap your Part IV retriever as a tool, run it through your own tool loop with no framework, and log every tool call and error. Details: [lab/README.md](lab/README.md).

## Key concepts

Agent loop · Tool schema · Tool-call evaluation · Hosted vs client-side tools

## Folder layout

- `notebooks/` — mandatory track, plus the helper files those notebooks import
- `optional/` — alternate, platform-specific and extension notebooks
- `exercises/` — exercises and solutions, where the module has them
- `assets/` — images and data used by this module's notebooks
- `lab/` — the module lab brief

## Where each file comes from

| File | Source repo | Source path |
|---|---|---|
| `optional/01a_reflection_pattern.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/01_agents_from_scratch/notebooks/01_reflection_pattern.ipynb` |
| `notebooks/01b_tool_use_pattern.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/01_agents_from_scratch/notebooks/02_tool_use_pattern.ipynb` |
| `notebooks/01c_planning_pattern_react.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/01_agents_from_scratch/notebooks/03_planning_pattern_react.ipynb` |
| `optional/02a_real_world_agent_hacker_news_chatbot.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/01_agents_from_scratch/notebooks/04_real_world_agent_hacker_news_chatbot.ipynb` |
| `notebooks/03a_defining_tools.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/01_defining_tools.ipynb` |
| `notebooks/04a_tool_calling_manual_loop.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/02_tool_calling_manual_loop.ipynb` |
| `notebooks/04b_augmented_llm_with_tools_langgraph.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/03_augmented_llm_with_tools_langgraph.ipynb` |
| `notebooks/05a_tool_loop_errors_and_evaluation.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/04_tool_loop_errors_and_evaluation.ipynb` |
| `notebooks/06a_hosted_vs_client_side_tools.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/05_hosted_vs_client_side_tools.ipynb` |
| `optional/06b_hosted_code_execution.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/06_hosted_code_execution.ipynb` |
| `optional/06c_agentic_image_generation.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/07_agentic_image_generation.ipynb` |
