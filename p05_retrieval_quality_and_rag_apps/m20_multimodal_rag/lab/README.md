# Lab: M20 Multimodal RAG

## Brief

Chart-aware RAG: index a report that holds key numbers only in figures and show which of the three approaches answers questions about them.

## Approach

- Text extraction keeps "Figure 1 shows availability by region" and drops the bars. The report in `data/report.pdf` is built that way on purpose: its numbers exist only as pixels.
- CLIP embeds text and images into one space, but its text-to-text and text-to-image similarities sit on different scales, so in one shared ranking the right figure can rank below every text item and never reach the model.
- Captioning turns each figure into text once, at index time. The model can answer from a caption only as far as the caption wrote the numbers down.
- Late interaction (ColPali) keeps one vector per query token and one per page patch and scores a page by summing each token's best match. It retrieves page images, so the model reads the chart itself.
- Choose by what the model must read at answer time: a caption is cheap to store and search, while a page image keeps the chart, the table layout and the text together.
- Scoring is a string check: every part of the expected answer (for example `Virginia` and `99.91%`) must appear in the reply.

## How to run

The worked solution is [solution/m20_solution.ipynb](solution/m20_solution.ipynb). Open it from `lab/solution/` (Jupyter starts the kernel in the notebook's folder, so `../data/` resolves) and run it top to bottom.

Run with the `colpali` group: `uv run --group colpali jupyter lab` (it resolves `transformers` and `torch` for CLIP and `byaldi` for ColPali in one environment). The first run downloads `openai/clip-vit-base-patch32` and `vidore/colpali-v1.2`; the ColPali model is several GB and runs far faster on a GPU.

Keys, as environment variables in the `.env` file at the repo root: `EXPERIENTIALLABS_API_KEY` for the chat model, which must accept image input (swap in another model through `src/helpers` if it does not), and `DATABRICKS_HOST` and `DATABRICKS_TOKEN` for the default embeddings used by the caption index. Downloading the ColPali weights may need `HF_TOKEN`.

## Data

The solution reads `data/report.pdf` (a fictional three-page Larkspur quarterly report whose numbers are only in its charts) and `data/questions.jsonl` (five questions with answers read from the plotted data). The Larkspur corpus is in `data/larkspur/` as in every lab, but this solution does not read it. [data/README.md](data/README.md) names every file, its source and its licence.

## Results

The solution has not been run yet. The table fills in from its first run, with the run date and the models used; until then no numbers are reported here.

| Measure | Result |
|---|---|
| Run date and models | *pending run* |
| CLIP shared space: right page, correct answers (of 5) | *pending run* |
| Caption then index: right page, correct answers (of 5) | *pending run* |
| ColPali page image: right page, correct answers (of 5) | *pending run* |
| Which approach answers which question | *pending run* |

Back to the module: [README.md](../README.md)
