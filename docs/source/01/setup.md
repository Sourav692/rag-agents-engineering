# Setup

## 1. Install

```bash
git clone https://github.com/Sourav692/ai-engineering-demystified-01-foundations.git
cd ai-engineering-demystified-01-foundations
uv sync
```

`uv sync` creates `.venv/` with Python 3.12 and installs the pinned default dependencies from `uv.lock`: the data, database, web and provider-SDK libraries for modules 01–05, plus the `dev` group (Jupyter, pytest, ruff, pre-commit, nbstripout).

### Heavy ML stack (modules 04 notebook 03, 07, 08)

```bash
uv sync --group hf
```

Adds torch, torchaudio, transformers, diffusers, accelerate, datasets, trl, gradio, OpenCV, librosa, pyannote.audio, pydub and the Lamini client. This is several GB; install it only when you reach those modules. The AutoTrain notebook in module 08 installs `autotrain-advanced` itself with `!pip install`, as in the original course.

## 2. Configure keys

```bash
cp .env.example .env
```

Fill in only what you need — see the table in the README. Notebooks that prompt with `getpass` do not read `.env`; paste the key when asked.

## 3. Verify (offline)

```bash
uv run pytest
```

Runs the structural checks — notebooks are valid, titled and output-free, every file path a notebook reads resolves, all links resolve, and every Python file compiles. No network and no API keys.

## 4. Work through the notebooks

```bash
uv run jupyter lab
```

Open notebooks from their own folder; relative paths such as `../assets/…` assume Jupyter's working directory is the notebook's folder, which is the default. Module 03's lessons are scripts:

```bash
uv run python modules/03_concurrency_and_asyncio/notebooks/01_threading.py
```

## Databases for module 02

Notebook 04 uses in-memory SQLite and needs nothing. Notebooks 05 and 06 need a MySQL and a PostgreSQL server you can reach; the connection values in those notebooks (host, user, password, `ai_agent_db`) are placeholders to replace. A throwaway local server is enough, for example:

```bash
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=change-me -p 3306:3306 mysql:8
docker run -d --name postgres -e POSTGRES_PASSWORD=change-me -p 5432:5432 postgres:16
```

## Contributing

`uv run pre-commit install` once per clone. The hooks strip notebook outputs and run the same checks as `pytest`. See [CONTRIBUTING.md](../CONTRIBUTING.md).
