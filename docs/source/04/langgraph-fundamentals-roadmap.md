# LangGraph Fundamentals Tutorial Roadmap

A notebook-based learning roadmap for this repository: **12 modules, 19 notebooks**, progressing from graph construction to persistent, interactive, asynchronous workflows.

Follow modules **01 → 12**, and run each module's notebooks in their numbered order. Module names match the repository folders. Topics below come from the notebooks' explanations and code examples.

## Before you start

Know Python functions and type hints (`TypedDict`, `Annotated`, `Literal`), basic `async`/`await`, Pydantic, LangChain chat messages, and Jupyter. No prior LangGraph knowledge is required. See [Prerequisites](prerequisites.md) and [Setup](setup.md).

**API access:** 10 notebooks run without an API key; 8 use an LLM; the graph-basics notebook needs an LLM only for its final conversation section. The existing LLM examples use `OPENAI_API_KEY`; see each module's README for details.

## Learning sequence

| Stage | Modules | Learning goal |
|---|---|---|
| 1. Build and control graphs | 01–04 | Define state, merge updates, route execution, choose schemas, and pass configuration and context into nodes. |
| 2. Persist and interact | 05–07 | Save and inspect runs, pause for human input, resume execution, and define public input/output contracts. |
| 3. Compose and execute | 08–11 | Compose subgraphs, run asynchronously, stream progress and tokens, retry failures, and bound graph loops. |
| 4. Apply the mechanics | 12 | Combine state, persistence, human review, recovery, parallel execution, and replay in deterministic examples. |

## Module 01 — Graphs, State and Reducers

Learn how a graph executes and how node updates change shared state.

### [01_State_and_Graph_Basics.ipynb](../modules/01_graphs_state_and_reducers/notebooks/01_State_and_Graph_Basics.ipynb)

**Topics covered:**

- **`StateGraph`:** Create a graph builder around a shared state schema.
- **`TypedDict` state:** Define the fields that nodes read and update.
- **Node functions:** Return partial state updates from each processing step.
- **Normal edges:** Connect nodes in a fixed execution order.
- **`START` and `END`:** Mark the graph entry and termination points.
- **Graph lifecycle:** Build, compile, invoke, and visualize a graph.
- **Sequential pipelines:** Pass state through multiple processing nodes.
- **Default updates:** Observe how a field is overwritten without a reducer.
- **`Annotated` reducers:** Specify how incoming updates merge with existing state.
- **Custom numeric reducers:** Combine numeric updates using a custom merge function.
- **`add_messages`:** Merge message updates into conversation state.
- **LLM conversations:** Call a chat model from a node and manually carry history across turns.

### [02_MessagesState.ipynb](../modules/01_graphs_state_and_reducers/notebooks/02_MessagesState.ipynb)

**Topics covered:**

- **`MessagesState`:** Use the prebuilt message-state schema with its inherited reducer.
- **Custom state fields:** Extend `MessagesState` with additional workflow data.
- **Message types:** Add `HumanMessage` and `AIMessage` objects to state.
- **Mixed state updates:** Accumulate messages while updating an ordinary counter across multiple nodes.

**Ready to move on when:** you can build a small graph and predict whether each state field is overwritten or merged.

## Module 02 — Conditional Edges and LLM Nodes

Choose a path from state and use a chat model inside a graph node.

### [01_Conditional_Routing.ipynb](../modules/02_conditional_edges_and_llm_nodes/notebooks/01_Conditional_Routing.ipynb)

**Topics covered:**

- **Edge types:** Compare fixed execution paths with conditional branches.
- **Routing functions:** Choose the next destination from the current state.
- **`add_conditional_edges`:** Attach a routing function to a source node.
- **Route mappings:** Map routing labels to destination node names.
- **Two-way branching:** Route a weather example to rainy or sunny processing.
- **Multi-branch routing:** Choose among several topic-specific processing paths.
- **Branch termination:** Connect each completed path to `END`.

### [02_LLM_Powered_Chatbot.ipynb](../modules/02_conditional_edges_and_llm_nodes/notebooks/02_LLM_Powered_Chatbot.ipynb)

**Topics covered:**

- **Chatbot state:** Store the conversation as a sequence of messages.
- **`add_messages`:** Merge new user and assistant messages into the conversation.
- **LLM nodes:** Invoke a chat model inside a graph node.
- **Conversation context:** Pass the accumulated message history to the model.
- **Invocation versus streaming:** Compare `invoke()` results with incremental `stream()` output.
- **`values` streaming:** Observe complete state snapshots during execution.
- **`updates` streaming:** Observe the state changes returned by individual nodes.
- **History limitations:** Understand how conversation history is handled without checkpointing.

**Ready to move on when:** you can route to different nodes and explain the difference between a final result, a state snapshot, and a node update.

