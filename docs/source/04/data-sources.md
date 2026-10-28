# Data sources

Every data, asset or copied support file committed to this repository.

**No datasets or images are committed.** `data/sample/` is absent and no module has an `assets/` folder: every notebook here builds its state in code, and the diagrams some notebooks embed are loaded from imgur at view time. The one binary that sat beside a source notebook, `graph_code.png` in the cycles-and-loops lesson, is output the notebook writes when run, so it was dropped as generated (see `scripts/path_allowlist.txt`). The router knowledge base (`router_agent_documents.json`) and its `prompts.yaml` were deferred with the agentic-RAG router notebooks to repository 09.

## Copied support code

None. The monorepo's `helpers/` LLM factory was first copied to `src/helpers/`, then removed: notebooks now install the shared [`aied-helpers`](https://github.com/Sourav692/ai-engineering-demystified-shared) package as a dependency instead.
