# M26.6 Theory: Self-consistency, tree of thoughts and LATS

*[M26 theory](../README.md) · Lesson 26.6 · Notebooks: [`06a_self_consistency.ipynb`](../../../../course/p08_agent_foundations/m26_planning_reflection_reasoning/notebooks/06a_self_consistency.ipynb), [`06b_tree_of_thoughts.ipynb`](../../../../course/p08_agent_foundations/m26_planning_reflection_reasoning/notebooks/06b_tree_of_thoughts.ipynb), [`06c_lats.ipynb`](../../../../course/p08_agent_foundations/m26_planning_reflection_reasoning/optional/06c_lats.ipynb) (optional) · [All theory pages](../../../README.md)*

## Tree of thoughts / LATS

A single chain of thought is one sample from many possible reasoning paths. The three notebooks spend extra LLM calls on more paths, each in a different place:

| Pattern | Where the extra calls go | What picks the answer | Fails when |
|---|---|---|---|
| Self-consistency (Wang et al., 2022) | N whole answers to the same prompt at temperature above 0 | A majority vote over the final answers | The error is systematic: the samples agree on the same wrong answer |
| Tree of thoughts (Yao et al., 2023) | Several proposed next steps from every state, level by level | An evaluator scores each state; the best `BEAM` survive | The evaluator prunes the state that leads to the solution |
| LATS (Zhou et al., 2024) | One leaf at a time, chosen by Monte Carlo tree search | Rewards backpropagated to the root, plus lessons from dead ends | The value model misleads selection |

Self-consistency needs short, comparable answers (a number, a label) and nothing else. Notebook 06a has both cases. On the sum of all digits from 1 to 100 the wrong answers were scattered, which a vote washes out; on three-digit numbers whose digits add up to 10, most wrong answers were the same number, 55, which a vote locks in. High agreement is a cheap confidence signal, but consistent is not the same as correct.

Tree of thoughts (ToT) spends its calls on intermediate steps instead. Notebook 06b uses the Game of 24, the benchmark from the ToT paper: combine four numbers with `+ - * /` to make 24. A state is the numbers still in play; a thought is one move. Four pieces make the search:

- **Rules in code.** Moves are applied with exact fractions, so an illegal or mis-computed proposal is dropped and the tree holds only legal states.
- **A proposer.** The LLM, at temperature 0.7, suggests up to `PROPOSALS = 8` moves per state.
- **An evaluator.** With three numbers left, an LLM at temperature 0 judges `sure`, `likely` or `impossible` (scores 3, 1, 0). With two left, code checks the six operations exactly. Where code can decide it should: while prototyping, an LLM judged `[4, 24]` as `sure` because 24 was in the list.
- **Beam search.** `expand → evaluate` in a LangGraph loop keeps the best `BEAM = 5` states per level, and a pure router stops at a solution, an empty frontier or the depth limit.

The notebook reports that in its runs single-pass CoT solved between a twentieth and a quarter of the samples, while ToT solved about half of the eight puzzles at roughly 10 to 15 LLM calls per puzzle. Every ToT solution is valid by construction, and every failure is an evaluator failure: the solving state was scored `impossible` and pruned, or never proposed.

LATS replaces the level-by-level beam with Monte Carlo tree search, one leaf per iteration:

```mermaid
flowchart LR
    S["Select a leaf<br/>by UCB1"] --> E["Expand<br/>up to K moves"]
    E --> V["Evaluate<br/>code or LLM"]
    V --> B["Backpropagate<br/>reward to the root"]
    B --> F{"Solved?"}
    F -- no --> L["Reflect on<br/>dead ends"]
    L --> S
    F -- yes --> A[/Solution/]
```

Selection walks down from the root, at each level taking the child with the best average value plus an exploration bonus:

```
UCB1(child) = child.value / child.visits + c * sqrt(ln(parent.visits) / child.visits)
```

An unvisited child scores infinity, so every child is tried once. Notebook 06c sets `c = 1.4`, `K_CANDIDATES = 4`, `MAX_ITERATIONS = 10` and rewards of 1, 0.33 and 0 for `sure`, `likely` and `impossible`. A node whose children all died gets one more expansion (`MAX_EXPANSIONS = 2`) with the latest reflections in its prompt, then is pruned for good. Each dead end becomes a one-sentence lesson that later proposals read, which is Reflexion (lesson 26.3) used inside a search.

On these eight puzzles LATS did not win: the notebook reports it solved 2 to 4 of 8, the ToT beam about 4, and LATS spent more LLM calls. Its solved runs finished in two or three iterations, because it stops at the first success. LATS was designed for problems with a larger branching factor and a better value model.

For a Larkspur support assistant most questions have one good path, and lessons 26.1 and 26.4 are the tools to reach for. Reach for these patterns when one path is not reliable enough and something can score a partial answer: a code check, a test suite, or a judge you have measured. Without that evaluator, more branches only multiply the calls.

## Key Takeaways

- Self-consistency votes over N sampled answers and needs short, comparable answers. It washes out scattered errors but locks in systematic ones, so high agreement signals confidence, not correctness.
- Tree of thoughts proposes several moves per state, scores them and keeps the best `BEAM` per level. Enforce the rules in code and let code judge whatever it can decide exactly.
- LATS picks one leaf at a time by UCB1 and learns from dead ends, yet on the Game of 24 it did not win. Use these searches only when something reliable can score a partial answer.

## Check yourself

<details>
<summary>1. When does a majority vote over sampled answers fail to fix a wrong answer?</summary>

When the error is systematic and the samples agree on the same wrong answer. On three-digit numbers whose digits add up to 10, most wrong answers were 55, which a vote locks in; on the sum of the digits from 1 to 100 the wrong answers were scattered and the vote washed them out. Consistent is not the same as correct.

</details>

<details>
<summary>2. In the Game of 24 search, an LLM evaluator judged the state with 4 and 24 left as sure. What should judge two-number states instead?</summary>

Code. With two numbers left, the notebook checks the six operations exactly, because where code can decide, it should. The LLM said `sure` only because 24 was in the list.

</details>

<details>
<summary>3. Should Larkspur's support assistant answer handbook questions with tree of thoughts or LATS?</summary>

Usually not. Most of its questions have one good path, and plan-and-execute or chain-of-verification fit them. Reach for these search patterns only when one path is not reliable enough and something can score a partial answer: a code check, a test suite or a judge you have measured. Without that, more branches only multiply the calls.

</details>

---
*Previous: [26.4 Chain-of-verification and constitutional critique](../04_chain_of_verification_and_constitutional_critique/README.md). Next: [M26 interview questions](../README.md#interview-spotlight-5-questions-you-might-get-asked).*
