# M22.4 Theory: The manual tool loop and the augmented LLM in LangGraph

*[M22 theory](../README.md) · Lesson 22.4 · Notebooks: [`04a_tool_calling_manual_loop.ipynb`](../../notebook/04a_tool_calling_manual_loop.ipynb), [`05a_tool_loop_errors_and_evaluation.ipynb`](../../notebook/05a_tool_loop_errors_and_evaluation.ipynb) (Part 3.1) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Two tool calls in one reply, one id each, and the edge that turns a tool user into an agent -->

## Native tool calls and the message trace

> **What you'll learn**
>
> - **Explain** how native tool calling returns structured calls with ids instead of tagged text.
> - **Trace** a two-tool question message by message and count what the history holds.
> - **Diagnose** the broken history that a dropped tool result leaves behind.
> - **Compare** an augmented LLM with an agent loop, and name the one edge between them.

Lesson 22.3 turned each tool into a schema. This lesson sends those schemas with a real request and follows what comes back.

A Larkspur customer asks *Is my server web-1 running, and does a reboot change its IP address?* Answering needs two lookups, a server status and a handbook search, and neither depends on the other. The model can ask for both in one reply, which means your code has to keep track of which result answers which request.

### A reply that requests tools

With **native tool calling**, the tool schemas travel in the API request, and the provider returns tool requests as structured data instead of tagged text. A reply that requests tools is an **AI message** whose text content is often empty and whose list of **tool calls** holds one entry per request:

| Field | Example from the recorded weather run | What it is for |
|---|---|---|
| Name | The weather tool | Which tool to run |
| Arguments | City: Munich | What to pass |
| Call id | A unique id the provider generates | Pairing the result with this request |

*Table 1: One entry in a reply's tool calls.*

Ask about the weather and outdoor seating together, and the same reply holds two calls, one per tool, with a finish reason that says the model stopped to request tools. The model asks for both at once because neither depends on the other, which saves a round trip.

### One result for each call

The model still runs nothing. The loop from lesson 22.1 becomes four moves over typed messages:

```mermaid
sequenceDiagram
    participant C as Your code
    participant M as Model
    participant T as Tools
    C->>M: human message
    M-->>C: AI message, two calls with ids
    C->>T: run call 1
    T-->>C: result 1
    C->>T: run call 2
    T-->>C: result 2
    C->>M: two tool messages, one id each
    M-->>C: AI message, the answer
```

*Figure 1: The native loop. Each tool message carries the id of the call it answers.*

1. Send the user's question as a **human message**, and append the model's AI message with its tool calls.
2. For each call, look the tool up by name and run it with the given arguments.
3. Append one **tool message** per call, holding the result and the id of the call it answers.
4. Call the model again with the whole list. It answers from the results.

The call id is what pairs a result with its request. With two parallel calls, the model would otherwise receive two unlabelled strings and no way to tell which tool produced which.

> **Pitfall: the orphaned call.** OpenAI's API rejects a history in which a tool call has no matching tool message. A loop that drops the result of a failed call breaks the next request, not only that answer.

Matching ids only records which request a result belongs to. It does not prove the tool ran correctly or that the server was actually checked.

### Counting messages in a two-tool run

The M22 lab's two-tool question shows the whole trace on Larkspur's tools:

| # | Message | Content |
|---|---|---|
| 0 | Human | *Is my server web-1 running, and does a reboot change its IP address?* |
| 1 | AI | Two calls: server status for web-1, and a handbook search for "reboot server IP address" |
| 2 | Tool | web-1: running |
| 3 | Tool | The reboot chunk (score 0.747): "You can reboot a server from the console. A reboot takes about a minute and does not change the server IP address." The sizing chunk follows with a score of 0.156 |
| 4 | AI | The answer, with no tool calls |

*Table 2: The two-tool trace, five messages.*

Five messages, two of them tool results. The scores are real TF-IDF scores over the M10 handbook chunks; the model's turns are scripted. Message count is a cheap diagnostic: a single-tool question takes four messages, so six on the same question means an extra round, which lesson 22.5 traces to a malformed first call.

