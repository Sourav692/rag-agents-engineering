# Lab data

| File | Source | Licence |
|---|---|---|
| [larkspur/](larkspur/README.md) | Copy of [`data/larkspur/`](../../../../data/larkspur/README.md), byte for byte (`tests/test_labs.py` checks it): 13 handbook files and `golden.jsonl`, 30 questions. Never edit the copy. | Written for this course; fictional company; the repository's licence |
| `grading_pairs.jsonl` | Written for this lab from the Larkspur handbook (see below) | The repository's licence |

## grading_pairs.jsonl

30 rows with `id`, `question`, `passage` and `label` (`yes` or `no`). For 15 golden questions (`g01`, `g03` to `g08`, `g10` to `g12`, `g14`, `g16`, `g22`, `g24`, `g25`), the handbook was split with `RecursiveCharacterTextSplitter` (500 characters, 50 overlap) and ranked with scikit-learn TF-IDF (English stop words), as in `src/lab_kit.py`. Each question has two rows:

- `<id>-pos`: the highest-ranked passage that holds one of the question's evidence spans.
- `<id>-neg`: the highest-ranked passage that holds none of them, usually a passage on the same topic.

The labels were written by reading each pair: `yes` when the passage states what the question asks, `no` when it does not. For these 30 pairs the reading agreed with the span rule, so the set has 15 `yes` and 15 `no`.

Back to the lab: [README.md](../README.md)
