"""Regenerate course/, src/, data/ and docs/source/ from the four source repositories.

The source repos are canonical (option B in CLAUDE.md). Never edit generated files here:
fix the notebook in its source repo, pull it, and re-run this script.

    uv run python scripts/migrate.py --sources ..          # rebuild
    uv run python scripts/migrate.py --sources .. --check  # validate only, write nothing

`--sources` is the folder holding clones of the four source repos, named as in
curriculum.yaml (`sources.<key>.repo`).
"""
from __future__ import annotations

import argparse
import csv
import filecmp
import posixpath
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

from curriculum_lib import COURSE_DIR, ROOT, items, load, module_dir, source_module, source_root

SKIP_DIRS = {".git", ".venv", ".ipynb_checkpoints", "__pycache__", ".pytest_cache", ".ruff_cache"}
# Folders regenerated on every run. Everything else in the repo is hand-maintained.
GENERATED = [".env.example", COURSE_DIR, "src/helpers", "src/rag_paths.py", "data",
             "docs/source", "docs/third_party", "docs/content-inventory.csv"]


def walk_notebooks(repo_root: Path):
    for p in repo_root.rglob("*.ipynb"):
        if not SKIP_DIRS & set(p.relative_to(repo_root).parts):
            yield p.relative_to(repo_root).as_posix()


def rewrite_notebook(text: str, repo: str, source_path: str) -> str:
    """Notebooks sit one folder deeper here (course/<part>/<module>/<folder>/ vs modules/<module>/notebooks/)."""
    if not source_path.startswith("modules/"):
        return text
    text = text.replace("../../../data/", "../../../../data/")
    text = text.replace("../../../src", "../../../../src")
    return text.replace("../../../docs/", f"../../../../docs/source/{repo}/")


RUN = re.compile(r"(%run\s+\\?['\"]?)([^'\"\s\\]+\.ipynb)")
LINK = re.compile(r"(\]\(|src=\\?[\"'])([^)\s\"'\\]+)")


class LinkMap:
    """Maps a source-repo path (modules/... or solutions/...) to its new path in this repo."""

    def __init__(self, its, repo_names: dict[str, str]):
        self.repo_names = repo_names
        self.items = {(it.repo, it.source_path): it.dest for it in its}
        votes = defaultdict(Counter)
        for it in its:
            if it.source_path.startswith("modules/"):
                votes[(it.repo, source_module(it.source_path))][module_dir(it.module)] += 1
        self.modules = {k: c.most_common(1)[0][0] for k, c in votes.items()}
        self.companions: dict[tuple[str, str], str] = {}

    def resolve(self, repo: str, path: str) -> str | None:
        if (repo, path) in self.items:
            return self.items[(repo, path)]
        if (repo, path) in self.companions:
            return self.companions[(repo, path)]
        parts = path.split("/")
        if parts[0] == "modules" and len(parts) >= 2 and (repo, parts[1]) in self.modules:
            dmod = self.modules[(repo, parts[1])]
            if len(parts) == 2 or parts[2:] == ["README.md"]:
                return f"{dmod}/README.md"
            if parts[2] == "assets":
                return "/".join([dmod, *parts[2:]])
        return None

    def fix(self, text: str, repo: str, source_path: str, dest: str, roots_too: bool = False) -> str:
        """Rewrite relative links from source-repo paths to course paths.

        Notebooks leave data/, docs/ and src/ links to rewrite_notebook (a plain depth shift);
        Markdown files pass roots_too=True and get those resolved here.
        """
        sdir, ddir = posixpath.dirname(source_path), posixpath.dirname(dest)

        def sub(m):
            target = m.group(2)
            if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|/)", target, re.I):
                return m.group(0)
            path, sep, anchor = target.partition("#")
            src = posixpath.normpath(posixpath.join(sdir, path))
            if src.startswith(".."):
                return m.group(0)
            if src.startswith(("data/", "docs/", "src/")) or src in ("data", "docs", "src"):
                if not roots_too:
                    return m.group(0)  # handled by the depth rewrite in rewrite_notebook
                new = f"docs/source/{repo}/{src[5:]}" if src.startswith("docs/") else src
            else:
                new = self.resolve(repo, src)
            if new is None and src.startswith(("modules/", "solutions/")):
                # not part of the course (e.g. a planned module): link to the source repo instead
                url = f"https://github.com/Sourav692/{self.repo_names[repo]}/tree/main/{src}"
                return m.group(1) + url + sep + anchor
            if new is None:
                return m.group(0)
            return m.group(1) + posixpath.relpath(new, ddir) + sep + anchor

        def sub_run(m):
            new = self.resolve(repo, posixpath.normpath(posixpath.join(sdir, m.group(2))))
            return m.group(0) if new is None else m.group(1) + posixpath.relpath(new, ddir)

        return RUN.sub(sub_run, LINK.sub(sub, text))


