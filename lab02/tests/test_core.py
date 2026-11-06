"""
Лабораторна робота №2: Автоматизовані тести для перевірки чистоти функцій та HOF.
"""

from copy import deepcopy
import pytest
from core import (
    StockItem,
    analyze_warehouse,
    compose,
    curried_price_multiplier,
    filter_pure,
    map_pure,
)


@pytest.fixture
def sample_stock() -> list[StockItem]:
    return [
        {
            "id": 1,
            "name": "Item A",
            "stock": 2,
            "price": 100.0,
            "min_stock": 10,
            "category": "Cat1",
        },
        {
            "id": 2,
            "name": "Item B",
            "stock": 15,
            "price": 50.0,
            "min_stock": 10,
            "category": "Cat2",
        },
        {
            "id": 3,
            "name": "Item C",
            "stock": 0,
            "price": 200.0,
            "min_stock": 5,
            "category": "Cat1",
        },
    ]


def test_referential_transparency(sample_stock: list[StockItem]) -> None:
    res1 = analyze_warehouse(sample_stock)
    res2 = analyze_warehouse(sample_stock)
    assert res1 == res2


def test_no_input_mutation(sample_stock: list[StockItem]) -> None:
    snapshot = deepcopy(sample_stock)
    analyze_warehouse(sample_stock)
    assert sample_stock == snapshot


def test_map_and_filter_pure(sample_stock: list[StockItem]) -> None:
    prices = map_pure(lambda x: x["price"], sample_stock)
    assert prices == [100.0, 50.0, 200.0]

    cat1_items = filter_pure(lambda x: x["category"] == "Cat1", sample_stock)
    assert len(cat1_items) == 2


def test_compose_function() -> None:
    add_five = lambda x: x + 5
    double = lambda x: x * 2
    add_then_double = compose(double, add_five)
    assert add_then_double(10) == 30


def test_curried_multiplier() -> None:
    ten_percent_increase = curried_price_multiplier(1.10)
    assert ten_percent_increase(100.0) == 110.0
    assert ten_percent_increase(50.0) == 55.0


def test_analyze_warehouse_filtering(sample_stock: list[StockItem]) -> None:
    summary = analyze_warehouse(
        sample_stock,
        category_filter=lambda cat: cat == "Cat1",
    )
    assert summary["total_items_count"] == 2
    assert summary["total_inventory_value"] == 200.0
    assert len(summary["items_needing_restock"]) == 2