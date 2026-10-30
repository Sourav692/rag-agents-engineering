# M07 — LangChain Core: Models, Prompts & Parsers

> Generated from `curriculum.yaml` by `scripts/build_curriculum.py`. Do not edit by hand. Notebooks are copied from the source repositories by `scripts/migrate.py`; fix them there (see `CLAUDE.md`).

**Part III · LangChain & LangGraph Fundamentals** · **Level:** Foundation · **Time:** ~4 h · **Notebooks:** 9 mandatory, 13 optional

## Why it matters

Most RAG notebooks in this course are written in LangChain. This module covers its building blocks in the 1.x package layout: chat models, messages, prompt templates and output parsers.

## Theory

Read the [theory page](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/README.md) before the notebooks: the module overview and interview questions, with a page per lesson that explains its key concepts with diagrams and trade-offs. [`index.html`](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/index.html) has the module and its lessons as one page (open it in a browser).

- Interactive lab: [The parser bench](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/06_output_parsers/interactive/parser-bench-lab.html) (open the file in a browser)

## Learning objectives

- Call commercial and open-source models natively and through LangChain
- Navigate the LangChain 1.x package split and imports
- Use messages, chat models and prompt templates, including few-shot
- Parse model output into structured data

## Lessons

Do the **Mandatory** notebooks in order. **Optional** ones are alternates, platform-specific variants or extensions.

| # | Topic | Mandatory | Optional |
|---|---|---|---|
| 7.1 | LangChain introduction and the 1.x package split ([theory](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/01_langchain_introduction_and_the_1_x_package_split/README.md)) | [`01a_LangChain_Introduction.ipynb`](notebooks/01a_LangChain_Introduction.ipynb)<br>[`01b_Package_Split_and_Imports_LangChain_v1.ipynb`](notebooks/01b_Package_Split_and_Imports_LangChain_v1.ipynb) | — |
| 7.2 | Commercial LLMs natively and with LangChain ([theory](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/02_commercial_llms_natively_and_with_langchain/README.md)) | [`02a_Commercial_LLMs_with_LangChain.ipynb`](notebooks/02a_Commercial_LLMs_with_LangChain.ipynb) | [`02b_Commercial_LLMs_Natively.ipynb`](optional/02b_Commercial_LLMs_Natively.ipynb) *(extension)* |
| 7.3 | Open-source LLMs: Transformers, Inference Client, Groq, LangChain | [`03a_Open_Source_LLMs_with_LangChain.ipynb`](notebooks/03a_Open_Source_LLMs_with_LangChain.ipynb) | [`03b_Open_Source_LLMs_HF_Transformers.ipynb`](optional/03b_Open_Source_LLMs_HF_Transformers.ipynb) *(alternate)*<br>[`03c_Open_Source_LLMs_HF_Inference_Client.ipynb`](optional/03c_Open_Source_LLMs_HF_Inference_Client.ipynb) *(alternate)*<br>[`03d_Open_Source_LLMs_Groq_Cloud.ipynb`](optional/03d_Open_Source_LLMs_Groq_Cloud.ipynb) *(alternate)* |
| 7.4 | Inputs and outputs: messages, LLM vs chat model ([theory](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/04_inputs_and_outputs_messages_llm_vs_chat_model/README.md)) | [`04a_LangChain_Inputs_and_Outputs.ipynb`](notebooks/04a_LangChain_Inputs_and_Outputs.ipynb)<br>[`04b_LLM_vs_ChatModel.ipynb`](notebooks/04b_LLM_vs_ChatModel.ipynb) | — |
| 7.5 | Prompt templates and few-shot composition ([theory](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/05_prompt_templates_and_few_shot_composition/README.md)) | [`05a_Prompt_Templates.ipynb`](notebooks/05a_Prompt_Templates.ipynb) | [`05b_Few_Shot_Composition_and_Serialization.ipynb`](optional/05b_Few_Shot_Composition_and_Serialization.ipynb) *(extension)* |
| 7.6 | Output parsers ([theory](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/06_output_parsers/README.md)) | [`06a_Output_Parser.ipynb`](notebooks/06a_Output_Parser.ipynb) | — |
| 7.7 | LangChain 1.x recap course, ending in a structured-output Q&A bot ([theory](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/07_langchain_1_x_recap_course_ending_in_a_structured_output_q_a_bot/README.md)) | [`07a_smart_bot_section1.ipynb`](notebooks/07a_smart_bot_section1.ipynb) | [`07b_core_concepts.ipynb`](optional/07b_core_concepts.ipynb) *(alternate)*<br>[`07c_working_with_llms.ipynb`](optional/07c_working_with_llms.ipynb) *(alternate)*<br>[`07d_prompt_messages.ipynb`](optional/07d_prompt_messages.ipynb) *(alternate)*<br>[`07e_prompt_templates_all.ipynb`](optional/07e_prompt_templates_all.ipynb) *(alternate)*<br>[`07f_output_parsers_demo.ipynb`](optional/07f_output_parsers_demo.ipynb) *(alternate)*<br>[`07g_output_parsers_final.ipynb`](optional/07g_output_parsers_final.ipynb) *(alternate)*<br>[`07h_chains_v1.ipynb`](optional/07h_chains_v1.ipynb) *(alternate)*<br>[`07i_main_connectivity_check.ipynb`](optional/07i_main_connectivity_check.ipynb) *(extension)* |

