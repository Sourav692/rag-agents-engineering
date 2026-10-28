"""Depth-independent resource resolution for the RAG curriculum.

Why this exists
---------------
The canonical lessons in this repository must not depend on fragile ``../../``
paths or on which directory the kernel happened to start in. They must still be
able to reach the shared corpora under ``data/sample/`` and the few module
assets that live next to a single module.

This module reconciles the two: notebooks ask for a resource by name, and the
resolver finds it relative to the repository root regardless of notebook depth
or kernel working directory.

Usage
-----
    from rag_paths import repo_root, asset, ASSET_ROOTS

    repo_root()                    # -> Path to the repository root
    asset("Transformer.pdf")       # -> resolved Path, searched across roots
    asset("bella_vista.txt")

Bootstrapping from a notebook (the module is not an installed package)::

    import sys, pathlib
    p = pathlib.Path.cwd()
    while not (p / "src/rag_paths.py").is_file() and p != p.parent:
        p = p.parent
    sys.path.insert(0, str(p / "src"))

Note on module-name collisions
------------------------------
This module is deliberately named ``rag_paths`` rather than ``utils`` or
``helpers`` so it can never shadow, or be shadowed by, the repository's
installed ``helpers`` package or a module-local ``utils.py``.
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["repo_root", "asset", "curriculum_root", "ASSET_ROOTS", "find_all"]

# Lessons live under course/ in this repository.
CURRICULUM_REL = "course"

# A directory is the repository root if it contains all of these.
_ROOT_MARKERS = ("src/rag_paths.py", "pyproject.toml")


def repo_root(start: Path | str | None = None) -> Path:
    """Walk upward from *start* (default: cwd) until the repository root is found.

    Falls back to this file's own location, which is always one level below
    the root, so the resolver still works if the kernel is started somewhere
    unexpected.
    """
    candidates = []
    if start is not None:
        candidates.append(Path(start).resolve())
    candidates.append(Path.cwd().resolve())
    candidates.append(Path(__file__).resolve())

    for candidate in candidates:
        current = candidate if candidate.is_dir() else candidate.parent
        while True:
            if all((current / marker).exists() for marker in _ROOT_MARKERS):
                return current
            if current == current.parent:
                break
            current = current.parent

    # __file__ is <root>/src/rag_paths.py
    return Path(__file__).resolve().parents[1]


def curriculum_root(start: Path | str | None = None) -> Path:
    """Return the ``modules/`` directory that holds the lessons."""
    return repo_root(start) / CURRICULUM_REL


# Search order for `asset()`. `data/sample/` holds the corpora shared by several
# modules, so it comes first; the remaining roots hold assets used by one module.
ASSET_ROOTS: tuple[str, ...] = (
    "data/sample",
    "data/sample/rag_techniques",
    "course/p05_ingestion_and_indexing/m13_chunking/assets",
)


def find_all(name: str, start: Path | str | None = None) -> list[Path]:
    """Return every match for *name* across ``ASSET_ROOTS``, in search order.

    Useful when two roots hold same-named files: a filename match does not
    mean the files are interchangeable, so a lesson that cares can inspect all
    candidates before choosing.
    """
    root = repo_root(start)
    return [p for r in ASSET_ROOTS if (p := root / r / name).exists()]


def asset(name: str, start: Path | str | None = None) -> Path:
    """Resolve a shared input asset by filename.

    Raises ``FileNotFoundError`` listing the roots that were searched, rather
    than silently substituting a different document.
    """
    matches = find_all(name, start)
    if matches:
        return matches[0]
    root = repo_root(start)
    searched = "\n".join(f"  - {root / r}" for r in ASSET_ROOTS)
    raise FileNotFoundError(
        f"Asset {name!r} not found. Searched these roots:\n{searched}\n"
        "Add its directory to rag_paths.ASSET_ROOTS or copy the file into "
        "data/sample/."
    )
