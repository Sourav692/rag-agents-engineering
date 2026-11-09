# M31.1 Theory: RAG as a tool inside a LangGraph agent

*[M31 theory](../README.md) · Lesson 31.1 · Notebooks: [`01a_rag_as_tool_in_agents.ipynb`](../../notebook/01a_rag_as_tool_in_agents.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Who decides to search, what the model reads before it does, and how to measure a tool description -->

## Agent-decided retrieval

> **What you'll learn**
>
> - **Compare** a graph where the pipeline decides to retrieve with one where the model decides through a tool call.
> - **Explain** what a retriever tool hands back to the model, and why the sources go missing.
> - **Measure** tool descriptions on a routing golden set and on held-out questions.
> - **Diagnose** the planted routing failures: a vocabulary miss, a scope gap and an overfitted description.

M22 built the agent loop, and [M30](../../../../m30_adaptive_rag_routing/mandatory/theory/README.md) routed questions inside a fixed graph where code decided whether to retrieve. This lesson puts the retriever inside the loop and hands that decision to the model.

A Larkspur customer asks *How long does a refund take?* The support agent has a `handbook_search` tool, and the handbook says refunds take 5 to 10 business days. The agent gives a confident, generic answer with no citation: the trace shows one model call and no tool call.

Two things can cause it: the graph gave the model the decision and the model declined it, or the description gave the model no reason to pick the tool. This page takes them in that order.

### Two graphs over one retriever

The notebook builds two graphs over one retriever: four short documents about a fictional cafe in Chroma, searched with `k = 2`. In the first, the pipeline decides. A classifier node, `topic_decision`, asks the model a yes or no question with structured output, and a conditional edge sends the question either to `retrieve` and `generate_answer` or to a fixed off-topic reply:

```mermaid
flowchart LR
    Q[/Question/] --> C{"topic_decision<br/>on topic?"}
    C -- yes --> R[retrieve] --> G[generate_answer]
    C -- no --> O["off_topic_response<br/>fixed message"]
```

*Figure 1: The pipeline decides. Every on-topic question is retrieved exactly once, with the user's words as the query.*

### The model decides

**Agent-decided retrieval** means the retriever is one of the model's tools, and the model chooses whether to call it, how often and with which query. In the second graph the retriever becomes `retriever_tool`, beside an `off_topic` tool for unrelated questions. The `agent` node calls the model and `ToolNode` runs the tools it asked for; the run loops back to `agent` while the reply carries tool calls and ends when it carries none:

```mermaid
sequenceDiagram
    participant U as User
    participant A as agent node
    participant T as ToolNode
    U->>A: HumanMessage: Can I export my data<br/>after I cancel my plan?
    A->>T: AIMessage with tool_calls:<br/>retriever_tool(query)
    T->>A: ToolMessage: 2 chunks
    A->>U: AIMessage, no tool_calls: the answer
```

*Figure 2: The model decides. The retriever runs only because the model's reply asked for it.*

Both graphs spend two model calls on a handbook question: classify then generate in the first, tool call then answer in the second. They differ in who decides and in what the retriever receives:

| | Pipeline decides | Model decides |
|---|---|---|
| The retrieval decision | `topic_decision`, then fixed edges | the model, through `tool_calls` |
| What the decision reads | the classifier's system prompt | each tool's name, description and argument schema |
| Query sent to the retriever | the user's message, unchanged | the `query` argument the model writes |
| Retrievals per question | 0 or 1 | 0, 1 or more, because `tools` loops back to `agent` |
| Unrelated questions | `off_topic_response`, a fixed message | the `off_topic` tool, or a direct answer |
| Typical failure | the classifier says no and the handbook is never searched | the model answers from memory and never calls the tool |

*Table 1: The two graphs compared on the same retriever.*

The model-decided graph handles small talk with no retrieval, rewrites a follow-up into a better query, and searches again when the first chunks miss. It pays with a decision you no longer control in code.

We call the last row's failure a **silent skip**: the model answers a policy question without calling `handbook_search`, from its training data, with nothing to cite. The refund reply above is one. Its mirror in the fixed graph is the **classifier veto**: a no from `topic_decision`, and the handbook is never searched.

### What the tool hands back

A retriever tool turns a list of Documents into one message, and that step can lose the sources. The standard wrapper, `create_retriever_tool`, joins the chunk texts with a blank line and drops each Document's metadata. We wrapped a fixed retriever that returns one chunk, *Refunds take 5 to 10 business days.*, tagged `refund-timing`, three ways:

| Wrapper setting | What the model receives | Source visible to the model |
|---|---|---|
| Default | the chunk text only | ✗ |
| A document prompt that prints the source | `refund-timing: Refunds take 5 to 10 business days.` | ✓ |
| Content plus artifact | the chunk text, with the full Documents kept beside it for your code | ✗ for the model, ✓ for your code |

*Table 2: One chunk through three wrapper settings (run against the installed `langchain_core`).*

We call the default row's failure the **lost source**: the model quotes a correct policy and cannot say where it came from. Print the source into each chunk when the answer must cite; keep the artifact when your code checks citations.

Getting the evidence back intact matters only once the model has chosen the tool, and that choice rests on the description.

## Tool descriptions

A **tool description** is the short text the model reads to decide whether a tool fits the question. When the model picks a tool it sees three things per tool and nothing else:

```mermaid
flowchart LR
    N["Name<br/>retriever_tool"] --> M["Model<br/>picks a tool"]
    D["Description<br/>the scope in words"] --> M
    S["Argument schema<br/>query: string"] --> M
    M --> C[/"Tool call<br/>or answer"/]
```

*Figure 3: The model's whole view of a tool. It never sees the documents behind it.*

In the notebook the description reads *Information related to pricing, hours, or the founder of Cafe Lumiere*, over one `query` string argument. That sentence now carries the scope the first graph kept in its classifier prompt, and it has to separate the retriever from every other tool the model can call.

### Measuring routing with a stand-in router

The [interactive lab](interactive/tool-routing-lab.html) gives the Larkspur agent `handbook_search` and `web_search` and routes twenty golden questions (ten for the handbook, six for the web, four for no tool) plus five held out. Its router stands in for the model: the M10 TF-IDF retriever scores each question against the two descriptions and picks the higher, or no tool when neither shares a word. Its scores match scikit-learn's `TfidfVectorizer` to within 4.5e-16:

| Descriptions | Golden set, of 20 | Sent to the wrong tool | Held out, of 5 | Tokens per call |
|---|---|---|---|---|
| Names only: "Search tool." for both | 4 | 0 | 0 | 6 |
| Vague: "Information related to Larkspur Cloud plans and pricing." | 5 | 0 | 0 | 20 |
| Specific: the topics each tool covers | 15 | 1 | 2 | 84 |
| Tuned: Specific plus words taken from the golden questions | 19 | 0 | 4 | 133 |

*Table 3: Routing scores for the four description presets. Tokens are the lab's estimate of four characters per token.*

- **Names only** gets right only the four questions that needed no tool. The other sixteen are silent skips.
- **Vague** catches *When are monthly plans billed?* on "plans" and nothing else; *Can I export my data after I cancel my plan?* misses because TF-IDF treats "plan" and "plans" as different words.
- **Specific** gets three handbook questions right for a thin reason: *goes down*, *reboot* and *size* match nothing, and the word "server" carries them.

<!-- lab: interactive/tool-routing-lab.html -->

### Planted failures in the Specific preset

We reran the lab's router against scikit-learn to see why Specific misses its five golden questions:

| Question | Routed to | Why |
|---|---|---|
| *How long does a refund take?* | no tool | the description says "refunds"; the question says "refund" |
| *Is there a major AWS outage right now?* | no tool | the web description says "other cloud providers" and never names AWS or outages |
| *What is the latest stable PostgreSQL release?* | no tool | the description says "releases" and never names PostgreSQL |
| *Who won the Champions League final this year?* | no tool | "sports" is in the web description; no word of the question is |
| *What does Hetzner charge for a 4 GB server?* | `handbook_search` | "server" appears only in the handbook description |

*Table 4: Specific's five golden misses, read from the router's scores.*

The first four are **vocabulary misses**: the description covers the topic in words the question does not use, and a model would catch most of them. The last is a **scope gap**: neither description says which tool owns other providers' prices, so the router guessed, and a model would have to guess too. It is the worst miss in the set, because a competitor's price gets answered from Larkspur's handbook. Adding "refund" to the handbook description takes Specific to 16 of 20 and leaves the Hetzner question wrong: more Larkspur words cannot draw a boundary neither description states.

### Planted failure: the overfitted description

Tuned copies the golden questions' own words (PostgreSQL, AWS, Hetzner, Docker, Ubuntu) into the descriptions and fixes every golden row but one. On the held-out five, *What is the newest Node.js version?* still gets no tool. We call this an **overfitted description**: it scores well on the questions it was written against and worse on the next one a user types, like a retriever tuned on its own test set.

### From the stand-in to a real model

Descriptions also cost tokens, because each one is sent with every model call. Tuned carries 133 to Specific's 84, so 49 more per call; a handbook question takes two calls (Table 1), so 98 more per question. A model forgives vocabulary misses but fails on a scope gap the same way the stand-in does. A description that earns its tokens states four things:

- **What it searches, and whose data**: "the Larkspur Cloud handbook" against "the public web".
- **The topics, in the words users type**: refunds, cancelling, data export, outages, server sizing.
- **Where it stops**: Larkspur's own prices and policies belong to `handbook_search`; other providers' prices belong to `web_search`.
- **What it returns**: handbook passages as plain text, so the model knows what comes back and that it should quote it.

Treat the descriptions as a retrieval setting: a routing golden set of questions with the tool each should use, a held-out set, and the misses from production traces added over time.

## In practice: the Larkspur refund question

Back to the customer, with the fixes in place:

1. `handbook_search` lists refunds among Larkspur's own policies, and `web_search` says it covers other providers, so the model calls `handbook_search` with "refund timing".
2. The tool prints each chunk's source in front of its text, and the model answers 5 to 10 business days, citing `refund-timing`.
3. The question joins the routing golden set with `handbook_search` as its expected tool, so a description change that breaks it shows up before release.

Hand the decision to the model only once that routing golden set exists; without it, a silent skip is invisible.

> **Key distinction:** the routing golden set scores which tool was called; the M10 golden set scores the answer. A right tool with a wrong answer is a retrieval or generation failure. Keep both sets.

## Limits of this evidence

- **The router is a stand-in**, stricter about wording than a model. Its scores show how descriptions fail, not how often a model does.
- **No model routing scores yet.** The module's lab solution measures a real model's tool choice on 20 labelled questions; its results are pending a run.

## Key Takeaways

- Retrieval as a tool lets the model skip it for small talk, rewrite the query and search again. The cost is a silent skip: a model that answers from memory has nothing to cite.
- The default retriever tool drops each chunk's source. Print the source into the chunk text, or keep the Documents beside the text, before you ask the model to cite.
- Write each description to say what it searches, its topics in users' words, where it stops and what it returns. Score every change on a routing golden set and on held-out questions, because a description copied from the golden set overfits.

## Check yourself

<details>
<summary>1. What does letting the model decide when to retrieve gain over a fixed classifier, and what does it give up?</summary>

It handles small talk with no retrieval, rewrites a follow-up into a better query, and searches again when the first chunks miss. It gives up a decision you control in code. A model that answers a refund question without calling `handbook_search` makes a silent skip: the answer comes from its training data, with nothing to cite.

</details>

<details>
<summary>2. With the Specific descriptions, the question about Hetzner's price for a 4 GB server goes to the handbook tool. Why, and what fixes it?</summary>

"server" appears only in the handbook description, and neither description says which tool owns other providers' prices, so the router guessed. That is a scope gap, and adding more Larkspur words does not close it. State where each tool stops: Larkspur's own prices and policies belong to `handbook_search`, other providers' prices to `web_search`.

</details>

<details>
<summary>3. The Tuned descriptions route 19 of 20 golden questions because they copy words from those questions. What else must you check before trusting them?</summary>

The held-out questions, where they reach 4 of 5 and still give the Node.js question no tool, which marks an overfitted description. Check the cost too: 133 tokens on every model call against 84. Score each description change against the golden set and the held-out set, and add misses from production traces.

</details>

---
*Previous: [M31 overview](../README.md). Next: [31.2 Managed RAG platforms: Contextual AI](../../../optional/theory/02_managed_rag_platforms_contextual_ai/README.md).*
