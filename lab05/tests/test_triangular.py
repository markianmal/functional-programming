from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st
import pytest
from streams import take
from triangular_numbers import (
    triangular_differences,
    triangular_stream,
    triangular_stream_gen,
    triangular_up_to,
)


def test_triangular_stream_values() -> None:
    expected = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
    assert take(10, triangular_stream()) == expected


def test_triangular_generators_parity() -> None:
    assert take(30, triangular_stream()) == take(30, triangular_stream_gen())


def test_triangular_up_to() -> None:
    res = list(triangular_up_to(40))
    assert res == [1, 3, 6, 10, 15, 21, 28, 36]
    assert list(triangular_up_to(0)) == []


def test_triangular_differences() -> None:
    data = [1, 3, 6, 10, 15]
    assert list(triangular_differences(data)) == [2, 3, 4, 5]


def test_triangular_differences_empty_and_single() -> None:
    assert list(triangular_differences([])) == []
    assert list(triangular_differences([1])) == []


def test_triangular_laziness() -> None:
    eval_count = 0

    def monitored_generator():
        nonlocal eval_count
        total = 0
        n = 1
        while True:
            eval_count += 1
            total += n
            yield total
            n += 1

    gen = monitored_generator()
    first_5 = take(5, gen)
    assert first_5 == [1, 3, 6, 10, 15]
    assert eval_count == 5


def test_triangular_differences_property() -> None:
    triangles = take(15, triangular_stream())
    diffs = list(triangular_differences(triangles))
    expected = list(range(2, 17))
    assert diffs == expected


@given(st.integers(min_value=1, max_value=50))
def test_triangular_closed_form_property(n: int) -> None:
    # Перевірка формули T_n = n * (n + 1) // 2
    seq = take(n, triangular_stream())
    expected = n * (n + 1) // 2
    assert seq[-1] == expected