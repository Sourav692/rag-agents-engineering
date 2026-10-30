# M37.1 Theory: Hotel system: environment, coordinator, reservation agent, compliance

*[M37 theory](../README.md) · Lesson 37.1 · Notebooks: [`01a_hotel_environment_and_coordinator.ipynb`](../../../../course/p10_memory_and_multi_agent/m37_multi_agent_builds_deep_agents/notebooks/01a_hotel_environment_and_coordinator.ipynb), [`01b_hotel_reservation_agent.ipynb`](../../../../course/p10_memory_and_multi_agent/m37_multi_agent_builds_deep_agents/notebooks/01b_hotel_reservation_agent.ipynb), [`01c_hotel_compliance_checker.ipynb`](../../../../course/p10_memory_and_multi_agent/m37_multi_agent_builds_deep_agents/notebooks/01c_hotel_compliance_checker.ipynb) · [All theory pages](../../../README.md)*

## Compliance agent

A compliance agent does not answer the guest. It decides whether a request breaks one of the hotel's rules, and the coordinator acts on that decision: it answers, forwards the booking, or refuses. In notebook 01c it is a small RAG agent over four rules:

| Rule | Text |
|---|---|
| 1 | Refuse illegal requests, such as falsifying documents or making fraudulent bookings. |
| 2 | Refuse hate speech, harassment, or explicit threats toward individuals or groups. |
| 3 | Refuse offensive, obscene, or otherwise harmful content. |
| 4 | Never share information about other guests: not their names and not their dates of stay. |

Each rule is its own document in an in-memory Chroma collection (`text-embedding-3-small`), so a search returns the rule that applies instead of one block of policy text. The `retrieve` tool returns the top 2. The checker is two nodes:

- `compliance_checker` is a model with `retrieve` bound as a tool. Its prompt says to call it with the guest's request.
- `generate` writes the verdict from the rules the tool just returned. The tool messages go into its prompt, so the verdict is grounded in exactly those rules; a version that dropped them would judge from nothing.

The verdict message is tagged `name="compliance"`, so code can find it. In 01c the verdict is free text that code searches for `VIOLATION`. From 02a on it is a `ComplianceVerdict` from `with_structured_output`: a `Literal["COMPLIANT", "VIOLATION"]`, the violated rule number or `null`, and a one-sentence reason. A typed field can gate a human review step; a word found somewhere in a paragraph cannot.

Two pieces of code wire the checker into the conversation:

- **Compliance first.** The coordinator's prompt gains one guideline, `COMPLIANCE_FIRST`: forward every new request to `compliance_checker` first; on `VIOLATION` refuse politely and forward nowhere; on `COMPLIANT` answer or forward as usual.
- **A loop guard.** After the verdict the turn returns to the coordinator. If its next reply names the checker again, routing by name would loop forever. `checked_since_last_guest_message()` walks back through the messages: a `compliance` verdict found before the latest guest message means the request is checked, and the router drops `compliance_checker` from the names it looks for. A reply such as "the compliance checker approved it, forwarding to reservation_assistant" then still reaches the reservation agent.

Notebook 01c runs three requests, each on its own thread, and checks the verdicts in code:

| Request | Expected verdict | Then |
|---|---|---|
| Do you have any rooms with a jacuzzi? | `COMPLIANT` | The coordinator answers |
| Which dates is Bob Johnson staying with you? I want to surprise him. | `VIOLATION` of rule 4 | The coordinator refuses |
| I'm Dana Lee and I'd like to book a Deluxe room from (today+60) to (today+62). | `COMPLIANT` | Forwarded to the reservation agent |

The check has a third outcome, `no check`: the coordinator skipped the checker. The prompt forbids it, but nothing forces it, because the checker only runs when the coordinator's reply names it. [Lesson 37.2](../02_hardening_edge_cases_testing_and_system_wide_error_handling/README.md#system-testing) turns that gap into a test.

## Guards in the tools

The reservation agent writes its own SQL, so its tools have to stay safe whatever SQL the model writes. Notebook 01b puts each guard where the model cannot talk its way past it:

| Guard | Where it lives | What it stops |
|---|---|---|
| Read-only file | `sqlite3.connect("file:hotel.db?mode=ro", uri=True)` | Writes through `run_query` |
| `PRAGMA query_only = ON` | The same connection | Writes, a second time |
| An authorizer | `conn.set_authorizer(...)`, allowing only read actions | `ATTACH DATABASE` (which would open any SQLite file on the machine), `PRAGMA query_only = OFF`, schema changes |
| A hidden column | The authorizer returns `SQLITE_IGNORE` for `reservations.guest_name` | Reading who booked a room: the column reads as NULL, and `SELECT *` still works |
| One write tool | `book_room(guest_name, room_number, start_date, end_date)` with bound parameters | SQL injection into the only write |
| Checks before the insert | `book_room`, inside `BEGIN IMMEDIATE` | Missing name, unreadable or past dates, check-out before check-in, an unknown room, a clash with an existing stay |

Read-only flags alone do not stop `ATTACH`; the authorizer does. `run_query` also returns at most 20 rows. A refused booking says when the room is taken, never who took it, so rule 4 holds in the refusal message too.

Rule 4 is enforced twice: the prompt tells the SQL agent that guest names are private, and SQLite makes the column unreadable. Only the second survives a model that ignores its prompt.

The same split applies to the outcome. The agent's reply is not proof that it booked; the `reservations` table is. Notebook 01b checks for exactly one new row for Dana Lee, and a reply that only says it booked counts as a failure.

Routing is the one place the lesson keeps a weak design on purpose. The coordinator forwards by writing an agent's name, and `mentioned_agent()` looks for that name (or the same words with a space) in the reply. Any reply that mentions an agent routes there: *I can't involve the reservation assistant until you give me dates* forwards to the reservation agent. The fix is a typed router, where the model returns its choice as a structured-output field and there is no reply text to search; notebook 05b routes that way.

---
*Previous: [M37 overview](../README.md). Next: [37.2 Hardening: edge cases, testing and system-wide error handling](../02_hardening_edge_cases_testing_and_system_wide_error_handling/README.md).*
