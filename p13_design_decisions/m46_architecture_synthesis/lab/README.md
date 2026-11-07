# Lab: M46 Architecture Synthesis: Choosing a System Design

## Brief

Architecture review: write a two-page design document for your capstone that justifies each component against a simpler alternative.

Solution: [solution/m46_solution.ipynb](solution/m46_solution.ipynb), a worked design document for [Capstone A, Enterprise Knowledge Assistant](../../../capstones/A_enterprise_knowledge_assistant/README.md).

## Approach

The document follows the [decision framework page](../mandatory/theory/03_decision_framework_picking_the_simplest_architecture_that_works/README.md) of this module:

- **Architecture selection.** Each component answers a failure the golden set shows, cheapest fix first: retrieval, then routing, index shape, an agent loop, and a check last. A component with no failure behind it stays out, and the document says which evidence would bring it back.
- **Complexity budget.** Every row records the model calls it adds per question. A component earns its place with a measured gain on the golden set that nothing cheaper buys.
- **One row per component.** Each row names the simpler alternative, why it is not enough, and the check behind that claim. Capstone A's required components (ingestion with metadata, measured chunking and embeddings, pgvector with incremental indexing, hybrid retrieval and reranking, per-claim citations, a CRAG fallback) each get a row, plus the plain RAG baseline and the RAG or fine-tune choice.

Code cells appear only where a claim can be checked on the Larkspur golden set:

1. **Is plain RAG enough?** `lab_kit.baseline` and the list of questions whose evidence is missing from the top 4, by question type.
2. **Chunk size.** 250, 500 and 1,000 characters on the same TF-IDF baseline.
3. **Retrieval.** TF-IDF, dense embeddings and their reciprocal rank fusion, scored with the `lab_kit` metrics.
4. **Out-of-corpus questions.** Whether a threshold on the top TF-IDF score separates the five out-of-corpus questions from the answerable ones, the simpler alternative to a relevance grader. The CRAG web branch is replaced by a decline, because the company's facts are private (M29).

What to watch: hit rate is scored on the 25 golden questions with evidence, so one question moves it by 0.04. Treat a small difference between two rows as a tie and keep the cheaper component.

**The row that depends on M45.** The last row, RAG or fine-tune, takes its decision from the [M45 lab verdict](../../m45_fine_tuning_model_adaptation/lab/README.md#verdict). Until that verdict exists the row reads *pending the M45 verdict*.

## How to run

```bash
uv sync
uv run jupyter lab p13_design_decisions/m46_architecture_synthesis/lab/solution/m46_solution.ipynb
```

Keys: sections 1, 2 and 4 run offline with no keys. Section 3 needs `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings.

## Data

[data/README.md](data/README.md): the Larkspur handbook and golden set (`data/larkspur/`, an unchanged copy).

## Results

*Pending run.* The owner runs the solution and fills these tables from its Results cell, with the date and the embedding model.

| Check | Hit rate | Recall@4 | MRR |
|---|---|---|---|
| TF-IDF, 250-character chunks | *pending run* | *pending run* | *pending run* |
| TF-IDF, 500-character chunks (baseline) | *pending run* | *pending run* | *pending run* |
| TF-IDF, 1,000-character chunks | *pending run* | *pending run* | *pending run* |
| Dense, 500-character chunks | *pending run* | *pending run* | *pending run* |
| Hybrid (RRF), 500-character chunks | *pending run* | *pending run* | *pending run* |

| Question | Answer |
|---|---|
| Baseline misses in the top 4 (of 25), and how many are `multi_hop` | *pending run* |
| Does a score threshold separate the out-of-corpus questions? | *pending run* |
| RAG or fine-tune | *pending the M45 verdict* |

Back to the module: [README.md](../README.md)
