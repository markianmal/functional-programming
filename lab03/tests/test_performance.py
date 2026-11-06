"""Порівняння мутабельного підходу та незмінних структур (Benchmark)."""
import time
from model import Ingredient
from core import calculate_margin_cached


def test_mutable_vs_immutable_operations(benchmark=None) -> None:
    # 1. Мутабельний список
    mut_start = time.perf_counter()
    mut_items = []
    for i in range(10_000):
        mut_items.append({"name": f"Item_{i}", "cost": float(i), "weight": 10.0})
    mut_time = time.perf_counter() - mut_start

    # 2. Незмінні tuple / frozen сутності
    immut_start = time.perf_counter()
    immut_items = tuple(
        Ingredient(name=f"Item_{i}", cost=float(i), weight_grams=10.0)
        for i in range(10_000)
    )
    immut_time = time.perf_counter() - immut_start

    assert len(mut_items) == len(immut_items) == 10_000
    assert immut_time >= 0.0
    assert mut_time >= 0.0


def test_cached_margin_benchmark() -> None:
    calculate_margin_cached.cache_clear()
    for _ in range(5000):
        calculate_margin_cached(250.0, 100.0)
    assert calculate_margin_cached.cache_info().hits == 4999