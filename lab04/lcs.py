"""Модуль обчислення довжини та відновлення рядка LCS."""

from __future__ import annotations

from functools import lru_cache


def lcs_len_naive(s1: str, s2: str) -> int:
    """Наївна рекурсивна довжина LCS: O(2^(n+m))."""
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Обидва аргументи мають бути рядками")

    def _rec(i: int, j: int) -> int:
        if i == len(s1) or j == len(s2):
            return 0
        if s1[i] == s2[j]:
            return 1 + _rec(i + 1, j + 1)
        return max(_rec(i + 1, j), _rec(i, j + 1))

    return _rec(0, 0)


def lcs_len_memo(s1: str, s2: str) -> int:
    """Мемоізована довжина LCS за станами (i, j): O(n * m)."""
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Обидва аргументи мають бути рядками")

    @lru_cache(maxsize=100_000)
    def _rec(i: int, j: int) -> int:
        if i == len(s1) or j == len(s2):
            return 0
        if s1[i] == s2[j]:
            return 1 + _rec(i + 1, j + 1)
        return max(_rec(i + 1, j), _rec(i, j + 1))

    res = _rec(0, 0)
    lcs_len_memo._last_cache_info = _rec.cache_info  # type: ignore[attr-defined]
    lcs_len_memo._last_cache_clear = _rec.cache_clear  # type: ignore[attr-defined]
    return res


def lcs_string(s1: str, s2: str) -> str:
    """Відновлення найдовшого спільного підрядка-підпослідовності (рекурсивно з мемоізацією)."""
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Обидва аргументи мають бути рядками")

    @lru_cache(maxsize=100_000)
    def _rec(i: int, j: int) -> str:
        if i == len(s1) or j == len(s2):
            return ""
        if s1[i] == s2[j]:
            return s1[i] + _rec(i + 1, j + 1)
        left = _rec(i + 1, j)
        right = _rec(i, j + 1)
        return left if len(left) >= len(right) else right

    return _rec(0, 0)


def lcs_iterative(s1: str, s2: str) -> int:
    """Ітеративна табуляція O(min(n, m)) пам'яті, безпечна для глибоких стеків."""
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Обидва аргументи мають бути рядками")

    if len(s1) < len(s2):
        s1, s2 = s2, s1

    prev = [0] * (len(s2) + 1)
    for ch1 in s1:
        curr = [0] * (len(s2) + 1)
        for j, ch2 in enumerate(s2, 1):
            if ch1 == ch2:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr

    return prev[len(s2)]