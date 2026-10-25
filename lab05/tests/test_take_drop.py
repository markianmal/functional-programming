from __future__ import annotations

from itertools import count, islice
from hypothesis import given
from hypothesis import strategies as st
import pytest
from streams import drop, take


def test_take_basic() -> None:
    assert take(3, [1, 2, 3, 4, 5]) == [1, 2, 3]
    assert take(0, [1, 2, 3]) == []
    assert take(10, [1, 2]) == [1, 2]


def test_drop_basic() -> None:
    assert list(drop(2, [1, 2, 3, 4])) == [3, 4]
    assert list(drop(5, [1, 2])) == []
    assert list(drop(0, [1, 2])) == [1, 2]


def test_take_drop_on_count() -> None:
    xs = count(1)
    assert take(5, xs) == [1, 2, 3, 4, 5]
    assert take(3, xs) == [6, 7, 8]


def test_negative_n_raises() -> None:
    with pytest.raises(ValueError):
        take(-1, [1, 2, 3])
    with pytest.raises(ValueError):
        list(drop(-1, [1, 2, 3]))


def test_laziness_evaluation() -> None:
    eval_count = 0

    def side_effect_stream():
        nonlocal eval_count
        for i in count(1):
            eval_count += 1
            yield i

    stream = side_effect_stream()
    result = take(5, stream)
    assert result == [1, 2, 3, 4, 5]
    assert eval_count == 5


@given(st.integers(min_value=0, max_value=20))
def test_property_take_drop_count(n: int) -> None:
    stream = count(0)
    skipped = drop(n, stream)
    assert next(skipped) == n