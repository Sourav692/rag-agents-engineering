# Curriculum Map

Module → notebook → one-line learning objective. Work through the modules in order.

## [01_getting_started](../modules/01_getting_started/) — Getting started: models natively and through LangChain

| Notebook | Learning objective |
|---|---|
| [`01_LangChain_Introduction.ipynb`](../modules/01_getting_started/notebooks/01_LangChain_Introduction.ipynb) | What LangChain is and a first prompt-model-parser call |
| [`02_Commercial_LLMs_Natively.ipynb`](../modules/01_getting_started/notebooks/02_Commercial_LLMs_Natively.ipynb) | Call OpenAI and Gemini with their native SDKs, as the baseline LangChain abstracts |
| [`03_Commercial_LLMs_with_LangChain.ipynb`](../modules/01_getting_started/notebooks/03_Commercial_LLMs_with_LangChain.ipynb) | Call commercial chat models through LangChain's common interface |
| [`04_Open_Source_LLMs_HF_Transformers.ipynb`](../modules/01_getting_started/notebooks/04_Open_Source_LLMs_HF_Transformers.ipynb) | Run an open-source LLM locally with Hugging Face Transformers |
| [`05_Open_Source_LLMs_HF_Inference_Client.ipynb`](../modules/01_getting_started/notebooks/05_Open_Source_LLMs_HF_Inference_Client.ipynb) | Call hosted open-source models via the Hugging Face Inference Client |
| [`06_Open_Source_LLMs_Groq_Cloud.ipynb`](../modules/01_getting_started/notebooks/06_Open_Source_LLMs_Groq_Cloud.ipynb) | Call open-source models on Groq Cloud with the native SDK |
| [`07_Open_Source_LLMs_with_LangChain.ipynb`](../modules/01_getting_started/notebooks/07_Open_Source_LLMs_with_LangChain.ipynb) | Use open-source models (Groq, Hugging Face) through LangChain |
| [`08_Package_Split_and_Imports_LangChain_v1.ipynb`](../modules/01_getting_started/notebooks/08_Package_Split_and_Imports_LangChain_v1.ipynb) | Where imports moved in the LangChain 1.x package split (langchain / core / classic / partners) |

## [02_inputs_outputs_prompts](../modules/02_inputs_outputs_prompts/) — Inputs, outputs, prompt templates and output parsers

| Notebook | Learning objective |
|---|---|
| [`01_LangChain_Inputs_and_Outputs.ipynb`](../modules/02_inputs_outputs_prompts/notebooks/01_LangChain_Inputs_and_Outputs.ipynb) | What goes into and comes out of a model call: invoke, batch, messages, conversation history |
| [`02_LLM_vs_ChatModel.ipynb`](../modules/02_inputs_outputs_prompts/notebooks/02_LLM_vs_ChatModel.ipynb) | Text-completion LLMs vs chat models, and how LangChain converts inputs between them |
| [`03_Prompt_Templates.ipynb`](../modules/02_inputs_outputs_prompts/notebooks/03_Prompt_Templates.ipynb) | PromptTemplate and ChatPromptTemplate: formatting, PromptValues, chains and batching |
| [`04_Few_Shot_Composition_and_Serialization.ipynb`](../modules/02_inputs_outputs_prompts/notebooks/04_Few_Shot_Composition_and_Serialization.ipynb) | Few-shot and chain-of-thought templates, prompt composition and serialization |
| [`05_Output_Parser.ipynb`](../modules/02_inputs_outputs_prompts/notebooks/05_Output_Parser.ipynb) | Turn model text into structured Python objects with output parsers |

## [03_lcel_and_runnables](../modules/03_lcel_and_runnables/) — LCEL and Runnables

| Notebook | Learning objective |
|---|---|
| [`01_LCEL_Introduction.ipynb`](../modules/03_lcel_and_runnables/notebooks/01_LCEL_Introduction.ipynb) | Compose prompt | model | parser pipelines with LCEL |
| [`02_Runnables.ipynb`](../modules/03_lcel_and_runnables/notebooks/02_Runnables.ipynb) | The Runnable interface and its building blocks (Passthrough, Parallel, Lambda) |
| [`03_LCEL_Deepdive.ipynb`](../modules/03_lcel_and_runnables/notebooks/03_LCEL_Deepdive.ipynb) | How the pipe operator and Runnable composition work under the hood |
| [`04_LCEL_and_Runnables.ipynb`](../modules/03_lcel_and_runnables/notebooks/04_LCEL_and_Runnables.ipynb) | invoke/stream/batch (sync and async) and shaping chain input, incl. a retriever as a Runnable |
| [`05_Branching_Routing_Merging_Chains.ipynb`](../modules/03_lcel_and_runnables/notebooks/05_Branching_Routing_Merging_Chains.ipynb) | Deterministic workflow primitives with LCEL: linking, branching, merging, routing, moderating |

