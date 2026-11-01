# M18.5 Theory: HyDE: embed a hypothetical answer

*[M18 theory](../README.md) · Lesson 18.5 · Notebooks: [`05a_hyde.ipynb`](../../../../course/p06_retrieval_quality/m18_query_transformation/notebooks/05a_hyde.ipynb), [`05b_hyde_walkthrough.ipynb`](../../../../course/p06_retrieval_quality/m18_query_transformation/optional/05b_hyde_walkthrough.ipynb) (optional), [`05c_hyde_rag_techniques.ipynb`](../../../../course/p06_retrieval_quality/m18_query_transformation/optional/05c_hyde_rag_techniques.ipynb) (optional) · [All theory pages](../../../README.md)*

## HyDE

HyDE (Hypothetical Document Embeddings, Gao et al., [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)) attacks the shape half of the [query-document asymmetry](../01_query_rewriting_and_expansion/README.md#querydocument-asymmetry). Instead of embedding the question, it asks an LLM to write an answer, embeds that answer, and searches with its vector. An invented answer is declarative, long and full of the vocabulary documentation uses, so it lands nearer the real passage than the question does.

```mermaid
flowchart LR
    Q[/Question/] --> G["LLM writes a<br/>hypothetical answer"]
    G --> E["Embed the answer<br/>same model as the index"]
    E --> S["Search the index<br/>by vector"]
    S --> C[/Real chunks/]
```

The hypothetical answer is a search key. Its facts may be wrong, and that does not matter: it is discarded after embedding, never reaches the user and never enters the context. The chunks that come back are real.

### Two models, one index

HyDE always needs an LLM to write and an embedding model to embed, and the embedding model must be the one that built the index, or the vectors are not comparable. The index itself is built plainly. Documents are already answer-shaped, and indexing through an LLM would cost a generation per chunk.

LangChain packages the three steps as `HypotheticalDocumentEmbedder`, which behaves differently for the two methods of the `Embeddings` interface:

| Method | What it does |
|---|---|
| `embed_documents()` | Passes straight through to the base embedder, no LLM call |
| `embed_query()` | Runs the LLM, then embeds the generated text |

The 05a notebook checks the first row: a document embedded through the HyDE wrapper matches the plain embedding. That pass-through is what lets you hand the HyDE embedder to `Chroma.from_documents()` as a drop-in (indexing stays plain, every `similarity_search()` applies HyDE), or call `embed_query()` yourself and search an existing index with `similarity_search_by_vector()`. `from_llm()` takes a prompt key naming one of eight built-in templates inherited from the BEIR datasets the paper used; `web_search` is the general one, *"Please write a passage to answer the question"*. The 05a notebook writes its own prompt instead, asking for an excerpt from technical documentation, so the hypothetical answer matches the genre of the indexed chunks.

### Several hypothetical answers

The paper generates several hypothetical answers and averages their embeddings, so no single invention dominates the search vector. The current, Runnable-based `HypotheticalDocumentEmbedder` cannot do this: its chain returns one string, so `combine_embeddings()` always averages exactly one vector. The 05a notebook generates three answers itself at `temperature=0.8`, embeds them and averages them, then checks their cosine similarity to each other. Near 1.0 means the three are near-identical and the average bought nothing for three times the cost.

### When it helps and when it hurts

| | Plain retrieval | HyDE |
|---|---|---|
| Cost per query | one embedding call | one LLM call plus one embedding call |
| Short or vague questions | often misses | the LLM supplies the missing vocabulary |
| Niche or private corpus | retrieves what is there | the LLM invents plausible jargon and can steer away from the right chunk |
| Questions that already read like documents | strong | no better, sometimes worse |

The Larkspur handbook is the private case. No model was trained on Larkspur's refund window or its outage credits, so a hypothetical answer to *What happens if my server goes down?* is written from what the model knows about hosting providers in general. That text is likely to use outage vocabulary, which helps here, and it can also name terms the handbook never uses, which pull the vector toward nothing. The 05a notebook ends with the test that settles it: retrieve with and without HyDE on the same questions and count the overlap, rather than assume a gain.

## Key Takeaways

- HyDE embeds an LLM-written answer instead of the question, because an answer-shaped text lands nearer the real passage. The invented answer is only a search key and is discarded.
- Embed with the same model that built the index. `HypotheticalDocumentEmbedder` keeps indexing plain and applies the LLM only in `embed_query()`.
- HyDE helps short or vague questions and can hurt on a private corpus, where the LLM invents jargon the documents never use. Compare retrieval with and without it before turning it on.

## Check yourself

<details>
<summary>1. The hypothetical answer HyDE writes may state wrong facts. Why does that not mislead the user?</summary>

It is only a search key. It is embedded, then discarded: it never reaches the user and never enters the context. The chunks that come back from the index are real, and the answer is built from them.

</details>

<details>
<summary>2. You pass the HyDE embedder to Chroma.from_documents to build the Larkspur index. Does indexing call the LLM?</summary>

No. `embed_documents()` passes straight through to the base embedder, so indexing stays plain, while `embed_query()` runs the LLM and embeds its text, so every `similarity_search()` applies HyDE. The base embedder must be the model that built the index, or the vectors are not comparable.

</details>

<details>
<summary>3. Should you turn HyDE on for the Larkspur handbook?</summary>

Only after testing it. No model was trained on Larkspur's refund window or outage credits, so a hypothetical answer comes from general hosting knowledge: its outage vocabulary may help, and terms the handbook never uses can pull the vector toward nothing. Retrieve with and without HyDE on the same questions and count the overlap.

</details>

---
*Previous: [18.3 RAG-Fusion with Reciprocal Rank Fusion](../03_rag_fusion_with_reciprocal_rank_fusion/README.md). Next: [18.6 Query decomposition for multi-hop questions](../06_query_decomposition_for_multi_hop_questions/README.md).*
