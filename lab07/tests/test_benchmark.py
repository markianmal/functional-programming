from __future__ import annotations

import timeit
from core import clean_and_rank_courses
from loaders import load_courses


def test_benchmark_pipeline() -> None:
    data = [{"title": f"Course_{i}", "category": "IT", "students": i, "rating": 4.0 + (i % 10) / 10, "price": 10} for i in range(100)]
    t = timeit.timeit(lambda: clean_and_rank_courses(data, min_rating=4.5, top=5), number=50)
    assert t < 1.0


def test_benchmark_loaders() -> None:
    raw = '[{"title": "C", "category": "IT", "students": 10, "rating": 4.8, "price": 10}]'
    t = timeit.timeit(lambda: load_courses(raw), number=100)
    assert t < 0.5