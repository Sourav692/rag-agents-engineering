# M12.5 Theory: Web, YouTube and arXiv sources; bulk directory loading

*[M12 theory](../README.md) · Lesson 12.5 · Notebooks: [`05a_url_loader.ipynb`](../../../../course/p05_ingestion_and_indexing/m12_document_ingestion/notebooks/05a_url_loader.ipynb), [`05b_youtube_transcript_loader.ipynb`](../../../../course/p05_ingestion_and_indexing/m12_document_ingestion/optional/05b_youtube_transcript_loader.ipynb) (optional), [`05c_research_paper_loader.ipynb`](../../../../course/p05_ingestion_and_indexing/m12_document_ingestion/optional/05c_research_paper_loader.ipynb) (optional), [`05d_directory_loader.ipynb`](../../../../course/p05_ingestion_and_indexing/m12_document_ingestion/optional/05d_directory_loader.ipynb) (optional) · [All theory pages](../../../README.md)*

## Routing a mixed folder

The M12 lab asks for a mixed folder: the handbook as PDF, the onboarding guide as DOCX, release notes in Markdown, `plans.csv` and the status page from the web. `DirectoryLoader` loads a folder with one loader class per file type. The directory notebook builds one `DirectoryLoader` per extension, each with its own `glob`, `loader_cls` and `loader_kwargs`, because the default `loader_cls` is `UnstructuredFileLoader` for everything.

Two defaults matter on a real folder:

- **`silent_errors=False`** stops the whole run at the first file that fails to parse. Set it to `True` for a nightly job, and then compare the number of files with the number of distinct `source` values, because a skipped file only shows up in the log.
- **`show_progress` and `use_multithreading`** are off. Turn them on for folders of thousands of files; `max_concurrency` defaults to 4.

Loading the folder is the easy half. Each loader writes its own metadata, with its own key names and counting rules. This is what each one sets, in `langchain-community` 0.4.2, run on files in this repo's `data/sample/` (the last three read from the loader source, since they need the network):

| Loader | One Document per | Metadata it sets |
|---|---|---|
| `TextLoader`, `Docx2txtLoader` | file | `source` |
| `PyPDFLoader` | page | `source`, `page` (0-based), `page_label`, `total_pages`, `producer`, `creator`, `creationdate`, `moddate` |
| `PyMuPDFLoader` | page | `source`, `page` (0-based), `total_pages`, `producer`, `creationdate`, `moddate`, plus `file_path`, `format`, `title`, `author` and the dates again in PDF format (`creationDate`, `modDate`); no `page_label` |
| `CSVLoader` | row | `source` as you passed it, `row` (0-based) |
| `JSONLoader` | jq match | `source` as an absolute path, `seq_num` (1-based) |
| `RecursiveUrlLoader` | page crawled | `source` (the URL), `content_type`, `title`, `description`, `language` |
| `YoutubeLoader` | video, or time window | `source` (the video id); with chunks also `start_seconds`, `start_timestamp` |
| `ArxivLoader` | paper | `Published`, `Title`, `Authors`, `Summary`; no `source` at all |

None of these fill the lab's five fields (`source`, `type`, `section`, `page`, `date`) the same way. Map each loader's output onto the schema in one function, right after loading and before splitting, so every later stage sees one shape:

```python
def to_schema(doc, kind):
    m = doc.metadata
    page = m.get("page")
    fields = {
        "source": m.get("source") or m.get("entry_id"),   # arXiv: load_all_available_meta=True
        "type": kind,                                      # set by the route, not guessed
        "page": page + 1 if page is not None else m.get("page_number"),
        "date": m.get("creationdate") or m.get("Published"),
    }
    doc.metadata = {k: v for k, v in fields.items() if v is not None}
    return doc
```

The function chooses one meaning per field: `page` is always 1-based, `date` is always ISO, and `source` is always something a reader can open. It drops the fields a loader did not set instead of storing `None`, so a filter on `page` only ever meets numbers. `section` is missing on purpose: only an element-level parser can fill it (lesson 12.4), so add it on the routes that use one.

## Web pages, transcripts and papers

Remote sources fail more quietly than files, because the loader returns whatever the server sent.

**Web pages.** `RecursiveUrlLoader` crawls from a root URL to `max_depth=2` by default and stays under that root (`prevent_outside=True`). Without an `extractor`, `page_content` is the raw HTML, so tags, scripts and navigation menus get embedded; the URL notebook passes a BeautifulSoup `bs4_extractor` to keep only the text. Two more defaults to change:

- `check_response_status=False` keeps error responses. A 404 page becomes a Document holding the error page's text, and it gets indexed. Set it to `True`.
- The loader fetches HTML and does not run JavaScript. A page that renders its content in the browser comes back as an empty shell. Flag Documents whose text is much shorter than the HTML they came from.

**YouTube transcripts.** By default `YoutubeLoader` returns one Document per video with the video id as `source`. With `transcript_format=TranscriptFormat.CHUNKS` it returns one Document per `chunk_size_seconds` window (120 by default; the notebook uses 10 and 15), and each `source` becomes the video URL with `&t=<seconds>s`, so a citation opens the video at that moment. `add_video_info=True` adds title and author but needs another network call, which is where the notebook's SSL errors come from.

**arXiv papers.** `ArxivLoader` downloads each matching PDF, reads it with PyMuPDF, and joins every page into one Document. The page numbers are lost, so a citation can name the paper but not the page. `Published` holds the date of the latest version, not the first submission. `load_max_docs` defaults to 100, and `get_summaries_as_docs()` returns only the abstracts, which is often enough for a "find me papers about X" index and far cheaper to embed.

---
*Previous: [12.4 PDF and Word: parser comparison and element-level parsing](../04_pdf_and_word_parser_comparison_and_element_level_parsing/README.md). Next: [12.6 Custom loaders with lazy loading](../06_custom_loaders_with_lazy_loading/README.md).*
