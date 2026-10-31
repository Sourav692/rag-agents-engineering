# M30.4 Theory: Strategy per query type

*[M30 theory](../README.md) · Lesson 30.4 · Notebooks: [`04a_adaptive_retrieval_rag_techniques.ipynb`](../../../../course/p09_agentic_rag/m30_adaptive_rag_routing/notebooks/04a_adaptive_retrieval_rag_techniques.ipynb) · [All theory pages](../../../README.md)*

## Per-query strategy

Lessons 30.1 to 30.3 route a question to a place: a knowledge base, a person, the web. The 04a notebook routes it to a method. A classifier labels the question Factual, Analytical, Opinion or Contextual, and each label runs a different retrieval strategy over the same index. The idea is to spend retrieval work where the question needs it: precision for a fact, coverage for an analysis, spread for an opinion, the user's situation for a contextual question.

| Type | What the question wants | How 04a retrieves | LLM calls per question |
|---|---|---|---|
| Factual | One verifiable fact | Rewrites the query, retrieves 8 chunks, has the LLM score each from 1 to 10, keeps the top 4 | Up to 11 |
| Analytical | An explanation that covers several aspects | Generates 4 sub-questions, retrieves 2 chunks for each, has the LLM pick the 4 most diverse and relevant | 4 |
| Opinion | Several viewpoints | Has the LLM name 3 viewpoints, retrieves 2 chunks for each, has the LLM pick 3 representative ones | 4 |
| Contextual | An answer for this user | Rewrites the query with the user's context, retrieves 8 chunks, scores each against query and context, keeps the top 4 | Up to 11 |

The call counts include the classifier and the final answer. The factual and contextual strategies score chunks one LLM call at a time, so their cost grows with the number retrieved; the analytical and opinion strategies spend one call to plan the searches and one to select.

On the Larkspur handbook the four types look like this:

- **Factual:** *How long does a refund take?* One chunk holds the answer; precision matters more than coverage.
- **Analytical:** *Should we move from monthly to annual billing?* The answer needs the billing cycle, the refund window and cancellation, three chunks a single query may not reach together.
- **Opinion:** *Is the starter plan good enough for a small shop?* A handbook states policies, not opinions, so a viewpoint search finds little; the honest answer lists the facts that bear on the choice.
- **Contextual:** *Which server size do I need?* The answer depends on the customer's peak memory use, which belongs in the context passed to the strategy.

The notebook's code has four faults worth knowing before you reuse it:

- **The classifier's label is free text.** `categories_options.category` is a `str`, and `AdaptiveRetriever` looks it up in a dictionary of four strategies. Any other spelling raises a `KeyError`. A `Literal` field, as in lesson 30.1, closes the set.
- **The opinion strategy cannot finish.** The selection call returns `SelectedIndices`, whose `indices` field is already a list of integers, and the code then calls `.split()` on it, which raises an `AttributeError`. Iterating over the list fixes it.
- **The user's context never arrives.** `ContextualRetrievalStrategy.retrieve` accepts `user_context`, but `AdaptiveRetriever` calls every strategy with the query alone, so the contextual path always runs with "No specific context provided".
- **Each strategy builds its own index.** All four inherit a constructor that splits the texts (800 characters, no overlap), embeds them and builds a FAISS index, so the corpus is embedded four times at start-up. One shared index serves all four.

The demo corpus is one sentence about the Earth. Every search returns that one chunk, so the four strategies cannot retrieve different evidence and the demo cannot show that the routing helps. To see it, run the four sample questions over a real corpus and compare each strategy against plain top-k retrieval on the same golden set, the way M11 sets a baseline.

The Adaptive-RAG paper behind lesson 30.3 routes on a different axis, question complexity: no retrieval, one step or several. The two combine. A complexity router decides how many rounds of retrieval to run; a type router decides what each round looks for.

## Check yourself

<details>
<summary>1. What does the per-query strategy router choose, compared with the routers in the earlier lessons of this module?</summary>

The earlier routers send a question to a place: a knowledge base, a person or the web. This one sends it to a method over the same index, spending retrieval work where the question needs it: precision for a fact, coverage for an analysis, spread for an opinion, the user's situation for a contextual question.

</details>

<details>
<summary>2. A Larkspur customer asks whether to move from monthly to annual billing. Which query type is it, and how does that strategy retrieve?</summary>

Analytical. The answer needs the billing cycle, the refund window and cancellation, three chunks a single query may not reach together. The strategy generates 4 sub-questions, retrieves 2 chunks for each and has the LLM pick the 4 most diverse and relevant, for 4 LLM calls in all.

</details>

<details>
<summary>3. In the notebook's demo all four strategies return the same evidence. Does that show routing by query type does not help?</summary>

No. The demo corpus is one sentence about the Earth, so every search returns that one chunk and the strategies cannot differ. Run the four sample questions over a real corpus and compare each strategy with plain top-k retrieval on the same golden set, the way M11 sets a baseline.

</details>

---
*Previous: [30.3 Adaptive RAG: vector store vs web, with hallucination grading](../03_adaptive_rag_vector_store_vs_web_with_hallucination_grading/README.md). Next: [M30 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
