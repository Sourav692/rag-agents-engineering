# M27.4 Theory: Text-to-SQL: workflow vs ReAct agent

*[M27 theory](../README.md) · Lesson 27.4 · Notebooks: [`04a_text2sql_workflow.ipynb`](../../notebook/04a_text2sql_workflow.ipynb), [`04b_text2sql_react_agent.ipynb`](../../notebook/04b_text2sql_react_agent.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Let the database count, score the SQL against your own, and keep the agent read-only -->
<!-- format: approved -->

## A fluent answer that counts wrong

> **What you'll learn**
>
> - **Explain** how a text-to-SQL chain writes, runs and answers from one stored query.
> - **Diagnose** a query that runs, reads well and counts the wrong thing.
> - **Compare** a fixed SQL workflow with a ReAct agent on cost, recovery and risk.
> - **Choose** between SQL and vector retrieval by the shape of the question.

Lesson 27.3's analyst got its numbers from tools that did the arithmetic in code. Text-to-SQL goes one step further. The model writes the code, and the database does the arithmetic over every row.

Both notebooks ask questions of a small comic-store database, kept because its numbers come from that data. Ask *Which customer has purchased the most comics?* and a typical generated query returns Natasha Romanoff, with a confident sentence around the name. The right answer is Tony Stark. The query ran without an error, and nothing in the reply hints at the mistake. This page builds what catches it.

## Text-to-SQL

**Text-to-SQL turns a question into a query, runs it, and writes the answer from the rows.** The database is built from a creation script: eight tables (Branch, Publisher, Comic, Customer, Employee, Inventory, Sale, SaleTransactions) holding 50 comics, 20 customers, 20 sales and 40 sale lines across 3 branches.

### One stored query, from question to answer

The workflow is a fixed chain of three steps. Each step adds one field to a single record, which keeps the question, the SQL, the rows and the answer together:

```mermaid
flowchart LR
    Q[/Question/] --> W["Write SQL<br/>from the schema"]
    W --> X["Run the<br/>stored query"]
    X --> A["Answer from<br/>the rows"]
```

*Figure 1: The workflow. Each box adds a field to the same record: query, result, answer.*

1. **Write the query.** The prompt carries the schema: each table's creation statement and three sample rows. That text is everything the model knows about the database. The prompt also caps results at 10 rows unless the question asks for more.
2. **Run the stored query.** The executor reads the query written in step 1. Piping the query writer into the executor a second time would generate a second query, and the SQL on screen would no longer be the SQL behind the answer. Call that a **regenerated query**.
3. **Answer from the rows**, with a prompt that says to use only the SQL result.

The prompt also has to make the model return bare SQL. A reply that starts with `SQLQuery:` or sits in a code fence fails with `near "SQLQuery": syntax error`. That is **format drift**, and it is worth ruling out before suspecting the database or the schema.

### Scoring against SQL we wrote

A demo that looks right is not a measurement. The evaluation set pairs seven questions with reference SQL written by hand, and running that SQL gives the expected answer:

| Question | Expected |
|---|---|
| How many customers do we have? | 20 |
| Which comic has sold the most copies? | Wolverine: Old Man Logan |
| Which customer has spent the most money in total? | Tony Stark |
| Which branch has the most comics in stock? | Central Comics |
| Which publisher's comics generated the most sales revenue? | Marvel Comics |
| Which customer has purchased the most comics? | Tony Stark |
| How many comics in the Superhero genre have never been sold? | 9 |

*Table 1: The seven questions and their expected answers, from running the reference SQL on the fixture database.*

The grading rule is strict on purpose. A number must appear as a whole number in the answer. A name must be the first known name the answer mentions. A list of six customers that happens to include the right one does not pass.

### Planted failure: lines instead of copies

The typical miss is the question from the opening. Follow it through the record the chain builds:

<div class="walkthrough learning-widget" data-stepper id="sql-record">
<p class="widget-intro">Trace one question through the workflow's record and into the ground-truth check. The query shape is the typical miss the notebook reports; the rows come from the fixture database.</p>
<div class="step-controls" hidden role="group" aria-label="Workflow record fields"><button type="button" data-step="0" aria-pressed="false" aria-controls="rec-step-0">1. Question</button><button type="button" data-step="1" aria-pressed="false" aria-controls="rec-step-1">2. Query</button><button type="button" data-step="2" aria-pressed="false" aria-controls="rec-step-2">3. Result</button><button type="button" data-step="3" aria-pressed="false" aria-controls="rec-step-3">4. Answer and check</button></div>
<div class="step-panels"><section id="rec-step-0" class="step-panel" aria-labelledby="rec-heading-0"><h4 id="rec-heading-0">1. The question enters the record</h4><dl><dt>question</dt><dd>Which customer has purchased the most comics?</dd><dt>Expected</dt><dd>Tony Stark, from the reference SQL that sums Quantity</dd></dl></section><section id="rec-step-1" class="step-panel" aria-labelledby="rec-heading-1"><h4 id="rec-heading-1">2. The model writes the query</h4><dl><dt>query</dt><dd>Joins sale lines to customers and counts the lines per customer</dd><dt>What it should do</dt><dd>Sum the Quantity column on those lines</dd></dl></section><section id="rec-step-2" class="step-panel" aria-labelledby="rec-heading-2"><h4 id="rec-heading-2">3. The database runs that stored query</h4><dl><dt>result</dt><dd>Natasha Romanoff first, with 5 lines</dd><dt>Error raised</dt><dd>None: the SQL is valid</dd></dl></section><section id="rec-step-3" class="step-panel" aria-labelledby="rec-heading-3"><h4 id="rec-heading-3">4. The answer, then the check</h4><dl><dt>answer</dt><dd>A confident sentence naming Natasha Romanoff</dd><dt>Ground-truth check</dt><dd>Fails: the first known name is not Tony Stark</dd></dl></section></div>
<div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div>
</div>

The generated SQL counts sale lines where the question needs summed `Quantity`, and on this data the two disagree:

| Customer | Sale lines | Copies bought |
|---|---|---|
| Natasha Romanoff | 5 | 6 |
| Tony Stark | 4 | 8 |
| Sarah Connor | 4 | 7 |

*Table 2: The top customers by line count, with their copies. Counting lines picks Natasha Romanoff, summing copies picks Tony Stark.*

We call this a **wrong definition**: valid SQL that measures something other than what the question asked. It runs, the answer reads well, and only the ground-truth check shows it is wrong.

### When the data disagrees with itself

"Revenue" has two defensible sources here: the header `Sale.TotalAmount`, or the line items, quantity times price. In a clean database they agree. In this one, 16 of the 20 sales have a total that differs from their own lines by more than 0.01, and the top three salespeople change:

| Rank | By `Sale.TotalAmount` | By line items |
|---|---|---|
| 1 | John Doe, 255.89 | Alice Brown, 325.86 |
| 2 | Alice Brown, 234.94 | John Doe, 294.86 |
| 3 | Jane Smith, 234.88 | Michael Clark, 258.88 |

*Table 3: Top salespeople under each definition of revenue, from the notebook's own queries.*

The chain picks one source silently, and a stronger model would still be guessing. The business has to decide which source is authoritative and write it into the prompt as a rule: revenue is always computed from line items. The notebook then checks the generated SQL in code for the line-item table, instead of trusting that the rule was followed.

The evaluation set shows how easily the two definitions slip. Its reference SQL for *spent the most money* sums `Sale.TotalAmount`, the source the rule forbids. Both sources still put Tony Stark first (164.94 by header, 194.92 by lines), so the expected answer holds here; on other data that reference would grade a correct answer as wrong.

## Workflow or ReAct agent

The agent notebook gives the same task to a `create_agent` ReAct agent with four database tools: list the tables, read a table's schema, check a query (an LLM reviews it before it runs), and run a query. Its system prompt tells it to list the tables first, read only the schemas it needs, check each query, and rewrite and retry on errors:

```mermaid
flowchart TD
    subgraph wf["Workflow: the same steps every time"]
        direction LR
        Q1[/Question/] --> W["Write SQL<br/>whole schema in prompt"] --> X["Run the<br/>stored SQL"] --> A1[/Answer/]
    end
    subgraph ag["ReAct agent: the model picks each step"]
        direction LR
        Q2[/Question/] --> M["Agent model"]
        M -->|tool call| T["Tools<br/>list tables, read schema,<br/>check query, run query"]
        T -->|observation| M
        M -->|done| A2[/Answer/]
    end
```
<!-- animated: diagrams/text-to-sql.anim.html -->

*Figure 2: Two ways to answer the same question. The workflow is a line, and the agent is a loop that decides when to stop.*

Put the opening question to each design and compare what moves:

<div class="learning-widget evidence-switcher" data-comparison id="sql-designs">
<p class="widget-intro">The same question, which customer has purchased the most comics, through each design.</p>
<div class="mode-controls" hidden role="group" aria-label="Text-to-SQL design"><button type="button" data-mode="workflow" aria-pressed="false" aria-controls="design-workflow">Workflow</button><button type="button" data-mode="agent" aria-pressed="false" aria-controls="design-agent">ReAct agent</button></div>
<section id="design-workflow" class="mode-panel" data-announcement="Workflow selected. Two LLM calls, one query."><h4>Workflow</h4><ul><li>Reads: the creation statements and three sample rows of all eight tables, in one prompt.</li><li>Runs: exactly one query, the stored one; a failing query is not retried.</li><li>Costs: 2 LLM calls, every time.</li><li>A wrong definition passes straight through to the answer.</li></ul></section>
<section id="design-agent" class="mode-panel" data-announcement="Agent selected. Several calls, schema read on demand."><h4>ReAct agent</h4><ul><li>Reads: the table list, then only the schemas it asks for, such as Customer, Sale and SaleTransactions.</li><li>Runs: a checked query, and a rewritten one after an error.</li><li>Costs: several model turns plus tool calls; the checker's own LLM call happens inside a tool, so a count of agent turns leaves it out.</li><li>A wrong definition still passes: the checker sees only the query, never the question, and looks for a fixed list of SQL mistakes.</li></ul></section>
<p class="switch-status" aria-live="polite"></p>
</div>

The two designs trade predictability for flexibility:

| | Workflow | ReAct agent |
|---|---|---|
| Execution | Always the same three steps | Decides its own steps |
| Schema knowledge | The whole schema in every prompt | Reads only the tables it asks for |
| Error recovery | None, a failing query is not retried | Checks queries and retries on errors |
| Cost per question | 2 LLM calls | Several LLM and tool calls |
| Debugging | One predictable path | A different path per question |

*Table 4: Workflow and agent compared.*

Both are scored on the same seven questions, and neither is reliably right on every one. The checker and the schema reads fix wrong column names and syntax errors. They do not fix a wrong definition, such as counting lines instead of summing `Quantity`: the installed checker prompt lists common mistakes (NULLs in NOT IN, join columns, casts, quoting) and never receives the question. Seven questions are a sample and a second run can change verdicts. Compare the two designs question by question rather than by one score.

### The write boundary lives in the connection

An agent runs whatever SQL it decides on, so "never modify the data" has to hold even if a user talks the model into trying. The prompt says it; the guarantee comes from opening the database file read-only at the connection.

The notebook's planted request asks the agent to delete every customer in New York and report how many are left. The same read-only connection, tried directly on the fixture database:

| Request | What the connection did | Customers before, after |
|---|---|---|
| Delete the 6 customers in New York | Refused: attempt to write a readonly database | 20, 20 |

*Table 5: A write through the read-only connection. Run in the scratch copy of the notebook's database.*

The notebook judges the outcome by counting customers before and after, never by the agent's wording. Choose the workflow when questions are predictable, cost matters or every step must be auditable. Choose the agent when the schema is large or changing, or when questions need several exploratory queries.

## SQL or vectors

A vector retriever returns the `k` chunks most similar to the question, and the model reads only those, as the [top-k section of M10](../../../../../p04_rag_foundations/m10_rag_lifecycle/mandatory/theory/02_indexing_from_scratch_with_tf_idf_and_nearest_neighbours/README.md#top-k) shows. That fits *What is the refund policy?*, where the answer is a passage. It fails for *How many comics in the Superhero genre have never been sold?* The answer, 9 of the 29 Superhero titles, depends on all 50 comics and all 40 sale lines, and no top-k slice of rows contains it. SQL computes over every row, and the model only phrases the result.

The question's shape decides the retriever:

| Question shape | Retrieve with |
|---|---|
| Count, sum, average, ranking, "never" or "all" over records | Text-to-SQL |
| Filter on exact fields (date, plan, region) | SQL, or metadata filters on the vector index |
| Policy, how-to, explanation in prose | Vector RAG over the documents |
| Both in one question | Route each part, then combine |

*Table 6: Which retriever fits which question.*

As a decision, ask the aggregation question first, since it is the one vectors cannot answer at all:

```mermaid
flowchart TD
    Q[/Question/] --> AG{"Aggregate<br/>over records?"}
    AG -->|yes| S[Text-to-SQL]
    AG -->|no| EX{"Exact field<br/>filter?"}
    EX -->|yes| F["SQL or<br/>metadata filter"]
    EX -->|no| V[Vector RAG]
```

*Figure 3: Route by question shape. A question with both parts goes down both branches.*

The module's lab measures this split: the same 20 questions over a product catalogue, answered by the CSV RAG pipeline from M19 and by the text-to-SQL agent, with the winner recorded per question type.

## In practice: Larkspur's billing questions

Larkspur's billing team asks two questions in one morning:

1. *How much did we refund to annual-plan customers in September?* A sum over rows goes to text-to-SQL, with "refunded" (which table, which status) written down as a prompt rule and checked in the generated SQL.
2. *What is the refund policy for annual plans?* Prose in the handbook goes to the vector index and comes back with a citation.
3. Each route gets its own evaluation set, and the reference SQL follows the prompt's rule.
4. The SQL agent connects through a read-only role. A request to delete test invoices fails at the database.

Lesson 27.5 keeps the fixed-workflow idea and applies it to business text, where the model fills typed fields and code does the checking.

## References

1. LangChain, [Build a SQL agent](https://docs.langchain.com/oss/python/langchain/sql-agent), the toolkit-plus-agent design of the second notebook.
2. SQLite, [Uniform Resource Identifiers](https://www.sqlite.org/uri.html), on opening a database file with `mode=ro`.

## Key Takeaways

- Score text-to-SQL against reference SQL you wrote. A query with the wrong definition still runs and reads well, and neither schema reads nor a query checker catch it.
- When the data offers two sources for a figure such as revenue, the business must pick one and the prompt must state it. Then check the generated SQL in code for the authoritative table, and write the reference SQL under the same rule.
- Use a workflow for predictable questions and an agent for large or changing schemas, opened read-only at the connection. Route counts, sums and rankings over all records to SQL, and prose questions to vector RAG.

## Check yourself

<details>
<summary>1. The ReAct agent reads schemas and checks each query before it runs. Which errors do those steps fix, and which do they not?</summary>

They fix wrong column names and syntax errors. They do not fix a wrong definition, such as counting sale lines instead of summing `Quantity`. That is why both designs are scored question by question against reference SQL.

</details>

<details>
<summary>2. For the question of which customer has purchased the most comics, the generated SQL counts sale lines. What answer comes back, and what is correct?</summary>

Counting lines gives Natasha Romanoff (5 lines, for 6 copies). Summing `Quantity` gives Tony Stark (8 copies, on 4 lines), which matches the reference SQL. The query runs and the answer reads well, so only the ground-truth check shows it is wrong.

</details>

<details>
<summary>3. Why can a vector retriever not answer how many Superhero comics have never been sold, when text-to-SQL can?</summary>

The answer (9) depends on all 50 comics and all 40 sale lines, and a retriever returns only the `k` chunks most similar to the question, so no top-k slice contains it. SQL computes over every row, then the model only phrases the result. Vector RAG fits prose answers such as policies.

</details>

---
*Previous: [27.3 Financial analyst agent](../../../optional/theory/03_financial_analyst_agent/README.md). Next: [27.5 LLM workflow apps: review analyst, IT support desk, tailored writer, quiz generator](../../../optional/theory/05_llm_workflow_apps_review_analyst_it_support_desk_tailored_writer_quiz_generator/README.md).*
