# Lab: M06 LangChain Core: Models, Prompts & Parsers

## Brief

Structured answers: build a prompt template and parser that turn a question plus three passages into a JSON answer with a citations list.

## Approach

The solution, [solution/m06_solution.ipynb](solution/m06_solution.ipynb), retrieves three Larkspur passages per question with TF-IDF, labels them `P1` to `P3`, and asks for `{"answer": str, "citations": [str]}` through a `ChatPromptTemplate` and a `PydanticOutputParser`. It runs the first 10 golden questions that have evidence spans and counts parse failures and citations that name a passage without an evidence span.

- **Format instructions must arrive.** The template has a `{format_instructions}` slot filled once with `.partial()`, and the solution prints the formatted prompt once to confirm the schema is in it (lessons 6.5 and 6.6).
- **Count failures, do not crash.** The model call and `parser.parse` are separate steps, so an `OutputParserException` is counted and the loop goes on (lesson 6.6).
- **The schema allows what it allows.** `list[str]` accepts any citation, so the check against the offered ids and the evidence spans runs after the parser. Typing the ids as `Literal["P1", "P2", "P3"]`, or `with_structured_output` on a model that supports it, moves part of that check into the schema (lesson 6.7).
- **What to watch.** A citation to a passage without an evidence span is not always wrong; a passage can support part of an answer in other words. Read those rows before counting them as errors.

## How to run

- Environment: the default `uv sync`; no extra group.
- Keys: `EXPERIENTIALLABS_API_KEY`, read from the repository's `.env` (template: `.env.example`). Docker: none.
- Execute in place: `uv run jupyter nbconvert --to notebook --execute p03_llm_application_frameworks/m06_langchain_core/lab/solution/m06_solution.ipynb --output /tmp/m06_run.ipynb`

## Data

`data/larkspur/`, a byte-for-byte copy of the course corpus. See [data/README.md](data/README.md).

## Results

Not run yet; the owner runs the solution and fills this table with the run date and the model.

| Questions | Parse failures | Citations | Citations to a passage without an evidence span | Answers with no citation |
|---|---|---|---|---|
| 10 | *pending run* | *pending run* | *pending run* | *pending run* |

Back to the module: [README.md](../README.md)
