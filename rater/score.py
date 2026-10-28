import re

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_token = re.compile(r"[a-z0-9+#.]+")


def tokenize(text: str) -> list[str]:
    return [t.strip(".") for t in _token.findall(text.lower()) if t.strip(".")]


def tfidf_scores(jd: str, docs: list[str]) -> np.ndarray:
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    mat = vec.fit_transform([jd, *docs])
    return cosine_similarity(mat[0], mat[1:]).ravel()


def bm25_scores(jd: str, docs: list[str]) -> np.ndarray:
    bm25 = BM25Okapi([tokenize(d) for d in docs])
    return np.asarray(bm25.get_scores(tokenize(jd)), dtype=float)


def skill_overlap(jd_skills: set[str], resume_skills: set[str]) -> float:
    if not jd_skills:
        return 0.0
    return len(jd_skills & resume_skills) / len(jd_skills)


def minmax(x: np.ndarray) -> np.ndarray:
    span = x.max() - x.min() if len(x) else 0
    if span == 0:
        return np.zeros_like(x, dtype=float)
    return (x - x.min()) / span
