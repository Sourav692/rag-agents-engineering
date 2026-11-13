# M45.7 Theory: Fine-tuning Llama 2 with AutoTrain

*[M45 theory](../../../mandatory/theory/README.md) · Lesson 45.7 · Notebooks: [`07a_3_ways_fine_tuning_llama_2_with_autotrain.ipynb`](../../notebook/07_llama2_autotrain/07a_3_ways_fine_tuning_llama_2_with_autotrain.ipynb) (optional) · [All theory pages](../../../../../THEORY.md)*
<!-- subtitle: LoRA and 4-bit loading bring a 7-billion-parameter fine-tune onto one GPU, and the notebook's AutoTrain command needs new flag names and a sane learning rate -->
<!-- format: approved -->

## Start with a model too big to train

> **What you'll learn**
>
> - **Explain** how LoRA trains a small low-rank update beside each frozen weight matrix.
> - **Calculate** LoRA's trainable parameters for one layer and for a whole Llama 2 7B model.
> - **Explain** what 4-bit loading stores, and why LoRA plus 4-bit loading (QLoRA) fits one GPU.
> - **Diagnose** the notebook's AutoTrain command: outdated flags and a learning rate far too high.

Lessons 45.3 to 45.6 update every weight of a 70-million-parameter model. The Larkspur team now wants the same house style on a model large enough to serve customers, with one 24 GB GPU. Llama 2 7B has 6,738,415,616 parameters: 13.5 GB in 16-bit floats before any gradients or optimiser state, so a full fine-tune does not fit. The notebook fine-tunes it with two settings that change what is stored and what is trained: parameter-efficient fine-tuning and 4-bit loading.

## LoRA and 4-bit loading

**LoRA (low-rank adaptation, the PEFT method used here) freezes every original weight matrix `W` and trains two small matrices beside it, `A` and `B`, whose product is added to the layer's output.** With rank `r`, a layer of shape `d_out × d_in` gains `r × (d_in + d_out)` trainable parameters:

```mermaid
flowchart LR
    X[/"input x"/] --> W["W, frozen<br/>4096 × 4096"]
    X --> A["A, trained<br/>16 × 4096"]
    A --> B["B, trained<br/>4096 × 16"]
    W --> S(("sum"))
    B --> S
    S --> Y[/"output"/]
```

*Figure 1: A LoRA layer. The input goes through the frozen weight and through the trained low-rank pair, and the two results are summed.*

The intuition: the change fine-tuning makes to a layer is assumed to need far fewer dimensions than the layer itself. Rank 16 says "the update can be described by 16 directions", and the two thin matrices hold exactly that much.

For the attention query projection of Llama 2 7B at rank 16, the arithmetic is small enough to do by hand:

| Quantity | Value |
|---|---|
| Frozen weights, 4,096 × 4,096 | 16,777,216 |
| Trained, 16 × (4,096 + 4,096) | 131,072 |
| Trained as a share of the layer | 0.78% |

*Table 1: LoRA at rank 16 on one 4,096 by 4,096 projection.*

Across the model, with the settings AutoTrain uses by default (rank 16, every linear layer):

| Setup | Trainable parameters | Share of the model |
|---|---|---|
| Full fine-tuning | 6,738,415,616 | 100% |
| LoRA, rank 16, every linear layer | 39,976,960 | 0.59% |
| LoRA, rank 16, query and value projections only | 8,388,608 | 0.12% |

*Table 2: Trainable parameters for Llama 2 7B. The LoRA rows are `r × (d_in + d_out)` summed over the targeted layers of the 32-layer model; `peft` 0.20 gives the same counts on a weightless copy of the model.*

**4-bit loading** stores the frozen weights in 4 bits instead of 16 while the LoRA matrices train in higher precision. LoRA on top of 4-bit weights is **QLoRA**, one of the "3 ways" the notebook's title refers to. The two designs store and train different things:

```mermaid
flowchart LR
    D[/"Larkspur support text"/] --> M["All 6.74B weights<br/>16-bit, trained"]
    M --> G["Gradients and optimiser state<br/>for every weight"]
    G --> O[("Saved: full model<br/>13.5 GB")]
```

*Figure 2: Full fine-tuning. Every weight is trained, and every weight carries gradients and optimiser state.*

