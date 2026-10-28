# Setup

## 1. Install the root environment

```bash
uv sync                  # Python 3.12, notebook stack, local helpers package, dev tools
cp .env.example .env     # names only; fill in the keys for what you plan to run
uv run pytest            # offline: notebook structure, links, and a smoke test; no API keys, no network
uv run jupyter lab
```

The root environment covers the ten notebooks (modules 01 and 05) and the repository checks:

- **A2A notebooks (module 05):** `a2a-sdk[http-server]` pinned to the 0.3 line (`>=0.3.0,<0.4`). The notebooks use `A2AClient`, `A2AStarletteApplication` and the pydantic `a2a.types` models, which a2a-sdk 1.x removed. Also `uvicorn`, `httpx`, `nest-asyncio` and LangGraph.
- **`src/helpers`**, installed in editable mode, so `from helpers import get_llm` works. Its default provider is Databricks (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`). `get_llm(provider="openai", model="gpt-4o")` uses `OPENAI_API_KEY` instead.
- **Anthropic MCP course notebooks (module 01):** `anthropic`, `openai`, `arxiv`, `mcp`. Their `IFrame(...)` cells read `DLAI_LOCAL_URL`, which exists only in DeepLearning.AI's hosted notebooks. Skip those cells locally and use the terminal commands in the module README.

## 2. Runnable sub-projects

Every folder under `modules/NN_topic/projects/` is a self-contained server, client or app that you run as a process from its own folder. There are two kinds.

**Sub-projects with their own manifest run in their own environment.** Their `pyproject.toml`, `uv.lock` and `requirements.txt` are unchanged from the source.

| Sub-project | Manifest | Start with |
|---|---|---|
| `01_mcp_foundations/projects/lesson4_research_server`, `lesson5_mcp_chatbot`, `lesson6_reference_servers_chatbot`, `lesson7_prompts_and_resources`, `lesson9_remote_research_server` | `pyproject.toml` + `uv.lock` | `uv sync`, then `uv run research_server.py` or `uv run mcp_chatbot.py` |
| `03_building_mcp_clients/projects/02_multi_server_client` | Dockerfiles, `docker-compose.yml`, `servers/terminal_server/requirements.txt` | its README (`docker compose build`) |
| `03_building_mcp_clients/projects/03_sse_transport_server_client` | `servers/sse_server/requirements.txt`, Dockerfile | its README |
| `05_a2a/projects/mcp_a2a_agentic_rag` | `requirements.txt` (authoritative) and `pyproject.toml` | `uv venv && uv pip install -r requirements.txt`, then `uv run python main.py` |

`mcp_a2a_agentic_rag` pulls in torch and sentence-transformers, which is a large download. Its `pyproject.toml` lists `a2a-python`, while its `requirements.txt` lists `a2a-sdk>=0.3.0`, the package its code imports. Install from `requirements.txt`.

**Sub-projects without a manifest use the root environment plus an optional group:**

| Group | Command | What it adds | Used by |
|---|---|---|---|
| `mcp-labs` | `uv sync --group mcp-labs` | `fastmcp`, `langchain-mcp-adapters`, `langchain-google-genai`, `google-genai`, `google-adk`, `wikipedia`, `rich`, `click` | 01 `wikipedia_assistant_*`; 02 projects 01–03; 03 projects 01 and 04 (and the clients of 02–03) |
| `databricks` | `uv sync --group databricks` | `databricks-sdk`, `databricks-sql-connector`, `yfinance`, `pandas` | 02 project 04 |
| `mcp-apps` | `uv sync --group mcp-apps` | `fastmcp`, `mcp-use`, `langchain-ollama`, `langchain-chroma`, `langchain-mcp-adapters`, `streamlit`, `PyPDF2` | module 04 projects |

Groups can be combined: `uv sync --group mcp-labs --group mcp-apps`. Then run from the sub-project's folder, for example `uv run python mcp_client.py`. `uv run` finds the root environment from any subfolder that has no `pyproject.toml` of its own.

## 3. External tools some sub-projects need

- **Node.js / `npx`:** MCP Inspector (`npx @modelcontextprotocol/inspector`) in module 01, and the third-party servers in module 04's Claude Desktop config (Playwright, Airbnb, Excel, Notion, filesystem, Firecrawl).
- **Docker:** module 03 lab 2, the lesson-9 server image, and module 03 lab 3's optional server image.
- **Ollama:** module 04 projects 02, 06 and 07 (`qwen3`, `gpt-oss`, `nomic-embed-text`).
- **Claude Desktop:** module 04 project 03. Replace the `/ABSOLUTE/PATH/TO/…` placeholders in `claude_desktop_config.json` with your clone's location.

## 4. Environment variables

Notebooks load `.env` from the repository root. Sub-projects call `load_dotenv()` from their own folder, so copy the lines they need into a `.env` there, or export them in your shell. [.env.example](../.env.example) names every variable and what reads it.

## 5. Checks

```bash
uv run pytest -q                         # all three checks
uv run python scripts/check_notebooks.py # structure, clean outputs, relative paths resolve
uv run python scripts/check_links.py     # links resolve; no absolute or old-monorepo paths
uv run ruff check .                      # lesson and sub-project code is excluded (kept as taught)
```

Paths that notebooks write, or that resolve from a sub-project's folder rather than the notebook's, are listed in `scripts/path_allowlist.txt`.
