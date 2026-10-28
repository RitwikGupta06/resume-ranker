from pathlib import Path

import pytest

from rater.parse import extract_text, load_folder
from rater.rank import METHODS, rank

EXAMPLES = Path(__file__).parent.parent / "examples"


@pytest.fixture
def data():
    return extract_text(EXAMPLES / "jds/ml_intern.txt"), load_folder(EXAMPLES / "resumes")


@pytest.mark.parametrize("method", METHODS)
def test_frontend_dev_ranks_last(data, method):
    jd, resumes = data
    assert rank(jd, resumes, method)[-1].name == "sam_ortiz"


def test_matched_and_missing(data):
    jd, resumes = data
    sam = next(r for r in rank(jd, resumes) if r.name == "sam_ortiz")
    assert "git" in sam.matched
    assert "pytorch" in sam.missing


def test_empty():
    assert rank("python", {}) == []


def test_bad_method():
    with pytest.raises(ValueError):
        rank("python", {"a": "python"}, method="magic")