## [04_legacy_chains_and_migration](../modules/04_legacy_chains_and_migration/) — Legacy chains and migrating them to LCEL

| Notebook | Learning objective |
|---|---|
| [`01_Basics_of_Chains.ipynb`](../modules/04_legacy_chains_and_migration/notebooks/01_Basics_of_Chains.ipynb) | Legacy LLMChain / SimpleSequentialChain basics (langchain-classic) |
| [`02_Chains_Basics_and_OutputParsers.ipynb`](../modules/04_legacy_chains_and_migration/notebooks/02_Chains_Basics_and_OutputParsers.ipynb) | Legacy chains combined with output parsers |
| [`03_Advanced_Chains.ipynb`](../modules/04_legacy_chains_and_migration/notebooks/03_Advanced_Chains.ipynb) | Legacy multi-input, sequential and router chains |
| [`04_Chain_Migrations.ipynb`](../modules/04_legacy_chains_and_migration/notebooks/04_Chain_Migrations.ipynb) | Migrate LLMChain and RetrievalQA to their LCEL equivalents |
| [`05_Chain_Migration_Advanced.ipynb`](../modules/04_legacy_chains_and_migration/notebooks/05_Chain_Migration_Advanced.ipynb) | Migrate ConversationalRetrievalChain to hand-composed LCEL |

## [05_summarization](../modules/05_summarization/) — Summarization

| Notebook | Learning objective |
|---|---|
| [`01_Summarization_Essentials.ipynb`](../modules/05_summarization/notebooks/01_Summarization_Essentials.ipynb) | Summarize long text: stuff, map-reduce and refine with LCEL |
| [`02_Doc_Chains_to_LCEL_LangChain_v1.ipynb`](../modules/05_summarization/notebooks/02_Doc_Chains_to_LCEL_LangChain_v1.ipynb) | Rewrite load_summarize_chain document-combining chains as LCEL |

## [06_langchain_v1_course_recap](../modules/06_langchain_v1_course_recap/) — LangChain 1.x end-to-end recap course

| Notebook | Learning objective |
|---|---|
| [`00_main_connectivity_check.ipynb`](../modules/06_langchain_v1_course_recap/notebooks/00_main_connectivity_check.ipynb) | Check .env loading, package versions and OpenAI/Anthropic connectivity |
| [`01_core_concepts.ipynb`](../modules/06_langchain_v1_course_recap/notebooks/01_core_concepts.ipynb) | Recap LCEL and Runnables in LangChain 1.x |
| [`02_working_with_llms.ipynb`](../modules/06_langchain_v1_course_recap/notebooks/02_working_with_llms.ipynb) | Work with chat models from several providers in LangChain 1.x |
| [`03_prompt_messages.ipynb`](../modules/06_langchain_v1_course_recap/notebooks/03_prompt_messages.ipynb) | Message types as prompt building blocks |
| [`04_prompt_templates_all.ipynb`](../modules/06_langchain_v1_course_recap/notebooks/04_prompt_templates_all.ipynb) | All prompt template types in one tour |
| [`05_output_parsers_demo.ipynb`](../modules/06_langchain_v1_course_recap/notebooks/05_output_parsers_demo.ipynb) | Output parsers demo |
| [`06_output_parsers_final.ipynb`](../modules/06_langchain_v1_course_recap/notebooks/06_output_parsers_final.ipynb) | Output parsers vs with_structured_output |
| [`07_chains_v1.ipynb`](../modules/06_langchain_v1_course_recap/notebooks/07_chains_v1.ipynb) | Chains in LCEL: basic, parallel, passthrough, branching, debugging |
| [`08_smart_bot_section1.ipynb`](../modules/06_langchain_v1_course_recap/notebooks/08_smart_bot_section1.ipynb) | Capstone: structured-output Q&A bot with batching and error handling |

## Reference

- [LangChain 0.x vs 1.x — what actually changed](langchain-v0-vs-v1.md): migration tables used throughout modules 01, 04 and 05.
