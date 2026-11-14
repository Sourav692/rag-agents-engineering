# M17.4 Theory: Step-back prompting

*[M17 theory](../README.md) · Lesson 17.4 · Notebooks: [`04a_step_back_prompting.ipynb`](../../notebook/04a_step_back_prompting.ipynb) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: A narrow question retrieves its premise; a broader one retrieves what settles it -->
<!-- format: approved -->

## The specificity trap

> **What you'll learn**
>
> - **Explain** why a specific question, especially one with a false premise, retrieves the wrong context.
> - **Trace** step-back retrieval: a broader question, two searches, one combined context.
> - **Explain** why two worked examples teach "make it broader" better than an instruction.
> - **Choose** between step-back and plain retrieval by question type and cost.

Lessons 17.2 and 17.3 reworded the question to reach the handbook's vocabulary. Rewording keeps the question's scope. Some questions fail because the scope itself is wrong.

Notebook `04a` opens with *Did Leonardo da Vinci invent the printing press?* A retriever searches for exactly that and mostly finds pages about Gutenberg, movable type and 1440. None of them says what Leonardo did invent, which is the knowledge that settles the question. The question carries a **false premise**, and searching on its words retrieves documents about the premise rather than the answer.

We call this the **specificity trap**: the narrower and more assumption-laden the question, the more its words steer retrieval toward the assumption.

Larkspur has the same shape of question. A customer on a monthly plan asks *Can I get a refund on my monthly plan?* The handbook offers refunds on annual plans only, and the answer the customer needs is "no, but cancelling stops the next charge". That second fact sits in the `cancel` chunk, which shares almost no words with the question.

## Asking the broader question

