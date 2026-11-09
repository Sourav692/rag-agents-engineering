# M45.5 Theory: Training

*[M45 theory](../README.md) · Lesson 45.5 · Notebooks: [`05a_training_lab.ipynb`](../../notebook/05_training/05a_training_lab.ipynb), [`05b_training_lecture.ipynb`](../../../optional/notebook/05_training/05b_training_lecture.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: What the Trainer does on each update, and the arithmetic that shows a three-step run trains on under 1% of the data -->

## Trainer

> **What you'll learn**
>
> - **Explain** the loop the Hugging Face `Trainer` runs, and what gradient accumulation does to memory and batch size.
> - **Read** a `TrainingArguments` configuration setting by setting.
> - **Calculate** examples seen, share of an epoch and the learning rate of each update for a short run.
> - **Diagnose** a run that reports steps but trained on almost nothing.

Lesson 45.4 produced 1,260 tokenized training rows. A Larkspur engineer runs the notebook's training cell on rows like these, sees a loss logged at every step, and reports "fine-tuned". The run made three updates. One of them had a learning rate of zero, and the logged loss was smoothed so heavily that it could not have moved. We call that the **step-count illusion**: a run that looks like training in the log and changes almost nothing in the weights.

**The Hugging Face `Trainer` runs the training loop you would otherwise write by hand**: batch the data, run the model forward, compute the loss, run it backward, step the optimizer and the learning-rate schedule, evaluate, log and save checkpoints. `TrainingArguments` holds every setting. The notebook trains `EleutherAI/pythia-70m` (70.4 million parameters, about 0.28 GB of weights in 32-bit floats) on `lamini/lamini_docs` with these:

| Argument | Value | What it does |
|---|---|---|
| `learning_rate` | `1.0e-5` | Peak step size, reached after warmup |
| `max_steps` | `3` | Optimizer updates to run; overrides `num_train_epochs` |
| `per_device_train_batch_size` | `1` | Examples per forward pass |
| `gradient_accumulation_steps` | `4` | Forward passes summed into one update |
| `warmup_steps` | `1` | Updates spent ramping the learning rate up from 0 |
| `optim` | `"adafactor"` | An optimizer that stores less state per weight than Adam |
| `eval_steps`, `save_steps` | `120` | Evaluate and checkpoint every 120 updates |
| `logging_steps` | `1` | Log after every update |
| `load_best_model_at_end` | `True` | Reload the checkpoint with the lowest `eval_loss` when training ends |

*Table 1: The notebook's training settings.*

One optimizer step, with a batch of 1 and four accumulation steps, runs like this:

```mermaid
flowchart LR
    M["Micro-batch<br/>1 example"] --> F["Forward<br/>loss"]
    F --> B["Backward<br/>add gradients"]
    B --> Q{"4 collected?"}
    Q -- no --> M
    Q -- yes --> U["Optimizer step<br/>lr from schedule"]
    U --> Z["Zero gradients"]
```
<!-- animated: diagrams/training-step.anim.html -->

*Figure 1: One optimizer update with gradient accumulation. Four forward and backward passes feed a single step.*

**Gradient accumulation** gives the update of a batch of 4 while holding only one example in memory. After the gradients are zeroed, the next update starts again from a fresh micro-batch.

### The notebook's custom trainer

The notebook does not use the library `Trainer` directly. It imports a subclass from its `utilities.py` that adds three things:

- **An empty-input guard**: it skips a batch whose `input_ids` are empty, which is the blank row lesson 45.4 found.
- **Speed logging**: it logs iteration time, floating-point operations per second and remaining time.
- **A smoothed loss**: it logs an exponential average that gives each new step a weight of 1/100.

The third one hides the effect of a short run. With a weight of 1/100, three steps move the logged loss by a few percent of the gap at most. In a 3-step run the log barely moves from its first value. Read the raw loss when you judge a short run.

The operations figure uses the rule the library's `Trainer.floating_point_ops` implements: 6 × tokens × non-embedding parameters. The arithmetic for one update at the notebook's settings:

| Quantity | Value |
|---|---|
| Non-embedding parameters in pythia-70m | 44,670,976 |
| Tokens per example, at the 2,048 cap | 2,048 |
| Examples per update | 4 |
| 6 × 2,048 × 4 × 44,670,976 | about 2.2 trillion operations |

*Table 2: The notebook's operations estimate per update. Parameter counts are from the pythia-70m configuration, checked against the library's counting rule.*

### Version drift

On the `transformers` 5.17 this course pins, the notebook no longer runs as written. Four things changed under it:

| The notebook does | `transformers` 5.17 expects |
|---|---|
| Passes `evaluation_strategy` to `TrainingArguments` | `eval_strategy`; the old name is rejected |
| Calls `floating_point_ops` on the model | The method lives on the `Trainer` |
| Passes the parent's arguments to `__init__` by position | A new signature, so positions no longer line up |
| Defines `training_step(model, inputs)` | An extra `num_items_in_batch` argument the loop now passes |

*Table 3: Where the notebook's trainer code meets the pinned library version, checked against the installed `transformers` 5.17 source.*

The mechanism the notebook teaches is unchanged. Only the names moved, which is why the next section reasons about the run in counts rather than code.

## Steps, examples and epochs

**A step is one optimizer update, not one example.** An **epoch** is one pass over every training row. The arithmetic for the notebook's run:

| | Value |
|---|---|
| Examples per update | 1 per batch × 4 accumulated = 4 |
| Updates | `max_steps` = 3 |
| Examples seen | 12 |
| Training rows | 1,260 |
| Share of one epoch | 0.95% |

*Table 4: Examples seen by the notebook's run.*

The learning rate is not constant either. With the default linear schedule, one warmup step and 3 steps in all, the library's linear-warmup schedule gives each update its own rate:

| Update | Phase | Learning rate |
|---|---|---|
| 1 | Warmup starts at 0 | 0 |
| 2 | Peak | 1e-5 |
| 3 | Linear decay, halfway to 0 | 5e-6 |

*Table 5: The learning rate of each update in the 3-step run.*

The first of the three updates changes nothing. And because evaluation and checkpoints happen every 120 updates, this run never computes an `eval_loss`. `load_best_model_at_end` has no checkpoint to choose. We call that a **phantom checkpoint**: a setting that promises the best model and has nothing to choose from.

That is why the notebook calls its result "finetuned slightly" and then loads `lamini/lamini_docs_finetuned`, the same base model trained for two epochs: 2,520 examples against 12. A run that sees under 1% of the data, with one of its three updates at a learning rate of 0, shows the mechanics of training and almost none of its effect.

### Sizing a real Larkspur run

The fix for the step-count illusion is to plan in examples and derive the steps, in this order:

1. Decide how many epochs the data supports; a small dataset seen too many times starts to memorize.
2. Multiply by the training rows and divide by examples per update to get the number of updates.
3. Set warmup as a fraction of those updates, not a fixed count.
4. Put `eval_steps` and `save_steps` well inside the run. The held-out loss is then tracked while it trains, and the best-checkpoint setting has something to choose.

The held-out loss tells you the model fits unseen rows of the same kind. It does not yet tell you the model does the Larkspur job, which is the next lesson.

## Key Takeaways

- `Trainer` runs the loop and `TrainingArguments` holds every setting. Gradient accumulation gives the update of a larger batch while holding only one micro-batch in memory.
- A step is one optimizer update, not one example. Work out examples seen, share of an epoch and the learning rate per step before you judge a run.
- Size a real run in examples: choose the epochs, derive the updates, set warmup as a fraction of them, and put `eval_steps` inside the run. Read the raw loss, since a smoothed one barely moves on short runs.

## Check yourself

<details>
<summary>1. With a batch size of 1 and 4 gradient-accumulation steps, how does the trainer produce one optimizer update?</summary>

It runs four micro-batches of one example each forward and backward, adding their gradients. Once four are collected it steps the optimizer at the learning rate from the schedule and zeroes the gradients. The update matches a batch of 4 while only one example is held in memory.

</details>

<details>
<summary>2. In the lesson 45.5 run, what learning rates do the three updates get, and what share of an epoch does the model see?</summary>

0, 1e-5 and 5e-6, from the linear schedule with one warmup step. The first update changes nothing. Three updates of 4 examples each see 12 of the 1,260 training rows: 0.95% of one epoch.

</details>

<details>
<summary>3. Why does load_best_model_at_end have no checkpoint to choose in the lesson 45.5 run, and how should a real Larkspur run be set?</summary>

Evaluation and checkpoints happen every 120 updates and the run has 3, so it never computes an `eval_loss`. Size a real run in examples: decide the epochs the data supports, derive the number of updates, set warmup to a fraction of them, and put `eval_steps` well inside the run.

</details>

---
*Previous: [45.4 Data preparation](../04_data_preparation/README.md). Next: [45.6 Evaluation](../06_evaluation/README.md).*
