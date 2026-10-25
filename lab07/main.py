"""Точка входу: демонстрація роботи конвеєра, завантажувача та models."""

from __future__ import annotations

from operator import attrgetter
from pathlib import Path

from core import clean_and_rank_courses
from loaders import load_courses
from models import CourseRank


def main() -> None:
    print("=== Лабораторна робота 7: functools та operator ===")

    json_path = Path("sample_courses.json")
    courses_from_json = load_courses(json_path)
    ranked = clean_and_rank_courses(courses_from_json, min_rating=4.5, top=3)

    print(f"Top-{len(ranked)} курсів за популярністю та рейтингом:")
    for rank, c in enumerate(ranked, 1):
        print(
            f"  {rank}. {c.title} ({c.category}) - "
            f"Рейтинг: {c.rating}, Студентів: {c.students}, Ціна: ${c.price}"
        )

    csv_path = Path("sample_courses.csv")
    courses_from_csv = load_courses(csv_path)
    ranked_csv = clean_and_rank_courses(courses_from_csv, min_rating=4.5, top=2)
    print(f"\nTop-{len(ranked_csv)} курсів з CSV-файлу:")
    for rank, c in enumerate(ranked_csv, 1):
        print(f"  {rank}. {c.title} - {c.rating} зірок ({c.students} учнів)")

    c1 = CourseRank("Python Pro", "dev", 1500, 4.9, 50.0)
    c2 = CourseRank("Python Basic", "dev", 1200, 4.8, 30.0)
    print(f"\nПорівняння total_ordering: c1 > c2 -> {c1 > c2} (c1 == c2 -> {c1 == c2})")
    print(f"Вибірка через attrgetter: {attrgetter('title', 'rating')(c1)}")


if __name__ == "__main__":
    main()