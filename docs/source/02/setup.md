# Setup

## Install

```bash
uv sync                  # Python 3.12 venv in .venv, all notebook deps + dev tools (pytest, ruff, jupyterlab, pre-commit, nbstripout)
uv run pre-commit install   # once per clone: strips notebook outputs and runs the checks on commit
cp .env.example .env     # optional
uv run jupyter lab
```

Dependencies are declared in `pyproject.toml` and pinned in `uv.lock`. There are no optional groups: everything the notebooks import is light enough for the default install.

## Things to know before running a notebook

- **Skip the `!pip install` cells.** Each notebook starts with the install cell from its original course. `uv sync` already installed tested versions; re-running those cells can replace them (a bare `pip install moviepy` installs moviepy 2, which removed `moviepy.editor`).
- **LangChain is pinned to 0.3.x.** Module 02's ReAct section imports `AgentExecutor` from `langchain.agents`, which LangChain 1.x removed.
- **API keys** are requested with `getpass` when a notebook starts. See the README's environment-variable table for which notebook needs which key.
- **Sample media are downloaded at run time.** Module 04's notebooks fetch images, a PDF, audio and video with `!curl`, `!wget` and `!gdown` into their own folder. `curl` and `wget` must be on your PATH; `gdown` comes with `uv sync`. The downloaded files are not committed (and are listed in `scripts/path_allowlist.txt` so the offline checks know about them).
- **ffmpeg** — module 04's GPT-4o video section asks you to install it (`brew install ffmpeg` or `sudo apt install ffmpeg`).
- **Model names** are as found in the source (for example `gemini-1.5-flash`, `llama-3.2-90b-vision-preview`). Providers retire models; if a call is rejected, substitute a current model.

## Offline checks

```bash
uv run pytest            # notebook structure, links/self-containment, smoke test - no keys, no network
uv run ruff check .
```

`uv run pytest` never calls a model. The notebooks themselves are not executed by the test suite.
