# LangGraph fundamentals - interview cheatsheet

24 patterns from 19 notebooks across all 12 repository modules. Print the PDF on A3 landscape.

Independent patterns: g = builder; app = compiled graph. Supply named nodes, schemas, llm/tools, and inputs; cfg carries thread_id.

## Core imports

```python
from typing import Annotated, Literal, TypedDict
from operator import add
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command, interrupt, RetryPolicy
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
```

## State - What moves through the graph

### 01. State + reducers (modules 01, 12)

Plain keys overwrite; reducers merge updates, so return only the new delta.

```python
class State(TypedDict):
    n: int
    events: Annotated[list[str], add]
def step(s):
    return {"n": s["n"] + 1,
            "events": ["step"]}
```

### 02. Build, compile, invoke (modules 01)

Nodes return partial updates; edges order work; compile creates the runnable.

```python
g = StateGraph(State)
g.add_node("step", step)
g.add_edge(START, "step")
g.add_edge("step", END)
app = g.compile()
app.invoke({"n": 0, "events": []})
```

### 03. MessagesState + LLM node (modules 01, 02)

add_messages appends new IDs and replaces matching IDs; return the new reply.

```python
class Chat(MessagesState):
    topic: str
def chat(s):
    reply = llm.invoke(s["messages"])
    return {"messages": [reply]}
g = StateGraph(Chat)
```

### 04. Choose a state schema (modules 03)

TypedDict is hints; dataclass adds defaults; Pydantic validates node inputs.

```python
from dataclasses import dataclass
from pydantic import BaseModel
@dataclass
class Defaults: n: int = 0
class Validated(BaseModel):
    n: int = 0
```

### 05. Input / internal / output (modules 07)

Separate the public I/O contract from internal channels; schemas are not access control.

```python
class Input(TypedDict): question: str
class Output(TypedDict): answer: str
class Internal(Input, Output): calls: int
g = StateGraph(Internal,
    input_schema=Input,
    output_schema=Output)
```

### 06. Prune model context (modules 12)

RemoveMessage deletes by ID with add_messages; preserve valid tool-call pairs.

```python
from langchain_core.messages import RemoveMessage
def trim(s):
    old = s["messages"][:-2]
    return {"messages": [
        RemoveMessage(id=m.id) for m in old
    ]}
```

## Flow - Where execution goes next

### 07. Conditional edges (modules 02)

A router reads state and selects a registered destination without updating state.

```python
def route(s):
    return "yes" if s["n"] > 0 else "no"
g.add_conditional_edges("check", route,
    {"yes": "accept", "no": "reject"})
```

### 08. Command = update + route (modules 04)

Command changes state and chooses the next node; static outgoing edges still run.

```python
def decide(s) -> Command[Literal["done"]]:
    return Command(
        update={"n": s["n"] + 1},
        goto="done")
```

### 09. Guard a cycle (modules 11)

Loop until success or an explicit cap; recursion_limit counts supersteps, not node calls.

```python
def again(s):
    stop = s["ok"] or s["n"] >= 3
    return END if stop else "work"
g.add_conditional_edges("check", again)
g.add_edge("work", "check")
app.invoke(inputs, {"recursion_limit": 20})
```

### 10. Subgraph: shared keys (modules 08)

A compiled child can be a parent node when their state channels overlap.

```python
child = child_builder.compile()
g.add_node("child", child)
g.add_edge(START, "child")
g.add_edge("child", END)
```

### 11. Subgraph: map schemas (modules 08)

Wrap the child invocation to translate the parent input and child output.

```python
def adapt(s):
    out = child.invoke({"text": s["task"]})
    return {"result": out["answer"]}
g.add_node("child_adapter", adapt)
```

### 12. Tool-call loop (modules 06, 08, 09)

Bind tools to the model; route AI tool calls to ToolNode, then return to the LLM.

```python
from langgraph.prebuilt import (
    ToolNode, tools_condition)
llm = llm.bind_tools(tools)
g.add_node("tools", ToolNode(tools))
g.add_conditional_edges("assistant", tools_condition)
g.add_edge("tools", "assistant")
```

