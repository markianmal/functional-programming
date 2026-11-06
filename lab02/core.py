"""
Лабораторна робота №2: Вищі функції, лямбди та функціональні перетворення.
Варіант 12: Складський облік.
Чисте функціональне ядро без побічних ефектів та мутацій даних.
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


class ProcessedStockItem(TypedDict):
    id: int
    name: str
    category: str
    stock: int
    min_stock: int
    price: float
    total_value: float
    needs_restock: bool
    restock_qty: int


class StockSummary(TypedDict):
    total_items_count: int
    total_inventory_value: float
    categories_summary: dict[str, int]
    items_needing_restock: list[ProcessedStockItem]


# Функції вищого порядку (HOF) та комбінатори
def map_pure(fn: Callable[[A], B], items: Iterable[A]) -> list[B]:
    """Чиста версія map, що повертає новий список."""
    return [fn(item) for item in items]


def filter_pure(pred: Callable[[A], bool], items: Iterable[A]) -> list[A]:
    """Чиста версія filter, що повертає новий список."""
    return [item for item in items if pred(item)]


def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    """Композиція двох функцій: f(g(x))."""
    return lambda x: f(g(x))


def curried_price_multiplier(multiplier: float) -> Callable[[float], float]:
    """Каррована функція (каррування / closure) для перерахунку цін."""
    return lambda price: round(price * multiplier, 2)


# Трансформація складських позицій за допомогою лямбд та вищих функцій
def process_stock_item(item: StockItem) -> ProcessedStockItem:
    """Перетворює сирий StockItem у розширений ProcessedStockItem без мутацій."""
    stock = item["stock"]
    min_stock = item["min_stock"]
    price = item["price"]
    needs_restock = stock < min_stock
    restock_qty = max(0, min_stock - stock)
    total_value = round(stock * price, 2)

    return {
        "id": item["id"],
        "name": item["name"],
        "category": item["category"],
        "stock": stock,
        "min_stock": min_stock,
        "price": price,
        "total_value": total_value,
        "needs_restock": needs_restock,
        "restock_qty": restock_qty,
    }


def analyze_warehouse(
    items: Iterable[StockItem],
    *,
    category_filter: Callable[[str], bool] | None = None,
    price_adjuster: Callable[[float], float] | None = None,
) -> StockSummary:
    """
    Аналізує складські запаси за допомогою мапування, фільтрації та генераторів списків.
    Параметризована функціями-фільтрами та модифікаторами цін.
    """
    adjust_price = price_adjuster or (lambda p: p)

    # Нормалізація цін через map
    adjusted_items: list[StockItem] = map_pure(
        lambda it: {**it, "price": adjust_price(it["price"])}, items
    )

    # Фільтрація за категорією, якщо передано предикат
    filtered_items = (
        filter_pure(lambda it: category_filter(it["category"]), adjusted_items)
        if category_filter
        else adjusted_items
    )

    # Обробка кожної позиції через чистий map_pure
    processed_items = map_pure(process_stock_item, filtered_items)

    # Використання генераторів списків та агрегацій
    total_inventory_value = round(
        sum(item["total_value"] for item in processed_items), 2
    )

    # Фільтрація тих, що потребують дозамовлення
    needing_restock = filter_pure(lambda it: it["needs_restock"], processed_items)

    # Створення словника підсумків по категоріях через генератор словників
    categories = {it["category"] for it in processed_items}
    categories_summary = {
        cat: sum(1 for it in processed_items if it["category"] == cat)
        for cat in categories
    }

    return {
        "total_items_count": len(processed_items),
        "total_inventory_value": total_inventory_value,
        "categories_summary": categories_summary,
        "items_needing_restock": needing_restock,
    }