# Lab: M03 Hugging Face Models & Gradio Demos

## Brief

Model demo: wrap an open embedding or text model from the Hub in a Gradio app that shows its output for a user-entered query.

## Approach

The solution, [solution/m03_solution.ipynb](solution/m03_solution.ipynb), loads `sentence-transformers/all-MiniLM-L6-v2` once, embeds the Larkspur handbook passages with normalised vectors, and serves a `gr.Blocks` app that returns the three closest passages for a typed question. The same search function is called directly on golden questions `g01` to `g03`, and each result is checked against the evidence spans.

- **Load once, call many times.** The model and the passage vectors are built at start-up; the search function only embeds the query (lesson 3.5).
- **Mind the token limit.** Text past a model's input limit is dropped without an error. The passages are 500-character splits, well inside the limit, and theory lesson 3.2 shows how to count tokens with the model's own tokenizer.
- **Pin what you load.** A moving `main` branch can change results without a code change; pass `revision=` with a commit hash once you settle on a version (lesson 3.1).
- **A demo is not a service.** Gradio adds no login, rate limit or monitoring. `demo.launch(prevent_thread_lock=True)` hands control back to the notebook and `demo.close()` stops the server.

## How to run

- Environment: `uv sync --group hf --group hf-foundations`. `sentence-transformers` is in the `hf` group and `gradio` in `hf-foundations`; both groups install torch.
- Keys: none (the model is public). Docker: none. The first run downloads the model from the Hub.
- Execute in place: `uv run --group hf --group hf-foundations jupyter nbconvert --to notebook --execute p01_ai_engineering_foundations/m03_hugging_face_models/lab/solution/m03_solution.ipynb --output /tmp/m03_run.ipynb`

## Data

`data/larkspur/`, a byte-for-byte copy of the course corpus. See [data/README.md](data/README.md).

## Results

Not run yet; the owner runs the solution and fills this table with the run date and the model revision.

| Question | Hit in top 3 | First hit rank |
|---|---|---|
| g01 How long does a refund take? | *pending run* | *pending run* |
| g02 What happens if my server goes down? | *pending run* | *pending run* |
| g03 Can I export my data after I cancel my plan? | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
