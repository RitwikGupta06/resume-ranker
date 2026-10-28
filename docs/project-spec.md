# resume-ranker: Resume Rater & JD Matcher

> Rank resumes against a job description, with reasons, using only local models.

**Author:** Ritwik Gupta · **Status:** Phase 1 in progress · **Target date:** Late December 2026 (1-2 months from 2026-10-28)

---

## 1. Problem and goal

- **Problem:** Recruiters spend hours manually screening resumes against a job description (JD).
- **Goal:** Rank uploaded resumes against a JD and shortlist the top candidates, with reasons, using only local models (no LLM API, no API keys).
- **Primary audience for this project:** Internship recruiters reading my resume
- **Framing:** A ranking assistant with a human in the loop, not an automated hiring decision-maker.

## 2. Scope

### MVP (must have)
- [ ] Upload a JD (text or PDF) and multiple resumes (PDF/DOCX)
- [ ] Parse resumes into text and extract skills, experience, education
- [ ] Score and rank resumes against the JD
- [ ] Show matched and missing skills per candidate
- [ ] Export the shortlist as CSV

### Stretch (nice to have)
- [ ] Learned ranker (LightGBM) trained on labeled pairs
- [ ] SHAP explanations
- [ ] Blind mode (strip names/gender cues) plus a bias test
- [ ] Recruiter feedback loop (thumbs up/down) with periodic retraining
- [ ] Async batch uploads (Celery + Redis) for many resumes at once

### Out of scope
- Automated hiring decisions
- Any external LLM API
- {{OUT_OF_SCOPE}}

## 3. ML design

| Component | Choice |
| --- | --- |
| Resume parsing | PyMuPDF + python-docx (Tesseract OCR fallback later) |
| Skill extraction | Hand-built alias list with regex matching to start, ESCO/O*NET taxonomy later |
| Lexical scorer | Both TF-IDF and BM25 (compared in the ablation) |
| Semantic scorer | all-MiniLM-L6-v2 (sentence-transformers) |
| Structured features | Skill overlap, years of experience, education level |
| Ranker | Weighted hybrid first, then LightGBM LGBMRanker |
| Explainability | {{EXPLAINABILITY}} |

### Evaluation
- **Dataset:** {{DATASET}}
- **Labeled pairs:** {{NUM_LABELED_PAIRS}} resume/JD pairs, labeled by {{LABELING_METHOD}}
- **Metrics:** NDCG@k, precision@k
- **Ablation:** TF-IDF vs BM25 vs embeddings vs hybrid vs learned ranker
- **Result table:** to fill after experiments
- **CI eval set:** small synthetic set committed to the repo (real resumes stay local)

## 4. Architecture and stack

| Layer | Choice |
| --- | --- |
| Language | Python 3.11+ |
| Backend | FastAPI |
| Frontend | React |
| Async jobs | Celery + Redis |
| Database | SQLite for MVP, Postgres later |
| Vector search | In-memory numpy for now, FAISS if it gets slow |
| Experiment tracking | JSON result files for now |

## 5. DevOps

- **Docker:** {{DOCKER_PLAN}} (multi-stage build, docker-compose)
- **CI (GitHub Actions):** ruff, mypy, pytest on every push/PR (live); image build + push to GHCR in phase 5
- **Repo:** github.com/RitwikGupta06/resume-ranker, PR-only merges to main, CI required
- **ML gate in CI:** fail the build if NDCG@10 drops below {{NDCG_THRESHOLD}}
- **CD:** deploy to HF Spaces on merge to main
- **Monitoring:** {{MONITORING}} (Prometheus + Grafana / basic logging)
- **Load test:** {{LOAD_TEST}} (Locust)

## 6. Hosting

- **Platform:** Hugging Face Spaces (Docker Space)
- **Domain:** {{DOMAIN}}
- **Constraints:** free tier, CPU only, small embedding model

## 7. Privacy and security

- Resumes contain personal data (PII).
- **Retention:** auto-delete after {{RETENTION_DAYS}} days
- **Auth:** {{AUTH}}
- **Rate limiting:** {{RATE_LIMIT}}

## 8. Timeline

| Phase | Deliverable | Target |
| --- | --- | --- |
| 1 | Parser + TF-IDF baseline + simple UI | Nov 11 (proposed) |
| 2 | Labeled eval set + metrics | Nov 18 (proposed) |
| 3 | Embeddings + hybrid + ablation table | Nov 28 (proposed) |
| 4 | LightGBM ranker + explanations | Dec 8 (proposed) |
| 5 | Docker + CI/CD + hosting | Dec 18 (proposed) |
| 6 | Batch jobs, feedback loop, monitoring, bias test | Dec 28 (proposed) |

## 9. Resume bullets (fill in after building)

- {{BULLET_1}}
- {{BULLET_2}}
- {{BULLET_3}}

## 10. Open questions

- {{OPEN_QUESTION_1}}
- {{OPEN_QUESTION_2}}
