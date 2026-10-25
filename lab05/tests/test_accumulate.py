from __future__ import annotations

from itertools import accumulate
import operator


def test_accumulate_basic() -> None:
    assert list(accumulate([1, 2, 3, 4])) == [1, 3, 6, 10]


def test_accumulate_mul() -> None:
    assert list(accumulate([1, 2, 3, 4], operator.mul)) == [1, 2, 6, 24]