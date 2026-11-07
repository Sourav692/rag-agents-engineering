# M22.1 Theory: Agentic patterns from scratch: reflection, tool use, ReAct planning

*[M22 theory](../README.md) · Lesson 22.1 · Notebooks: [`01b_tool_use_pattern.ipynb`](../../notebook/01b_tool_use_pattern.ipynb), [`01c_planning_pattern_react.ipynb`](../../notebook/01c_planning_pattern_react.ipynb), [`01a_reflection_pattern.ipynb`](../../../optional/notebook/01a_reflection_pattern.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*

## Agent loop

A Larkspur customer asks how long a refund takes. Your model can request a handbook search, but your application must run it and return the evidence. You will trace that exchange, then see why dependent actions need a loop and a stopping rule.

### Step 1: Read the three stopping rules

The three implementations below use the raw OpenAI SDK and `gpt-4o-mini`. They describe tools in prompt text rather than using the native `tools=` parameter. An observation is the result your code sends back after executing the requested function.

| Pattern | Implementation | What repeats | Stops when |
|---|---|---|---|
| Reflection | Draft and critic | Generate a draft, critique it with a second persona, regenerate | The critic answers `<OK>`, or after `n_steps` rounds |
| Tool use | One-round `ToolAgent` | Nothing: one round of tool calls, then the answer | The model has answered from the observation |
| ReAct planning | Repeated `ReactAgent` | Thought, tool call, observation | The model writes `<response>`, or after `max_rounds` (10 by default) |

### Step 2: Turn a request into an observation

In the one-round implementation, the model never receives a function. It receives text: a system prompt that lists each tool's signature inside `<tools>` tags and asks for calls in a fixed format. The model answers *What's the current temperature in Madrid, in Celsius?* with text, not an answer:

```
<tool_call>
{"name": "get_current_weather","arguments": {"location": "Madrid", "unit": "celsius"}}
</tool_call>
```

Your code does the rest: a regular expression strips the tags, `json.loads` turns the call into a dict, `get_current_weather(**arguments)` runs it, and the result goes back as a user message, `Observation: {"temperature": 25, "unit": "celsius"}`. A second model call turns that into the sentence the user reads. The `@tool` decorator automates the signature (name, docstring, type hints), and `validate_arguments` casts values to the annotated types, so `"5"` becomes `5` when the hint says `int`.

The one-round `ToolAgent` stops after one round. It cannot use one tool's result to choose the next call, and that is the gap ReAct fills.

### Step 3: Feed each result into the next action

The ReAct implementation gives the model a protocol: think inside `<thought>`, act with a `<tool_call>`, read the `<observation>` your code sends back, and finish inside `<response>`. The reference example's task needs three calls in order, each depending on the one before:

```mermaid
sequenceDiagram
    participant C as Your code
    participant M as Model
    C->>M: question and three tool signatures
    M-->>C: thought, sum_two_elements(1234, 5678)
    C->>M: observation 6912
    M-->>C: thought, multiply_two_elements(6912, 5)
    C->>M: observation 34560
    M-->>C: thought, compute_log(34560)
    C->>M: observation 10.450452222917992
    M-->>C: response, about 10.45
```

Dependent steps work because every observation stays in the chat history for the next turn. In pseudocode, `ReactAgent.run()` is this loop. The helper names stand for parsing and dispatch operations rather than runnable Python:

```text
for _ in range(max_rounds):                    # 10 by default
    reply = model(history)
    if has_tag(reply, "response"):
        return the response                    # the model says it is done
    for call in tool_calls(reply):
        history.append(observation(run(call)))  # results feed the next turn
```

The loop has two exits. The `<response>` tag is the model's own decision to stop. `max_rounds` is yours: without it, a model that keeps asking for tools (because the tool keeps returning nothing useful, say) runs and bills forever.

### Step 4: Diagnose a broken call before retrying

Nothing forces the model to write valid JSON, name a real tool or supply every argument. The parser raises `ValueError` when the tags or the JSON are wrong. The type casting covers four types (`int`, `str`, `bool`, `float`). Native tool calling (lesson 22.4) moves the schema into the API, so the provider returns structured `tool_calls` with ids. The loop stays the same.

For Larkspur's support agent the loop is identical with different tools. *How long does a refund take?* becomes a thought ("I need the refund policy"), a call to `search_handbook`, an observation holding the retrieved chunks, and a response that quotes them. The M22 lab runs that question through LangGraph's version of this loop, including a first call that fails.

### Try it yourself

Trace the arithmetic example with a one-round `ToolAgent` instead of `ReactAgent`. Which result is unavailable when the first calls are chosen? Check that the multiplication needs the observed sum, 6912, and the logarithm needs the observed product, 34560. Then set a round cap below the required dependent actions and explain why the run must stop without a complete answer.

### Practice notebook

Use the implementation below to test the exercise and inspect each state update. Follow its provider setup for live model calls. Recorded model responses and timings can change on a new run.

- [One-round tool use](../../notebook/01b_tool_use_pattern.ipynb).
- [ReAct from scratch](../../notebook/01c_planning_pattern_react.ipynb).
- [Reflection from scratch](../../../optional/notebook/01a_reflection_pattern.ipynb) (optional).

## Key Takeaways

- The model never runs a tool. It writes a call as text, your code parses and runs it, and the result goes back as an observation.
- ReAct loops thought, tool call and observation, and keeps every observation in the history, so later calls can depend on earlier results.
- Give the loop two exits: the model's own `<response>` and a `max_rounds` cap you own. Without the cap, a model that keeps asking for tools runs and bills forever.

## Check yourself

<details>
<summary>1. Why can the ReAct agent chain three dependent tool calls when the one-round tool-use agent cannot?</summary>

The one-round `ToolAgent` runs one round of tool calls and then answers, so it cannot use one result to choose the next call. `ReactAgent.run()` loops, and every observation stays in the chat history, so the model sees `6912` before it asks to multiply it by 5.

</details>

<details>
<summary>2. The ReAct task sums 1234 and 5678, multiplies the result by 5, then takes the log. How many observations does your code send back, and what is the second?</summary>

Three observations: `6912`, `34560` and `10.450452222917992`. The second, `34560`, is the result of `multiply_two_elements(6912, 5)`. After the third the model finishes inside `<response>` with about 10.45.

</details>

<details>
<summary>3. A hand-written ReAct agent keeps calling a search tool that returns nothing useful, and the bill keeps growing. Which exit was missing?</summary>

`max_rounds`, the exit you own (10 by default). The `<response>` tag only fires when the model decides it is done, and a model that keeps asking for tools never decides that. Without `max_rounds` the loop runs and bills forever.

</details>

---
*Previous: [M22 overview](../README.md). Next: [22.3 Defining tools and binding them to a model](../03_defining_tools_and_binding_them_to_a_model/README.md).*
