"""Налаштування тестового середовища та Hypothesis."""

import pytest
from hypothesis import HealthCheck, settings

settings.register_profile(
    "ci",
    max_examples=50,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.load_profile("ci")


@pytest.fixture(autouse=True)
def clear_caches() -> None:
    from algorithms import fib
    from lcs import _lcs_memo_rec, _lcs_str_rec

    fib.cache_clear()
    _lcs_memo_rec.cache_clear()
    _l