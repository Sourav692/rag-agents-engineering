# M04 — Fine-Tuning Fundamentals

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part I · AI Engineering Foundations** · **Level:** Core · **Time:** ~5 h · **Notebooks:** 5 mandatory, 8 optional

## Why it matters

Fine-tuning is the main alternative to retrieval for adding knowledge or behaviour. Knowing what it can and cannot do is how you decide between RAG, fine-tuning, or both.

## Theory

Read the [theory page](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Truncation and padding](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/04_data_preparation/interactive/truncation-padding-lab.html) (open the file in a browser)

## Learning objectives

- Explain when fine-tuning beats prompting or RAG, and where it fits after pre-training
- Build instruction-tuning data and prepare it (tokenize, pad, truncate, split)
- Train a small model with the Hugging Face Trainer and evaluate it
- Fine-tune Llama 2 with AutoTrain

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 4.1 | Why fine-tune ([theory](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/01_why_fine_tune/README.md)) | [`01a_why_finetuning_lab.ipynb`](notebooks/01_why_finetune/01a_why_finetuning_lab.ipynb) | [`01b_why_finetuning_lecture.ipynb`](optional/01_why_finetune/01b_why_finetuning_lecture.ipynb) *(alternate)* |
| 4.2 | Where fine-tuning fits *(optional lesson)* ([theory](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/02_where_fine_tuning_fits/README.md)) | — | [`02a_where_finetuning_fits_in_lab.ipynb`](optional/02_where_finetuning_fits/02a_where_finetuning_fits_in_lab.ipynb) *(extension)*<br>[`02b_where_finetuning_fits_in_lecture.ipynb`](optional/02_where_finetuning_fits/02b_where_finetuning_fits_in_lecture.ipynb) *(alternate)* |
| 4.3 | Instruction tuning ([theory](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/03_instruction_tuning/README.md)) | [`03a_instruction_tuning_lab.ipynb`](notebooks/03_instruction_tuning/03a_instruction_tuning_lab.ipynb) | [`03b_instruction_tuning_lecture.ipynb`](optional/03_instruction_tuning/03b_instruction_tuning_lecture.ipynb) *(alternate)* |
| 4.4 | Data preparation ([theory](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/04_data_preparation/README.md)) | [`04a_data_preparation_lab.ipynb`](notebooks/04_data_preparation/04a_data_preparation_lab.ipynb) | [`04b_data_preparation_lecture.ipynb`](optional/04_data_preparation/04b_data_preparation_lecture.ipynb) *(alternate)* |
| 4.5 | Training ([theory](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/05_training/README.md)) | [`05a_training_lab.ipynb`](notebooks/05_training/05a_training_lab.ipynb) | [`05b_training_lecture.ipynb`](optional/05_training/05b_training_lecture.ipynb) *(alternate)* |
| 4.6 | Evaluation ([theory](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/06_evaluation/README.md)) | [`06a_evaluation_lab.ipynb`](notebooks/06_evaluation/06a_evaluation_lab.ipynb) | [`06b_evaluation_lecture.ipynb`](optional/06_evaluation/06b_evaluation_lecture.ipynb) *(alternate)* |
| 4.7 | Fine-tuning Llama 2 with AutoTrain *(optional lesson)* ([theory](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/07_fine_tuning_llama_2_with_autotrain/README.md)) | — | [`07a_3_ways_fine_tuning_llama_2_with_autotrain.ipynb`](optional/07_llama2_autotrain/07a_3_ways_fine_tuning_llama_2_with_autotrain.ipynb) *(platform-specific)* |

## Hands-on lab

RAG or fine-tune: for one narrow task, compare the M11 RAG baseline with a small fine-tuned model on the same questions and write down which wins and why. Details: [lab/README.md](lab/README.md).

## Key concepts

[Instruction tuning](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/03_instruction_tuning/README.md#instruction-tuning) · [Data preparation](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/04_data_preparation/README.md#data-preparation) · [Trainer](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/05_training/README.md#trainer) · [Evaluation](../../../theory/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/06_evaluation/README.md#evaluation)

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
| `notebooks/01_why_finetune/01a_why_finetuning_lab.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/01_why_finetune/01_why_finetuning_lab.ipynb` |
| `optional/01_why_finetune/01b_why_finetuning_lecture.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/01_why_finetune/01_why_finetuning_lecture.ipynb` |
| `optional/02_where_finetuning_fits/02a_where_finetuning_fits_in_lab.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/02_where_finetuning_fits/02_where_finetuning_fits_in_lab.ipynb` |
| `optional/02_where_finetuning_fits/02b_where_finetuning_fits_in_lecture.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/02_where_finetuning_fits/02_where_finetuning_fits_in_lecture.ipynb` |
| `notebooks/03_instruction_tuning/03a_instruction_tuning_lab.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/03_instruction_tuning/03_instruction_tuning_lab.ipynb` |
| `optional/03_instruction_tuning/03b_instruction_tuning_lecture.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/03_instruction_tuning/03_instruction_tuning_lecture.ipynb` |
| `notebooks/04_data_preparation/04a_data_preparation_lab.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/04_data_preparation/04_data_preparation_lab.ipynb` |
| `optional/04_data_preparation/04b_data_preparation_lecture.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/04_data_preparation/04_data_preparation_lecture.ipynb` |
| `notebooks/05_training/05a_training_lab.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/05_training/05_training_lab.ipynb` |
| `optional/05_training/05b_training_lecture.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/05_training/05_training_lecture.ipynb` |
| `notebooks/06_evaluation/06a_evaluation_lab.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/06_evaluation/06_evaluation_lab.ipynb` |
| `optional/06_evaluation/06b_evaluation_lecture.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/06_evaluation/06_evaluation_lecture.ipynb` |
| `optional/07_llama2_autotrain/07a_3_ways_fine_tuning_llama_2_with_autotrain.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/08_fine_tuning_fundamentals/notebooks/07_llama2_autotrain/07_3_ways_fine_tuning_llama_2_with_autotrain.ipynb` |
