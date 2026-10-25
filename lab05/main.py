"""Точка входу: демонстрація генераторів, комбінаторів itertools та варіанта 12."""

from __future__ import annotations

from itertools import islice
from streams import drop, fib_stream, naturals, sliding_window, take
from triangular_numbers import triangular_differences, triangular_stream, triangular_up_to


def main() -> None:
    print("=== Лабораторна робота 5: Ліниві обчислення ===")
    print("1. Перші 10 чисел Фібоначчі:", take(10, fib_stream()))
    print("2. Пропуск 5, взяття 8 Фібоначчі:", take(8, drop(5, fib_stream())))

    win_demo = list(sliding_window([1, 2, 3, 4, 5], 3))
    print("3. Sliding window k=3 на [1,2,3,4,5]:", win_demo)

    triangles_10 = take(10, triangular_stream())
    print("4. Варіант 12. Перші 10 трикутних чисел:", triangles_10)

    triangles_limit = list(triangular_up_to(40))
    print("5. Варіант 12. Трикутні числа <= 40:", triangles_limit)

    diffs = list(triangular_differences(triangles_limit))
    print("6. Варіант 12. Різниці сусідніх значень:", diffs)


if __name__ == "__main__":
    main()