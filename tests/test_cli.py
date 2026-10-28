import csv
from pathlib import Path

from rater.cli import main

EXAMPLES = Path(__file__).parent.parent / "examples"


def test_rank_writes_csv(tmp_path, capsys):
    out = tmp_path / "shortlist.csv"
    code = main(
        [
            "rank",
            "--jd",
            str(EXAMPLES / "jds/ml_intern.txt"),
            "--resumes",
            str(EXAMPLES / "resumes"),
            "--out",
            str(out),
        ]
    )
    assert code == 0
    rows = list(csv.DictReader(out.open()))
    assert len(rows) == 4 and rows[0]["rank"] == "1"


def test_eval_runs(capsys):
    assert main(["eval", "--data", str(EXAMPLES), "--k", "3"]) == 0
    assert "ndcg@3" in capsys.readouterr().out
