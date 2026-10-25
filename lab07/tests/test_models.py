from __future__ import annotations

from models import CourseRank


def test_total_ordering_equality() -> None:
    c1 = CourseRank("Python", "dev", 100, 4.8, 10.0)
    c2 = CourseRank("Python", "dev", 100, 4.8, 10.0)
    assert c1 == c2


def test_total_ordering_comparisons() -> None:
    c_high = CourseRank("Course A", "dev", 1000, 4.9, 20.0)
    c_low = CourseRank("Course B", "dev", 1000, 4.7, 20.0)
    assert c_high > c_low
    assert c_low < c_high
    assert c_high >= c_low
    assert c_low <= c_high


def test_total_ordering_sorting() -> None:
    courses = [
        CourseRank("B", "it", 100, 4.5, 10),
        CourseRank("A", "it", 100, 4.9, 10),
        CourseRank("C", "it", 200, 4.5, 10),
    ]
    ranked = sorted(courses, reverse=True)
    assert [c.title for c in ranked] == ["A", "C", "B"]


def test_total_ordering_not_implemented() -> None:
    c = CourseRank("Test", "it", 10, 4.5, 10)
    assert c.__eq__("not a course") is NotImplemented
    assert c.__lt__("not a course") is NotImplemented