from __future__ import annotations

import pytest
from decorators import timed


def test_timed_logging_ms() -> None:
    ticks = [10.0, 10.015]
    logs: list[str] = []

    @timed("calc", unit="ms", logger=logs.append, clock=lambda: ticks.pop(0))
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5
    assert len(logs) == 1
    assert "calc took 15.000 ms" in logs[0]


def test_timed_exception_logging() -> None:
    ticks = [0.0, 0.005]
    logs: list[str] = []

    @timed("failing", unit="s", logger=logs.append, clock=lambda: ticks.pop(0))
    def fail():
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        fail()
    assert len(logs) == 1
    assert "failing took 0.005 s" in logs[0]


def test_timed_metadata_preserved() -> None:
    @timed()
    def my_func():
        """Docstring."""
        pass

    assert my_func.__name__ == "my_func"
    assert my_func.__doc__ == "Docstring."
    assert hasattr(my_func, "__wrapped__")