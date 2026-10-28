"""Run model-written Python in a separate process with a time limit (notebooks 11 and 12).

This is NOT a sandbox. The child process runs as you: the code can still read and write your files and reach the
network. The runner only keeps a runaway snippet from hanging the notebook, keeps the notebook's variables and API
keys out of the child's reach, and closes the keyboard. Code from a model you do not control belongs in a container
or a hosted sandbox.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def run_python(code: str, timeout: float = 10, env: dict[str, str] | None = None) -> str:
    """Run `code` as a script in a new Python process and return what it printed (stdout, then stderr).

    - The process starts in a fresh, empty temporary folder, which is deleted afterwards.
    - `sys.executable -I` is this environment's Python in isolated mode: no user site-packages and no PYTHON*
      variables; the snippet's folder is not on the import path.
    - `env` is the child's whole environment: by default empty, so no API keys reach it.
    - Standard input is closed, so `input()` raises EOFError instead of waiting for a keyboard.
    - After `timeout` seconds the process is killed.
    """
    with tempfile.TemporaryDirectory() as folder:
        script = Path(folder) / "snippet.py"
        script.write_text(code, encoding="utf-8")
        try:
            done = subprocess.run(
                [sys.executable, "-I", str(script)],
                cwd=folder, env=env or {}, stdin=subprocess.DEVNULL,
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return f"Timed out: the code ran longer than {timeout}s and was stopped."
    output = (done.stdout + done.stderr).strip()
    return output or "(no output: use print(...) to show values)"
