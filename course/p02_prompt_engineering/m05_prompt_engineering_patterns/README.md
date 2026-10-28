# M05 — Prompt Engineering Patterns

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part II · Prompt & Context Engineering** · **Level:** Foundation · **Time:** ~3 h · **Notebooks:** 4 mandatory, 3 optional

## Why it matters

Query rewriting, grading, routing and answer generation are all prompts. The patterns here are the building blocks of every LLM step in a RAG pipeline.

## Learning objectives

- Apply persona, flipped-interaction, N-shot, directional-stimulus, template and meta-language patterns
- Use chain-of-thought, self-consistency, least-to-most and ReAct-format prompting
- Run the same tasks across GPT-4o-mini, Gemini and Llama models and compare the results
- Combine the patterns on real business tasks

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 5.1 | Core prompt patterns | [`01a_prompt_engineering_patterns.ipynb`](notebooks/01a_prompt_engineering_patterns.ipynb) | — |
| 5.2 | Reasoning prompts: chain-of-thought, self-consistency, least-to-most, ReAct | [`02a_advanced_prompt_engineering_patterns.ipynb`](notebooks/02a_advanced_prompt_engineering_patterns.ipynb) | — |
| 5.3 | The same tasks across models | [`03a_openai_gpt_4o_mini.ipynb`](notebooks/03a_openai_gpt_4o_mini.ipynb) | [`03b_google_gemini_1_5_flash.ipynb`](optional/03b_google_gemini_1_5_flash.ipynb) *(alternate)*<br>[`03c_meta_llama_3_2_90b_groq.ipynb`](optional/03c_meta_llama_3_2_90b_groq.ipynb) *(alternate)*<br>[`03d_meta_llama_3_2_1b_huggingface.ipynb`](optional/03d_meta_llama_3_2_1b_huggingface.ipynb) *(alternate)* |
| 5.4 | Applied prompting on business tasks | [`04a_gpt_4o_and_llama_3_2_real_world_tasks.ipynb`](notebooks/04a_gpt_4o_and_llama_3_2_real_world_tasks.ipynb) | — |

## Hands-on lab

Prompt bake-off: write three prompts for grading whether a retrieved passage answers a question, and measure their agreement with your own labels on 30 pairs. Details: [lab/README.md](lab/README.md).

## Key concepts

Few-shot · Chain-of-thought · Self-consistency · ReAct format

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
| `notebooks/01a_prompt_engineering_patterns.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/01_prompting_basics/notebooks/01_prompt_engineering_patterns.ipynb` |
| `notebooks/02a_advanced_prompt_engineering_patterns.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/02_advanced_prompt_patterns/notebooks/01_advanced_prompt_engineering_patterns.ipynb` |
| `notebooks/03a_openai_gpt_4o_mini.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/03_model_specific_practice/notebooks/01_openai_gpt_4o_mini.ipynb` |
| `optional/03b_google_gemini_1_5_flash.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/03_model_specific_practice/notebooks/02_google_gemini_1_5_flash.ipynb` |
| `optional/03c_meta_llama_3_2_90b_groq.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/03_model_specific_practice/notebooks/03_meta_llama_3_2_90b_groq.ipynb` |
| `optional/03d_meta_llama_3_2_1b_huggingface.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/03_model_specific_practice/notebooks/04_meta_llama_3_2_1b_huggingface.ipynb` |
| `notebooks/04a_gpt_4o_and_llama_3_2_real_world_tasks.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/06_applied_prompting/notebooks/01_gpt_4o_and_llama_3_2_real_world_tasks.ipynb` |
