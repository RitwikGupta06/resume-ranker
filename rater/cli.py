import argparse
import csv
import sys
from pathlib import Path

import numpy as np

from rater.evaluate import load_labels, ndcg_at_k, precision_at_k
from rater.parse import extract_text, load_folder
from rater.rank import METHODS, rank


def cmd_rank(args: argparse.Namespace) -> int:
    jd = extract_text(args.jd)
    resumes = load_folder(args.resumes)
    if not resumes:
        print(f"no resumes found in {args.resumes}", file=sys.stderr)
        return 1

    results = rank(jd, resumes, method=args.method)[: args.top]
    for i, r in enumerate(results, 1):
        print(f"{i:>2}. {r.name:<30} {r.score:.3f}")
        print(f"    matched: {', '.join(r.matched) or '-'}")
        print(f"    missing: {', '.join(r.missing) or '-'}")

    if args.out:
        with open(args.out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["rank", "name", "score", "matched", "missing"])
            for i, r in enumerate(results, 1):
                w.writerow([i, r.name, f"{r.score:.4f}", ";".join(r.matched), ";".join(r.missing)])
        print(f"\nwrote {args.out}")
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    """Expects <dir>/jds/<jd_id>.txt, <dir>/resumes/*, and <dir>/labels.csv"""
    root = Path(args.data)
    labels = load_labels(root / "labels.csv")
    resumes = load_folder(root / "resumes")

    for method in args.methods:
        ndcgs, precs = [], []
        for jd_id, graded in labels.items():
            jd = extract_text(root / "jds" / f"{jd_id}.txt")
            pool = {name: resumes[name] for name in graded if name in resumes}
            ranked = rank(jd, pool, method=method)
            grades = [graded[r.name] for r in ranked]
            ndcgs.append(ndcg_at_k(grades, args.k))
            precs.append(precision_at_k(grades, args.k))
        print(f"{method:<8} ndcg@{args.k}={np.mean(ndcgs):.3f}  p@{args.k}={np.mean(precs):.3f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="resume-ranker")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("rank", help="rank a folder of resumes against a JD")
    r.add_argument("--jd", required=True)
    r.add_argument("--resumes", required=True)
    r.add_argument("--method", choices=METHODS, default="hybrid")
    r.add_argument("--top", type=int, default=10)
    r.add_argument("--out", help="write the shortlist to a csv")
    r.set_defaults(func=cmd_rank)

    e = sub.add_parser("eval", help="score methods against labeled data")
    e.add_argument("--data", required=True)
    e.add_argument("--k", type=int, default=10)
    e.add_argument("--methods", nargs="+", choices=METHODS, default=list(METHODS))
    e.set_defaults(func=cmd_eval)

    args = p.parse_args(argv)
    return int(args.func(args))