## Hands-on lab

Structured answers: build a prompt template and parser that turn a question plus three passages into a JSON answer with a citations list. Details: [lab/README.md](lab/README.md).

## Key concepts

[Chat models](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/02_commercial_llms_natively_and_with_langchain/README.md#chat-models) · [Messages](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/04_inputs_and_outputs_messages_llm_vs_chat_model/README.md#messages) · [Prompt templates](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/05_prompt_templates_and_few_shot_composition/README.md#prompt-templates) · [Output parsers](../../../theory/p03_langchain_and_langgraph/m07_langchain_core/06_output_parsers/README.md#output-parsers)

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
| `notebooks/01a_LangChain_Introduction.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/01_getting_started/notebooks/01_LangChain_Introduction.ipynb` |
| `notebooks/01b_Package_Split_and_Imports_LangChain_v1.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/01_getting_started/notebooks/08_Package_Split_and_Imports_LangChain_v1.ipynb` |
| `notebooks/02a_Commercial_LLMs_with_LangChain.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/01_getting_started/notebooks/03_Commercial_LLMs_with_LangChain.ipynb` |
| `optional/02b_Commercial_LLMs_Natively.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/01_getting_started/notebooks/02_Commercial_LLMs_Natively.ipynb` |
| `notebooks/03a_Open_Source_LLMs_with_LangChain.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/01_getting_started/notebooks/07_Open_Source_LLMs_with_LangChain.ipynb` |
| `optional/03b_Open_Source_LLMs_HF_Transformers.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/01_getting_started/notebooks/04_Open_Source_LLMs_HF_Transformers.ipynb` |
| `optional/03c_Open_Source_LLMs_HF_Inference_Client.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/01_getting_started/notebooks/05_Open_Source_LLMs_HF_Inference_Client.ipynb` |
| `optional/03d_Open_Source_LLMs_Groq_Cloud.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/01_getting_started/notebooks/06_Open_Source_LLMs_Groq_Cloud.ipynb` |
| `notebooks/04a_LangChain_Inputs_and_Outputs.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/02_inputs_outputs_prompts/notebooks/01_LangChain_Inputs_and_Outputs.ipynb` |
| `notebooks/04b_LLM_vs_ChatModel.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/02_inputs_outputs_prompts/notebooks/02_LLM_vs_ChatModel.ipynb` |
| `notebooks/05a_Prompt_Templates.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/02_inputs_outputs_prompts/notebooks/03_Prompt_Templates.ipynb` |
| `optional/05b_Few_Shot_Composition_and_Serialization.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/02_inputs_outputs_prompts/notebooks/04_Few_Shot_Composition_and_Serialization.ipynb` |
| `notebooks/06a_Output_Parser.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/02_inputs_outputs_prompts/notebooks/05_Output_Parser.ipynb` |
| `notebooks/07a_smart_bot_section1.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/06_langchain_v1_course_recap/notebooks/08_smart_bot_section1.ipynb` |
| `optional/07b_core_concepts.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/06_langchain_v1_course_recap/notebooks/01_core_concepts.ipynb` |
| `optional/07c_working_with_llms.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/06_langchain_v1_course_recap/notebooks/02_working_with_llms.ipynb` |
| `optional/07d_prompt_messages.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/06_langchain_v1_course_recap/notebooks/03_prompt_messages.ipynb` |
| `optional/07e_prompt_templates_all.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/06_langchain_v1_course_recap/notebooks/04_prompt_templates_all.ipynb` |
| `optional/07f_output_parsers_demo.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/06_langchain_v1_course_recap/notebooks/05_output_parsers_demo.ipynb` |
| `optional/07g_output_parsers_final.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/06_langchain_v1_course_recap/notebooks/06_output_parsers_final.ipynb` |
| `optional/07h_chains_v1.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/06_langchain_v1_course_recap/notebooks/07_chains_v1.ipynb` |
| `optional/07i_main_connectivity_check.ipynb` | `ai-engineering-demystified-03-langchain-fundamentals` | `modules/06_langchain_v1_course_recap/notebooks/00_main_connectivity_check.ipynb` |
