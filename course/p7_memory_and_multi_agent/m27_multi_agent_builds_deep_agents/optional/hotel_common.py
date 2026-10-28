"""Shared building blocks for the hotel-reservation notebooks (01-10).

`01_hotel_environment_and_coordinator.ipynb` walks through the database, the rules, the prompts and the routing
helper; `02_hotel_reservation_agent.ipynb` the SQL tools; `03_hotel_compliance_checker.ipynb` the compliance core;
`04_hotel_edge_cases_and_errors.ipynb` the structured verdict; `06_hotel_parallel_reservation_agents.ipynb` the
two-hotel parallel branch. Those notebooks keep an explained copy inline; the others import the versions below, so
each one can focus on the single idea it teaches.

Contents
- ROOMS, sample_reservations(), init_hotel_db()     the SQLite room/reservation database
- make_sql_tools()                                  read-only SQL tools (guest names hidden) plus a parameterised book_room tool
- COMPLIANCE_RULES, build_compliance_retriever()    the compliance rules as a searchable vector store + tool
- SQL_SCHEMA, conversation_prompt(), SQL_PROMPT, SQL_READ_PROMPT, COMPLIANCE_PROMPT, COMPLIANCE_FIRST   prompts
- ComplianceVerdict, latest_verdict(), make_core_nodes()   the reservation agent and the compliance checker
- mentioned_agent(), route_by_mention(), CONFIDENCE_THRESHOLD   how the coordinator's replies are routed
- HOTELS, init_two_hotels(), free_rooms(), reservation_mapper(), branch_done(), make_hotel_assistant()   two hotels
- run_turn(), run_traced(), chat_with_agent(), print_edges()   running and inspecting a graph
"""
# ruff: noqa: E501  (prompt text is kept on long lines so it reads as the model sees it)
from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import date, timedelta
from pathlib import Path
from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# The room database
# ---------------------------------------------------------------------------
ROOMS = [
    (101, "Single", 100, 1, "TV, Wi-Fi"),
    (102, "Double", 150, 2, "TV, Wi-Fi, Balcony"),
    (103, "Suite", 250, 3, "TV, Wi-Fi, Balcony, Jacuzzi"),
    (104, "Deluxe", 200, 2, "TV, Wi-Fi, Mini-bar"),
    (105, "Family Suite", 300, 4, "TV, Wi-Fi, Balcony, Kitchenette"),
    (106, "Executive Suite", 350, 2, "TV, Wi-Fi, Balcony, Jacuzzi, City View"),
    (107, "Double", 150, 2, "TV, Wi-Fi"),
    (108, "Deluxe", 200, 2, "TV, Wi-Fi, Balcony, Fireplace"),
]

SQL_SCHEMA = """Table: rooms
  room_number (INTEGER PRIMARY KEY)
  room_type (TEXT NOT NULL)
  price (REAL NOT NULL)
  max_capacity (INTEGER NOT NULL)
  amenities (TEXT)

Table: reservations
  reservation_id (INTEGER PRIMARY KEY AUTOINCREMENT)
  guest_name (TEXT NOT NULL)
  room_number (INTEGER NOT NULL, FOREIGN KEY REFERENCES rooms(room_number))
  start_date (DATE NOT NULL)
  end_date (DATE NOT NULL)"""


def sample_reservations(today: date | None = None) -> list[tuple]:
    """Three existing bookings, placed relative to today so the data never goes stale.

    Room 105 (the Family Suite) is booked from today+30 to today+33, which the notebooks use to show a clash.
    """
    t = today or date.today()
    d = lambda days: (t + timedelta(days=days)).isoformat()  # noqa: E731
    return [
        ("Alice Smith", 102, d(14), d(17)),
        ("Bob Johnson", 105, d(30), d(33)),
        ("Charlie Brown", 106, d(45), d(47)),
    ]