```mermaid
flowchart LR
    D[/"Larkspur support text"/] --> Q["Base weights<br/>4-bit, frozen"]
    Q --> L["LoRA pairs, rank 16<br/>trained in 16-bit"]
    L --> G["Gradients and optimiser state<br/>for 40M parameters"]
    G --> O[("Saved: adapter<br/>about 80 MB")]
```

*Figure 3: QLoRA. The base model is frozen in 4 bits; only the low-rank pairs train and are saved.*

<div class="learning-widget evidence-switcher" data-comparison id="design-switcher">
<p class="widget-intro">The same Llama 2 7B fine-tune on Larkspur support text, set up both ways. Pick a design to see what the GPU holds and what you ship.</p>
<div class="mode-controls" hidden role="group" aria-label="Fine-tuning design">
<button type="button" data-mode="full" aria-pressed="false" aria-controls="design-full">Full fine-tune, 16-bit</button>
<button type="button" data-mode="qlora" aria-pressed="false" aria-controls="design-qlora">QLoRA, rank 16</button>
</div>
<section id="design-full" class="mode-panel" data-announcement="Full fine-tune selected. 13.5 GB of weights, all trained."><h4>Full fine-tune, 16-bit</h4><dl><dt>Base weights in memory</dt><dd>13.5 GB, all trained</dd><dt>Parameters with gradients and optimiser state</dt><dd>6,738,415,616</dd><dt>Fits one 24 GB GPU</dt><dd>No: the weights alone take more than half of it before any gradient</dd><dt>Saved artefact</dt><dd>A full 13.5 GB model per task</dd></dl></section>
<section id="design-qlora" class="mode-panel" data-announcement="QLoRA selected. About 4 GB of frozen weights, 40 million trained."><h4>QLoRA, rank 16, every linear layer</h4><dl><dt>Base weights in memory</dt><dd>About 4.2 GB, frozen</dd><dt>Parameters with gradients and optimiser state</dt><dd>39,976,960</dd><dt>Fits one 24 GB GPU</dt><dd>Yes, with room for activations</dd><dt>Saved artefact</dt><dd>An adapter of about 80 MB in 16-bit floats, loaded onto the base model</dd></dl></section>
<p class="switch-status" aria-live="polite"></p>
</div>

| | Full fine-tune, 16-bit | QLoRA, rank 16 |
|---|---|---|
| Base weights in memory | 13.5 GB, all trained | about 4.2 GB, frozen |
| Parameters with gradients and optimiser state | 6,738,415,616 | 39,976,960 |
| Saved artefact | A full 13.5 GB model | An adapter of about 80 MB in 16-bit floats |

*Table 3: Full fine-tuning against QLoRA for Llama 2 7B. Gradients and optimiser state exist only for the trained parameters, which is what brings the fine-tune within reach of one GPU.*

The 4.2 GB is an estimate. Four bits for every weight would be 3.4 GB, but the input embedding and the output layer usually stay in 16-bit (0.52 GB together), and with AutoTrain's 4-bit settings (no double quantisation) the per-block scaling constants add about 0.4 GB more.

The adapter is saved on its own. You can merge it into the base model for serving, or keep one base model and load a different adapter per task, for instance a Larkspur support adapter and a separate one for an internal tool. Pick full fine-tuning only when you have the memory and need to change the whole model; for a style and refusal job like Larkspur's, QLoRA is the default.

> **Pitfall: the oversized learning rate.** LoRA trains few parameters, but they still need a small step size; AutoTrain's default is 3e-5. The notebook's command sets a value thousands of times larger, which is its second problem.

## The AutoTrain command today

The notebook's AutoTrain cell (it appears twice, once on one line and once split over lines) fine-tunes a sharded 16-bit copy of Llama 2 7B on `timdettmers/openassistant-guanaco`, a dataset whose `text` column holds each whole conversation (the text-only form from lesson 45.2), with supervised fine-tuning, and pushes the result to the Hugging Face Hub. Its settings, flag by flag:

| Setting | The notebook's flag and value | Name in `autotrain-advanced` 0.8.36 |
|---|---|---|
| Train LoRA adapters | `--use_peft` | `--peft` |
| 4-bit base weights | `--use_int4` | `--quantization int4` (the default) |
| Learning rate | `--learning_rate 0.4` | `--lr` (default 3e-5) |
| Batch size | `--train_batch_size 3` | `--batch-size` (default 2) |
| Epochs | `--num_train_epochs 2` | `--epochs` |
| Text column | `--text_column text` | unchanged |
| Context length | `--model_max_length 1048`, `--block_size 1048` | unchanged (underscore and hyphen forms both accepted) |
| Hub destination | `--push_to_hub --repo_id …` | `--push-to-hub` still accepted; `--repo_id` is gone, use `--username` |

