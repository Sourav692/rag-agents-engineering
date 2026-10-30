# M08.4 Theory: Legacy chains and migration to LCEL

*[M08 theory](../README.md) · Lesson 8.4 · Notebooks: [`04a_Chain_Migrations.ipynb`](../../../../course/p03_langchain_and_langgraph/m08_lcel_runnables_and_chains/notebooks/04a_Chain_Migrations.ipynb), [`04b_Basics_of_Chains.ipynb`](../../../../course/p03_langchain_and_langgraph/m08_lcel_runnables_and_chains/optional/04b_Basics_of_Chains.ipynb) (optional), [`04c_Chains_Basics_and_OutputParsers.ipynb`](../../../../course/p03_langchain_and_langgraph/m08_lcel_runnables_and_chains/optional/04c_Chains_Basics_and_OutputParsers.ipynb) (optional), [`04d_Advanced_Chains.ipynb`](../../../../course/p03_langchain_and_langgraph/m08_lcel_runnables_and_chains/optional/04d_Advanced_Chains.ipynb) (optional), [`04e_Chain_Migration_Advanced.ipynb`](../../../../course/p03_langchain_and_langgraph/m08_lcel_runnables_and_chains/optional/04e_Chain_Migration_Advanced.ipynb) (optional) · [All theory pages](../../../README.md)*

## Legacy chains to LCEL

Before LCEL, LangChain packaged each pattern as a class: `LLMChain` for prompt plus model, `RetrievalQA` for retrieval plus answer, `load_summarize_chain` for summaries. In LangChain 1.x these classes left the `langchain` package. They live in the compatibility package `langchain-classic`, still run, and carry deprecation markers with removal set for 2.0.0. Older tutorials and older Larkspur services still use them, so each one is listed here with the pipe that replaces it.

| Legacy (0.x) | LCEL (1.x) | What changes for the caller |
|---|---|---|
| `LLMChain(llm=llm, prompt=prompt)` | `prompt \| llm \| StrOutputParser()` | the legacy chain returns a dict with the inputs and a `text` key; the pipe returns a string |
| `RetrievalQA.from_llm(llm, retriever=retriever, prompt=prompt)` | `{"context": retriever \| format_docs, "question": RunnablePassthrough()} \| prompt \| llm \| StrOutputParser()` | input key `query` and output key `result` become a plain string in and a string out |
| `load_summarize_chain(llm, chain_type=...)` | one of three short pipes (lesson 8.5) | you join the Documents into the prompt's `{text}` yourself |
| `chain({...})`, `chain.run(...)` | `chain.invoke({...})` | the call style was replaced in 0.1.0 |
| `hub.pull("rlm/rag-prompt")` | the prompt written inline in `ChatPromptTemplate.from_messages` | no network call and no untrusted object to load |

**Two deprecations per legacy cell.** Notebook 04a points out that running a legacy cell warns twice: once for the class and once for calling a chain directly with `chain({...})`. `RetrievalQA` usually warns more often, because it builds a `StuffDocumentsChain` and an `LLMChain` inside itself, and both are deprecated too.

**`hub.pull` fails outright.** `langchain_classic.hub.pull` is deprecated since 1.0.6, and on the repo's pinned `langsmith` it raises `ValueError: Pulling a public prompt by owner/name is disabled by default because prompts may contain untrusted serialized LangChain objects.` Notebook 04a lists the three options in order: inline the prompt, call `langsmith.Client().pull_prompt(..., dangerously_pull_public_prompt=True)` and accept the risk, or keep `hub.pull`, which raises.

**No warning at build time.** Notebook 05b shows that `load_summarize_chain(llm, chain_type="stuff")` returns a deprecated `StuffDocumentsChain` and emits no warning when it is built. The only warning arrives when `.run()` is called, and it is about `.run()`, not about the class. Code built this way keeps working until 2.0 removes it, which is why audits should grep for imports from `langchain_classic` rather than wait for warnings.

**A migration that does not break callers.**

1. Repoint the imports to `langchain_classic` so the service runs on 1.x unchanged.
2. Replace one chain with its pipe behind the same function, mapping the output shape: callers that read `result["result"]` from `RetrievalQA` now receive the string itself.
3. Replace `chain(...)` and `.run()` with `.invoke()`.
4. Run a fixed question set through old and new versions and compare answers before you delete the old class.

The optional notebooks show more legacy classes: 04b builds `LLMChain` and `SimpleSequentialChain`, 04c adds `StructuredOutputParser`, 04d covers `SequentialChain` and the router class `MultiPromptChain` (whose LCEL form is lesson 8.3's `RunnableBranch`), and 04e rewrites `ConversationalRetrievalChain` as a rephrase pipe followed by a retrieval pipe.

---
*Previous: [8.3 Branching, routing and merging chains](../03_branching_routing_and_merging_chains/README.md). Next: [8.5 Summarization: stuff, map-reduce, refine](../05_summarization_stuff_map_reduce_refine/README.md).*
