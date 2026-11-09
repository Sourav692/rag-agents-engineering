# M17.2 Theory: Multi-query retrieval

*[M17 theory](../README.md) · Lesson 17.2 · Notebooks: [`02a_multi_query_retrieval.ipynb`](../../notebook/02a_multi_query_retrieval.ipynb), [`02b_multiquery_retrieval_walkthrough.ipynb`](../../../optional/notebook/02b_multiquery_retrieval_walkthrough.ipynb) (optional), [`02c_better_queries.ipynb`](../../../optional/notebook/02c_better_queries.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Ask the question three ways, search each way, and keep everything any phrasing found -->

## One question, one point in space

> **What you'll learn**
>
> - **Explain** why several phrasings of one question reach chunks a single phrasing misses.
> - **Trace** three variants of a Larkspur question through retrieval and a flat union.
> - **Diagnose** two silent multi-query bugs: the id-only merge and junk variants.
> - **Judge** whether the extra calls bought anything, against the single-query baseline.

Lesson 17.1 named the vocabulary gap and closed it with one expanded query. Expansion still produces a single query, and a single query is a single point in embedding space.

If that point happens to sit far from how the handbook words the answer, the relevant chunks are missed, and nothing reports it. Retrieval fails silently: the top `k` is always full, as lesson 16.1 showed. The outage question in the M10 index retrieves `reboot`, `sizing` and `export` with confidence and neither evidence chunk.

**Multi-query retrieval** asks an LLM to write several phrasings of the question, retrieves for each, and merges the results:

```mermaid
flowchart LR
    Q[/Question/] --> V["LLM writes<br/>3 phrasings"]
    V --> R["Retrieve for<br/>each phrasing"]
    R --> U["Flat union<br/>each chunk once"]
    U --> A["Answer prompt<br/>+ original question"]
```

*Figure 1: Multi-query retrieval. One LLM call in, one retrieval per phrasing, one merged list out.*

Notebook `02a` asks for three phrasings, each targeting a different angle of the question. Its knowledge base is two LangChain blog posts, chunked at 400 tokens with 60 of overlap, and its baseline cell first records what the question alone retrieves, so the variants have something to beat.

## Vocabulary spread

The mechanism is **vocabulary spread**: each phrasing reaches for different words, and each set of words lands near different chunks. `02a` illustrates it with three ways of asking about LangSmith. A definition question lands near product overviews, a debugging question near tracing and errors, a production question near reliability.

The module's lab carries hand-written variants for the Larkspur golden questions, in the style of the `02a` prompt. Here are the first three for the outage question, each retrieving its top 4 from the M10 TF-IDF index:

| Phrasing | Retrieved (top 4, nonzero only) |
|---|---|
| *What happens if my server goes down?* (as asked) | `reboot`, `sizing`, `export` |
| *What compensation do I receive when an outage affects my server?* | **`sla`**, `reboot`, `sizing`, `export` |
| *How does Larkspur communicate during a service incident?* | **`sla`**, **`incidents`**, `reboot` |
| *What uptime or availability does Larkspur guarantee?* | **`sla`**, `reboot` |

*Table 1: Three variants of the outage question (the module's query-variant lab, M10 index, TF-IDF). Evidence chunks in bold.*

The variants succeed by borrowing the handbook's vocabulary: "outage", "incident", "availability". None of them is a better question than the original. Together they cover more of the space around it.

## Merging: the flat union

Three lists come back, and they overlap. The **flat union** keeps each chunk once, in the order it was first seen: the first variant's list, then whatever the second adds, and so on. Here is what the union buys over the question as asked, on all three golden questions:

| Golden question | Union of 3 variants | Recall at 2 | Recall at 3 | As asked, recall at 2 |
|---|---|---|---|---|
| *How long does a refund take?* | `refund-timing`, `refund-window`, `support`, `retention`, `export`, `sla` | 1.00 | 1.00 | 0.50 |
| *What happens if my server goes down?* | `sla`, `reboot`, `sizing`, `export`, `incidents` | 0.50 | 0.50 | 0.00 |
| *Can I export my data after I cancel my plan?* | `retention`, `export`, `refund-window`, `cancel`, `reboot`, `sizing` | 1.00 | 1.00 | 1.00 |
| **Mean** | | **0.83** | **0.83** | **0.50** |

*Table 2: Flat union of three variants against the question as asked (same lab and index).*

Mean recall at 2 rises from 0.50 to 0.83. The outage row shows what the union cannot do. `incidents` was found, by the second variant, and still lands 5th, because the first variant's four chunks come first. The union knows nothing about rank or agreement: a chunk every variant ranked first looks the same as one that scraped into one list. We call this **order by arrival**, and lesson 17.3 replaces it with rank fusion.

`02a` ends with the check that keeps the technique honest: compare the merged chunks with the baseline. If the variants return what the original query returned, multi-query is pure overhead on that corpus, and the export question above is such a case.

## Two silent bugs

Both bugs below shipped in earlier versions of the notebooks, and neither raised an error.

**The id-only merge.** The original `get_unique_union()` in `02a` de-duplicated by document id and returned the ids, not the documents. Every LangChain document has an id attribute, so that branch always ran, and the answer prompt's context held a list of bare identifiers. The model answered from memory, fluently, and the output looked like a working RAG chain. The fix keys the merge by the chunk's text and returns the documents themselves; `02a` then asserts that the context contains real passage text.

**Junk variants.** Parsing the LLM's reply by splitting it on newlines assumes exactly three bare lines. Models add headers, numbering, blank lines and preambles such as "Here are three variations:", and each of those becomes a query sent to the retriever. The failure is intermittent: the same chain returns clean lines on one run and markdown on the next. `02a` binds a schema with structured output, so the reply is a list of exactly the phrasings. The optional notebooks `02b` and `02c` show the older approach, a regular expression that cleans the split text, and use the same pattern to generate five hypothetical answers for HyDE (lesson 17.5).

> **Pitfall: fluent answers from an empty context.** A RAG chain whose context is broken still answers. Print what the retriever handed to the prompt before judging the answer.

## What it costs

Multi-query adds one LLM call and turns one retrieval into three:

| Step | LLM calls | Retrievals |
|---|---|---|
| Write 3 phrasings | 1 | 0 |
| Retrieve per phrasing | 0 | 3, run in parallel |
| Answer | 1 | 0 |
| **Total** | **2** | **3** |

*Table 3: Calls per question, against 1 and 1 for plain RAG.*

The retrievals are independent, so `02a` runs them as one parallel batch, and the wall-clock cost is roughly one retrieval plus one LLM call. The context also grows: the outage union holds 5 chunks where the original question returned 3.

## In practice: multi-query on the Larkspur handbook

1. **Use it where the baseline misses.** The refund and outage questions gain; the export question gains nothing.
2. **Parse with a schema** and log every phrasing, so a drifting or junk variant is visible in traces.
3. **Assert the context is text**, not ids, in a test that runs on every change.
4. **Cut by rank, not arrival.** At two chunks the union drops `incidents`. Lesson 17.3 keeps the same variants and fixes the order.

## Key Takeaways

- One question is one point in embedding space. Multi-query writes three phrasings, retrieves for each, and keeps the union, which lifts mean recall at 2 on the Larkspur golden questions from 0.50 to 0.83.
- The flat union orders chunks by arrival, so found evidence can still miss the cut: `incidents` lands 5th for the outage question.
- Return documents from the merge, never ids, and parse phrasings with a schema. Both bugs fail silently while the chain keeps answering fluently.

## Check yourself

<details>
<summary>1. The outage question as asked retrieves neither evidence chunk. How do three phrasings reach them?</summary>

By vocabulary spread. Each phrasing uses different words, and the variants borrow the handbook's own: "outage", "incident", "availability". The compensation variant reaches `sla`, and the incident variant reaches both `sla` and `incidents`.

</details>

<details>
<summary>2. The union of three variants contains incidents, yet recall at 2 for the outage question is only 0.50. Why?</summary>

The flat union orders chunks by arrival: the first variant's four chunks come first, and `incidents`, found by the second variant, lands 5th. The union ignores rank and agreement, so found evidence can still miss the cut. Rank fusion (lesson 17.3) fixes the order.

</details>

<details>
<summary>3. A multi-query chain gives fluent answers, but they never quote the handbook. Where do you look first?</summary>

At what the retriever handed to the answer prompt. If the merge returned document ids instead of documents, the context holds bare identifiers and the model answers from memory. Key the merge by chunk text, return the documents, and assert that the context contains passage text.

</details>

---
*Previous: [17.1 Query rewriting and expansion](../01_query_rewriting_and_expansion/README.md). Next: [17.3 RAG-Fusion with Reciprocal Rank Fusion](../03_rag_fusion_with_reciprocal_rank_fusion/README.md).*
