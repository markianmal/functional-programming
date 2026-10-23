"""Чисте функціональне ядро для складського обліку (Варіант 12).

Повністю ізольоване від I/O, глобального стану та мутацій вхідних даних.
"""

from collections.abc import Callable, Iterable
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


# Аліаси типів для параметризації через Callable
NeedRestockFn = Callable[[StockItem], bool]
RestockQtyFn = Callable[[StockItem], int]
DiscountFn = Callable[[float, int], float]
TaxFn = Callable[[float], float]
ProcessorFn = Callable[[Iterable[StockItem]], RestockReport]


def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    """Математична композиція функцій: (f ∘ g)(x) = f(g(x))."""
    return lambda x: f(g(x))


def is_below_minimum(item: StockItem) -> bool:
    """Чистий предикат: чи опустився залишок нижче мінімального запасу."""
    return item["stock"] < item["min_stock"]


def calc_restock_qty_to_min(item: StockItem) -> int:
    """Чисте обчислення дефіциту до мінімального рівня."""
    return max(0, item["min_stock"] - item["stock"])


def calc_bulk_discount(base_cost: float, qty: int) -> float:
    """Політика оптової знижки: 10% знижки при замовленні від 20 одиниць."""
    if qty >= 20:
        return base_cost * 0.90
    if qty >= 10:
        return base_cost * 0.95
    return base_cost


def apply_standard_vat(amount: float) -> float:
    """Політика ПДВ: нарахування 20% податку."""
    return amount * 1.20


def build_restock_order(
    item: StockItem,
    qty: int,
    apply_discount: DiscountFn,
    apply_tax: TaxFn,
) -> RestockOrder:
    """Створює новий незмінний запис RestockOrder без мутації вихідного об'єкта."""
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


def make_restock_processor(
    *,
    should_restock: NeedRestockFn,
    calc_qty: RestockQtyFn,
    discount_policy: DiscountFn,
    tax_policy: TaxFn,
) -> ProcessorFn:
    """Функція вищого порядку (фабрика), яка конфігурує пайплайн обробки складу."""

    def process(items: Iterable[StockItem]) -> RestockReport:
        filtered = [item for item in items if should_restock(item)]

        orders: list[RestockOrder] = [
            build_restock_order(
                item=item,
                qty=calc_qty(item),
                apply_discount=discount_policy,
                apply_tax=tax_policy,
            )
            for item in filtered
        ]

        total_units = sum(order["order_qty"] for order in orders)
        total_budget = round(sum(order["final_cost"] for order in orders), 2)

        return {
            "items_to_order_count": len(orders),
            "total_units_to_order": total_units,
            "total_budget_needed": total_budget,
            "orders": orders,
        }

    return process


def process_warehouse_pure(
    items: Iterable[StockItem],
    *,
    should_restock: NeedRestockFn = is_below_minimum,
    calc_qty: RestockQtyFn = calc_restock_qty_to_min,
    discount_policy: DiscountFn = calc_bulk_discount,
    tax_policy: TaxFn = apply_standard_vat,
) -> RestockReport:
    """Прямий чистий інтерфейс виклику з дефолтними політиками."""
    processor = make_restock_processor(
        should_restock=should_restock,
        calc_qty=calc_qty,
        discount_policy=discount_policy,
        tax_policy=tax_policy,
    )
    return processor(items)