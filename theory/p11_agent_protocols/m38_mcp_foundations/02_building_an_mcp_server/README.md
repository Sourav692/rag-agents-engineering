# M38.2 Theory: Building an MCP server

*[M38 theory](../README.md) · Lesson 38.2 · Notebooks: [`02a_creating_an_mcp_server.ipynb`](../../../../course/p11_agent_protocols/m38_mcp_foundations/notebooks/02a_creating_an_mcp_server.ipynb) · [All theory pages](../../../README.md)*

## From a function to a tool definition

Larkspur wants a search function discoverable by any MCP client. You will expose it through FastMCP, inspect the generated input and output schemas and test the server before writing an agent host.

### Step 1: Expose a typed function as a server tool

A server that offers tools answers two requests: list the tools, and call one. The MCP Python SDK gives two ways to build it. The low-level `Server` makes you handle `ListToolsRequest` and `CallToolRequest` yourself. `FastMCP`, which the reference implementation uses, does it for you: create the server, decorate functions, run it.

Implementation excerpt from the configured application. The practice material supplies its models, data and session setup:

```text
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

### Step 2: Start the server outside the example cell

The example writes this file with `%%writefile`, so the cell saves the server instead of running it; the server starts later from a terminal or from a client. On `stdio` the server reads requests from its standard input and writes replies to its standard output, one JSON-RPC message per line.

Inspect discovery locally with the pinned MCP SDK. This registers a synthetic tool and lists it in-process. It does not start a network server or search arXiv.

```python
import asyncio
from mcp.server.fastmcp import FastMCP

server = FastMCP("schema-demo")

@server.tool()
def search_handbook(query: str, max_results: int = 2) -> str:
    """Search the Larkspur handbook."""
    return query

tools = asyncio.run(server.list_tools())
definition = tools[0]
print(definition.name)
print(definition.inputSchema["required"])
print(definition.inputSchema["properties"]["max_results"]["default"])
```

**Expected output**

```text
search_handbook
['query']
2
```

### Step 3: Inspect the advertised tool definition

FastMCP builds the definition from the function. Here is what SDK 1.30.0 sends for `search_papers` in reply to `tools/list`, recorded from the example's server and printed as the dict the chatbot builds:

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

### Step 4: Compare generated metadata with a hand-written schema

Compare it with the schema the reference implementation wrote by hand. That one gave each parameter a description (“The topic to search for”) and a one-line tool description. The generated pair is 989 characters of compact JSON against 611 for the hand-written pair, and the model reads the parameter help only as free text inside the description. When a parameter needs help or limits, put them in the type: with `Annotated[int, Field(description="Number of chunks to return", ge=1, le=12)]`, SDK 1.30.0 adds `description`, `minimum` and `maximum` to that property.

### Step 5: Read the output contract before returning a value

FastMCP also infers an output schema from the return type. For the Larkspur `search_handbook` tool, which returns `str`, the definition carries `"outputSchema": {"properties": {"result": {"title": "Result", "type": "string"}}, "required": ["result"], "title": "search_handbookOutput", "type": "object"}`, and every call returns the text twice: once in `content` and once in `structuredContent`. The example's chatbot passes only `result.content` to the model, so the copy costs bytes on the wire and nothing in the prompt.

Test a server before writing a client. The MCP Inspector launches it the way a client would, `npx @modelcontextprotocol/inspector uv run research_server.py`, and lets you list and call tools by hand. If a tool works in the Inspector and fails in the chatbot, look in the client first.

### Try it yourself

List the server's tools and compare required topic with defaulted max_results. Check that a docstring Args block does not automatically become per-argument JSON Schema descriptions in the recorded SDK version. Add a Field description and inspect the definition again before binding it to a model.

### Practice notebook

Run the complete implementation from the practice material after checking the trace or calculation above. Use its stated environment for live model or server calls; recorded model choices and timings are observations, not guaranteed outputs.

- [Creating an MCP server](../../../../course/p11_agent_protocols/m38_mcp_foundations/notebooks/02a_creating_an_mcp_server.ipynb).

## Key Takeaways

- `FastMCP` builds each tool definition from the function: the name, the whole docstring as description, types and `required` from the hints, and defaults from Python.
- Docstring `Args:` lines never become property descriptions. Put parameter help and limits in the type with `Annotated[..., Field(...)]` so they appear in the schema.
- Test a new server in the MCP Inspector before writing a client. If a tool passes there and fails in the chatbot, the fault is in the client.

## Check yourself

<details>
<summary>1. Where does FastMCP take each part of a tool definition from, and where do the docstring's parameter descriptions end up?</summary>

The name comes from the function name, the description from the whole docstring, the types and `required` from the type hints, and `default` from the Python default. Nothing fills the property descriptions: the `Args:` lines stay inside the tool description, so the model reads parameter help only as free text.

</details>

<details>
<summary>2. The Larkspur search tool needs a chunk count between 1 and 12 that the model can see in the schema. How do you declare it?</summary>

Put the help and the limits in the type: `Annotated[int, Field(description="Number of chunks to return", ge=1, le=12)]`. SDK 1.30.0 then adds `description`, `minimum` and `maximum` to that property. An `Args:` line in the docstring would only add free text to the tool description.

</details>

<details>
<summary>3. A tool works when you call it by hand in the MCP Inspector but fails inside your chatbot. Where do you look first?</summary>

In the client. The Inspector launches the server the way a client would and calls the tool directly, so a pass there shows the server and the tool work. Test the server in the Inspector before writing a client, so this split is available when something breaks.

</details>

---
*Previous: [38.1 From a tool-calling chatbot to MCP](../01_from_a_tool_calling_chatbot_to_mcp/README.md). Next: [38.3 Building an MCP client](../03_building_an_mcp_client/README.md).*
