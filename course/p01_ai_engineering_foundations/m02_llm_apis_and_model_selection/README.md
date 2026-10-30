# M02 — LLM Provider APIs & Model Selection

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part I · AI Engineering Foundations** · **Level:** Foundation · **Time:** ~3 h · **Notebooks:** 4 mandatory, 1 optional

## Why it matters

Every RAG answer ends in a model call. Knowing how to call hosted and open models directly, and when a reasoning model is worth its cost, makes every later choice about the generator concrete.

## Theory

Read the [theory page](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [Where effort stops paying](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/04_reasoning_effort_levers_and_cost/interactive/effort-knee-lab.html) (open the file in a browser)

## Learning objectives

- Call the OpenAI and Gemini chat APIs directly from Python
- Call open-source models through the Hugging Face InferenceClient and run one locally
- Measure when a reasoning model pays for itself against a fast model
- Sweep reasoning effort and find the cost/accuracy knee

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 2.1 | Calling commercial LLM APIs: OpenAI and Gemini ([theory](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/01_calling_commercial_llm_apis_openai_and_gemini/README.md)) | [`01a_using_chatgpt_or_google_gemini.ipynb`](notebooks/01a_using_chatgpt_or_google_gemini.ipynb) | — |
| 2.2 | Open-source LLMs via Hugging Face Inference and locally ([theory](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/02_open_source_llms_via_hugging_face_inference_and_locally/README.md)) | [`02a_open_source_llms_via_hugging_face_inference_api.ipynb`](notebooks/02a_open_source_llms_via_hugging_face_inference_api.ipynb) | [`02b_open_source_llms_locally.ipynb`](optional/02b_open_source_llms_locally.ipynb) *(extension)* |
| 2.3 | Reasoning vs non-reasoning models ([theory](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/03_reasoning_vs_non_reasoning_models/README.md)) | [`03a_Reasoning_vs_NonReasoning.ipynb`](notebooks/03a_Reasoning_vs_NonReasoning.ipynb) | — |
| 2.4 | Reasoning-effort levers and cost ([theory](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/04_reasoning_effort_levers_and_cost/README.md)) | [`04a_Reasoning_Effort_Levers.ipynb`](notebooks/04a_Reasoning_Effort_Levers.ipynb) | — |

## Hands-on lab

Generator choice: answer 20 questions with a fast model, a reasoning model at two effort levels and an open model, and record accuracy, latency and cost per answer. Details: [lab/README.md](lab/README.md).

## Key concepts

[Chat completions](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/01_calling_commercial_llm_apis_openai_and_gemini/README.md#chat-completions) · [Inference endpoints](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/02_open_source_llms_via_hugging_face_inference_and_locally/README.md#inference-endpoints) · [Reasoning models](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/03_reasoning_vs_non_reasoning_models/README.md#reasoning-models) · [Cost vs accuracy](../../../theory/p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/04_reasoning_effort_levers_and_cost/README.md#cost-vs-accuracy)

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
| `notebooks/01a_using_chatgpt_or_google_gemini.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/04_llm_provider_apis/notebooks/01_using_chatgpt_or_google_gemini.ipynb` |
| `notebooks/02a_open_source_llms_via_hugging_face_inference_api.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/04_llm_provider_apis/notebooks/02_open_source_llms_via_hugging_face_inference_api.ipynb` |
| `optional/02b_open_source_llms_locally.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/04_llm_provider_apis/notebooks/03_open_source_llms_locally.ipynb` |
| `notebooks/03a_Reasoning_vs_NonReasoning.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/05_model_landscape_and_selection/notebooks/01_Reasoning_vs_NonReasoning.ipynb` |
| `notebooks/04a_Reasoning_Effort_Levers.ipynb` | `ai-engineering-demystified-01-foundations` | `modules/05_model_landscape_and_selection/notebooks/02_Reasoning_Effort_Levers.ipynb` |
