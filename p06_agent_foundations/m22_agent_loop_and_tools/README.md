# M22 — The Agent Loop & Tool Calling

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part VI · Agent Foundations** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 7 mandatory, 4 optional

## Why it matters

Agentic RAG is an agent loop with a retriever as one of its tools. Writing that loop by hand first makes every framework later in the course transparent.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Where a tool error goes](mandatory/theory/05_tool_errors_and_evaluating_tool_calls/interactive/tool-error-routing-lab.html) (open the file in a browser)

## Learning objectives

- Implement tool use and ReAct-style planning with raw API calls and no framework
- Define tools, bind them to a model and run the tool-calling loop by hand and in LangGraph
- Handle tool errors and evaluate whether the model called the right tool with the right arguments
- Choose between client-side tools and provider-hosted tools such as code execution

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 22.1 | Agentic patterns from scratch: reflection, tool use, ReAct planning ([theory](mandatory/theory/01_agentic_patterns_from_scratch_reflection_tool_use_react_planning/README.md)) | [`01b_tool_use_pattern.ipynb`](mandatory/notebook/01b_tool_use_pattern.ipynb)<br>[`01c_planning_pattern_react.ipynb`](mandatory/notebook/01c_planning_pattern_react.ipynb) | [`01a_reflection_pattern.ipynb`](optional/notebook/01a_reflection_pattern.ipynb) *(extension)* |
| 22.2 | A real-world agent on raw API calls (Hacker News chatbot) *(optional lesson)* | — | [`02a_real_world_agent_hacker_news_chatbot.ipynb`](optional/notebook/02a_real_world_agent_hacker_news_chatbot.ipynb) *(extension)* |
| 22.3 | Defining tools and binding them to a model ([theory](mandatory/theory/03_defining_tools_and_binding_them_to_a_model/README.md)) | [`03a_defining_tools.ipynb`](mandatory/notebook/03a_defining_tools.ipynb) | — |
| 22.4 | The manual tool loop and the augmented LLM in LangGraph ([theory](mandatory/theory/04_the_manual_tool_loop_and_the_augmented_llm_in_langgraph/README.md)) | [`04a_tool_calling_manual_loop.ipynb`](mandatory/notebook/04a_tool_calling_manual_loop.ipynb)<br>[`04b_augmented_llm_with_tools_langgraph.ipynb`](mandatory/notebook/04b_augmented_llm_with_tools_langgraph.ipynb) | — |
| 22.5 | Tool errors and evaluating tool calls ([theory](mandatory/theory/05_tool_errors_and_evaluating_tool_calls/README.md)) | [`05a_tool_loop_errors_and_evaluation.ipynb`](mandatory/notebook/05a_tool_loop_errors_and_evaluation.ipynb) | — |
| 22.6 | Hosted vs client-side tools: code execution and image generation ([theory](mandatory/theory/06_hosted_vs_client_side_tools_code_execution_and_image_generation/README.md)) | [`06a_hosted_vs_client_side_tools.ipynb`](mandatory/notebook/06a_hosted_vs_client_side_tools.ipynb) | [`06b_hosted_code_execution.ipynb`](optional/notebook/06b_hosted_code_execution.ipynb) *(extension)*<br>[`06c_agentic_image_generation.ipynb`](optional/notebook/06c_agentic_image_generation.ipynb) *(extension)* |

## Hands-on lab

Retriever as a tool, by hand: wrap your Part V retriever as a tool, run it through your own tool loop with no framework, and log every tool call and error. Details: [lab/README.md](lab/README.md).

## Key concepts

[Agent loop](mandatory/theory/01_agentic_patterns_from_scratch_reflection_tool_use_react_planning/README.md#agent-loop) · [Tool schema](mandatory/theory/03_defining_tools_and_binding_them_to_a_model/README.md#tool-schema) · [Tool-call evaluation](mandatory/theory/05_tool_errors_and_evaluating_tool_calls/README.md#tool-call-evaluation) · [Hosted vs client-side tools](mandatory/theory/06_hosted_vs_client_side_tools_code_execution_and_image_generation/README.md#hosted-vs-client-side-tools)

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
| `optional/notebook/01a_reflection_pattern.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/01_agents_from_scratch/notebooks/01_reflection_pattern.ipynb` |
| `mandatory/notebook/01b_tool_use_pattern.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/01_agents_from_scratch/notebooks/02_tool_use_pattern.ipynb` |
| `mandatory/notebook/01c_planning_pattern_react.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/01_agents_from_scratch/notebooks/03_planning_pattern_react.ipynb` |
| `optional/notebook/02a_real_world_agent_hacker_news_chatbot.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/01_agents_from_scratch/notebooks/04_real_world_agent_hacker_news_chatbot.ipynb` |
| `mandatory/notebook/03a_defining_tools.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/01_defining_tools.ipynb` |
| `mandatory/notebook/04a_tool_calling_manual_loop.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/02_tool_calling_manual_loop.ipynb` |
| `mandatory/notebook/04b_augmented_llm_with_tools_langgraph.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/03_augmented_llm_with_tools_langgraph.ipynb` |
| `mandatory/notebook/05a_tool_loop_errors_and_evaluation.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/04_tool_loop_errors_and_evaluation.ipynb` |
| `mandatory/notebook/06a_hosted_vs_client_side_tools.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/05_hosted_vs_client_side_tools.ipynb` |
| `optional/notebook/06b_hosted_code_execution.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/06_hosted_code_execution.ipynb` |
| `optional/notebook/06c_agentic_image_generation.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/02_tools_and_function_calling/notebooks/07_agentic_image_generation.ipynb` |
