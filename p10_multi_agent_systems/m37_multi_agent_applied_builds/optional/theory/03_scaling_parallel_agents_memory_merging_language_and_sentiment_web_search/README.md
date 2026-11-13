# M37.3 Theory: Scaling: parallel agents, memory merging, language and sentiment, web search

*[M37 theory](../../../mandatory/theory/README.md) · Lesson 37.3 · Notebooks: [`03a_hotel_parallel_reservation_agents.ipynb`](../../notebook/03a_hotel_parallel_reservation_agents.ipynb) (optional), [`03b_hotel_merging_and_conversation_memory.ipynb`](../../notebook/03b_hotel_merging_and_conversation_memory.ipynb) (optional), [`03c_hotel_guest_language_and_sentiment.ipynb`](../../notebook/03c_hotel_guest_language_and_sentiment.ipynb) (optional), [`03d_hotel_web_search_integration.ipynb`](../../notebook/03d_hotel_web_search_integration.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Fan out to parallel agents, merge their answers into one reply, and fold old turns into a summary the thread keeps -->
<!-- format: approved -->

## Start with two replies to one question

> **What you'll learn**
>
> - **Explain** what parallel branches need before their answers can come back together: a reducer, a key per branch and a join.
> - **Trace** two hotels' answers through a merge that writes one reply in priority order.
> - **Compare** trimming old turns with summarizing them into state.
> - **Diagnose** a sentiment score that reads raw foreign-language text as neutral.

Lesson 37.2 hardened the single-hotel desk. Now the chain has two hotels. Hotel 1 has rooms 101 to 104 and Hotel 2 rooms 105 to 108, each in its own database with its own read-only SQL tools. A guest asking for a Deluxe room should hear about both.

Wire the two hotel agents naively and the guest gets two replies, the first one missing a hotel. Or one hotel's agent answers from the other hotel's database, and nothing in the reply says so. Both failures come from how the branches' outputs come back together.

## Memory merging

**Memory merging** is the work of bringing several agents' outputs back into one state: the answers of parallel branches into one reply, and old turns into something smaller than the full transcript. The shape that works:

```mermaid
flowchart LR
    C[Coordinator] --> M["Mapper<br/>copies the conversation"]
    M --> A1["Hotel 1 assistant<br/>messages_hotel1"]
    M --> A2["Hotel 2 assistant<br/>messages_hotel2"]
    A1 <--> T1[(Hotel 1 tools)]
    A2 <--> T2[(Hotel 2 tools)]
    A1 --> D1[hotel1_done]
    A2 --> D2[hotel2_done]
    D1 --> J["Merge<br/>by priority"]
    D2 --> J
    J --> R[/One reply/]
```

*Figure 1: Fan-out to two hotel assistants, each with its own message key and tools, then a join and one merge.*

### Four wiring attempts

The build reaches that shape in steps, and each failure is a LangGraph rule. Its stub graphs need no model. We reran them offline with the notebook's own cells; Hotel 1's stub takes two tool rounds and Hotel 2's one, as real agents rarely take the same number of steps.

<div class="walkthrough learning-widget" data-stepper id="wiring-walkthrough">
<p class="widget-intro">Follow the stub request "Any Deluxe rooms?" through each wiring. Each stage shows what the run printed and the rule it teaches.</p>
<div class="step-controls" hidden role="group" aria-label="Wiring attempts"><button type="button" data-step="0" aria-pressed="false" aria-controls="wiring-step-0">1. Plain key</button><button type="button" data-step="1" aria-pressed="false" aria-controls="wiring-step-1">2. Shared list</button><button type="button" data-step="2" aria-pressed="false" aria-controls="wiring-step-2">3. No join</button><button type="button" data-step="3" aria-pressed="false" aria-controls="wiring-step-3">4. Join</button></div>
<div class="step-panels"><section id="wiring-step-0" class="step-panel" aria-labelledby="wiring-heading-0"><h4 id="wiring-heading-0">1. Two nodes write one plain key</h4><dl><dt>Wiring</dt><dd>Both hotel nodes run in the same step and write <code>last_writer</code></dd><dt>Run printed</dt><dd><code>InvalidUpdateError</code>: the key can receive only one value per step</dd><dt>Rule</dt><dd>A key written by parallel nodes needs a reducer, such as list concatenation. With one, both values are kept.</dd></dl></section><section id="wiring-step-1" class="step-panel" aria-labelledby="wiring-heading-1"><h4 id="wiring-heading-1">2. Both tool loops share one message list</h4><dl><dt>Wiring</dt><dd>Each hotel has a tool node with a same-named <code>list_rooms</code> tool, both on <code>messages</code></dd><dt>Run printed</dt><dd>Hotel 1's call never got a result. Hotel 2's agent received both results, one from Hotel 1's rooms.</dd><dt>Rule</dt><dd>One message key per branch, for the tool node and for the condition that routes to it</dd></dl></section><section id="wiring-step-2" class="step-panel" aria-labelledby="wiring-heading-2"><h4 id="wiring-heading-2">3. Separate keys, each branch wired to the merge</h4><dl><dt>Wiring</dt><dd><code>messages_hotel1</code> and <code>messages_hotel2</code>; each agent's "finished" edge goes straight to the merge node</dd><dt>Run printed</dt><dd>The merge ran twice: first with Hotel 1 unfinished, then again with both finished</dd><dt>Rule</dt><dd>A conditional edge fires the merge every time any branch reaches it</dd></dl></section><section id="wiring-step-3" class="step-panel" aria-labelledby="wiring-heading-3"><h4 id="wiring-heading-3">4. Sync nodes and a join edge</h4><dl><dt>Wiring</dt><dd>Each branch ends in a <code>*_done</code> sync node; one edge from both sync nodes leads to the merge</dd><dt>Run printed</dt><dd>The merge ran once, with both branches finished</dd><dt>Rule</dt><dd>A join waits for every listed node. The sync node exists because the agent node itself also runs mid-loop.</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

The shared-key failure is the dangerous one. A tool node answers the latest tool call in its list, which may belong to the other branch. With the real SQL tools both hotels have a tool called `run_query`, and the wrong database answers without any error. Call it **crossed tool results**.

Two more choices keep the branches honest. Both assistants come from one factory, which binds each to its own hotel's tools; copying the first assistant to make the second is how Hotel 2's agent ends up reading Hotel 1's database. And the branches cannot book. Both run the same request at the same time, and a booking tool in each would create two reservations. They report availability and prices; booking waits until the guest picks a hotel.

### Merging by priority

The merge itself is an agent. It reads the guest's request and each hotel's final answer, listed in a fixed priority order (Hotel 1, then Hotel 2), and writes one reply under three rules:

1. Recommend the first hotel that can help and offer the other as an alternative.
2. Ignore a hotel that cannot help, unless none can.
3. Keep room numbers, prices and dates exactly as the assistants gave them.

Only the merged reply enters the shared conversation; each branch's tool calls stay in its own key. The two test turns:

| Guest asks | Ground truth from SQLite | The reply should |
|---|---|---|
| A Deluxe room in two months | Hotel 1 room 104, Hotel 2 room 108 | Name 104 before 108 |
| The Family Suite during Bob's stay | None free: Hotel 1 has no Family Suite, Hotel 2's is booked | Say plainly that none is free |

*Table 1: The merge's two test turns and the ground truth each is checked against.*

Code checks the first case by the position of the room numbers in the reply, against free rooms computed from the databases, never against the model's claim.

### Two ways to shrink the thread

Every turn now adds several agent messages to the thread. Something has to keep it small, and the two options differ in what they lose. **Trimming**, from M33, changes only what the model sees on one call:

```mermaid
flowchart TB
    S[("Stored thread<br/>every message kept")] --> W["Trim on read<br/>last messages only"]
    W --> L[Model call]
```

*Figure 2: Trimming. The thread keeps everything; old turns drop out of the model's view.*

**Summarizing into state** changes what the thread stores. A summarize node runs at the start of each turn when the stored conversation has more than 6 messages:

1. It keeps the last guest turn word for word; everything before it is old. The cut is always at a guest message, so no tool call is separated from its result.
2. It asks the model to fold the old messages into a running `summary` field, keeping every concrete fact: names, room types and numbers, prices, dates, what was offered and refused.
3. It returns a removal marker for each old message id, and the message reducer deletes them.

```mermaid
flowchart TB
    S[("Stored thread<br/>over 6 messages")] --> F["Summarize node<br/>fold old turns"]
    F --> Y[("summary field")]
    F --> D["Remove old<br/>messages by id"]
    Y --> L["Model call<br/>summary as system message"]
```

*Figure 3: Summarizing into state. Old turns become a summary, and the messages themselves are deleted.*

The summary reaches the coordinator's and assistants' prompts as a system message, never the guest's reply. The new graph continues the same thread because both graphs share one checkpointer.

<div class="learning-widget evidence-switcher" data-comparison id="shrink-switcher">
<p class="widget-intro">The test turn asks <em>Remind me: which Deluxe room did you recommend, and at what price?</em> after the recommendation has fallen out of the recent messages. Compare what each option leaves the model (illustrative).</p>
<div class="mode-controls" hidden role="group" aria-label="How the thread shrinks">
<button type="button" data-mode="trim" aria-pressed="false" aria-controls="shrink-trim">Trimming</button>
<button type="button" data-mode="summary" aria-pressed="false" aria-controls="shrink-summary">Summarizing into state</button>
</div>
<section id="shrink-trim" class="mode-panel" data-announcement="Trimming. The answer is stored but outside the model's view."><h4>Trimming</h4><ul><li>Cost: no model call.</li><li>The recommendation is still stored, but outside the window the model sees.</li></ul><p>The model cannot name the room. Facts outside the window are forgotten for this call.</p></section>
<section id="shrink-summary" class="mode-panel" data-announcement="Summarizing into state. The answer comes from the summary, if it kept the fact."><h4>Summarizing into state</h4><ul><li>Cost: one model call when the thread passes 6 messages.</li><li>The recommendation message is deleted; its room and price survive only inside <code>summary</code>.</li></ul><p>The model answers from the summary. A fact the summary left out is gone for good.</p></section>
<p class="switch-status" aria-live="polite"></p>
</div>

Call the summarizer's risk **lossy folding**: a fact it drops cannot be recovered from the thread. That is why its prompt lists the fact types to keep, and why the test asks for a specific room and price.

## Adding agents around the core

The last two builds add capabilities without changing the coordinator, the checker or the reservation agent. Each adds its capability to the core from lesson 37.1 on its own; no build composes all of them into one graph.

```mermaid
flowchart LR
    G[/Guest message/] --> TI["translate_in<br/>to English"]
    TI --> SA["sentiment<br/>score"]
    SA --> C["Coordinator<br/>and specialists"]
    C --> TO["translate_out<br/>guest language"]
    TO --> R[/Reply/]
```

*Figure 4: The language and sentiment build. Translation wraps the core, and the coordinator reads the sentiment score.*

### Language and sentiment

The inbound node detects the guest's language and replaces the message with an English version, using one structured-output call for the language code and the text. A sentiment node then scores the English text with TextBlob's word lexicon. The coordinator adds a de-escalation instruction only when the message reads as negative, and the outbound node translates the final reply back.

The language is a per-thread state field. A global language variable breaks the moment two guests write at once, which is a form of **shared global state** across threads.

The order of translation and scoring matters, because the lexicon is English-only and word-level. We reran the build's own `analyse()` on its sample reviews, raw and untranslated, with its thresholds of -0.1 and +0.1:

| Text | Human label | Lexicon label | Polarity | Words scored |
|---|---|---|---|---|
| The service is terrible and the room was dirty. | negative | negative | -0.80 | terrible, dirty |
| Die Bedienung ist schrecklich und das Zimmer war schmutzig. | negative | neutral | 0.00 | none |
| Le service est horrible et la chambre était sale. | negative | negative | -1.00 | horrible |
| Das Personal war wunderbar und das Frühstück war köstlich. | positive | neutral | 0.00 | personal |
| Le personnel était merveilleux et le petit-déjeuner délicieux. | positive | neutral | 0.00 | none |
| Great, another cold shower. Just what I needed. | negative | positive | +0.10 | great, cold |

*Table 2: TextBlob on raw text, from the build's sample reviews.*

Raw German scores nothing, so an angry German guest never triggers de-escalation. The French complaint is caught only because "horrible" is also an English word. Sarcasm fools the lexicon in English too. Scoring the translation fixes the first problem and leaves the sarcasm.

### Web search

A web search assistant with Tavily, capped at 3 results per search, answers questions about the neighbourhood, which no hotel database holds. It is one more tool loop and one more name the coordinator can route to. The test checks which node ran for a nearby-places question and for a booking question.

## Larkspur in two regions

Larkspur runs billing in two regions, each with its own database. The same rules carry over:

1. A question about plan prices fans out to both regional agents, each with its own message key and read-only tools.
2. A join waits for both, and the merge answers in a fixed region order, keeping figures exactly as each agent gave them.
3. Any refund or plan change happens once, after the customer picks a region, never inside a branch.
4. Long support threads fold into a summary that must keep account ids, amounts and dates, and a test asks for one of them after the fold.

Lesson 37.4 swaps the hotel agents for a research team and asks who decides which agent runs next.

## Limits of this evidence

- **Stubs prove wiring, not answers.** The four wiring attempts and the TextBlob scores were rerun offline from the notebooks' own cells. The merged replies, the summaries and the translations need an OpenAI key, and the web search a Tavily key; their wording varies by run.
- **The priority check is positional.** Code checks that room 104 appears before 108 in the reply. It does not check that the prices or dates in the reply match the databases.
- **One lexicon, a handful of samples.** Table 2 shows six of the build's seven short reviews (the seventh, an English compliment, scores positive), scored by TextBlob's English pattern lexicon. It shows the failure; it does not measure how often translation fixes it.

## References

1. [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), for reducers, parallel branches and join edges.
2. [LangGraph: add and manage memory](https://docs.langchain.com/oss/python/langgraph/add-memory), for trimming and summarizing messages.
3. [TextBlob documentation](https://textblob.readthedocs.io/en/dev/), for the pattern analyser's polarity and assessments.
4. [Tavily documentation](https://docs.tavily.com), for the search API behind the web search assistant.

## Key Takeaways

- Parallel branches need a reducer on any key they share, a separate message key per tool loop and a join that waits for every branch. Without the join, the merge runs once per branch.
- Keep branches read-only when they run the same request at once, and merge their answers by a fixed priority. Check the merged reply against ground truth from the database, never the model's claim.
- Summarizing into state deletes old turns and keeps a running summary, at one model call when the thread passes its limit. Facts the summary leaves out are gone for good, where trimming only hides them.

## Check yourself

<details>
<summary>1. Why does each parallel hotel branch need its own message key instead of sharing one message list?</summary>

A tool node answers the latest tool call in its list, which may be the other branch's. Both hotels have a tool called `run_query`, and the wrong database can answer with no error. In the stub run one branch's call never got a result while the other branch received both.

</details>

<details>
<summary>2. For a Deluxe room in two months, Hotel 1 has room 104 free and Hotel 2 has room 108. What should the merged reply say, and how is it checked?</summary>

It should recommend Hotel 1 first, because Hotel 1 comes first in the priority order, and offer Hotel 2 as the alternative with numbers, prices and dates exactly as the assistants gave them. Code checks that 104 appears before 108 in the reply, against free rooms computed from the databases, never against the model's claim.

</details>

<details>
<summary>3. In the two-hotel graph, the guest gets two replies and the first one misses a hotel. What is wrong with the wiring?</summary>

Each branch's end goes straight to the merge node, and a conditional edge fires the merge every time any branch arrives. Add a sync node at the end of each branch and a join edge from both sync nodes to the merge, which then waits for both.

</details>

---
*Previous: [37.2 Hardening: edge cases, testing and system-wide error handling](../../../mandatory/theory/02_hardening_edge_cases_testing_and_system_wide_error_handling/README.md). Next: [37.4 Research systems: supervisor financial research, summarisation, full research system](../../../mandatory/theory/04_research_systems_supervisor_financial_research_summarisation_full_research_system/README.md).*
