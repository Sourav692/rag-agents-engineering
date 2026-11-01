# M08.2 Theory: LCEL deep dive

*[M08 theory](../README.md) · Lesson 8.2 · Notebooks: [`02a_LCEL_Deepdive.ipynb`](../../../../course/p03_langchain_and_langgraph/m08_lcel_runnables_and_chains/notebooks/02a_LCEL_Deepdive.ipynb), [`02b_LCEL_and_Runnables.ipynb`](../../../../course/p03_langchain_and_langgraph/m08_lcel_runnables_and_chains/optional/02b_LCEL_and_Runnables.ipynb) (optional) · [All theory pages](../../../README.md)*

## Pipe composition

The `|` in `prompt | model | parser` is ordinary Python. `a | b` calls `a.__or__(b)`, the same way `2 + 4` calls `(2).__add__(4)`. LangChain's `Runnable.__or__` returns a `RunnableSequence` that holds both sides, and the sequence's `invoke` runs the first step and feeds its output to the next.

Notebook 02a proves this by building the mechanism from scratch. `CRunnable.__or__` returns a `CRunnableSequence(self, other)`, and its `invoke` is `self.second.invoke(self.first.invoke(data))`. Three small steps piped together give:

```mermaid
flowchart LR
    I[/10/] --> A[AddTen] -->|20| B[MultiplyByTwo] -->|40| C[ConvertToString] --> O[/"'Result: 40'"/]
```

LangChain's real `RunnableSequence` works the same way and adds what the toy lacks: `batch`, `stream` and async on the whole pipe, tracing of every step, and flattening, so `(a | b) | c` is one sequence of three steps rather than a sequence nested in a sequence.

**A dict in a pipe becomes a `RunnableParallel`.** When the left side of `|` is a plain dict, Python calls the Runnable's `__ror__` instead, and LangChain turns the dict into a `RunnableParallel`. Each value runs on the same input and the output is a dict with the same keys. Notebook 02a's runs, which you can repeat without an API key:

| Chain | Input | Output |
|---|---|---|
| `RunnableParallel({"x": RunnablePassthrough(), "y": RunnablePassthrough()})` | `"hello"` | `{'x': 'hello', 'y': 'hello'}` |
| same, with `"y": lambda z: z["input2"]` | `{"input": "hello", "input2": "goodbye"}` | `{'x': {'input': 'hello', 'input2': 'goodbye'}, 'y': 'goodbye'}` |
| `"x": RunnablePassthrough() \| RunnableLambda(find_keys_to_uppercase)` | the same dict | `{'x': 'HELLO', 'y': 'goodbye'}` |
| `RunnableParallel({"x": RunnablePassthrough()}).assign(extra=RunnableLambda(lambda _: 100))` | the same dict | `{'x': {'input': 'hello', 'input2': 'goodbye'}, 'extra': 100}` |

Two rules follow from the table. A plain lambda in a dict is wrapped in a `RunnableLambda` for you. A branch can be a pipe of its own, so pipes nest inside dicts and dicts inside pipes.

**`.assign()` adds keys and keeps the rest.** `RunnableParallel` replaces its input with the new dict; `.assign(key=runnable)` (or `RunnablePassthrough.assign(...)`) computes the new key from the current dict and returns the old keys with it. This is how a pipe carries the question forward while later steps add `context`, then `answer`, then `sources`.

**Finished chains compose like any step.** Notebook 02a pipes the `.assign()` chain into a second chain that reads `extra` and upper-cases it; the result is the string `'100'`. Optional notebook 02b applies the same pieces to a RAG chain over a vector store.

For Larkspur, the RAG chain from lesson 8.4 is the dict rule in action:

```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)
rag_chain.invoke("How long does a refund take?")
```

The question string goes to both dict values. The retriever turns it into Documents and `format_docs` joins them into one string; the passthrough keeps the question as it is. The prompt receives `{"context": ..., "question": ...}`, which is exactly the pair of variables it declares.

## Key Takeaways

- The `|` operator calls `__or__`, which returns a flattened `RunnableSequence` that feeds each step's output to the next and adds batch, streaming, async and tracing.
- A plain dict in a pipe becomes a `RunnableParallel`: every value runs on the same input, and lambdas are wrapped for you. Pipes nest inside dicts and dicts inside pipes.
- Use `.assign()` to add a key while keeping the rest, so the question travels forward as later steps add context, answer and sources.

## Check yourself

<details>
<summary>1. What does Python actually do when you join two Runnables with the pipe operator, and what object comes back?</summary>

`a | b` calls `a.__or__(b)`, the same way `2 + 4` calls `(2).__add__(4)`. LangChain's `Runnable.__or__` returns a `RunnableSequence` holding both sides, whose `invoke` runs the first step and feeds its output to the next. It also flattens, so `(a | b) | c` is one sequence of three steps.

</details>

<details>
<summary>2. The Larkspur RAG chain starts with a plain dict of context and question. What does each value receive, and what reaches the prompt?</summary>

The dict becomes a `RunnableParallel`, so the question string goes to both values. The retriever turns it into Documents and `format_docs` joins them into one string, while the passthrough keeps the question as it is. The prompt receives `{"context": ..., "question": ...}`, exactly the two variables it declares.

</details>

<details>
<summary>3. A later step needs the original question, but the RunnableParallel before it replaced its input. What should you use instead?</summary>

`.assign()`. `RunnableParallel` replaces its input with the new dict, while `.assign(key=runnable)` computes the new key from the current dict and returns the old keys with it. That is how a pipe carries the question forward while later steps add `context`, then `answer`, then `sources`.

</details>

---
*Previous: [8.1 LCEL and the Runnable interface](../01_lcel_and_the_runnable_interface/README.md). Next: [8.3 Branching, routing and merging chains](../03_branching_routing_and_merging_chains/README.md).*
