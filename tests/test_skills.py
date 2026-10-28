from rater.skills import extract_skills


def test_aliases_map_to_canonical():
    assert extract_skills("used sklearn and k8s") == {"scikit-learn", "kubernetes"}


def test_symbols():
    assert {"c++", "c#"} <= extract_skills("Wrote C++ and C# code")


def test_no_partial_words():
    # "java" shouldn't fire inside "javascript", "go" isn't a skill on its own
    assert extract_skills("javascript, let's go") == {"javascript"}


def test_multiword_preferred():
    assert "machine learning" in extract_skills("Machine Learning projects")
