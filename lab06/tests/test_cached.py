from __future__ import annotations

from decorators import cached


def test_cached_basic_hit_miss() -> None:
    calls = 0

    @cached()
    def square(x: int) -> int:
        nonlocal calls
        calls += 1
        return x * x

    assert square(4) == 16
    assert square(4) == 16
    assert calls == 1
    assert square.cache_info() == {"hits": 1, "misses": 1}


def test_cached_ttl_expiry() -> None:
    curr_time = 1000.0

    @cached(ttl=5.0, time_fn=lambda: curr_time)
    def compute(x: int) -> int:
        return x * 10

    assert compute(2) == 20
    assert compute(2) == 20
    assert compute.cache_info() == {"hits": 1, "misses": 1}

    curr_time += 6.0
    assert compute(2) == 20
    assert compute.cache_info() == {"hits": 1, "misses": 2}


def test_cached_clear() -> None:
    @cached()
    def f(x: int) -> int:
        return x + 1

    f(1)
    f(1)
    assert f.cache_info()["hits"] == 1
    f.cache_clear()
    assert f.cache_info() == {"hits": 0, "misses": 0}
    f(1)
    assert f.cache_info() == {"hits": 0, "misses": 1}


def test_cached_invalidate_predicate() -> None:
    @cached()
    def get_data(k: str, mode: str = "fast") -> str:
        return f"{k}:{mode}"

    get_data("u1", mode="fast")
    get_data("u2", mode="fast")
    get_data("u1", mode="slow")

    removed = get_data.cache_invalidate(lambda args, kw: args[0] == "u1")
    assert removed == 2


def test_cached_kwargs_support() -> None:
    calls = 0

    @cached()
    def op(a: int, b: int = 0) -> int:
        nonlocal calls
        calls += 1
        return a + b

    assert op(1, b=2) == 3
    assert op(1, b=2) == 3
    assert calls == 1