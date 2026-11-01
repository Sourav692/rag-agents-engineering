# M34.5 Theory: MemGPT tiers, Voyager skill library, Agent Workflow Memory

*[M34 theory](../README.md) · Lesson 34.5 · Notebooks: [`05a_memgpt_tiered_memory.ipynb`](../../../../course/p10_memory_and_multi_agent/m34_long_term_agentic_memory/notebooks/05a_memgpt_tiered_memory.ipynb), [`05b_voyager_skill_library.ipynb`](../../../../course/p10_memory_and_multi_agent/m34_long_term_agentic_memory/optional/05b_voyager_skill_library.ipynb) (optional), [`05c_agent_workflow_memory.ipynb`](../../../../course/p10_memory_and_multi_agent/m34_long_term_agentic_memory/optional/05c_agent_workflow_memory.ipynb) (optional) · [All theory pages](../../../README.md)*

## Tiered memory

MemGPT (Packer et al., 2023, [arXiv:2310.08560](https://arxiv.org/abs/2310.08560); the framework is now Letta) treats the context window like an operating system treats RAM. A small **main context** is always in the prompt; an unbounded **archival memory** sits outside it, like disk. The agent moves information between the two with tools, so the agent decides what stays close, where the earlier lessons used a fixed rule.

| Tier | Holds | In the prompt? | The notebook's version |
|---|---|---|---|
| Core memory | A few durable facts, in named blocks (`persona`, `human`) | Always | A dict, edited by tools |
| Message window | The last N messages | Always | A list capped at `max_messages = 6` |
| Archival memory | Evicted messages and anything inserted on purpose | Only what a search returns | A list with a keyword-overlap search, top 3 |

The model gets four tools: `core_memory_append` and `core_memory_replace` edit core memory, `archival_memory_insert` and `archival_memory_search` move things to and from the archive. Every turn rebuilds the system prompt from the current core memory, runs any tool calls (at most `MAX_TOOL_ROUNDS = 5` rounds), and then appends the answer to the window, which evicts the oldest messages once the window is full.

```mermaid
flowchart LR
    N[/New message/] --> W["Window<br/>last 6 messages"]
    W -- overflow --> AR[("Archive<br/>evicted messages")]
    C["Core memory<br/>always in prompt"] --> P[Prompt]
    W --> P --> L[Model]
    L -- search --> AR
```
<!-- animated: diagrams/paging.anim.html -->

The [interactive lab](interactive/tiered-memory-lab.html) runs the notebook's `MainContext` and `ArchivalMemory` code, ported to JavaScript and checked against the Python classes on every window size from 1 to 12 and 408 queries (4,932 comparisons, 0 mismatches). Dana tells the Larkspur assistant her plan in turn 1, says in turn 2 that she bought it 12 days ago and has used 80 GB of outbound traffic, asks three unrelated questions, and in turn 6 asks whether she can still get a full refund. The handbook's rule needs both numbers.

| Window (`max_messages`) | Messages in view at turn 6 | Archived | Prompt, about this many tokens | Turn-2 message |
|---|---|---|---|---|
| 1 | 1 | 10 | 44 | Archived |
| 6 | 6 | 5 | 117 | Archived |
| 9 | 9 | 2 | 156 | In view |
| 11 or more | 11 | 0 | 195 | In view |

Token counts are characters divided by four, for core memory plus the window. At the notebook's window of 6, the answer depends on a search the model must decide to make, and on the words it chooses:

| Query the agent sends | Turn-2 message | Why |
|---|---|---|
| `outbound traffic` | Rank 1 | Shares 2 words |
| `refund annual plan` | Rank 3 of 3 | Shares only `plan`; both turn-1 messages also score 1, on `annual`, and come first |
| `how much traffic?` | Missed | `traffic?` is not `traffic`; the search returns "How do I reboot a server?" on `how` |
| `data usage this month` | Missed | No shared word at all |

<!-- lab: interactive/tiered-memory-lab.html -->

Three things follow from those numbers:

- **The window is a budget.** Each extra message is paid on every call. A window of 9 keeps Dana's traffic message in view at about 156 tokens of conversation per call, against 117 at a window of 6.
- **Recall depends on the agent asking.** The notebook checks in code whether the model called `archival_memory_search` in turn 6. If it did not, the answer comes without the 80 GB figure. The notebook also had to tell the model to keep one-off details out of core memory; without that rule gpt-4o-mini tends to put every detail in core memory, and the archive stops mattering.
- **The search is part of memory quality.** The notebook's keyword overlap keeps punctuation and ties easily. A real system embeds archive entries and searches by meaning (M14), the same retrieval choices as any RAG index.

## Skill library

The earlier layers remember facts and events. Two architectures remember capabilities: code that worked, and tool-call sequences that worked. Both follow one loop: look in the library first, build something new only when nothing fits, check it, and store only what passed.

```mermaid
flowchart TD
    T[/New task/] --> L{"Library has<br/>a fit?"}
    L -- yes --> RU[Reuse or compose]
    L -- no --> GN[Generate new]
    GN --> V{"Passes<br/>its tests?"}
    V -- yes --> SV[Store it]
    V -- no --> X[Discard]
```

**Voyager** (Wang et al., 2023, [arXiv:2305.16291](https://arxiv.org/abs/2305.16291)) played Minecraft without fine-tuning by saving each working piece of code as a named skill. The notebook moves the idea to small Python text tasks:

- The library maps a skill name to its description, code, function and usage count, seeded with `count_vowels` and `reverse_string`.
- Before generating, a model call reads the library's descriptions and decides `reuse: true` or `false`. Task 3 composes the whitespace remover the agent wrote in Task 2 with `reverse_string`, with no code-generation call at all. Task 4's new palindrome check calls library skills inside its own code.
- Every new skill, and every reuse, runs against test cases before it counts, and the test cases must be able to fail. A candidate that always returns `True` is rejected on Task 4's first `False` case.
- Generated code is untrusted. The notebook screens it with a denylist, runs it with restricted builtins in a child `python -I` process with an empty environment and a timeout, and says plainly that a denylist is not a sandbox: code from a model you do not control belongs in a container or a hosted sandbox with no network and no secrets.

**Agent Workflow Memory** (Wang et al., 2024, [arXiv:2409.07429](https://arxiv.org/abs/2409.07429)) stores procedures instead of code. A small ReAct loop logs every tool call; after a success, a model call turns the concrete trajectory into a template with placeholders (look up `{entity}`, then multiply by `{factor}`). For a new task, a model call picks the structurally similar template, a second fills in the placeholders as a full plan, and the executor runs it, resolving `{step_1}` from earlier observations. Adapting costs a fixed two model calls however many steps the workflow has; planning from scratch costs one call per step plus the final answer. A task with a new shape matches no template and falls back to planning.

| | Remembers | Written by | Checked by |
|---|---|---|---|
| Procedural memory (34.2) | Instructions | A staff proposal | A human, through `interrupt()` |
| Voyager skill library | Python functions | The agent | Test cases that can fail |
| Agent Workflow Memory | Tool-call templates | The agent, after a success | The success of the run it came from |

Both notebooks retrieve with a model call over a short list, which works at their size. With hundreds of skills or workflows, embed the descriptions and retrieve by similarity, as lesson 34.4 does for facts.

## Key Takeaways

- MemGPT keeps core memory and a short message window in the prompt and moves everything else to an archive the agent searches with tools. The window is a budget paid on every call.
- Archived facts come back only if the agent searches, with words that match. At a window of 6, Dana's 80 GB message ranked first for `outbound traffic` and was missed for `data usage this month`.
- Voyager and Agent Workflow Memory store what worked, as code or tool-call templates. Check the library first, store only what passed tests that can fail, and treat generated code as untrusted.

## Check yourself

<details>
<summary>1. In MemGPT-style tiered memory, what has to happen for a message evicted from the window to reach the prompt again?</summary>

The agent has to call `archival_memory_search` with words that match it, and the message returns only among the top 3 results. Core memory is always in the prompt; the archive appears only through a search the model decides to make. So recall depends on the agent asking, and on the search itself.

</details>

<details>
<summary>2. At a window of 6, Dana's turn-2 traffic message is archived by turn 6. Which lab query ranks it first, and why do some queries miss it?</summary>

`outbound traffic` finds it at rank 1, because it shares two words. `how much traffic?` misses because the keyword overlap keeps punctuation, so `traffic?` is not `traffic`, and the search returns "How do I reboot a server?" on `how`; `data usage this month` shares no word with it at all. A window of 9 would keep the message in view, at about 156 tokens per call against 117.

</details>

<details>
<summary>3. A Voyager-style agent generates a palindrome check that always returns True. What should keep it out of the skill library?</summary>

Test cases that can fail. The notebook runs every new skill, and every reuse, against tests before it counts, and this candidate is rejected on Task 4's first `False` case. Only what passes is stored.

</details>

---
*Previous: [34.4 Episodic + semantic stack and multi-hop graph memory](../04_episodic_semantic_stack_and_multi_hop_graph_memory/README.md). Next: [M34 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
