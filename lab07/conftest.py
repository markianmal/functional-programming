"""Конфігурація pytest та Hypothesis."""

from hypothesis import HealthCheck, settings

settings.register_profile(
    "ci",
    max_examples=40,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.load_profile("ci")