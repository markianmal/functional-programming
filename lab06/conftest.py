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
def fake_clock():
    ticks = [0.0, 0.012345, 0.05, 0.1]

    def _clock() -> float:
        return ticks.pop(0) if ticks else 1.0

    return _clock