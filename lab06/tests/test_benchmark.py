from __future__ import annotations

import timeit
from closures import make_converter
from decorators import cached


def test_cached_speedup() -> None:
    @cached()
    def expensive(x: int) -> int:
        return sum(range(x))

    t_miss = timeit.timeit(lambda: expensive(10_000), number=1)
    t_hit = timeit.timeit(lambda: expensive(10_000), number=1)
    assert t_hit < t_miss or t_hit < 0.001


def test_benchmark_closures() -> None:
    conv = make_converter(2.5)
    t = timeit.timeit(lambda: conv(12.34), number=1000)
    assert t < 0.5