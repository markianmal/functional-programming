from __future__ import annotations

import pytest
from decorators import retries


def test_retries_success_immediate() -> None:
    calls = 0

    @retries(attempts=3)
    def ok():
        nonlocal calls
        calls += 1
        return "done"

    assert ok() == "done"
    assert calls == 1


def test_retries_success_after_failure() -> None:
    calls = 0
    slept: list[float] = []

    @retries(attempts=4, delay=0.1, backoff=2.0, sleep=slept.append)
    def flaky():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise ConnectionError("drop")
        return "recovered"

    assert flaky() == "recovered"
    assert calls == 3
    assert slept == [0.1, 0.2]


def test_retries_failure_all_attempts() -> None:
    calls = 0
    slept: list[float] = []

    @retries(attempts=3, delay=0.05, sleep=slept.append)
    def bad():
        nonlocal calls
        calls += 1
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError, match="fail"):
        bad()
    assert calls == 3
    assert len(slept) == 2


def test_retries_non_matching_exception() -> None:
    @retries(attempts=3, exceptions=(ValueError,))
    def raise_type_err():
        raise TypeError("wrong type")

    with pytest.raises(TypeError):
        raise_type_err()