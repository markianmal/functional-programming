from __future__ import annotations

from closures import make_converter
from decorators import cached, count_calls, timed


def test_data_converter_caching() -> None:
    converter = make_converter(scale=1.60934, precision=2)
    evals = 0

    @cached(ttl=10.0)
    def convert_distance(miles: float) -> float:
        nonlocal evals
        evals += 1
        return converter(miles)

    assert convert_distance(10.0) == 16.09
    assert convert_distance(10.0) == 16.09
    assert evals == 1
    assert convert_distance.cache_info() == {"hits": 1, "misses": 1}


def test_count_calls_decorator() -> None:
    @count_calls()
    def fn(a: int) -> int:
        return a * 2

    assert fn.calls() == 0
    fn(1)
    fn(2)
    assert fn.calls() == 2
    fn.reset()
    assert fn.calls() == 0


def test_composition_cached_count_timed() -> None:
    logs: list[str] = []

    @timed("pipeline", logger=logs.append)
    @count_calls()
    @cached()
    def parse_item(raw_id: int) -> str:
        return f"ITEM_{raw_id}"

    assert parse_item(101) == "ITEM_101"
    assert parse_item(101) == "ITEM_101"
    assert parse_item.calls() == 2
    assert len(logs) == 2


def test_wraps_metadata_preserved() -> None:
    @count_calls()
    def func_with_doc(x: int) -> int:
        """Документація функції."""
        return x + 5

    assert func_with_doc.__name__ == "func_with_doc"
    assert func_with_doc.__doc__ == "Документація функції."
    assert hasattr(func_with_doc, "__wrapped__")