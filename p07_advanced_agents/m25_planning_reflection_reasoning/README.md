# M25 — Planning, Reflection & Reasoning Patterns

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part VII · Advanced Agents** · **Level:** Advanced · **Time:** ~6 h · **Notebooks:** 8 mandatory, 9 optional

## Why it matters

Deep research and multi-hop RAG need a plan, and grounded answers need self-checks. Reflection and chain-of-verification are the general forms of Self-RAG's groundedness checks.

## Theory

Read the [theory page](mandatory/theory/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](mandatory/theory/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Plan or react: the call budget](mandatory/theory/01_plan_and_execute_vs_react_decompose_execute_replan/interactive/plan-or-react-lab.html) (open the file in a browser)

## Learning objectives

- Compare ReAct with plan-and-execute and add replanning
- Build a deep-research planner and a reflective dynamic planning agent
- Apply Reflection, Reflexion, chain-of-verification and constitutional critique
- Use self-consistency, tree of thoughts and LATS when one reasoning path is not reliable enough

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 25.1 | Plan-and-execute vs ReAct; decompose, execute, replan ([theory](mandatory/theory/01_plan_and_execute_vs_react_decompose_execute_replan/README.md)) | [`01a_planning_react_vs_plan.ipynb`](mandatory/notebook/01a_planning_react_vs_plan.ipynb)<br>[`01b_planning_decompose_execute_replan.ipynb`](mandatory/notebook/01b_planning_decompose_execute_replan.ipynb) | — |
| 25.2 | Deep-research and reflective dynamic planners | [`02a_planning_agent_deep_research.ipynb`](mandatory/notebook/02a_planning_agent_deep_research.ipynb) | [`02b_reflective_dynamic_planning_agent.ipynb`](optional/notebook/02b_reflective_dynamic_planning_agent.ipynb) *(extension)* |
| 25.3 | Reflection and Reflexion agents | [`03a_reflection_agents.ipynb`](mandatory/notebook/03a_reflection_agents.ipynb)<br>[`03b_reflexion_agents.ipynb`](mandatory/notebook/03b_reflexion_agents.ipynb) | [`03c_reflection_architecture.ipynb`](optional/notebook/03c_reflection_architecture.ipynb) *(alternate)* |
| 25.4 | Chain-of-verification and constitutional critique ([theory](mandatory/theory/04_chain_of_verification_and_constitutional_critique/README.md)) | [`04a_chain_of_verification.ipynb`](mandatory/notebook/04a_chain_of_verification.ipynb) | [`04b_constitutional_ai_critique_loop.ipynb`](optional/notebook/04b_constitutional_ai_critique_loop.ipynb) *(extension)* |
| 25.5 | Self-Discover and reflective code generation *(optional lesson)* | — | [`05a_self_discover.ipynb`](optional/notebook/05a_self_discover.ipynb) *(extension)*<br>[`05b_reflective_code_generation_agent.ipynb`](optional/notebook/05b_reflective_code_generation_agent.ipynb) *(extension)* |
| 25.6 | Self-consistency, tree of thoughts and LATS ([theory](mandatory/theory/06_self_consistency_tree_of_thoughts_and_lats/README.md)) | [`06a_self_consistency.ipynb`](mandatory/notebook/06a_self_consistency.ipynb)<br>[`06b_tree_of_thoughts.ipynb`](mandatory/notebook/06b_tree_of_thoughts.ipynb) | [`06c_lats.ipynb`](optional/notebook/06c_lats.ipynb) *(extension)* |
| 25.7 | Simulator-in-the-loop, metacognition and exemplar memory *(optional lesson)* | — | [`07a_mental_loop_simulator.ipynb`](optional/notebook/07a_mental_loop_simulator.ipynb) *(extension)*<br>[`07b_reflexive_metacognitive.ipynb`](optional/notebook/07b_reflexive_metacognitive.ipynb) *(extension)*<br>[`07c_self_improving_exemplar_memory.ipynb`](optional/notebook/07c_self_improving_exemplar_memory.ipynb) *(extension)* |

## Hands-on lab

Verified answers: add chain-of-verification to your RAG answer step and measure how many unsupported claims it removes on the golden set. Details: [lab/README.md](lab/README.md).

## Key concepts

[Plan-and-execute](mandatory/theory/01_plan_and_execute_vs_react_decompose_execute_replan/README.md#plan-and-execute) · [Replanning](mandatory/theory/01_plan_and_execute_vs_react_decompose_execute_replan/README.md#replanning) · [Chain-of-verification](mandatory/theory/04_chain_of_verification_and_constitutional_critique/README.md#chain-of-verification) · [Tree of thoughts / LATS](mandatory/theory/06_self_consistency_tree_of_thoughts_and_lats/README.md#tree-of-thoughts--lats)

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
| `mandatory/notebook/01a_planning_react_vs_plan.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/10_planning/notebooks/01_planning_react_vs_plan.ipynb` |
| `mandatory/notebook/01b_planning_decompose_execute_replan.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/10_planning/notebooks/02_planning_decompose_execute_replan.ipynb` |
| `mandatory/notebook/02a_planning_agent_deep_research.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/10_planning/notebooks/03_planning_agent_deep_research.ipynb` |
| `optional/notebook/02b_reflective_dynamic_planning_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/10_planning/notebooks/04_reflective_dynamic_planning_agent.ipynb` |
| `mandatory/notebook/03a_reflection_agents.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/11_reflection/notebooks/01_reflection_agents.ipynb` |
| `mandatory/notebook/03b_reflexion_agents.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/11_reflection/notebooks/02_reflexion_agents.ipynb` |
| `optional/notebook/03c_reflection_architecture.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/11_reflection/notebooks/03_reflection_architecture.ipynb` |
| `mandatory/notebook/04a_chain_of_verification.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/11_reflection/notebooks/04_chain_of_verification.ipynb` |
| `optional/notebook/04b_constitutional_ai_critique_loop.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/11_reflection/notebooks/06_constitutional_ai_critique_loop.ipynb` |
| `optional/notebook/05a_self_discover.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/11_reflection/notebooks/05_self_discover.ipynb` |
| `optional/notebook/05b_reflective_code_generation_agent.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/11_reflection/notebooks/07_reflective_code_generation_agent.ipynb` |
| `mandatory/notebook/06a_self_consistency.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/12_advanced_cognitive_patterns/notebooks/01_self_consistency.ipynb` |
| `mandatory/notebook/06b_tree_of_thoughts.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/12_advanced_cognitive_patterns/notebooks/02_tree_of_thoughts.ipynb` |
| `optional/notebook/06c_lats.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/12_advanced_cognitive_patterns/notebooks/03_lats.ipynb` |
| `optional/notebook/07a_mental_loop_simulator.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/12_advanced_cognitive_patterns/notebooks/04_mental_loop_simulator.ipynb` |
| `optional/notebook/07b_reflexive_metacognitive.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/12_advanced_cognitive_patterns/notebooks/05_reflexive_metacognitive.ipynb` |
| `optional/notebook/07c_self_improving_exemplar_memory.ipynb` | `ai-engineering-demystified-06-agent-fundamentals` | `modules/12_advanced_cognitive_patterns/notebooks/06_self_improving_exemplar_memory.ipynb` |