*Table 4: The notebook's AutoTrain flags against the parameter names of `autotrain-advanced` 0.8.36, checked in that release's source.*

Two problems follow from the table:

- **Flag drift.** In 0.8.36 the `llm` command builds its arguments from the fields of its parameter model, and parses them strictly. The old names `--use_peft`, `--use_int4`, `--learning_rate`, `--train_batch_size`, `--num_train_epochs` and `--repo_id` stop it with an error before training starts.
- **A runaway learning rate.** `0.4` is more than 13,000 times AutoTrain's default of `3e-5`, and 40,000 times lesson 45.5's `1e-5`. Keep the default unless a measured run says otherwise.

With the names fixed and the learning rate left at its default, the command runs this pipeline:

<div class="walkthrough learning-widget" data-stepper id="autotrain-walkthrough">
<p class="widget-intro">What the corrected command does, stage by stage, with the defaults read from <code>autotrain-advanced</code> 0.8.36. No GPU run was made here.</p>
<div class="step-controls" hidden role="group" aria-label="AutoTrain stages"><button type="button" data-step="0" aria-pressed="false" aria-controls="at-step-0">1. Parse</button><button type="button" data-step="1" aria-pressed="false" aria-controls="at-step-1">2. Load</button><button type="button" data-step="2" aria-pressed="false" aria-controls="at-step-2">3. Attach LoRA</button><button type="button" data-step="3" aria-pressed="false" aria-controls="at-step-3">4. Prepare text</button><button type="button" data-step="4" aria-pressed="false" aria-controls="at-step-4">5. Train and save</button></div>
<div class="step-panels"><section id="at-step-0" class="step-panel" aria-labelledby="at-heading-0"><h4 id="at-heading-0">1. Parse the flags</h4><dl><dt>Input</dt><dd><code>autotrain llm --train --peft --trainer sft</code> and the rest</dd><dt>Check</dt><dd>Every flag must name a field of the parameter model</dd><dt>Old flags</dt><dd>Rejected here, before any download</dd></dl></section><section id="at-step-1" class="step-panel" aria-labelledby="at-heading-1"><h4 id="at-heading-1">2. Load the base model in 4 bits</h4><dl><dt>Model</dt><dd>The sharded 16-bit Llama 2 7B copy</dd><dt>Quantisation</dt><dd><code>int4</code> by default</dd><dt>Memory</dt><dd>About 4.2 GB of frozen weights</dd></dl></section><section id="at-step-2" class="step-panel" aria-labelledby="at-heading-2"><h4 id="at-heading-2">3. Attach LoRA pairs</h4><dl><dt>Rank</dt><dd>16</dd><dt>Targets</dt><dd><code>all-linear</code>: every linear layer except the output layer</dd><dt>Trainable</dt><dd>39,976,960 parameters, 0.59% of the model</dd></dl></section><section id="at-step-3" class="step-panel" aria-labelledby="at-heading-3"><h4 id="at-heading-3">4. Prepare the text</h4><dl><dt>Column</dt><dd><code>text</code>, one whole conversation per row</dd><dt>End token</dt><dd>Added by the SFT trainer to any row that lacks one</dd><dt>Packing</dt><dd>On: rows are packed into fixed-length blocks</dd></dl></section><section id="at-step-4" class="step-panel" aria-labelledby="at-heading-4"><h4 id="at-heading-4">5. Train and save the adapter</h4><dl><dt>Schedule</dt><dd>Learning rate 3e-5, 10% warmup, 4 accumulation steps, 2 epochs</dd><dt>Output</dt><dd>An adapter of about 80 MB</dd><dt>Hub</dt><dd>Pushed under <code>--username</code> when <code>--push-to-hub</code> is set</dd></dl></section></div><div class="step-footer" hidden><button type="button" data-walk="previous">Previous</button><p class="step-status" aria-live="polite"></p><button type="button" data-walk="next">Next step</button></div></div>

AutoTrain's other defaults are worth reading too:

| Default in 0.8.36 | Value | Why it matters here |
|---|---|---|
| Gradient accumulation | 4 steps | The same accumulation as lesson 45.5 |
| Warmup | 10% of the run | Warmup as a fraction, the rule lesson 45.5 recommends |
| `model_max_length` | 2,048 tokens | The cap lesson 45.4 measured against |
| Append end token | On | The step lessons 45.4 and 45.6 show the M45 data missing |

