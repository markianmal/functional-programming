from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st
from core import pipeline
from models import CourseRank


@given(st.integers())
def test_property_pipeline_associativity(x: int) -> None:
    f1 = lambda v: v + 2
    f2 = lambda v: v * 3
    assert pipeline(x, f1, f2) == (x + 2) * 3


@given(st.floats(min_value=1.0, max_value=5.0), st.integers(min_value=0, max_value=10000))
def test_property_course_total_ordering(rating: float, students: int) -> None:
    c1 = CourseRank("C1", "dev", students, rating, 10.0)
    c2 = CourseRank("C2", "dev", students + 1, rating, 10.0)
    assert c2 > c1