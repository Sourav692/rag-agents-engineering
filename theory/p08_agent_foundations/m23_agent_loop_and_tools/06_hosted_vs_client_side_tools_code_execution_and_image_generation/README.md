# M23.6 Theory: Hosted vs client-side tools: code execution and image generation

*[M23 theory](../README.md) · Lesson 23.6 · Notebooks: [`06a_hosted_vs_client_side_tools.ipynb`](../../../../course/p08_agent_foundations/m23_agent_loop_and_tools/notebooks/06a_hosted_vs_client_side_tools.ipynb), [`06b_hosted_code_execution.ipynb`](../../../../course/p08_agent_foundations/m23_agent_loop_and_tools/optional/06b_hosted_code_execution.ipynb) (optional), [`06c_agentic_image_generation.ipynb`](../../../../course/p08_agent_foundations/m23_agent_loop_and_tools/optional/06c_agentic_image_generation.ipynb) (optional) · [All theory pages](../../../README.md)*

## Hosted vs client-side tools

Larkspur must enforce account access before a status lookup runs. A public web search may need different controls. You will follow the same question through client-side and hosted execution, then identify what your application can inspect or refuse at each boundary.

### Step 1: Follow both execution paths

Every tool so far ran on your machine: the model returned a call, your code ran it, you sent the result back. A hosted tool runs on the provider's infrastructure instead, and the reply arrives with the result already folded in. The API difference is a few lines. The difference in what you can see and control is large.

The recorded comparison answers *What is the current population of Lisbon?* both ways with `gpt-4o-mini`:

```mermaid
sequenceDiagram
    participant Y as Your code
    participant P as Provider
    Note over Y,P: Client-side, Chat Completions
    Y->>P: question and a function schema
    P-->>Y: tool call lookup_population(Lisbon)
    Note over Y: your code runs it and can log, refuse, cache or redact
    Y->>P: the tool result
    P-->>Y: answer
    Note over Y,P: Hosted, Responses API
    Y->>P: question and tools=[web_search]
    Note over P: the provider chooses the query and runs the search
    P-->>Y: answer and a web_search_call item
```

In the recorded run the client-side path took two round trips and 1.86 s. The hosted path took one round trip and 3.16 s. One run proves little about latency, but it does show that one round trip is not automatically faster. The hosted reply carries a `web_search_call` output item with its status and the query the provider chose (`current population of Lisbon 2023`). That item is your only window into the execution: you did not choose the query, you cannot see the raw results, and nothing of yours ran between retrieval and generation.

| | Client-side | Hosted |
|---|---|---|
| Who executes | Your process | The provider's infrastructure |
| See the arguments | Yes, before execution | Sometimes, after the fact |
| Intercept or refuse a call | Yes, it is your code | No |
| Deterministic tests | Yes, stub the function | No, it hits the live world |
| Failure | Your exception, your retry | A status across an API boundary; you can only re-run the whole request |
| Cost | Tokens and your infrastructure | Tokens and a fee per tool call (code interpreter: per container session) |

### Step 2: Place the policy check before execution

The gap between "the model asked" and "the model sees the result" is where policy lives. The client-side `guarded_lookup` is four lines that refuse any city outside an allow-list. Asked about Pyongyang, it returns an error and the model says it cannot retrieve that population. Allow-lists, tenant scoping, PII redaction and spend caps all sit in that seam, and choosing a hosted tool means choosing not to have it.

### Step 3: Compare the evidence returned by each tool

Hosted tools expose different amounts of execution detail in these examples:

| Hosted tool | What comes back besides the answer |
|---|---|
| `web_search` | The query, roughly; no raw results |
| `code_interpreter`  | The source it ran, its output and any files, so you can audit the method |
| `image_generation`  | The `revised_prompt` the model wrote for itself and the image as base64 |

