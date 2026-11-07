"""larkspur-rag: retrieval over the Larkspur handbook as an MCP server, served over stdio.

    uv run --group protocols python rag_server.py      # normally started by an MCP client

Two tools, in the shape of the module's 06_mcp_rag_with_langchain server: `retrieve` returns the top
passages with their source files, and `db_info` describes the index. The index is offline TF-IDF over
../data/larkspur/handbook (src/lab_kit.py), so the server needs no keys.
"""
import sys
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from mcp.server.fastmcp import FastMCP

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../src").resolve()))
from lab_kit import load_handbook, tfidf_retriever  # noqa: E402

HANDBOOK = HERE / "../data/larkspur/handbook"
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
PAGES = load_handbook(HANDBOOK)
CHUNKS = [{"source": p["source"], "text": c} for p in PAGES for c in splitter.split_text(p["text"])]
SOURCE = {c["text"]: c["source"] for c in CHUNKS}
search = tfidf_retriever([c["text"] for c in CHUNKS], k=10)

mcp = FastMCP("larkspur-rag")


@mcp.tool()
def retrieve(query: str, n: int = 4) -> list[dict]:
    """Retrieve the n handbook passages most relevant to the query. Each result has `source` and `text`."""
    return [{"source": SOURCE[t], "text": t} for t in search(query)[: max(1, min(n, 10))]]


@mcp.tool()
def db_info() -> dict:
    """Describe the index: the handbook sections it holds and how many passages."""
    return {"sections": [p["title"] for p in PAGES], "passages": len(CHUNKS),
            "splitter": "recursive, 500 characters, 50 overlap", "ranking": "TF-IDF cosine"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
