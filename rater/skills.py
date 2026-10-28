import re
from functools import lru_cache
from importlib import resources


@lru_cache(maxsize=1)
def load_skills() -> dict[str, str]:
    """alias -> canonical skill name, from rater/data/skills.txt.

    Each line is `canonical | alias | alias ...`. Swap this for ESCO/O*NET later.
    """
    text = resources.files("rater").joinpath("data/skills.txt").read_text(encoding="utf-8")
    lookup = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        names = [n.strip().lower() for n in line.split("|")]
        for n in names:
            lookup[n] = names[0]
    return lookup


@lru_cache(maxsize=1)
def _pattern() -> re.Pattern[str]:
    # longest first so "machine learning" wins over "learning"-style partial hits
    aliases = sorted(load_skills(), key=len, reverse=True)
    # plain \b breaks on things like c++ and c#, so use lookarounds instead
    alt = "|".join(re.escape(a) for a in aliases)
    return re.compile(rf"(?<![\w+#])(?:{alt})(?![\w+#])", re.IGNORECASE)


def extract_skills(text: str) -> set[str]:
    lookup = load_skills()
    return {lookup[m.group(0).lower()] for m in _pattern().finditer(text)}