def init_hotel_db(path: str | Path = "hotel.db", rooms: list[tuple] = ROOMS, reservations: list[tuple] | None = None) -> str:
    """(Re)create the database from scratch and return its path.

    Dropping and recreating makes every run start from the same data: re-running the cell never duplicates bookings.
    """
    reservations = sample_reservations() if reservations is None else reservations
    with closing(sqlite3.connect(path)) as conn, conn:
        conn.executescript(
            """
            DROP TABLE IF EXISTS reservations;
            DROP TABLE IF EXISTS rooms;
            CREATE TABLE rooms (
              room_number INTEGER PRIMARY KEY,
              room_type TEXT NOT NULL,
              price REAL NOT NULL,
              max_capacity INTEGER NOT NULL,
              amenities TEXT
            );
            CREATE TABLE reservations (
              reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
              guest_name TEXT NOT NULL,
              room_number INTEGER NOT NULL,
              start_date DATE NOT NULL,
              end_date DATE NOT NULL,
              FOREIGN KEY (room_number) REFERENCES rooms(room_number)
            );
            """
        )
        conn.executemany("INSERT INTO rooms VALUES (?, ?, ?, ?, ?)", rooms)
        conn.executemany(
            "INSERT INTO reservations (guest_name, room_number, start_date, end_date) VALUES (?, ?, ?, ?)",
            reservations,
        )
    return str(path)


# ---------------------------------------------------------------------------
# SQL tools: model-written queries on a read-only connection, bookings through one parameterised tool
# ---------------------------------------------------------------------------
MAX_ROWS = 20  # the most rows one query returns to a model

# SQLite asks the authorizer about every action while it compiles a statement. Only reads pass: writes, schema
# changes, ATTACH (which would open any SQLite file on this machine) and PRAGMA are refused before they run.
READ_ACTIONS = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION, sqlite3.SQLITE_RECURSIVE}
# Columns model-written SQL may never see: they read as NULL (SQLITE_IGNORE), so `SELECT *` still works.
# Model-written SQL sees rooms and dates, never who booked them (compliance rule 4: other guests stay private).
PRIVATE_COLUMNS = {("reservations", "guest_name")}


def _allow_reads_only(action, arg1, arg2, db_name, trigger) -> int:
    if action == sqlite3.SQLITE_READ and (arg1, arg2) in PRIVATE_COLUMNS:
        return sqlite3.SQLITE_IGNORE  # the column reads as NULL
    return sqlite3.SQLITE_OK if action in READ_ACTIONS else sqlite3.SQLITE_DENY


def read_only_connection(path: str | Path) -> sqlite3.Connection:
    """Open `path` so that it only reads, three times over: a read-only file, `query_only`, and an authorizer.

    The authorizer also hides `reservations.guest_name` (it reads as NULL). `check_same_thread=False` because agents
    run their tools in worker threads.
    """
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, check_same_thread=False)
    conn.execute("PRAGMA query_only = ON")
    conn.set_authorizer(_allow_reads_only)  # installed after the PRAGMA, which it would refuse
    return conn


