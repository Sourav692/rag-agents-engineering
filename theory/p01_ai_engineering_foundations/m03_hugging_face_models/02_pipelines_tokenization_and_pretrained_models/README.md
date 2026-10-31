# M03.2 Theory: Pipelines, tokenization and pretrained models

*[M03 theory](../README.md) · Lesson 3.2 · Notebooks: [`02a_pipelines_for_nlp_tasks.ipynb`](../../../../course/p01_ai_engineering_foundations/m03_hugging_face_models/notebooks/02a_pipelines_for_nlp_tasks.ipynb), [`02b_understanding_llms.ipynb`](../../../../course/p01_ai_engineering_foundations/m03_hugging_face_models/notebooks/02b_understanding_llms.ipynb), [`02c_accessing_pretrained_models.ipynb`](../../../../course/p01_ai_engineering_foundations/m03_hugging_face_models/optional/02c_accessing_pretrained_models.ipynb) (optional) · [All theory pages](../../../README.md)*

## Pipelines

`pipeline()` from `transformers` loads a tokenizer and a model from one Hub repo and runs three steps on every call: pre-processing (the tokenizer turns text into token ids), the forward pass (the model turns ids into numbers) and post-processing (those numbers become a label, a span or generated text). Notebook `02a` runs it for sentiment, named entities, question answering and translation; `01b` uses it to label 1,066 movie reviews and computes accuracy against the dataset's labels.

```mermaid
flowchart LR
    X[/"Ticket text"/] --> T["Tokenizer<br/>tokens, ids"]
    T --> M["Model<br/>logits"]
    M --> P["Post-process<br/>softmax, id2label"]
    P --> Y[/"label, score"/]
```
<!-- animated: diagrams/pipeline.anim.html -->

For a Larkspur ticket, *My refund took three weeks.*, the sentiment pipeline's tokenizer produces nine ids: `[CLS] my ref ##und took three weeks . [SEP]`. The model returns two logits, softmax turns them into probabilities, and the model's `config.json` maps index 0 to `NEGATIVE` and 1 to `POSITIVE`. Each step can go wrong on its own. A ticket longer than the model's 512 positions has to be truncated at the tokenizer, a model trained on movie reviews misreads billing language in the forward pass, and a two-label head cannot say "billing" or "outage" at all.

**A task name picks a model for you.** `pipeline(task="text-classification")` with no `model=` loads the task's default, and `transformers` prints "No model was supplied, defaulted to … Using a pipeline without specifying a model name and revision in production is not recommended." In `transformers` 5.17.0, the version this course locks, the defaults include:

| Task | Default model | Pinned revision |
|---|---|---|
| `text-classification` (alias `sentiment-analysis`) | `distilbert/distilbert-base-uncased-finetuned-sst-2-english` | `714eb0f` |
| `token-classification` (alias `ner`) | `dbmdz/bert-large-cased-finetuned-conll03-english` | `4c53496` |
| `text-generation` | `HuggingFaceTB/SmolLM3-3B` | `a07cc9a` |

The NER default is 1.33 GB of weights, five times the sentiment model's 268 MB, which is why `02a` warns before loading it. Pass `model=` (and `revision=` with a commit hash) to choose the model yourself: `02a` loads `ProsusAI/finbert` for financial headlines, and the task comes from the repo's metadata.

**The task list changes between releases.** The list printed at the top of `02a` comes from an older `transformers`. Version 5.17.0 has no `question-answering`, `translation`, `summarization`, `text2text-generation` or `conversational` task, so the notebook's `pipeline('question-answering')` and `pipeline('translation_en_to_fr')` cells fail in this course's environment. Print `transformers.pipelines.get_supported_tasks()` to see what your installed version supports.

Two smaller points from the notebooks. `save_pretrained(folder)` writes the tokenizer, model and config into a folder that `pipeline(model=folder)` loads again; `02a` saves the text-classification pipeline that way, not the NER one, and writes the folder next to the notebook. Notebook `02c` shows the same text generation twice: once with `AutoTokenizer` and `AutoModelForCausalLM` and an explicit `generate()`, once as `pipeline("text-generation", model="gpt2")`. The pipeline is shorter; the explicit version lets you read the logits, which the next two sections need.

## Tokenization

Models read tokens, pieces of text from a fixed vocabulary, each mapped to an integer id. Notebook `02b` explains why the pieces are subwords: a character vocabulary is small but needs many tokens per sentence, a word vocabulary is large and still meets unknown words, and subwords keep common words whole while building rare ones from parts. Every model ships its own tokenizer, and the ids mean nothing to any other model. These are real outputs of the two tokenizers this module and M14 use, from `AutoTokenizer` in `transformers` 5.17.0:

| Text | GPT-2 (byte-level BPE, 50,257 tokens) | `all-MiniLM-L6-v2` (WordPiece, lower case, 30,522 tokens) |
|---|---|---|
| *Larkspur Cloud* | `L` `arks` `pur` `␣Cloud` | `[CLS]` `lark` `##sp` `##ur` `cloud` `[SEP]` |
| *Preposterous, I'm flabbergasted!* | `Prep` `oster` `ous` `,` `␣I` `'m` `␣fl` `ab` `berg` `asted` `!` | `[CLS]` `prep` `##ost` `##ero` `##us` `,` `i` `'` `m` `fl` `##ab` `##berg` `##ast` `##ed` `!` `[SEP]` |
| *Can I export my data after I cancel my plan?* | 11 tokens, one per word plus `?` | 13 tokens, the same split plus `[CLS]` and `[SEP]` |

