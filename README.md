# resume-ranker

[![CI](https://github.com/RitwikGupta06/resume-ranker/actions/workflows/ci.yml/badge.svg)](https://github.com/RitwikGupta06/resume-ranker/actions/workflows/ci.yml)

Ranks a pile of resumes against a job description and shows why each one landed where it did:
which required skills matched and which are missing. Everything runs locally, no LLM APIs.

It's meant to help a recruiter get through a stack faster, not make the decision for them.

## Status

Phase 1 of 6: parsing, skill extraction, TF-IDF / BM25 / hybrid ranking, NDCG eval.
Embeddings, a learned ranker, the web UI and deployment are on the way. See the
[milestones](https://github.com/RitwikGupta06/resume-ranker/milestones) and
[project spec](docs/project-spec.md).

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# rank the sample resumes against the sample JD
python -m rater rank --jd examples/jds/ml_intern.txt --resumes examples/resumes --out shortlist.csv

# compare methods on labeled data
python -m rater eval --data examples --k 3
```

Resumes can be PDF, DOCX or TXT.

## How scoring works (for now)

| Method | What it does |
| --- | --- |
| `tfidf` | cosine similarity on TF-IDF vectors (unigrams + bigrams) |
| `bm25` | Okapi BM25 with the JD as the query |
| `hybrid` | 0.4 BM25 (min-max scaled) + 0.2 TF-IDF + 0.4 skill overlap |

Skill overlap is the share of JD skills found in the resume, using the list in
`rater/data/skills.txt` (aliases like `sklearn` -> `scikit-learn` are handled).

## Evaluation

Labels are graded 0-3 per (JD, resume) pair, see `data/labels.example.csv`.
Metrics are NDCG@k and precision@k (grade >= 2 counts as relevant).

Results table goes here once the labeled set is done.

## Data and privacy

Real resumes are personal data and are never committed. `data/` is gitignored apart from
the example labels file. Everything under `examples/` is made up.

## Layout

```
rater/        parsing, skills, scoring, ranking, eval, cli
tests/
examples/     fake JD + resumes + labels, used by tests and CI
docs/         project spec
```
