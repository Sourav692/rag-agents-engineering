# M06 — Multimodal Prompting

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part II · Prompt & Context Engineering** · **Level:** Foundation · **Time:** ~2 h · **Notebooks:** 1 mandatory, 2 optional

## Why it matters

Multimodal RAG (M21) ends with a model reading images, PDFs or video frames. This module shows how to prompt those models directly first.

## Learning objectives

- Prompt Gemini with images, PDFs, audio and video
- Prompt GPT-4o with images and summarise a video from frames and transcript

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 6.1 | Multimodal prompting with Gemini | [`01a_multimodal_google_gemini.ipynb`](notebooks/01a_multimodal_google_gemini.ipynb) | — |
| 6.2 | Multimodal prompting with GPT-4o *(optional lesson)* | — | [`02a_multimodal_openai_gpt_4o.ipynb`](optional/02a_multimodal_openai_gpt_4o.ipynb) *(alternate)* |
| 6.3 | Exercise: financial report analysis *(optional lesson)* | — | [`03a_financial_report_analysis.ipynb`](exercises/03a_financial_report_analysis.ipynb) *(extension)* |

## Hands-on lab

Report reader: answer five questions about a chart-heavy PDF page by prompting a multimodal model with the page image. Details: [lab/README.md](lab/README.md).

## Key concepts

Image prompts · PDF and audio input · Frame sampling

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
| `notebooks/01a_multimodal_google_gemini.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/04_multimodal_prompting/notebooks/01_multimodal_google_gemini.ipynb` |
| `optional/02a_multimodal_openai_gpt_4o.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/04_multimodal_prompting/notebooks/02_multimodal_openai_gpt_4o.ipynb` |
| `exercises/03a_financial_report_analysis.ipynb` | `ai-engineering-demystified-02-prompt-context-engineering` | `modules/04_multimodal_prompting/exercises/01_financial_report_analysis.ipynb` |
