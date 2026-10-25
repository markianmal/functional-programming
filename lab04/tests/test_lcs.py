"""Тести варіанта 12."""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st
import pytest
from lcs import lcs_iterative, lcs_len_memo, lcs_len_naive, lcs_string


@pytest.mark.parametrize("func", [lcs_len_naive, lcs_len_memo, lcs_iterative])
def test_empty_cases(func) -> None:
    assert func("", "") == 0
    assert func("ABC", "") == 0
    assert func("", "XYZ") == 0


@pytest.mark.parametrize("func", [lcs_len_naive, lcs_len_memo, lcs_iterative])
def test_matching_and_disjoint(func) -> None:
    assert func("ABC", "ABC") == 3
    assert func("ABC", "DEF") == 0


def test_lcs_recovery() -> None:
    assert lcs_string("AGGTAB", "GXTXAYB") == "GTAB"
    assert lcs_string("ABCDE", "ACE") == "ACE"
    assert lcs_string("", "ABC") == ""


def test_type_error_raised() -> None:
    with pytest.raises(TypeError):
        lcs_len_memo(123, "ABC")  # type: ignore[arg-type]


def test_cache_metrics() -> None:
    lcs_len_memo("ABCDEF", "AZCXEF")
    info = lcs_len_memo._last_cache_info()  # type: ignore[attr-defined]
    assert info.hits > 0
    assert info.misses > 0
    lcs_len_memo._last_cache_clear()  # type: ignore[attr-defined]
    assert lcs_len_memo._last_cache_info().currsize == 0  # type: ignore[attr-defined]


@given(st.text(max_size=20), st.text(max_size=20))
def test_property_memo_equals_iterative(s1: str, s2: str) -> None:
    assert lcs_len_memo(s1, s2) == lcs_iterative(s1, s2)
    assert len(lcs_string(s1, s2)) == lcs_iterative(s1, s2)