## Module 03 — State Schemas

Choose a state representation and understand what validates at runtime.

### [01_Different_Graph_States.ipynb](../modules/03_state_schemas/notebooks/01_Different_Graph_States.ipynb)

**Topics covered:**

- **Dictionary state:** Represent graph state with a plain dictionary.
- **`TypedDict` state:** Describe dictionary fields using type hints.
- **Dataclass state:** Define structured state with attribute access and defaults.
- **Pydantic state:** Use `BaseModel` for a runtime-validated state representation.
- **State access:** Compare dictionary lookup with attribute access across schemas.
- **Defaults and type hints:** Compare how state representations declare values and types.
- **Custom reducers:** Attach merge behavior to fields using `Annotated`.
- **Schema comparison:** Run the same graph with different state representations.

### [02_Pydantic_State_Validation.ipynb](../modules/03_state_schemas/notebooks/02_Pydantic_State_Validation.ipynb)

**Topics covered:**

- **`TypedDict` enforcement:** Observe that type hints alone do not validate inputs at runtime.
- **Pydantic validation:** Validate incoming state at graph entry.
- **Valid and invalid inputs:** Compare successful runs with rejected state values.
- **`ValidationError`:** Inspect the error raised when input violates a Pydantic schema.
- **State access styles:** Compare dictionary fields with Pydantic model attributes.
- **Message reducers:** Use `add_messages` with both `TypedDict` and Pydantic schemas.

**Ready to move on when:** you can choose a schema and explain why type hints alone do not reject invalid input.

## Module 04 — Nodes, Runtime Context and Commands

Control node inputs and combine state updates with routing decisions.

### [01_Node_Patterns.ipynb](../modules/04_nodes_runtime_context_and_commands/notebooks/01_Node_Patterns.ipynb)

**Topics covered:**

- **State-only nodes:** Define a node that receives only graph state.
- **Config-aware nodes:** Accept `RunnableConfig` alongside state.
- **Runtime-aware nodes:** Accept `Runtime[Context]` alongside state.
- **Request configuration:** Read configurable values supplied for a graph invocation.
- **Typed context schemas:** Declare the context available to runtime-aware nodes.
- **Context passing:** Supply execution context when invoking a graph.

### [02_Runtime_Context.ipynb](../modules/04_nodes_runtime_context_and_commands/notebooks/02_Runtime_Context.ipynb)

**Topics covered:**

- **Dependency injection:** Pass execution dependencies through `context_schema`.
- **Dataclass context:** Define typed context fields with default values.
- **`runtime.context`:** Access injected context inside a node.
- **Context overrides:** Compare runs using default and explicitly supplied context.
- **State versus context:** Separate mutable workflow data from execution dependencies.

### [03_Command_Objects.ipynb](../modules/04_nodes_runtime_context_and_commands/notebooks/03_Command_Objects.ipynb)

**Topics covered:**

- **`Command` returns:** Return a control-flow object from a graph node.
- **Combined updates and routing:** Use `Command(update=..., goto=...)` to change state and choose the next node.
- **Destination annotations:** Declare possible destinations with `Command[Literal[...]]`.
- **Branch testing:** Run both paths of a temperature-check graph.

**Ready to move on when:** you can distinguish state, request configuration, and runtime context, and route with `Command`.

## Module 05 — Checkpointing

Give runs an identity and inspect or reuse their saved state.

### [01_Checkpointing.ipynb](../modules/05_checkpointing/notebooks/01_Checkpointing.ipynb)

**Topics covered:**

- **Checkpointer integration:** Compile a graph with a saver to record execution state.
- **`MemorySaver`:** Store checkpoints in memory for the current process.
- **`SqliteSaver`:** Persist checkpoints in SQLite and reopen saved state.
- **Thread identity:** Use `thread_id` to identify a conversation or workflow.
- **Conversation persistence:** Reuse saved messages across multiple turns.
- **State inspection:** Read the current thread snapshot with `get_state()`.
- **Checkpoint history:** Inspect earlier snapshots with `get_state_history()`.
- **Conversation branching:** Copy saved state into separate threads using `update_state()`.
- **Checkpoint anatomy:** Inspect checkpoint IDs, metadata, pending nodes, and saved state.

**Ready to move on when:** you can inspect a thread's state and history, and distinguish in-memory storage from persistence across restarts.

## Module 06 — Interrupts and Human-in-the-Loop

Pause execution for a person, inspect or edit state, and continue the same workflow.

### [01_HITL_Mechanics.ipynb](../modules/06_interrupts_and_human_in_the_loop/notebooks/01_HITL_Mechanics.ipynb)

**Topics covered:**

