"""Модель даних із повним відношенням порядку (Варіант 12: Навчальні онлайн-курси)."""

from __future__ import annotations

from functools import total_ordering
from typing import Any


@total_ordering
class CourseRank:
    """Представлення онлайн-курсу з підтримкою повного відношення лінійного порядку.

    Критерії порівняння за спаданням пріоритету:
    1. rating (вищий рейтинг -> кращий курс)
    2. students (більше студентів -> кращий курс)
    3. title (за абеткою, нижчий лексикографічний індекс -> кращий курс)
    """

    __slots__ = ("title", "category", "students", "rating", "price")

    def __init__(
        self,
        title: str,
        category: str,
        students: int,
        rating: float,
        price: float,
    ) -> None:
        self.title = title
        self.category = category
        self.students = students
        self.rating = rating
        self.price = price

    def __repr__(self) -> str:
        return (
            f"CourseRank({self.title!r}, {self.category!r}, "
            f"students={self.students}, rating={self.rating}, price={self.price})"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CourseRank):
            return NotImplemented
        return (self.rating, self.students, self.title) == (
            other.rating,
            other.students,
            other.title,
        )

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, CourseRank):
            return NotImplemented
        # Порядок: вищий рейтинг і кількість студентів є 'більшими' об'єктами
        return (-self.rating, -self.students, self.title) > (
            -other.rating,
            -other.students,
            other.title,
        )