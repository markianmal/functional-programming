"""
Лабораторна робота №2: Вищі функції, лямбди та функціональні перетворення.
Варіант 12: Складський облік.
Чисте функціональне ядро без побічних ефектів та мутацій даних.
"""

from collections.abc import Callable, Iterable
from functools import partial, reduce
from typing import TypedDict, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class StockItem(TypedDict):
    id: int
    name: str
    stock: int
    price: float
    min_stock: int
    category: str


class RestockOrder(TypedDict):
    id: int
    name: str
    category: str
    order_qty: int
    unit_price: float
    base_cost: float
    discounted_cost: float
    final_cost: float


class RestockReport(TypedDict):
    items_to_order_count: int
    total_units_to_order: int
    total_budget_needed: float
    orders: list[RestockOrder]


# Аліаси типів функцій
NeedRestockFn = Callable[[StockItem], bool]
RestockQtyFn = Callable[[StockItem], int]
DiscountFn = Callable[[float, int], float]
TaxFn = Callable[[float], float]
ProcessorFn = Callable[[Iterable[StockItem]], RestockReport]


# 1. Функції вищого порядку (HOF) та комбінатори
def map_pure(fn: Callable[[A], B], items: Iterable[A]) -> list[B]:
    return list(map(fn, items))


def filter_pure(pred: Callable[[A], bool], items: Iterable[A]) -> list[A]:
    return list(filter(pred, items))


def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    return lambda x: f(g(x))


def multiply_price(multiplier: float, price: float) -> float:
    return round(price * multiplier, 2)


def curried_price_multiplier(multiplier: float) -> Callable[[float], float]:
    return partial(multiply_price, multiplier)


# 2. Чисті правила та предикати
def is_below_minimum(item: StockItem) -> bool:
    return item["stock"] < item["min_stock"]


def calc_restock_qty_to_min(item: StockItem) -> int:
    return max(0, item["min_stock"] - item["stock"])


def calc_bulk_discount(base_cost: float, qty: int) -> float:
    if qty >= 20:
        return round(base_cost * 0.90, 2)
    if qty >= 10:
        return round(base_cost * 0.95, 2)
    return round(base_cost, 2)


def apply_standard_vat(amount: float) -> float:
    return round(amount * 1.20, 2)


# 3. Побудова окремого замовлення без мутацій
def build_restock_order(
    item: StockItem,
    qty: int,
    apply_discount: DiscountFn,
    apply_tax: TaxFn,
) -> RestockOrder:
    base = round(qty * item["price"], 2)
    discounted = round(apply_discount(base, qty), 2)
    final = round(apply_tax(discounted), 2)

    return {
        "id": item["id"],
        "name": item["name"],
        "category": item["category"],
        "order_qty": qty,
        "unit_price": item["price"],
        "base_cost": base,
        "discounted_cost": discounted,
        "final_cost": final,
    }


# 4. Фабрика обробників дозамовлення
def make_restock_processor(
    *,
    should_restock: NeedRestockFn = is_below_minimum,
    calc_qty: RestockQtyFn = calc_restock_qty_to_min,
    discount_policy: DiscountFn = calc_bulk_discount,
    tax_policy: TaxFn = apply_standard_vat,
) -> ProcessorFn:
    def process(items: Iterable[StockItem]) -> RestockReport:
        filtered = list(filter(should_restock, items))

        orders = list(
            map(
                lambda item: build_restock_order(
                    item, calc_qty(item), discount_policy, tax_policy
                ),
                filtered,
            )
        )

        items_count = len(orders)
        total_units = reduce(lambda acc, o: acc + o["order_qty"], orders, 0)
        total_budget = round(
            reduce(lambda acc, o: acc + o["final_cost"], orders, 0.0), 2
        )

        return {
            "items_to_order_count": items_count,
            "total_units_to_order": total_units,
            "total_budget_needed": total_budget,
            "orders": orders,
        }

    return process


def process_warehouse_pure(items: Iterable[StockItem]) -> RestockReport:
    processor = make_restock_processor()
    return processor(items)