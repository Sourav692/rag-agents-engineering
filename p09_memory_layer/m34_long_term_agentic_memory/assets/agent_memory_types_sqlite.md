# Agent Memory Types — One Agent, Every Layer, One SQLite File

Companion notes for `06_combined_memory_agent_sqlite.ipynb`, the capstone of module 03. The notebooks before it build one memory layer each; the capstone runs all five in one LangGraph agent. This document explains how the layers fit together, what scopes each one, who writes it, and walks through the notebook's end-to-end demo. For the theory of each layer and the cross-cutting gotchas, see [`memory_layers_guide.md`](memory_layers_guide.md).

---

## The five layers at a glance

| Layer | Scope key | Who writes, and how | How the agent reads it | Where it lives |
|---|---|---|---|---|
| **Short-term (working)** | `thread_id` | the checkpointer, after every graph step | full replay of the thread | `SqliteSaver`: `checkpoints`, `writes` tables |
| **Session** | `session_id` | the app, with a TTL | preloaded into the system prompt | `SqliteStore`, namespace `("session", session_id)` |
| **Semantic** | `user_id` | the model, through a tool, one stable key per fact (upsert) | preloaded, with keys | `("semantic", user_id)` |
| **Episodic** | `user_id` | a graph node after each finished task; append, then prune | newest N preloaded | `("episodic", user_id)` |
| **Procedural** | `agent_id` | a human, after approval | highest approved version preloaded | `("procedures", agent_id)` |

All five live in one file, `agent_memory.db`. The checkpointer owns the `checkpoints` and `writes` tables; the four store layers share the store's single table and are kept apart by their namespaces.

---

## 1. One file, two persistence primitives

```python
store = SqliteStore(sqlite3.connect(DB_PATH, check_same_thread=False, isolation_level=None))
store.setup()
checkpointer = SqliteSaver(sqlite3.connect(DB_PATH, check_same_thread=False))
checkpointer.setup()
```

Each primitive opens its own connection to the same file. `isolation_level=None` lets `SqliteStore` run its own `BEGIN`/`COMMIT`. The graph is compiled with both: `builder.compile(checkpointer=checkpointer, store=store)`.

## 2. Scope keys, side by side

| Id | Passed as | Scopes | Lives as long as |
|---|---|---|---|
| `thread_id` | `config["configurable"]` | one conversation's messages | the checkpointer keeps the thread |
| `session_id` | `context` | one visit, across all of its threads | the session item's TTL |
| `user_id` | `context` | one person, across all visits | until deleted |
| `agent_id` | `context` | one agent's (or tenant's) procedures | until retired |

Every id comes from the server — the chat window, the visit, the login, the deployment — never from the model. The three context ids travel in one dataclass:

```python
@dataclass
class Context:
    user_id: str
    session_id: str
    agent_id: str = "ops-assistant"

agent.invoke({"messages": [HumanMessage(text)]},
             {"configurable": {"thread_id": "priya-thread-1"}},
             context=Context(user_id="u-priya", session_id="priya-visit-1"))
```

Nodes read the context and the store from `runtime: Runtime[Context]`; tools from `runtime: ToolRuntime[Context]`. That runtime parameter is not part of a tool's schema, so the model cannot pass a different `user_id`.

## 3. One write rule per layer

**Semantic — the model upserts.** `save_user_fact(key, fact)` writes `store.put(("semantic", user_id), key, ...)`. The preload shows each fact as `[key] fact`, so when a fact changes the model reuses its key and the item is overwritten instead of duplicated.

**Episodic — a node appends and prunes.** In test runs, gpt-4o-mini given a `save_episode` tool and a system-prompt rule never saved an episode on its own (0 of 6). So the capstone adds a `record_episode` node that runs after every final answer. It asks the LLM for a structured summary in which the model must quote the work request from the user's own words. Code then checks that the quote really appears in the message: if it does, the turn becomes a new episode under a fresh key, and the oldest episodes past `MAX_EPISODES` are deleted.

**Session — the app writes, with a TTL.** `store.put(("session", session_id), "preferences", {...}, ttl=30)`. The per-item `ttl=` means only session items expire; facts, episodes and procedures don't. On `SqliteStore`, an expired item stays readable until `sweep_ttl()` (or a background sweeper) deletes it.

**Procedural — a human approves.** Procedures are versioned items with a `status`. The agent reads only the highest `approved` version of each procedure name; a `proposed` v2 has no effect until someone approves it (the `interrupt()` flow of `05_long_term_procedural_memory_sqlite.ipynb`).

