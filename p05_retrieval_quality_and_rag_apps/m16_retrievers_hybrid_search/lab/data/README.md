# Lab data

The solution reads only these files, through `../data/`. Never edit them; a solution that changes files works on a copy in a temporary folder.

| File | What it is | Source and licence |
|---|---|---|
| [larkspur/](larkspur/README.md) | The Larkspur Cloud handbook (13 files) and the 30-question golden set, copied unchanged from the repository's `data/larkspur/`. | Written for this course; repository licence. |
| `extra_questions.jsonl` | Five lab-local questions in the golden-set schema (`id`, `question`, `type`, `evidence_spans`, `reference_answer`), each pairing an exact term with a paraphrase. Their spans are exact handbook substrings. The solution scores them only when fewer than three golden questions are answered by hybrid search alone. | Written for this course; repository licence. |
