import pytest

from rater.evaluate import load_labels, ndcg_at_k, precision_at_k


def test_ndcg_perfect():
    assert ndcg_at_k([3, 2, 1, 0], k=4) == pytest.approx(1.0)


def test_ndcg_worse_when_reversed():
    assert ndcg_at_k([0, 1, 2, 3], k=4) < 0.6


def test_ndcg_all_zero():
    assert ndcg_at_k([0, 0, 0], k=3) == 0.0


def test_precision():
    assert precision_at_k([3, 0, 2, 1], k=2) == 0.5


def test_load_labels(tmp_path):
    f = tmp_path / "labels.csv"
    f.write_text("jd_id,resume_id,grade\nj1,r1,3\nj1,r2,0\n")
    assert load_labels(f) == {"j1": {"r1": 3, "r2": 0}}