## 4. The graph

```
START → agent ─┬─(tool call)──→ tools → agent
               └─(final answer)→ record_episode → END
```

1. `agent` reads all four store layers with the ids from `runtime.context` and builds one system prompt: facts with keys, recent episodes, the session instruction and the approved procedures.
2. While the model calls `save_user_fact`, the graph loops through `tools`.
3. When the model answers, `record_episode` decides whether the turn was a task and, if so, appends and prunes.
4. The checkpointer saves every step under the `thread_id` — short-term memory needs no code of its own.

---

## 5. The end-to-end demo, step by step

Before the conversation starts, the notebook writes what the app and a reviewer would have written: a session instruction for Priya's first visit ("on a phone: keep every reply under 60 words, with at most 4 short list items"), an approved `checklist` procedure v1 (number every item, end with a `Risk:` line) plus a pending v2, and three month-old episodes from Priya's earlier work.

**Visit 1** — thread `priya-thread-1`, session `priya-visit-1`:
1. *"Hi, I'm Priya. I'm a site reliability engineer, and I prefer Terraform over Pulumi."* The model saves three facts under stable keys; `record_episode` records nothing, because there is no task.
2. *"Draft a checklist for rotating our production database credentials."* The reply is a numbered checklist ending in a `Risk:` line (the approved procedure) and stays under 60 words (the session instruction). `record_episode` appends the task and prunes the oldest of the four episodes.

**Visit 2** — new thread `priya-thread-2`, new session `priya-visit-2`:
1. *"What's my role, and what did we work on last time?"* Short-term memory is empty and there is no session instruction, yet the agent names her role (semantic) and the credentials checklist (episodic).
2. *"Update: I've switched, and I now prefer Pulumi over Terraform."* The model reuses the preference's key: the fact count stays the same and the old value is overwritten.

**Marco** — thread `marco-thread-1`, user `u-marco`: *"What do you know about me, and what have we worked on together?"* His namespaces are empty, so the agent knows nothing about him. He still gets the same approved procedure, because procedures are scoped to the agent, not the user.

The notebook checks each of these outcomes in code and finally reads every layer back from `agent_memory.db`: the store's namespaces with their item counts, each thread's checkpointed messages, and a `sweep_ttl()` that deletes nothing yet, because the 30-minute session TTL hasn't passed.

---

## 6. The production path

Nodes and tools only see `runtime.store` and the compiled checkpointer, so moving to Postgres changes the setup, not the agent:

```python
with (
    PostgresSaver.from_conn_string(DB_URI) as checkpointer,
    PostgresStore.from_conn_string(DB_URI, ttl={"omit_expired": True, "sweep_interval_minutes": 10}) as store,
):
    checkpointer.setup()
    store.setup()
    store.start_ttl_sweeper()
    agent = builder.compile(checkpointer=checkpointer, store=store)
```

Postgres brings concurrent writers, `omit_expired` that really hides expired session items, and — with `index=` and pgvector — `search(..., query=...)` to retrieve facts and episodes by meaning once they outgrow the preload.

### Sidebar: the same layers as plain SQL

The layers are a design pattern, not an API. Two hand-written tables can do the same job:

```sql
CREATE TABLE semantic_memory (user_id TEXT, key TEXT, fact TEXT, updated_at TEXT,
                              PRIMARY KEY (user_id, key));   -- stable key: INSERT OR REPLACE upserts
CREATE TABLE episodic_memory (id TEXT PRIMARY KEY, user_id TEXT, task TEXT, outcome TEXT,
                              created_at TEXT);              -- fresh id per event: append-only
```

Hand-written tables give you joins, constraints and indexes of your choosing. The `Store` gives you namespaces, per-item TTLs, embedding search and a Postgres swap without touching the agent. `SqliteStore` keeps its own items in an internal table whose schema may change between versions — read it through `get`/`search`, not SQL.

---

## Quick reference

| Need | Layer | Mechanism |
|---|---|---|
| Follow-up question in the same chat | Short-term | `SqliteSaver` checkpoint, keyed by `thread_id` |
| A preference for this visit only | Session | `store.put(..., ttl=...)` under `("session", session_id)` |
| Remember the user's role across visits | Semantic | `save_user_fact` tool, stable key, upsert |
| Recall what you did for them last time | Episodic | `record_episode` node, append + prune |
| Make the agent follow an approved playbook | Procedural | highest `approved` version under `("procedures", agent_id)` |
| Keep users apart | All | ids in `context`, read through `Runtime` / `ToolRuntime` — never from the model |
