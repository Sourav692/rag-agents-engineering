# Phase 4: v2 Parts X to XII (M35 to M44)

Parts: `p10_multi_agent_systems`, `p11_agent_protocols`, `p12_knowledge_graphs_and_graph_rag`. Depends only on [Phase 0](phase-0-foundations.md). Branch: `restructure/phase-4`.

Part XI modules have `projects/` sub-projects that notebooks write into at run time. Check the restructure report for `../projects/` paths before writing those labs.

### Task 4.1: Restructure the three parts

Same steps as [Task 1.1](phase-1-parts-01-03.md#task-11-restructure-the-three-parts), for these three parts. M37 loses lessons 37.4 and 37.6 to M26: check that `p10_multi_agent_systems/m37_multi_agent_applied_builds/` has five lesson pages, that the research-system files are `04a_*` to `04c_*`, and that the five-pattern files are `05a_*` to `05e_*` (lesson 37.5, still on hold for a theory page). Commit message: `content: copy v2 Parts X to XII into the part-folder layout`.

### Tasks 4.2 to 4.11: one lab per module

Each row is one task. Follow the [lab recipe](README.md#lab-recipe-every-module-lab-task-follows-it). Every row uses `larkspur/` in `data/` unless it says otherwise.

| Task | Module | Extra `data/` contents | Run with | The solution must show |
|---|---|---|---|---|
| 4.2 | M35 Multi-Agent Architectures | `kb/` and `tickets.jsonl` (the same split and tickets as the M30 lab, copied into this lab) | default | a single router against a supervisor over three specialist RAG agents; routing accuracy and cost per ticket for both |
| 4.3 | M36 Collaboration, Control & Parallel Agents | none | default | a decomposed multi-hop question whose sub-questions run as parallel agents (`Send`), with partial answers streamed; wall-clock time sequential against parallel on the 6 multi-hop questions |
| 4.4 | M37 Multi-Agent Applied Builds | `conflicting.md` (a lab-local document that contradicts one handbook fact) | default; `TAVILY_API_KEY` | a supervisor with a RAG researcher, a web researcher and a writer that cites sources; three edge cases run: no results, conflicting sources, and a tool that raises |
| 4.5 | M38 MCP Foundations | none | `protocols` group | the retriever exposed as a tool by a FastMCP server over stdio (`solution/server.py`); an MCP client chatbot that calls it for three golden questions |
| 4.6 | M39 Building MCP Servers & Clients | none | `protocols` group; `TAVILY_API_KEY` | a retriever server and a web-search server (`solution/retriever_server.py`, `solution/web_server.py`); one client that routes between them; the routing printed for five questions |
| 4.7 | M40 MCP Applications & RAG over MCP | none | `protocols` group | the RAG-over-MCP server connected to a LangGraph agent and to a second local agent; their answers compared on five questions. A Claude Desktop config is shown in the README as an optional manual step, not run by the notebook |
| 4.8 | M41 A2A: Agent-to-Agent Protocol | none | `protocols` group | an agentic RAG graph served over A2A; a client agent built in a different framework (pick from what the `protocols` group installs, as the module's notebooks do) calling it for three questions |
| 4.9 | M42 Hierarchical & Memory-Augmented Retrieval | `global_questions.jsonl` (ten "summarise or compare across the whole handbook" questions with reference answers) | default | flat RAG, RAPTOR and LightRAG on the ten questions; answer quality per system (judge prompt shown) |
| 4.10 | M43 Knowledge Graphs with Neo4j | `extra_docs/` (enough fictional Larkspur team and incident records to reach 20 documents with the handbook), `multihop.jsonl` (five multi-hop questions with reference answers) | Docker (Neo4j) | `solution/docker-compose.yml` for Neo4j; a graph extracted from the 20 documents and loaded; the five questions answered by graph queries and by vector RAG, with the vector failures shown |
| 4.11 | M44 GraphRAG Techniques | `global_questions.jsonl` and `multihop.jsonl` (copies of the M42 and M43 sets) | default | GraphRAG, RAPTOR and a hybrid on both sets; indexing cost in tokens and seconds; a one-page recommendation in the notebook's last cell |

### Task 4.12: Close the phase

Same steps as [Task 1.11](phase-1-parts-01-03.md#task-111-close-the-phase), adding `"p10_multi_agent_systems", "p11_agent_protocols", "p12_knowledge_graphs_and_graph_rag"` to `DONE_PARTS`.
