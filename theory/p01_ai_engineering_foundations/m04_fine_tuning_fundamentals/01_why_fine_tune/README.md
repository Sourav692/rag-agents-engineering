# M04.1 Theory: Why fine-tune

*[M04 theory](../README.md) · Lesson 4.1 · Notebooks: [`01a_why_finetuning_lab.ipynb`](../../../../course/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/notebooks/01_why_finetune/01a_why_finetuning_lab.ipynb), [`01b_why_finetuning_lecture.ipynb`](../../../../course/p01_ai_engineering_foundations/m04_fine_tuning_fundamentals/optional/01_why_finetune/01b_why_finetuning_lecture.ipynb) (optional) · [All theory pages](../../../README.md)*

## When to fine-tune

Fine-tuning updates the model’s weights with your examples. Prompting changes only the input, and RAG (M11) changes only what the input contains. Each fixes a different gap:

| | Prompting | RAG | Fine-tuning |
|---|---|---|---|
| What changes | The instructions and examples in each call | The evidence pasted into each call | The weights |
| Good for | Format and tone you can describe in a few lines | Facts that change, private documents, citations | Behaviour too long or subtle to describe: a house style, a narrow task, consistent refusals |
| Cost of a change | Edit the prompt | Re-index a document | Rebuild the dataset and retrain |
| Per-call cost | Grows with every instruction and example | Retrieval plus a few chunks | Lowest: the behaviour is in the weights |
| Main risk | Long prompts, drift between calls | Retrieval misses the evidence | Stale facts, lost general ability, no citations |

For the Larkspur support assistant the split is clear. *How long does a refund take?* has an answer that the policy team will change, so it stays in the index. Leading every answer with *Yes* or *No* and declining *What do you think of Mars?* is behaviour, and a fine-tune can carry it on a smaller, cheaper model. Most production systems that fine-tune also retrieve.

```mermaid
flowchart TD
    A{"Does a clear prompt<br/>with examples work?"} -- yes --> P["Prompt it<br/>M05"]
    A -- no --> B{"Is the gap a fact<br/>that changes?"}
    B -- yes --> R["Retrieve it<br/>M11"]
    B -- no --> C{"Is it behaviour you<br/>can show in examples?"}
    C -- yes --> F["Fine-tune<br/>this module"]
    C -- no --> D["Define the task<br/>before training"]
```

If you cannot write a few hundred examples of the behaviour you want, you cannot fine-tune for it, and you cannot evaluate it either.

## Base and chat models

The lesson 4.1 notebook sends the same prompts to `meta-llama/Llama-2-7b-hf`, a base model, and `meta-llama/Llama-2-7b-chat-hf`, the same model after instruction tuning and preference training. The outputs it prints are recorded in the notebook’s `llama.py`:

| Prompt | Base model | Chat model |
|---|---|---|
| Tell me how to train my dog to sit | “Tell me how to train my dog to stay. Tell me how to teach my dog to come. …” | “on command. Training your dog to sit is a basic obedience command …” followed by numbered steps |
| `[INST]`Tell me how to train my dog to sit`[/INST]` | Echoes the prompt unchanged | The numbered steps, without the “on command” fragment |
| What do you think of Mars? | “I think it’s a great planet. I think it’s a good planet. …” for 30 lines | A paragraph about Mars |

The base model does what pre-training taught it: continue the text with something that looks like more of the same, here a list of similar questions. The chat model treats the text as a request. The `[INST]` row shows the second lesson: the chat model was trained with that wrapper, and with it the answer starts cleanly; without it, the model first completes the sentence (“on command.”). A fine-tuned model expects the format it was trained on, which lesson 4.3 comes back to.

The weights changed and the architecture did not. Everything that separates the two columns came from the training data, which is why the rest of this module is about the data.

## Key Takeaways

- Prompting changes the instructions, RAG changes the evidence and fine-tuning changes the weights. Keep facts that change in the index, and fine-tune for behaviour too long or subtle to describe.
- Try a clear prompt with examples first. Fine-tune only when you can write a few hundred examples of the behaviour, since you need them to train and to evaluate.
- A base model continues text and a chat model answers requests, with the same architecture. The difference comes from training data, and a fine-tuned model expects the format it was trained on.

## Check yourself

<details>
<summary>1. Why does the refund-time answer stay in the Larkspur index while opening every answer with Yes or No can go into a fine-tune?</summary>

The refund time is a fact the policy team will change: RAG picks up a change with a re-index, while a fine-tuned model would need a rebuilt dataset and a retrain, and risks stale facts. Leading with Yes or No, and declining off-topic questions, is behaviour, which a fine-tune can carry in the weights on a smaller, cheaper model.

</details>

<details>
<summary>2. You send Tell me how to train my dog to sit, without any wrapper, to the Llama 2 base and chat models. What does each return, and why?</summary>

The base model continues with similar questions ("Tell me how to train my dog to stay. ..."), because pre-training taught it to continue text. The chat model treats it as a request but first finishes the sentence ("on command."), because it was trained with the `[INST]` wrapper; with the wrapper its answer starts cleanly.

</details>

<details>
<summary>3. A team wants to fine-tune for a behaviour but cannot write a few hundred examples of it. What should they do?</summary>

Not fine-tune: without the examples they can neither train for the behaviour nor evaluate it. The decision chain says to prompt it if a clear prompt with examples works (M05), retrieve it if the gap is a fact that changes (M11), and otherwise define the task before training.

</details>

---
*Previous: [M04 overview](../README.md). Next: [4.2 Where fine-tuning fits](../02_where_fine_tuning_fits/README.md).*
