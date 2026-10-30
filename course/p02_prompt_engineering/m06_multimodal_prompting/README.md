# M06 — Multimodal Prompting

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part II · Prompt & Context Engineering** · **Level:** Foundation · **Time:** ~2 h · **Notebooks:** 1 mandatory, 2 optional

## Why it matters

Multimodal RAG (M21) ends with a model reading images, PDFs or video frames. This module shows how to prompt those models directly first.

## Theory

Read the [theory page](../../../theory/p02_prompt_engineering/m06_multimodal_prompting/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p02_prompt_engineering/m06_multimodal_prompting/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Frame sampling](../../../theory/p02_prompt_engineering/m06_multimodal_prompting/02_multimodal_prompting_with_gpt_4o/interactive/frame-sampling-lab.html) (open the file in a browser)

## Learning objectives

- Prompt Gemini with images, PDFs, audio and video
- Prompt GPT-4o with images and summarise a video from frames and transcript

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 6.1 | Multimodal prompting with Gemini ([theory](../../../theory/p02_prompt_engineering/m06_multimodal_prompting/01_multimodal_prompting_with_gemini/README.md)) | [`01a_multimodal_google_gemini.ipynb`](notebooks/01a_multimodal_google_gemini.ipynb) | — |
| 6.2 | Multimodal prompting with GPT-4o *(optional lesson)* ([theory](../../../theory/p02_prompt_engineering/m06_multimodal_prompting/02_multimodal_prompting_with_gpt_4o/README.md)) | — | [`02a_multimodal_openai_gpt_4o.ipynb`](optional/02a_multimodal_openai_gpt_4o.ipynb) *(alternate)* |
| 6.3 | Exercise: financial report analysis *(optional lesson)* ([theory](../../../theory/p02_prompt_engineering/m06_multimodal_prompting/03_exercise_financial_report_analysis/README.md)) | — | [`03a_financial_report_analysis.ipynb`](exercises/03a_financial_report_analysis.ipynb) *(extension)* |

## Hands-on lab

Report reader: answer five questions about a chart-heavy PDF page by prompting a multimodal model with the page image. Details: [lab/README.md](lab/README.md).

## Key concepts

[Image prompts](../../../theory/p02_prompt_engineering/m06_multimodal_prompting/01_multimodal_prompting_with_gemini/README.md#image-prompts) · [PDF and audio input](../../../theory/p02_prompt_engineering/m06_multimodal_prompting/01_multimodal_prompting_with_gemini/README.md#pdf-and-audio-input) · [Frame sampling](../../../theory/p02_prompt_engineering/m06_multimodal_prompting/02_multimodal_prompting_with_gpt_4o/README.md#frame-sampling)

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
