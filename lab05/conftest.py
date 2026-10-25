"""Конфігурація pytest та Hypothesis."""

import pytest
from hypothesis import HealthCheck, settings

settings.register_profile(
    "ci",
    max_examples=50,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.load_profile("ci")


@pytest.fixture
def sample_naturals() -> list[int]:
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]