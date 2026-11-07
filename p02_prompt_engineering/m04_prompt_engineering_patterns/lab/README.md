# Lab: M04 Prompt Engineering Patterns

## Brief

Prompt bake-off: write three prompts for grading whether a retrieved passage answers a question, and measure their agreement with your own labels on 30 pairs.

## Approach

The solution, [solution/m04_solution.ipynb](solution/m04_solution.ipynb), grades 30 hand-labelled question and passage pairs with three prompts: zero-shot, few-shot (one `yes` and one `no` example taken from passages outside the 30 pairs) and quote-then-decide (copy the answering sentence or write NONE, then a label). Each prompt is scored with accuracy and Cohen's kappa from `sklearn.metrics`, plus its false `yes`, false `no` and parse failures.

- **Examples teach the boundary.** Few-shot examples teach the label set, the output shape and the class boundaries, and they are paid for on every call. Cover every label and keep them balanced (lesson 4.1).
- **Hard negatives.** Each `no` passage is the best-ranked passage on the same topic that lacks the fact, the case a lenient grader passes.
- **Kappa over accuracy.** With 15 `yes` and 15 `no`, a prompt that always says `yes` scores 0.5 accuracy and 0 kappa.
- **Do not vote a weak grader.** Self-consistency amplifies the majority answer, so it makes a yes/no grader worse when one sample is right less than half the time (lesson 4.2). Measure one-sample agreement first, as this lab does.
- **Parse strictly.** A reply with no `yes` or `no` counts as a parse failure and is scored as `no`, so unreadable output is not rewarded.

## How to run

- Environment: the default `uv sync`; no extra group.
- Keys: `EXPERIENTIALLABS_API_KEY`, read from the repository's `.env` (template: `.env.example`). Docker: none.
- Execute in place: `uv run jupyter nbconvert --to notebook --execute p02_prompt_engineering/m04_prompt_engineering_patterns/lab/solution/m04_solution.ipynb --output /tmp/m04_run.ipynb`

## Data

`data/grading_pairs.jsonl` (30 labelled pairs, built from the handbook) and `data/larkspur/`. How the pairs were built and labelled: [data/README.md](data/README.md).

## Results

Not run yet; the owner runs the solution and fills this table with the run date and the model.

| Prompt | Accuracy | Cohen's kappa | False yes | False no | Parse failures |
|---|---|---|---|---|---|
| zero-shot | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| few-shot | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| quote-then-decide | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