*Table 5: AutoTrain defaults that line up with earlier lessons.*

The last row is the one to notice, with a qualification. AutoTrain's own `add_eos_token` setting applies to its default trainer. The notebook picks `--trainer sft`, which hands the data to `trl`'s `SFTTrainer`, and that trainer appends the end token itself to any text that lacks one. Either way the end token is there, which is the guard against the runaway answer from lesson 45.6.

The notebook's other two cells sketch the other two of the "3 ways": one through Lamini's hosted model runner and one through `trl`'s `SFTTrainer`. Both use names the notebook never defines (the base model, the PEFT configuration and the training arguments, among others), and they do not run as written. The `SFTTrainer` cell also passes `dataset_text_field`, `max_seq_length` and `tokenizer` directly. `trl` 1.16 takes the first two as `dataset_text_field` and `max_length` on an `SFTConfig`, and the tokeniser as `processing_class`. Read both cells as outlines of the same pipeline: a base model, LoRA settings, training arguments and a text column.

## Limits of this evidence

- No model was trained or loaded with weights. Parameter counts come from `peft` 0.20.0 on a weightless Llama 2 7B configuration; memory figures are arithmetic, and the 4.2 GB estimate assumes 16-bit embedding and output layers and AutoTrain's `nf4` setting without double quantisation.
- Flag names, defaults and the end-token handling were read from the `autotrain-advanced` 0.8.36 and `trl` 1.16.0 sources; neither command was run end to end.
- Whether a learning rate of 0.4 diverges at once or after a few steps was not tested. The page relies on the gap to the default.

## References

- Hu et al. (2021), [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685).
- Dettmers et al. (2023), [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314).
- Touvron et al. (2023), [Llama 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/abs/2307.09288).
- Hugging Face: [PEFT LoRA guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora), [bitsandbytes quantisation](https://huggingface.co/docs/transformers/main/en/quantization/bitsandbytes), [TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer) and [AutoTrain Advanced](https://github.com/huggingface/autotrain-advanced).
- Dataset: [`timdettmers/openassistant-guanaco`](https://huggingface.co/datasets/timdettmers/openassistant-guanaco).

## Key Takeaways

- LoRA freezes the original weights and trains small low-rank matrices beside them, adding `r × (d_in + d_out)` parameters per layer. At rank 16 on every linear layer of Llama 2 7B, 0.59% of the model trains.
- 4-bit loading cuts the frozen weights from 13.5 GB to about 4.2 GB. Combined with LoRA it is QLoRA, and the saved adapter is about 80 MB.
- Check CLI flag names against the installed AutoTrain version, and keep its default learning rate of `3e-5` unless a measured run says otherwise.

## Check yourself

<details>
<summary>1. Why does LoRA with 4-bit loading bring a 7B fine-tune within reach of one GPU?</summary>

LoRA freezes every original weight matrix and trains small `A` and `B` matrices beside it, so at rank 16 on every linear layer only 39,976,960 parameters (0.59%) train, and gradients and optimiser state exist only for those. 4-bit loading stores the frozen weights in about 4.2 GB instead of 13.5 GB in 16-bit floats. Together this is QLoRA.

</details>

<details>
<summary>2. How many trainable parameters does rank-16 LoRA add to a 4096 by 4096 query projection, and what share of the layer is that?</summary>

`r × (d_in + d_out)` = 16 × (4,096 + 4,096) = 131,072 trainable parameters, beside 16,777,216 frozen ones: 0.78%.

</details>

<details>
<summary>3. You run the notebook's AutoTrain command on autotrain-advanced 0.8.36 and it stops with an error. Why, and what else would you change?</summary>

Flag drift: its flag names are from an older AutoTrain, and the CLI parses arguments strictly. Use `--peft`, `--quantization int4`, `--lr`, `--batch-size`, `--epochs`, and `--username` with `--push-to-hub`. Also drop the learning rate of `0.4`, which is more than 13,000 times the default `3e-5`; keep the default unless a measured run says otherwise.

</details>

---
*Previous: [45.6 Evaluation](../../../mandatory/theory/06_evaluation/README.md). Next: [M45 interview questions](../../../mandatory/theory/README.md#interview-spotlight-5-questions-you-might-get-asked).*