**Step-back prompting** (Zheng et al., [arXiv:2310.06117](https://arxiv.org/abs/2310.06117)) asks an LLM for a more general question, retrieves for both the original and the general one, and answers from the combined context:

```mermaid
flowchart LR
    Q[/Question/] --> G["LLM writes a<br/>broader question"]
    Q --> R1["Retrieve<br/>original"]
    G --> R2["Retrieve<br/>step-back"]
    R1 --> A["Answer prompt<br/>both contexts + question"]
    R2 --> A
```

*Figure 1: Step-back retrieval. Two searches, one for specifics and one for background.*

The two contexts do different jobs. The original question's context supplies specifics; the step-back context supplies the background that can correct a premise. `04a` feeds both, plus the original question, to a community answer prompt written to take exactly those three inputs.

Here is the Larkspur refund question through those stages. The step-back question is written by hand and the chunks come from the M10 index, as in Table 1 below:

<div class="walkthrough learning-widget" data-stepper id="stepback-walkthrough">
<p class="widget-intro">Step through the monthly-plan refund question from the step-back call to the answer prompt.</p>
<div class="step-controls" hidden role="group" aria-label="Stages of step-back retrieval"><button type="button" data-step="0" aria-pressed="false" aria-controls="stepback-step-0">1. Step back</button><button type="button" data-step="1" aria-pressed="false" aria-controls="stepback-step-1">2. Two searches</button><button type="button" data-step="2" aria-pressed="false" aria-controls="stepback-step-2">3. Combine</button><button type="button" data-step="3" aria-pressed="false" aria-controls="stepback-step-3">4. Answer</button></div>
<div class="step-panels"><section id="stepback-step-0" class="step-panel" aria-labelledby="stepback-heading-0"><h4 id="stepback-heading-0">1. Step back</h4><dl><dt>Input</dt><dd><em>Can I get a refund on my monthly plan?</em></dd><dt>Call</dt><dd>one LLM call, primed with the two worked examples of Table 2</dd><dt>Output</dt><dd><em>What is the refund policy for each plan type?</em></dd></dl></section><section id="stepback-step-1" class="step-panel" aria-labelledby="stepback-heading-1"><h4 id="stepback-heading-1">2. Two searches</h4><dl><dt>Original</dt><dd><code>refund-window</code>, <code>billing</code>, <code>sla</code></dd><dt>Step-back</dt><dd><code>refund-window</code>, <code>retention</code>, <code>cancel</code></dd><dt>Order</dt><dd>independent; they run in parallel</dd></dl></section><section id="stepback-step-2" class="step-panel" aria-labelledby="stepback-heading-2"><h4 id="stepback-heading-2">3. Combine</h4><dl><dt>Context</dt><dd>five distinct chunks; <code>refund-window</code> appears in both</dd><dt>New fact</dt><dd><code>cancel</code>: cancelling stops the next charge</dd></dl></section><section id="stepback-step-3" class="step-panel" aria-labelledby="stepback-heading-3"><h4 id="stepback-heading-3">4. Answer</h4><dl><dt>Prompt inputs</dt><dd>the original context, the step-back context and the original question</dd><dt>Answer it can now give</dt><dd>no refund on a monthly plan, and cancelling stops the next charge</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

Here are both questions for each example, with what each one surfaces:

| | Question searched | What it surfaces |
|---|---|---|
| Original | *Did Leonardo da Vinci invent the printing press?* | Printing-press history: Gutenberg |
| Step-back | *What inventions is Leonardo da Vinci associated with?* | Leonardo's actual work |
| Original | *Can I get a refund on my monthly plan?* | `refund-window`, `billing`, `sla` |
| Step-back | *What is the refund policy for each plan type?* | `refund-window`, `retention`, `cancel` |

*Table 1: Original against step-back retrieval. The Leonardo rows are `04a`'s live web search; the Larkspur rows are the top 3 from the M10 TF-IDF index, with the step-back question written by hand.*

The same question with and without the second search:

<div class="learning-widget evidence-switcher" data-comparison id="stepback-switcher">
<p class="widget-intro">Choose which retrieval feeds the answer prompt for the monthly-plan refund question.</p>
<div class="mode-controls" hidden role="group" aria-label="Retrieval used">
<button type="button" data-mode="plain" aria-pressed="false" aria-controls="stepback-plain">Original only</button>
<button type="button" data-mode="both" aria-pressed="false" aria-controls="stepback-both">Original plus step-back</button>
</div>
<section id="stepback-plain" class="mode-panel" data-announcement="Original only selected. Three chunks, no cancel fact."><h4>Original only (plain RAG)</h4><dl><dt>Context</dt><dd>3 chunks: <code>refund-window</code>, <code>billing</code>, <code>sla</code></dd><dt>What the model can say</dt><dd>refunds apply to annual plans; nothing on what a monthly customer can do instead</dd><dt>Cost</dt><dd>1 LLM call, 1 retrieval</dd></dl></section>
<section id="stepback-both" class="mode-panel" data-announcement="Original plus step-back selected. Five chunks, cancel fact included."><h4>Original plus step-back</h4><dl><dt>Context</dt><dd>5 distinct chunks, adding <code>retention</code> and <code>cancel</code></dd><dt>What the model can say</dt><dd>no refund on a monthly plan, but cancelling stops the next charge</dd><dt>Cost</dt><dd>2 LLM calls, 2 retrievals</dd></dl></section>
<p class="switch-status" aria-live="polite"></p>
</div>

On the Larkspur handbook the gain is small and honest. Both questions find `refund-window`, the chunk that states the annual-plan rule. The step-back question adds `cancel`, the fact the customer needs next, and the combined context holds five distinct chunks where the original held three. On a twelve-chunk handbook there is little background to miss; on the open web, `04a`'s search results move from Gutenberg to Leonardo.

## Teaching abstraction by example

"Make this question more general" is hard to specify in prose. Too loose, and the model rewrites the question into something unrelated; too strict, and it barely changes anything. `04a` teaches the move with two worked examples instead:

| Input | Output |
|---|---|
| *Did the Beatles ever write a book?* | *What types of creative works did the Beatles produce?* |
| *Was Albert Einstein a musician?* | *What fields did Albert Einstein work in?* |

*Table 2: The two few-shot examples in `04a`.*

Both show the same pattern: a yes-or-no question about one specific thing becomes an open question about the category it belongs to. The few-shot template expands into real message pairs (a user turn, then the model's reply) before the real question, so the model imitates the pattern rather than interpreting an instruction.

The pattern can overshoot. We call that **over-generalising**: a step-back question so broad that it retrieves a vague overview instead of the background that matters. *What does Larkspur offer?* would be a step back from the refund question too, and it would retrieve almost anything.

## When it pays

Step-back doubles the calls of plain RAG:

| | Plain RAG | Step-back RAG |
|---|---|---|
| LLM calls per question | 1 (answer) | 2 (step-back question, answer) |
| Retrievals | 1 | 2 |
| False-premise questions | Often confidently wrong | Retrieves the context that corrects the premise |
| Multi-hop or reasoning questions | Weak | Background context supports the reasoning |
| Direct lookups | Ideal | Wasted call; the broad query can dilute a precise one |
| Failure mode | Misses context | Over-generalises and retrieves something vague |

*Table 3: Plain against step-back RAG, from `04a`'s comparison.*

The two retrievals are independent. `04a` runs them in parallel, and the extra latency is mostly one short LLM call.

> **Interview tip:** step-back helps only when the corpus contains the broader background. On a narrow corpus, generalising returns the same documents, as the Larkspur rows of Table 1 nearly do.

## In practice: step-back on Larkspur's policy questions

1. **Route yes-or-no policy questions here**, especially ones that name a plan, a period or an amount the policy might not cover.
2. **Write Larkspur few-shots**: *Can I pause my server for a month?* becomes *What can I change about a running server?*
3. **Keep the original retrieval.** It supplies the specifics; the step-back retrieval only adds background.
4. **Skip direct lookups** such as *What is the refund window?*, where the original question already matches the chunk.

Lesson 17.5 attacks the other half of the asymmetry from lesson 17.1: not the question's scope, but its shape.

## Limits

- **The Leonardo rows are a live web search.** `04a` searches DuckDuckGo with four results per query: its contexts change from run to run. When the search fails, the notebook's wrapper returns the placeholder "(web search unavailable)" instead of raising: the chain still answers, from no evidence. Print both contexts before judging an answer.
- **The Larkspur step-back question is hand-written.** Table 1's Larkspur rows show what a good step-back question retrieves, not what a model wrote.
- **The answer prompt is pulled from a public hub.** `04a` loads a community prompt at run time, which means its wording can change upstream. Pin or copy a prompt you depend on.
- **No accuracy measurement.** The notebooks compare contexts, not answer accuracy. The paper's reported gains come from its own benchmarks and models.

## References

1. Zheng et al., [Take a step back: evoking reasoning via abstraction in large language models](https://arxiv.org/abs/2310.06117), 2023.
2. LangChain, [FewShotChatMessagePromptTemplate API reference](https://reference.langchain.com/python/langchain-core/prompts/few_shot/FewShotChatMessagePromptTemplate).

## Key Takeaways

- A specific question, especially one with a false premise, steers retrieval toward its assumption (the specificity trap): Leonardo's question finds Gutenberg.
- Step-back retrieves for the original and a broader question and answers from both. It costs 2 LLM calls and 2 retrievals, and helps only where the corpus holds the background.
- Teach the abstraction with two worked examples, and watch for over-generalising, a step-back question too broad to retrieve anything specific.

## Check yourself

<details>
<summary>1. Why does "Did Leonardo da Vinci invent the printing press?" retrieve pages about Gutenberg?</summary>

The question carries a false premise, and its words are about the printing press, so retrieval finds documents about the premise. The knowledge that settles it, what Leonardo did invent, shares few of those words. A broader step-back question retrieves it.

</details>

<details>
<summary>2. For "Can I get a refund on my monthly plan?", what does the step-back question add to the Larkspur context?</summary>

Both questions retrieve `refund-window`, which states the annual-plan rule. The step-back question, *What is the refund policy for each plan type?*, adds `cancel`, which says cancelling stops the next charge, the fact a monthly customer needs. The gain is small because the handbook is small.

</details>

<details>
<summary>3. A teammate wants step-back on every Larkspur question. What do you tell them?</summary>

It doubles the calls (2 LLM calls and 2 retrievals) and only helps specific or premise-laden questions on a corpus with background to find. Direct lookups lose a call and risk a diluted query. Route policy questions with a possible false premise to step-back and send direct lookups straight to retrieval.

</details>

---
*Previous: [17.3 RAG-Fusion with Reciprocal Rank Fusion](../03_rag_fusion_with_reciprocal_rank_fusion/README.md). Next: [17.5 HyDE: embed a hypothetical answer](../05_hyde_embed_a_hypothetical_answer/README.md).*
