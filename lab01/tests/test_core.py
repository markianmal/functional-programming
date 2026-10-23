"""Модульні тести для перевірки вимог функціонального програмування."""

from copy import deepcopy
import pytest
from core import (
    StockItem,
    apply_standard_vat,
    build_restock_order,
    calc_bulk_discount,
    calc_restock_qty_to_min,
    compose,
    is_below_minimum,
    make_restock_processor,
    process_warehouse_pure,
)


@pytest.fixture
def sample_stock() -> list[StockItem]:
    return [
        {
            "id": 1,
            "name": "ESP32",
            "stock": 5,
            "price": 200.0,
            "min_stock": 15,
            "category": "Electronics",
        },
        {
            "id": 2,
            "name": "Servo SG90",
            "stock": 30,
            "price": 70.0,
            "min_stock": 20,
            "category": "Motors",
        },
        {
            "id": 3,
            "name": "Sensor HC-SR04",
            "stock": 2,
            "price": 80.0,
            "min_stock": 25,
            "category": "Sensors",
        },
    ]


def test_referential_transparency(sample_stock: list[StockItem]) -> None:
    """Перевірка детермінованості: однаковий вхід дає абсолютно тотожний вихід."""
    res1 = process_warehouse_pure(sample_stock)
    res2 = process_warehouse_pure(sample_stock)
    assert res1 == res2


def test_no_input_mutation(sample_stock: list[StockItem]) -> None:
    """Перевірка імутабельності: функція не змінює вхідний список або словники."""
    original_snapshot = deepcopy(sample_stock)
    _ = process_warehouse_pure(sample_stock)
    assert sample_stock == original_snapshot


def test_pure_functions_logic() -> None:
    """Тестування окремих чистих атомів бізнес-логіки."""
    item_deficit: StockItem = {
        "id": 1,
        "name": "Item A",
        "stock": 5,
        "price": 100.0,
        "min_stock": 10,
        "category": "Cat A",
    }
    item_sufficient: StockItem = {
        "id": 2,
        "name": "Item B",
        "stock": 15,
        "price": 100.0,
        "min_stock": 10,
        "category": "Cat B",
    }

    assert is_below_minimum(item_deficit) is True
    assert is_below_minimum(item_sufficient) is False
    assert calc_restock_qty_to_min(item_deficit) == 5
    assert calc_restock_qty_to_min(item_sufficient) == 0


def test_custom_callable_policies(sample_stock: list[StockItem]) -> None:
    """Перевірка параметризації через typing.Callable (інжекція власних політик)."""
    # Завжди дозамовляємо фіксовано 10 штук для товарів з залишком менше 10
    strict_filter = lambda it: it["stock"] < 10
    fixed_qty = lambda _: 10
    flat_discount = lambda base, _: base * 0.80  # 20% знижка на все
    zero_vat = lambda amount: amount  # без ПДВ

    custom_processor = make_restock_processor(
        should_restock=strict_filter,
        calc_qty=fixed_qty,
        discount_policy=flat_discount,
        tax_policy=zero_vat,
    )

    result = custom_processor(sample_stock)

    # Підходять позиції 1 (stock=5) та 3 (stock=2)
    assert result["items_to_order_count"] == 2
    assert result["total_units_to_order"] == 20

    # Позиція 1: base = 10 * 200 = 2000; discounted = 2000 * 0.8 = 1600; tax = 1600
    # Позиція 3: base = 10 * 80 = 800; discounted = 800 * 0.8 = 640; tax = 640
    # Разом: 1600 + 640 = 2240.0
    assert result["total_budget_needed"] == 2240.0


def test_function_composition() -> None:
    """Перевірка роботи функції compose."""
    add_ten = lambda x: x + 10
    multiply_two = lambda x: x * 2

    # f(g(x)) = (x * 2) + 10
    composed = compose(add_ten, multiply_two)
    assert composed(5) == 20