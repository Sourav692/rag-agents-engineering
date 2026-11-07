"""Offline checks for src/lab_kit.py and the Larkspur corpus and golden set (data/larkspur/)."""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from lab_kit import baseline, hit_rate, load_handbook, load_jsonl, mrr, normalise, recall_at_k, tfidf_retriever  # noqa: E402

LARKSPUR = ROOT / "data/larkspur"
TOPK_LAB = ROOT / ("p04_rag_foundations/m10_rag_lifecycle/mandatory/theory/02_indexing_from_scratch_with_tf_idf_and_nearest_neighbours"
                   "/interactive/top-k-retrieval-lab.html")


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


GOLDEN = [{"id": "q1", "evidence_spans": ["refunds take 5 days"]},
          {"id": "q2", "evidence_spans": ["status page"]},
          {"id": "q3", "evidence_spans": []}]
RESULTS = {"q1": ["Intro.", "Refunds take 5 days to clear."], "q2": ["Pricing."], "q3": ["x"]}


def test_metrics():
    assert hit_rate(RESULTS, GOLDEN) == 0.5
    assert recall_at_k(RESULTS, GOLDEN) == 0.5
    assert mrr(RESULTS, GOLDEN) == 0.25


def test_load_handbook():
    pages = load_handbook(LARKSPUR / "handbook")
    assert pages[0]["source"] == "01_billing.md" and pages[0]["title"] == "Billing and payments"
    assert not pages[0]["text"].startswith("#")


def test_tfidf_retriever_ranks_and_drops_zero_scores():
    search = tfidf_retriever(["Refunds take 5 days.", "The status page lists outages.", "Pricing."], k=2)
    assert search("status page outages") == ["The status page lists outages."]


def test_baseline_runs_offline():
    b = baseline(LARKSPUR)
    assert b["n"] == 25 and b["k"] == 4
    assert 0.0 <= b["hit_rate"] <= 1.0
