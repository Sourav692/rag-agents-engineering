# M13.3 Theory: Proposition chunking with LLM quality checks

*[M13 theory](../README.md) · Lesson 13.3 · Notebooks: [`03a_proposition_chunking.ipynb`](../../../../course/p05_ingestion_and_indexing/m13_chunking/notebooks/03a_proposition_chunking.ipynb), [`03b_proposition_chunking_rag_techniques.ipynb`](../../../../course/p05_ingestion_and_indexing/m13_chunking/optional/03b_proposition_chunking_rag_techniques.ipynb) (optional) · [All theory pages](../../../README.md)*

## Propositions

A proposition is one fact written so it stands alone. It has to be:

- **Atomic:** one claim. "Annual plans can be refunded within 30 days and refunds take 5 to 10 business days" is two.
- **Self-contained:** no unresolved references. "It takes 5 to 10 business days" means nothing once retrieved alone; "A Larkspur Cloud refund takes 5 to 10 business days to appear" does.

The refund sentence becomes three propositions:

1. Larkspur Cloud gives a full refund on an annual plan requested within 30 days of purchase.
2. A full refund on a Larkspur Cloud annual plan requires the account to have used less than 100 GB of outbound traffic.
3. After day 30, a Larkspur Cloud annual-plan refund is prorated to the unused whole months, minus a 15% early-termination fee.

Each proposition names its own subject and condition, so the golden question can match proposition 1 and the retriever can return proposition 2 beside it.

```mermaid
flowchart LR
    C[Source chunk] --> G["LLM: rewrite as<br/>atomic, self-contained facts"]
    G --> P[Propositions]
    P --> J{"Grade each one against the source:<br/>accurate, clear, complete, concise"}
    J -- pass --> IDX[(Index propositions<br/>with source chunk id)]
    J -- fail --> DROP[Drop or regenerate]
```

Grade every proposition against its source chunk before indexing it. A splitter can only cut text, while an LLM can merge two facts, drop a qualifier ("less than 100 GB" disappears) or state something the source only implied. Keep the source chunk id in metadata so you can show the original text at answer time.

Cost decides where propositions are worth it: one LLM call per source chunk to generate, about one more to grade, and usually several times as many vectors. Use them for dense, high-value text (policies, specs, medical or legal facts) where a missed qualifier is expensive, not for a whole document lake.

---
*Previous: [13.2 Semantic chunking: breakpoints on embedding distance](../02_semantic_chunking_breakpoints_on_embedding_distance/README.md). Next: [13.4 Choosing chunk size empirically: retrieval quality, faithfulness, latency](../04_choosing_chunk_size_empirically_retrieval_quality_faithfulness_latency/README.md).*
