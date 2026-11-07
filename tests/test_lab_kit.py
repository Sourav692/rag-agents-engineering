"""Offline checks for the Larkspur corpus and golden set (data/larkspur/)."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LARKSPUR = ROOT / "data/larkspur"
TOPK_LAB = ROOT / ("theory/p04_rag_foundations/m11_rag_lifecycle/02_indexing_from_scratch_with_tf_idf_and_nearest_neighbours"
                   "/interactive/top-k-retrieval-lab.html")


def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def normalise(text):
    return " ".join(text.lower().split())


GOLD = load_jsonl(LARKSPUR / "golden.jsonl")
HANDBOOK = normalise(" ".join(p.read_text() for p in sorted((LARKSPUR / "handbook").glob("*.md"))))


def test_golden_shape():
    assert len(GOLD) == 30
    assert [g["id"] for g in GOLD] == [f"g{i:02d}" for i in range(1, 31)]
    assert Counter(g["type"] for g in GOLD) == {"lookup": 15, "multi_hop": 6, "numeric": 4, "out_of_corpus": 5}


def test_golden_spans_are_in_the_handbook():
    for g in GOLD:
        assert (g["type"] == "out_of_corpus") == (not g["evidence_spans"]), g["id"]
        for s in g["evidence_spans"]:
            assert normalise(s) in HANDBOOK, (g["id"], s)


def test_multi_hop_spans_come_from_two_files():
    files = {p.name: normalise(p.read_text()) for p in (LARKSPUR / "handbook").glob("*.md")}
    for g in GOLD:
        if g["type"] == "multi_hop":
            hit = {name for name, text in files.items() for s in g["evidence_spans"] if normalise(s) in text}
            assert len(hit) >= 2, (g["id"], hit)


def test_handbook_files_start_with_a_title():
    pages = sorted((LARKSPUR / "handbook").glob("*.md"))
    assert 12 <= len(pages) <= 15
    for p in pages:
        assert p.read_text().startswith("# "), p.name


def test_top_k_lab_chunks_are_in_the_handbook():
    chunks = re.findall(r'^\["[\w-]+","(.+?)"\]', TOPK_LAB.read_text(), re.M)
    assert len(chunks) == 12
    for c in chunks:
        assert normalise(c) in HANDBOOK, c
    assert [g["question"] for g in GOLD[:3]] == [
        "How long does a refund take?", "What happens if my server goes down?", "Can I export my data after I cancel my plan?"]
