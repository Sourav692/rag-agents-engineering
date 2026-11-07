# Lab data

The solution reads only these files, through `../data/`. Never edit them; a solution that changes files works on a copy in a temporary folder.

| File | What it is | Source and licence |
|---|---|---|
| [larkspur/](larkspur/README.md) | The Larkspur Cloud handbook (13 files) and the 30-question golden set, copied unchanged from the repository's `data/larkspur/`. | Written for this course; repository licence. |
| `report.pdf` | A fictional three-page Larkspur Cloud quarterly report. Each page has a short text paragraph and one chart drawn with matplotlib and embedded as a raster image, so its numbers are not in the PDF text layer. | Written for this course; repository licence. |
| `report_data.json` | The values plotted in `report.pdf`. The solution does not read it; it documents the charts. | Written for this course; repository licence. |
| `questions.jsonl` | Five questions (`id`, `question`, `answer`, `page`) whose answers are read from the plotted data. | Written for this course; repository licence. |