The two schemes differ in ways that matter later. GPT-2 keeps case and attaches a leading space to the token after it (`␣` above), so "fl" at the start of a text is id 2704 and " fl" after a space is id 781; `02b`'s markdown quotes the second. WordPiece lower-cases everything, marks a piece that continues a word with `##`, and adds `[CLS]` and `[SEP]` around every input.

Prices and limits are counted in tokens, so the ratio of characters to tokens decides what a text costs. M11 estimated tokens as characters divided by four. On the handbook that holds: the refunds section is 1,111 characters and 246 GPT-2 tokens (4.52 characters per token), the FAQ page 1,415 characters and 308 tokens (4.59). It fails on rare words: *Preposterous, I'm flabbergasted!* runs at 2.91 characters per GPT-2 token and 2.29 per MiniLM token. Product names, codes and other languages move the ratio the same way, so count with the model's own tokenizer before you budget.

**Every model has a token limit, and the text past it is dropped without an error.** GPT-2 has 1,024 positions. The MiniLM tokenizer reports 512, but sentence-transformers reads `max_seq_length: 256` from the repo's `sentence_bert_config.json` and cuts every input there, `[CLS]` and `[SEP]` included. The FAQ page is 291 MiniLM tokens, so its last 35 tokens, 183 characters holding the support response times and the promotional-credit rule, never reach the model. Embedding the whole page and embedding its first 1,231 characters give the same vector (cosine similarity 1.0000). *How fast does support answer a ticket?* then scores 0.229 against the page and 0.687 against the support answer on its own. This is the reason M13 sizes chunks and why the size must be measured in the embedding model's tokens.

The [interactive lab](interactive/token-limit-lab.html) holds the real token ids for five Larkspur texts under both tokenizers and cuts them exactly as `tokenizer(text, truncation=True, max_length=N)` does; it matches the library at every limit from 8 to 320, 3,130 settings with 0 mismatches. Lower the limit on the refunds section to 128 and MiniLM keeps the text up to "less than 100 GB of out", splitting the sentence M13's golden question needs, while GPT-2's cut falls one word earlier, before "GB".

<!-- lab: interactive/token-limit-lab.html -->

## From logits to text

A causal language model such as GPT-2 predicts the next token. Notebook `02b` feeds it *I skip across the*, four tokens, and gets logits of shape `[1, 4, 50257]`: one batch, one row per input token, one score per vocabulary entry. The last row scores every possible next token; `argmax` picks the most likely, and `softmax` turns the row into probabilities. `generate()` repeats that step, appending each new token to the input.

```mermaid
flowchart LR
    I["4 input ids"] --> G["GPT-2"]
    G --> L["Last row<br/>50,257 logits"]
    L --> C{"Pick next<br/>token"}
    C --> A["Append it"]
    A -- repeat --> G
```

How the next token is picked is the decoding strategy, set by `generate()`'s arguments. The notebook's settings:

- **Greedy** (the default): the most likely token every time. Deterministic, and prone to repeating itself in long text.
- **Beam search**, `num_beams=5`: keeps the five most likely sequences and returns the best whole one; `repetition_penalty=1.2` lowers the score of tokens already used.
- **Sampling**, `do_sample=True`: draws from the probabilities. `temperature=0.4` sharpens them toward the top tokens, `top_k=10` draws only from the ten most likely, and `top_p=0.94` from the smallest set whose probabilities add up to 0.94. The notebook sets `top_k=0` to switch the top-k filter off when it tests temperature and top-p alone.

Two details catch people out. `max_new_tokens=20` counts only generated tokens, while `max_length=40` counts the prompt too and leaves room for 36 new tokens after the 4-token prompt. And GPT-2 has no padding token; `02c` passes `pad_token_id=tokenizer.eos_token_id` to silence the warning `generate()` gives about it. The code comment in `02b`'s first tokenizer cell, `tensor([[1026, 373, 257, 3223, 290, 6388, 88]])`, is the encoding of *It was a dark and stormy*, not of the sentence in that cell.

## Check yourself

<details>
<summary>1. Why is pipeline with only a task name a risk in production code?</summary>

It loads the task's default model, chosen by the installed `transformers` version, and the library warns that a pipeline without a model name and revision is not recommended in production. In 5.17.0, `text-classification` loads `distilbert/distilbert-base-uncased-finetuned-sst-2-english` at `714eb0f`. Pass `model=` and `revision=` with a commit hash to choose it yourself.

</details>

<details>
<summary>2. The FAQ page is 291 MiniLM tokens. Why does the support-speed question score 0.229 against the whole page but 0.687 against the support answer alone?</summary>

sentence-transformers cuts every input at `max_seq_length: 256`, so the page's last 35 tokens, the 183 characters with the support response times, never reach the model. The whole page and its first 1,231 characters give the same vector, so the page's embedding carries no trace of the answer. This is why M13 sizes chunks in the embedding model's tokens.

</details>

<details>
<summary>3. A GPT-2 reply generated with default settings repeats itself in long text. Which generate arguments from the notebook change that?</summary>

The default is greedy decoding, which is deterministic and prone to repetition. Beam search with `num_beams=5` and `repetition_penalty=1.2` lowers the score of tokens already used. Sampling with `do_sample=True` draws from the probabilities instead, shaped by `temperature`, `top_k` and `top_p`.

</details>

---
*Previous: [3.1 Hub setup, datasets and models](../01_hub_setup_datasets_and_models/README.md). Next: [3.5 Building demos with Gradio](../05_building_demos_with_gradio/README.md).*
