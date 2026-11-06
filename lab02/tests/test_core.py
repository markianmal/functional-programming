"""
Лабораторна робота №2: Автоматизовані тести для перевірки чистоти функцій та HOF.
"""

from copy import deepcopy
import pytest
from core import (
    StockItem,
    compose,
    curried_price_multiplier,
    filter_pure,
    make_restock_processor,
    map_pure,
    process_warehouse_pure,
)


@pytest.fixture
def sample_stock() -> list[StockItem]:
    return [
        {
            "id": 101,
            "name": "Item A",
            "stock": 4,
            "price": 100.0,
            "min_stock": 15,
            "category": "Cat1",
        },
        {
            "id": 102,
            "name": "Item B",
            "stock": 25,
            "price": 50.0,
            "min_stock": 10,
            "category": "Cat2",
        },
        {
            "id": 103,
            "name": "Item C",
            "stock": 5,
            "price": 200.0,
            "min_stock": 20,
            "category": "Cat1",
        },
    ]


def test_referential_transparency(sample_stock: list[StockItem]) -> None:
    res1 = process_warehouse_pure(sample_stock)
    res2 = process_warehouse_pure(sample_stock)
    assert res1 == res2


def test_no_input_mutation(sample_stock: list[StockItem]) -> None:
    snapshot = deepcopy(sample_stock)
    process_warehouse_pure(sample_stock)
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


def test_custom_callable_policies(sample_stock: list[StockItem]) -> None:
    processor = make_restock_processor(
        should_restock=lambda it: it["stock"] < 10,
        calc_qty=lambda it: 10,
        discount_policy=lambda b, q: b * 0.8,
        tax_policy=lambda a: a,
    )
    res = processor(sample_stock)
    assert res["items_to_order_count"] == 2