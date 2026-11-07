# Lab: M02 LLM Provider APIs & Model Selection

## Brief

Generator choice: answer 20 questions with a fast model, a reasoning model at two effort levels and an open model, and record accuracy, latency and cost per answer.

## Approach

The solution, [solution/m02_solution.ipynb](solution/m02_solution.ipynb), gives each Larkspur question its golden evidence spans as context, so the comparison measures the generator alone. The four configurations follow the module's notebooks: `gpt-4o-mini` (fast) and `o4-mini` at `reasoning_effort` low and high through the OpenAI SDK (notebooks 03a and 04a), and `meta-llama/Llama-3.1-8B-Instruct` through the Hugging Face Inference API (notebook 02a). A separate judge model marks each answer correct or incorrect against `reference_answer`.

- **Cost comes from `usage`.** A reasoning model bills hidden reasoning tokens at the output rate and never returns them, so the reply text says nothing about the bill (lesson 2.3).
- **Price each effort step.** `reasoning_effort` changes only how many reasoning tokens the model spends. A step that adds tokens and latency without adding accuracy is pure cost (lesson 2.4).
- **Open models.** The model id names the weights, not the server; the price depends on the provider Hugging Face routes to, so its cost stays empty until you set one (lesson 2.2).
- **What to watch.** The judge is a model too: read the rows it marks wrong before trusting the accuracy column. The golden set has 19 `lookup` and `numeric` questions, so `g02` (the first `multi_hop` one) makes the 20th.

## How to run

- Environment: the default `uv sync`; no extra group.
- Keys: `OPENAI_API_KEY`, `HF_TOKEN`, `EXPERIENTIALLABS_API_KEY` (judge), read from the repository's `.env` (template: `.env.example`). Docker: none.
- Before running, check the prices in the "Prices" cell against each provider's pricing page and set `PRICES_CHECKED_ON`. The starting values are the ones in notebook 03a.
- Execute in place: `uv run jupyter nbconvert --to notebook --execute p01_ai_engineering_foundations/m02_llm_apis_and_model_selection/lab/solution/m02_solution.ipynb --output /tmp/m02_run.ipynb`

## Data

`data/larkspur/`, a byte-for-byte copy of the course corpus. See [data/README.md](data/README.md).

## Results

Not run yet; the owner runs the solution and fills this table with the run date, the models and the date the prices were checked.

| Configuration | Model | Accuracy (20) | Mean latency (s) | Mean reasoning tokens | Cost per answer (USD) |
|---|---|---|---|---|---|
| fast | `gpt-4o-mini` | *pending run* | *pending run* | *pending run* | *pending run* |
| reasoning, low effort | `o4-mini` | *pending run* | *pending run* | *pending run* | *pending run* |
| reasoning, high effort | `o4-mini` | *pending run* | *pending run* | *pending run* | *pending run* |
| open | `meta-llama/Llama-3.1-8B-Instruct` | *pending run* | *pending run* | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
