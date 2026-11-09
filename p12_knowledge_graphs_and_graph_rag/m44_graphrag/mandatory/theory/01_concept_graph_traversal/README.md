# M44.1 Theory: Concept-graph traversal

*[M44 theory](../README.md) · Lesson 44.1 · Notebooks: [`01a_graph_rag.ipynb`](../../notebook/01a_graph_rag.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: How a graph of similar chunks extends flat retrieval, and why a traversal that looks like Dijkstra can stop one hop short of the passage it needs -->

## Chunk graphs and traversal

> **What you'll learn**
>
> - **Explain** how a chunk graph is built from cosine similarity and shared concepts, and what its edge weight means.
> - **Trace** the notebook's priority-queue traversal and the completeness check that stops it.
> - **Diagnose** two traversal faults: an inverted seed priority and neighbours that are discovered but never expanded.
> - **Choose** the budgets and logs that make a traversal auditable.

[M43](../../../../m43_knowledge_graphs_neo4j/mandatory/theory/README.md) stored facts as typed nodes and relationships and queried them with Cypher. This module asks a different question: how can graph structure decide which passages reach the answer model?

Take a Larkspur Cloud customer who asks which export mechanism remains available after cancellation. The answer depends on three passages: the cancellation policy, the export options and the snapshot retention rule. Flat top-k retrieval scores each chunk against the question on its own, and the retention passage barely mentions cancellation. It can rank below a billing chunk that shares more words with the question.

A **chunk graph** is a graph whose nodes are text chunks and whose edges join chunks that are similar enough to be read together. Retrieval finds a few seed chunks, then walks the edges to collect neighbours that the question alone would not rank. The first notebook builds one over the first 10 pages of a climate-change PDF and walks it to answer a question.

The build runs in four stages:

| Stage | What the notebook does | What it produces |
|---|---|---|
| Split | Recursive splitter, 1,000 characters with 200 of overlap | 30 chunks from the 10 pages |
| Concepts | A structured LLM call per chunk, plus spaCy named entities (people, organisations, places, works) | A concept list per node |
| Embed and compare | One embedding per chunk, cosine similarity for every pair | 435 pair scores (30 × 29 / 2) |
| Link | An edge when cosine is strictly above 0.8 | Weighted, undirected edges |

*Table 1: The chunk-graph build. Chunk and pair counts come from running the notebook's loader and splitter in the scratchpad; no model was called.*

The comparison is quadratic. Doubling the corpus to 60 chunks would mean 1,770 pairs, and the concept stage costs one model call per chunk on top of the embeddings.

```mermaid
flowchart TD
    S[Similar chunks] --> T{Cosine above threshold?}
    T -->|Yes| W[Weight by similarity<br/>and shared concepts]
    T -->|No| X[No edge]
    W --> N[Expand toward new concepts]
```

*Figure 1: Edge creation. The threshold decides whether an edge exists; shared concepts only change its weight.*

Once a pair passes the threshold, the notebook weights the edge as 0.7 × cosine + 0.3 × the shared-concept fraction. The fraction divides the number of shared concepts by the size of the smaller concept set, and is zero when that set is empty. We ran the notebook's own weight function on four illustrative Larkspur chunk pairs:

| Edge | Cosine | Shared concepts | Smaller set | Weight |
|---|---|---|---|---|
| Cancellation policy, Export options | 0.86 | 1 | 3 | 0.702 |
| Cancellation policy, Billing cycle | 0.84 | 1 | 2 | 0.738 |
| Export options, Snapshot retention | 0.88 | 1 | 2 | 0.766 |
| Billing cycle, Outage status | 0.82 | 0 | 2 | 0.574 |

*Table 2: Edge weights from the notebook's weight function. Cosine scores and concept lists are illustrative inputs.*

The billing edge outweighs the export edge despite a lower cosine, because the billing chunk has a smaller concept list. The weight mixes two signals the notebook author chose. It has no calibrated meaning as a probability that one chunk supports the other.

> **Pitfall: the edge as evidence.** A cancellation chunk and an export chunk can share a product name while describing different dates or account states. An edge is a retrieval lead; read both passages before turning it into a policy statement.

At query time the notebook retrieves 5 chunks from FAISS and compresses each with an LLM extractor that keeps only the question-relevant sentences. To find each compressed span's place in the graph, it runs a second nearest-neighbour search with the compressed text and takes the closest stored chunk. That chunk may not be the one the span came from, and two chunks with identical text map to whichever node comes first. Stable chunk IDs carried through compression remove the guess.

## How the traversal runs

The notebook describes its walk as Dijkstra-like. Each seed enters a min-heap with priority 1 / score, where the score comes from the seed lookup. Popping a node adds its text to the context and asks the model whether the context now answers the question. If not, and the node brings concepts not seen yet, each neighbour gets a distance of the current priority plus 1 / edge weight.

The loop has one detail that changes its reach:

```mermaid
flowchart TD
    P[Pop lowest priority] --> V{Already in path?}
    V -->|yes| P
    V -->|no| A[Add text, check answer]
    A --> C{New concepts?}
    C -->|no| P
    C -->|yes| N["Neighbour closer:<br/>push, add text, check"]
    N --> P
```

*Figure 2: The traversal loop. A neighbour joins the path when it is discovered, so the pop that later reaches it is skipped.*

Read the right-hand branch closely. A neighbour's text is added, and the neighbour is recorded as visited, at the moment it is discovered. When the heap later pops that neighbour, the "already in path" test skips it, and its own neighbours are never examined. We call this **discovered but never expanded**: the walk reaches the seeds and their direct neighbours, and stops.

The seed priority has a second problem. LangChain's FAISS store returns L2 distance by default, where a lower score means a closer match. Dividing 1 by a distance gives the closest seed the largest priority, and the min-heap pops it last. We call this the **inverted seed priority**. A distance of exactly zero would also divide by zero.

We ran the notebook's traversal code on the five illustrative chunks from Table 2, with a stub vector store and a stub completeness check that answers "complete" once cancellation, export and retention are all in context:

| Order | Node | How it entered | Completeness check |
|---|---|---|---|
| 1 | Billing cycle | Seed at L2 0.70, priority 1.43 | incomplete |
| 2 | Outage status | Neighbour of billing | incomplete |
| 3 | Cancellation policy | Seed at L2 0.40, priority 2.50 | incomplete |
| 4 | Export options | Neighbour of cancellation | incomplete |

*Table 3: The notebook's traversal on a hand-built graph (scratchpad run, stub retrieval and stub answer check).*

The farther seed went first. Export options was added as a neighbour and later skipped when popped. Snapshot retention, two hops from the cancellation seed, never entered the context. The loop ended after four completeness calls and fell through to generating an answer from incomplete context. With the cancellation chunk as the only seed, the path was cancellation, export, billing: the same one-hop limit.

| Planted case | What the traversal did | Why |
|---|---|---|
| Two seeds at L2 0.40 and 0.70 | Expanded the farther seed first | 1 / distance inverts the order |
| Retention two hops from the seed | Never reached | Discovered neighbours are never expanded |
| A node whose concepts were all seen | No neighbours pushed | The new-concept test gates expansion |

*Table 4: Planted cases and their causes. The first two come from Table 3's run; the third is the gate in Figure 2.*

None of this makes the notebook useless as a teaching build. It shows the moving parts of graph-guided retrieval. It should not be described as an unmodified shortest-path search, and its reach should be measured before it is trusted with multi-hop questions.

## Budgets and stopping

The query engine sets a maximum context length of 4,000, but no branch of the traversal reads it. A variable named as a budget supplies no protection until code checks it. Count the accumulated context with the answer model's tokenizer and stop before an explicit limit. Cap visited nodes and completeness calls separately, since each check is a model call over the whole context so far.

The cost of checking grows with the walk:

| Nodes added | Completeness calls | Context sent per call |
|---|---|---|
| 1 | 1 | 1 chunk |
| 4 | 4 | 1, 2, 3, then 4 chunks |
| n | n | 1 + 2 + … + n chunks in total |

*Table 5: Completeness calls in the notebook's loop. Table 3's run made four calls over contexts of 1, 2, 3 and 4 chunks.*

At 1,000-character chunks, a walk that adds 10 nodes resends 55 chunks of text across its checks. That is the price of asking after every node.

An LLM saying "complete" is a stopping heuristic. For the cancellation question, check that the context holds the cancellation condition, the available export mechanism and the retention condition. If the graph has no path to one of those passages, report the missing evidence. More context cannot create a relation absent from the index.

For each query, log the seed IDs, the edges followed, the source spans retrieved, the context size and the stopping reason. Then compare against flat retrieval on the same golden questions. A longer traversal can add work while leaving the answer's supporting evidence unchanged, and lesson 44.2 turns that evidence into explicit citations.

## Key Takeaways

- A chunk graph joins chunks whose cosine passes a threshold and weights each edge by similarity and shared concepts. The weight is a retrieval lead, never a calibrated probability.
- Measure a traversal's reach before trusting it: the notebook's walk inverts its seed order on L2 distances and never expands the neighbours it discovers; it stops one hop out.
- A budget variable protects nothing until code checks it. Count context with the answer model's tokenizer, cap nodes and completeness calls separately, and treat "complete" as a heuristic.

## Check yourself

<details>
<summary>1. Two chunks have cosine similarity 0.85 and share 2 concepts, with 4 in the smaller concept set. What weight does their edge get, and what does that weight mean?</summary>

The edge exists because 0.85 is above the 0.8 threshold, and its weight is 0.7 × 0.85 + 0.3 × 0.5 = 0.745. The weight combines two signals the notebook author chose and is not a calibrated probability that either chunk supports the other. Treat the edge as a retrieval lead and read both passages.

</details>

<details>
<summary>2. The traversal sets max_context_length=4000. Does that stop the context from growing past 4000?</summary>

No. No branch of the traversal checks that attribute, so it supplies no protection. Count the accumulated context with the answer model's tokenizer and stop before an explicit budget, and cap visited nodes and completeness-check calls separately.

</details>

<details>
<summary>3. The snapshot retention chunk sits two edges from the cancellation seed, yet it never reaches the context. What in the traversal explains that?</summary>

The loop adds a neighbour to the path the moment it discovers it, and later skips that neighbour when it is popped, so its own neighbours are never examined. The walk reaches the seeds and their direct neighbours only. Log the path and measure reach on a question whose evidence is two hops away before relying on the traversal.

</details>

---
*Previous: [M44 overview](../README.md). Next: [44.2 Local GraphRAG with source attribution](../../../optional/theory/02_local_graphrag_with_source_attribution/README.md).*