def make_sql_tools(path: str | Path = "hotel.db", *, can_book: bool = True) -> list:
    """The reservation agent's tools for one database: `list_tables`, `describe_table`, `run_query` and `book_room`.

    `run_query` runs model-written SQL on a read-only connection that sees rooms and dates but never guest names
    (`guest_name` reads as NULL). `book_room` is the only way to write: its values are bound parameters (never pasted
    into SQL), and it checks the dates and the room before inserting.
    `can_book=False` leaves `book_room` out, for agents that must only report availability.
    """
    conn = read_only_connection(path)

    def fetch(sql: str) -> str:
        """Run ONE statement; return a header line plus at most MAX_ROWS rows, as text."""
        with closing(conn.execute(sql)) as cursor:  # closing it releases the read lock, even after a partial fetch
            rows = cursor.fetchmany(MAX_ROWS)
            columns = [column[0] for column in cursor.description or []]
        if not rows:
            return "No rows."
        header = " | ".join(columns)
        return "\n".join([header, *(" | ".join(str(value) for value in row) for row in rows)])

    @tool
    def list_tables() -> str:
        """List the tables in the hotel database."""
        return ", ".join(row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"))

    @tool
    def describe_table(table: str) -> str:
        """Return the CREATE TABLE statement (columns, types, keys) of one table."""
        row = conn.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)).fetchone()
        return row[0] if row else f"No table named {table!r}; call list_tables first."

    @tool
    def run_query(sql: str) -> str:
        """Run ONE read-only SQL query (SQLite dialect) on the hotel database; returns up to 20 rows.
        Guest names are private: reservations.guest_name always reads as NULL."""
        try:
            return fetch(sql)
        except sqlite3.Error as error:
            return f"Error: {error}"  # the agent reads the error and can fix its query

    @tool
    def book_room(guest_name: str, room_number: int, start_date: str, end_date: str) -> str:
        """Book one room for a guest. Dates are YYYY-MM-DD; end_date is the check-out day.
        Refuses unreadable or past dates, an unknown room, and a room that is already booked for any of those nights."""
        guest_name = guest_name.strip()
        if not guest_name:
            return "Cannot book: the guest's name is missing."
        try:
            start, end = date.fromisoformat(start_date), date.fromisoformat(end_date)
        except ValueError:
            return "Cannot book: give both dates as YYYY-MM-DD."
        if start >= end:
            return f"Cannot book: check-out ({end}) must be after check-in ({start})."
        if start < date.today():
            return f"Cannot book: check-in {start} is in the past (today is {date.today()})."
        with closing(sqlite3.connect(path, timeout=10)) as db, db:
            db.execute("BEGIN IMMEDIATE")  # take the write lock first, so the checks and the insert are one step
            room = db.execute("SELECT room_type FROM rooms WHERE room_number = ?", (room_number,)).fetchone()
            if room is None:
                return f"Cannot book: there is no room {room_number}."
            clash = db.execute(
                "SELECT start_date, end_date FROM reservations WHERE room_number = ? AND start_date < ? AND end_date > ?",
                (room_number, end.isoformat(), start.isoformat()),
            ).fetchone()
            if clash:  # say when, never who: other guests' names stay private
                return f"Cannot book: room {room_number} is already booked from {clash[0]} to {clash[1]}."
            cursor = db.execute(
                "INSERT INTO reservations (guest_name, room_number, start_date, end_date) VALUES (?, ?, ?, ?)",
                (guest_name, room_number, start.isoformat(), end.isoformat()),
            )
        return (f"Booked room {room_number} ({room[0]}) for {guest_name} from {start} to {end} "
                f"(check-out day). Reservation id {cursor.lastrowid}.")

    tools = [list_tables, describe_table, run_query]
    return tools + [book_room] if can_book else tools


# ---------------------------------------------------------------------------
# Compliance rules and their retriever
# ---------------------------------------------------------------------------
COMPLIANCE_RULES = [
    "Refuse illegal requests, such as falsifying documents or making fraudulent bookings.",
    "Refuse hate speech, harassment, or explicit threats toward individuals or groups.",
    "Refuse offensive, obscene, or otherwise harmful content.",
    "Never share information about other guests: not their names and not their dates of stay.",
]


def build_compliance_retriever(collection_name: str = "compliance_rules", k: int = 2):
    """Index each rule as its own document in an in-memory Chroma collection and return a `retrieve` tool.

    `reset_collection()` empties the collection first, so re-running the cell never duplicates the rules.
    """
    from aied_helpers import get_embeddings
    from langchain_chroma import Chroma

    store = Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(provider="openai", model="text-embedding-3-small"),
    )
    store.reset_collection()
    store.add_texts(COMPLIANCE_RULES, metadatas=[{"rule": i + 1} for i in range(len(COMPLIANCE_RULES))])

    @tool(response_format="content_and_artifact")
    def retrieve(query: str):
        """Retrieve the hotel compliance rules most relevant to a guest request."""
        docs = store.similarity_search(query, k=k)
        return "\n\n".join(f"Rule {d.metadata['rule']}: {d.page_content}" for d in docs), docs

    return retrieve


# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------
HOTEL_ADDRESS = "36 W 106th St, New York, NY 10025, United States"


