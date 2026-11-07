# Lab: M45 Fine-Tuning & Model Adaptation

## Brief

RAG or fine-tune: for one narrow task, compare the M10 RAG baseline with a small fine-tuned model on the same questions and write down which wins and why.

Solution: [solution/m45_solution.ipynb](solution/m45_solution.ipynb).

## Approach

The narrow task is refund and billing questions about Larkspur Cloud. Three systems answer the same nine questions: the eight golden questions of that task (`g01`, `g06`, `g08`, `g09`, `g14`, `g18`, `g25` and the out-of-corpus `g26`) and the off-topic probe from the M45 notebooks, *What do you think of Mars?*

- **RAG baseline.** The M10 pipeline from `src/lab_kit.py`: recursive split at 500 characters with 50 overlap, TF-IDF top 4, and an LLM prompted to answer only from the excerpts or reply *The handbook does not say.*
- **Fine-tuned model.** `google/flan-t5-small`, trained with `Seq2SeqTrainer` on the 101 pairs of `data/train.jsonl`, with 10% held out for evaluation loss. It answers from its weights alone.
- **Base model.** The same `flan-t5-small` before training, so the table shows what training changed.

Why the comparison is built this way, from the [M45 theory pages](../mandatory/theory/README.md):

- **Fine-tune for behaviour, retrieve for facts.** Lesson 45.1 shows fine-tuning is strongest at a format change and weakest at facts that change. Refund windows and fees are facts that change, so the lab ends by changing one (5 to 10 business days becomes 3 to 5) and asking both systems again: RAG after a re-index, the fine-tuned model without retraining.
- **The training text is all the model learns from.** Lesson 45.4 found the `lamini_docs` rows had no end token, so the model never learned to stop. The solution asserts that the T5 tokenizer appends its end token, and that `max_length = 64` cuts no training row, before it trains.
- **Count examples, not steps.** Lesson 45.5's run saw under 1% of one epoch. The solution prints training examples times epochs next to the step count.
- **Exact match fails on free text.** Lesson 45.6 scores 0 exact matches in 139 answers. The solution uses an LLM judge against the golden `reference_answer`, adds token F1 as a check that needs no model, and string-checks refusals. The refusal rows in `train.jsonl` are what give the fine-tuned model a chance on `g26` and the Mars probe.

What to watch: a 101-row dataset and a small model can memorise phrasings without the facts, so read the per-question table, not only the totals; and check that the judge and token F1 agree before you trust either.

## How to run

```bash
uv sync --group hf-foundations
uv run --group hf-foundations jupyter lab p13_fine_tuning/m45_fine_tuning_model_adaptation/lab/solution/m45_solution.ipynb
```

Keys: `EXPERIENTIALLABS_API_KEY` (RAG answers and the judge). The first run downloads `google/flan-t5-small` from the Hugging Face Hub; training runs on a CPU.

## Data

[data/README.md](data/README.md): the Larkspur handbook and golden set (`data/larkspur/`, an unchanged copy) and `data/train.jsonl`.

## Results

*Pending run.* The owner runs the solution and fills these tables from its last cells, with the date and the models used.

| System | Judged correct (of 8) | Mean token F1 | Declines `g26` | Declines Mars probe | Cites sources | Mean seconds per answer |
|---|---|---|---|---|---|---|
| RAG baseline | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| Base `flan-t5-small` | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |
| Fine-tuned `flan-t5-small` | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* | *pending run* |

After changing the refund window to 3 to 5 business days:

| System | Gives the new window | Gives the old window |
|---|---|---|
| RAG, re-indexed | *pending run* | *pending run* |
| Fine-tuned, not retrained | *pending run* | *pending run* |

## Verdict

*Pending run.* The verdict is written from the tables above with the rule in the solution's Verdict cell: the fine-tuned model replaces retrieval only if it matches the RAG baseline's judged-correct count, declines both unanswerable questions, and survives the fact change. [M46](../../../p14_architecture_decisions/m46_architecture_synthesis/lab/README.md) takes its RAG or fine-tune row from this verdict.

Back to the module: [README.md](../README.md)
