"""larkspur-handbook: the Larkspur handbook retriever as an MCP tool, served over stdio.

    uv run --group protocols python server.py      # normally started by the notebook's MCP client

The retriever is the lab baseline: RecursiveCharacterTextSplitter (500 characters, 50 overlap) and
TF-IDF top-k from src/lab_kit.py, over ../data/larkspur/handbook. It runs offline and needs no keys.
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
CHUNKS = [
    {"source": page["source"], "text": chunk}
    for page in load_handbook(HANDBOOK)
    for chunk in splitter.split_text(page["text"])
]
SOURCE = {c["text"]: c["source"] for c in CHUNKS}
search = tfidf_retriever([c["text"] for c in CHUNKS], k=8)

mcp = FastMCP("larkspur-handbook")


@mcp.tool()
def search_handbook(query: str, k: int = 4) -> str:
    """Search the Larkspur Cloud customer handbook and return the top k passages, each with its source file."""
    hits = search(query)[: max(1, min(k, 8))]
    if not hits:
        return "No passage matches the query."
    return "\n\n".join(f"[{SOURCE[h]}]\n{h}" for h in hits)


if __name__ == "__main__":
    mcp.run(transport="stdio")
