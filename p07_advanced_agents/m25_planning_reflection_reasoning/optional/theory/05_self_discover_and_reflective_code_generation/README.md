# M25.5 Theory: Self-Discover and reflective code generation

*[M25 theory](../../../mandatory/theory/README.md) · Lesson 25.5 · Notebooks: [`05a_self_discover.ipynb`](../../notebook/05a_self_discover.ipynb) (optional), [`05b_reflective_code_generation_agent.ipynb`](../../notebook/05b_reflective_code_generation_agent.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: Spend extra calls before the answer on how to reason, or after it on running what the model wrote -->
<!-- format: approved -->

## A recommendation that drops one constraint

> **What you'll learn**
>
> - **Explain** Self-Discover's four stages and why only the last one sees the specific problem.
> - **Measure** a reasoning structure against direct answers with a brute-force ground truth.
> - **Explain** how running generated code turns critique from opinion into evidence.
> - **Choose** between spending calls before an answer and spending them after it.

Larkspur's sales assistant gets the same kind of question every day: *which plan and server sizes fit this workload?* The answer depends on several constraints at once (server count, peak memory, backup needs). A customer runs five servers, and the assistant recommends Starter, which allows three. The reply reads well and is still invalid, because one constraint fell out of the reasoning.

Lessons 25.3 and 25.4 spent their extra calls after a draft existed, on critique and verification. This lesson spends them in two other places. **Before** the answer, the model works out how to reason about this kind of problem. **After** the answer, a critic runs the output instead of reading it.

## Self-Discover: plan the reasoning first

**Self-Discover** (Zhou et al., 2024) has the model compose a reasoning plan for the *type* of task before it attempts any instance. It runs in four stages:

```mermaid
flowchart LR
    S["SELECT<br/>modules from<br/>a catalog"] --> A["ADAPT<br/>reword each<br/>for the task type"]
    A --> I["IMPLEMENT<br/>an ordered<br/>reasoning plan"]
    I --> V["SOLVE<br/>one instance<br/>with the plan"]
```

*Figure 1: Self-Discover. The first three stages see only the task type, and SOLVE is the only stage that sees the instance.*

1. **SELECT** picks the relevant entries from a fixed catalog of generic reasoning modules. The notebook's catalog has 10, among them Decomposition, Constraint Propagation, Case Analysis and Verification.
2. **ADAPT** rewords each selected module as an instruction for this type of task.
3. **IMPLEMENT** orders the instructions into a structured plan with numbered steps: the discovered structure, still not an answer.
4. **SOLVE** gives the model the structure and one instance, and it returns a worked trace and a typed answer.

Stages 1 to 3 never see an instance. Their output is reusable across every instance of the type, and you can read it before any effort goes into a specific case. The catalog is fixed. The model only selects and rewords its entries, which keeps the structure made of named, inspectable moves instead of an opaque chain of thought.

### A puzzle with a known answer

The notebook tests the pattern on a scheduling puzzle. Priya, Quinn and Rae each take one interview slot, 9:00 AM, 11:00 AM or 2:00 PM, under four clues:

1. Priya is not at 9:00.
2. Quinn is earlier than Rae.
3. If Priya is at 2:00, then Quinn is at 9:00.
4. Rae is not at 11:00.

Code brute-forces all six assignments and keeps the ones that satisfy every clue. Every model answer can then be checked against a ground truth nobody typed in by hand:

| Priya | Quinn | Rae | Clues broken |
|---|---|---|---|
| 9:00 | 11:00 | 2:00 | 1 |
| 9:00 | 2:00 | 11:00 | 1, 2, 4 |
| **11:00** | **9:00** | **2:00** | **none** |
| 11:00 | 2:00 | 9:00 | 2 |
| 2:00 | 9:00 | 11:00 | 4 |
| 2:00 | 11:00 | 9:00 | 2, 3 |

*Table 1: The six assignments and the clues each one breaks, from running the notebook's brute-force check. Exactly one satisfies all four.*

Both approaches answer with the same typed assignment, and both sample at temperature 0.7. The only difference is the structure:

<div class="learning-widget evidence-switcher" data-comparison id="puzzle-switcher">
<p class="widget-intro">Choose how the model answers the interview-slot puzzle, and compare what it reads and what the recorded runs found.</p>
<div class="mode-controls" hidden role="group" aria-label="Direct answers or Self-Discover"><button type="button" data-mode="direct" aria-pressed="false" aria-controls="puzzle-direct">Direct answer</button><button type="button" data-mode="discover" aria-pressed="false" aria-controls="puzzle-discover">Self-Discover</button></div>
<section id="puzzle-direct" class="mode-panel" data-announcement="Direct answer selected. Rarely right in the recorded runs."><h4>Direct answer: final assignment only</h4><dl><dt>Reads</dt><dd>the puzzle and the instruction to give the final answer only</dd><dt>Calls</dt><dd>one per sample, five samples</dd><dt>Recorded result</dt><dd>between 0 of 5 and 2 of 6 right; the usual wrong answer puts Rae at 11:00, which clue 4 forbids</dd></dl></section>
<section id="puzzle-discover" class="mode-panel" data-announcement="Self-Discover selected. Right far more often in the recorded runs."><h4>Self-Discover: one structure, reused</h4><dl><dt>Reads</dt><dd>the discovered structure plus the puzzle, with the instruction to skip no step, verification included</dd><dt>Calls</dt><dd>three discovery calls once, then one SOLVE call per sample, three samples</dd><dt>Recorded result</dt><dd>3 of 3, 4 of 4 and 2 of 3 right; better, and still not always right</dd></dl></section>
<p class="switch-status" aria-live="polite"></p>
</div>

The direct answers failed in a recognisable way. Rae at 11:00 breaks clue 4, and in the fifth row of Table 1 (Priya at 2:00, Quinn at 9:00) it is the only clue broken. We call this the **dropped constraint**: an answer that satisfies most clues and quietly ignores one. The structure added no knowledge. It made the steps that catch a dropped constraint (enumerate the cases, check every clue against the final assignment) mandatory instead of optional.

The gain has a ceiling. On a harder five-person version of the puzzle, `gpt-4o-mini` failed with and without the structure. A checklist helps a model apply reasoning it can already do, and adds nothing beyond its reach.

### What the structure costs

The three discovery stages run once per task type, and SOLVE runs once per instance:

| Instances of the type | Direct answers | Self-Discover |
|---|---|---|
| 1 | 1 call | 3 + 1 = 4 calls |
| 3 | 3 calls | 3 + 3 = 6 calls |
| 100 | 100 calls | 3 + 100 = 103 calls |

*Table 2: LLM calls, with the discovery cost shared across instances.*

The structure pays off on a task type you see often, where its fixed cost spreads thin. For a one-off question it quadruples the calls. Self-Discover improves the reasoning before an answer exists. The second pattern checks an answer by running it.

## Execution as the critic

Lesson 25.3's optional notebook showed a critic that reads code and trusts its own guess about bugs. The reflective code-generation agent replaces that critic with the Python interpreter. **Execution as the critic** means running the generated code and treating any exception as the feedback for the next attempt. An exception is evidence, where a reviewer's "this looks fine" is an opinion.

```mermaid
flowchart TD
    G["Generate<br/>prefix, imports, code"] --> I{"Imports<br/>run?"}
    I -- no --> F["Feedback:<br/>the import error"]
    I -- yes --> C{"Code<br/>runs?"}
    C -- no --> F2["Feedback:<br/>the exception,<br/>reflect and retry"]
    C -- yes --> E[/Done/]
    F --> K{"3 attempts<br/>used?"}
    F2 --> K
    K -- no --> G
    K -- yes --> X[/Stop, still failing/]
```

*Figure 2: Generate, check, retry. The router ends on success or at the attempt cap.*

The generator returns a structured object with three fields: a **prefix** describing the approach, the **imports** and the **code**. Splitting them lets the checker run the imports first, and a missing library then produces a precise message. The code then runs with the imports. An exception goes back to the generator as a user message that names the error, asks the model to say what went wrong and asks for the full solution again. A pure router stops when the code runs or after `MAX_ATTEMPTS = 3` generations.

### The repair path, traced

Models rarely fail on demand, so the notebook plants the failure. Its first generator call returns code that uses the `statistics` module without importing it; later calls go to the real model. We replayed the graph without a model, with a stub second attempt that adds the import:

<div class="walkthrough learning-widget" data-stepper id="repair-walkthrough">
<p class="widget-intro">Step through the repair run, from the planted bug to the finish.</p>
<div class="step-controls" hidden role="group" aria-label="Steps of the repair run"><button type="button" data-step="0" aria-pressed="false" aria-controls="repair-step-0">1. Generate</button><button type="button" data-step="1" aria-pressed="false" aria-controls="repair-step-1">2. Check</button><button type="button" data-step="2" aria-pressed="false" aria-controls="repair-step-2">3. Feedback</button><button type="button" data-step="3" aria-pressed="false" aria-controls="repair-step-3">4. Finish</button></div>
<div class="step-panels"><section id="repair-step-0" class="step-panel" aria-labelledby="repair-heading-0"><h4 id="repair-heading-0">1. Attempt 1 is generated</h4><dl><dt>Imports</dt><dd>empty</dd><dt>Code</dt><dd>prints the mean and median of eight numbers through <code>statistics</code></dd><dt>State</dt><dd>attempts 1</dd></dl></section><section id="repair-step-1" class="step-panel" aria-labelledby="repair-heading-1"><h4 id="repair-heading-1">2. The check runs it</h4><dl><dt>Imports</dt><dd>run cleanly, because there are none</dd><dt>Code</dt><dd>raises <code>NameError</code>: <code>statistics</code> is not defined</dd><dt>State</dt><dd>error flag yes</dd></dl></section><section id="repair-step-2" class="step-panel" aria-labelledby="repair-heading-2"><h4 id="repair-heading-2">3. The error becomes feedback</h4><dl><dt>Message</dt><dd>the exception name and text, a request to reflect on it and a request for the full solution</dd><dt>Router</dt><dd>1 attempt of 3 used: back to the generator</dd></dl></section><section id="repair-step-3" class="step-panel" aria-labelledby="repair-heading-3"><h4 id="repair-heading-3">4. Attempt 2 runs</h4><dl><dt>Imports</dt><dd>now import <code>statistics</code></dd><dt>Check</dt><dd>no exception, one line of program output</dd><dt>Result</dt><dd>2 attempts, error flag no, the router ends the run</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

The notebook proves all three paths, two of them without asking the model to fail:

| Run | Generator | What happens |
|---|---|---|
| Real task: a pandas pivot table | The model | Usually runs on the first attempt, the happy path |
| Repair path | The planted missing import, then the real model | The check raises a `NameError`, the model sees the real error and repairs the import |
| The cap | A stub that always returns code raising an error, no LLM calls | Stops after exactly 3 attempts and reports the code as still failing |

*Table 3: The three paths the notebook runs. The stubs make the repair and the cap repeatable; our replay of the cap also ended at 3 attempts with the error flag set.*

### What execution cannot see

Two failure modes limit the pattern. The first is the **runs-but-wrong** answer: code that executes cleanly and computes the wrong result, which this critic cannot see. "It runs" is a weak test. Add assertions or hidden tests, as lesson 25.3's ten-test parser check does, when correctness matters. The second is the **unfixable environment**: a task that needs an API key, a network call or a model download fails for reasons no rewrite of the code can repair, and the loop hits its cap.

> **Pitfall: running model-written code.** The notebook executes the generated code directly on the machine. That is acceptable for a small, self-contained task. Anything untrusted belongs in a sandbox, such as the hosted code interpreter from M22.

## Before the answer or after it

The module now has extra calls in four places. Each fixes a different failure:

| Where the calls go | Pattern | Fixes | Leaves |
|---|---|---|---|
| Before the answer, on how to reason | Self-Discover | Dropped constraints within the model's reach | Reasoning beyond its reach |
| After, on opinion | Reflection, lesson 25.3 | Style and structure | Facts and bugs |
| After, on independent questions | Chain-of-verification, lesson 25.4 | Unsupported claims | Missing claims |
| After, on running the output | Execution critic | Crashes and import errors | Code that runs and is wrong |

*Table 4: Four places to spend extra calls.*

The decision rule follows from the last column. Spend calls before the answer when the failure is a skipped step on a task type you see often. Spend them on execution when the output is code and you can also check its result.

## In practice: fitting a Larkspur plan

An illustrative application to the sales question, using the handbook's limits:

1. **Discover once.** Run SELECT, ADAPT and IMPLEMENT on the task type "fit a workload to a Larkspur plan and server sizes". A good structure starts from the hardest constraint: the server count fixes the plan (Starter up to 3, Business up to 50, Enterprise unlimited), then each server's peak memory picks its size (Small 4 GB, Medium 16 GB, Large 64 GB), then every constraint is checked against the final answer.
2. **Solve per question.** A customer with five servers, one of them peaking at 40 GB, gets Business and a Large server for that workload, because Medium has 16 GB. The structure's final check catches a Starter answer.
3. **Verify in code.** The plan limits and sizes fit in a table, and a short function can check every answer the way the brute force checked the puzzle.
4. **Run what is written.** When the assistant writes a sizing script for the customer, an execution critic runs it with test inputs and assertions before it is shared.

## Limits of this evidence

- **Recorded runs, not reruns.** The puzzle accuracies come from the notebook's own recorded runs with `gpt-4o-mini`; we did not call a model for this page. Sampled answers vary from run to run.
- **One puzzle.** Table 1 was recomputed from the notebook's clue check. One small puzzle shows the dropped constraint; it does not measure how often it happens elsewhere.
- **A stub repair.** Our trace of the repair path used a stub for attempt 2. In the notebook the real model writes that attempt, and it may need more than one.

## References

1. Zhou et al., [Self-Discover: Large Language Models Self-Compose Reasoning Structures](https://arxiv.org/abs/2402.03620), 2024.
2. LangChain, [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview).
3. Python Software Foundation, [Built-in function exec](https://docs.python.org/3/library/functions.html#exec).

## Key Takeaways

- Self-Discover composes a reasoning plan from a fixed catalog for a task type, once, and reuses it for every instance. It makes checks like case analysis and final verification mandatory, and helps only within the model's reach.
- Measure a reasoning strategy against a ground truth computed in code, over several samples. The puzzle's direct answers dropped a constraint, and the structured answers mostly did not.
- Running generated code makes the critique evidence. Cap the retries, prove the repair and the cap with stubs, and add tests, because code that runs can still be wrong.

## Check yourself

<details>
<summary>1. Why do the SELECT, ADAPT and IMPLEMENT stages never see the specific puzzle?</summary>

They work out how to reason about the task type, so their output is a reusable structure for every instance of that type and can be inspected before any instance is solved. Only SOLVE sees the instance, and it follows the structure step by step.

</details>

<details>
<summary>2. The direct answers to the interview-slot puzzle usually put Rae at 11:00 AM. What went wrong, and what did the discovered structure change?</summary>

That assignment breaks clue 4, which says Rae is not at 11:00, so the model dropped one constraint. The structure did not add knowledge. It made enumerating the cases and checking every clue against the final assignment mandatory, and the structured answers were right far more often.

</details>

<details>
<summary>3. A code-generation agent with an execution critic reports success, yet the function returns wrong totals. How did that pass, and what should be added?</summary>

The critic only checks that the imports and the code run without an exception, and wrong output raises none. Add assertions or hidden tests with expected values, so the check measures correctness as well as whether the code runs.

</details>

---
*Previous: [25.4 Chain-of-verification and constitutional critique](../../../mandatory/theory/04_chain_of_verification_and_constitutional_critique/README.md). Next: [25.6 Self-consistency, tree of thoughts and LATS](../../../mandatory/theory/06_self_consistency_tree_of_thoughts_and_lats/README.md).*
