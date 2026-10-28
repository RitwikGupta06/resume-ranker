from dataclasses import dataclass, field

import numpy as np

from rater.score import bm25_scores, minmax, skill_overlap, tfidf_scores
from rater.skills import extract_skills

METHODS = ("tfidf", "bm25", "hybrid")

# hand-picked for now, the learned ranker should replace these in phase 4
HYBRID_WEIGHTS = {"bm25": 0.4, "tfidf": 0.2, "skills": 0.4}


@dataclass
class Result:
    name: str
    score: float
    matched: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)


def rank(jd: str, resumes: dict[str, str], method: str = "hybrid") -> list[Result]:
    if method not in METHODS:
        raise ValueError(f"method must be one of {METHODS}")
    if not resumes:
        return []

    names = list(resumes)
    docs = [resumes[n] for n in names]
    jd_skills = extract_skills(jd)
    cand_skills = [extract_skills(d) for d in docs]

    if method == "tfidf":
        scores = tfidf_scores(jd, docs)
    elif method == "bm25":
        scores = bm25_scores(jd, docs)
    else:
        overlap = np.array([skill_overlap(jd_skills, s) for s in cand_skills])
        w = HYBRID_WEIGHTS
        # bm25 isn't bounded so it gets squashed to 0-1 within the batch
        scores = (
            w["bm25"] * minmax(bm25_scores(jd, docs))
            + w["tfidf"] * tfidf_scores(jd, docs)
            + w["skills"] * overlap
        )

    results = [
        Result(
            name=n,
            score=float(s),
            matched=sorted(jd_skills & cs),
            missing=sorted(jd_skills - cs),
        )
        for n, s, cs in zip(names, scores, cand_skills, strict=True)
    ]
    return sorted(results, key=lambda r: r.score, reverse=True)