A model without native tool calling needs the text protocol from lesson 22.1 instead: tool descriptions in the system prompt and your code parsing the call out of the reply. Nothing guarantees valid JSON, a real tool name or every argument, so use it only when the model leaves no choice.

## The augmented LLM

LangGraph can take over the dispatch. The graph has three pieces:

- **Model node**: calls the model with the tools bound.
- **Router**: checks the latest reply; tool calls send the run to the tool node, no tool calls end it.
- **Tool node**: runs every requested call and writes one tool message per call into the graph's state.

```mermaid
flowchart LR
    S([START]) --> L["tool_calling_llm<br/>bound model"]
    L --> C{tools_condition}
    C -- tool calls --> T["tools<br/>ToolNode"]
    C -- none --> E([END])
    T --> E
    T -. "lesson 22.5" .-> L
```

*Figure 2: A one-shot tool graph. The solid edges stop after the tools; the dashed edge is the loop.*

Follow the solid edges with two questions:

| Question | Path | What the user gets |
|---|---|---|
| *Explain tool calling in one sentence* | Model, router, end | A direct answer; no tool needed |
| *What's the weather in Tokyo?* | Model, router, tool node, end | The tool's raw output and no sentence |

*Table 3: Two questions through the one-shot graph.*

The second run ends on a tool message. Nobody reads the result, the user gets no sentence, and a second call that depends on the first is impossible. We call that **stopping at the tool**.

That graph is an **augmented LLM**: a model that can use tools once, but not a loop. One more edge, from the tool node back to the model node (the dashed line), makes it an agent. The model then reads each result and decides whether to call another tool or answer, which is the loop in the module's mental model.

> **Key distinction:** an augmented LLM ends on whatever the tools return; an agent ends when the model writes a reply with no tool calls. The difference is one edge, and it changes the final message from a tool result to an answer.

## In practice: the web-1 question

Run the web-1 question through both graphs:

1. **Augmented LLM**: the model requests both lookups, the tool node runs them, and the run ends on the handbook chunk. The customer sees raw tool output.
2. **Agent loop**: the same two tool messages go back to the model, which answers that web-1 is running and that a reboot does not change its IP address. The final message is an AI message with no tool calls.

In both runs each tool message carries its call id, so the model can tell the status from the handbook chunk. Lesson 22.5 adds what happens when one of those calls fails.

## Key Takeaways

- A model with tools bound returns an AI message with tool calls and runs nothing. Independent calls arrive together in one reply, saving a round trip.
- Answer every call with exactly one tool message carrying its call id. The id pairs results with requests, and OpenAI rejects a history with an unanswered call.
- A graph that goes from the tool node to the end is an augmented LLM. One edge from the tool node back to the model turns it into an agent loop.

## Check yourself

<details>
<summary>1. Why does every ToolMessage carry the id of the tool call it answers?</summary>

The call id pairs a result with its request. With two parallel calls the model would otherwise get two unlabelled strings and no way to tell which tool produced which. OpenAI's API also rejects a history in which a tool call has no matching tool message, so dropping a failed call's result breaks the next request.

</details>

<details>
<summary>2. A customer asks if web-1 is running and if a reboot changes its IP. How many messages does the trace hold, and why are both tools requested at once?</summary>

Five: the human message, one AI message with two calls (server status and handbook search), two tool messages and the final AI message. Neither call depends on the other, so the model asks for both at once and saves a round trip.

</details>

<details>
<summary>3. A graph answers a weather question with the tool's raw output and no sentence. What is missing, and which one change fixes it?</summary>

The tool node goes straight to the end, so nobody reads the result and no dependent call is possible. That graph is an augmented LLM. Adding an edge from the tool node back to the model makes it an agent loop, and the model then turns the result into an answer.

</details>

---
*Previous: [22.3 Defining tools and binding them to a model](../03_defining_tools_and_binding_them_to_a_model/README.md). Next: [22.5 Tool errors and evaluating tool calls](../05_tool_errors_and_evaluating_tool_calls/README.md).*
