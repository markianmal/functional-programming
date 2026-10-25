"""Модуль обчислення довжини та відновлення найдовшої спільної підпослідовності (LCS)."""

from __future__ import annotations

from functools import lru_cache


def lcs_naive(s1: str, s2: str) -> int:
    """Наївна рекурсивна реалізація LCS без кешування.

    Складність: O(2^(n+m)), глибина стеку: O(n + m).
    """

    def _rec(i: int, j: int) -> int:
        # База рекурсії: вихід за межі будь-якого з рядків
        if i == len(s1) or j == len(s2):
            return 0

        # Крок рекурсії
        if s1[i] == s2[j]:
            return 1 + _rec(i + 1, j + 1)
        return max(_rec(i + 1, j), _rec(i, j + 1))

    return _rec(0, 0)


def lcs_memo(s1: str, s2: str) -> int:
    """Рекурсивна реалізація LCS із мемоізацією станів через lru_cache.

    Складність: O(n * m), глибина стеку: O(n + m).
    """

    @lru_cache(maxsize=None)
    def _rec(i: int, j: int) -> int:
        # База рекурсії
        if i == len(s1) or j == len(s2):
            return 0

        # Крок рекурсії
        if s1[i] == s2[j]:
            return 1 + _rec(i + 1, j + 1)
        return max(_rec(i + 1, j), _rec(i, j + 1))

    res = _rec(0, 0)
    # Зберігаємо доступ до cache_info/clear для аналізу
    lcs_memo._last_cache_info = _rec.cache_info  # type: ignore[attr-defined]
    lcs_memo._last_cache_clear = _rec.cache_clear  # type: ignore[attr-defined]
    return res


def lcs_iterative(s1: str, s2: str) -> int:
    """Ітеративна реалізація LCS (Bottom-Up Tabulation).

    Часова складність: O(n * m), просторова складність: O(min(n, m)).
    Безпечна для глибоких послідовностей (не залежить від ліміту стека викликів).
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    # dp[j] зберігає LCS для поточного підрядка другого рядка
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