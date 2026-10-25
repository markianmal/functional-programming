"""Базові будівельні блоки лінивих обчислень, генератори та утиліти itertools."""

from __future__ import annotations

from collections import deque
from itertools import count, islice
from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")


def fib_stream() -> Iterator[int]:
    """Нескінченний лінивий генератор чисел Фібоначчі: 0, 1, 1, 2, 3, 5, ..."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def naturals(start: int = 1) -> Iterator[int]:
    """Нескінченний потік натуральних чисел, починаючи зі start."""
    yield from count(start)


def take(n: int, it: Iterable[T]) -> list[T]:
    """Повертає перші n елементів ітерованого об'єкта у вигляді списку."""
    if n < 0:
        raise ValueError("n має бути невід'ємним числом")
    return list(islice(it, n))


def drop(n: int, it: Iterable[T]) -> Iterator[T]:
    """Ліниво пропускає перші n елементів ітерованого об'єкта."""
    if n < 0:
        raise ValueError("n має бути невід'ємним числом")
    iterator = iter(it)
    next(islice(iterator, n, n), None)
    return iterator


def sliding_window(it: Iterable[T], k: int) -> Iterator[tuple[T, ...]]:
    """Ліниве ковзне вікно розміру k на базі deque(maxlen=k)."""
    if k <= 0:
        raise ValueError("Розмір вікна k має бути строго додатним")

    iterator = iter(it)
    dq: deque[T] = deque(maxlen=k)

    for _ in range(k):
        try:
            dq.append(next(iterator))
        except StopIteration:
            return

    yield tuple(dq)

    for x in iterator:
        dq.append(x)
        yield tuple(dq)


def moving_average(it: Iterable[float | int], k: int) -> Iterator[float]:
    """Лінивий розрахунок простого рухомого середнього для вікна k."""
    for win in sliding_window(it, k):
        yield sum(win) / k