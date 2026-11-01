# M20.1 Theory: Environment setup and a complete RAG system

*[M20 theory](../README.md) · Lesson 20.1 · Notebooks: [`01a_setup.ipynb`](../../../../course/p07_rag_applications/m20_end_to_end_rag_systems/notebooks/01a_setup.ipynb), [`01b_build_a_simple_rag_system.ipynb`](../../../../course/p07_rag_applications/m20_end_to_end_rag_systems/notebooks/01b_build_a_simple_rag_system.ipynb), [`01c_simple_rag_pdf.ipynb`](../../../../course/p07_rag_applications/m20_end_to_end_rag_systems/optional/01c_simple_rag_pdf.ipynb) (optional) · [All theory pages](../../../README.md)*

## Grounded generation

A grounded answer comes from evidence the system retrieved for this question, and the model is told to use nothing else. Lesson 20.1 builds the whole pipeline in one notebook, from two kinds of source to a chain that answers from them.

| Stage | What `01b` does |
|---|---|
| Load | `JSONLoader` reads `wikidata_rag_demo.jsonl` one line per Document; each article's `paragraphs` are joined and `title`, `id` and `source` kept as metadata. `PyMuPDFLoader` reads every PDF in `data/sample/`. |
| Split | `RecursiveCharacterTextSplitter`, `chunk_size=3500`, `chunk_overlap=200`, for the PDFs. Wikipedia articles stay whole. |
| Embed | `text-embedding-3-small`, 1,536 dimensions. |
| Store | Chroma, persisted to `./my_db`, with `collection_metadata={"hnsw:space": "cosine"}`. Without it Chroma uses Euclidean distance ([M11.4](../../../p04_rag_foundations/m11_rag_lifecycle/04_your_first_langchain_rag_with_chroma/README.md#distance-not-similarity)). |
| Retrieve | `as_retriever(search_type="similarity", search_kwargs={"k": 5})`. |
| Generate | `gpt-4o-mini` at `temperature=0`, with a prompt that restricts it to the retrieved context. |

The chain is three LCEL steps:

```mermaid
flowchart LR
    Q[/Question/] --> R["similarity_retriever<br/>k = 5"]
    R --> F["format_docs<br/>page_content only"]
    Q --> P["rag_prompt_template<br/>question + context"]
    F --> P
    P --> L["gpt-4o-mini<br/>temperature 0"]
    L --> A[/AIMessage/]
```

Grounding rests on three things, and the notebook's prompt has all three:

1. **The evidence is retrieved for this question.** The model sees five chunks, not the corpus.
2. **The instruction limits the model to that evidence.** "Answer the following question using only the following pieces of retrieved context."
3. **The model has a way out.** "If the answer is not in the context, do not make up answers, just say that you don't know." Without a permitted refusal, a model asked about something the context lacks will answer from what it learned in training.

On the Larkspur handbook, *Can I export my data after I cancel my plan?* retrieves the `export` and `retention` chunks, and the answer should say "within 30 days, from Settings, then Data". *Does Larkspur offer a free tier?* has no chunk in the handbook, so the grounded answer is "I don't know". Whether a given model complies is a property you test: put questions with no answer in the golden set and count the refusals.

The instruction does not guarantee compliance. A model can still blend in outside knowledge or misread a chunk; [M29](../../../p09_agentic_rag/m29_crag_and_self_rag/README.md) and [M32](../../../p09_agentic_rag/m32_reliability_feedback/README.md) add a second call that grades the answer against its evidence.

### What this chain throws away

`format_docs` joins `doc.page_content` and nothing else, so the title, id and source in metadata never reach the model, and the chain returns only an `AIMessage`. The answer may be grounded, but nobody can check it. There is no list of chunks and no way to say which one a sentence came from. Lesson 20.2 keeps both.

### A setup trap from the notebook

`openai_embed_model.embed_documents("Hello, world!")` returns 13 vectors. `embed_documents` expects a list of strings, and a Python string is iterable, so each of the 13 characters is embedded on its own. Use `embed_query(text)` for one string, or `embed_documents([text])`; either gives one 1,536-dimension vector. The same mistake inside an indexing loop embeds characters and stores garbage without an error.

The optional `01c` notebook builds the same pipeline on FAISS from one PDF, `Understanding_Climate_Change.pdf`, with 1,000-character chunks, 200 overlap and `k=2`, and reconstructs the index matrix to show its shape: one row per chunk, 1,536 columns.

## Key Takeaways

- Grounding needs three things in the prompt: evidence retrieved for this question, an instruction to use only that evidence, and permission to say "I don't know".
- The instruction does not guarantee compliance. Put questions with no answer in the golden set and count the refusals.
- A chain that formats only `page_content` and returns only the answer cannot be checked. Keep the chunks and their metadata if anyone needs to verify a sentence.

## Check yourself

<details>
<summary>1. What three things in the 01b prompt keep an answer grounded?</summary>

The evidence is retrieved for this question, five chunks rather than the corpus. The instruction limits the model to that evidence. And the model has a way out: it may say it does not know, because without a permitted refusal a model asked about something the context lacks answers from training.

</details>

<details>
<summary>2. A user asks the Larkspur system whether Larkspur offers a free tier. What should the grounded answer be, and how do you know the model complies?</summary>

"I don't know", because no chunk in the handbook covers a free tier. The instruction does not guarantee compliance, so put questions with no answer in the golden set and count the refusals.

</details>

<details>
<summary>3. Embedding the string Hello, world! with embed documents returns 13 vectors. What went wrong?</summary>

`embed_documents` expects a list of strings, and a Python string is iterable, so each of the 13 characters was embedded on its own. Use `embed_query(text)` or `embed_documents([text])` for one 1,536-dimension vector. Inside an indexing loop the same mistake stores garbage without an error.

</details>

---
*Previous: [M20 overview](../README.md). Next: [20.2 Answers with sources and per-claim citations](../02_answers_with_sources_and_per_claim_citations/README.md).*
