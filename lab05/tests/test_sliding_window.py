from __future__ import annotations

import pytest
from streams import moving_average, sliding_window


def test_sliding_window_basic() -> None:
    assert list(sliding_window([1, 2, 3, 4], 3)) == [(1, 2, 3), (2, 3, 4)]
    assert list(sliding_window(range(5), 2)) == [(0, 1), (1, 2), (2, 3), (3, 4)]


def test_sliding_window_k_greater_than_len() -> None:
    assert list(sliding_window([1, 2], 5)) == []


def test_sliding_window_invalid_k() -> None:
    with pytest.raises(ValueError):
        list(sliding_window([1, 2, 3], 0))
    with pytest.raises(ValueError):
        list(sliding_window([1, 2, 3], -2))


def test_sliding_window_empty() -> None:
    assert list(sliding_window([], 3)) == []


def test_moving_average() -> None:
    res = list(moving_average([10, 20, 30, 40], 2))
    assert res == [15.0, 25.0, 35.0]