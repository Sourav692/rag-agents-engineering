# M30.1 Theory: Router agentic RAG over multiple knowledge bases

*[M30 theory](../README.md) · Lesson 30.1 · Notebooks: [`01a_router_agentic_rag.ipynb`](../../notebook/01a_router_agentic_rag.ipynb), [`01b_router_agentic_rag_modular.ipynb`](../../../optional/notebook/01b_router_agentic_rag_modular.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: A closed label set, an exact filter, and a fallback for the routes the classifier gets wrong -->
<!-- format: approved -->

## Start with a ticket sent to the wrong knowledge base

> **What you'll learn**
>
> - **Explain** why a router's output must come from a closed label set, and what breaks when it does not.
> - **Trace** a support ticket from its label to the metadata filter that limits retrieval.
> - **Diagnose** a silent misroute, a case mismatch and a shared-filter race.
> - **Choose** a confidence floor for an all-knowledge-base fallback, and say what it costs.

M17 introduced routing as one step inside a retrieval pipeline. This module moves the router to the front of the whole graph, and its decision limits everything that runs after it.

A Larkspur customer writes *How long do you keep my data after I cancel?* The retention policy sits in the general knowledge base. The router reads "data", calls the ticket technical, and retrieval searches only the technical chunks. It finds the data-export chunk or nothing, and the customer gets a confident wrong answer or an apology.

Nothing raised an error. The router chose where retrieval was allowed to look, and the answer was somewhere else. That one failure sets three jobs:

- **Classify**: turn free text into one label from a fixed set.
- **Filter**: turn the label into the exact metadata value the index stores.
- **Hedge**: decide what to do when the router is unsure.

Every router in this module has the same skeleton:

```mermaid
flowchart LR
    T[/Ticket/] --> C["Classifier<br/>closed labels"]
    C --> L["Label to<br/>filter value"]
    L --> R["Filtered<br/>retrieval"]
    R --> A[/Answer/]
```

*Figure 1: The router skeleton. Each arrow is a place where the ticket can be sent the wrong way without an error.*

## Query classification

**A router is a classifier whose output decides where a question goes.** In the 01a notebook it is one LLM call with structured output: the model must fill a schema whose only field is the category, and the field's type lists the three allowed values, Technical, Billing and General.

That type is what makes the label set **closed**. The parser accepts only those three strings, and the routing function downstream can compare against them with no defensive parsing:

| Model output | What the schema does | What reaches the router |
|---|---|---|
| `Billing` | Accepts it | Billing |
| `billing` | Rejects it with a literal error | Nothing; the call fails before routing |

*Table 1: A closed label set rejects a near-miss before the router sees it.*

The prompt gives each label a one-line definition, such as "Billing queries will focus more on payment and purchase related aspects". Those definitions are the router's whole specification. A ticket that fits two of them gets whichever label the model leans toward that day.

### Six routers, one shape

Every M30 lesson puts a classifier of this kind in front of something:

| Router | Labels | Field type | What the label decides |
|---|---|---|---|
| General support (30.1) | Technical, Billing, General | Closed | Which knowledge base filter to apply |
| General support (30.1) | Positive, Neutral, Negative | Closed | Escalate to a human or answer |
| Clinic (30.2) | Billing, Appointments, Records, Insurance | Closed | Which department's documents to search |
| Clinic (30.2) | Positive, Neutral, Negative, Distress | Closed | Human support, on-call team or answer |
| Source (30.3) | vectordb, web_search | Closed | Vector store or web search |
| Strategy (30.4) | Factual, Analytical, Opinion, Contextual | Free text | Which retrieval strategy runs |

*Table 2: The M30 routers. Five close their label set; one does not.*

The last row breaks. The strategy router's value is a key into a table of four strategies, and `factual` or `Factual query` fails the lookup with a key error. We call this an **open label set**: the classifier may say something the code has no branch for. A closed field turns the same mistake into a rejected parse, which you can retry or default.

The 01a notebook classifies category and sentiment in two sequential LLM calls. One call with a two-field schema, as in the lab solution, halves the classification cost; two prompts are easier to test separately. Either way, keep the labels you route on in the schema, never in free text you parse afterwards.

An LLM classifier is **logical routing** in M17's terms. **Semantic routing** instead compares the question with example text for each route and takes the closest; this page's lab uses it with TF-IDF, because its scores can be checked exactly.

## Multi-KB routing

**Multi-KB routing means each label selects a different knowledge base, and retrieval sees only that one.** In the notebook, the three knowledge bases are not three stores. They are one Chroma collection, compared by cosine distance, where every document carries a `category` field in its metadata. A response node sets a metadata filter on that field, and the retriever returns at most three chunks scoring 0.2 or more. The clinic notebook in lesson 30.2 notes the other design, one vector store per category. Both trust the label equally.

### The label must match the stored value

Chroma compares metadata values exactly. The classifier returns `Technical` and the documents store `technical`, and each response node lowercases the label first. The notebook runs the refund question under three filters:

| Filter value | What the search can return | Why |
|---|---|---|
| `general` | The refund chunks | Matches the stored value |
| `General` | Nothing | Capital G matches no document |
| `technical` | Whatever clears 0.2 among technical chunks, or nothing | This is what a misroute retrieves |

*Table 3: The refund question under three filters.*

Lowercasing works only while labels and stored values differ by case alone; lesson 30.2 needs an explicit mapping.

### Trace the retention ticket through the router

The [interactive lab](interactive/kb-router-lab.html) routes eighteen Larkspur tickets with TF-IDF (scikit-learn's weighting, the M10 lab's index). Each knowledge base is scored by its best chunk, and the ticket goes to the highest. Follow the retention ticket:

<div class="walkthrough learning-widget" data-stepper id="route-walkthrough">
<p class="widget-intro">Follow the retention ticket from its scores to the answer. Each stage shows what the router knows and what retrieval can reach.</p>
<div class="step-controls" hidden role="group" aria-label="Routing stages"><button type="button" data-step="0" aria-pressed="false" aria-controls="route-step-0">1. Score</button><button type="button" data-step="1" aria-pressed="false" aria-controls="route-step-1">2. Route</button><button type="button" data-step="2" aria-pressed="false" aria-controls="route-step-2">3. Floor</button><button type="button" data-step="3" aria-pressed="false" aria-controls="route-step-3">4. Retrieve</button><button type="button" data-step="4" aria-pressed="false" aria-controls="route-step-4">5. Answer</button></div>
<div class="step-panels"><section id="route-step-0" class="step-panel" aria-labelledby="route-heading-0"><h4 id="route-heading-0">1. Score each knowledge base</h4><dl><dt>Billing</dt><dd>0.232, from the cancel chunk</dd><dt>Technical</dt><dd>0.320, from the export chunk, through the word "data"</dd><dt>General</dt><dd>0.184, from the retention chunk, which says "cancelled", not "cancel"</dd></dl></section><section id="route-step-1" class="step-panel" aria-labelledby="route-heading-1"><h4 id="route-heading-1">2. Pick the best label</h4><dl><dt>Label</dt><dd>Technical, the highest of the three</dd><dt>Correct label</dt><dd>General</dd><dt>Error raised</dt><dd>None</dd></dl></section><section id="route-step-2" class="step-panel" aria-labelledby="route-heading-2"><h4 id="route-heading-2">3. Check the confidence floor</h4><dl><dt>Floor</dt><dd>0.01</dd><dt>Decision</dt><dd>0.320 clears it, and the route stands</dd><dt>Logged</dt><dd>The label, the score and the chunks</dd></dl></section><section id="route-step-3" class="step-panel" aria-labelledby="route-heading-3"><h4 id="route-heading-3">4. Retrieve with the filter</h4><dl><dt>Filter</dt><dd>category equals technical, passed with this search call</dd><dt>Reachable chunks</dt><dd>sizing, reboot, export, incidents. The retention chunk is outside the filter.</dd></dl></section><section id="route-step-4" class="step-panel" aria-labelledby="route-heading-4"><h4 id="route-heading-4">5. Answer</h4><dl><dt>Result</dt><dd>How to export data, with no word on the 30-day retention window</dd><dt>Where it shows</dt><dd>A reopened ticket in the per-route signals</dd><dt>Fix</dt><dd>Add the ticket to a labelled routing set; give the general route an example retention ticket, or use embeddings that match "cancel" to "cancelled"</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

### Planted failure: the silent misroute

Filtered to the wrong knowledge base, the retriever behaves correctly: it returns whatever clears the threshold there, or nothing, and with no chunks the prompt makes the model apologise. Nothing records that the route was wrong. We call this a **silent misroute**, the default failure of every router in this module. It shows up only downstream: empty retrievals, apology answers, reopened tickets.

### Planted failure: the shared-filter race

The notebook writes the filter onto the retriever object itself, which every request shares. Two requests served at the same time can overwrite each other's filter, and a billing ticket can retrieve technical chunks. We call this the **shared-filter race**. The fix is to pass the filter with each search call, which the LangChain retriever merges over its defaults, and leave the shared object unchanged.

The optional modular notebook binds one response function to all three response nodes, turning three prompts into one template. A fourth knowledge base then needs one prompt entry, one node and one routing branch.

## Giving an uncertain route a fallback

The notebook's schema has no "unsure" label, and its classifier must always answer, as in Figure 1. A router that can abstain needs a confidence score and a rule for what happens below it:

```mermaid
flowchart LR
    T[/Ticket/] --> C{"Best KB score<br/>at or above floor?"}
    C -- yes --> F["Search one KB<br/>filter: category"]
    C -- no --> A["Search all three<br/>no filter"]
```

*Figure 2: The confidence floor. Below it, the ticket searches every knowledge base.*

A fallback always includes the right knowledge base but costs three searches instead of one. The lab's four presets show the trade:

<!-- lab: interactive/kb-router-lab.html -->

<div class="learning-widget evidence-switcher" data-comparison id="floor-switcher">
<p class="widget-intro">Pick a floor and see what happens to the eighteen lab tickets.</p>
<div class="mode-controls" hidden role="group" aria-label="Confidence floor">
<button type="button" data-mode="f000" aria-pressed="false" aria-controls="floor-f000">0.00, always route</button>
<button type="button" data-mode="f001" aria-pressed="false" aria-controls="floor-f001">0.01</button>
<button type="button" data-mode="f030" aria-pressed="false" aria-controls="floor-f030">0.30</button>
<button type="button" data-mode="f042" aria-pressed="false" aria-controls="floor-f042">0.42</button>
</div>
<section id="floor-f000" class="mode-panel" data-announcement="Floor 0.00 selected. Three misroutes, no fallbacks."><h4>Floor 0.00: always route</h4><ul><li>3 misrouted, 0 fall back, 15 of 18 reach the right knowledge base.</li><li>1.00 searches per ticket.</li></ul></section>
<section id="floor-f001" class="mode-panel" data-announcement="Floor 0.01 selected. Two misroutes, one fallback."><h4>Floor 0.01</h4><ul><li>2 misrouted, 1 falls back, 16 of 18 reach the right knowledge base.</li><li>1.11 searches per ticket. The dashboard ticket, which matched nothing, now searches all three.</li></ul></section>
<section id="floor-f030" class="mode-panel" data-announcement="Floor 0.30 selected. Two misroutes, four fallbacks."><h4>Floor 0.30</h4><ul><li>2 misrouted, 4 fall back, 16 of 18 reach the right knowledge base.</li><li>1.44 searches per ticket. Three correct tickets fall back and no new misroute is caught.</li></ul></section>
<section id="floor-f042" class="mode-panel" data-announcement="Floor 0.42 selected. No misroutes, eleven fallbacks."><h4>Floor 0.42</h4><ul><li>0 misrouted, 11 fall back, 18 of 18 reach the right knowledge base.</li><li>2.22 searches per ticket. Eight correct tickets pay for the fallback.</li></ul></section>
<p class="switch-status" aria-live="polite"></p>
</div>

The three misroutes at floor 0.00 fail for three different reasons:

| Ticket | Routed to, score | Why it misroutes | Smallest floor that catches it |
|---|---|---|---|
| *The dashboard keeps logging me out.* | Billing, 0.000 | Shares no term with any chunk; billing is first in the list | Any floor above zero |
| *How long do you keep my data after I cancel?* | Technical, 0.320 | "data" matches the export chunk; the retention chunk scores 0.184 | 0.32, when three correct tickets also fall back |
| *My server went down for an hour. Will I be compensated?* | Technical, 0.416 | Reduces to the single word "server" once stop words go ("down" is one), exactly like *How do I restart a server that stopped responding?* | None that spares the right ones: at 0.42, 8 correct tickets fall back with it |

*Table 4: Three misroutes, three causes.*

The first row is a **no-signal route**, and its score says so. The third is a **confident misroute**: it scores as high as a correct route, and the router's own confidence cannot find it.

> **Key distinction:** a floor removes no-signal routes cheaply. Confident misroutes need a better classifier (embeddings, an LLM, or several example tickets per route) and a labelled routing set to find them.

## Choosing a router and a floor

The decisions on this page reduce to a short sequence:

```mermaid
flowchart TD
    S[New router] --> L{"One label<br/>per ticket?"}
    L -->|yes| C[Closed schema field]
    L -->|no| D["Multi-label schema<br/>or decompose, M17"]
    C --> F{"Can it score<br/>its confidence?"}
    F -->|yes| FL["Floor plus<br/>all-KB fallback"]
    F -->|no| LR[Labelled routing set]
```

*Figure 3: Close the labels first, then decide how to catch the misroutes.*

| | Always route | Floor and fallback | Better classifier |
|---|---|---|---|
| Searches per ticket | 1 | 1.11 to 2.22 in the lab | 1 |
| Catches no-signal routes | No | Yes | Sometimes |
| Catches confident misroutes | No | Only at high cost | Yes, if the labelled set shows it |
| Main risk | Silent misroute | Fallback swallows correct routes | Cost of labelling and evaluating |

*Table 5: Three ways to live with misroutes.*

The two combine: a low floor such as 0.01 catches tickets that match nothing, and the labelled set shows which confident routes need a better classifier.

## Limits of this evidence

- **TF-IDF stands in for the LLM.** The lab routes by TF-IDF similarity so its scores can be checked against scikit-learn. The notebook's LLM classifier will misroute different tickets.
- **Eighteen hand-written tickets.** The floor numbers describe this set, not a production ticket mix.
- **No recorded notebook run.** Notebooks ship without outputs; Table 3 follows from Chroma's exact-match filter, not from a logged run.

## References

1. scikit-learn, [`TfidfVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), the weighting the lab reproduces.
2. LangChain, [Structured outputs](https://python.langchain.com/docs/concepts/structured_outputs/), the schema-bound call behind a closed label set.

## Key Takeaways

- Close the router's label set in its output schema, and code never meets a value it cannot handle. The prompt's one-line label definitions are the router's whole specification.
- Map each label to its exact stored metadata value and pass the filter per call, not onto a shared retriever. A silent misroute leaves no trace, because the wrong knowledge base just returns weaker chunks or none.
- A confidence floor with an all-KB fallback catches no-signal routes, in the lab for 0.11 extra searches per ticket. Confident misroutes need a better classifier and a labelled routing set.

## Check yourself

<details>
<summary>1. Why can the query-type classifier crash on a label such as factual, while the knowledge-base classifier never returns a label the code cannot handle?</summary>

The knowledge-base classifier's field lists the three allowed values, so the parsed output can only be Technical, Billing or General. The query-type classifier's field is free text used as a key into a table of strategies, so `factual` or `Factual query` fails the lookup and crashes the request. A closed field turns the same mistake into a rejected parse instead.

</details>

<details>
<summary>2. The outage-compensation ticket scores 0.416 for technical, the same as a genuine restart ticket. Can a confidence floor catch this misroute?</summary>

Not without heavy cost. Once stop words are removed both tickets reduce to "server", so they score the same and no floor separates them; catching it at 0.42 sends 8 correct tickets to the fallback too. It is a confident misroute, so it needs a better classifier and a labelled routing set, since the router's own score cannot find it.

</details>

<details>
<summary>3. Under load, two requests sometimes retrieve from each other's knowledge base. What in the notebook causes this, and what is the fix?</summary>

The notebook writes the category filter onto the shared retriever object, so concurrent requests overwrite each other's filter: the shared-filter race. Pass the filter with each search call instead, which the retriever merges over its defaults, and leave the shared object unchanged.

</details>

---
*Previous: [M30 overview](../README.md). Next: [30.2 Customer-facing routing with sentiment and human escalation](../../../optional/theory/02_customer_facing_routing_with_sentiment_and_human_escalation/README.md).*
