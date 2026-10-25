from __future__ import annotations

from itertools import islice
from streams import drop, fib_stream, take


def test_first_10_fib() -> None:
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert list(islice(fib_stream(), 10)) == expected


def test_fib_drop_and_take() -> None:
    seq = fib_stream()
    result = take(8, drop(5, seq))
    assert result == [5, 8, 13, 21, 34, 55, 89, 144]