# M27.5 Theory: LLM workflow apps: review analyst, IT support desk, tailored writer, quiz generator

*[M27 theory](../../../mandatory/theory/README.md) · Lesson 27.5 · Notebooks: [`05a_review_analyst.ipynb`](../../notebook/05a_review_analyst.ipynb) (optional), [`05b_multilingual_it_support_desk.ipynb`](../../notebook/05b_multilingual_it_support_desk.ipynb) (optional), [`05c_audience_tailored_writer.ipynb`](../../notebook/05c_audience_tailored_writer.ipynb) (optional), [`05d_quiz_generator.ipynb`](../../notebook/05d_quiz_generator.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: The model fills typed fields, and code routes, checks and renders everything with a right answer -->
<!-- format: approved -->

## A reply that invents a number

> **What you'll learn**
>
> - **Explain** the shape every workflow app shares: typed LLM steps, then checks and rendering in code.
> - **Compare** four applications of that shape by what the model fills and what code verifies.
> - **Diagnose** the planted failures each check catches: a wrong route, an invented figure, an unsupported quote.
> - **Choose** between one structured call and a chain of calls by measuring both on the same inputs.

Lesson 27.4 compared a fixed SQL workflow with an agent and found the workflow cheaper, more predictable and easier to test. This lesson applies the fixed workflow to business text: reviews, support tickets, a fact sheet, a PDF.

Larkspur's support queue gets tickets in several languages. A model can read each one, sort it and draft a reply, and most drafts are good. The bad ones read just as well. A draft that tells a customer the annual-plan refund window is 14 days, when the handbook says 30, looks exactly like a correct draft until someone checks the number.

So the model's output needs a shape that code can inspect, and the decisions with a right answer need to move out of the model.

## Workflow apps

**A workflow app runs a fixed sequence of LLM steps over business text, with no tool loop.** The model fills typed fields, and code does everything that has a right answer: routing, checking and assembling the final document. Anything that fails a check goes to a person instead of the customer:

```mermaid
flowchart LR
    IN[/"Business text"/] --> S["LLM step<br/>structured output"]
    S --> C{"Checks in code<br/>pass?"}
    C -->|yes| R["Route and render<br/>in code"]
    C -->|no| H["Flag for<br/>human review"]
```

*Figure 1: The shared shape. Only the first box is a model call.*

Four notebooks apply that shape to four jobs. Table 1 sets them side by side by what the model fills and what code verifies:

| App | The model fills | Code decides or checks |
|---|---|---|
| **Review analyst** | One typed analysis per review (summary, positives, negatives, a three-value sentiment, 3 to 5 emotions), for six reviews in one batch, then one email per review | Sentiment against hand labels; the email writer by dictionary lookup; each email's greeting, sign-off, tone and length |
| **IT support desk** | Language, category, English translation and replies for ten tickets in nine languages, in one of two designs | Detected language, a reply that really is translated, leaked prompt text, calls and wall time |
| **Audience-tailored writer** | Three adverts from one phone fact sheet and three reports from one research abstract, each set written in parallel | Headings, a five-row specification table, word and line limits, bullet counts, and every number against the source |
| **Quiz generator** | A summary of a PDF on prompt engineering, then five questions, each with four options, an answer index and an evidence quote | Question count, four distinct options, a valid index, every quote in the PDF text, and the final sheet from a template |

*Table 1: Four workflow apps. Each row is one notebook.*

Three details in those notebooks are easy to miss. The review analyst checks its sentiment against six hand labels before any email goes out, because the sentiment picks the email: the office-lamp review mixes a damaged part with praise for the support team, and a person labelled it positive. Its instruction router classifies a free-text request into four intents (summarise, sentiment, email, other). The quiz generator cleans the PDF text before any check runs: raw extraction from the 4,917-character file holds 768 line breaks, roughly one word per line, and an exact-quote check on that text would fail every honest quote.

### Five rules for the model's output

The four apps differ in content and agree on these rules:

- **Ask for a closed type.** A sentiment that can only be positive, negative or neutral gives code a value to branch on. An answer index points at an option instead of restating it, so the answer cannot drift from the options.
- **Route in code when the signal is already structured.** The review analyst picks the email writer with a dictionary and no extra model call. When the input is free text, as in its instruction router, classify into a closed set of intents and keep an `other` intent for requests the tool does not handle.
- **Check every output with code that cannot be talked round.** String and number checks are cheap enough to run on every call.
- **Render the final document in code.** Asking the model to merge a checked summary and checked questions into a report would let it reword them after the checks. Call that **post-check rewording**. A template cannot do it, and it marks any question that failed a check for review by hand.
- **Measure the design choice** on the same inputs before picking it, as the support desk does below.

### Planted failures the checks catch

Each notebook plants at least one bad output to prove its check works. The first three rows below were rerun from the notebooks' own check functions:

| Planted output | Check | Result |
|---|---|---|
| "Dear Customer, we are sorry to hear about your experience. Regards, Support", sent for a positive review | Email rules | Fails signature and tone |
| An advert table listing a 50 MP camera, when the fact sheet gives RAM, screen sizes, resolution and battery rating but no camera resolution | Every number in the source | Flags 50 as unsupported |
| A quiz question whose evidence is "Fine-tuning always requires at least 50 examples." | Evidence quote in the PDF | Evidence not found in the PDF |
| *What's the capital of France?* sent to the instruction router | Closed intents | Expected intent `other` (a live model call) |

*Table 2: One planted failure per check. Rows 1 to 3 come from running the notebooks' check functions in a scratch copy.*

The second row is an **invented figure**, a plausible number with no source. A schema checks the table's shape and cannot know the number is false. Only the comparison with the source catches it. The number check ignores list numbering and the values 0 and 1, so "Gen 1" or "1 year" does not raise a false alarm.

A failed evidence check is a flag, not a verdict. The model may have paraphrased a true sentence, or quoted its own summary instead of the PDF, which the prompt forbids and which still happens. The question goes to a reviewer either way.

## One call or four: the support desk

The support desk is the one app that measures two designs against each other. Both start from the same ticket:

```mermaid
flowchart TB
    T[/Ticket/] --> A["Design A<br/>one structured call"]
    T --> D["Design B<br/>detect language"]
    D --> TR["Translate<br/>to English"]
    TR --> AN["Answer<br/>in English"]
    AN --> BK["Translate<br/>back"]
```

*Figure 2: The two designs. Design A returns all six fields at once, and Design B makes one call per step.*

The call count follows from the shapes:

| Design | Calls per ticket | Calls for the 10 tickets |
|---|---|---|
| A: one structured call | 1 | 10 |
| B: four-step chain | 4 | 40 |

*Table 3: Model calls per design. Wall time depends on the provider and is measured in the notebook.*

Switch between the designs to see what each one gives you for the same Japanese ticket about printer toner:

<div class="learning-widget evidence-switcher" data-comparison id="desk-designs">
<p class="widget-intro">One ticket, two designs: what comes back, what can go wrong and what you can change.</p>
<div class="mode-controls" hidden role="group" aria-label="Support desk design"><button type="button" data-mode="a" aria-pressed="false" aria-controls="desk-a">A: one structured call</button><button type="button" data-mode="b" aria-pressed="false" aria-controls="desk-b">B: four-step chain</button></div>
<section id="desk-a" class="mode-panel" data-announcement="Design A selected. One call returns six typed fields."><h4>Design A: one structured call</h4><ul><li>Returns: six typed fields at once (original message, language, category, English translation, reply, English reply).</li><li>Costs: 1 call per ticket.</li><li>Typical risk: a wrong field, visible only after the call; nothing in between to inspect.</li><li>Prompt text cannot leak into a field the way it can into free text.</li></ul></section>
<section id="desk-b" class="mode-panel" data-announcement="Design B selected. Four calls, each output visible."><h4>Design B: four-step chain</h4><ul><li>Returns: each step's text, added to one record in order; steps for one ticket run one after another.</li><li>Costs: 4 calls per ticket.</li><li>Typical risk: a step copies a code fence from the prompt's delimiters, or a line such as "The customer message in English is:", into the next step and the reply.</li><li>Gains control: each step can be tested, cached, logged or given its own model, and a bad translation shows up as its own value.</li></ul></section>
<p class="switch-status" aria-live="polite"></p>
</div>

Design A makes a quarter of the calls and leaves no room for **scaffolding leaks**. Design B buys control, which matters once you need to inspect, reuse or upgrade one step. The notebook measures language accuracy, translated replies, leaks, calls and wall time on the same tickets, and its advice follows: start with one call, and move a step into its own prompt when you need that control.

## In practice: Larkspur's support queue

Here is the same shape on Larkspur's tickets:

1. **One structured call per ticket** returns the language, a category (refund, outage, sizing) and a draft reply.
2. **Code routes** outage tickets to the incident template.
3. **Code checks** that every number in a reply appears in the handbook, such as the 30-day refund window for annual plans and the 99.95% availability guarantee. The 14-day draft from the opening fails here.
4. **A person sees** any reply that fails a check before the customer does.
5. **Actions go through the gate.** A reply that issues a refund is an action. It goes through the [approval gate from lesson 27.1](../../../mandatory/theory/01_dry_run_harness_and_human_approval/README.md#approval-gates), which binds the approval to the previewed action.

These apps are workflows in the sense of lesson 27.4: the same steps every time, cheap and testable. Choose an agent only when the next step depends on what the model finds.

## References

1. Anthropic, [Building effective agents](https://www.anthropic.com/research/building-effective-agents), on workflows with predefined paths versus agents that direct their own steps.
2. LangChain, [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output), on returning a typed record from one model call.

## Key Takeaways

- In a workflow app the model fills typed fields and code does everything that has a right answer. Ask for closed types, such as a three-value sentiment, so code can branch on them without another LLM call.
- Check every output with code that cannot be talked round, such as confirming each number appears in the source. Render the final document from a template so nothing is reworded after the checks.
- Measure a design choice on the same inputs before picking it. Send actions such as issuing a refund through an approval gate, and choose an agent only when the next step depends on what the model finds.

## Check yourself

<details>
<summary>1. Why do the workflow apps render the final document from a template instead of asking the model to merge the checked parts?</summary>

A model asked to merge a checked summary and checked questions could reword them after the checks ran. A template cannot, so what the user reads is exactly what passed the checks.

</details>

<details>
<summary>2. The writer's fact sheet gives RAM, screen sizes and a battery rating but no camera figure, and an advert claims 50 MP. What catches it?</summary>

The code check that every number in the output appears in the source flags "50" as unsupported. String and number checks are cheap enough to run on every call. The Larkspur triage version runs the same check against the handbook's numbers, such as the 30-day refund window.

</details>

<details>
<summary>3. For the multilingual support desk, should you use one structured call per ticket or the four-step translate chain?</summary>

Measure both on the same tickets before choosing. One structured call makes a quarter of the LLM calls (10 against 40 for ten tickets), and the chain's free-text steps can leak a code fence or "The customer message in English is:" into the reply. The chain earns its cost when you need to test, cache, log or swap one step.

</details>

---
*Previous: [27.4 Text-to-SQL: workflow vs ReAct agent](../../../mandatory/theory/04_text_to_sql_workflow_vs_react_agent/README.md). Next: [M27 interview questions](../../../mandatory/theory/README.md#interview-spotlight-5-questions-you-might-get-asked).*
