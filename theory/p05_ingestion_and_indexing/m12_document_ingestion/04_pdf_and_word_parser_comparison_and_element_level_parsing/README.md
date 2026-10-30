# M12.4 Theory: PDF and Word: parser comparison and element-level parsing

*[M12 theory](../README.md) · Lesson 12.4 · Notebooks: [`04a_pdf_loader.ipynb`](../../../../course/p05_ingestion_and_indexing/m12_document_ingestion/notebooks/04a_pdf_loader.ipynb), [`04b_ms_word_loader.ipynb`](../../../../course/p05_ingestion_and_indexing/m12_document_ingestion/optional/04b_ms_word_loader.ipynb) (optional) · [All theory pages](../../../README.md)*

## Element-level parsing

A page-level parser returns the page as one string. An element-level parser (Unstructured with `mode="elements"`) returns one Document per layout element, each with a `category` such as `Title`, `NarrativeText`, `Table`, `ListItem`, `Header` or `Footer`.

![Page-level versus element-level parsing](diagrams/page-to-elements.svg)

What the three PDF loaders in lesson 12.4 produce from the handbook page:

| | `PyPDFLoader` | `PyMuPDFLoader` | `UnstructuredPDFLoader`, `mode="elements"`, `hi_res` |
|---|---|---|---|
| Documents from the page | 1 | 1 | 10 |
| Header and footer | Inside the text | Inside the text | Separate elements you can drop |
| Pricing table | Rows of space-separated values | One cell per line | `Table` element with `text_as_html` |
| Section of each piece | Unknown | Unknown | `parent_id` points to its `Title` |
| Page number | `page` (0-based) | `page` (0-based) | `page_number` (1-based) |
| Speed and dependencies | Fast, pure Python | Fastest; AGPL licence | Slowest; layout models and system packages |

Three consequences for retrieval:

- **Boilerplate pollutes embeddings.** If every chunk starts with "Larkspur Cloud · Customer Handbook", every chunk shares that text, and similarity between chunks from different pages rises. Drop `Header` and `Footer` elements, or strip repeated lines from page-level text.
- **Flattened tables lose their meaning.** "Business 4 16 GB 5 TB $48" can be read, but once a splitter cuts it, "16 GB" no longer has a column name. Keep a table as one chunk and give the model its HTML or Markdown form.
- **Granularity is decided at load time.** One Document per file, page, row or element sets the smallest thing retrieval can return, and changing it later means re-ingesting.

Element-level parsing costs time and dependencies, so use it where layout carries meaning: reports, manuals, forms, anything with tables. Plain prose PDFs do fine with PyPDF or PyMuPDF.

The [interactive lab](interactive/pdf-parsers-lab.html) shows all three loaders on the handbook page.

---
*Previous: [12.1 The Document abstraction and metadata design](../01_the_document_abstraction_and_metadata_design/README.md). Next: [12.6 Custom loaders with lazy loading](../06_custom_loaders_with_lazy_loading/README.md).*