## Runtime - How each run executes

### 13. Per-run configuration (modules 04, 07)

RunnableConfig carries thread identity, tracing settings, and configurable run options.

```python
from langchain_core.runnables import RunnableConfig
def node(s, config: RunnableConfig):
    lang = config["configurable"]["language"]
    return {"answer": lang}
app.invoke(inputs, {"configurable": {
    "thread_id": "t1", "language": "Hindi"}})
```

### 14. Runtime context (modules 04)

Inject read-only run dependencies through context; graph updates belong in state.

```python
from langgraph.runtime import Runtime
class Ctx(TypedDict): user_id: str
def node(s, runtime: Runtime[Ctx]):
    return {"owner": runtime.context["user_id"]}
g = StateGraph(S, context_schema=Ctx)
app.invoke(inputs, context={"user_id": "u1"})
```

### 15. Async node + ainvoke (modules 09, 12)

Await I/O in async nodes and use ainvoke for the completed graph result.

```python
async def chat(s):
    reply = await llm.ainvoke(s["messages"])
    return {"messages": [reply]}
g.add_node("assistant", chat)
result = await app.ainvoke(inputs, cfg)
```

### 16. Stream updates / values / tokens (modules 02, 09)

updates emits node deltas; values emits full state; messages emits LLM chunks + metadata.

```python
for state in app.stream(inputs, cfg,
    stream_mode="values"): print(state)
async for delta in app.astream(inputs, cfg,
    stream_mode="updates"): print(delta)
async for chunk, meta in app.astream(inputs, cfg,
    stream_mode="messages"): print(chunk.content)
```

### 17. Retry transient failures (modules 10, 12)

Retry only matching errors with backoff; max_attempts includes the first attempt.

```python
g.add_node("fetch", fetch,
    retry_policy=RetryPolicy(
        max_attempts=3, initial_interval=1,
        backoff_factor=2, max_interval=10,
        jitter=True, retry_on=ConnectionError))
```

### 18. Parallel fan-out + merge (modules 12)

Same-step writes to one plain key conflict; use a suitable reducer and explicit join.

```python
class Totals(TypedDict):
    score: Annotated[int, add]
g.add_edge(START, "a")
g.add_edge(START, "b")
g.add_edge(["a", "b"], "join")
```

## Persistence - How work pauses and returns

### 19. Checkpoint + thread identity (modules 05, 12)

Reuse thread_id to restore progress; RAM is for tests, SQLite persists to disk.

```python
app = g.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "t1"}}
app.invoke(inputs, cfg)
with SqliteSaver.from_conn_string("ck.db") as db:
    app = g.compile(checkpointer=db)
    app.invoke(inputs, cfg)
```

### 20. Inspect, replay, fork (modules 05, 12)

Inspect values/next/tasks; replay reruns later work; update_state applies reducers and forks.

```python
snap = app.get_state(cfg)
hist = list(app.get_state_history(cfg))
prior = next(cp for cp in hist if cp.next)
app.invoke(None, prior.config)
fork = app.update_state(prior.config, {"n": 99})
app.invoke(None, fork)
```

### 21. Interrupt: approve / reject (modules 06)

A dynamic pause needs a saver and thread; resume restarts the node from its beginning.

```python
def review(s):
    decision = interrupt("Approve?")
    return Command(goto="yes" if
        decision == "approve" else "no")
app.invoke(Command(resume="approve"), cfg)
```

### 22. Interrupt: edit / validate (modules 06)

Resume supplies the interrupt return value; validate it before returning an update.

```python
def edit(s):
    text = interrupt({"draft": s["draft"]})
    while not isinstance(text, str):
        text = interrupt("Enter text")
    return {"draft": text}
app.invoke(Command(resume="new draft"), cfg)
```

### 23. Breakpoint / crash recovery (modules 06, 12)

Static pauses and repaired failures continue with None; dynamic pauses use Command(resume=...).

```python
app = g.compile(
    checkpointer=InMemorySaver(),
    interrupt_before=["review"])
app.invoke(inputs, cfg)
app.update_state(cfg, {"n": 7})
app.invoke(None, cfg)
```

