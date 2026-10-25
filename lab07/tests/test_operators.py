from __future__ import annotations

from operator import attrgetter, itemgetter, methodcaller
from models import CourseRank


def test_itemgetter_single_and_multi() -> None:
    d = {"title": "Python", "rating": 4.9, "students": 1000}
    assert itemgetter("title")(d) == "Python"
    assert itemgetter("rating", "students")(d) == (4.9, 1000)


def test_attrgetter_usage() -> None:
    c = CourseRank("DevOps", "cloud", 500, 4.7, 30.0)
    assert attrgetter("title")(c) == "DevOps"
    assert attrgetter("category", "rating")(c) == ("cloud", 4.7)


def test_methodcaller_usage() -> None:
    assert methodcaller("strip")("   spaced   ") == "spaced"
    assert methodcaller("replace", "old", "new")("old text") == "new text"