Code interpreter is also configurable: The code-execution example sets a memory ceiling and a network policy (`{"type": "disabled"}` for a sandbox that works only on data you supplied). What you still cannot do is approve the code before it runs, veto one call, or stub it in a test. The image-generation example adds a different caution: the agent narrates what it *meant* to draw, and only feeding the image back to a vision model shows what it actually drew. The model also has to leave the tool alone when a turn asks for advice; The image example checks that it does.

### Step 4: Choose an execution location for each task

For Larkspur's support agent the split follows the data:

- `search_handbook` and `get_server_status` stay client-side. They read the customer's account and Larkspur's own policy, need tenant scoping and logging, and must be stubbed in tests (the M23 lab runs them deterministically for this reason).
- A hosted `web_search` fits questions the handbook cannot answer, about public software or third-party services, where there is nothing to enforce between the call and the result.
- Hosted code execution fits arithmetic on numbers the customer pasted into the chat. The arithmetic example shows why execution matters: a model that runs three lines of Python computes, while one that answers directly samples plausible digits.

In these OpenAI examples, hosted tools use the Responses API, while Chat Completions carries the client-side function calls. The reference example uses `client.responses.create` on the raw OpenAI client to make hosted-tool configuration explicit. Check the integration and provider version before choosing a wrapper. A third placement, a tool on a server you run that the model reaches over a protocol, is MCP (M38 to M40), and it gives back much of the seam that hosted tools remove.

### Try it yourself

Apply the Lisbon comparison to a lookup for a city outside the allow-list. Identify the exact place where `guarded_lookup` can refuse the call and explain why the hosted search has no equivalent client-side interception point. Then choose a path for a tenant-scoped server lookup. Check that your design enforces account scope before execution and can stub the lookup in a test.

### Practice notebook

Use the implementation below to test the exercise and inspect each state update. Follow its provider setup for live model calls. Recorded model responses and timings can change on a new run.

- [Tool execution placement](../../../../course/p08_agent_foundations/m23_agent_loop_and_tools/notebooks/06a_hosted_vs_client_side_tools.ipynb).
- [Hosted code execution](../../../../course/p08_agent_foundations/m23_agent_loop_and_tools/optional/06b_hosted_code_execution.ipynb) (optional).
- [Agent image generation](../../../../course/p08_agent_foundations/m23_agent_loop_and_tools/optional/06c_agentic_image_generation.ipynb) (optional).

## Key Takeaways

- A hosted tool runs on the provider's side and returns the result folded into the reply. You lose the seam where your code can log, refuse, redact or cache a call.
- Hosted tools vary in visibility: web search shows roughly the query, code interpreter shows the code and output, image generation shows its revised prompt. None can be stubbed in a test.
- Keep tools that touch customer data or need tenant scoping client-side. Use hosted tools for public lookups and arithmetic on data the user supplied.

## Check yourself

<details>
<summary>1. What do you give up when you move a tool from client-side to hosted?</summary>

The seam between the model asking and the model seeing the result, which is where policy lives: allow-lists, tenant scoping, PII redaction and spend caps. You also lose the chance to see arguments before execution, refuse a call, or stub the tool in a deterministic test, and a failure can only be handled by re-running the whole request.

</details>

<details>
<summary>2. Larkspur's support agent needs the customer's server status and an answer about a third-party service. Which should run client-side, and which suits a hosted tool?</summary>

`get_server_status` stays client-side: it reads the customer's account, needs tenant scoping and logging, and must be stubbed in tests. A hosted `web_search` fits the third-party question, which the handbook cannot answer and where there is nothing to enforce between the call and the result.

</details>

<details>
<summary>3. The hosted search took one round trip and 3.16 s, the client-side path two and 1.86 s. Is hosted the way to cut latency?</summary>

Not on this evidence. One round trip is not automatically faster: in that run the hosted path was the slower one. One run also proves little about latency, so measure on your own traffic. And going hosted removes the seam where your code could log, refuse or redact the call.

</details>

---
*Previous: [23.5 Tool errors and evaluating tool calls](../05_tool_errors_and_evaluating_tool_calls/README.md). Next: [M23 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
