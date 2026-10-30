# M23.5 Theory: Tool errors and evaluating tool calls

*[M23 theory](../README.md) · Lesson 23.5 · Notebooks: [`05a_tool_loop_errors_and_evaluation.ipynb`](../../../../course/p08_agent_foundations/m23_agent_loop_and_tools/notebooks/05a_tool_loop_errors_and_evaluation.ipynb) · [All theory pages](../../../README.md)*

## Where tool errors go

`05a` closes the loop from lesson 23.4 with one edge, `tools` back to `agent`, and a router that ends the run when the last `AIMessage` has no tool calls. The message count tells you how the run went: *What's 25 * 17?* ends with 4 messages (question, tool call, result, answer), and *What's 100 / 4 and what's the weather in London?* with 5, because the model asked for two tools in one reply.

Then the tools fail. What matters is where the failure goes. If it reaches the model as a `ToolMessage`, the model can explain it or retry with better arguments. If it escapes as an exception, `graph.invoke` raises and the user gets nothing. There are two ways to send it to the model:

1. **The tool returns the error.** `divide` checks for zero and returns `"Error: Division by zero"`; the model reads it like any other result and explains that division by zero is undefined.
2. **The tool raises, and the `ToolNode` catches it.** That depends on `handle_tool_errors`, whose default is narrower than it looks.

| `handle_tool_errors` | Bad arguments from the model | Exception raised inside the tool |
|---|---|---|
| default | Error `ToolMessage` (`Please fix the error and try again.`) | **Re-raised: the run crashes** |
| `True` | Error `ToolMessage` (`Please fix your mistakes.`) | Error `ToolMessage` with the exception text |
| `False` | Re-raised | Re-raised |

The [interactive lab](interactive/tool-error-routing-lab.html) runs Larkspur's four golden questions through this loop under each setting. Its tool results and error texts are byte for byte what LangGraph 1.2.18 produces for the same calls (12 runs, 0 mismatches); the model's turns are scripted.

| Question | default | `True` | `False` |
|---|---|---|---|
| *Can I export my data after I cancel my plan?* | Answered, 4 messages | Answered, 4 | Answered, 4 |
| *Is my server web-1 running, and does a reboot change its IP address?* | Answered, 5 | Answered, 5 | Answered, 5 |
| *Is my server web-9 up?* (the tool raises `ValueError`) | **Crashed** | Answered, 4 | **Crashed** |
| *How long does a refund take?* (the model passes `q`, not `query`) | Answered, 6 | Answered, 6 | **Crashed** |
| Answered | 3 of 4 | 4 of 4 | 2 of 4 |

<!-- lab: interactive/tool-error-routing-lab.html -->

- **The unknown server is an execution error.** `get_server_status` raises `ValueError("Unknown server 'web-9'; your servers: ['db-1', 'web-1']")`. Only `True` catches it, and the model can then name the customer's real servers, because the exception text lists them.
- **The wrong argument name is a validation error.** The default and `True` both return it as a message, the model retries with `query`, and the run costs one extra round trip (6 messages instead of 4). `False` re-raises it as `ToolInvocationError`.
- **The two questions with no failure behave the same under every setting.** That is why a test suite with only happy-path questions never shows the difference.

Write error messages the model can act on. Say what was wrong and what would work. `handle_tool_errors` also accepts a custom string, an exception type or a tuple of them (catch only those), or a function that formats the message. Return an error yourself when the tool knows the failure (an unknown id, an empty result), and keep `handle_tool_errors=True` as the net for the failures it does not expect.

## Tool-call evaluation

A run can finish and still be wrong. For a tool-using agent, `05a` scores three things separately, all read from the message trace:

| Dimension | Question | How to score it |
|---|---|---|
| Tool selection | Did it pick the right tool or tools? | Compare called names with the golden set's expected calls |
| Tool input | Were the arguments well formed and relevant? | Validate against the schema, compare key values with the expected ones |
| Synthesis | Did the answer use what the tools returned, and nothing else? | An LLM judge or a reference answer |

The first two often need no model at all. Give each golden question its expected calls (*Is my server web-1 running, and does a reboot change its IP address?* expects `get_server_status` and `search_handbook`) and check the trace: the lab's trace column does exactly this, and marks the refund question's first call *Right tool, missing `query`*. A selection score that drops after a description change points at the description; an input score that drops points at the schema.

Synthesis needs judgement. The notebook's judge reads the trace of *Calculate 15% of 250 and check weather in Paris* and returns structured scores through `with_structured_output(ToolUseEvaluation)`: 5, 5 and 5, with a justification. Two cautions come with it:

- **The judge is the agent's own model** (`gpt-4o-mini` judging `gpt-4o-mini`), which tends to be lenient on its own work. Use a different, ideally stronger, model, and check its scores against a few human-graded runs before you trust a trend.
- **A single trace scored 5 out of 5 proves little.** The scores mean something across a fixed golden set, compared before and after one change, as with the [baseline in M11](../../../p04_rag_foundations/m11_rag_lifecycle/05_the_rag_lifecycle_and_a_measured_baseline/README.md#baseline-first-optimisation).

Add trace-level counts to the per-call scores: rounds per run, error `ToolMessage`s per tool, and crashed runs. They are cheap to log and catch the failures the lab shows, where the answer never arrives.

---
*Previous: [23.4 The manual tool loop and the augmented LLM in LangGraph](../04_the_manual_tool_loop_and_the_augmented_llm_in_langgraph/README.md). Next: [23.6 Hosted vs client-side tools: code execution and image generation](../06_hosted_vs_client_side_tools_code_execution_and_image_generation/README.md).*
