# M22.4 Theory: The manual tool loop and the augmented LLM in LangGraph

*[M22 theory](../README.md) · Lesson 22.4 · Notebooks: [`04a_tool_calling_manual_loop.ipynb`](../../notebook/04a_tool_calling_manual_loop.ipynb), [`05a_tool_loop_errors_and_evaluation.ipynb`](../../notebook/05a_tool_loop_errors_and_evaluation.ipynb) (Part 3.1) · [All theory pages](../../../../../THEORY.md)*

## Native tool calls and the message trace

A Larkspur customer asks whether web-1 is running and whether rebooting changes its IP address. One model reply can request both lookups. You will pair each request with its result, then compare a graph that stops after tool execution with one that lets the model answer.

### Step 1: Read the requested arguments

`llm.bind_tools(tools)` returns a model that sends the tool schemas with every request. A tool-request reply can be an `AIMessage` with empty `content` and a `tool_calls` list. In the recorded weather example, *How will the weather be in Munich today?* comes back as one call:

```text
[{'name': 'fake_weather_api', 'args': {'city': 'Munich'}, 'id': 'call_GRGobvpFuPRkrEUTERCcyNIw', 'type': 'tool_call'}]
```

Ask about the weather and outdoor seating together and the same reply holds two calls, one per tool, with `finish_reason: 'tool_calls'`. The model asks for both at once because neither depends on the other. There is no extra round trip.

### Step 2: Return one result for each call

The model still runs nothing. The loop from lesson 22.1 is now four steps over typed messages:

1. Send the `HumanMessage` and append the model's `AIMessage` with its `tool_calls`.
2. For each call, look the tool up by `name` and invoke it with `args`.
3. Append one `ToolMessage(output, tool_call_id=call["id"])` per call.
4. Call the model again with the whole list. It answers from the results.

The `tool_call_id` is what pairs a result with its request. With two parallel calls the model would otherwise have two unlabelled strings and no way to tell which tool produced which. OpenAI's API also rejects a history in which an `AIMessage`'s tool call has no matching `ToolMessage`, so a loop that drops a failed call's result breaks the next request.

Build a small message exchange with a scripted tool request. This checks result pairing without a model or a server lookup.

```python
from langchain_core.messages import AIMessage, ToolMessage

request = AIMessage(content="", tool_calls=[{
    "name": "get_server_status", "args": {"server_id": "web-1"}, "id": "status_1"
}])
result = ToolMessage(content="web-1: running", tool_call_id="status_1")
print(request.tool_calls[0]["id"] == result.tool_call_id)
print(result.content)
```

**Expected output**

```text
True
web-1: running
```

The equality is the association the next model turn needs. It does not execute the tool or establish that a server was checked.

### Step 3: Count messages in a two-tool run

The lab's two-tool question shows the shape on Larkspur's tools:

| # | Message | Content |
|---|---|---|
| 0 | `HumanMessage` | *Is my server web-1 running, and does a reboot change its IP address?* |
| 1 | `AIMessage` | two calls: `get_server_status(server_id='web-1')`, `search_handbook(query='reboot server IP address')` |
| 2 | `ToolMessage` | `web-1: running` |
| 3 | `ToolMessage` | `reboot (0.747): You can reboot a server from the console. A reboot takes about a minute and does not change the server IP address.` and `sizing (0.156): …` |
| 4 | `AIMessage` | the answer, no tool calls |

Five messages, two of them tool results. The scores are real TF-IDF over the M10 chunks. The model turns are scripted.

For a model without native tool calling, the alternative is a text protocol: the tool signatures go into the system prompt, and your code parses the call out of the reply. Lesson 22.1 builds one from scratch with `<tool_call>` tags. Nothing guarantees valid JSON, a real tool name or every argument, so use it only when the model leaves no choice.

## The augmented LLM

### Step 1: Route requests to the tool node

A one-shot LangGraph implementation hands tool dispatch to the framework. A `tool_calling_llm` node calls the bound model, the prebuilt `tools_condition` routes to a `ToolNode` when the reply has `tool_calls` and to `END` when it has none, and the `ToolNode` runs every requested call and writes the `ToolMessage`s into state.

```mermaid
flowchart LR
    S([START]) --> L["tool_calling_llm<br/>bound model"]
    L --> C{tools_condition}
    C -- tool calls --> T["tools<br/>ToolNode"]
    C -- none --> E([END])
    T --> E
    T -. "lesson 22.5" .-> L
```

### Step 2: Compare stopping after tools with answering

Follow the solid edges in this one-shot graph. *Explain tool calling in one sentence* ends at the first `END` with a direct answer. *What's the weather in Tokyo?* calls `get_weather`, and the run ends on the tool's raw output in a `ToolMessage`: nobody reads the result, the user gets no sentence, and a second, dependent call is impossible.

That graph is an augmented LLM. One more edge makes it an agent: `tools` back to the model instead of to `END` (the dashed line). The looping `create_tool_agent` implementation adds it with `graph.add_edge("tools", "agent")`, and the graph becomes the loop in the module's mental model.

### Try it yourself

Remove the return edge from `tools` to the model. For the two-tool question, name the final message type and whether a user-facing answer can exist. Check against the diagram: the solid `tools → END` path stops on a `ToolMessage`. Restore the return edge and check that the final `AIMessage` has no tool calls.

### Practice notebook

Use the implementation below to test the exercise and inspect each state update. Follow its provider setup for live model calls. Recorded model responses and timings can change on a new run.

- [Manual tool calling](../../notebook/04a_tool_calling_manual_loop.ipynb).
- [LangGraph tool dispatch](../../notebook/05a_tool_loop_errors_and_evaluation.ipynb) (Part 3.1, the opening of lesson 22.5's notebook).

## Key Takeaways

- A bound model returns an `AIMessage` with `tool_calls` and runs nothing. Independent calls arrive together in one reply, saving a round trip.
- Answer every call with one `ToolMessage` carrying its `tool_call_id`. The id pairs results with requests, and OpenAI rejects a history with an unanswered call.
- A graph that goes from tools to `END` is an augmented LLM. One edge from tools back to the model turns it into an agent loop.

## Check yourself

<details>
<summary>1. Why does every ToolMessage carry the id of the tool call it answers?</summary>

The `tool_call_id` pairs a result with its request. With two parallel calls the model would otherwise get two unlabelled strings and no way to tell which tool produced which. OpenAI's API also rejects a history in which a tool call has no matching `ToolMessage`, so dropping a failed call's result breaks the next request.

</details>

<details>
<summary>2. A customer asks if web-1 is running and if a reboot changes its IP. How many messages does the trace hold, and why are both tools requested at once?</summary>

Five: the `HumanMessage`, one `AIMessage` with two calls (`get_server_status` and `search_handbook`), two `ToolMessage`s and the final `AIMessage`. Neither call depends on the other, so the model asks for both at once and saves a round trip.

</details>

<details>
<summary>3. The graph from the one-shot graph example answers a weather question with the tool's raw output and no sentence. What is missing, and which one change fixes it?</summary>

The `tools` node goes straight to `END`, so nobody reads the result and no dependent call is possible. That graph is an augmented LLM. Adding the edge from `tools` back to the model (`graph.add_edge("tools", "agent")` in lesson 22.5's `create_tool_agent`) makes it an agent loop.

</details>

---
*Previous: [22.3 Defining tools and binding them to a model](../03_defining_tools_and_binding_them_to_a_model/README.md). Next: [22.5 Tool errors and evaluating tool calls](../05_tool_errors_and_evaluating_tool_calls/README.md).*
