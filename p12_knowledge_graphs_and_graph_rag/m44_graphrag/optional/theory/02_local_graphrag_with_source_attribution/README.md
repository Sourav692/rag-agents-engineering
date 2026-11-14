# M44.2 Theory: Local GraphRAG with source attribution

*[M44 theory](../../../mandatory/theory/README.md) · Lesson 44.2 · Notebooks: [`02a_graph_rag_local_attribution.ipynb`](../../notebook/02a_graph_rag_local_attribution.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Why a resolved citation marker is not evidence, and where an entity graph quietly overwrites the source it claims to keep -->
<!-- format: approved -->

## Start with a citation that supports nothing

> **What you'll learn**
>
> - **Explain** the difference between the route that found evidence and the passage that supports a claim.
> - **Trace** how the notebook turns `[N]` markers into citations, and what that check leaves out.
> - **Diagnose** provenance lost to overwrites and results hidden by a shared visited set.
> - **Choose** what to report when a local extraction model fails.

Lesson 44.1 walked a graph of similar chunks and ended on a log of seeds, edges and source spans. This lesson makes the last item explicit: every claim in the answer should point at the sentence that supports it.

Suppose the Larkspur assistant answers that exports stay available for 30 days after cancellation, and tags the claim `[1]`. Marker 1 resolves to a real handbook sentence. The sentence says that cancelling ends billing at the end of the period, which says nothing about exports. The answer looks cited and is unsupported. We call this **citation without support**.

## Source attribution

**Source attribution** links each generated claim to the exact source span that supports it, and keeps that link separate from the graph path that found the span. The optional notebook builds a local version: Ollama runs extraction and generation, `all-MiniLM-L6-v2` embeds entities, and a directed NetworkX graph holds the relationships.

Each record the notebook stores carries its provenance:

| Record | Fields that carry provenance | What it decides |
|---|---|---|
| Entity | source document, source sentence | Which sentence a node description came from |
| Relationship | relation type, source document, source sentence | Which sentence asserted the edge |
| Citation | claim, source document, source sentence, confidence, graph path | What the answer points at |

*Table 1: The notebook's data model, read from its dataclasses.*

At query time the notebook embeds the question, takes the 3 most similar entities as entry points, and follows outgoing edges breadth-first for up to 2 hops. For Larkspur, a path might run from Cancellation to Export to Snapshot. That path explains why retrieval reached the snapshot document. The policy claim still needs a passage that states when a snapshot export remains available.

```mermaid
flowchart TD
    E[Entity match] --> P[Relationship path]
    P --> S[Original source span]
    S --> C{Supports this claim?}
    C -->|Yes| A[Answer with reference]
    C -->|No| R[Retrieve or qualify]
```

*Figure 1: Route and support are separate checks. The path finds a span; only the span can support the claim.*

Keep two records for each generated claim: the route by which retrieval found evidence, and the exact passage used to support the claim. A traversable relation can be stale, wrongly extracted, or cut off from the conditions in the original text. Inspecting the source is how a reviewer rejects that relation.

## What the notebook verifies

We ran the notebook's ingestion, traversal and citation code with a scripted extraction (four Larkspur entities, four relations) and a scripted answer; no model was called. Step through how a marker becomes a citation:

<div class="walkthrough learning-widget" data-stepper id="citation-walkthrough">
<p class="widget-intro">Step through the notebook's citation path on the scripted Larkspur run.</p>
<div class="step-controls" hidden role="group" aria-label="Stages of citation resolution"><button type="button" data-step="0" aria-pressed="false" aria-controls="cite-step-0">1. Prompt</button><button type="button" data-step="1" aria-pressed="false" aria-controls="cite-step-1">2. Answer</button><button type="button" data-step="2" aria-pressed="false" aria-controls="cite-step-2">3. Markers</button><button type="button" data-step="3" aria-pressed="false" aria-controls="cite-step-3">4. Records</button></div>
<div class="step-panels"><section id="cite-step-0" class="step-panel" aria-labelledby="cite-heading-0"><h4 id="cite-heading-0">1. The prompt numbers the entities</h4><dl><dt>Context</dt><dd>retrieved entities as numbered lines of name and description</dd><dt>Not sent</dt><dd>the source sentences; they stay in the graph</dd></dl></section><section id="cite-step-1" class="step-panel" aria-labelledby="cite-heading-1"><h4 id="cite-heading-1">2. The model cites by number</h4><dl><dt>Scripted answer</dt><dd>one claim about exports tagged 1, one about snapshots tagged 3, and a stray marker 9</dd></dl></section><section id="cite-step-2" class="step-panel" aria-labelledby="cite-heading-2"><h4 id="cite-heading-2">3. A regular expression finds the markers</h4><dl><dt>Found</dt><dd>1, 3 and 9</dd><dt>Valid</dt><dd>1 and 3; 9 points past the three context items and is dropped without a warning</dd></dl></section><section id="cite-step-3" class="step-panel" aria-labelledby="cite-heading-3"><h4 id="cite-heading-3">4. Each valid marker becomes a record</h4><dl><dt>Attached</dt><dd>the stored source document and sentence, looked up after generation</dd><dt>Fields</dt><dd>confidence 0.9, a fixed constant; the claim field holds "Reference [N]", not the answer's sentence</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

Here is what the two resolved markers point at:

| Marker | Claim in the answer | Resolved sentence | Supports the claim |
|---|---|---|---|
| `[1]` | Exports stay available for 30 days | Cancelling ends billing at period end. | no |
| `[3]` | Snapshots last 30 days | Exports use the latest snapshot. | no |
| `[9]` | (see also) | none: dropped without a warning | not checked |

*Table 2: Citation resolution on a scripted run. Both resolved markers become citations with confidence 0.9.*

Nothing in the run noticed that neither resolved sentence supports its claim. The code demonstrates provenance storage and citation resolution. It does not check entailment, that is, whether the cited sentence actually implies the claim. A useful check splits the answer into claims, resolves each marker to a span, and asks whether the span supports the claim with its conditions and dates intact. Until that check passes, call the answer cited, not verified.

## Where provenance is lost

The graph keeps one source record per entity and one edge per ordered pair of entities. Both rules overwrite data silently. We call the pattern **last write wins**, and the same scripted run planted two cases:

| Planted case | What the graph kept | Why |
|---|---|---|
| An old FAQ re-extracts "export" after the policy page | The node now cites the old FAQ: "Exports are removed at cancellation." | Entity IDs hash the lowercased name, and a later write replaces the node's fields |
| Two relations from Export to Snapshot (uses, related to) | One edge, typed "related to"; 4 relations extracted, 3 edges stored | A directed graph allows one edge per ordered pair |
| A relation whose endpoint was never extracted as an entity | No edge | Edges are added only when both endpoints exist |

*Table 3: Overwrites and drops in the notebook's graph. The first two rows come from a scratchpad run of its ingestion code; the third is the guard in that code.*

The first row is the dangerous one. A stale FAQ sentence now contradicts the policy, and the traversal will cite it as the export node's source. Keep a list of source spans per entity, and a multigraph or a relation list when distinct relations between the same pair carry separate claims.

## Local execution boundaries

When the `ollama` package is not installed, the notebook's model helper returns an empty extraction rather than an error. An empty graph from that branch does not show that the documents contain no relationships. Report model availability and extraction failures separately from a legitimate zero-result retrieval.

The traversal has a subtler boundary. It shares one visited set across all seeds and processes them in order. A node already reached from an earlier seed is skipped when a later seed starts from it, along with everything beyond it. We ran the notebook's traversal over the same four entities with 2 hops, in both seed orders:

<div class="learning-widget evidence-switcher" data-comparison id="seed-order-switcher">
<p class="widget-intro">Choose a seed order to see which entities the 2-hop traversal returns.</p>
<div class="mode-controls" hidden role="group" aria-label="Seed order">
<button type="button" data-mode="cancel-first" aria-pressed="false" aria-controls="order-cancel-first">Cancellation first</button>
<button type="button" data-mode="snapshot-first" aria-pressed="false" aria-controls="order-snapshot-first">Snapshot first</button>
</div>
<section id="order-cancel-first" class="mode-panel" data-announcement="Cancellation first selected. Retention is missing."><h4>Cancellation, then Snapshot</h4><ul><li>Returned: Cancellation at depth 0, Export at 1, Snapshot at 2.</li><li>The Snapshot seed is already visited and its walk stops at once.</li><li>Retention, one hop from Snapshot, is missing.</li></ul></section>
<section id="order-snapshot-first" class="mode-panel" data-announcement="Snapshot first selected. Retention is returned."><h4>Snapshot, then Cancellation</h4><ul><li>Returned: Snapshot at depth 0, Retention at 1, Cancellation at 0, Export at 1.</li><li>Both seeds start from unvisited nodes.</li><li>Retention is returned.</li></ul></section>
<p class="switch-status" aria-live="polite"></p>
</div>

Retention is one hop from the Snapshot seed, well inside the budget, and still missing in the first order. We call this **seed-order shadowing**. When the required meaning is "within this many hops of any seed", store the best depth per node or run a true multi-source breadth-first search, which starts every seed at depth 0 together. Apply source access filters during traversal and again when building the context.

Lesson 44.3 moves from entity neighbourhoods to the whole corpus, where the evidence for an answer is a set of community summaries rather than a path.

## Limits of this evidence

- **No model was called.** Extraction and the answer were scripted; a live Ollama model may cite differently or skip markers altogether.
- **The planted cases are small.** Four entities and four relations show each failure once; they do not estimate how often a real corpus triggers it.
- **The support verdicts are ours.** Table 2's last column is a reading of each sentence, not the output of an entailment model.

## References

1. Bibin Prathap, [VeritasGraph](https://github.com/bibinprathap/VeritasGraph), the local, attributed GraphRAG project the notebook names as its model.
2. Gao et al., [Enabling Large Language Models to Generate Text with Citations](https://arxiv.org/abs/2305.14627), arXiv 2305.14627.
3. NetworkX, [DiGraph: directed graphs with self loops](https://networkx.org/documentation/stable/reference/classes/digraph.html).

## Key Takeaways

- Keep two records per claim: the graph route that found the evidence, and the exact passage that supports the claim. A traversable relation can be stale or wrongly extracted.
- Resolving `[N]` markers to sources proves provenance storage, not entailment. A fixed confidence of 0.9 is a constant; add a claim-to-span review before calling an answer verified.
- Report extraction failures separately from empty results, keep every source span and relation the graph would otherwise overwrite, and check that seed order cannot hide a result.

## Check yourself

<details>
<summary>1. A graph path runs from Cancellation to Export to Snapshot. Why record both that path and the exact passage behind each claim?</summary>

The path explains how retrieval reached the snapshot document; it does not support the policy claim. A traversable relation can be stale, wrongly extracted or cut off from the conditions in the original text. The source passage is what lets a reviewer check the claim, or reject the relation.

</details>

<details>
<summary>2. Each citation the notebook produces carries confidence 0.9. What does that number tell you about the answer?</summary>

Nothing measured: it is a fixed constant, and the claim field holds a reference label rather than the answer's claim. The code finds `[N]` markers and maps valid IDs back to source records, but it never checks that the cited sentence supports the claim. Add a claim-to-span review before treating an answer as verified.

</details>

<details>
<summary>3. After an old FAQ is ingested, answers about exports start citing it instead of the current policy. What in the graph caused that?</summary>

Entity IDs come from the lowercased name, so the FAQ's "export" maps to the same node as the policy's Export, and the later write replaces its description and source. This is last write wins. Keep a list of source spans per entity, with document versions, so a stale source can be filtered rather than silently substituted.

</details>

---
*Previous: [44.1 Concept-graph traversal](../../../mandatory/theory/01_concept_graph_traversal/README.md). Next: [44.3 Microsoft GraphRAG: communities, global vs local search](../../../mandatory/theory/03_microsoft_graphrag_communities_global_vs_local_search/README.md).*
