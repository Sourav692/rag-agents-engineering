# Phase 3: v2 Parts VII to IX (M25 to M34)

Parts: `p07_advanced_agents`, `p08_agentic_rag`, `p09_memory_layer`. Depends only on [Phase 0](phase-0-foundations.md). Branch: `restructure/phase-3`.

Several briefs say "your Part V system". Each solution builds it inline: `lab_kit` chunks and a vector retriever over `larkspur/`, plus an answer prompt with citations, in one cell the solution says it reuses.

### Task 3.1: Restructure the three parts

Same steps as [Task 1.1](phase-1-parts-01-03.md#task-11-restructure-the-three-parts), for these three parts. M26 is assembled from three v1 lessons (24.5, 37.4, 37.6): check that `p07_advanced_agents/m26_coding_computer_use_and_deep_agents/` has three lesson pages numbered 01 to 03, that the deep-agent files are `03a_simple_coding_agent.py`, `03b_long_term_memory_agent.py` and `03c_skills/`, and that the report lists no remaining `06c_skills` or `06a_simple_coding_agent` reference. Commit message: `content: copy v2 Parts VII to IX into the part-folder layout`.

### Tasks 3.2 to 3.11: one lab per module

Each row is one task. Follow the [lab recipe](README.md#lab-recipe-every-module-lab-task-follows-it). Every row uses `larkspur/` in `data/` unless it says otherwise.

| Task | Module | Extra `data/` contents | Run with | The solution must show |
|---|---|---|---|---|
| 3.2 | M25 Planning, Reflection & Reasoning Patterns | none | default | chain-of-verification added to the answer step; unsupported claims counted before and after (judge prompt shown) on the 25 answerable questions |
| 3.3 | M26 Coding, Computer-Use & Deep Agents | `spec.md` (the function to build: a Larkspur refund-amount calculator with its rules taken from the handbook) | default | a deep agent with a developer sub-agent and a tester sub-agent, built as `03a_simple_coding_agent.py` is; the function and its tests written to a temp folder; each iteration's test result logged until the tests pass, with an iteration cap |
| 3.4 | M27 Human Approval & Applied Single-Agent Builds | `catalogue.csv` (a product catalogue: reuse one from the module's `assets/` if its licence allows, else a fictional Larkspur plan and add-on catalogue), `questions.jsonl` (20 questions labelled lookup, filter or aggregate) | default | CSV RAG (as in M19) against a text-to-SQL agent over SQLite on the 20 questions; which wins for each question type |
| 3.5 | M28 Agentic RAG Foundations: Grading & Query Rewriting | none | default | a LangGraph graph with a relevance grader and a rewrite loop capped at two retries; how often each path fires on the 30 questions |
| 3.6 | M29 Self-Correcting RAG: CRAG & Self-RAG | `ooc_questions.jsonl` (10 more out-of-corpus questions beside the golden set's 5) | default; `TAVILY_API_KEY` | the baseline, CRAG and Self-RAG on the 15 out-of-corpus questions: refusals, web fallbacks and hallucinated answers counted per system |
| 3.7 | M30 Adaptive RAG & Query Routing | `kb/billing/`, `kb/technical/`, `kb/general/` (the handbook files split by section), `tickets.jsonl` (40 tickets labelled with route and sentiment by the author) | default | a router to three knowledge bases and escalation for negative sentiment; routing accuracy and escalation precision on the 40 tickets |
| 3.8 | M31 RAG as an Agent Tool | `mixed_questions.jsonl` (20 questions, each labelled with the tool it needs: `docs` or `web`) | default; `TAVILY_API_KEY` | an agent with a private-docs RAG tool and a web-search tool; tool-choice accuracy after each round of tool-description edits, with the descriptions shown |
| 3.9 | M32 Reliability, Feedback Loops & Diversity | none | default | 100 thumbs-up and thumbs-down events simulated with a fixed seed; a feedback-weighted reranking; rank of the target passage before and after for each affected query |
| 3.10 | M33 Short-Term Memory & Conversation State | `conversations.jsonl` (15 three-turn conversations written by the author; each turn has `evidence_spans`) | default | hit rate on turns two and three with and without history-aware query rewriting |
| 3.11 | M34 Long-Term & Agentic Memory | `preferences.jsonl` (a user's stated preferences across a first thread) | default | semantic memory in a LangGraph store with an embedding index; a second thread whose answers use the stored preferences, side by side with a no-memory run |

### Task 3.12: Close the phase

Same steps as [Task 1.11](phase-1-parts-01-03.md#task-111-close-the-phase), adding `"p07_advanced_agents", "p08_agentic_rag", "p09_memory_layer"` to `DONE_PARTS`.
