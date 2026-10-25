"""Конвеєр функціональної обробки, partial та operator-селектори."""

from __future__ import annotations

from functools import partial, reduce
from operator import itemgetter, methodcaller
from typing import Any, Callable, Iterable

from models import CourseRank

# Оптимізовані селектори з модуля operator
get_title = itemgetter("title")
get_category = itemgetter("category")
get_students = itemgetter("students")
get_rating = itemgetter("rating")
get_price = itemgetter("price")

# Оптимізовані виклики методів рядків
strip = methodcaller("strip")
title_case = methodcaller("title")
lower_case = methodcaller("lower")


def pipeline(value: Any, *funcs: Callable[[Any], Any]) -> Any:
    """Послідовне пропускання значення крізь ланцюжок функцій через reduce."""
    return reduce(lambda acc, f: f(acc), funcs, value)


def mapf(fn: Callable[[Any], Any]) -> Callable[[Iterable[Any]], Any]:
    """Часткове застосування map для конвеєрів."""
    return partial(map, fn)


def filt(pred: Callable[[Any], bool]) -> Callable[[Iterable[Any]], Any]:
    """Часткове застосування filter для конвеєрів."""
    return partial(filter, pred)


def normalize_course(row: dict[str, Any]) -> CourseRank:
    """Нормалізація полів словника в типізований об'єкт CourseRank."""
    return CourseRank(
        title=title_case(strip(str(get_title(row)))),
        category=lower_case(strip(str(get_category(row)))),
        students=int(get_students(row)),
        rating=float(get_rating(row)),
        price=float(get_price(row)),
    )


def clean_and_rank_courses(
    raw_courses: Iterable[dict[str, Any]],
    min_rating: float = 4.5,
    top: int = 3,
) -> list[CourseRank]:
    """Конвеєр: нормалізація -> фільтрація за рейтингом -> сортування -> Top-N."""
    min_rating_pred = lambda c: c.rating >= min_rating
    top_n = lambda n: lambda it: list(it)[:n]

    return pipeline(
        raw_courses,
        mapf(normalize_course),
        filt(min_rating_pred),
        list,
        partial(sorted, reverse=True),
        top_n(top),
    )