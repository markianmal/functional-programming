"""Модуль обчислення LCS: рекурсія, lru_cache та ітеративна табуляція."""

from __future__ import annotations

from functools import lru_cache


def lcs_len_naive(s1: str, s2: str) -> int:
    """Наївна рекурсивна реалізація без кешу: O(2^(n+m))."""
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Аргументи повинні бути рядками")

    def _rec(i: int, j: int) -> int:
        if i == len(s1) or j == len(s2):
            return 0
        if s1[i] == s2[j]:
            return 1 + _rec(i + 1, j + 1)
        return max(_rec(i + 1, j), _rec(i, j + 1))

    return _rec(0, 0)


@lru_cache(maxsize=100_000)
def _lcs_memo_rec(s1: str, s2: str, i: int, j: int) -> int:
    if i == len(s1) or j == len(s2):
        return 0
    if s1[i] == s2[j]:
        return 1 + _lcs_memo_rec(s1, s2, i + 1, j + 1)
    return max(_lcs_memo_rec(s1, s2, i + 1, j), _lcs_memo_rec(s1, s2, i, j + 1))


def lcs_len(s1: str, s2: str) -> int:
    """Довжина LCS із застосуванням functools.lru_cache: O(n * m)."""
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Аргументи повинні бути рядками")
    return _lcs_memo_rec(s1, s2, 0, 0)


def lcs_memo(s1: str, s2: str) -> int:
    """Аліас для сумісності з автотестами."""
    return lcs_len(s1, s2)


@lru_cache(maxsize=100_000)
def _lcs_str_rec(s1: str, s2: str, i: int, j: int) -> str:
    if i == len(s1) or j == len(s2):
        return ""
    if s1[i] == s2[j]:
        return s1[i] + _lcs_str_rec(s1, s2, i + 1, j + 1)
    left = _lcs_str_rec(s1, s2, i + 1, j)
    right = _lcs_str_rec(s1, s2, i, j + 1)
    return left if len(left) >= len(right) else right


def lcs_string(s1: str, s2: str) -> str:
    """Відновлення найдовшої спільної підпослідовності у вигляді рядка."""
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Аргументи повинні бути рядками")
    return _lcs_str_rec(s1, s2, 0, 0)


def lcs_iterative(s1: str, s2: str) -> int:
    """Ітеративна версія (bottom-up): O(n * m) часу, O(min(n, m)) пам'яті."""
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Аргументи повинні бути рядками")

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