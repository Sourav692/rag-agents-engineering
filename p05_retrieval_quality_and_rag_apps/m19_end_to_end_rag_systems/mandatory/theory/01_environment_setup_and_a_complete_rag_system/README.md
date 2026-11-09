# M19.1 Theory: Environment setup and a complete RAG system

*[M19 theory](../README.md) · Lesson 19.1 · Notebooks: [`01a_setup.ipynb`](../../notebook/01a_setup.ipynb), [`01b_build_a_simple_rag_system.ipynb`](../../notebook/01b_build_a_simple_rag_system.ipynb), [`01c_simple_rag_pdf.ipynb`](../../../optional/notebook/01c_simple_rag_pdf.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: A grounded answer needs evidence, a limit and a way out, and a checkable one needs its sources kept -->

## Grounded generation

> **What you'll learn**
>
> - **Trace** a complete RAG system from two kinds of source to an answer.
> - **Explain** the three parts of a grounded prompt and what each one prevents.
> - **Diagnose** a chain whose answers cannot be checked, and an embedding call that embeds characters.
> - **Test** grounding with questions the corpus cannot answer.

Lessons M16 to M18 made retrieval find more, rank better and fit the budget. M19 turns a retrieval pipeline into a system someone can rely on, and starts by building one end to end.

A Larkspur customer asks *Does Larkspur offer a free tier?* The handbook says nothing about one. A chain that retrieves five chunks and asks the model to "answer the question" gets a fluent reply anyway, drawn from what the model knows about other hosting providers. The answer reads as policy, and it is invented.

**Grounded generation** means the answer comes from evidence the system retrieved for this question, and the model is told to use nothing else. Notebook `01b` builds the whole pipeline:

| Stage | What `01b` does |
|---|---|
| Load | A JSON-lines loader reads a Wikipedia sample one article per document, keeping title, id and source as metadata; a PDF loader reads every PDF in a sample folder |
| Split | 3,500-character chunks with 200 of overlap for the PDFs; Wikipedia articles stay whole |
| Embed | `text-embedding-3-small`, 1,536 dimensions |
| Store | Chroma, persisted to disk, set to cosine distance; without that setting Chroma uses Euclidean distance ([M10.4](../../../../../p04_rag_foundations/m10_rag_lifecycle/mandatory/theory/04_your_first_langchain_rag_with_chroma/README.md#distance-not-similarity)) |
| Retrieve | Similarity search, `k = 5` |
| Generate | A small chat model at temperature 0, with a prompt that restricts it to the retrieved context |

*Table 1: The pipeline in `01b`.*

The chain itself is three steps:

```mermaid
flowchart LR
    Q[/Question/] --> R["similarity_retriever<br/>k = 5"]
    R --> F["format_docs<br/>page_content only"]
    Q --> P["rag_prompt_template<br/>question + context"]
    F --> P
    P --> L["gpt-4o-mini<br/>temperature 0"]
    L --> A[/AIMessage/]
```

*Figure 1: The `01b` chain. The retrieved chunks become plain text inside the prompt.*

Grounding rests on three things, and `01b`'s prompt has all three:

| Part | `01b`'s wording | What it prevents |
|---|---|---|
| **Evidence for this question** | The five retrieved chunks | The model answering from the whole of its training |
| **A limit** | "Answer the following question using only the following pieces of retrieved context" | Blending in outside knowledge |
| **A way out** | "If the answer is not in the context, do not make up answers, just say that you don't know" | A forced answer when the evidence is missing |

*Table 2: The three parts of a grounded prompt.*

The third part is the one most often left out. Without a permitted refusal, a model asked about something the context lacks answers from what it learned in training. We call that an **ungrounded fill**: the free-tier answer above.

Here is what grounding should produce on two Larkspur questions (*Illustrative*: expected answers, not a recorded run):

| Question | Retrieved evidence | Grounded answer |
|---|---|---|
| *Can I export my data after I cancel my plan?* | `export`, `retention` | Yes, within 30 days, from Settings, then Data |
| *Does Larkspur offer a free tier?* | Nothing relevant | I don't know |

*Table 3: Grounded answers, with and without evidence.*

Whether a given model complies is a property you test. Put questions with no answer in the golden set and count the refusals. The instruction does not guarantee compliance either: a model can still blend in outside knowledge or misread a chunk, and [M29](../../../../../p08_agentic_rag/m29_crag_and_self_rag/mandatory/theory/README.md) and [M32](../../../../../p08_agentic_rag/m32_reliability_feedback/mandatory/theory/README.md) add a second call that grades the answer against its evidence.

## What this chain throws away

`01b`'s formatting step joins the chunks' text and nothing else, so the title, id and source in metadata never reach the model, and the chain returns only the model's message. The answer may be grounded, but nobody can check it: there is no list of chunks, and no way to say which one a sentence came from. We call this **formatted-away sources**. Lesson 19.2 keeps both.

## A setup trap

`01b` embeds the string "Hello, world!" with the batch method meant for a list of documents, and gets back 13 vectors. A Python string is iterable, so each of its 13 characters is embedded on its own. The single-query method, or a one-item list, gives one 1,536-dimension vector.

> **Pitfall: character embedding.** The same mistake inside an indexing loop embeds characters and stores them without an error. Check that the number of vectors equals the number of chunks after every indexing run.

The optional `01c` notebook builds the same pipeline on FAISS from one climate-change PDF, with 1,000-character chunks, 200 of overlap and `k = 2`, and reconstructs the index matrix to show its shape: one row per chunk, 1,536 columns.

## In practice: a grounded Larkspur assistant

1. **Use all three parts** of Table 2 in the prompt, including the way out.
2. **Add unanswerable golden questions** (free tier, GPU servers) and track the refusal rate.
3. **Count vectors against chunks** after indexing.
4. **Keep the chunks in the output**, which lesson 19.2 shows how to do in one retrieval.

## Key Takeaways

- Grounding needs three things in the prompt: evidence retrieved for this question, an instruction to use only that evidence, and permission to say "I don't know". Without the last, the model fills gaps from training (an ungrounded fill).
- The instruction does not guarantee compliance. Put questions with no answer in the golden set and count the refusals.
- A chain that formats only the chunk text and returns only the answer cannot be checked (formatted-away sources). Keep the chunks and their metadata if anyone needs to verify a sentence.

## Check yourself

<details>
<summary>1. A Larkspur assistant answers "Does Larkspur offer a free tier?" with a confident description of one. Which part of a grounded prompt is missing?</summary>

Most likely the way out: permission to say "I don't know" when the answer is not in the context. Without it, a model whose evidence lacks the answer fills the gap from training. Add it, then test with unanswerable golden questions and count the refusals, because the instruction alone does not guarantee compliance.

</details>

<details>
<summary>2. The 01b chain's answers are grounded, but a reviewer cannot tell which chunk any sentence came from. Why?</summary>

The formatting step joins only the chunks' text, so titles, ids and sources never reach the model, and the chain returns only the model's message. There is no list of chunks to check against. Keeping the retrieved chunks in the output, as lesson 19.2 does, makes the answer checkable.

</details>

<details>
<summary>3. Embedding "Hello, world!" returns 13 vectors. What went wrong, and why is it dangerous in an indexing loop?</summary>

The batch method expects a list of strings, and a Python string is iterable, so each of its 13 characters was embedded separately. In an indexing loop the same mistake stores character vectors without an error. Use the single-query method or a one-item list, and check that vectors equal chunks after indexing.

</details>

---
*Previous: [M19 overview](../README.md). Next: [19.2 Answers with sources and per-claim citations](../02_answers_with_sources_and_per_claim_citations/README.md).*
