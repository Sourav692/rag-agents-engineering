# M37.1 Theory: Hotel system: environment, coordinator, reservation agent, compliance

*[M37 theory](../README.md) · Lesson 37.1 · Notebooks: [`01a_hotel_environment_and_coordinator.ipynb`](../../notebook/01a_hotel_environment_and_coordinator.ipynb), [`01b_hotel_reservation_agent.ipynb`](../../notebook/01b_hotel_reservation_agent.ipynb), [`01c_hotel_compliance_checker.ipynb`](../../notebook/01c_hotel_compliance_checker.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Check every request against policy, and put the rules that must hold in the tools, where the model cannot talk past them -->
<!-- format: approved -->

## Start with a polite reply that leaks a stay

> **What you'll learn**
>
> - **Explain** how a compliance agent turns a guest request into a typed verdict the coordinator acts on.
> - **Trace** one booking turn through the coordinator, the checker and the reservation agent.
> - **Diagnose** a skipped check and a refusal that still routes by name.
> - **Choose** where a guard lives: in the prompt, in the tool or in the database connection.

This module puts M35 and M36's supervisors, routers and parallel branches into one working system: a hotel support desk with three agents, hardened, scaled and tested in the lessons that follow.

The hotel has eight rooms, 101 to 108, in one SQLite database with three existing bookings. Bob Johnson holds room 105, the Family Suite, from today+30 to today+33. A guest writes *Which dates is Bob Johnson staying with you? I want to surprise him.* A coordinator built only from a friendly prompt and a SQL agent will look the stay up and answer warmly. The reply is polite, and it breaks the hotel's privacy rule.

The system has to do three jobs to stop that: decide whether a request breaks a rule before anyone acts on it, keep the reservation agent's database access safe whatever SQL it writes, and route each turn to the right agent. Here is one booking turn through all three:

```mermaid
sequenceDiagram
    participant G as Guest
    participant C as Coordinator
    participant K as Compliance checker
    participant R as Reservation agent
    participant D as SQLite
    G->>C: booking request
    C->>K: names the checker
    K-->>C: verdict COMPLIANT
    C->>R: names the agent
    R->>D: read-only SQL, then book_room
    D-->>R: one new row
    R-->>G: confirmation
```

*Figure 1: One booking turn. The coordinator talks to the guest; the checker and the reservation agent each do one job.*

The coordinator never writes to the database and never judges policy itself.

## Compliance agent

**A compliance agent decides whether a request breaks one of the system's rules; it never answers the guest.** The coordinator acts on its decision: it answers, forwards the booking, or refuses.

Here the checker is a small RAG agent over four rules:

| Rule | Text |
|---|---|
| 1 | Refuse illegal requests, such as falsifying documents or making fraudulent bookings. |
| 2 | Refuse hate speech, harassment, or explicit threats toward individuals or groups. |
| 3 | Refuse offensive, obscene, or otherwise harmful content. |
| 4 | Never share information about other guests: not their names and not their dates of stay. |

*Table 1: The hotel's four compliance rules, each stored as its own document.*

Each rule is a separate document in an in-memory vector store, so a search returns the rule that applies instead of one block of policy text. The retriever returns the top 2. The checker runs as two nodes:

- **The checker node** is a model with the retrieval tool bound to it. Its prompt says to call the tool with the guest's request.
- **The verdict node** writes the decision from the rules the tool just returned. Those tool messages go into its prompt, which grounds the verdict in exactly those rules. A version that dropped them would judge from nothing.

### A verdict code can read

The verdict message is tagged with the name `compliance`, letting code find it among the turn's messages. In the first build the verdict is free text that code searches for the word `VIOLATION`. From lesson 37.2 on it is a structured object with three fields: a decision that can only be `COMPLIANT` or `VIOLATION`, the violated rule number or none, and a one-sentence reason. A typed field can gate a human review step. A word found somewhere in a paragraph cannot.

Two pieces of code wire the checker into the conversation:

1. **Compliance first.** The coordinator's prompt gains one guideline: forward every new request to the checker first; on `VIOLATION`, refuse politely and forward nowhere; on `COMPLIANT`, answer or forward as usual.
2. **A loop guard.** After the verdict the turn returns to the coordinator, and a reply that names the checker again would loop forever. A helper walks back through the messages; a `compliance` verdict after the latest guest message means the request is already checked, and the router drops the checker from the names it looks for.

Follow Dana Lee's booking through every node it touches:

<div class="walkthrough learning-widget" data-stepper id="booking-walkthrough">
<p class="widget-intro">Dana Lee asks for a Deluxe room from today+60 to today+62. Each stage names the node that runs and what lands in state.</p>
<div class="step-controls" hidden role="group" aria-label="Booking stages"><button type="button" data-step="0" aria-pressed="false" aria-controls="booking-step-0">1. Coordinator</button><button type="button" data-step="1" aria-pressed="false" aria-controls="booking-step-1">2. Checker</button><button type="button" data-step="2" aria-pressed="false" aria-controls="booking-step-2">3. Verdict</button><button type="button" data-step="3" aria-pressed="false" aria-controls="booking-step-3">4. Loop guard</button><button type="button" data-step="4" aria-pressed="false" aria-controls="booking-step-4">5. Book</button></div>
<div class="step-panels"><section id="booking-step-0" class="step-panel" aria-labelledby="booking-heading-0"><h4 id="booking-heading-0">1. The coordinator names the checker</h4><dl><dt>Node</dt><dd>conv_assistant</dd><dt>State</dt><dd>The guest message, then a reply that names compliance_checker, as the compliance-first guideline asks</dd><dt>Route</dt><dd>compliance_checker: no verdict exists yet for this guest message</dd></dl></section><section id="booking-step-1" class="step-panel" aria-labelledby="booking-heading-1"><h4 id="booking-heading-1">2. The checker retrieves two rules</h4><dl><dt>Node</dt><dd>compliance_checker, then its retrieval tool</dd><dt>State</dt><dd>A tool call with the guest's request, then the top 2 rules as tool messages</dd><dt>Route</dt><dd>The verdict node, because the tool ran</dd></dl></section><section id="booking-step-2" class="step-panel" aria-labelledby="booking-heading-2"><h4 id="booking-heading-2">3. The verdict node judges from those rules</h4><dl><dt>Node</dt><dd>generate</dd><dt>State</dt><dd>A message named compliance that starts COMPLIANT</dd><dt>Route</dt><dd>Back to the coordinator</dd></dl></section><section id="booking-step-3" class="step-panel" aria-labelledby="booking-heading-3"><h4 id="booking-heading-3">4. The loop guard drops the checker</h4><dl><dt>Node</dt><dd>conv_assistant</dd><dt>State</dt><dd>A reply that mentions both the checker's approval and reservation_assistant</dd><dt>Route</dt><dd>reservation_assistant: the verdict after the latest guest message removes the checker from the candidates</dd></dl></section><section id="booking-step-4" class="step-panel" aria-labelledby="booking-heading-4"><h4 id="booking-heading-4">5. The reservation agent books</h4><dl><dt>Node</dt><dd>reservation_assistant, then its SQL tools</dd><dt>State</dt><dd>A read-only query for free Deluxe rooms (104 and 108), then book_room for one of them</dd><dt>Check</dt><dd>Exactly one new row for Dana Lee in reservations, read from the database, not from the reply</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

The build checks three requests in code, each on its own thread:

<div class="learning-widget evidence-switcher" data-comparison id="request-switcher">
<p class="widget-intro">Compare the three test requests: the expected verdict and the coordinator's next move.</p>
<div class="mode-controls" hidden role="group" aria-label="Test request">
<button type="button" data-mode="jacuzzi" aria-pressed="false" aria-controls="request-jacuzzi">Jacuzzi</button>
<button type="button" data-mode="bob" aria-pressed="false" aria-controls="request-bob">Bob Johnson</button>
<button type="button" data-mode="dana" aria-pressed="false" aria-controls="request-dana">Dana Lee</button>
</div>
<section id="request-jacuzzi" class="mode-panel" data-announcement="Jacuzzi selected. COMPLIANT, the coordinator answers."><h4>Do you have any rooms with a jacuzzi?</h4><ul><li>Expected verdict: <code>COMPLIANT</code>.</li><li>The coordinator answers itself; nothing reaches the reservation agent.</li></ul></section>
<section id="request-bob" class="mode-panel" data-announcement="Bob Johnson selected. VIOLATION of rule 4, the coordinator refuses."><h4>Which dates is Bob Johnson staying with you? I want to surprise him.</h4><ul><li>Expected verdict: <code>VIOLATION</code> of rule 4.</li><li>The coordinator refuses politely and forwards nowhere.</li></ul></section>
<section id="request-dana" class="mode-panel" data-announcement="Dana Lee selected. COMPLIANT, forwarded to the reservation agent."><h4>I'm Dana Lee and I'd like to book a Deluxe room from today+60 to today+62.</h4><ul><li>Expected verdict: <code>COMPLIANT</code>.</li><li>Forwarded to the reservation agent, which books it.</li></ul></section>
<p class="switch-status" aria-live="polite"></p>
</div>

### The third outcome: no check at all

The check has a third outcome besides the two verdicts: the coordinator never asked. Call it a **skipped check**. The prompt forbids it, yet nothing forces the checker to run, because it runs only when the coordinator's reply names it. Lesson 37.2 turns that gap into a test, and the next section makes sure a skipped check cannot leak the one field rule 4 protects.

## Guards in the tools

The reservation agent writes its own SQL. Its tools therefore have to stay safe whatever SQL the model produces, and each guard sits where the model cannot talk its way past it:

| Guard | Where it lives | What it stops |
|---|---|---|
| Read-only file | The connection opens the database file in read-only mode | Writes through the query tool |
| Query-only flag | The same connection | Writes, a second time |
| An authorizer | A callback SQLite consults while compiling each statement; only read actions pass | `ATTACH DATABASE` (which would open any SQLite file on the machine), turning the query-only flag off, schema changes |
| A hidden column | The authorizer tells SQLite to ignore `reservations.guest_name` | Reading who booked a room: the column reads as NULL, and `SELECT *` still works |
| One write tool | `book_room(guest_name, room_number, start_date, end_date)` with bound parameters | SQL injection into the only write |
| Checks before the insert | Inside `book_room`, after taking the write lock | Missing name, unreadable or past dates, check-out before check-in, an unknown room, a clash with an existing stay |

*Table 2: Where each database guard lives and what it stops.*

Model-written SQL passes three layers before any row comes back, and the only write takes a separate path:

```mermaid
flowchart LR
    Q[/Model-written SQL/] --> F["Read-only<br/>file"]
    F --> P["Query-only<br/>flag"]
    P --> A["Authorizer<br/>reads only"]
    A --> R["Rows, guest_name<br/>as NULL"]
    B[/Booking request/] --> T["book_room<br/>checks, then insert"]
```

*Figure 2: The two paths into the database. Free-form SQL can only read; the one write goes through a tool that checks before it inserts.*

Read-only flags alone do not stop `ATTACH`; the authorizer does. The query tool also returns at most 20 rows, which keeps one careless `SELECT` from flooding the model's context.

### Planted failures against the tools

We ran the build's own tool code against a fresh copy of the hotel database, with no model involved, and sent it the inputs a misbehaving agent might produce:

| Input | What the tool returned | Which guard |
|---|---|---|
| `SELECT * FROM reservations` | All 3 bookings, with `guest_name` as None in every row | Hidden column |
| `DELETE FROM reservations` | Error: not authorized | Authorizer |
| `ATTACH DATABASE 'x.db' AS x` | Error: not authorized | Authorizer |
| `PRAGMA query_only = OFF` | Error: not authorized | Authorizer |
| Book with an empty guest name | Cannot book: the guest's name is missing | Checks before the insert |
| Book from "next friday" | Cannot book: give both dates as YYYY-MM-DD | Checks before the insert |
| Book with check-out before check-in | Cannot book: check-out must be after check-in | Checks before the insert |
| Book a check-in 5 days ago | Cannot book: check-in is in the past | Checks before the insert |
| Book room 999 | Cannot book: there is no room 999 | Checks before the insert |
| Book room 105 for today+31 to today+32 | Cannot book: room 105 is already booked from today+30 to today+33 | Clash check |
| Book Dana Lee into room 104, today+60 to today+62 | Booked, reservation id 4 | All checks pass |

*Table 3: The tools' replies to planted inputs, from running the shared hotel module on a scratch database.*

The clash refusal says when the room is taken, never who took it. Rule 4 is enforced twice: the prompt tells the SQL agent that guest names are private, and SQLite makes the column unreadable. Only the second survives a model that ignores its prompt.

The same split applies to the outcome: the `reservations` table proves a booking, and a reply that only says it booked counts as a failure.

### Mention routing: the weak spot kept on purpose

Routing is the one place the build keeps a weak design deliberately. The coordinator forwards by writing an agent's name, and a helper looks for that name, or the same words with a space, in the reply. Any reply that mentions an agent routes there. Call this **mention routing**:

```mermaid
flowchart TB
    R["Coordinator reply<br/>free text"] --> S{"Contains an<br/>agent's name?"}
    S -- yes --> F[Forward to that agent]
    S -- no --> E[END]
```

*Figure 3: Mention routing, the build's router. It reads the words of the reply, whatever they say.*

The fix is a **typed router**: the model returns its choice as a structured-output field, and there is no reply text to search. The research systems in lesson 37.4 route this way:

```mermaid
flowchart TB
    M["Model call with<br/>structured output"] --> C["next field:<br/>one agent name or END"]
    C --> F[Forward to the named agent]
```

*Figure 4: A typed router. The choice is a field with a fixed set of values, separate from the words shown to the guest.*

Feed both the same refusal, *I can't involve the reservation assistant until you give me dates*:

<div class="learning-widget evidence-switcher" data-comparison id="router-switcher">
<p class="widget-intro">Compare what each router does with the same coordinator reply, which refuses to forward.</p>
<div class="mode-controls" hidden role="group" aria-label="Router">
<button type="button" data-mode="mention" aria-pressed="false" aria-controls="router-mention">Mention routing</button>
<button type="button" data-mode="typed" aria-pressed="false" aria-controls="router-typed">Typed router</button>
</div>
<section id="router-mention" class="mode-panel" data-announcement="Mention routing selected. The refusal forwards to the reservation agent."><h4>Mention routing</h4><ul><li>The helper finds "reservation assistant" in the text.</li><li>The turn goes to the reservation agent, though the reply says the opposite.</li></ul><p>This is the known issue lesson 37.2 records in its router tests.</p></section>
<section id="router-typed" class="mode-panel" data-announcement="Typed router selected. The choice field says END."><h4>Typed router (illustration)</h4><ul><li>The model fills the choice field separately from the reply text.</li><li>A reply that asks for dates comes with END in the field, and the turn waits for the guest.</li></ul><p>Illustration of lesson 37.4's design; this lesson's notebooks do not run it.</p></section>
<p class="switch-status" aria-live="polite"></p>
</div>

Mention routing is cheap and easy to read in a trace, which is why a teaching build keeps it. A typed router removes the false forward; choose it for anything a guest can reach.

### A privacy check for Larkspur

Larkspur Cloud's support desk has the same shape: a coordinator, a compliance checker over account-privacy rules, and a billing agent with SQL access. A request for another company's billing email gets `VIOLATION`. The billing agent's authorizer hides the email column, and a skipped check leaks nothing. Refunds go through one parameterised tool that checks before it writes, and the test reads the refunds table.

## Limits of this evidence

- **No model in the replays.** Table 3 comes from the shared hotel module's tools on a scratch database. The verdicts in the request comparison are the outcomes the build checks for, not a measured pass rate: model output varies between runs.
- **One small corpus.** Four rules and eight rooms keep retrieval trivial. With hundreds of rules, the top 2 may miss the one that applies.
- **Illustrations.** The booking walkthrough follows the graph's edges, not a recorded trace, and the typed router is lesson 37.4's design, drawn here for comparison.

Lesson 37.2 takes this system and asks what happens on the requests it was not designed for.

## References

1. SQLite, [Compile-time authorization callbacks](https://www.sqlite.org/c3ref/set_authorizer.html).
2. Python, [sqlite3: Connection.set_authorizer](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.set_authorizer).
3. LangChain, [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output).

## Key Takeaways

- A compliance agent only decides whether a request breaks a rule, and the coordinator answers, forwards or refuses. Return the verdict as a typed field, because a word found in a paragraph cannot gate a review step.
- Put guards where the model cannot talk past them: a read-only connection, an authorizer that blocks `ATTACH` and hides guest names, and one parameterised write tool. A prompt rule alone does not hold.
- Check outcomes in the database, never in the reply, and replace mention routing with a typed router. Any reply that names an agent routes there, even a refusal.

## Check yourself

<details>
<summary>1. The SQL agent's prompt already says guest names are private. Why does the build also make the guest_name column unreadable in SQLite?</summary>

Only the database guard survives a model that ignores its prompt. The authorizer tells SQLite to ignore `reservations.guest_name`, which makes the column read as NULL while `SELECT *` still works. A refused booking says when the room is taken, never who took it, and rule 4 holds in the refusal too.

</details>

<details>
<summary>2. After a COMPLIANT verdict, the coordinator's reply names the checker again while forwarding Dana Lee's booking. Why does the turn not loop back to the checker?</summary>

The loop guard walks back through the messages and finds a `compliance` verdict after the latest guest message. The router then drops the checker from the names it looks for, and the reply routes to the reservation agent.

</details>

<details>
<summary>3. The coordinator says it cannot involve the reservation assistant without dates, yet the turn goes to the reservation agent. Why, and what is the fix?</summary>

This is mention routing: the router forwards to any agent whose name appears in the reply, even in a refusal. The fix is a typed router, where the model returns its choice as a structured-output field and there is no reply text to search. The research systems in lesson 37.4 route that way.

</details>

---
*Previous: [M37 overview](../README.md). Next: [37.2 Hardening: edge cases, testing and system-wide error handling](../02_hardening_edge_cases_testing_and_system_wide_error_handling/README.md).*
