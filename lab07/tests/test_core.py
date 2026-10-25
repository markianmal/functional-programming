from __future__ import annotations

from core import clean_and_rank_courses, filt, mapf, normalize_course, pipeline


def test_pipeline_reduce_execution() -> None:
    add_one = lambda x: x + 1
    double = lambda x: x * 2
    assert pipeline(3, add_one, double, add_one) == 9


def test_pipeline_empty_sequence() -> None:
    assert pipeline(42) == 42


def test_partial_mapf_and_filt() -> None:
    data = [1, 2, 3, 4, 5, 6]
    evens = list(filt(lambda x: x % 2 == 0)(data))
    squared = list(mapf(lambda x: x * x)(evens))
    assert squared == [4, 16, 36]


def test_clean_and_rank_filtering() -> None:
    rows = [
        {"title": "C1", "category": "it", "students": 100, "rating": 4.8, "price": 10},
        {"title": "C2", "category": "it", "students": 200, "rating": 4.1, "price": 10},
    ]
    ranked = clean_and_rank_courses(rows, min_rating=4.5, top=5)
    assert len(ranked) == 1
    assert ranked[0].title == "C1"


def test_clean_and_rank_sorting_order() -> None:
    rows = [
        {"title": "B", "category": "it", "students": 100, "rating": 4.8, "price": 10},
        {"title": "A", "category": "it", "students": 500, "rating": 4.8, "price": 10},
        {"title": "C", "category": "it", "students": 50, "rating": 4.9, "price": 10},
    ]
    ranked = clean_and_rank_courses(rows, min_rating=4.0, top=3)
    assert [c.title for c in ranked] == ["C", "A", "B"]