### 24. Idempotent effects (modules 12)

Retries can repeat effects; use durable atomic deduplication or a provider idempotency key.

```python
ledger = {}  # Single-process sketch only
def pay_once(key):
    if key not in ledger:
        ledger[key] = provider_pay(key)
    return ledger[key]
```

## Interview recall

Interview recall: state stores data | edges choose work | reducers merge writes | checkpoints save progress | interrupts pause durably.

Watch for: returning full history to an append reducer; effects before interrupt(); expecting checkpoints to guarantee exactly-once effects.

## Notebook sources

- [01_graphs_state_and_reducers: 01_State_and_Graph_Basics](../../modules/01_graphs_state_and_reducers/notebooks/01_State_and_Graph_Basics.ipynb)

- [01_graphs_state_and_reducers: 02_MessagesState](../../modules/01_graphs_state_and_reducers/notebooks/02_MessagesState.ipynb)

- [02_conditional_edges_and_llm_nodes: 01_Conditional_Routing](../../modules/02_conditional_edges_and_llm_nodes/notebooks/01_Conditional_Routing.ipynb)

- [02_conditional_edges_and_llm_nodes: 02_LLM_Powered_Chatbot](../../modules/02_conditional_edges_and_llm_nodes/notebooks/02_LLM_Powered_Chatbot.ipynb)

- [03_state_schemas: 01_Different_Graph_States](../../modules/03_state_schemas/notebooks/01_Different_Graph_States.ipynb)

- [03_state_schemas: 02_Pydantic_State_Validation](../../modules/03_state_schemas/notebooks/02_Pydantic_State_Validation.ipynb)

- [04_nodes_runtime_context_and_commands: 01_Node_Patterns](../../modules/04_nodes_runtime_context_and_commands/notebooks/01_Node_Patterns.ipynb)

- [04_nodes_runtime_context_and_commands: 02_Runtime_Context](../../modules/04_nodes_runtime_context_and_commands/notebooks/02_Runtime_Context.ipynb)

- [04_nodes_runtime_context_and_commands: 03_Command_Objects](../../modules/04_nodes_runtime_context_and_commands/notebooks/03_Command_Objects.ipynb)

- [05_checkpointing: 01_Checkpointing](../../modules/05_checkpointing/notebooks/01_Checkpointing.ipynb)

- [06_interrupts_and_human_in_the_loop: 01_HITL_Mechanics](../../modules/06_interrupts_and_human_in_the_loop/notebooks/01_HITL_Mechanics.ipynb)

- [06_interrupts_and_human_in_the_loop: 02_LangGraph_Interrupt_Primitive](../../modules/06_interrupts_and_human_in_the_loop/notebooks/02_LangGraph_Interrupt_Primitive.ipynb)

- [06_interrupts_and_human_in_the_loop: 03_HITL_Patterns](../../modules/06_interrupts_and_human_in_the_loop/notebooks/03_HITL_Patterns.ipynb)

- [07_input_output_schemas_and_configuration: 01_Advanced_State](../../modules/07_input_output_schemas_and_configuration/notebooks/01_Advanced_State.ipynb)

- [08_subgraphs: 01_Subgraphs](../../modules/08_subgraphs/notebooks/01_Subgraphs.ipynb)

- [09_async_and_streaming: 01_Async_and_Streaming](../../modules/09_async_and_streaming/notebooks/01_Async_and_Streaming.ipynb)

- [10_retry_policies: 01_Retries](../../modules/10_retry_policies/notebooks/01_Retries.ipynb)

- [11_cycles_and_loops: 01_Cycles_and_Loops](../../modules/11_cycles_and_loops/notebooks/01_Cycles_and_Loops.ipynb)

- [12_state_management_in_practice: 01_LangGraph_State_Management](../../modules/12_state_management_in_practice/notebooks/01_LangGraph_State_Management.ipynb)

## API checks

Examples follow the repository environment: LangGraph 1.2.12.

- [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)

- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

- [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)

- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
