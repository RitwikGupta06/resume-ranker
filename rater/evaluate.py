import csv
from collections import defaultdict
from collections.abc import Sequence
from pathlib import Path

import numpy as np


def dcg(grades: Sequence[float]) -> float:
    g = np.asarray(grades, dtype=float)
    return float(np.sum((2**g - 1) / np.log2(np.arange(2, len(g) + 2))))


def ndcg_at_k(ranked_grades: Sequence[float], k: int) -> float:
    ideal = dcg(sorted(ranked_grades, reverse=True)[:k])
    return dcg(ranked_grades[:k]) / ideal if ideal > 0 else 0.0


def precision_at_k(ranked_grades: Sequence[float], k: int, threshold: int = 2) -> float:
    # grade >= 2 counts as relevant on the 0-3 scale
    top = ranked_grades[:k]
    return sum(g >= threshold for g in top) / k if k else 0.0


def load_labels(path: str | Path) -> dict[str, dict[str, int]]:
    """labels csv (jd_id, resume_id, grade) -> {jd_id: {resume_id: grade}}"""
    labels: dict[str, dict[str, int]] = defaultdict(dict)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            labels[row["jd_id"]][row["resume_id"]] = int(row["grade"])
    return dict(labels)