class Copier:
    """Copies files, refusing to overwrite a different file at the same destination."""

    def __init__(self, check: bool):
        self.check = check
        self.placed: dict[Path, Path] = {}
        self.conflicts: list[str] = []
        self.rows: list[dict] = []

    def copy(self, src: Path, dest: Path, row: dict | None = None, text_fn=None):
        if src.is_dir():
            for f in sorted(src.rglob("*")):
                if f.is_file() and not SKIP_DIRS & set(f.relative_to(src).parts):
                    self.copy(f, dest / f.relative_to(src), row and {**row, "kind": "folder file"})
            return
        prev = self.placed.get(dest)
        if prev is not None:
            if prev != src and not filecmp.cmp(prev, src, shallow=False):
                self.conflicts.append(f"{dest.relative_to(ROOT)}: {prev} vs {src}")
            return
        self.placed[dest] = src
        if row:
            self.rows.append({**row, "dest": dest.relative_to(ROOT).as_posix()})
        if self.check:
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        if text_fn:
            dest.write_text(text_fn(src.read_text()))
        else:
            shutil.copy2(src, dest)


def merged_env(cur: dict, roots: dict[str, Path]) -> str:
    """Union of the source repos' .env.example keys; each key keeps every repo's comment, tagged with the repo."""
    keys: dict[str, list[str]] = {}
    for k, root in roots.items():
        f = root / ".env.example"
        if not f.exists():
            continue
        comments: list[str] = []
        for line in f.read_text().splitlines():
            s = line.strip()
            if s.startswith("# ---") or not s:
                comments = []
            elif s.startswith("#"):
                comments.append(s.lstrip("# ").strip())
            elif "=" in s:
                name = s.split("=", 1)[0]
                note = " ".join(comments) or "(no comment in source)"
                keys.setdefault(name, []).append(f"# [{k}] {note}")
                comments = []
    out = ["# Copy to .env (never commit .env). Names only: fill in the values you need.",
           "# Generated by scripts/migrate.py from the source repos' .env.example files.",
           "# [05]/[06]/[08]/[09] say which source repo uses the key; module numbers in comments are",
           "# that repo's numbering;",
           "# docs/content-inventory.csv maps them to course modules. Most notebooks need only OPENAI_API_KEY.", ""]
    for name, notes in keys.items():
        out += notes + [f"{name}=", ""]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--sources", type=Path, default=ROOT.parent, help="folder holding the four source repo clones")
    ap.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = ap.parse_args()

    cur = load()
    its = items(cur)
    roots = {k: source_root(cur, args.sources, k) for k in cur["sources"]}
    errors = [f"source repo not found: {p}" for p in roots.values() if not p.is_dir()]
    if errors:
        print("\n".join(errors))
        return 1

    # 1. every source notebook is placed exactly once, and every placed source exists
    placed = Counter((it.repo, it.source_path) for it in its if it.is_notebook)
    for k, root in roots.items():
        for nb in walk_notebooks(root):
            if placed[(k, nb)] == 0:
                errors.append(f"not in curriculum.yaml: {k}:{nb}")
    errors += [f"placed {n} times: {k}:{p}" for (k, p), n in placed.items() if n > 1]
    errors += [f"missing in source: {it.repo}:{it.source_path}"
               for it in its if not (roots[it.repo] / it.source_path).exists()]
    dests = Counter(it.dest for it in its)
    errors += [f"two items share destination {d}" for d, n in dests.items() if n > 1]
    if errors:
        print("\n".join(errors))
        return 1

    if not args.check:
        for g in GENERATED:
            p = ROOT / g
            if p.is_dir():
                shutil.rmtree(p)
            elif p.exists():
                p.unlink()

    cp = Copier(args.check)
    item_paths = {(it.repo, it.source_path) for it in its}

    # 2. curriculum items, then the files that live beside them in the source folder
    companions: dict[tuple[str, str], set[str]] = defaultdict(set)
    for it in its:
        if it.is_notebook:
            companions[(it.repo, it.source_dir)].add(f"{module_dir(it.module)}/{it.folder}")
    links = LinkMap(its, {k: v["repo"] for k, v in cur["sources"].items()})
    for (repo, sdir), dest_dirs in companions.items():
        for f in (roots[repo] / sdir).iterdir():
            links.companions.setdefault((repo, f"{sdir}/{f.name}"), f"{sorted(dest_dirs)[0]}/{f.name}")
    for it in its:
        src = roots[it.repo] / it.source_path
        row = {"module": f"M{it.module['num']:02d}", "lesson": it.lesson_no, "tier": it.tier, "kind": "item",
               "source_repo": cur["sources"][it.repo]["repo"], "source_path": it.source_path}
        def fn(t, it=it):
            return rewrite_notebook(links.fix(t, it.repo, it.source_path, it.dest), it.repo, it.source_path)

        if not it.is_notebook:
            fn = None
        cp.copy(src, ROOT / it.dest, row, fn)
    for (repo, sdir), dest_dirs in sorted(companions.items()):
        for f in sorted((roots[repo] / sdir).iterdir()):
            rel = f"{sdir}/{f.name}"
            if f.suffix == ".ipynb" or f.name in SKIP_DIRS or (repo, rel) in item_paths:
                continue
            for d in sorted(dest_dirs):
                row = {"module": d.split("/")[2][:3].upper(), "lesson": "", "tier": "", "kind": "companion",
                       "source_repo": cur["sources"][repo]["repo"], "source_path": rel}
                cp.copy(f, ROOT / d / f.name, row)

    # 3. module assets: modules/<src>/assets -> <dest module>/assets
    src_mods: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for it in its:
        if it.source_path.startswith("modules/"):
            src_mods[module_dir(it.module)].add((it.repo, source_module(it.source_path)))
    asset_map: dict[str, str] = {}
    for dmod, srcs in sorted(src_mods.items()):
        for repo, smod in sorted(srcs):
            a = roots[repo] / "modules" / smod / "assets"
            if a.is_dir():
                asset_map[f"{repo}:modules/{smod}/assets"] = f"{dmod}/assets"
                cp.copy(a, ROOT / dmod / "assets", {"module": dmod.split("/")[2][:3].upper(), "lesson": "", "tier": "",
                                                    "kind": "asset", "source_repo": cur["sources"][repo]["repo"],
                                                    "source_path": f"modules/{smod}/assets"})

    # 4. shared code: src/helpers is identical in every repo that has it; rag_paths.py comes from 05
    helpers = [roots[k] / "src/helpers" for k in roots if (roots[k] / "src/helpers").is_dir()]
    for h in helpers[1:]:
        diff = filecmp.dircmp(helpers[0], h)
        if diff.diff_files or diff.left_only or diff.right_only:
            cp.conflicts.append(f"src/helpers differs between {helpers[0]} and {h}")
    if helpers:
        cp.copy(helpers[0], ROOT / "src/helpers")

    def patch_rag_paths(text: str) -> str:
        text = text.replace('CURRICULUM_REL = "modules"', f'CURRICULUM_REL = "{COURSE_DIR}"')
        text = text.replace("Lessons live under modules/", f"Lessons live under {COURSE_DIR}/")
        for src, dest in asset_map.items():
            if src.startswith("05:"):
                text = text.replace(f'"{src[3:]}"', f'"{dest}"')
        return text

    if (roots["05"] / "src/rag_paths.py").exists():
        cp.copy(roots["05"] / "src/rag_paths.py", ROOT / "src/rag_paths.py", text_fn=patch_rag_paths)

    # 5. data, licences and each source repo's docs (kept for provenance and for links from notebooks)
    for k, root in roots.items():
        for f in sorted((root / "data").rglob("*")) if (root / "data").is_dir() else []:
            if f.is_file() and f.name != "README.md":
                cp.copy(f, ROOT / "data" / f.relative_to(root / "data"))
        if (root / "data/README.md").exists():
            cp.copy(root / "data/README.md", ROOT / f"docs/source/{k}/data-README.md")
        if (root / "docs").is_dir():
            for f in sorted((root / "docs").iterdir()):
                if f.name == "third_party":
                    cp.copy(f, ROOT / "docs/third_party")
                else:
                    cp.copy(f, ROOT / f"docs/source/{k}/{f.name}")
        cp.copy(root / "LICENSE", ROOT / f"docs/source/{k}/LICENSE")

    # 6. Markdown copied into course/ links with source-repo paths too
    if not args.check:
        for dest, src in cp.placed.items():
            rel = dest.relative_to(ROOT).as_posix()
            if dest.suffix != ".md" or not rel.startswith(COURSE_DIR + "/"):
                continue
            repo = next(k for k, r in roots.items() if r in src.parents)
            src_rel = src.relative_to(roots[repo]).as_posix()
            dest.write_text(links.fix(dest.read_text(), repo, src_rel, rel, roots_too=True))

    if cp.conflicts:
        print("Conflicts (two different files want the same path):\n  " + "\n  ".join(cp.conflicts))
        return 1

    if not args.check:
        (ROOT / ".env.example").write_text(merged_env(cur, roots))
        with open(ROOT / "docs/content-inventory.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, ["dest", "module", "lesson", "tier", "kind", "source_repo", "source_path"])
            w.writeheader()
            w.writerows(sorted(cp.rows, key=lambda r: r["dest"]))

    nb = sum(1 for it in its if it.is_notebook)
    tiers = Counter(it.tier for it in its if it.is_notebook)
    print(f"{'checked' if args.check else 'migrated'}: {len(its)} items ({nb} notebooks: "
          + ", ".join(f"{n} {t}" for t, n in tiers.items()) + f"), {len(cp.placed)} files in total")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    sys.exit(main())
