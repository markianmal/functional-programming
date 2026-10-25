"""Модульні тести для перевірки коректності обчислення LCS."""

from __future__ import annotations

import pytest
from lcs import lcs_iterative, lcs_memo, lcs_naive


@pytest.mark.parametrize("func", [lcs_naive, lcs_memo, lcs_iterative])
def test_empty_cases(func) -> None:
    """Перевірка бази рекурсії та граничних випадків із порожніми рядками."""
    assert func("", "") == 0
    assert func("abc", "") == 0
    assert func("", "def") == 0


@pytest.mark.parametrize("func", [lcs_naive, lcs_memo, lcs_iterative])
def test_matching_and_disjoint(func) -> None:
    """Перевірка повного збігу та повної відсутності спільних символів."""
    assert func("pytest", "pytest") == 6
    assert func("abc", "xyz") == 0


@pytest.mark.parametrize("func", [lcs_naive, lcs_memo, lcs_iterative])
def test_standard_subsequences(func) -> None:
    """Перевірка на типових підпослідовностях."""
    assert func("AGGTAB", "GXTXAYB") == 4  # GTAB
    assert func("ABCDE", "ACE") == 3       # ACE
    assert func("ABCBDAB", "BDCAB") == 4   # BCAB / BDAB


def test_parity_between_memo_and_iterative() -> None:
    """Порівняння результатів мемоізованої та ітеративної версій на довших рядках."""
    s1 = "DYNAMIC_PROGRAMMING_AND_RECURSION"
    s2 = "MEMOIZATION_WITH_LRU_CACHE_TEST"
    assert lcs_memo(s1, s2) == lcs_iterative(s1, s2)


def test_lru_cache_behavior() -> None:
    """Демонстрація та валідація кешування станів (cache_info)."""
    s1 = "BANANA"
    s2 = "ATANA"
    lcs_memo(s1, s2)

    cache_info = lcs_memo._last_cache_info()  # type: ignore[attr-defined]
    assert cache_info.hits > 0
    assert cache_info.misses > 0

    lcs_memo._last_cache_clear()  # type: ignore[attr-defined]
    cleared_info = lcs_memo._last_cache_info()  # type: ignore[attr-defined]
    assert cleared_info.currsize == 0