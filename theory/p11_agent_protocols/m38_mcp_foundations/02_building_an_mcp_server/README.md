# M38.2 Theory: Building an MCP server

*[M38 theory](../README.md) · Lesson 38.2 · Notebooks: [`02a_creating_an_mcp_server.ipynb`](../../../../course/p11_agent_protocols/m38_mcp_foundations/notebooks/02a_creating_an_mcp_server.ipynb) · [All theory pages](../../../README.md)*

## From a function to a tool definition

A server that offers tools answers two requests: list the tools, and call one. The MCP Python SDK gives two ways to build it. The low-level `Server` makes you handle `ListToolsRequest` and `CallToolRequest` yourself. `FastMCP`, which notebook 02a uses, does it for you: create the server, decorate functions, run it.

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("research")

@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.
    ...
    """

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

The notebook writes this file with `%%writefile`, so the cell saves the server instead of running it; the server starts later from a terminal or from a client. On `stdio` the server reads requests from its standard input and writes replies to its standard output, one JSON-RPC message per line.

FastMCP builds the definition from the function. Here is what SDK 1.30.0 sends for `search_papers` in reply to `tools/list`, recorded from the notebook's server and printed as the dict the chatbot builds:

```json
{
  "name": "search_papers",
  "description": "\n    Search for papers on arXiv based on a topic and store their information.\n    \n    Args:\n        topic: The topic to search for\n        max_results: Maximum number of results to retrieve (default: 5)\n        \n    Returns:\n        List of paper IDs found in the search\n    ",
  "input_schema": {
    "properties": {
      "topic": {"title": "Topic", "type": "string"},
      "max_results": {"default": 5, "title": "Max Results", "type": "integer"}
    },
    "required": ["topic"],
    "title": "search_papersArguments",
    "type": "object"
  }
}
```

| Part of the definition | Where FastMCP takes it from |
|---|---|
| `name` | The function name |
| `description` | The whole docstring, indentation and `Args:` block included |
| Property types and `required` | The type hints; a parameter with a default is optional |
| `default` | The Python default (`max_results = 5`) |
| Property descriptions | Nothing: the `Args:` lines stay in the description |

Compare it with the schema notebook 01a wrote by hand. That one gave each parameter a description (“The topic to search for”) and a one-line tool description. The generated pair is 989 characters of compact JSON against 611 for the hand-written pair, and the model reads the parameter help only as free text inside the description. When a parameter needs help or limits, put them in the type: with `Annotated[int, Field(description="Number of chunks to return", ge=1, le=12)]`, SDK 1.30.0 adds `description`, `minimum` and `maximum` to that property.

FastMCP also infers an output schema from the return type. For the Larkspur `search_handbook` tool, which returns `str`, the definition carries `"outputSchema": {"properties": {"result": {"title": "Result", "type": "string"}}, "required": ["result"], "title": "search_handbookOutput", "type": "object"}`, and every call returns the text twice: once in `content` and once in `structuredContent`. The notebook's chatbot passes only `result.content` to the model, so the copy costs bytes on the wire and nothing in the prompt.

Test a server before writing a client. The MCP Inspector launches it the way a client would, `npx @modelcontextprotocol/inspector uv run research_server.py`, and lets you list and call tools by hand. If a tool works in the Inspector and fails in the chatbot, look in the client first.

---
*Previous: [38.1 From a tool-calling chatbot to MCP](../01_from_a_tool_calling_chatbot_to_mcp/README.md). Next: [38.3 Building an MCP client](../03_building_an_mcp_client/README.md).*