def conversation_prompt(agents: list[str], extra_guidelines: str = "") -> SystemMessage:
    """The coordinator's prompt. It routes by *naming* an agent in its reply (see `mentioned_agent`)."""
    agent_list = "\n".join(f"  - {name}" for name in agents)
    return SystemMessage(
        content=f"""Role: You are the Conversation Coordinator for a hotel chain's customer support system. You manage the
conversation with the guest and decide whether to handle a request yourself or forward it to a specialised agent.

Primary tasks:
- Engage with the guest politely and find out how you can help.
- Identify the nature of the request: a general question, a booking, an issue, or something needing a specialist.
- To forward the conversation, answer with the exact name of one agent. Available agents:
{agent_list}
- Keep a friendly, empathetic tone.

Guidelines:
- For general inquiries (facilities, amenities, location) answer directly. The hotel is at {HOTEL_ADDRESS}.
- To book a room you need the room type and the dates. Only when the guest has given both, forward to
  reservation_assistant; otherwise ask for what is missing and do not mention reservation_assistant.
{extra_guidelines}"""
    )


# The coordinator guideline every system with a compliance checker adds (03 explains it)
COMPLIANCE_FIRST = (
    "- Forward every NEW guest request to compliance_checker first. If its verdict is VIOLATION, "
    "politely refuse and do not forward anywhere. If COMPLIANT, answer or forward as usual."
)

_SQL_RULES = f"""You are an AI assistant specialised in SQL for the hotel's reservation database:

{SQL_SCHEMA}

You must:
- Reference only these two tables and their columns, and write valid SQLite.
- Read with run_query, one SELECT at a time. Its connection only reads, so any other statement fails.
- A room is free for a stay when it has no reservation with start_date before the check-out date and end_date after
  the check-in date.
- Guest names are private. reservations.guest_name always reads as NULL in your queries, so you cannot look
  bookings up by name, and you must never reveal who booked a room: report only whether it is free.
- If no room matches the request, say so plainly.
- If the request is unclear or impossible with this schema, ask for clarification."""

# For agents that only report availability (no booking tool)
SQL_READ_PROMPT = SystemMessage(content=_SQL_RULES)

SQL_PROMPT = SystemMessage(
    content=_SQL_RULES
    + """
- To book, call book_room(guest_name, room_number, start_date, end_date) with the dates as YYYY-MM-DD. Ask for the
  guest's name if you do not have it. book_room checks the dates and that the room is free, and says why it refuses."""
)

COMPLIANCE_PROMPT = SystemMessage(
    content="""You are the Compliance Checker agent. You do not answer the guest's request; you only decide whether it is
compliant with the hotel's rules.

Steps:
1. Call the `retrieve` tool with the guest's request to find the relevant rules.
2. Quote the rules that apply.
3. Give your verdict: say "COMPLIANT" if no retrieved rule is violated, otherwise say "VIOLATION" and name the rule.
Never invent rules: only cite what `retrieve` returned."""
)


# ---------------------------------------------------------------------------
# The core agents: reservation assistant and compliance checker (03 builds them, 04 adds the structured verdict)
# ---------------------------------------------------------------------------
class ComplianceVerdict(BaseModel):
    verdict: Literal["COMPLIANT", "VIOLATION"] = Field(description="VIOLATION only if a retrieved rule is broken")
    rule: int | None = Field(description="Number of the violated rule, or null if none")
    reason: str = Field(description="One sentence that cites the retrieved rule(s)")


def latest_verdict(messages) -> str | None:
    """The compliance verdict given since the latest guest message ('COMPLIANT'/'VIOLATION'), or None if unchecked."""
    for m in reversed(messages):
        if m.type == "human":
            return None
        if getattr(m, "name", None) == "compliance":
            return m.content.split(":")[0].split()[0]
    return None


def checked_since_last_guest_message(messages) -> bool:
    """The loop guard: has the compliance checker already judged the latest guest message?"""
    return latest_verdict(messages) is not None


def retrieved_rules(messages) -> str:
    """The rules to judge by: the tool results just before this step, or the fallback-rules message (09's degraded mode)."""
    tool_messages = []
    for message in reversed(messages):
        if message.type != "tool":
            break
        tool_messages.insert(0, message)
    if tool_messages:
        return "\n\n".join(m.content for m in tool_messages)
    if messages and getattr(messages[-1], "name", None) == "fallback_rules":
        return messages[-1].content
    return "(no rules retrieved)"


