# M42 lab data

All files were written for this course and carry the repository's licence. Larkspur Cloud is fictional.

| Path | Source | Licence |
|---|---|---|
| [larkspur/](larkspur/README.md) | Unchanged copy of `data/larkspur/`: the handbook and its golden set | Repository licence |
| [global_questions.jsonl](global_questions.jsonl) | Ten "summarise or compare across the whole handbook" questions written by the author, one per line: `id` (`q01` to `q10`), `question`, `sections` (the handbook files the answer draws on, two to seven per question) and `reference_answer` (written from the handbook text only) | Repository licence |

No single passage answers a global question: each reference answer combines facts from several handbook files, which is what RAPTOR's summaries and LightRAG's high-level keywords are for.
