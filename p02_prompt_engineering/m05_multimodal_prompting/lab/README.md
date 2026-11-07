# Lab: M05 Multimodal Prompting

## Brief

Report reader: answer five questions about a chart-heavy PDF page by prompting a multimodal model with the page image.

## Approach

The solution, [solution/m05_solution.ipynb](solution/m05_solution.ipynb), sends page 1 of the CRS report *Wildfire Statistics* as a PNG to `gemini-2.5-flash` (the model of notebook 01a) through the `google-genai` SDK, once per question, and checks each reply against values read off the page by hand.

- **Say what the image holds.** The prompt names the page's two figures and its table, asks for printed values only, fixes the output shape and gives the model a way out (`NOT_ON_PAGE`) instead of a guess (lesson 5.1).
- **Read labels, do not measure bars.** Figure 2 prints its values on the bars, so the prompt asks the model to read them (lesson 5.3).
- **Grade on known values.** Every question has a printed answer. The grader compares numbers, not substrings, so a reply that lists every year on the page does not pass by accident.
- **What to watch.** A failed check is worth reading against the image: a misread digit, a value from the wrong figure and a guessed value need different fixes.

## How to run

- Environment: the default `uv sync`; no extra group.
- Keys: `GOOGLE_API_KEY`, read from the repository's `.env` (template: `.env.example`). Docker: none.
- Execute in place: `uv run jupyter nbconvert --to notebook --execute p02_prompt_engineering/m05_multimodal_prompting/lab/solution/m05_solution.ipynb --output /tmp/m05_run.ipynb`

## Data

`data/if10244_page1.png` (the page, rendered from `data/sample/IF10244.pdf`) and `data/questions.jsonl` (five questions with hand-read answers). Source and licence: [data/README.md](data/README.md).

## Results

Not run yet; the owner runs the solution and fills this table with the run date and the model.

| Question | Source | Expected | Model reply | Correct |
|---|---|---|---|---|
| q1 Largest acreage year since 1960 | Figure 2 | 2015, 10.13 million acres | *pending run* | *pending run* |
| q2 Fires in 2006 | Figure 2 | 96.4 thousand | *pending run* | *pending run* |
| q3 Fewest fires of the five years | Figure 2 | 2020, 59.0 thousand | *pending run* | *pending run* |
| q4 Total fires in 2022 | Table 1 | 69.0 thousand | *pending run* | *pending run* |
| q5 Fewest acres burned, 2018 to 2022 | Table 1 | 2019, 4.7 million acres | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