def make_core_nodes(llm, sql_tools: list, rag_tools: list):
    """Return the nodes `(sql_assistant, rag_assistant, generate)` bound to this model and these tools.

    - `sql_assistant`: the reservation agent, with the SQL tools bound (`SQL_PROMPT`)
    - `rag_assistant`: the compliance checker, which calls `retrieve` (`COMPLIANCE_PROMPT`)
    - `generate`: writes a structured `ComplianceVerdict` from the retrieved rules, tagged `name="compliance"`

    06 and 07 pass `sql_tools=[]` and ignore `sql_assistant`: their hotel branches replace the single reservation agent.
    """
    llm_with_sql_tools = llm.bind_tools(sql_tools)
    llm_with_rag_tools = llm.bind_tools(rag_tools)
    verdict_llm = llm.with_structured_output(ComplianceVerdict)

    def sql_assistant(state: dict) -> dict:
        return {"messages": [llm_with_sql_tools.invoke([SQL_PROMPT] + state["messages"])]}

    def rag_assistant(state: dict) -> dict:
        response = llm_with_rag_tools.invoke([COMPLIANCE_PROMPT] + state["messages"])
        response.name = "compliance_checker"  # label its tool call in the conversation
        return {"messages": [response]}

    def generate(state: dict) -> dict:
        last_request = next(m for m in reversed(state["messages"]) if m.type == "human")
        v = verdict_llm.invoke([
            COMPLIANCE_PROMPT,
            SystemMessage(content=f"Retrieved rules:\n{retrieved_rules(state['messages'])}"),
            HumanMessage(content=f"Guest request: {last_request.content}\n\nGive your verdict."),
        ])
        text = v.verdict + (f" (rule {v.rule})" if v.rule else "") + f": {v.reason}"
        return {"messages": [AIMessage(content=text, name="compliance")]}

    return sql_assistant, rag_assistant, generate


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------
# The coordinator rates its confidence from 0 to 100 (05): 80-100 means the intent is clear, 50-79 clear but details
# are missing (the coordinator asks for them as usual), below 50 it cannot tell what the guest wants. Only that last
# band should stop the turn and ask the guest to repeat, so the threshold is 50.
CONFIDENCE_THRESHOLD = 50


def mentioned_agent(text: str, agents: list[str]) -> str | None:
    """Return the first agent whose name (with `_` or a space) appears in `text`, else None.

    This is how the coordinator routes: by naming an agent in its reply. It is simple and fragile (a reply that
    merely *mentions* an agent also routes). The series keeps it on purpose: `route_by_mention()` below adds 03's
    loop guard, 05 records the false positive as a known issue in its router tests, and the robust fix, a typed
    router (structured output), is in 13_multi_agent_research_summarization.ipynb.
    """
    lowered = text.lower()
    for name in agents:
        if name in lowered or name.replace("_", " ") in lowered:
            return name
    return None


def route_by_mention(messages, agents: list[str]) -> str | None:
    """The agent the coordinator's latest reply names, with 03's loop guard.

    Once the latest guest message has a verdict, `compliance_checker` is dropped from the candidates: naming it again
    cannot loop, and a reply such as "the compliance checker approved it, forwarding to reservation_assistant" still
    reaches the reservation agent.
    """
    checked = checked_since_last_guest_message(messages)
    candidates = [a for a in agents if not (a == "compliance_checker" and checked)]
    return mentioned_agent(messages[-1].content, candidates)


# ---------------------------------------------------------------------------
# Two hotels in parallel (06 explains each piece)
# ---------------------------------------------------------------------------
HOTELS = {"hotel1": "Hotel 1", "hotel2": "Hotel 2"}
HOTEL_ROOMS = {
    "hotel1": [room for room in ROOMS if room[0] <= 104],  # rooms 101-104
    "hotel2": [room for room in ROOMS if room[0] >= 105],  # rooms 105-108
}


def init_two_hotels() -> dict[str, str]:
    """Build one database per hotel from its rooms and the sample bookings for those rooms; return {hotel: path}."""
    paths = {}
    for hotel, rooms in HOTEL_ROOMS.items():
        numbers = {room[0] for room in rooms}
        bookings = [res for res in sample_reservations() if res[1] in numbers]
        paths[hotel] = init_hotel_db(f"{hotel}.db", rooms=rooms, reservations=bookings)
    return paths


