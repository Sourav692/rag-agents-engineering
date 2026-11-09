# M06.3 Theory: Open-source LLMs: Transformers, Inference Client, Groq, LangChain

*[M06 theory](../README.md) · Lesson 6.3 · Notebooks: [`03a_Open_Source_LLMs_with_LangChain.ipynb`](../../notebook/03a_Open_Source_LLMs_with_LangChain.ipynb), [`03b_Open_Source_LLMs_HF_Transformers.ipynb`](../../../optional/notebook/03b_Open_Source_LLMs_HF_Transformers.ipynb) (optional), [`03c_Open_Source_LLMs_HF_Inference_Client.ipynb`](../../../optional/notebook/03c_Open_Source_LLMs_HF_Inference_Client.ipynb) (optional), [`03d_Open_Source_LLMs_Groq_Cloud.ipynb`](../../../optional/notebook/03d_Open_Source_LLMs_Groq_Cloud.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: A small project: lesson 6.2's chain on three open-model backends, one on your own machine and two hosted, and what each one changes underneath -->

## The project: three open backends

> **What you'll build**
>
> - **A local backend** that downloads a 1.1B-parameter model and runs it in your own process.
> - **A hosted Hugging Face backend** that sends the same messages to a large model on Inference Providers.
> - **A Groq backend** that uses Groq's native LangChain chat model.
> - **One chain** that runs unchanged on all three.

Lesson 6.2 ran one `prompt | model` chain on commercial APIs. This project runs the same chain on open-weight models. It adds no new idea; it shows what the chat-model interface hides when the model moves to weights on your laptop, or to someone else's hardware.

For Larkspur this is the question behind a cost or data-residency review: whether the refund assistant can run on an open model without rewriting the chain. The call shape survives each move. What changes is where the tokens are computed, what the reply reports about itself, and which messages the backend accepts.

## Architecture

The two Hugging Face backends share one wrapper, and Groq needs none:

```mermaid
flowchart TB
    T["Prompt template<br/>Explain topic in 2 bullets"] --> W["ChatHuggingFace<br/>wrapper"]
    T --> G["ChatGroq<br/>native chat model"]
    W --> L["HuggingFacePipeline<br/>local weights"]
    W --> E["HuggingFaceEndpoint<br/>hosted model"]
    G --> GA["Groq API"]
```

*Figure 1: The three backends. `ChatHuggingFace` gives two completion-style classes the chat interface; `ChatGroq` is already a chat model.*

| Piece | What it does | Built on |
|---|---|---|
| **Prompt template** | One human message with a `{topic}` slot | Lesson 6.5's templates |
| **`ChatHuggingFace`** | Turns messages into what a Hugging Face LLM class takes, and its output into an `AIMessage` | Lesson 6.4's LLM vs chat model split |
| **`HuggingFacePipeline`** | Loads `TinyLlama/TinyLlama-1.1B-Chat-v1.0` with `transformers` and generates on CPU, GPU or Apple silicon | The optional Transformers notebook |
| **`HuggingFaceEndpoint`** | Calls `moonshotai/kimi-k2-instruct-0905` on Hugging Face's servers | The optional Inference Client notebook |
| **`ChatGroq`** | Calls `llama-3.1-8b-instant` on Groq's hosted inference | The optional Groq notebook |

*Table 1: The project's pieces. Each optional notebook does the same job with the backend's own library, without LangChain.*

## Following one request

Invoke the chain with the topic *AI*. The template produces one `HumanMessage`, and each backend takes it from there. We traced the paths in the installed `langchain-huggingface` 1.2.3 source; no model was called:

| Step | Local pipeline | Hosted endpoint | Groq |
|---|---|---|---|
| Messages become | one string, rendered with the model's own chat template | a list of role dicts | a list of role dicts |
| Generation | in your process, greedy, up to 256 new tokens | on Hugging Face's servers, up to 1,000 new tokens | on Groq's servers, temperature 0, up to 1,000 tokens |
| Reply becomes | an `AIMessage` with the text only | an `AIMessage` with token counts from the response | an `AIMessage` with token counts |

*Table 2: One request through each backend. The settings are the notebook's.*

The first row is the one to understand. A chat model trained on roles still reads one sequence of tokens; the roles are marked with special tokens that differ by model family. The optional Transformers notebook shows TinyLlama's format, a `<|user|>` line, the question, an end-of-turn token and an open `<|assistant|>` line for the model to continue. On the local path, `ChatHuggingFace` asks the tokenizer to render the messages in that format. On the hosted paths, the server does the rendering.

The optional notebooks do the same without LangChain. The Transformers notebook renders the chat template, encodes, generates and decodes by hand, then repeats it with a one-call `pipeline`. The Inference Client notebook calls `chat_completion` on a hosted model and reads token usage from the response. The Groq notebook calls Groq's own SDK and compares two Llama 4 variants on one prompt.

## Design choices worth copying

| Choice | Why |
|---|---|
| **Keep the chain, swap the model object** | The template and everything after the model stay the same: a backend comparison changes one line ([lesson 6.2](../02_commercial_llms_natively_and_with_langchain/README.md#chat-models)) |
| **Greedy decoding for the local model** | Sampling off makes reruns repeatable, which a comparison needs |
| **A short output cap on CPU** | 256 new tokens keeps a laptop run to a reasonable wait |
| **Model ids in one place** | Hosted providers retire ids; the Groq notebook warns that they change regularly |
| **The backend's own library first** | Seeing encode, generate and decode by hand explains what the wrapper does for you |

*Table 3: Five choices and the reason for each.*

## Limits

- **No token counts locally.** The pipeline path returns the text without usage metadata. Cost and length checks that read `.usage_metadata` see nothing.
- **The last message must be human.** The local wrapper raises an error when the last message is a system or AI message, and it accepts only system, human and AI messages. Tool results (M22) cannot pass through it.
- **Replies differ by backend.** A 1.1B model on a laptop and a large hosted model give different answers to the same prompt. Re-run the golden questions before relying on any of them (the silent provider swap from lesson 6.2).

To run it, the local part needs the course's optional Hugging Face dependency group and downloads about 2 GB of weights on first use; the hosted parts need a Hugging Face token and a Groq API key in the project's environment file.

## Key Takeaways

- The same `prompt | model` chain runs on a local model, a hosted Hugging Face model and Groq; only the model object changes.
- `ChatHuggingFace` gives completion-style Hugging Face classes the chat interface. Locally it renders messages with the model's own chat template; hosted, it sends role dicts to the server.
- The interface hides real differences: the local path reports no token counts and accepts only system, human and AI messages, and every backend answers differently.

## Check yourself

<details>
<summary>1. What does ChatHuggingFace do on the local path that the hosted path leaves to the server?</summary>

It renders the message list into one string with the model's own chat template, the special tokens that mark each role for that model family. The pipeline then generates from that string. On the hosted path the wrapper sends role dicts and the server does the rendering.

</details>

<details>
<summary>2. Larkspur logs input and output tokens from every reply. What happens to those logs when the refund chain moves to the local TinyLlama backend?</summary>

They go empty. The pipeline path returns an `AIMessage` with the text only and no usage metadata, while the hosted endpoint and Groq report token counts. Cost and length checks need another source of counts on the local path.

</details>

<details>
<summary>3. The chain runs on all three backends without a code change. Which backend should Larkspur pick for structured refund answers?</summary>

The chain running proves only that the call shape is the same. Re-run the golden questions and the parser test set on each backend and compare usable answers, citation validity and latency; a small local model may follow the JSON format instructions less reliably than a large hosted one.

</details>

---
*Previous: [6.2 Commercial LLMs natively and with LangChain](../02_commercial_llms_natively_and_with_langchain/README.md). Next: [6.4 Inputs and outputs: messages, LLM vs chat model](../04_inputs_and_outputs_messages_llm_vs_chat_model/README.md).*
