from __future__ import annotations

import timeit
from streams import fib_stream, take
from triangular_numbers import triangular_stream


def test_benchmark_streams() -> None:
    t = timeit.timeit(lambda: take(1000, fib_stream()), number=10)
    assert t < 1.0


def test_benchmark_triangular() -> None:
    t = timeit.timeit(lambda: take(1000, triangular_stream()), number=10)
    assert t < 1.0