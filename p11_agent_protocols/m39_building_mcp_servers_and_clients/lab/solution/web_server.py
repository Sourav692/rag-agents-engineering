"""web-search: Tavily web search as an MCP tool, served over stdio.

    uv run --group protocols python web_server.py      # normally started by the notebook's MCP client

Needs TAVILY_API_KEY in its environment; the client passes it when it starts this process.
"""
import os

from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
mcp = FastMCP("web-search")


@mcp.tool()
def search_web(query: str, max_results: int = 3) -> str:
    """Search the public web for current or general information that is not in the Larkspur Cloud handbook."""
    results = client.search(query, max_results=max(1, min(max_results, 5))).get("results", [])
    if not results:
        return "No web results."
    return "\n\n".join(f"[{r['url']}] {r['title']}\n{r.get('content', '')}" for r in results)


if __name__ == "__main__":
    mcp.run(transport="stdio")
