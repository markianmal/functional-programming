"""Варіант 12: Лінивий потік трикутних чисел, фільтрація та ковзні різниці."""

from __future__ import annotations

from itertools import accumulate, count, takewhile
from typing import Iterable, Iterator

from streams import sliding_window


def triangular_stream() -> Iterator[int]:
    """Нескінченний лінивий потік трикутних чисел T_n = 1 + 2 + ... + n: 1, 3, 6, 10, 15, ...

    Реалізовано через поєднання itertools.count та itertools.accumulate.
    """
    yield from accumulate(count(1))


def triangular_stream_gen() -> Iterator[int]:
    """Альтернативний генератор із yield для перевірки паритету та лінивості."""
    total = 0
    for n in count(1):
        total += n
        yield total


def triangular_up_to(limit: int) -> Iterator[int]:
    """Лінивий відбір трикутних чисел, значення яких не перевищують limit."""
    return takewhile(lambda x: x <= limit, triangular_stream())


def triangular_differences(it: Iterable[int]) -> Iterator[int]:
    """Обчислення різниць між сусідніми елементами за допомогою sliding_window(k=2).

    Для послідовності трикутних чисел різниці T_n - T_(n-1) відновлюють послідовність 2, 3, 4, ...
    """
    for prev, curr in sliding_window(it, 2):
        yield curr - prev