"""Поліморфний завантажувач джерел через functools.singledispatch."""

from __future__ import annotations

import csv
import io
import json
from functools import singledispatch
from pathlib import Path
from typing import Any


def _parse_raw_text(text: str, is_csv: bool = False) -> list[dict[str, Any]]:
    """Парсинг сирого текстового вмісту з автовизначенням формату."""
    s = text.strip()
    if is_csv or (not s.startswith(("[", "{")) and "," in s):
        reader = csv.DictReader(io.StringIO(s))
        return [dict(row) for row in reader]
    data = json.loads(s)
    if isinstance(data, dict):
        return [data]
    return list(data)


@singledispatch
def load_courses(src: Any) -> list[dict[str, Any]]:
    """Єдина точка входу для поліморфного завантаження курсів."""
    raise TypeError(f"Непідтримуваний тип джерела: {type(src)!r}")


@load_courses.register
def _(src: str) -> list[dict[str, Any]]:
    s = src.strip()
    if s.endswith(".csv"):
        return _parse_raw_text(Path(src).read_text(encoding="utf-8"), is_csv=True)
    if s.endswith(".json"):
        return _parse_raw_text(Path(src).read_text(encoding="utf-8"), is_csv=False)
    return _parse_raw_text(src)


@load_courses.register
def _(src: Path) -> list[dict[str, Any]]:
    is_csv = src.suffix.lower() == ".csv"
    return _parse_raw_text(src.read_text(encoding="utf-8"), is_csv=is_csv)


@load_courses.register
def _(src: io.TextIOBase) -> list[dict[str, Any]]:
    content = src.read()
    return _parse_raw_text(content)


@load_courses.register
def _(src: list) -> list[dict[str, Any]]:
    if src and not isinstance(src[0], dict):
        raise ValueError("Очікується список словників")
    return src