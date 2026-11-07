"""Offline helpers shared by the module lab solutions: the Larkspur corpus, retrieval metrics and a TF-IDF baseline.

    import sys; sys.path.insert(0, str(Path("../../../../src").resolve()))
    from lab_kit import baseline, load_handbook, load_jsonl, hit_rate, recall_at_k, mrr

Golden evidence is a text span, not a chunk id: a retrieved chunk is a hit when it contains a span
after lower-casing and collapsing whitespace, so any chunker can be scored. Metric functions take
`results`, a map from question id to retrieved chunk texts in rank order, and skip golden questions
with no spans (the out-of-corpus ones).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from sklearn.feature_extraction.text import TfidfVectorizer


def load_jsonl(path: str | Path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def load_handbook(path: str | Path) -> list[dict]:
    """One {"source", "title", "text"} per Markdown file, sorted by file name; text is the body after the H1."""
    out = []
    for p in sorted(Path(path).glob("*.md")):
        head, _, body = p.read_text().partition("\n")
        out.append({"source": p.name, "title": head.removeprefix("# ").strip(), "text": body.strip()})
    return out


def normalise(text: str) -> str:
    return " ".join(text.lower().split())


def is_hit(chunk: str, spans: list[str]) -> bool:
    chunk = normalise(chunk)
    return any(normalise(s) in chunk for s in spans)


def _scored(golden: list[dict]) -> list[dict]:
    return [g for g in golden if g["evidence_spans"]]


def hit_rate(results: dict[str, list[str]], golden: list[dict]) -> float:
    """Share of questions with at least one hit among the retrieved chunks."""
    gs = _scored(golden)
    return sum(any(is_hit(c, g["evidence_spans"]) for c in results.get(g["id"], [])) for g in gs) / len(gs)


def recall_at_k(results: dict[str, list[str]], golden: list[dict]) -> float:
    """Share of a question's spans found in any retrieved chunk, averaged over questions."""
    gs = _scored(golden)
    return sum(
        sum(any(is_hit(c, [s]) for c in results.get(g["id"], [])) for s in g["evidence_spans"]) / len(g["evidence_spans"])
        for g in gs
    ) / len(gs)


def mrr(results: dict[str, list[str]], golden: list[dict]) -> float:
    """Mean reciprocal rank of the first hit; 0 for a question with no hit."""
    gs = _scored(golden)
    total = 0.0
    for g in gs:
        rank = next((i for i, c in enumerate(results.get(g["id"], []), 1) if is_hit(c, g["evidence_spans"])), None)
        total += 1 / rank if rank else 0.0
    return total / len(gs)


def tfidf_retriever(chunks: list[str], k: int = 4) -> Callable[[str], list[str]]:
    """Top-k chunks by TF-IDF cosine similarity (English stop words, as in the RAG lifecycle top-k lab); zero scores are dropped."""
    vec = TfidfVectorizer(stop_words="english")
    matrix = vec.fit_transform(chunks)

    def search(query: str) -> list[str]:
        scores = (matrix @ vec.transform([query]).T).toarray().ravel()
        order = sorted(range(len(chunks)), key=lambda i: -scores[i])[:k]
        return [chunks[i] for i in order if scores[i] > 0]

    return search


def baseline(corpus_dir: str | Path, k: int = 4, chunk_size: int = 500, chunk_overlap: int = 50) -> dict:
    """Recursive split plus TF-IDF top-k over <corpus_dir>/handbook, scored on <corpus_dir>/golden.jsonl."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    corpus_dir = Path(corpus_dir)
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = [c for page in load_handbook(corpus_dir / "handbook") for c in splitter.split_text(page["text"])]
    golden = load_jsonl(corpus_dir / "golden.jsonl")
    search = tfidf_retriever(chunks, k)
    results = {g["id"]: search(g["question"]) for g in golden}
    return {"k": k, "n": len(_scored(golden)), "hit_rate": hit_rate(results, golden),
            "recall_at_k": recall_at_k(results, golden), "mrr": mrr(results, golden)}


if __name__ == "__main__":
    print(baseline(Path(__file__).resolve().parent.parent / "data/larkspur"))
