# M07.2 Theory: Commercial LLMs natively and with LangChain

*[M07 theory](../README.md) · Lesson 7.2 · Notebooks: [`02a_Commercial_LLMs_with_LangChain.ipynb`](../../../../course/p03_langchain_and_langgraph/m07_langchain_core/notebooks/02a_Commercial_LLMs_with_LangChain.ipynb), [`02b_Commercial_LLMs_Natively.ipynb`](../../../../course/p03_langchain_and_langgraph/m07_langchain_core/optional/02b_Commercial_LLMs_Natively.ipynb) (optional) · [All theory pages](../../../README.md)*

## Chat models

A chat model is any class that implements LangChain's `BaseChatModel` interface. The provider SDKs in the optional notebook (and in [M02](../../../p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/README.md)) each return their own response object; the LangChain classes return the same one for every provider. Every chat model has the same three calls:

| Call | Takes | Returns |
|---|---|---|
| `invoke` | a string, a message list or a `PromptValue` | one `AIMessage` |
| `batch` | a list of inputs | a list of `AIMessage`, run concurrently on a thread pool |
| `stream` | one input | the reply in chunks as it arrives |

The `AIMessage` carries more than the text. Lesson 7.2 reads three attributes:

- `.content`: the reply text.
- `.usage_metadata`: input, output and total token counts, under the same keys for every provider.
- `.response_metadata`: what the provider reported, such as `model_name` and `finish_reason`. On OpenAI a `finish_reason` of `length` means the reply hit the token limit and stopped mid-sentence, or mid-JSON; [lesson 7.6](../06_output_parsers/README.md#output-parsers) shows what the parsers make of that.

Changing provider changes one class. In the notebooks the same `prompt | model` chain runs on all of these:

| Class | Where the model runs | Model in the notebook |
|---|---|---|
| `ChatOpenAI` | OpenAI's API | `gpt-4o-mini` |
| `ChatGoogleGenerativeAI` | Google's Gemini API | `gemini-2.5-flash` |
| `ChatGroq` | Groq's hosted inference | `llama-3.1-8b-instant` |
| `ChatHuggingFace` over `HuggingFaceEndpoint` | Hugging Face Inference Providers | `moonshotai/kimi-k2-instruct-0905` |
| `ChatHuggingFace` over `HuggingFacePipeline` | your own machine | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` |

The last three come from lesson 7.3's [`03a_Open_Source_LLMs_with_LangChain.ipynb`](../../../../course/p03_langchain_and_langgraph/m07_langchain_core/notebooks/03a_Open_Source_LLMs_with_LangChain.ipynb). `ChatHuggingFace` is a wrapper: the two Hugging Face classes underneath are completion-style LLMs, and the wrapper gives them the chat interface ([lesson 7.4](../04_inputs_and_outputs_messages_llm_vs_chat_model/README.md#llm-vs-chat-model)).

`init_chat_model` moves the choice out of the import line and into a string, which is how notebook 01b loads its model:

```python
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Explain {topic} in 2 bullet points")
llm = init_chat_model("openai:gpt-4o-mini", temperature=0)
# llm = init_chat_model("groq:openai/gpt-oss-120b", temperature=0)

reply = (prompt | llm).invoke({"topic": "AI"})   # an AIMessage
```

The swap keeps the code running. It does not keep the replies the same: another model formats, refuses and rambles differently. For Larkspur, a provider change is a release like any other, checked against the golden questions from [M11](../../../p04_rag_foundations/m11_rag_lifecycle/README.md) before it ships.

---
*Previous: [7.1 LangChain introduction and the 1.x package split](../01_langchain_introduction_and_the_1_x_package_split/README.md). Next: [7.4 Inputs and outputs: messages, LLM vs chat model](../04_inputs_and_outputs_messages_llm_vs_chat_model/README.md).*
