# M27.3 Theory: Financial analyst agent

*[M27 theory](../../../mandatory/theory/README.md) · Lesson 27.3 · Notebooks: [`03a_financial_analyst_agent.ipynb`](../../notebook/03a_financial_analyst_agent.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: A small project: a scoped agent over market-data tools, with arithmetic in code and every number checked -->
<!-- format: approved -->

## Start with a P/E the provider never returned

> **What you'll build**
>
> - **Five market-data tools** for ticker lookup, price performance, fundamentals, news and market movers, none of which needs a market-data key.
> - **Compact tool output** that summarises a year of daily prices in code before the model sees it.
> - **A scope** written into the system prompt as two flows and a polite refusal, checked on one request of each kind.
> - **Follow-up questions** on one thread, with the numbers in the answers checked against the provider.

An investor asks for Intel's P/E ratio. The provider has no trailing P/E for Intel, because its trailing earnings were negative when the notebook was written. An analyst agent that answers *about 30* anyway has turned a gap in the data into a financial claim, and the sentence reads exactly like a correct one.

A second risk sits in the arithmetic. Hand the model a year of daily prices and ask for the six-month return, and it has to compute a figure that code would get right every time. This project removes both risks: the tools do the arithmetic, and a missing value says it is missing.

## The project: a scoped financial analyst

Lesson 27.2's agents answered from web pages, where a claim can only be traced to a URL. This agent answers from structured market data, where every number has a source to compare against. The machinery is unchanged: a `create_agent` agent from [M23](../../../../../p06_agent_foundations/m23_react_agents/mandatory/theory/README.md), tools in the style of M22 and an M09 checkpointer for follow-ups.

What changes is the discipline around numbers. The model reads figures and never computes them, a missing value says it is missing, and the agent declines questions outside its job. On Larkspur the same shape would fit a billing analyst over invoice data. The notebook is an engineering exercise, not investment advice.

## Architecture

The agent sits between an investor and five tools, each backed by a free data provider:

```mermaid
flowchart LR
    I[Investor] --> A["Analyst agent<br/>scope prompt + date"]
    A --> T["Ticker lookup<br/>SEC"]
    A --> P["Price metrics<br/>Yahoo Finance"]
    A --> F["Fundamentals<br/>Yahoo Finance"]
    A --> N["News<br/>web news search"]
    A --> M["Market movers<br/>Yahoo Finance"]
```

*Figure 1: The analyst and its tools. OpenBB routes each market-data call to a provider, and news comes from a web search.*

Table 1 lists each piece and the earlier lesson it reuses:

| Piece | What it does | Built on |
|---|---|---|
| **Ticker lookup** | Company name to ticker, SEC name and CIK, best five matches. A failed lookup returns a hint to fix the spelling | M22 tool errors as messages |
| **Price metrics** | Latest quote, returns over 1, 3, 6 and 12 months, 52-week range and moving averages, computed from a year of daily closes | |
| **Fundamentals** | P/E, forward P/E, market cap, margins and growth, with an explicit NOT AVAILABLE line for any missing key metric | |
| **News** | Up to five headlines from the last month, with dates and links | Lesson 27.2's search tool |
| **Market movers** | Most active stocks, top gainers and top losers, ten of each, with the percentage change formatted for the model | |
| **Scope prompt** | Today's date, then Flow 1 for market overviews, Flow 2 for a named company, and a friendly refusal for anything else | M23 `create_agent` |
| **Memory** | An in-memory checkpointer keyed by a thread id | M09 checkpointers |

*Table 1: The project's pieces.*

The price tool is where the arithmetic moves out of the model. Here is what each design hands over per call:

| Design | What the model receives | Who computes returns |
|---|---|---|
| Raw history | About 250 daily closes for a year | The model |
| The notebook's tool | 14 fields: symbol, name, currency, last price, previous close, day range, 52-week high and low, two moving averages, four returns | Code |

*Table 2: One year of prices, two ways. Returns use 21 trading days per month; the one-year return spans the whole fetched history.*

Two details of that tool matter when you read its output. The 52-week high and low are the highest and lowest daily closes, so an intraday peak above the close does not appear. A return is computed only when the history holds enough trading days, so a stock listed six months ago gets no one-year figure instead of a wrong one.

The fundamentals tool applies the same rule to missing data. It checks three key metrics (P/E, forward P/E and market cap) and appends a NOT AVAILABLE line naming any the provider left empty, with a note that a missing P/E usually means negative trailing earnings. Call the failure it prevents an **invented figure**: a plausible number with no source.

## Following a misspelled question

The notebook checks the scope with one request per path, and passes each on what the agent called, not on its wording:

| Request | Expected path | Passes when |
|---|---|---|
| *Tell me some stocks I could potentially look into today.* | Flow 1 | The market-movers tool was called |
| *What is the P/E ratio of microsfot?* | Flow 2, with a spelling fix | Fundamentals were fetched for `MSFT` |
| *Can you recommend a good pasta recipe for tonight?* | Out of scope | No tool was called |

*Table 3: Three planted requests and their pass conditions.*

The misspelled request exercises the recovery rule in the prompt, which names this very example and also suggests a shorter name when a long one fails. The values change daily, and the trace shows only the call order:

```mermaid
sequenceDiagram
    participant A as Agent
    participant T as Tools
    A->>T: ticker lookup "microsfot"
    T-->>A: no match, try another spelling
    A->>T: ticker lookup "microsoft"
    T-->>A: MSFT and its CIK
    A->>T: fundamentals for MSFT
    T-->>A: P/E, forward P/E, margins
    Note over A: answer with the P/E
```

*Figure 2: A failed lookup becomes a hint the agent acts on, then the ticker feeds the next call.*

### A follow-up conversation, checked against the provider

The second test asks three questions on one thread, then fetches the same metrics from the provider directly and compares. Step through what each turn depends on:

<div class="walkthrough learning-widget" data-stepper id="pe-followups">
<p class="widget-intro">Follow the investor's three turns on thread investor-1, then the check that compares the answers with the provider.</p>
<div class="step-controls" hidden role="group" aria-label="Follow-up conversation turns"><button type="button" data-step="0" aria-pressed="false" aria-controls="pe-step-0">1. Nvidia</button><button type="button" data-step="1" aria-pressed="false" aria-controls="pe-step-1">2. And Intel</button><button type="button" data-step="2" aria-pressed="false" aria-controls="pe-step-2">3. Which is better</button><button type="button" data-step="3" aria-pressed="false" aria-controls="pe-step-3">4. The check</button></div>
<div class="step-panels"><section id="pe-step-0" class="step-panel" aria-labelledby="pe-heading-0"><h4 id="pe-heading-0">1. What is the P/E ratio of Nvidia?</h4><dl><dt>Tools</dt><dd>Ticker lookup if needed, then fundamentals for NVDA</dd><dt>Answer must hold</dt><dd>The provider's trailing P/E, rounded to one or two decimals</dd></dl></section><section id="pe-step-1" class="step-panel" aria-labelledby="pe-heading-1"><h4 id="pe-heading-1">2. And Intel?</h4><dl><dt>Depends on</dt><dd>The checkpointer: the turn names no metric, so the agent reads the first question from the thread</dd><dt>Tool output</dt><dd>Fundamentals for INTC, ending with NOT AVAILABLE for the trailing P/E when earnings are negative</dd></dl></section><section id="pe-step-2" class="step-panel" aria-labelledby="pe-heading-2"><h4 id="pe-heading-2">3. Which of the two looks better on valuation?</h4><dl><dt>Depends on</dt><dd>Both earlier tool results in the thread</dd><dt>Expected</dt><dd>A short comparison that uses only those figures, with the prompt's do-your-own-research caveat</dd></dl></section><section id="pe-step-3" class="step-panel" aria-labelledby="pe-heading-3"><h4 id="pe-heading-3">4. The check against a direct fetch</h4><dl><dt>Nvidia</dt><dd>Passes when some number in the answer is within 0.051 of the provider's trailing P/E</dd><dt>Intel, no trailing P/E</dt><dd>Passes when the answer says it is unavailable (or negative, or not applicable) or quotes the forward P/E</dd><dt>Fails</dt><dd>Any other P/E figure: an invented figure</dd></dl></section></div>
<div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div>
</div>

If the provider does return a trailing P/E for Intel on the day you run it, the check switches to requiring that figure, as it does for Nvidia.

## Design choices worth copying

Each choice below protects against a failure this page or an earlier lesson names:

| Choice | Why |
|---|---|
| **Compute returns and ranges in code** | The model reads the figures instead of calculating them from 250 rows, and 14 fields cost far less context |
| **Name missing values** | A missing P/E stated as NOT AVAILABLE cannot be mistaken for zero or filled in with an invented figure |
| **Turn a failed lookup into a hint** | The agent retries with a corrected or shorter name instead of stopping (lesson 22.5) |
| **Scope with a refusal path** | Off-topic requests get a friendly decline and no tool calls, and a test proves it |
| **Check numbers against a direct fetch** | The answer is compared with the provider's own figures, never with the model's summary |
| **Key-less providers** | SEC and Yahoo Finance need no key. The notebook runs with no extra market-data accounts |

*Table 4: Six choices and what each one protects against.*

## Limits

- **Live data.** Every run sees different prices. The checks test agreement with the provider at run time, never fixed values.
- **Scope lives in the prompt.** Nothing in code blocks an off-topic tool call, and one request per path is a sample. A determined user can talk the agent around.
- **A loose number match.** The check accepts any number within 0.051 of the provider's value, so an unrelated figure that happens to be close also passes. The Intel check accepts keywords such as "negative", which a wrong answer can also contain.
- **Closing prices only.** The 52-week range comes from daily closes and can sit inside the range a trading site shows.
- **Advice.** The prompt allows recommendations with a do-your-own-research caveat. A production version would need compliance review.

The notebook needs OpenAI and Tavily keys and the course's `finance` dependency group, which cannot share an environment with the protocol groups.

## References

1. OpenBB, [Platform documentation](https://docs.openbb.co/platform), on providers behind one market-data interface.
2. LangChain, [Agents](https://docs.langchain.com/oss/python/langchain/agents), the `create_agent` loop the analyst runs on.
3. LangChain, [Short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory), on checkpointers and thread ids.

## Key Takeaways

- Do the arithmetic in the tool and hand the model a short table, so it reads figures instead of computing them from hundreds of rows.
- Make missing values explicit in tool output, and treat any figure the provider did not return as invented.
- Test a scoped agent on one request per path, judging each by the tools it called, and check its numbers against a direct fetch from the same provider.

## Check yourself

<details>
<summary>1. Why does the price tool compute returns and the 52-week range in code instead of passing a year of prices to the model?</summary>

A year of daily prices is about 250 rows. The tool reduces them to 14 fields, which costs far less context, and the model only reads the returns and range rather than calculating them, which it does unreliably.

</details>

<details>
<summary>2. The provider has no trailing P/E for a company with negative earnings. What does the fundamentals tool return, and what does the answer check accept?</summary>

The tool ends its output with an explicit NOT AVAILABLE line naming the missing metric. The check accepts an answer that says the trailing P/E is unavailable or quotes the forward P/E, and treats any other P/E figure as invented.

</details>

<details>
<summary>3. How does the notebook show that the analyst's scope works, and what does the out-of-scope request prove?</summary>

It sends one request per path and passes each on the tools called: market movers for the overview, fundamentals for MSFT after the misspelled lookup, and no tools for the pasta recipe. The last shows the refusal path declines without touching any tool on that request; one sample does not prove every off-topic request is blocked.

</details>

---
*Previous: [27.2 Research and competitive-intelligence agents](../../../mandatory/theory/02_research_and_competitive_intelligence_agents/README.md). Next: [27.4 Text-to-SQL: workflow vs ReAct agent](../../../mandatory/theory/04_text_to_sql_workflow_vs_react_agent/README.md).*
