# M03 — Hugging Face Models & Gradio Demos

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are maintained in this repository (see `CLAUDE.md`).

**Part I · AI Engineering Foundations** · **Level:** Foundation · **Time:** ~4 h · **Notebooks:** 5 mandatory, 16 optional

## Why it matters

Open models from the Hub power local embeddings, rerankers and captioning later in the course. This module covers loading them, running pipelines, and putting a quick Gradio front end on a model.

## Theory

Read the [theory page](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Tokens and the limit](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/02_pipelines_tokenization_and_pretrained_models/interactive/token-limit-lab.html) (open the file in a browser)

## Learning objectives

- Log in to the Hub and load datasets and models
- Run NLP pipelines and tokenize/generate with causal LMs
- Work with image, diffusion, video and audio models
- Build and style Gradio demos around a model

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 3.1 | Hub setup, datasets and models ([theory](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/01_hub_setup_datasets_and_models/README.md)) | [`01a_hf_setup.ipynb`](notebooks/01a_hf_setup.ipynb)<br>[`01b_hf_basics.ipynb`](notebooks/01b_hf_basics.ipynb) | — |
| 3.2 | Pipelines, tokenization and pretrained models ([theory](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/02_pipelines_tokenization_and_pretrained_models/README.md)) | [`02a_pipelines_for_nlp_tasks.ipynb`](notebooks/02a_pipelines_for_nlp_tasks.ipynb)<br>[`02b_understanding_llms.ipynb`](notebooks/02b_understanding_llms.ipynb) | [`02c_accessing_pretrained_models.ipynb`](optional/02c_accessing_pretrained_models.ipynb) *(extension)* |
| 3.3 | Images, diffusion and video generation *(optional lesson)* | — | [`03a_understanding_image_data.ipynb`](optional/03a_understanding_image_data.ipynb) *(extension)*<br>[`03b_understanding_diffusion_models.ipynb`](optional/03b_understanding_diffusion_models.ipynb) *(extension)*<br>[`03c_autopipelines_diffusers.ipynb`](optional/03c_autopipelines_diffusers.ipynb) *(extension)*<br>[`03d_stable_video_diffusion.ipynb`](optional/03d_stable_video_diffusion.ipynb) *(platform-specific)*<br>[`03e_image2videogen_xl.ipynb`](optional/03e_image2videogen_xl.ipynb) *(platform-specific)* |
| 3.4 | Audio: data, classification, transcription, generation *(optional lesson)* | — | [`04a_audio_data.ipynb`](optional/04a_audio_data.ipynb) *(extension)*<br>[`04b_audio_classification.ipynb`](optional/04b_audio_classification.ipynb) *(extension)*<br>[`04c_audio_transcription.ipynb`](optional/04c_audio_transcription.ipynb) *(extension)*<br>[`04d_audio_generation.ipynb`](optional/04d_audio_generation.ipynb) *(extension)* |
| 3.5 | Building demos with Gradio ([theory](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/05_building_demos_with_gradio/README.md)) | [`05a_gradio_introduction.ipynb`](notebooks/05a_gradio_introduction.ipynb) | [`05b_gradio_layout.ipynb`](optional/05b_gradio_layout.ipynb) *(extension)*<br>[`05c_gradio_interactions.ipynb`](optional/05c_gradio_interactions.ipynb) *(extension)*<br>[`05d_gradio_image_ml_integration.ipynb`](optional/05d_gradio_image_ml_integration.ipynb) *(extension)*<br>[`05e_gradio_text_ml_integration.ipynb`](optional/05e_gradio_text_ml_integration.ipynb) *(extension)*<br>[`05f_gradio_modals_errors.ipynb`](optional/05f_gradio_modals_errors.ipynb) *(extension)*<br>[`05g_gradio_styling_and_themes.ipynb`](optional/05g_gradio_styling_and_themes.ipynb) *(extension)* |

## Hands-on lab

Model demo: wrap an open embedding or text model from the Hub in a Gradio app that shows its output for a user-entered query. Details: [lab/README.md](lab/README.md).

## Key concepts

[Hub & cache](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/01_hub_setup_datasets_and_models/README.md#hub--cache) · [Pipelines](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/02_pipelines_tokenization_and_pretrained_models/README.md#pipelines) · [Tokenization](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/02_pipelines_tokenization_and_pretrained_models/README.md#tokenization) · [Gradio Blocks](../../../theory/p01_ai_engineering_foundations/m03_hugging_face_models/05_building_demos_with_gradio/README.md#gradio-blocks)

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
| `notebooks/01a_hf_setup.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/01_hf_setup.ipynb` |
| `notebooks/01b_hf_basics.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/02_hf_basics.ipynb` |
| `notebooks/02a_pipelines_for_nlp_tasks.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/03_pipelines_for_nlp_tasks.ipynb` |
| `notebooks/02b_understanding_llms.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/04_understanding_llms.ipynb` |
| `optional/02c_accessing_pretrained_models.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/21_accessing_pretrained_models.ipynb` |
| `optional/03a_understanding_image_data.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/05_understanding_image_data.ipynb` |
| `optional/03b_understanding_diffusion_models.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/06_understanding_diffusion_models.ipynb` |
| `optional/03c_autopipelines_diffusers.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/07_autopipelines_diffusers.ipynb` |
| `optional/03d_stable_video_diffusion.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/08_stable_video_diffusion.ipynb` |
| `optional/03e_image2videogen_xl.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/09_image2videogen_xl.ipynb` |
| `optional/04a_audio_data.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/10_audio_data.ipynb` |
| `optional/04b_audio_classification.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/11_audio_classification.ipynb` |
| `optional/04c_audio_transcription.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/12_audio_transcription.ipynb` |
| `optional/04d_audio_generation.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/13_audio_generation.ipynb` |
| `notebooks/05a_gradio_introduction.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/14_gradio_introduction.ipynb` |
| `optional/05b_gradio_layout.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/15_gradio_layout.ipynb` |
| `optional/05c_gradio_interactions.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/16_gradio_interactions.ipynb` |
| `optional/05d_gradio_image_ml_integration.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/17_gradio_image_ml_integration.ipynb` |
| `optional/05e_gradio_text_ml_integration.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/18_gradio_text_ml_integration.ipynb` |
| `optional/05f_gradio_modals_errors.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/19_gradio_modals_errors.ipynb` |
| `optional/05g_gradio_styling_and_themes.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/07_hugging_face_models/notebooks/20_gradio_styling_and_themes.ipynb` |