- **Runtime interrupts:** Pause execution with an `interrupt()` payload.
- **Persistence requirements:** Attach a checkpointer and identify the paused thread.
- **Runtime resume:** Supply human input through `Command(resume=...)`.
- **Static interrupts:** Pause before or after selected nodes with `interrupt_before` and `interrupt_after`.
- **Static resume:** Continue a static pause using `invoke(None, config)`.
- **Resume lifecycle:** Observe interrupted-node re-execution when a runtime interrupt resumes.
- **Human input validation:** Repeat interrupts until the supplied input is valid.

### [02_LangGraph_Interrupt_Primitive.ipynb](../modules/06_interrupts_and_human_in_the_loop/notebooks/02_LangGraph_Interrupt_Primitive.ipynb)

**Topics covered:**

- **Review workflow:** Build a draft → human review → finalize graph by hand.
- **Arbitrary pause points:** Place a human gate wherever the workflow needs review.
- **Interrupt inspection:** Read the review payload exposed through `__interrupt__`.
- **Checkpoint-backed suspension:** Preserve workflow state while waiting for a human response.
- **Custom resume payloads:** Resume with approval or an edited plan.
- **Primitive and middleware:** Understand the relationship between raw interrupts and the middleware mentioned in the recap.

### [03_HITL_Patterns.ipynb](../modules/06_interrupts_and_human_in_the_loop/notebooks/03_HITL_Patterns.ipynb)

**Topics covered:**

- **Assistant pause points:** Interrupt execution before an assistant node.
- **Paused-state inspection:** Inspect and edit conversational state before continuing.
- **Human-feedback nodes:** Make the review step explicit in the graph structure.
- **Attributed updates:** Apply human feedback with `update_state(..., as_node=...)`.
- **Approve/reject routing:** Choose an approved or rejected path using `Command`.
- **Edit/review workflows:** Let a person revise generated output before downstream processing.
- **Tool-call review:** Inspect a requested tool action before it executes.
- **Reusable review wrappers:** Add a human-review step around an existing tool.

**Ready to move on when:** you can pause and resume a thread, and explain why code before a runtime interrupt may run again.

## Module 07 — Input/Output Schemas and Configuration

Define a narrow public interface while nodes use richer internal state.

### [01_Advanced_State.ipynb](../modules/07_input_output_schemas_and_configuration/notebooks/01_Advanced_State.ipynb)

**Topics covered:**

- **Schema boundaries:** Compare one shared schema with separate `InputState`, `OutputState`, and `PrivateState` schemas.
- **Combined internal state:** Use `OverallState` to make all internal fields available to nodes.
- **Public input/output:** Restrict the external interface with `input_schema` and `output_schema`.
- **Private bookkeeping:** Keep internal fields such as an LLM call counter out of the public interface.
- **Config-aware nodes:** Accept request settings through `RunnableConfig`.
- **Configurable values:** Read per-invocation settings from `config["configurable"]`.
- **Response-language configuration:** Change the model response language for each invocation.

**Ready to move on when:** you can expose only the needed input/output fields and pass a per-request setting through configuration.

## Module 08 — Subgraphs

Reuse a compiled graph inside a larger graph.

### [01_Subgraphs.ipynb](../modules/08_subgraphs/notebooks/01_Subgraphs.ipynb)

**Topics covered:**

- **Standalone subgraphs:** Build, visualize, and invoke a child graph independently.
- **Model/tool loop:** Use a weather-tool example as the child workflow.
- **Shared-state embedding:** Add a compiled subgraph directly as a parent node when state keys are shared.
- **Different-schema wrappers:** Invoke a subgraph through a wrapper when parent and child schemas differ.
- **Boundary transformations:** Map parent inputs into child state and child outputs back into parent state.

**Ready to move on when:** you can choose direct subgraph embedding or a wrapper based on the parent/child state boundary.

## Module 09 — Async and Streaming

Run graph nodes asynchronously and observe intermediate results.

### [01_Async_and_Streaming.ipynb](../modules/09_async_and_streaming/notebooks/01_Async_and_Streaming.ipynb)

**Topics covered:**

- **Synchronous baseline:** Build a tool-calling graph before converting its execution to async.
- **Message and tool nodes:** Use `MessagesState`, `ToolNode`, and conditional routing for the tool loop.
- **Persisted conversations:** Reuse checkpoint-backed state across multiple turns.
- **Async node functions:** Convert a processing node to `async def`.
- **Async model calls:** Await the model response with `model.ainvoke()`.
- **Async graph invocation:** Run the complete graph with `graph.ainvoke()`.
- **Progress streaming:** Consume node updates through `astream(..., stream_mode="updates")`.
- **Token streaming:** Receive model message chunks with `stream_mode="messages"`.
- **Chunk metadata:** Inspect metadata accompanying streamed message chunks.
- **Chunk assembly:** Combine `AIMessageChunk` objects into a complete response.

