"""Базові та варіативні замикання (closures) із утриманням стану."""

from __future__ import annotations

from typing import Callable


def make_counter(start: int = 0) -> Callable[[], int]:
    """Замикання зі змінним станом лічильника через nonlocal."""
    value = start

    def inc() -> int:
        nonlocal value
        value += 1
        return value

    return inc


def make_logger(
    prefix: str,
    sink: Callable[[str], None] = print,
) -> Callable[[str], None]:
    """Ін'єкція залежностей через замикання без мутації стану."""

    def log(msg: str) -> None:
        sink(f"[{prefix}] {msg}")

    return log


def make_converter(scale: float, precision: int = 2) -> Callable[[float], float]:
    """Замикання параметрів конвертації даних (Варіант 12)."""

    def converter(val: float) -> float:
        return round(val * scale, precision)

    return converter