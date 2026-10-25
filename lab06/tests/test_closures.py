from __future__ import annotations

from closures import make_converter, make_counter, make_logger


def test_counter_state() -> None:
    c = make_counter(0)
    assert c() == 1
    assert c() == 2
    assert c() == 3


def test_counter_independent_instances() -> None:
    c1 = make_counter(10)
    c2 = make_counter(20)
    assert c1() == 11
    assert c2() == 21
    assert c1() == 12


def test_logger_closure() -> None:
    messages: list[str] = []
    log = make_logger("TEST", sink=messages.append)
    log("hello")
    assert messages == ["[TEST] hello"]


def test_converter_closure() -> None:
    c = make_converter(scale=2.5, precision=1)
    assert c(4.0) == 10.0
    assert c(3.33) == 8.3