**Ready to move on when:** you can run an async graph and choose between progress updates and streamed model tokens.

## Module 10 — Retry Policies

Retry transient node failures with an explicit policy.

### [01_Retries.ipynb](../modules/10_retry_policies/notebooks/01_Retries.ipynb)

**Topics covered:**

- **Node retry policies:** Attach `RetryPolicy` using `add_node(..., retry_policy=...)`.
- **Transient failures:** Observe a flaky simulated API that raises a custom exception.
- **Attempt limits:** Bound execution attempts with `max_attempts`.
- **Initial delay:** Set the first retry interval with `initial_interval`.
- **Backoff growth:** Increase retry delays using `backoff_factor`.
- **Maximum delay:** Cap retry intervals with `max_interval`.
- **Jitter:** Add randomness to exponential backoff delays.
- **Selective retries:** Choose retryable exception types with `retry_on`.
- **Exhausted attempts:** Handle the error when the retry policy reaches its limit.

**Ready to move on when:** you can select which errors to retry and explain what happens when the attempt limit is reached.

## Module 11 — Cycles and Loops

Repeat graph steps until a success condition or iteration limit ends the run.

### [01_Cycles_and_Loops.ipynb](../modules/11_cycles_and_loops/notebooks/01_Cycles_and_Loops.ipynb)

**Topics covered:**

- **Loop-back edges:** Route execution back to an earlier node using conditional edges.
- **Termination guards:** Stop loops using iteration counters and explicit limits.
- **Accumulated state:** Append errors and findings with an `operator.add` reducer.
- **Self-correcting generation:** Repeat a generate → validate → regenerate code workflow.
- **Code validation:** Check generated code for syntax errors, runtime errors, and failing test cases.
- **Iterative research:** Generate follow-up questions that guide subsequent research rounds.
- **Depth limits:** Bound the number of research iterations.
- **Final synthesis:** Combine accumulated findings after the loop finishes.

**Ready to move on when:** you can build a bounded loop and distinguish workflow-level refinement from retrying a failed node.

## Module 12 — State Management in Practice

Consolidate the earlier mechanics and learn additional state-management patterns through deterministic mocks. **No LLM API key is required.**

### [01_LangGraph_State_Management.ipynb](../modules/12_state_management_in_practice/notebooks/01_LangGraph_State_Management.ipynb)

**Topics covered:**

- **State schema and reducers (§1):** Merge partial updates using overwrite, append, `operator.add` event logs, and `add_messages`.
- **Checkpointing (§2):** Save superstep checkpoints with a saver and inspect current state and history.
- **Thread isolation and restarts (§3):** Separate runs with `thread_id` and recover SQLite-backed state through a new graph connection.
- **Explicit state machine (§4):** Model a refund workflow with named steps, risk-based routing, and legal transitions.
- **Human-in-the-loop (§5):** Persist a waiting state, inspect its interrupt payload and pending human gate, and resume an approval.
- **Crash recovery (§6):** Inspect a failed thread and continue with `invoke(None, config)` while preserving completed work.
- **Idempotency and retries (§7):** Combine targeted `RetryPolicy` retries with idempotency keys and a mock ledger to avoid duplicate side effects.
- **Parallel fan-out and merge conflicts (§8):** Observe `InvalidUpdateError` from conflicting branch writes and merge outputs with a reducer.
- **Time travel (§9):** Select historical checkpoints, replay execution, and fork with `update_state()` before continuing the returned configuration.
- **Context-window management (§10):** Prune messages by ID with `RemoveMessage` while retaining recent context and a separate event log.
- **Async execution (§11):** Run async nodes with `ainvoke()` and stream node updates through `astream()`.

**Ready to finish when:** you can trace a workflow through normal execution, a human pause, a failure, and a replay or fork, and explain how its state changes.

## Coverage boundaries and cross-references

- **Tool-calling graphs are example scaffolding** in modules 06, 08, and 09. The learning goals here are human review, graph composition, and async execution. The full agent-design curriculum lives in repository 06, linked from the [repository README](../README.md#out-of-scope).
- **Additional topics concentrated in module 12:** crash recovery (§6), idempotent side effects (§7), parallel merge conflicts (§8), historical replay/fork (§9), and message pruning (§10). These are part of this roadmap even though they have no separate module folders.
- **Example scope:** the module 12 execution ledger is an in-memory demonstration of idempotency. Durable ledgers, production operations, retrieval, and multi-agent system design belong to the later curricula described in the [README](../README.md#out-of-scope).
- **Existing references:** use the [Curriculum Map](curriculum-map.md) for one-line notebook objectives and the [full course Learning Path](learning-path.md) for this repository's place in the wider course.