def free_rooms(path: str | Path, room_type: str, start: date, end: date) -> list[int]:
    """Ground truth, straight from SQLite: rooms of this type with no overlapping booking."""
    with closing(sqlite3.connect(path)) as conn:
        rows = conn.execute(
            """SELECT room_number FROM rooms WHERE room_type = ? AND room_number NOT IN (
                   SELECT room_number FROM reservations WHERE start_date < ? AND end_date > ?)""",
            (room_type, end.isoformat(), start.isoformat()),
        ).fetchall()
    return [row[0] for row in rows]


def reservation_count(path: str | Path) -> int:
    with closing(sqlite3.connect(path)) as conn:
        return conn.execute("SELECT COUNT(*) FROM reservations").fetchone()[0]


def reservation_mapper(state: dict) -> dict:
    """Fan-out: give each hotel assistant a fresh copy of the conversation in its own key."""
    return {f"messages_{hotel}": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *state["messages"]] for hotel in HOTELS}


def branch_done(state: dict) -> dict:
    """Sync node: runs once, when its branch's tool loop has finished. Writes nothing."""
    return {}


def make_hotel_assistant(llm, hotel: str, tools: list, context=None):
    """One factory for every hotel's assistant, so each is bound to its OWN hotel's tools and message key.

    `context(state)` may return extra system messages to put in front of the branch's messages (07 passes the
    running summary).
    """
    key = f"messages_{hotel}"
    numbers = ", ".join(str(room[0]) for room in HOTEL_ROOMS[hotel])
    prompt = SystemMessage(content=SQL_READ_PROMPT.content + f"""

You are one of several reservation assistants answering in parallel, one per hotel of the chain. You handle
{HOTELS[hotel]} only (rooms {numbers}). Report availability and prices for your hotel. You cannot book: the guest
first chooses a hotel.""")
    llm_with_tools = llm.bind_tools(tools)

    def hotel_assistant(state: dict) -> dict:
        extra = context(state) if context else []
        return {key: [llm_with_tools.invoke([prompt, *extra, *state[key]])]}

    return hotel_assistant


# ---------------------------------------------------------------------------
# Running and inspecting a graph
# ---------------------------------------------------------------------------
def run_turn(graph, text: str, thread_id: str, *, verbose: bool = True, recursion_limit: int = 30) -> dict:
    """Send one guest message on a thread, print every message this turn added, and return the final state values.

    `recursion_limit` caps the graph steps in one turn, so an agent loop that never settles stops with an error.
    """
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": recursion_limit}
    before = len(graph.get_state(config).values.get("messages", [])) if graph.checkpointer else 0
    print(f"👤 Guest: {text}\n")
    state = graph.invoke({"messages": [HumanMessage(content=text)]}, config)
    if verbose:
        for message in state["messages"][before + 1:]:
            message.pretty_print()
    return state


def run_traced(graph, text: str, thread_id: str, *, recursion_limit: int = 40, verbose: bool = True) -> tuple[list[str], dict]:
    """Send one guest message; return (the names of the nodes that ran, in order; the final state values).

    `stream_mode=["updates", "values"]`: each "updates" chunk names the node that just finished, and the last
    "values" chunk is the final state, so the path is recorded from the run itself rather than assumed.
    """
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": recursion_limit}
    nodes_run, final = [], None
    if verbose:
        print(f"👤 Guest: {text}\n")
    for mode, chunk in graph.stream({"messages": [HumanMessage(content=text)]}, config, stream_mode=["updates", "values"]):
        if mode == "updates":
            nodes_run.extend(chunk)
        else:
            final = chunk
    return nodes_run, final


def chat_with_agent(graph, thread_id: str) -> None:
    """Interactive chat loop for running a notebook yourself (type 'quit' to stop). Not used by the scripted demos."""
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"quit", "exit"}:
            break
        run_turn(graph, user_input, thread_id)


def print_edges(graph) -> None:
    """Print a compiled graph's edges (a text alternative to rendering a diagram)."""
    for edge in graph.get_graph().edges:
        print(f"  {edge.source} -> {edge.target}{'  (conditional)' if edge.conditional else ''}")
